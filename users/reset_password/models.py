from django.db import models
from users.models import User
from datetime import datetime, timedelta
from django.conf import settings


class ResetPasswordData(models.Model):
    code = models.CharField(max_length=8, null=True, blank=True)
    ip_address = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    has_been_used = models.BooleanField(default=False)

    def check_code(self, request_code):
        if not self.code:
            return False
        return self.code == request_code


class ChangePasswordAttempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def allow_increase_counter(self):
        if self.count < settings.MAX_PASSWORD_ATTEMPTS:
            self.count += 1
            self.save()
            return True
        now = datetime.now()
        exp = self.updated_at + timedelta(hours=1)
        if now > exp:
            self.count = 0
            self.allow_increase_counter()
        return False
