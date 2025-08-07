from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import register_view, login_view, profile_view, profile_edit

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home-page'), name='logout'),  # Django built-in
    path('profile/', profile_view, name='profile-details'),
    path('profile/edit/', profile_edit, name='profile-edit'),
]