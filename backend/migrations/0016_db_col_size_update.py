# Generated by Django 4.2.1 on 2024-09-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0015_log_tag_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appsetting",
            name="aws_access_key",
            field=models.CharField(blank=True, default="", max_length=1024),
        ),
        migrations.AlterField(
            model_name="appsetting",
            name="aws_secret_access_key",
            field=models.CharField(blank=True, default="", max_length=1024),
        ),
    ]