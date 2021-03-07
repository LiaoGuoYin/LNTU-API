import hashlib
import re
import time

import requests
from lxml import etree
from requests import Session
from sentry_sdk import capture_message
from starlette import status

from app import schemas, exceptions
from app.education import parser
from app.education.urls import URLEnum, ClassTableTypeEnum
from app.education.utils import save_html_to_file
from app.constants import constantsShared


def is_education_online() -> bool:
    try:
        response = requests.head(URLEnum.LOGIN.value, timeout=(1, 3))
        if response.status_code == 200:
            return True
        else:
            raise exceptions.NetworkException("教务无响应，爆炸爆炸，请稍后重试")
    except (requests.exceptions.RequestException, requests.exceptions.RequestException, exceptions.NetworkException):
        return False


def login(username: str, password: str) -> Session:
    if not is_education_online():
        raise exceptions.NetworkException("教务无响应，爆炸爆炸，请稍后重试")
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/86.0.4240.111 Safari/537.36',
        'Connection': 'close',
    }
    session.keep_alive = False
    response = session.get(URLEnum.LOGIN.value)
    token = re.findall(r"SHA1\('(.*?)'", response.text)[0]
    if token is None:
        raise exceptions.SpiderParserException("页面上没找到 SHA1token")
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    time.sleep(0.48)  # 延迟 0.48 秒防止被 ban
    response = session.post(URLEnum.LOGIN.value, data={'username': username, 'password': key})
    if '密码错误' in response.text:
        raise exceptions.FormException(F"{username} 用户名或密码错误")
    elif '请不要过快点击' in response.text:
        raise exceptions.AccessException("页面请求过快")
    elif '账户不存在' in response.text:
        raise exceptions.FormException(F"{username} 用户不存在")
    elif '超过人数上限' in response.text:
        raise exceptions.FormException("超过人数上限，请稍后再试，请稍后重试")
    elif '您当前位置' in response.text:
        return session
    elif 'security.AccountExpired' in response.text:
        raise exceptions.FormException("账号已到期，可能是已经毕业")
    else:
        raise exceptions.AccessException("页面未知错误，请稍后重试")


def get_stu_info(username: str, password: str, session=None, is_save: bool = False) -> schemas.UserInfo:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.STUDENT_INFO.value)
    if "学籍信息" in response.text:
        if is_save:
            save_html_to_file(response.text, 'info')
        html_doc = etree.HTML(response.text)
        return parser.parse_stu_info(username=username, html_doc=html_doc)
    else:
        raise exceptions.SpiderParserException("[个人信息页]获取失败，请稍后重试")


def get_plan(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.PlanGroup]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.PLAN.value)
    if is_save:
        save_html_to_file(response.text, 'plan')
    if '计划完成情况' in response.text:
        return parser.parse_plan(html_doc=etree.HTML(response.text))
    elif '请先完成评教' in response.text:
        raise exceptions.FormException("请完成评教后重试")
    else:
        raise exceptions.SpiderParserException("[个人培养方案完成情况页]获取失败，请稍后重试")


def get_course_table(username: str, password: str, semester_id: int = constantsShared.current_semester_id,
                     session: Session = None, course_table_type: str = ClassTableTypeEnum.classes.value,
                     is_save: bool = False) -> [schemas.CourseTable]:
    def get_std_ids(tmp_session):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = tmp_session.get(URLEnum.COURSE_TABLE_OF_STD_IDS.value)
        if is_save:
            save_html_to_file(response_inner.text, 'get_ids')
        stu_id_list = re.findall(r'\(form,"ids","(.*?)"\);', response_inner.text)
        if len(stu_id_list) is None:
            raise exceptions.SpiderParserException("页面上没找到 ids，请稍后重试")
        else:
            return stu_id_list[0] if course_table_type == ClassTableTypeEnum.student.value else stu_id_list[1]

    if not session:
        session = login(username, password)
    ids = get_std_ids(session)
    response = session.get(URLEnum.COURSE_TABLE.value, params={
        'ignoreHead': 1,
        'setting.kind': course_table_type,  # std/class
        'ids': ids,
        'semester.id': semester_id,
    })
    html_text = response.text
    if is_save:
        save_html_to_file(html_text, 'course-table')
    if "课表格式说明" in html_text:
        part_course_list = parser.parse_course_table_bottom(html_doc=etree.HTML(html_text))
        return parser.parse_course_table_body(html_text, course_dict_list=part_course_list)
    else:
        capture_message("[课表页]获取失败，请稍后重试")
        return []


def get_grade(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.Grade]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.GRADE.value)
    if is_save:
        save_html_to_file(response.text, 'grade')
    if '学年学期' in response.text:
        return parser.parse_grade(html_doc=etree.HTML(response.text))
    elif '所有成绩尚未发布' in response.text:
        return []
    else:
        raise exceptions.SpiderParserException("[成绩查询页]请求失败，请稍后重试")


