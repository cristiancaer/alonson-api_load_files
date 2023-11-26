from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from utils.request_data import get_field_from_url_args
from django.core.exceptions import BadRequest
from utils.exceptions import NO_RECORDS, TASK_DONE, format_serializer_errors


class BasicCrudApiView(APIView):
    class_model = Model
    class_serializer = ModelSerializer
    use_user = False
    id_field_name = 'id'
    use_user_as = 'user'

    def get(self, request, **kwargs):
        try:
            instances = self.class_model.objects.all()
            if self.use_user:
                instances = instances.filter(**{self.use_user_as: request.user.id})

            id_value = get_field_from_url_args(kwargs, self.id_field_name, False)
            if id_value:
                instances = instances.filter(id=id_value)

            if not instances:
                return Response(NO_RECORDS, status=status.HTTP_204_NO_CONTENT)
            if id_value:
                serializer = self.class_serializer(instances.first())
            else:
                serializer = self.class_serializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, **kwargs):
        try:
            data = request.data
            if self.use_user:
                if isinstance(data, dict):
                    data = {**data, self.use_user_as: request.user.id}
                else:
                    data = {**data.dict(), self.use_user_as: request.user.id}
            serializer = self.class_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, **kwargs):
        try:
            data = request.data
            if self.use_user:
                if isinstance(data, dict):
                    data = {**data, self.use_user_as: request.user.id}
                else:
                    data = {**data.dict(), self.use_user_as: request.user.id}
            id = get_field_from_url_args(kwargs, self.id_field_name)
            instance = self.class_model.objects.filter(id=id).first()
            if not instance:
                return Response(NO_RECORDS, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.class_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(format_serializer_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except BadRequest as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, **kwargs):
        try:
            id = get_field_from_url_args(kwargs, self.id_field_name)
            if self.use_user:
                instance = self.class_model.objects.filter(id=id, **{self.use_user_as: request.user.id}).first()
            else:
                instance = self.class_model.objects.filter(id=id).first()
            if not instance:
                return Response(NO_RECORDS, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(TASK_DONE, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
