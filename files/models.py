from django.db import models
from companies.models import Company, Area
from users.models import User
from utils.fields import setRangeValidators


class File(models.Model):
    def company_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/<company>/<area>/<filename>
        return f"{instance.company.code}/{instance.area.name}/{instance.year}/{instance.month}_{filename}"

    file = models.FileField(upload_to=company_directory_path)
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
