# Generated by Django 5.0.3 on 2024-04-08 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="periodicity",
            field=models.CharField(
                choices=[("День", "раз в день"), ("Неделя", "раз в неделю"), ("Месяц", "раз в месяц")],
                default="Месяц",
                max_length=8,
                verbose_name="Периодичность",
            ),
        ),
    ]
