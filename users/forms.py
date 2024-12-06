from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, User, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from users.models import Profile


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('email_or_username')


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["birthday"].widget = forms.SelectDateWidget(
            years=range(1900, datetime.now().year + 1),
        )

    class Meta:
        model = Profile
        fields = (
            "birthday",
            "about",
            "image",
        )
