from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 
            'title', 
            'tmdb_id', 
            'popularity', 
            'release_date', 
            'overview'
        )