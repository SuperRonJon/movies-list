from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Collection, Movie, Tag
from ..serializers import CollectionSerializer, MovieSerializer, TagSerializer


class CollectionsView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionDeleteView(generics.DestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionMoviesView(APIView):
    def get(self, request, collection_id):
        movies = Movie.objects.filter(collection__exact=collection_id)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class CollectionTagsView(APIView):
    def get(self, request, collection_id):
        tags = Tag.objects.filter(collection__exact=collection_id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
