# Generated by Django 4.2.7 on 2023-12-14 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0019_transaction_index_in_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('file', 'index_in_file')},
        ),
    ]
