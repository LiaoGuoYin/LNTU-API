# Generated by Django 3.0.2 on 2020-02-01 05:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0009_auto_20200131_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='GPA',
            field=models.IntegerField(null=True, verbose_name='Grade Point Average'),
        ),
    ]