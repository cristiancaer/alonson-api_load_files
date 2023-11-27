from utils.views import RollAccessApiView
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UsersApiView(RollAccessApiView):
    permission_classes = (IsAuthenticated,)
    model = User
    serializer = UserSerializer
    id_field_name = 'user_id'
