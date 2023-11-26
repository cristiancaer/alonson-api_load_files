from django.urls import path, include
from django.http import JsonResponse
from rest_framework import status


def test():
    return lambda req: JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)


urlpatterns = [
    path('test', test(), name='test'),
    path('users/', include('users.urls')),
    path('companies/', include('companies.urls')),
]
