import datetime

from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, FormView, UpdateView, DeleteView, View

from quotes.forms import QuoteForm
from quotes.models import Quote, Rate


def to_seconds(time: datetime.time):
    return time.hour * 60 + time.minute


def from_seconds(time: int):
    return datetime.time(hour=time // 60, minute=time % 60)


class CreateQuoteView(FormView, LoginRequiredMixin):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/create.html"
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = self.model.objects.create(author=self.request.user, video=form.cleaned_data['video'],
                                            title=form.cleaned_data['title'],
                                            full_text=form.cleaned_data['full_text'],
                                            time=to_seconds(form.cleaned_data['time']))
            self.success_url = reverse_lazy("quotes:by_id", args=[obj.id])
            messages.success(self.request, _("quote_created"))
        return super().post(request, *args, **kwargs)


class QuoteDetailView(DetailView):
    model = Quote
    template_name = "quotes/quote.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my"] = self.get_object().author.pk == self.request.user.pk
        context["duration"] = from_seconds(self.get_object().time)
        context["reaction"] = Rate.objects.filter(quote=self.get_object(), user=self.request.user.id).first()
        return context


class EditQuoteView(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/update.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if hasattr(self, "object"):
            form.fields["time"].initial = from_seconds(self.object.time)
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = self.get_object()
            obj.time = to_seconds(form.cleaned_data["time"])
            obj.save()
            self.success_url = reverse_lazy("quotes:by_id", args=[obj.id])
            messages.success(self.request, _("quote_updated"))
        return super().post(request, *args, **kwargs)


class DeleteQuoteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy("search:overview")
    template_name = "quotes/confirm_delete.html"
    success_message = _("quote_deleted")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj


class SetReactionView(LoginRequiredMixin, View):
    success_message = _("reaction_set")

    def post(self, request, *args, **kwargs):
        quote = get_object_or_404(Quote.objects.only("id"), pk=self.kwargs.get("pk"))
        rate = Rate.objects.filter(quote__id=kwargs["pk"], user=self.request.user).first()
        if self.kwargs.get("reaction") not in [0, 1]:
            raise BadRequest()
        value = Rate.Values.like if self.kwargs.get("reaction") == 1 else Rate.Values.dislike
        if rate:
            if rate.value == value:
                rate.delete()
                messages.success(self.request, _("reaction_removed"))
            else:
                rate.value = value
                rate.save()
                messages.success(self.request, _("reaction_set"))
        else:
            Rate.objects.create(quote=quote, value=value, user=self.request.user)
            messages.success(self.request, _("reaction_set"))
        return redirect(reverse("quotes:by_id", args=[quote.id]))


class AddToFavouritesView(SuccessMessageMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quote = get_object_or_404(Quote.objects.only("id"), pk=self.kwargs.get("pk"))
        if quote not in request.user.profile.favourites.all():
            request.user.profile.favourites.add(quote)
            messages.success(self.request, _("fav_set"))
        else:
            request.user.profile.favourites.remove(quote)
            messages.success(self.request, _("fav_removed"))
        return redirect(reverse("quotes:by_id", args=[quote.id]))