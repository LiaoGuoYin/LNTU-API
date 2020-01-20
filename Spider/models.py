from django.db import models
from django.db.models import UniqueConstraint


class User(models.Model):
    username = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=32)
    latest_login = models.DateTimeField(auto_now=True)


class Score(models.Model):
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
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score")

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        UniqueConstraint(fields=['strId', 'semester_year', 'semester_season', 'username'], name="unique_stu_score")


class CET(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cet")
    id = models.AutoField(primary_key=True)
    exam_date = models.DateField(null=False)
    level = models.CharField(max_length=64)
    score = models.CharField(max_length=16, null=True)

    def __str__(self):
        return str(self.level)

    class Meta:
        UniqueConstraint(fields=['exam_date', 'username'], name="unique_stu_cet")


class ExamPlan(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="examPlan")
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=64)
    date = models.DateField()
    time = models.DateTimeField()
    room = models.CharField(max_length=32)

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        UniqueConstraint(fields=['id', 'course', 'username'], name="unique_stu_examPlan")


class StudentInfo(models.Model):
    # number = models.ForeignKey(User, max_length=32, on_delete=models.CASCADE, primary_key=True)  # 学号
    number = models.CharField(max_length=32, primary_key=True)  # 学号
    name = models.CharField(max_length=64)  # 姓名
    citizenship = models.CharField(max_length=64, null=True)  # 国籍
    native_from = models.CharField(max_length=64, null=True)  # 籍贯
    foreign_name = models.CharField(max_length=64, null=True)
    birthday = models.DateField(null=True)  # 出生年月
    card_kind = models.CharField(max_length=32)  # 证件类型
    ID_number = models.CharField(max_length=32)  # 证件号
    politics = models.CharField(max_length=64, null=True)  # 政治面貌
    section = models.CharField(max_length=64, null=True)  # 乘车区间
    gender = models.CharField(max_length=32)  # 性别
    nation = models.CharField(max_length=32, null=True)  # 民族
    academy = models.CharField(max_length=64)  # 学院
    major = models.CharField(max_length=64)  # 专业
    class_number = models.CharField(max_length=32)  # 班级
    category = models.CharField(max_length=32, null=True)  # 考生类别
    province = models.CharField(max_length=32, null=True)  # 高考考区
    score = models.FloatField(null=True)  # 高考分数
    exam_number = models.CharField(max_length=32, null=True)  # 高考证号
    graduate_from = models.CharField(max_length=64, null=True)  # 高中学校
    foreign_language = models.CharField(max_length=32, null=True)  # 外语语种
    enroll_number = models.CharField(max_length=32, null=True)  # 入学录取证号
    enroll_method = models.CharField(max_length=32, null=True)  # 入学方式
    enroll_at = models.DateField(null=True)  # 入学日期
    graduate_at = models.DateField(null=True)  # 毕业日期
    train_method = models.CharField(max_length=32, null=True)  # 培养方式
    address = models.CharField(max_length=255, null=True)  # 家庭住址
    zip = models.CharField(max_length=32, null=True)  # 邮政编码
    phone = models.CharField(max_length=16, null=True)  # 联系电话
    email = models.CharField(max_length=64, null=True)  # 邮箱
    roll_number = models.CharField(max_length=64, null=True)  # 学籍表号
    source_from = models.CharField(max_length=255, null=True)  # 学生来源
    graduate_to = models.CharField(max_length=255, null=True)  # 毕业去向
    comment = models.CharField(max_length=255, null=True)  # 备注

    def __str__(self):
        return str(self.__dict__)
