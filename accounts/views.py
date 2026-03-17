"""Auth views: login, signup, logout, profile, personalization (email verification removed)."""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, ProfileUpdateForm, PersonalizationForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        Profile.objects.get_or_create(user=self.request.user)
        return reverse_lazy('home')


def signup_view(request):
    """Sign up new users; create profile immediately."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def profile_view(request):
    """View and edit profile: avatar, bio, job preferences."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    quiz_labels = []
    try:
        quiz_labels = request.user.quiz_result.pill_labels or []
    except Exception:
        pass
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form,
        'quiz_pill_labels': quiz_labels,
    })


@login_required
def personalization_view(request):
    """View and edit AI personalization: base style, custom instructions."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PersonalizationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('personalization')
    else:
        form = PersonalizationForm(instance=profile)
    return render(request, 'accounts/personalization.html', {
        'profile': profile,
        'form': form,
    })
