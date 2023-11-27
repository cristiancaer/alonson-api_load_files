from django.urls import path
from .views import FilesApiView


urlpatterns = [
    path('', FilesApiView.as_view(), name='files'),
    path('<int:file_id>', FilesApiView.as_view(), name='files'),
]
