from django.urls import path
from .views import LoadedFilesLogApiView


urlpatterns = [
    path('loaded_files', LoadedFilesLogApiView.as_view(), name='loaded_files_log'),
]