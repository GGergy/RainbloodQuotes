from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings

from rainblood_quotes.sitemaps import StaticSitemap, QuoteSitemap, ProfileSitemap
from rainblood_quotes.views import HomepageView


sitemaps = {
    "static": StaticSitemap,
    "quotes": QuoteSitemap,
    "users": ProfileSitemap,
}

urlpatterns = [
    path("", HomepageView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path("quotes/", include("quotes.urls")),
    path("users/", include("users.urls")),
    path("search/", include("search.urls")),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("favicon.ico/", RedirectView.as_view(url="/static/img/fav/favicon.ico", permanent=True)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
