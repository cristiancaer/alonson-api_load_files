from django.db import models
from users.models import User


class UsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_usage_logs', blank=True, null=True)
    method = models.CharField(max_length=25)
    path = models.CharField(max_length=250)
    ip = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=100)
    status_code = models.PositiveIntegerField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usage_logs'
        ordering = ('-created_at',)
