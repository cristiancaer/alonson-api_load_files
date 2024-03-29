# Generated by Django 4.2.7 on 2023-12-14 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0017_transactioncolumnnameoption_is_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_reprocessing',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='credit',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='debit',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='final_balance',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='initial_balance',
            field=models.FloatField(),
        ),
    ]
