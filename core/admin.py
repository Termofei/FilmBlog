from django.contrib import admin
from django.contrib.auth.models import User

from core.models import Movie, Review


# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    ...

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ...