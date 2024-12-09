import re

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


def simplify(item: str) -> str:
    if not item:
        return item
    item = item.strip().lower()
    item = re.sub(r'\W', '', item)
    item = re.sub(r'\s+', ' ', item)
    new = item[0]
    for letter in item[1:]:
        if new[-1] != letter:
            new += letter
    return new


class Video(models.Model):
    youtube_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='uploads/videos/')

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class QuoteObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("rate").annotate(rating=models.Sum("rate__value", default=0))


class Quote(models.Model):
    objects = QuoteObjectManager()
    title = models.CharField(max_length=100, verbose_name="заголовок")
    full_text = models.TextField(verbose_name="полный текст", max_length=1000)
    time = models.PositiveIntegerField(verbose_name="временная метка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes', verbose_name="автор")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='quotes', verbose_name="видео")
    created_at = models.DateTimeField(auto_now_add=True)
    search_string = models.TextField(verbose_name="строка поиска")

    def full_clean(self, *args, **kwargs):
        self.search_string = simplify(self.title + " " + self.full_text)
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.search_string:
            self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return self.title


class Rate(models.Model):
    class Values(models.IntegerChoices):
        like = 1, _("like")
        dislike = -1, _("dislike")

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="rate")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rate")
    value = models.IntegerField(choices=Values.choices, verbose_name="оценка")

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
        unique_together = ('quote', 'user')

    def __str__(self):
        return f"{self.quote} - {self.user} - {self.value}"
