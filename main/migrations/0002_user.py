# Generated by Django 5.0.7 on 2025-03-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=200)),
                ('sessonId', models.CharField(max_length=100)),
                ('userName', models.CharField(max_length=200)),
            ],
        ),
    ]
