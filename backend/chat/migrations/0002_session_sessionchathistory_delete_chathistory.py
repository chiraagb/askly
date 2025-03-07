# Generated by Django 4.2.7 on 2024-04-11 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SessionChatHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("is_user_message", models.BooleanField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_history",
                        to="chat.session",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ChatHistory",
        ),
    ]
