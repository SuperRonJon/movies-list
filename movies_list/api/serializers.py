from rest_framework import serializers
from .models import Movie, Tag, Collection


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
            'poster_path',
            'collection'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'movie',
            'name',
            'collection'
        )


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'id',
            'name'
        )