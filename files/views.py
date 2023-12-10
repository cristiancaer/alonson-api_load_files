from .models import File
from .serializers import FileSerializer
from utils.views import RollAccessApiView


class FilesApiView(RollAccessApiView):
    model = File
    serializer = FileSerializer
    id_field_name = 'file_id'
    user_field_name = 'loaded_by'
