from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.models import Review
from users.forms import ProfileEditForm
from users.models import UserProfile


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the instance
            # Auto-login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')  # Send to homepage instead of login
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register-page.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home-page')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login-page.html', {'form': form})

@login_required
def profile_view(request):
    user_reviews = Review.objects.filter(author=request.user)
    return render(request, 'accounts/profile-details-page.html', {'reviews': user_reviews})


@login_required
def profile_edit(request):
    profile = UserProfile.objects.get(user=request.user)  # Simple get (no get_or_create)

    if request.method == 'POST':
        profile.avatar_url = request.POST['avatar_url']  # Direct access
        profile.bio = request.POST['bio']
        profile.save()
        return redirect('home-page')  # Hard redirect

    return render(request, 'accounts/profile-edit-page.html', {
        'avatar_url': profile.avatar_url,
        'bio': profile.bio,
        'username': request.user.username
    })