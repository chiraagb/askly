# Generated by Django 4.2.7 on 2024-04-29 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_organization_user_organization"),
        ("chat", "0006_pdfdetail"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assistant",
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
                ("assistant_id", models.CharField(max_length=50)),
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.organization",
                    ),
                ),
            ],
        ),
    ]
