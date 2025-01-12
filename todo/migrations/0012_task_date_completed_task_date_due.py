# Generated by Django 4.2.8 on 2023-12-20 15:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0011_alter_task_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="date_completed",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="date_due",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
