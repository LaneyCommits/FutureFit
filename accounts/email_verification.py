"""Email verification codes: generate, hash, send, cooldown."""
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import EmailVerificationState, Profile

logger = logging.getLogger(__name__)

CODE_LENGTH = 6
CODE_EXPIRY_MINUTES = 20
RESEND_COOLDOWN_SECONDS = 60
MAX_FAILED_ATTEMPTS = 8

SESSION_PENDING_KEY = 'pending_verification_user_id'


def _generate_numeric_code():
    return f'{secrets.randbelow(900000) + 100000}'


def issue_new_code(user):
    """Create a new code, persist hashed state, return plaintext code (for email only)."""
    code = _generate_numeric_code()
    code_hash = make_password(code)
    now = timezone.now()
    expires = now + timedelta(minutes=CODE_EXPIRY_MINUTES)
    EmailVerificationState.objects.update_or_create(
        user=user,
        defaults={
            'code_hash': code_hash,
            'expires_at': expires,
            'last_sent_at': now,
            'failed_attempts': 0,
        },
    )
    return code


def send_verification_email(user, code):
    subject = 'Your ExploringU verification code'
    body = (
        f'Hi {user.username},\n\n'
        f'Your verification code is: {code}\n\n'
        f'This code expires in {CODE_EXPIRY_MINUTES} minutes.\n\n'
        f'If you did not create an account, you can ignore this email.\n'
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_initial_verification(user):
    """Signup: always send a fresh code. Call inside transaction.atomic() so mail failure rolls back user."""
    code = issue_new_code(user)
    send_verification_email(user, code)
    return user.email_verification_state


def ensure_active_code_for_unverified_login(user):
    """
    Login with unverified account: send a code only if missing or expired.
    If current code still valid, do not resend (avoid inbox spam).
    """
    try:
        state = user.email_verification_state
        if state.expires_at > timezone.now():
            return state
    except EmailVerificationState.DoesNotExist:
        pass
    with transaction.atomic():
        code = issue_new_code(user)
        send_verification_email(user, code)
    return user.email_verification_state


def seconds_until_resend_allowed(state):
    """Return 0 if resend is allowed, else seconds remaining."""
    if state is None:
        return 0
    elapsed = (timezone.now() - state.last_sent_at).total_seconds()
    remaining = RESEND_COOLDOWN_SECONDS - elapsed
    return max(0, int(remaining))


def resend_code(user):
    """
    User clicked Resend. Enforce cooldown.
    Returns (success: bool, state_or_none, wait_seconds_if_failed).
    """
    try:
        state = user.email_verification_state
    except EmailVerificationState.DoesNotExist:
        state = None

    wait = seconds_until_resend_allowed(state)
    if wait > 0:
        return False, state, wait

    with transaction.atomic():
        code = issue_new_code(user)
        send_verification_email(user, code)
    return True, user.email_verification_state, 0


def verify_code_submission(user, code_input):
    """
    Check submitted code. On success: mark profile verified, delete state.
    Returns (success: bool, error_key: str|None).
    """
    code_input = (code_input or '').strip().replace(' ', '')
    if len(code_input) != CODE_LENGTH or not code_input.isdigit():
        return False, 'invalid_format'

    try:
        state = user.email_verification_state
    except EmailVerificationState.DoesNotExist:
        return False, 'no_code'

    if timezone.now() > state.expires_at:
        return False, 'expired'

    if state.failed_attempts >= MAX_FAILED_ATTEMPTS:
        return False, 'locked'

    if not check_password(code_input, state.code_hash):
        EmailVerificationState.objects.filter(pk=state.pk).update(
            failed_attempts=F('failed_attempts') + 1
        )
        return False, 'wrong_code'

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.email_verified = True
    profile.save(update_fields=['email_verified'])
    EmailVerificationState.objects.filter(user=user).delete()
    return True, None
