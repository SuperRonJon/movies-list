from django.urls import path
from .views import hello_world, MoviesView, MovieView, SearchView, InfoView, TagsView, TagMovieView, TagRemoveView, TagUniqueView, TagBulkView

urlpatterns = [
    path('', hello_world),
    path('movies/', MoviesView.as_view()),
    path('movies/<int:tmdb_id>/', MovieView.as_view()),
    path('search/', SearchView.as_view()),
    path('info/<int:id>/', InfoView.as_view()),
    path('tags/', TagsView.as_view()),
    path('movies/<int:movie>/tags/', TagMovieView().as_view()),
    path('tags/<int:pk>/', TagRemoveView.as_view()),
    path('tags/unique/', TagUniqueView.as_view()),
    path('tags/bulk/', TagBulkView.as_view()),
]