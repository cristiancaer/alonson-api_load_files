# Generated by Django 4.2.1 on 2023-11-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reset_password', '0003_changepasswordattempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changepasswordattempts',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
