from rest_framework import generics, status
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
        collections = Collection.objects.filter(id__exact=collection_id)
        if len(collections) == 0:
            return Response({"message": "Collection does not exist"}, status=status.HTTP_404_NOT_FOUND)
        movies = Movie.objects.filter(collection__exact=collection_id)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class CollectionTagsView(APIView):
    def get(self, request, collection_id):
        collections = Collection.objects.filter(id__exact=collection_id)
        if len(collections) == 0:
            return Response({"message": "Collection does not exist"}, status=status.HTTP_404_NOT_FOUND)
        tags = Tag.objects.filter(collection__exact=collection_id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class CollectionExportView(APIView):
    def get(self, request, collection_id):
        collections = Collection.objects.filter(id__exact=collection_id)
        if len(collections) == 0:
            return Response({"message": "Collection does not exist"}, status=status.HTTP_404_NOT_FOUND)
        movies = Movie.objects.filter(collection__exact=collection_id)
        movie_serializer = MovieSerializer(movies, many=True)
        results = []
        for movie in movie_serializer.data:
            tags = Tag.objects.filter(movie__exact=movie['id'])
            tag_serializer = TagSerializer(tags, many=True)
            movie['tags'] = tag_serializer.data
            results.append(movie)
        return Response(results)
    
    def post(self, request, collection_id):
        # Ensure the collection exists
        collections = Collection.objects.filter(id__exact=collection_id)
        data_added = []
        if len(collections) == 0:
            return Response({"message": "Collection does not exist"}, status=status.HTTP_404_NOT_FOUND)
        for movie in request.data:
            # If the movie is not in the collection, add it
            to_return = {}
            movie_data = {
                "title": movie['title'],
                "tmdb_id": movie['tmdb_id'],
                "popularity": movie['popularity'],
                "release_date": movie['release_date'],
                "overview": movie['overview'],
                "poster_path": movie['poster_path'],
                "collection": collection_id
            }
            movies = Movie.objects.filter(tmdb_id__exact=movie_data['tmdb_id'], collection__exact=movie_data['collection'])
            if len(movies) == 0:
                movie_serializer = MovieSerializer(data=movie_data)
                if movie_serializer.is_valid():
                    movie_serializer.save()
                    to_return = movie_serializer.data

                    # Add the correct tags to newly added movie
                    for tag in movie['tags']:
                        tag_data = {
                            "name": tag['name'],
                            "movie": to_return['id'],
                            "collection": collection_id
                        }
                        tag_serializer = TagSerializer(data=tag_data)
                        if tag_serializer.is_valid():
                            tag_serializer.save()
                            to_return['tags'] = tag_serializer.data
                            data_added.append(to_return)
                        else:
                            return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data_added, status=status.HTTP_201_CREATED)
                    