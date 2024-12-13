from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from quotes.models import Quote
from users.models import Profile


class QuoteSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return Quote.objects.all().order_by('id')

    @staticmethod
    def lastmod(obj):
        return obj.updated_at


class ProfileSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Profile.objects.all().order_by('id')

    @staticmethod
    def lastmod(obj):
        return obj.updated_at


class StaticSitemap(Sitemap):

    def items(self):
        return ["search:overview", "index"]

    def location(self, item):
        return reverse(item)
