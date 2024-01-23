from django.contrib.auth.backends import ModelBackend
from users.models import User


class UserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        try:
            user = User.objects.get(email=email)
            valid_password = user.check_password(password)
            if valid_password and user.is_active and user.company.is_active:
                return user
        except User.DoesNotExist:
            pass
