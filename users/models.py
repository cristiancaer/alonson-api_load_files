from django.db import models
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
    PBKDF2PasswordHasher,
)
from django.contrib.auth.models import BaseUserManager
from utils.fields import validate_password
from companies.models import Company, Area


class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    is_active = models.BooleanField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_users')
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, related_name='area_users')
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _password = None
    _hasher = PBKDF2PasswordHasher()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = BaseUserManager()

    class Meta:
        db_table = 'users'
        unique_together = (('company', 'email'),)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.is_super_admin:
            self.is_admin = True
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        validate_password(raw_password, 8, raise_error=True)
        self.password = make_password(raw_password, hasher=self._hasher)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter, preferred=self._hasher)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False