def get_grade_table(username: str, password: str, session: Session = None, is_save: bool = False) -> [
    schemas.GradeTable]:
    # 备用：获取成绩表格
    if not session:
        session = login(username, password)
    response = session.post(URLEnum.GRADE_TABLE.value, params={'template': 'grade.origin'})
    if is_save:
        save_html_to_file(response.text, 'grade-table')
    if '个人成绩总表打印' in response.text:
        return parser.parse_grade_table(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[总成绩查询页]获取失败，请稍后重试")


def get_exam(username: str, password: str, semester_id: int = constantsShared.current_semester_id,
             session: Session = None, is_save: bool = False) -> [schemas.Exam]:
    def get_exam_id_list(tmp_session, inner_semester_id, inner_is_save) -> [int]:
        response_inner = tmp_session.get(URLEnum.EXAM_OF_BATCH_ID.value, params={'semester.id': inner_semester_id})
        if inner_is_save:
            save_html_to_file(response_inner.text, 'exam-batch-id')

        batch_id_dict = parser.parse_exam_id(etree.HTML(response_inner.text))
        return [] if len(batch_id_dict) == 0 else batch_id_dict.values()

    exam_list = []
    if not session:
        session = login(username, password)
    current_semester_exam_batch_id_list = get_exam_id_list(session, semester_id, is_save)
    previous_semester_exam_batch_id_list = get_exam_id_list(session,
                                                            constantsShared.get_semester_id(
                                                                constantsShared.get_previous_semester(
                                                                    constantsShared.get_semester_from_semester_id(
                                                                        semester_id
                                                                    )
                                                                )
                                                            ),
                                                            is_save)
    exam_batch_id_list = list(previous_semester_exam_batch_id_list) + list(current_semester_exam_batch_id_list)
    for batch_id in exam_batch_id_list:
        response = session.get(URLEnum.EXAM.value, params={'examBatch.id': batch_id})
        if '课程序号' in response.text:
            html_content = etree.HTML(response.text)

            if batch_id in current_semester_exam_batch_id_list \
                    and batch_id not in previous_semester_exam_batch_id_list:

                current_parse_result = parser.parse_exam(html_doc=html_content)

            elif batch_id in previous_semester_exam_batch_id_list \
                    and batch_id not in current_semester_exam_batch_id_list:

                current_parse_result = parser.parse_exam_makeup_only(html_doc=html_content)

            else:
                raise exceptions.ExamException(f"exam的batch_id意外的在当前学期和上学期都出现过，请修复。出现问题的batch_id值为 {batch_id}")

            exam_list.extend(current_parse_result)

        if is_save:
            save_html_to_file(response.text, 'exam')

    return exam_list


def get_other_exam(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.OtherExam]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.OTHER_EXAM.value)
    if is_save:
        save_html_to_file(response.text, 'other-exam')
    if '资格考试' in response.text:
        return parser.parse_other_exam(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[资格考试页]获取失败，请稍后重试")


def evaluate_teacher(username: str, password: str, submit: bool, session: Session = None,
                     is_save: bool = False) -> (int, str, [schemas.TeacherEvaluationResponse]):
    def submit_evaluation(semester_id: int, course_id: int, session: Session = None) -> bool:
        response = session.post(URLEnum.EVALUATE_SUBMIT.value, data={
            "teacher.id": "",
            "semester.id": semester_id,
            "evaluationLesson.id": course_id,
            "result1_0.questionName": "1.该课程每节课的学习目标清晰。",
            "result1_0.content": "赞成",
            "result1_0.score": "0.5",
            "result1_1.questionName": "2.该课程学习资源满足我的学习需要。",
            "result1_1.content": "赞成",
            "result1_1.score": "0.5",
            "result1_2.questionName": "3.教师与我们沟通交流及时、顺畅。",
            "result1_2.content": "赞成",
            "result1_2.score": "0.5",
            "result1_3.questionName": "4.我的学习表现得到教师及时反馈。",
            "result1_3.content": "赞成",
            "result1_3.score": "0.5",
            "result1_4.questionName": "5.教师讲授能够激发我的学习兴趣、调动我的学习积极性。",
            "result1_4.content": "赞成",
            "result1_4.score": "0.5",
            "result1_5.questionName": "6.教师能够帮助我改进学习方法。",
            "result1_5.content": "赞成",
            "result1_5.score": "0.5",
            "result1_6.questionName": "7.教师能够关注我的学习效果。",
            "result1_6.content": "赞成",
            "result1_6.score": "0.5",
            "result1_7.questionName": "8.教师能够客观公正地评价我的学习水平。",
            "result1_7.content": "赞成",
            "result1_7.score": "0.5",
            "result1_8.questionName": "9.我的学习成果达到课程要求。",
            "result1_8.content": "赞成",
            "result1_8.score": "0.5",
            "result1_9.questionName": "10.该课程使我的表达、沟通能力得到提高。",
            "result1_9.content": "赞成",
            "result1_9.score": "0.5",
            "result1Num": "10",
            "result2Num": "0",
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return True if response.status_code == 200 else False

    if not session:
        session = login(username, password)
    response = session.get(URLEnum.EVALUATE.value)
    if is_save:
        save_html_to_file(response.text, 'evaluation')
    if '评教' in response.text:
        evaluation_list = parser.parse_teacher_evaluation(html_doc=etree.HTML(response.text))
        if submit:  # 一键评教 Mode
            submit_evaluation_count = 0
            for each in evaluation_list:
                if each.status == '评教完成':
                    continue
                else:
                    if submit_evaluation(constantsShared.current_semester_id, each.id, session=session):
                        each.status = '评教完成'
                        submit_evaluation_count += 1
            return status.HTTP_200_OK, f'一键评教成功，共完成 {submit_evaluation_count} 条教师评价（好评）', evaluation_list
        else:  # 查询评教状态 Mode
            need_to_submit_evaluation_count = 0
            for each in evaluation_list:
                if each.status != '评教完成':
                    need_to_submit_evaluation_count += 1
            if need_to_submit_evaluation_count == 0:
                return status.HTTP_404_NOT_FOUND, f'查询评教状态成功，本学期共 {len(evaluation_list)} 门课程，已经全部完成评教，无需进一步操作', evaluation_list
            else:
                return status.HTTP_200_OK, f'查询评教状态成功，本学期共 {len(evaluation_list)} 门课程，还有 {need_to_submit_evaluation_count} 门课程没有完成评教，可以进一步一键评教', evaluation_list
    else:
        raise exceptions.SpiderParserException("[教室评价页]获取失败，请稍后重试")
