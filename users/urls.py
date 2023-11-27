from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import UsersApiView


urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UsersApiView.as_view(), name='users'),
    path('<int:user_id>', UsersApiView.as_view(), name='user'),
]
