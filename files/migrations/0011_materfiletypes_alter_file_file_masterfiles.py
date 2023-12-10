# Generated by Django 4.2.7 on 2023-12-10 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import files.models
import files.storages


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0010_file_uploaded_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterFileTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'master_file_types',
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=files.storages.AzureStorage(), upload_to=files.models.File.get_company_directory_path),
        ),
        migrations.CreateModel(
            name='MasterFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_filename', models.CharField(max_length=255)),
                ('file', models.FileField(storage=files.storages.AzureStorage(), upload_to=files.models.MasterFiles.get_company_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_master_files', to='companies.area')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_master_files', to='companies.company')),
                ('loaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_master_files', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_files', to='files.materfiletypes')),
            ],
            options={
                'db_table': 'master_files',
                'ordering': ('-created_at',),
                'unique_together': {('company', 'area')},
            },
        ),
    ]
