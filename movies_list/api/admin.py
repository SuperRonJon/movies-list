from django.contrib import admin
from api.models import Collection, Movie, Tag

# Register your models here.
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(Tag)