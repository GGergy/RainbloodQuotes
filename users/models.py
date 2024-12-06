from django.db import models
from django.contrib.auth.models import User as DjangoUser

from quotes.models import Quote

DjangoUser._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(
        DjangoUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="день рождения",)
    about = models.TextField(verbose_name="обо мне", null=True, blank=True,)
    image = models.ImageField(
        upload_to="uploads/profile_pics/",
        null=True,
        blank=True,
        verbose_name="изображение профиля",
    )
    favourites = models.ManyToManyField(Quote, blank=True, related_name="favourites", verbose_name="избранное")

    class Meta:
        verbose_name = "Профиль"
