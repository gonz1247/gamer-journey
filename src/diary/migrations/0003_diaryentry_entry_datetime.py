# Generated by Django 5.2.1 on 2025-06-04 01:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_alter_diaryentry_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='entry_datetime',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 3, 18, 49, 35, 482405)),
            preserve_default=False,
        ),
    ]
