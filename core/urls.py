from django.urls import path

from core.views import HomePageView, MovieDetailView, MovieListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('films/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
]