from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from .views import UsersApiView, MeApiView


urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UsersApiView.as_view(), name='users'),
    path('me', MeApiView.as_view(), name='users.me'),
    path('<int:user_id>', UsersApiView.as_view(), name='user'),
    path('reset_password/', include('users.reset_password.urls'))
]
