from django.urls import path

from search.views import Overview, SearchView


app_name = "search"


urlpatterns = [
    path("overview/", Overview.as_view(), name="overview"),
    path("", SearchView.as_view(), name="by"),
]
