# Generated by Django 3.2.9 on 2021-11-03 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_owmuser_email_verified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owmuser",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]