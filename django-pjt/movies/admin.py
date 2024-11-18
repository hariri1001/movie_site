from django.contrib import admin

# Register your models here.
from .models import Movie


admin.site.register(Movie)
# admin.site.register(Rank)
# admin.site.register(Genre)