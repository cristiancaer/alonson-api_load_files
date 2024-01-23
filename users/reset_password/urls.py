from django.urls import path
from .views import RequestResetPasswordApiView, CheckPasswordCodeApiView, ChangePasswordApiView


urlpatterns = [
    path('', RequestResetPasswordApiView.as_view()),
    path('check_code', CheckPasswordCodeApiView.as_view()),
    path('change_password', ChangePasswordApiView.as_view(), name='change_password')
]
