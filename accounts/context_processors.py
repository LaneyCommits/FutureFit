"""Context processors for accounts app."""
from .models import Profile


def user_profile(request):
    """
    Add user_profile to the template context when available.

    Profiles are created at signup; email must be verified before the user is logged in.
    """
    if request.user.is_authenticated:
        try:
            return {'user_profile': request.user.profile}
        except Profile.DoesNotExist:
            pass
    return {'user_profile': None}
