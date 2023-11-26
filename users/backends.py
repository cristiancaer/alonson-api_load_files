from django.contrib.auth.backends import ModelBackend
from users.models import User


class UserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        try:
            user = User.objects.get(email=email)
            valid = user.check_password(password)
            if valid:
                return user
        except User.DoesNotExist:
            pass
