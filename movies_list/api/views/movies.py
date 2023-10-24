from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Movie
from ..serializers import MovieSerializer
from ..tmdb_service import get_search_results, get_movie_info

# Create your views here.

def hello_world(request):
    return HttpResponse("Hello world")


class MoviesView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    def post(self, request):
        movies = Movie.objects.filter(tmdb_id__exact=request.data['tmdb_id'], collection__exact=request.data['collection'])
        if len(movies) > 0:
            return Response({'message': 'Movie already in collection'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieView(generics.RetrieveDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SearchView(APIView):
    def get(self, request):
        search_query = request.query_params.get('q')
        if search_query is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        movies = get_search_results(search_query)
        return Response(movies, status=status.HTTP_200_OK)


class InfoView(APIView):
    def get(self, request, id):
        info = get_movie_info(id)
        if info is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(info)
