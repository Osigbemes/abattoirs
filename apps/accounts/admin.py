from django.contrib import admin
from apps.accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "firstname", "lastname", "created_at", )
    search_fields = ("email", "firstname", "lastname", )
    list_filter = ("created_at", )