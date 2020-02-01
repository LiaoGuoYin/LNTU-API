# Generated by Django 3.0.2 on 2020-01-30 03:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0006_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='buildingId',
            field=models.IntegerField(default=4, verbose_name='教学楼编号'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='week',
            field=models.IntegerField(default=-1, verbose_name='周'),
        ),
    ]