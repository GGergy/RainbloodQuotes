import datetime

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView, FormView, UpdateView, DeleteView

from quotes.forms import QuoteForm
from quotes.models import Quote


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
