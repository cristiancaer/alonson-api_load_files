from .models import File
from .serializers import FileSerializer
from utils.views import RollAccessApiView
from rest_framework.response import Response
from rest_framework import status
from utils.request_data import get_field_from_request
from utils.exceptions import format_serializer_errors
from django.core.exceptions import BadRequest


class FilesApiView(RollAccessApiView):
    model = File
    serializer = FileSerializer
    id_field_name = 'file_id'
    user_field_name = 'loaded_by'

    def put(self, request, **kwargs):
        try:
            data = self.get_validated_data(request)
            query = self.get_queryset(request)
            company = get_field_from_request(data, 'company')
            area = get_field_from_request(data, 'area')
            year = get_field_from_request(data, 'year')
            month = get_field_from_request(data, 'month')
            stored_file = query.filter(company=company, area=area, year=year, month=month).first()
            if not stored_file:
                serializer = self.serializer(data=data)
            else:
                serializer = self.serializer(instance=stored_file, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
