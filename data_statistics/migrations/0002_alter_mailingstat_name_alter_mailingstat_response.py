# Generated by Django 5.0.3 on 2024-04-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_statistics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingstat",
            name="name",
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name="Название статистики рассылки"),
        ),
        migrations.AlterField(
            model_name="mailingstat",
            name="response",
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name="Ответ почтового сервера"),
        ),
    ]
