from django.db import models
from django.db.models import UniqueConstraint


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = "user"
        ordering = ['-last_login', 'username']


class Score(models.Model):
    course_id = models.CharField("课程号", max_length=32)
    name = models.CharField("课程名", max_length=64, null=True)
    course_number = models.IntegerField("选课序号", null=True)
    scores = models.CharField("成绩", max_length=16, null=True)  # 有等级制、分数制，应该为 Char
    credit = models.FloatField("学分", null=True)
    inspect_method = models.CharField("考核方式", max_length=64, null=True)
    course_properties = models.CharField("选课属性", max_length=64, null=True)
    status = models.CharField("备注：正常，挂科", max_length=64, null=True)
    exam_categories = models.CharField("考试类别", max_length=64, null=True)
    semester = models.CharField("学年学期", max_length=32)
    is_delay_exam = models.CharField("是否缓考", max_length=8, null=True)
    details_print_id = models.CharField("打卷申请ID", max_length=128, null=True)
    made_up_of = models.CharField("成绩组成", max_length=128, null=True)
    daily_score = models.CharField("平时成绩", max_length=8, null=True)
    midterm_score = models.CharField("期中成绩", max_length=8, null=True)
    exam_score = models.CharField("考试成绩", max_length=8, null=True)
    final_score = models.CharField("最终成绩", max_length=8, null=True)
    last_updated = models.DateTimeField("最后更新时间", auto_now=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = "exam_score"
        UniqueConstraint(fields=['course_id', 'semester', 'username'], name="unique_stu_score")
        ordering = ['-semester', '-last_updated']


class CET(models.Model):
    date = models.CharField("考试日期", max_length=16, null=False)
    level = models.CharField("等级", max_length=16)
    score = models.CharField("分数", max_length=16, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cet")

    def __str__(self):
        return str(self.level)

    class Meta:
        db_table = "cet"
        UniqueConstraint(fields=['username', 'date'], name="unique_stu_cet")
        ordering = ['username', '-date']


class ExamPlan(models.Model):
    name = models.CharField("课程名", max_length=64)
    room = models.CharField("考场", max_length=32)
    date = models.DateField("考试日期")
    time = models.CharField("考试时间", max_length=32)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_plan")

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "plan_exam"
        UniqueConstraint(fields=['username', 'name', 'date'], name="unique_stu_exam_plan")
        ordering = ['username', '-date']


class StudentInfo(models.Model):
    # number = models.ForeignKey(User, max_length=32, on_delete=models.CASCADE, primary_key=True)
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
    exam_number = models.CharField("高考证号", max_length=32, null=True)
    graduate_from = models.CharField("毕业高中", max_length=64, null=True)
    enroll_number = models.CharField("入学录取证号", max_length=32, null=True)
    enroll_method = models.CharField("入学方式", max_length=32, null=True)
    enroll_at = models.DateField("入学日期", null=True)
    graduate_at = models.DateField("毕业日期", null=True)
    foreign_language = models.CharField("外语语种", max_length=32, null=True)
    train_method = models.CharField("培养方案", max_length=32, null=True)
    address = models.CharField("家庭住址", max_length=255, null=True)
    zip = models.CharField("邮编", max_length=32, null=True)
    phone = models.CharField("手机号", max_length=16, null=True)
    email = models.CharField("邮箱", max_length=64, null=True)
    roll_number = models.CharField("学籍表号", max_length=64, null=True)
    source_from = models.CharField("学生来源", max_length=255, null=True)
    graduate_to = models.CharField("毕业去向", max_length=255, null=True)
    comment = models.CharField("备注", max_length=255, null=True)
    img_url = models.URLField("头像地址")
    last_updated = models.DateTimeField("最后更新时间", auto_now=True)

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = "info"
        ordering = ['-last_updated', '-number']


class TeachingPlanCourse(models.Model):
    semester = models.CharField("学年学期", max_length=32)
    course_id = models.CharField("课程号", max_length=32)
    course_name = models.CharField("课程名称", max_length=64)
    inspect_method = models.CharField("考核方式", max_length=64, null=True)
    credit = models.FloatField("学分", null=True)
    period = models.IntegerField("总学时", null=True)
    course_type = models.CharField("课程类别", max_length=16, null=True)
    course_group = models.CharField("所属分组", max_length=16, null=True)
    course_properties = models.CharField("选课属性", max_length=64, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        self.__dict__.pop("_state")
        return str(self.__dict__)

    class Meta:
        db_table = "plan_teaching"
        UniqueConstraint(fields=['course_id', 'username', 'semester'], name="unique_teaching_plan")
        ordering = ['username']
