# Generated by Django 4.2.7 on 2023-12-26 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=25)),
                ('path', models.CharField(max_length=250)),
                ('ip', models.CharField(max_length=50)),
                ('user_agent', models.CharField(max_length=100)),
                ('status_code', models.PositiveIntegerField()),
                ('response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_usage_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usage_logs',
            },
        ),
    ]
