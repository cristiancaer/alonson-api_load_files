from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50)
    code = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return f'Company({self.name})'


class Area(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'areas'

    def __str__(self):
        return f'Area({self.name})'
