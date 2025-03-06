# Generated by Django 4.2.7 on 2024-04-29 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0010_assitantvectorstore_assistantfile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assistant",
            name="vector_store_id",
        ),
        migrations.AddField(
            model_name="assitantvectorstore",
            name="assistant",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vectorstore",
                to="chat.assistant",
            ),
            preserve_default=False,
        ),
    ]
