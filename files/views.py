from .models import TransactionFile, MasterFileType, MasterFile, TransactionColumnNameOption
from .serializers import FileSerializer, MasterFileTypeSerializer, MasterFileSerializer, TransactionColumnNameOptionSerializer
from utils.views import RollAccessApiView, BasicCrudApiView
from rest_framework.response import Response
from rest_framework import status
from utils.request_data import get_field_from_request
from utils.exceptions import format_serializer_errors
from django.core.exceptions import BadRequest
from users.permissions import IsSuperAdminOrReadOnly
from django.db import transaction
from .transactions import TransactionsHandler
from utils.request_data import get_field_from_url_args
from utils.exceptions import NO_RECORDS


class FilesApiView(RollAccessApiView):
    model = TransactionFile
    serializer = FileSerializer
    id_field_name = 'file_id'
    user_field_name = 'loaded_by'

    def get(self, request, **kwargs):
        try:
            data = self.get_queryset(request)
            id = get_field_from_url_args(kwargs, self.id_field_name, False)
            year = get_field_from_url_args(request.GET, 'year', False)
            month = get_field_from_url_args(request.GET, 'month', False)
            company = get_field_from_url_args(request.GET, 'company', False)
            area = get_field_from_url_args(request.GET, 'area', False)
            if year:
                data = data.filter(year=year)
            if month:
                data = data.filter(month=month)
            if company:
                data = data.filter(company__id=company)
            if area:
                data = data.filter(area__id=area)
            if id:
                data = data.filter(id=id).first()
            if not data:
                return Response(NO_RECORDS, status=status.HTTP_204_NO_CONTENT)
            serializer = self.serializer(data, many=not bool(id))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, **kwargs):
        try:
            data = self.get_validated_data(request)
            query = self.get_queryset(request)
            company = get_field_from_request(data, 'company')
            area = get_field_from_request(data, 'area')
            year = get_field_from_request(data, 'year')
            month = get_field_from_request(data, 'month')
            is_adjustment = get_field_from_request(data, 'is_adjustment')
            file = get_field_from_request(data, 'file')
            stored_file = query.filter(company=company, area=area, year=year, month=month, is_adjustment=is_adjustment).first()
            if not stored_file:
                serializer = self.serializer(data=data)
            else:
                serializer = self.serializer(instance=stored_file, data=data, partial=True)
            if serializer.is_valid():
                with transaction.atomic():
                    transaction_file = serializer.save()
                    transactions = TransactionsHandler(transaction_file, file)
                    print(transactions.df.head(20))
                    print(transactions.df.tail(20))
                    transactions.save_in_db()
                    print(transactions.df.head())
                    print('done')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MaterTypesApiView(BasicCrudApiView):
    model = MasterFileType
    serializer = MasterFileTypeSerializer
    id_field_name = 'type_id'
    permission_classes = (IsSuperAdminOrReadOnly,)


class TransactionColumnNameOptionsApiView(RollAccessApiView):
    model = TransactionColumnNameOption
    serializer = TransactionColumnNameOptionSerializer
    id_field_name = 'column_name_id'
    permission_classes = (IsSuperAdminOrReadOnly,)


class MasterFilesApiView(RollAccessApiView):
    model = MasterFile
    serializer = MasterFileSerializer
    id_field_name = 'master_id'
    user_field_name = 'loaded_by'

    def put(self, request, **kwargs):
        try:
            data = self.get_validated_data(request)
            query = self.get_queryset(request)
            company = get_field_from_request(data, 'company')
            area = get_field_from_request(data, 'area')
            type = get_field_from_request(data, 'type')
            stored_file = query.filter(company=company, area=area, type=type).first()
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
