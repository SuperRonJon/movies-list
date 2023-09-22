from rest_framework import serializers
from .models import Movie, Tag

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 
            'title', 
            'tmdb_id', 
            'popularity', 
            'release_date', 
            'overview',
            'poster_path'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'movie',
            'name'
        )