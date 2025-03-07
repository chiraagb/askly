# Generated by Django 4.2.7 on 2024-04-22 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0004_session_thread_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="session",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
