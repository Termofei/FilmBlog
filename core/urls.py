from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import HomePageView, MovieDetailView, AddReviewView, ReviewEditView, ReviewedMovieListView, \
    ReviewDeleteView, MovieViewSet, ReviewViewSet

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('reviews', ReviewViewSet)  # ← Add this


urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('films/', ReviewedMovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:pk>/review/', AddReviewView.as_view(), name='add-review'),
    path('reviews/<int:pk>/edit/', ReviewEditView.as_view(), name='review-edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('api/', include(router.urls)),
]