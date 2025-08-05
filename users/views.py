from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.models import Review


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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


# class CustomLoginView(LoginView):
#     template_name = 'accounts/login-page.html'
#     redirect_authenticated_user = True  # Redirects if already logged in
#     success_url = reverse_lazy('home-page')  # Where to redirect after login
