from django.urls import path

from quotes import views


app_name = "quotes"


urlpatterns = [
    path("create/", views.CreateQuoteView.as_view(), name="create"),
    path("<slug:pk>/", views.QuoteDetailView.as_view(), name="by_id"),
    path("edit/<slug:pk>/", views.EditQuoteView.as_view(), name="edit"),
    path("delete/<slug:pk>/", views.DeleteQuoteView.as_view(), name="delete"),
    path("<slug:pk>/reaction/<int:reaction>/", views.SetReactionView.as_view(), name="set_reaction"),
    path("<slug:pk>/favourite/", views.AddToFavouritesView.as_view(), name="favourite"),
]
