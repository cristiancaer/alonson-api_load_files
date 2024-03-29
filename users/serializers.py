from rest_framework import serializers
from .models import User
from companies.serializers import CompanySerializer, AreaSerializer, Company, Area


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    area = AreaSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        company = data.get('company', None)
        if company:
            internal_value['company'] = Company.objects.get(id=company)
        area = data.get('area', None)
        if area:
            internal_value['area'] = Area.objects.get(id=area)
        return internal_value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
