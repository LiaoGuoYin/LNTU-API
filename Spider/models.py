from django.db import models
from django.db.models import UniqueConstraint


class User(models.Model):
    username = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=32)
    latest_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"


class Score(models.Model):
    strId = models.CharField("课程号", max_length=64)
    name = models.CharField("课程名", max_length=64)
    numberId = models.IntegerField("选课序号")
    scores = models.CharField("成绩", max_length=16)  # 有等级制、分数制，应该为 Char
    credit = models.FloatField("学分")
    check_method = models.CharField("考核方式", max_length=64)
    select_properties = models.CharField("选课属性", max_length=64)
    status = models.CharField("备注：正常，挂科", max_length=64)
    exam_status = models.CharField("考试类别", max_length=64)
    semester_year = models.IntegerField("学年")
    semester_season = models.CharField("学期", max_length=32)
    is_delay_exam = models.CharField("是否缓考", max_length=8)
    details_print_id = models.CharField("打卷申请", max_length=128, null=True)
    score_composition = models.CharField("成绩组成", max_length=128, null=True)
    daily_score = models.CharField("平时成绩", max_length=8, null=True)
    midterm_score = models.CharField("期中成绩", max_length=8, null=True)
    exam_score = models.CharField("考试成绩", max_length=8, null=True)
    final_score = models.CharField("最终成绩", max_length=8, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score")

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = "score"
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
        db_table = "cet"
        UniqueConstraint(fields=['exam_date', 'username'], name="unique_stu_cet")


class ExamPlan(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="examPlan")
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=64)
    room = models.CharField(max_length=32)
    date = models.DateField()
    time = models.DateTimeField()

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = "exam"
        UniqueConstraint(fields=['id', 'course', 'username'], name="unique_stu_examPlan")


class StudentInfo(models.Model):
    # number = models.ForeignKey(User, max_length=32, on_delete=models.CASCADE, primary_key=True)  # 学号
    number = models.CharField("学号", max_length=32, primary_key=True)
    name = models.CharField("姓名", max_length=64)
    citizenship = models.CharField("国籍", max_length=64, null=True)
    native_from = models.CharField("籍贯", max_length=64, null=True)
    foreign_name = models.CharField("外语", max_length=64, null=True)
    birthday = models.DateField("出生年月", null=True)
    card_kind = models.CharField("证件类型", max_length=32)
    ID_number = models.CharField("证件号", max_length=32)
    politics = models.CharField("政治面貌", max_length=64, null=True)
    section = models.CharField("乘车区间", max_length=64, null=True)
    gender = models.CharField("性别", max_length=32)  #
    nation = models.CharField("民族", max_length=32, null=True)
    academy = models.CharField("学院", max_length=64)
    major = models.CharField("专业", max_length=64)
    class_number = models.CharField("学号", max_length=32)
    category = models.CharField("班级", max_length=32)
    province = models.CharField("高考考区", max_length=32, null=True)
    score = models.FloatField("高考分数", null=True)  #
    exam_number = models.CharField("学号", max_length=32, null=True)
    graduate_from = models.CharField("高中学校", max_length=64, null=True)
    enroll_number = models.CharField("入学录取证号", max_length=32, null=True)
    enroll_method = models.CharField("入学方式", max_length=32, null=True)
    enroll_at = models.DateField("入学日期", null=True)
    graduate_at = models.DateField("学号",
                                   null=True)  # 毕业日期    foreign_language = models.CharField("学号", max_length=32, null=True)  #
    train_method = models.CharField("学号", max_length=32, null=True)
    address = models.CharField("家庭住址", max_length=255, null=True)
    zip = models.CharField("学号", max_length=32, null=True)
    phone = models.CharField("手机号", max_length=16, null=True)
    email = models.CharField("邮箱", max_length=64, null=True)
    roll_number = models.CharField("学号", max_length=64, null=True)  #
    source_from = models.CharField("学号", max_length=255, null=True)  # 学生来源
    graduate_to = models.CharField("学号", max_length=255, null=True)  # 毕业去向
    comment = models.CharField("学号", max_length=255, null=True)  # 备注
    img_url = models.URLField("学号", )  # 头像地址
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = "stu_info"
