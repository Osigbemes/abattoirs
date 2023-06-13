import uuid
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.common.models import BaseModel

class User(AbstractBaseUser, PermissionsMixin):
    
    """
    This is a custom user model that inherits the abstract base user and safe delete mode
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    firstname = models.CharField(verbose_name=(_("First Name")), max_length=200)
    lastname = models.CharField(verbose_name=(_("Last Name")), max_length=200)
    email = models.EmailField(verbose_name=(_("Email")), unique=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    active = models.BooleanField(default=True)
    account_verified = models.BooleanField(default=False)
    account_verified_at = models.DateTimeField(null=True)
    staff = models.BooleanField(default=False)  # a admin user
    admin = models.BooleanField(default=False)  # a superuser
    is_identity_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # role = models.IntegerField()
    
    REQUIRED_FIELDS = [firstname, lastname]
    USERNAME_FIELD = "email"
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ("-created_at",)