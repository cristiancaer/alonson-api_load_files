# Generated by Django 4.2.7 on 2023-12-14 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0015_transactioncolumnnameoption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactioncolumnnameoption',
            old_name='value',
            new_name='values',
        ),
    ]