from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UsageLog
from .serializers import UsageLogSerializer


class LoadedFilesLogApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            UPLOADED_FILES_URLS = ['/files/', '/files/master_files']
            data = self.get_validated_data(request)
            area_files = UsageLog.objects.filter(user__company=data['company'], user__area=data['area'], method__in=['POST', 'PUT'], path__in=UPLOADED_FILES_URLS)
            serializer = UsageLogSerializer(area_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_validated_data(self, request):
        data = request.GET
        if request.user.is_super_admin:
            return data
        if request.user.is_admin:
            {**data, 'company': request.user.company.id}
            return data
        data = {**data, 'company': request.user.company.id, 'area': request.user.area.id}
        return data