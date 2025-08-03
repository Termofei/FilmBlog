from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Review, Movie


# Create your views here.


class HomePageView(ListView):
    template_name = 'core/home-page.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            return Movie.objects.filter(
                Q(title__icontains=search_query) |
                Q(director__icontains=search_query)
            )
        return Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_reviews'] = Review.objects.order_by('-created_at')[:5]
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie-detail.html'

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie-list.html'  # Create this template
    context_object_name = 'movies'