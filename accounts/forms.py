"""Custom auth forms with username rules and email; profile and personalization."""
import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.]+\Z')
USERNAME_MAX_LENGTH = 20


class CustomUserCreationForm(UserCreationForm):
    """Signup form: username max 20 chars, only letters, numbers, _ and .; email required."""

    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='',
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = USERNAME_MAX_LENGTH
        self.fields['username'].widget.attrs['maxlength'] = str(USERNAME_MAX_LENGTH)
        self.fields['username'].help_text = ''  # remove default "@/./+/-/_ only" text

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if len(username) > USERNAME_MAX_LENGTH:
            raise ValidationError(
                f'Username must be {USERNAME_MAX_LENGTH} characters or fewer.',
                code='username_too_long',
            )
        if not USERNAME_PATTERN.match(username):
            raise ValidationError(
                'Username can only contain letters, numbers, underscores (_) and periods (.).',
                code='username_invalid',
            )
        existing = User.objects.filter(username__iexact=username).first()
        if existing:
            prof = Profile.objects.filter(user=existing).first()
            if prof and prof.email_verified:
                raise ValidationError(
                    'A user with that username already exists.',
                    code='username_exists',
                )
            existing.delete()
        return username

    def clean_password1(self):
        """
        Make passwords case-insensitive by normalizing to lowercase.
        Note: existing users will need to reset/recreate their accounts for this to take effect.
        """
        pw1 = self.cleaned_data.get('password1')
        return pw1.lower() if pw1 is not None else pw1

    def clean_password2(self):
        pw2 = self.cleaned_data.get('password2')
        return pw2.lower() if pw2 is not None else pw2

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        for u in User.objects.filter(email__iexact=email):
            prof = Profile.objects.filter(user=u).first()
            if prof and prof.email_verified:
                raise ValidationError(
                    'An account with this email already exists. Sign in instead.',
                    code='email_exists_verified',
                )
            u.delete()
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()
        if commit:
            user.save()
            self.save_m2m()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Login form that normalizes the password to lowercase so login is case-insensitive.
    """

    def clean_password(self):
        pw = self.cleaned_data.get('password')
        return pw.lower() if pw is not None else pw


class ProfileUpdateForm(forms.ModelForm):
    """Profile avatar, bio, job preferences, and AI personalization."""

    class Meta:
        model = Profile
        fields = (
            'avatar', 'bio', 'major_key', 'preferred_job_type',
            'preferred_remote', 'preferred_location', 'min_salary',
            'base_style', 'custom_instructions',
        )
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-input profile-avatar-file',
                'accept': 'image/*',
            }),
            'preferred_location': forms.TextInput(attrs={
                'placeholder': 'e.g. New York, San Francisco',
            }),
            'min_salary': forms.NumberInput(attrs={
                'placeholder': 'e.g. 50000',
                'min': '0',
            }),
            'custom_instructions': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-input',
                'placeholder': (
                    'e.g. Write like a real human. Stay professional but casual. '
                    'Avoid buzzwords and jargon.'
                ),
            }),
        }
        labels = {
            'major_key': 'Major',
            'preferred_job_type': 'Preferred job type',
            'preferred_remote': 'Work setting',
            'preferred_location': 'Preferred location',
            'min_salary': 'Minimum salary ($)',
            'base_style': 'Base style and tone',
            'custom_instructions': 'Custom instructions',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from career_quiz.quiz_data import MAJORS
        major_choices = [('', 'Not set')] + [(m[0], m[1]) for m in MAJORS]
        self.fields['major_key'].widget = forms.Select(choices=major_choices)
        self.fields['base_style'].widget.attrs.setdefault('class', 'form-input')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2 MB
            raise ValidationError('Image must be under 2 MB.')
        return avatar


