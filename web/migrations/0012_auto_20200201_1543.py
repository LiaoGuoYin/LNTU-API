# Generated by Django 3.0.2 on 2020-02-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0011_auto_20200201_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='citizenship',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='exam_number',
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='train_method',
            field=models.CharField(max_length=32, null=True, verbose_name='培养方案'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='native_from',
            field=models.CharField(max_length=64, null=True, verbose_name='国籍籍贯'),
        ),
    ]