from django.urls import path
from .views import hello_world, MoviesView, MovieView, SearchView, InfoView

urlpatterns = [
    path('', hello_world),
    path('movies/', MoviesView.as_view()),
    path('movies/<int:tmdb_id>/', MovieView.as_view()),
    path('search/', SearchView.as_view()),
    path('info/<int:id>/', InfoView.as_view())
]