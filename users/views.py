from django.conf import settings
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.signing import TimestampSigner, BadSignature
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from users.forms import SignUpForm, UpdateProfileForm, UserUpdateForm
from users.models import Profile


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, gettext("logout_success"))


class MessagedLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy("index")
    success_message = gettext("login_success")


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save()
        instance.is_active = False
        instance.save()
        Profile.objects.create(user=instance)
        token = TimestampSigner().sign(form.cleaned_data['username'])
        link = request.build_absolute_uri(reverse_lazy('users:activate', args=(token,)))
        send_mail(
            subject="Verification email",
            message=f"Welcome! For activate your account,"
                    f" go to:\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.cleaned_data["email"]],
        )
        messages.success(request, gettext("user_created"))
        return redirect(reverse("users:login"))
    return render(
        request,
        "users/signup.html",
        {"form": form},
    )


@login_required(login_url=reverse_lazy("users:login"))
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, gettext("profile_updated"))
            return redirect(reverse("users:profile_edit"))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "users/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def activate(request, username):
    try:
        username = TimestampSigner().unsign(username)
    except BadSignature:
        messages.error(request, gettext("bad_activate_link"))
        return redirect("index")
    user = User.objects.get(username=username)
    if user.is_active:
        messages.error(request, gettext("user_is_active"))
        return redirect("index")
    user.is_active = True
    messages.success(request, gettext("account_activated"))
    user.save()
    return redirect(reverse("users:login"))


class WatchProfileView(TemplateView):
    template_name = "users/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(User.objects.select_related("profile"), username=self.kwargs["username"])
        if not context["profile"]:
            return HttpResponseNotFound()
        context["num_quotes"] = context["profile"].quotes.count()
        context["num_fav"] = context["profile"].profile.favourites.count()
        context["my"] = context["profile"].pk == self.request.user.pk
        context["quotes"] = context["profile"].quotes.all()[:4]
        return context
