# Generated by Django 4.2.7 on 2024-04-29 08:22

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_rename_file_organizationfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationfile",
            name="file",
            field=models.FileField(
                upload_to=accounts.models.organization_directory_path
            ),
        ),
    ]
