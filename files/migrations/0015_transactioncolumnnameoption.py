# Generated by Django 4.2.7 on 2023-12-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0014_rename_file_transactionfile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionColumnNameOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=25, unique=True)),
                ('value', models.JSONField()),
            ],
            options={
                'db_table': 'transaction_column_name_options',
            },
        ),
    ]