from enum import Enum, unique


@unique
class UrlEnums(Enum):
    # URL_ROOT = "http://202.199.224.24:11189/academic/"
    URL_ROOT = "http://202.199.224.24:11089/newacademic/"

    LOGIN = URL_ROOT + "j_acegi_security_check"
    STUDENT_INFO = URL_ROOT + "student/studentinfo/studentinfo.jsdo"
    TEACHING_PLAN = URL_ROOT + "student/studyschedule/"
    TEACHING_PLAN_IDS = URL_ROOT + "student/studyschedule/studyschedule.jsdo"
    CLASS_TABLE = URL_ROOT + "student/currcourse/currcourse.jsdo"
    TEACHER_EVALUATE_QUERY = URL_ROOT + "eva/index/resultlist.jsdo"
    TEACHER_EVALUATE = URL_ROOT + "eva/index/putresult.jsdo"
    EXAM_PLAN = URL_ROOT + "student/exam/index.jsdo"
    SCORE = URL_ROOT + "student/queryscore/queryscore.jsdo"
    UN_PASS = URL_ROOT + "student/unpasscourse/unpasscourse.jsdo"
    SCORES_DETAIL = URL_ROOT + "student/queryscore/"
    CET = URL_ROOT + "student/queryscore/skilltestscore.jsdo"
    EDU_PLAN = URL_ROOT + "student/studyschedule/studyschedule_view_byterm.jsdo?studentId=2884962&classId=11611"  # TODO 参数

    def __str__(self):
        return self.value

# for name, member in UrlEnums.__members__.items():
#     print(name.lower(), member.value)
# # print(list(UrlEnums))
