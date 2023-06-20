from django.contrib import admin
from apps.abattoirs.models import Abattoir

@admin.register(Abattoir)
class AbattoirAdmin(admin.ModelAdmin):
    list_display = ('name', 'emailAddress', 'country', 'state', 'created_at')
    search_fields = ("name", "country", "state")
    list_filter = ("created_at", )