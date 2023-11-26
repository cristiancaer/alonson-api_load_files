from utils.views import BasicCrudApiView
from .models import User
from .serializers import UserSerializer


class UsersApiView(BasicCrudApiView):
    class_model = User
    class_serializer = UserSerializer
    field_id = 'user_id'
