

from django.contrib.auth import get_user_model

User = get_user_model()

def authenticate_email(email, password):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
