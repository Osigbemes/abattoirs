from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel
# Create your models here.

class Abattoir(BaseModel):
    name = models.CharField(verbose_name=(_("Abattoir Name")), max_length=200)
    operatingAddress = models.CharField(verbose_name=(_("Operating Address")), max_length=200)
    contactPhone = models.CharField(verbose_name=(_("Contact Phonenumber")), max_length=200)
    emailAddress = models.EmailField(verbose_name=(_("Email Address")), max_length=200)
    accountNumber = models.CharField(verbose_name=(_("Account Number")), max_length=200)
    bankCode = models.CharField(verbose_name=(_("Bank Code")), max_length=200)
    bankName = models.CharField(verbose_name=(_("Bank Name")), max_length=200)
    accountName = models.CharField(verbose_name=(_("Account Name")), max_length=200)
    approvalNumber = models.CharField(verbose_name=(_("Approval Number")), max_length=200)
    country = models.CharField(verbose_name=(_("Country")), max_length=200)
    state = models.CharField(verbose_name=(_("State")), max_length=200)
    
    class Meta:
        verbose_name = _("Abattoir")
        verbose_name_plural = _("Abattoirs")
        
    def __str__(self):
        return self.name