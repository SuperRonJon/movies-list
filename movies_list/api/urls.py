from django.urls import path
from .views.movies import hello_world, MoviesView, MovieView, SearchView, InfoView
from .views.tags import TagsView, TagMovieView, TagRemoveView, TagUniqueView, TagBulkView
from .views.collections import CollectionsView, CollectionMoviesView, CollectionTagsView, CollectionDeleteView

urlpatterns = [
    path('', hello_world),
    # Movie Routes
    path('movies/', MoviesView.as_view()),
    path('movies/<int:pk>/', MovieView.as_view()),

    # TMDB Routes
    path('search/', SearchView.as_view()),
    path('info/<int:id>/', InfoView.as_view()),

    # Tag Routes
    path('tags/', TagsView.as_view()),
    path('movies/<int:movie>/tags/', TagMovieView().as_view()),
    path('tags/<int:pk>/', TagRemoveView.as_view()),
    path('tags/unique/', TagUniqueView.as_view()),
    path('tags/bulk/', TagBulkView.as_view()),

    # Collection Routes
    path('collections/', CollectionsView.as_view()),
    path('collections/<int:collection_id>/movies/', CollectionMoviesView.as_view()),
    path('collections/<int:collection_id>/tags/', CollectionTagsView.as_view()),
    path('collections/<int:pk>/', CollectionDeleteView.as_view()),
]