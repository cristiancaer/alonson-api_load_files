from django.urls import path
from django.http import JsonResponse
from rest_framework import status


def test():
    return lambda req: JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)


urlpatterns = [
    path('test/', test(), name='test'),
]
