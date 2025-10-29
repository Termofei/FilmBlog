from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, permissions

from core.forms import ReviewForm
from core.models import Review, Movie
from core.serializers import MovieSerializer, ReviewSerializer


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        if self.request.user.is_authenticated:
            context['user_review'] = Review.objects.filter(
                movie=self.object,
                author=self.request.user
            ).first()
        return context

class ReviewedMovieListView(ListView):
    template_name = 'movies/movie-list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(
            reviews__author=self.request.user
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for movie in context['movies']:
            movie.user_review = movie.reviews.filter(
                author=self.request.user
            ).first()
        return context



class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movies/movie-detail.html'

    def dispatch(self, request, *args, **kwargs):
        if Review.objects.filter(
                movie_id=self.kwargs['pk'],
                author=request.user
        ).exists():
            return HttpResponseForbidden("You've already reviewed this movie.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.movie_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('movie-detail', kwargs={'pk': self.kwargs['pk']})


class ReviewEditView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movies/review-edit-page.html'

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author != request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('movie-detail', kwargs={'pk': self.object.movie.id})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'movies/review_confirm_delete.html'
    success_url = reverse_lazy('movie-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer