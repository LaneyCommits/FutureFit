"""Auth views: login, signup, verify email code, profile."""
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST

from .email_verification import (
    SESSION_PENDING_KEY,
    resend_code,
    verify_code_submission,
    seconds_until_resend_allowed,
    RESEND_COOLDOWN_SECONDS,
)
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfileUpdateForm
from .models import Profile

User = get_user_model()
logger = logging.getLogger(__name__)

_RESEND_SEND_FAILED = (
    'Could not send email. Check SMTP settings in your environment, or use the '
    'console email backend for local development.'
)


def _mask_email(email):
    if not email or '@' not in email:
        return ''
    local, _, domain = email.partition('@')
    if len(local) <= 2:
        masked = local[0] + '***'
    else:
        masked = local[0] + '***' + local[-1]
    return f'{masked}@{domain}'


def _get_pending_user(request):
    uid = request.session.get(SESSION_PENDING_KEY)
    if not uid:
        return None
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        request.session.pop(SESSION_PENDING_KEY, None)
        return None


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        Profile.objects.get_or_create(user=self.request.user)
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        Profile.objects.get_or_create(user=user)
        return super().form_valid(form)


def signup_view(request):
    """Sign up: create user, mark email verified, log in, redirect home."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    profile, created = Profile.objects.get_or_create(
                        user=user,
                        defaults={'email_verified': True},
                    )
                    if not created:
                        profile.email_verified = True
                        profile.save(update_fields=['email_verified'])
            except Exception:
                logger.exception('Signup failed')
                form.add_error(
                    None,
                    'Something went wrong creating your account. Please try again.',
                )
                return render(request, 'accounts/signup.html', {'form': form})
            login(request, user)
            messages.success(request, 'Welcome! You are signed in.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def verify_email_view(request):
    """Enter verification code; user is not logged in until success."""
    user = _get_pending_user(request)
    if user is None:
        messages.warning(request, 'Sign in or create an account to verify your email.')
        return redirect('login')

    profile, _ = Profile.objects.get_or_create(user=user)
    if profile.email_verified:
        request.session.pop(SESSION_PENDING_KEY, None)
        login(request, user)
        return redirect('home')

    try:
        state = user.email_verification_state
    except ObjectDoesNotExist:
        state = None

    resend_wait = seconds_until_resend_allowed(state)

    if request.method == 'POST':
        code = request.POST.get('code', '')
        ok, err = verify_code_submission(user, code)
        if ok:
            request.session.pop(SESSION_PENDING_KEY, None)
            login(request, user)
            messages.success(request, 'Your email is verified. Welcome!')
            next_url = request.session.pop('post_verify_next', None)
            if next_url:
                return redirect(next_url)
            return redirect('home')
        err_messages = {
            'invalid_format': 'Enter the 6-digit code from your email.',
            'no_code': 'No verification code on file. Use Resend to get a new code.',
            'expired': 'That code has expired. Click resend for a new code.',
            'locked': 'Too many attempts. Request a new code with Resend.',
            'wrong_code': 'That code is not correct. Try again.',
        }
        messages.error(request, err_messages.get(err, 'Verification failed.'))
        return redirect('verify_email')

    return render(request, 'accounts/verify_email.html', {
        'masked_email': _mask_email(user.email),
        'resend_seconds_remaining': resend_wait,
        'resend_cooldown_total': RESEND_COOLDOWN_SECONDS,
    })


@require_POST
def resend_verification_view(request):
    """AJAX/JSON: resend code if cooldown allows."""
    user = _get_pending_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'session'}, status=403)

    profile, _ = Profile.objects.get_or_create(user=user)
    if profile.email_verified:
        return JsonResponse({'ok': False, 'error': 'already_verified'}, status=400)

    try:
        ok, state, wait = resend_code(user)
    except Exception:
        logger.exception('Resend verification email failed')
        return JsonResponse({'ok': False, 'error': 'send_failed', 'message': _RESEND_SEND_FAILED}, status=503)

    if not ok:
        return JsonResponse({
            'ok': False,
            'retry_after_seconds': wait,
        }, status=429)

    return JsonResponse({
        'ok': True,
        'cooldown_seconds': RESEND_COOLDOWN_SECONDS,
    })


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def profile_view(request):
    """View and edit profile: avatar, bio, job preferences, AI personalization."""
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
            messages.success(request, 'Profile saved.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form,
        'quiz_pill_labels': quiz_labels,
    })


@login_required
def personalization_redirect_view(request):
    """Old URL /accounts/profile/personalization/ → profile (AI settings live there)."""
    return redirect(f"{reverse('profile')}#customize-ai")
