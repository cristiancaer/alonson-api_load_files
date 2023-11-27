from utils.views import BasicCrudApiView
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UsersApiView(BasicCrudApiView):
    permission_classes = (IsAuthenticated,)
    class_model = User
    class_serializer = UserSerializer
    id_field_name = 'user_id'
