from utils.views import RollAccessApiView
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminUser


class UsersApiView(RollAccessApiView):
    permission_classes = (IsAdminUser,)
    model = User
    serializer = UserSerializer
    id_field_name = 'user_id'


class MeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
