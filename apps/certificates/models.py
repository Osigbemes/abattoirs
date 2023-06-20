from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel
from apps.abattoirs.models import Abattoir

class Certificate(BaseModel):
    code = models.CharField(verbose_name=(_("Certificate code")), max_length=200)
    issuedBy = models.UUIDField(verbose_name=(_("Issued By")), max_length=200)
    abattoir = models.OneToOneField(Abattoir, on_delete=models.CASCADE, related_name="abattoir")
    beefWeightInKg = models.DecimalField(max_digits=4, decimal_places=3)
    # distributor = models.OneToOneField(Distributor, on_delete=models.CASCADE, related_name="distributor")
    animalSpecie = models.CharField(verbose_name=(_("Animal Specie")), max_length=200)
    typeOfParts = models.CharField(verbose_name=(_("Types Of Part")), max_length=200)
    typeOfPackaging = models.CharField(verbose_name=(_("Types Of Packaging")), max_length=200)
    numberOfParts = models.IntegerField(verbose_name=(_("Number Of Parts")))
    identificationMark = models.CharField(max_length=200)
    dispatchedTo = models.CharField(verbose_name=(_("Dispatched To")), max_length=200)
    serialNumberOfCarcass = models.CharField(max_length=200)
    dispatchedTo = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")
        
    def __str__(self):
        return self.abattoir.name