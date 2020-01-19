from django.db import models
from django.db.models import UniqueConstraint


class User(models.Model):
    username = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=32)
    latest_login = models.DateTimeField(auto_now=True)


class Score(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score")
    id = models.AutoField(primary_key=True)
    strId = models.CharField("1课程号", max_length=64)
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
    is_delay_exam = models.CharField("12是否缓考", max_length=8)
    details_print_id = models.CharField("13打卷申请", max_length=128, null=True)
    score_composition = models.CharField("成绩组成", max_length=128, null=True)
    daily_score = models.CharField("平时成绩", max_length=8, null=True)
    midterm_score = models.CharField("期中成绩", max_length=8, null=True)
    exam_score = models.CharField("考试成绩", max_length=8, null=True)
    final_score = models.CharField("最终成绩", max_length=8, null=True)

    class Meta:
        UniqueConstraint(fields=['strId', 'semester_year', 'semester_season', 'username'], name="unique_stu_score")

        def __str__(self):
            return str(self.__dict__)


class CET(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cet")
    id = models.AutoField(primary_key=True)
    exam_date = models.DateField(null=False)
    level = models.CharField(max_length=64)
    score = models.CharField(max_length=16, null=True)

    class Meta:
        UniqueConstraint(fields=['exam_date', 'username'], name="unique_stu_cet")

    def __str__(self):
        return str(self.level)


class ExamPlan(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="examPlan")
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=64)
    date = models.DateField()
    time = models.DateTimeField()
    location = models.CharField(max_length=32)

    class Meta:
        UniqueConstraint(fields=['id', 'course', 'username'], name="unique_stu_examPlan")

    def __str__(self):
        return str(self.__dict__)
