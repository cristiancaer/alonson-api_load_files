# Generated by Django 4.2.7 on 2023-11-26 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0005_alter_file_unique_together_alter_file_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='loaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_files', to=settings.AUTH_USER_MODEL),
        ),
    ]
