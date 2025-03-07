# Generated by Django 4.2.7 on 2024-05-03 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0012_alter_assitantvectorstore_assistant"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assitantvectorstore",
            name="assistant",
        ),
        migrations.RemoveField(
            model_name="session",
            name="file",
        ),
        migrations.AddField(
            model_name="session",
            name="vectorstore",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sessions",
                to="chat.assitantvectorstore",
            ),
        ),
    ]
