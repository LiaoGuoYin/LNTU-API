# Generated by Django 3.0.2 on 2020-01-28 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='course_id',
            field=models.CharField(max_length=32, verbose_name='课程号'),
        ),
        migrations.AlterModelTable(
            name='examplan',
            table='plan_exam',
        ),
        migrations.CreateModel(
            name='TeachingPlanCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=32, verbose_name='学年学期')),
                ('course_id', models.CharField(max_length=32, verbose_name='课程号')),
                ('course_name', models.CharField(max_length=64, verbose_name='课程名称')),
                ('inspect_method', models.CharField(max_length=64, null=True, verbose_name='考核方式')),
                ('credit', models.FloatField(null=True, verbose_name='学分')),
                ('period', models.IntegerField(null=True, verbose_name='总学时')),
                ('course_type', models.CharField(max_length=16, null=True, verbose_name='课程类别')),
                ('course_group', models.CharField(max_length=16, null=True, verbose_name='所属分组')),
                ('course_properties', models.CharField(max_length=64, null=True, verbose_name='选课属性')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.User')),
            ],
            options={
                'db_table': 'plan_teaching',
                'ordering': ['username'],
            },
        ),
    ]
