from django.urls import path
from .views import FilesApiView, MasterFilesApiView, MaterTypesApiView


urlpatterns = [
    path('', FilesApiView.as_view(), name='files'),
    path('<int:file_id>', FilesApiView.as_view(), name='files'),
    path('master_files', MasterFilesApiView.as_view(), name='master_files'),
    path('master_files/<int:master_id>', MasterFilesApiView.as_view(), name='master_files'),
    path('master_files/types', MaterTypesApiView.as_view(), name='master_types'),
    path('master_files/types/<int:type_id>', MaterTypesApiView.as_view(), name='master_types'),
]
