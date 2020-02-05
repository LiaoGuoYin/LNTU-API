from django.db import models


class Student(models.Model):
    sunny_id = models.IntegerField(primary_key=True)
    number = models.CharField("学号", max_length=32, null=True)
    name = models.CharField("姓名", max_length=32, null=True)
    gender = models.CharField("性别", max_length=8, null=True)
    school = models.CharField("学校", max_length=64, null=True)
    college = models.CharField("院系", max_length=32, null=True)
    i_class = models.CharField("班级", max_length=32, null=True)
    total_records = models.IntegerField(null=True)
    morning_records = models.IntegerField(null=True)
    success_records = models.IntegerField(null=True)
    failure_records = models.IntegerField(null=True)

    class Meta:
        db_table = "aipao_user"


class Success(models.Model):
    IIDD = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField("学号", max_length=32, null=True)
    name = models.CharField("姓名", max_length=32)
    type = models.CharField("长跑类型", max_length=32)
    client_type = models.CharField("客户端类型", max_length=32)
    speed = models.FloatField("配速", null=True)
    step = models.IntegerField("步数", null=True)
    cost_time_min = models.CharField("花费时间(min)", max_length=16, null=True)
    cost_time_s = models.FloatField("花费时间(s)", null=True)
    distance = models.FloatField("跑步距离", null=True)
    standard_distance = models.FloatField("标准距离", null=True)
    date = models.DateField("开始日期", null=True)
    time = models.CharField("开始时刻", null=True, max_length=16)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = "aipao_success"

    def __str__(self):
        return str(self.__dict__)


class Failure(models.Model):
    IIDD = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField("学号", max_length=32, null=True)
    name = models.CharField("姓名", max_length=32)
    type = models.CharField("长跑类型", max_length=32)
    client_type = models.CharField("客户端类型", max_length=32)
    speed = models.FloatField("配速", null=True)
    step = models.IntegerField("步数", null=True)
    cost_time_min = models.CharField("花费时间(min)", max_length=16, null=True)
    cost_time_s = models.FloatField("花费时间(s)", null=True)
    distance = models.FloatField("跑步距离", null=True)
    standard_distance = models.FloatField("标准距离", null=True)
    date = models.DateField("开始日期", null=True)
    time = models.CharField("开始时刻", null=True, max_length=16)
    reason = models.CharField("失败原因", max_length=32)
    reason_id = models.IntegerField("失败原因 ID", null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = "aipao_failure"

    def __str__(self):
        return str(self.__dict__)
