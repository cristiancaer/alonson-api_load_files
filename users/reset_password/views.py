from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import ResetPasswordData, ChangePasswordAttempts
from django.core.exceptions import BadRequest
from utils.request_data import get_field_from_request
from utils.exceptions import NO_RECORDS, TASK_DONE
from users.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import time
from threading import Thread
from django.utils.crypto import get_random_string


class RequestResetPasswordApiView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def reset_code(clc, email):
        historic_reset_data = ResetPasswordData.objects.filter(user__email=email)
        if historic_reset_data:  # make soft delete
            historic_reset_data.update(code=None)

    def post(self, request):
        try:
            email = get_field_from_request(request.data, 'email')
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(NO_RECORDS, status=status.HTTP_400_BAD_REQUEST)
            self.reset_code(email)
            new_reset_data = ResetPasswordData(code=self.generate_random_code(), ip_address=request.META['REMOTE_ADDR'], user=user)
            new_reset_data.save()
            self.delete_password_code(new_reset_data)
            self.send_mail(new_reset_data.code, user)
            return Response(TASK_DONE, status=status.HTTP_200_OK)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def generate_random_code(clc):
        while True:
            code = get_random_string(length=64)
            if not ResetPasswordData.objects.filter(code=code).exists():
                break
        return code

    def delete_password_code(self, reset_password_data):
        """delete the password_code after PASSWORD_LIFETIME min"""
        def soft_delete():
            time.sleep(settings.PASSWORD_LIFETIME)
            reset_password_data.refresh_from_db()
            reset_password_data.code = None
            reset_password_data.save()

        task = Thread(target=soft_delete)
        task.start()

    def send_mail(self, reset_code, user):
        context = {
            'current_user': user.email,
            'username': user.email,
            'email': user.email,
            'reset_password_code': f"{reset_code}",
            'url': f"{settings.RESET_PASSWORD_URL}?code={reset_code}"
        }
        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
        with get_connection(host=settings.EMAIL_HOST,
                            port=settings.EMAIL_PORT,
                            username=settings.EMAIL_HOST_USER,
                            password=settings.EMAIL_HOST_PASSWORD,
                            use_tls=settings.EMAIL_USE_TLS) as connection:
            msg = EmailMultiAlternatives(
                # title:
                subject=f"Password Reset for {settings.SITE_NAME}",
                # message:
                body=email_plaintext_message,
                # from:
                from_email=settings.EMAIL_HOST_USER,
                # to:
                to=[user.email],
                connection=connection
            )
            msg.attach_alternative(email_html_message, "text/html")
            msg.send()


class CheckPasswordCodeApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            code = get_field_from_request(request.data, 'code')
            return self.check(code)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def check(clc, code):
        if not code:
            return Response({'detail': ' invalid code', 'type': 'task'}, status=status.HTTP_400_BAD_REQUEST)
        if not clc.allow_attempt(code):
            return Response({'detail': 'you have exceeded the maximum number of attempts. you must wait one hour to try again', 'type': 'task'}, status=status.HTTP_400_BAD_REQUEST)
        reset_data = ResetPasswordData.objects.filter(code=code).first()
        if not reset_data:
            return Response(NO_RECORDS, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'valid code', 'type': 'task'}, status=status.HTTP_200_OK)

    @staticmethod
    def get_user(code):
        password_data = ResetPasswordData.objects.filter(code=code).first()
        if not password_data:
            return None
        return password_data.user

    @classmethod
    def get_attempts(clc, code):
        user = clc.get_user(code)
        if not user:
            return None, None
        attempts = ChangePasswordAttempts.objects.filter(user__email=user.email).first()
        if not attempts:
            user = User.objects.filter(email=user.email).first()
            attempts = ChangePasswordAttempts(user=user)
            attempts.save()
        return attempts, user

    @classmethod
    def allow_attempt(self, code):
        attempts, user = self.get_attempts(code)
        if not attempts:
            attempts = ChangePasswordAttempts(user=user)
            attempts.save()
        allow = attempts.allow_increase_counter()
        if not allow:
            RequestResetPasswordApiView.reset_code(user.email)
        return allow


class ChangePasswordApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            code = get_field_from_request(request.data, 'code')
            check_code = CheckPasswordCodeApiView.check(code)
            if check_code.status_code == status.HTTP_400_BAD_REQUEST:
                return check_code

            password = get_field_from_request(request.data, 'password')
            user = CheckPasswordCodeApiView.get_user(code)
            self.set_password(user, password, code)
            self.sent_mail(user.email)
            return Response(TASK_DONE, status=status.HTTP_200_OK)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_password(self, user, password, code):
        user.set_password(password)
        user.save()
        reset_data = ResetPasswordData.objects.filter(user__id=user.id, code=code).first()
        reset_data.code = None
        reset_data.has_been_used = True
        reset_data.save()

    def sent_mail(self, email):
        with get_connection(host=settings.EMAIL_HOST,
                            port=settings.EMAIL_PORT,
                            username=settings.EMAIL_HOST_USER,
                            password=settings.EMAIL_HOST_PASSWORD,
                            use_tls=settings.EMAIL_USE_TLS) as connection:
            msg = EmailMultiAlternatives(
                # title:
                subject=f"Password Reset for {settings.SITE_NAME}",
                # message:
                body='Su contraseña ha sido cambiada con éxito',
                # from:
                from_email=settings.EMAIL_HOST_USER,
                # to:
                to=[email],
                connection=connection
            )
            msg.send()
