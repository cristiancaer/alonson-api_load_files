from .models import UsageLog
from rest_framework import serializers


class UsageLogSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = UsageLog
        exclude = ('response',)
