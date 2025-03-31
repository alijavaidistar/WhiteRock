from django.contrib.auth import get_user_model

User = get_user_model()

def assign_basic_role(strategy, details, backend, user=None, *args, **kwargs):
    """
    Assigns 'basic' role to users who sign up via Microsoft authentication.
    """
    if user and not user.role:  # Only assign role if it's not already set
        user.role = 'basic'
        user.save()
    return {'user': user}
