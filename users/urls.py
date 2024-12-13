from django.contrib.auth import views
from django.urls import path, reverse_lazy

import users.views
from users import forms

app_name = "users"

urlpatterns = [
    path(
        "login/",
        users.views.MessagedLoginView.as_view(form_class=forms.LoginForm,),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("signup/", users.views.signup, name="signup"),
    path("profile/edit/", users.views.update_profile, name="profile_edit"),
    path("profiles/<username>/", users.views.WatchProfileView.as_view(), name="profile"),
    path("activate/<username>/", users.views.activate, name="activate"),
]
