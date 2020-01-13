from django.db import models


class User(models.Model):
    __tablename__ = 'user'

    userId = models.CharField("学号", max_length=16, primary_key=True, unique=True)
    password = models.CharField("密码", max_length=32)
    last_login = models.DateTimeField("最后一次登陆时间", auto_now_add=True)


class Score(models.Model):
    __tablename__ = 'score'

    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    strId = models.CharField("1课程号", max_length=64, primary_key=True, unique=True)
    name = models.CharField("2课程名", max_length=64)
    numberId = models.IntegerField("3课程序号")
    scores = models.CharField("4成绩", max_length=16)  # 有等级制、分数制，应该为 Char
    credit = models.FloatField("5学分")
    check_method = models.CharField("6考核方式", max_length=64)
    select_properties = models.CharField("7选课属性", max_length=64)
    status = models.CharField("8备注：正常，挂科", max_length=64)
    exam_status = models.CharField("9考试类别", max_length=64)
    semester_year = models.IntegerField("10学年")
    semester_season = models.CharField("11学期", max_length=32)
    is_delay_exam = models.BooleanField("12是否缓考", default=False)
    details_print_id = models.CharField("13打卷申请", max_length=128)
    score_composition = models.CharField("成绩组成", max_length=128)
    daily_score = models.IntegerField("平时成绩")
    midterm_score = models.IntegerField("期中成绩")
    exam_score = models.IntegerField("考试成绩")
    final_score = models.IntegerField("最终成绩")


class CET(models.Model):
    __tablename__ = 'CET'

    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=64)
    exam_date = models.DateField()
    score = models.IntegerField()


class ExamPlan(models.Model):
    __table__ = 'exam'

    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=64)
    date = models.DateField()
    time = models.DateTimeField()
    location = models.CharField(max_length=32)
