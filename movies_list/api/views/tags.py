from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Tag
from ..serializers import TagSerializer


class TagsView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagMovieView(APIView):
    def get(self, request, movie):
        tags = Tag.objects.filter(movie__exact=movie)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagRemoveView(generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagUniqueView(APIView):
    def get(self, request):
        tags = Tag.objects.order_by('name').values('name').distinct()
        return Response(tags)
    
    
class TagBulkView(APIView):
    def post(self, request):
        return_data = []
        for tag in request.data:
            serializer = TagSerializer(data=tag)
            if serializer.is_valid():
                serializer.save()
                return_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(return_data, status=status.HTTP_201_CREATED)