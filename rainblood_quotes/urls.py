from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from rainblood_quotes.sitemaps import StaticSitemap, QuoteSitemap, ProfileSitemap


sitemaps = {
    "static": StaticSitemap,
    "quotes": QuoteSitemap,
    "users": ProfileSitemap,
}

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path('admin/', admin.site.urls),
    path("quotes/", include("quotes.urls")),
    path("users/", include("users.urls")),
    path("search/", include("search.urls")),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
