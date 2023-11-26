from rest_framework import serializers
from .models import Company, Area


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
