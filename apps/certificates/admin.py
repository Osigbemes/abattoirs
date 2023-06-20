from django.contrib import admin
from apps.certificates.models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('abattoir', 'animalSpecie', 'typeOfParts', 'numberOfParts', 'dispatchedTo', 'serialNumberOfCarcass', 'created_at')
    search_fields = ("abattoir", "serialNumberOfCarcass", )
    list_filter = ("created_at", )