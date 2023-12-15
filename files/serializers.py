from rest_framework import serializers
from .models import TransactionFile, MasterFile, MasterFileType, TransactionColumnNameOption


class FileSerializer(serializers.ModelSerializer):
    last_version = serializers.IntegerField(read_only=True)

    class Meta:
        model = TransactionFile
        fields = '__all__'

    def to_internal_value(self, data):
        data.update({'uploaded_filename': data.get('file').name})
        return super().to_internal_value(data)


class MasterFileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterFileType
        fields = '__all__'


class MasterFileSerializer(serializers.ModelSerializer):
    type = MasterFileTypeSerializer(read_only=True)

    class Meta:
        model = MasterFile
        fields = '__all__'

    def to_internal_value(self, data):
        data.update({'uploaded_filename': data.get('file').name})
        internal_value = super().to_internal_value(data)
        type = MasterFileType.objects.get(id=data.get('type'))
        internal_value.update({'type': type})
        return internal_value


class TransactionColumnNameOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionColumnNameOption
        fields = '__all__'
