# core/signals.py
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
import math


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_movie_rating(sender, instance, **kwargs):
    """
    Recalculate average rating when reviews are saved or deleted
    """
    movie = instance.movie
    reviews = movie.reviews.all()

    if reviews.exists():
        # Calculate average and round up (ceiling)
        average = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        movie.average_rating = math.ceil(average)
    else:
        # No reviews = no rating
        movie.average_rating = None

    movie.save()