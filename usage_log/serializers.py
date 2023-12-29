from .models import UsageLog
from rest_framework import serializers


class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageLog
        fields = '__all__'
