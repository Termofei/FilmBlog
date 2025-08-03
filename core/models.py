from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255, blank=True)
    cast = models.CharField(max_length=500, blank=True)
    release_date = models.DateField(blank=True, null=True)
    poster_url = models.URLField(blank=True)  # TMDB/IMDb link
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.author.username}"