# Generated by Django 3.0.2 on 2020-02-01 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0010_user_gpa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='card_kind',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='enroll_method',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='enroll_number',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='graduate_to',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='roll_number',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='train_method',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='zip',
        ),
        migrations.AlterField(
            model_name='classcourse',
            name='details',
            field=models.CharField(max_length=255, null=True, verbose_name='上课时间、地点\t'),
        ),
    ]