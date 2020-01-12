# Generated by Django 3.0.2 on 2020-01-11 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(max_length=16, primary_key=True, serialize=False, unique=True, verbose_name='学号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='最后一次登陆时间')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('strId', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='1课程号')),
                ('name', models.CharField(max_length=64, verbose_name='2课程名')),
                ('numberId', models.IntegerField(verbose_name='3课程序号')),
                ('scores', models.FloatField(verbose_name='4成绩')),
                ('credit', models.FloatField(verbose_name='5学分')),
                ('check_method', models.CharField(max_length=64, verbose_name='6考核方式')),
                ('select_properties', models.CharField(max_length=64, verbose_name='7选课属性')),
                ('status', models.CharField(max_length=64, verbose_name='8备注：正常，挂科')),
                ('exam_status', models.CharField(max_length=64, verbose_name='9考试类别')),
                ('semester_year', models.IntegerField(verbose_name='10学年')),
                ('semester_season', models.CharField(max_length=32, verbose_name='11学期')),
                ('is_delay_exam', models.BooleanField(default=False, verbose_name='12是否缓考')),
                ('details_print_id', models.CharField(max_length=128, verbose_name='13打卷申请')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Spider.User')),
            ],
        ),
    ]