from django.db import models
from companies.models import Company, Area
from users.models import User
from utils.fields import setRangeValidators
from pathlib import Path
from .storages import AzureStorage
from utils.files import PLAIN_EXTENSIONS, EXCEL_EXTENSIONS


class File(models.Model):
    def get_company_directory_path(instance, filename):
        # file will be uploaded to azure_container/<company>/<area>/<filename>
        file_extension = Path(filename).suffix
        allowed_extensions = PLAIN_EXTENSIONS + EXCEL_EXTENSIONS
        if file_extension not in allowed_extensions:
            raise Exception(f"Extension {file_extension} not allowed. Allowed extensions are {allowed_extensions}")
        path_name = f"{instance.company.code}/{instance.area.name}/movimiento/{instance.year}_{instance.month:02}{file_extension}"
        return path_name

    file = models.FileField(storage=AzureStorage(), upload_to=get_company_directory_path)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_files')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name= 'area_files')
    loaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
    year = models.IntegerField(validators=setRangeValidators(1900, 2100))
    month = models.IntegerField(validators=setRangeValidators(1, 12))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'
        unique_together = (('company', 'area', 'year', 'month'),)
        ordering = ('-year', '-month')
