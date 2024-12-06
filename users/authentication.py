from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        mail_user = self.by_mail(username)
        name_user = self.by_username(username)
        user: User | bool = False
        if name_user:
            user = name_user
        elif mail_user:
            user = mail_user
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def by_mail(mail):
        try:
            return User.objects.get(email=mail)
        except User.DoesNotExist:
            return False

    @staticmethod
    def by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return False
