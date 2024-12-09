from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import gettext_lazy as _

from quotes.models import Quote

DjangoUser._meta.get_field('email')._unique = True


def max_size_validator(obj):
    print(obj.file.size )
    if obj and obj.file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f'{_("filesize_limit_increased")} ({settings.MAX_FILE_SIZE_MB} MB)')


class Profile(models.Model):
    user = models.OneToOneField(
        DjangoUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="день рождения",)
    about = models.TextField(verbose_name="обо мне", null=True, blank=True, max_length=1000)
    image = models.ImageField(
        upload_to="uploads/profile_pics/",
        null=True,
        blank=True,
        verbose_name="изображение профиля",
        validators=[max_size_validator],
    )
    favourites = models.ManyToManyField(Quote, blank=True, related_name="favourites", verbose_name="избранное")

    class Meta:
        verbose_name = "Профиль"
