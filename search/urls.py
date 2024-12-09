from django.urls import path

from search.views import Overview, SearchView, FavView


app_name = "search"


urlpatterns = [
    path("overview/", Overview.as_view(), name="overview"),
    path("my_fav/", FavView.as_view(), name="my_fav"),
    path("", SearchView.as_view(), name="by"),
]
