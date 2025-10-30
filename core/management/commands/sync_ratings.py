from django.core.management.base import BaseCommand
from core.models import Movie


class Command(BaseCommand):
    help = 'Sync average ratings for existing movies'

    def handle(self, *args, **options):
        movies = Movie.objects.filter(reviews__isnull=False).distinct()
        for movie in movies:
            # Reuse your signal logic
            from core.signals import update_movie_rating
            update_movie_rating(None, movie.reviews.first())

        self.stdout.write(
            self.style.SUCCESS(f'Synced ratings for {movies.count()} movies')
        )