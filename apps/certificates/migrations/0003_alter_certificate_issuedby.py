# Generated by Django 4.1.7 on 2023-06-23 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certificates', '0002_alter_certificate_issuedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='issuedBy',
            field=models.OneToOneField(default=1, max_length=200, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Issued By'),
        ),
    ]
