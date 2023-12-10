from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def to_internal_value(self, data):
        data.update({'uploaded_filename': data.get('file').name})
        return super().to_internal_value(data)