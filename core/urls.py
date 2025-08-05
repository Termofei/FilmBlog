from django.urls import path

from core.views import HomePageView, MovieDetailView, AddReviewView, ReviewEditView, ReviewedMovieListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('films/', ReviewedMovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:pk>/review/', AddReviewView.as_view(), name='add-review'),
    path('reviews/<int:pk>/edit/', ReviewEditView.as_view(), name='review-edit'),
]