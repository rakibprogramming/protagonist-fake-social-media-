# Generated by Django 5.0.7 on 2025-03-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_notification_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='time',
            field=models.CharField(default='1742224146.9047246', max_length=30),
        ),
    ]
