from django.db import models
from companies.models import Company, Area
from users.models import User
from utils.fields import setRangeValidators
from pathlib import Path
from .storages import AzureStorage
from utils.files import PLAIN_EXTENSIONS, EXCEL_EXTENSIONS


def get_base_area_path(instance):
    return f"{instance.company.name}_{instance.company.code}/{instance.area.name}"


class TransactionFile(models.Model):
    def get_company_directory_path(instance, filename):
        # file will be uploaded to azure_container/<company_code>/<area>/<movientos>/<filename>
        file_extension = Path(filename).suffix.strip('.')
        allowed_extensions = PLAIN_EXTENSIONS + EXCEL_EXTENSIONS
        if file_extension not in allowed_extensions:
            raise Exception(f"Extension {file_extension} not allowed. Allowed extensions are {allowed_extensions}")
        path_name = f"{get_base_area_path(instance)}/movimientos/{instance.year}_{instance.month:02}.{file_extension}"
        return path_name

    uploaded_filename = models.CharField(max_length=255)
    file = models.FileField(storage=AzureStorage(), upload_to=get_company_directory_path)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_files')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name= 'area_files')
    loaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
    year = models.IntegerField(validators=setRangeValidators(1900, 2100))
    month = models.IntegerField(validators=setRangeValidators(1, 12))
    last_version = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        self.last_version += 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'transaction_files'
        unique_together = (('company', 'area', 'year', 'month'),)
        ordering = ('-year', '-month')


class MasterFileType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master_file_types'
        ordering = ('name',)


class MasterFile(models.Model):
    def get_company_directory_path(instance, filename):
        # file will be uploaded to azure_container/<company_code>/<area>/<filename>
        file_extension = Path(filename).suffix.strip('.')
        allowed_extensions = PLAIN_EXTENSIONS + EXCEL_EXTENSIONS
        if file_extension not in allowed_extensions:
            raise Exception(f"Extension {file_extension} not allowed. Allowed extensions are {allowed_extensions}")
        path_name = f"{get_base_area_path(instance)}/maestros/{instance.type.name}.{file_extension}"
        return path_name

    type = models.ForeignKey(MasterFileType, on_delete=models.CASCADE, related_name='master_files')
    uploaded_filename = models.CharField(max_length=255)
    file = models.FileField(storage=AzureStorage(), upload_to=get_company_directory_path)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_master_files')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name= 'area_master_files')
    loaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_master_files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master_files'
        unique_together = (('company', 'area'),)
        ordering = ('-created_at',)


class Transaction(models.Model):
    index_in_file = models.PositiveIntegerField()
    file = models.ForeignKey(TransactionFile, on_delete=models.DO_NOTHING, related_name='transactions')
    account_level = models.CharField(max_length=20, null=True)  # nivel_cuenta
    is_transactional = models.BooleanField()  # transaccional
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    third_code = models.CharField(max_length=20, null=True)  # codigo_tercero
    branch = models.CharField(max_length=20, null=True)  # sucursal_tercero
    third_name = models.CharField(max_length=100, null=True)  # nombre_tercero
    initial_balance = models.FloatField()  # saldo_inicial
    debit = models.FloatField()  # movimiento_debito
    credit = models.FloatField()  # movimiento_credito
    final_balance = models.FloatField()
    is_active = models.BooleanField(default=True)  # activo
    # is_reprocessing = models.BooleanField(default=True)  # reproceso
    version = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ('file', 'index_in_file',)

    def __str__(self):
        return self.account_name


class TransactionColumnNameOption(models.Model):
    key_name = models.CharField(max_length=25, unique=True)
    values = models.JSONField()
    is_required = models.BooleanField(default=True)

    class Meta:
        db_table = 'transaction_column_name_options'
