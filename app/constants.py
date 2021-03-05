import yaml
import os

from app import schemas


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class Constants:
    def __init__(self):
        self.config = self._load_config_yaml()
        self.current_semester, self.current_week = self.calculate_semester_and_week(self.config.semesterStartDate)
        self.current_semester_id = self.semester.get(self.current_semester, '2020-秋')

    def _load_config_yaml(self) -> schemas.YamlConfig:
        with open(os.path.join(self.app_path, 'config.yaml'), encoding='utf-8') as fp:
            yaml_config = yaml.load(fp, Loader=yaml.BaseLoader)
        try:
            config = schemas.YamlConfig(
                message=yaml_config['message'],
                sentryURL=yaml_config['sentryUrl'],
                semesterStartDate=yaml_config['semesterStartDate'],
                host=yaml_config['mysql']['host'],
                port=yaml_config['mysql']['port'],
                user=yaml_config['mysql']['user'],
                password=yaml_config['mysql']['password'],
                database=yaml_config['mysql']['database'],
                testDatabase=yaml_config['mysql']['testDatabase'],
                educationUsername=yaml_config['account']['educationUsername'],
                educationPassword=yaml_config['account']['educationPassword'],
                qualityUsername=yaml_config['account']['qualityUsername'],
                qualityPassword=yaml_config['account']['qualityPassword'],
                bundleId=yaml_config['apple']['bundleId'],
                teamId=yaml_config['apple']['teamId'],
                keyId=yaml_config['apple']['keyId'],
                keyPath=yaml_config['apple']['keyPath'],
            )
            return config
        except KeyError as e:
            print('config.yaml 配置文件有误', e)
            exit(0)

    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    building = {'eyl': 20, 'jyl': 11, 'hldwlsys': 16, 'hldjf': 21, 'yhl': 14, 'bwl': 7, 'byl': 13, 'xhl': 19,
                'zhl': 17, 'zyl': 18, 'zxl': 8, 'wlsys': 15, 'zljf': 9}
    # building_str = {'fuxin': {'博文楼': 7, '博雅楼': 13, '新华楼': 19, '中和楼': 17, '致远楼': 18, '知行楼': 8, '物理实验室': 15, '主楼机房': 9},
    #                  'huludao': {'尔雅楼': 20, '静远楼': 11, '葫芦岛物理实验室': 16, '葫芦岛机房': 21, '耘慧楼': 14}}

    semester = {'2008-秋': 636, '2009-春': 637,
                '2009-秋': 643, '2010-春': 635,
                '2010-秋': 639, '2011-春': 632,
                '2011-秋': 628, '2012-春': 641,
                '2012-秋': 629, '2013-春': 640,
                '2013-秋': 645, '2014-春': 630,
                '2014-秋': 634, '2015-春': 631,
                '2015-秋': 623, '2016-春': 621,
                '2016-秋': 624, '2017-春': 619,
                '2017-秋': 625, '2018-春': 622,
                '2018-秋': 633, '2019-春': 642,
                '2019-秋': 620, '2020-春': 626,
                '2020-秋': 627, '2021-春': 662,
                '2021-秋': 663, '2022-春': 664,
                '2022-秋': 665, '2023-春': 666,
                '2023-秋': 667, '2024-春': 668}

    @staticmethod
    def calculate_semester_and_week(semester_start_date) -> (str, str):
        from datetime import datetime
        start = datetime.strptime(semester_start_date, '%Y-%m-%d')
        semester = f"{start.year}-{'秋' if start.month in [7, 8, 9, 10, 11, 12] else '春'}"
        delta = datetime.today() - start
        week = str((delta.days // 7) + 1)
        if int(week) < 0:
            week = 1
        return semester, week

    def get_local_html_file_dict(self) -> dict:
        return {
            'config': os.path.join(self.app_path, 'config.yaml'),
            'info': os.path.join(self.app_path, 'app/tests/static/', 'info.html'),
            'course-table': os.path.join(self.app_path, 'app/tests/static/', 'course-table.html'),
            'grade': os.path.join(self.app_path, 'app/tests/static/', 'grade.html'),
            'grade-table': os.path.join(self.app_path, 'app/tests/static/', 'grade-table.html'),
            'exam': os.path.join(self.app_path, 'app/tests/static/', 'exam.html'),
            'exam-batch-id': os.path.join(self.app_path, 'app/tests/static/', 'exam-batch-id.html'),
            'other-exam': os.path.join(self.app_path, 'app/tests/static/', 'other-exam.html'),
            'plan': os.path.join(self.app_path, 'app/tests/static/', 'plan.html'),
            'class-room-building': os.path.join(self.app_path, 'app/tests/static/', 'class-room-building.html'),
            'class-room': os.path.join(self.app_path, 'app/tests/static/', 'class-room.html'),
            'quality-report': os.path.join(self.app_path, 'app/tests/static/', 'quality-report.html'),
            'quality-activity': os.path.join(self.app_path, 'app/tests/static/', 'quality-activity.html'),
            'evaluation': os.path.join(self.app_path, 'app/tests/static/', 'evaluation.html'),
        }

    def get_education_user_dict(self) -> dict:
        return {
            'username': self.config.educationUsername,
            'password': self.config.educationPassword,
        }

    def get_quality_user_dict(self) -> dict:
        return {
            'username': self.config.qualityUsername,
            'password': self.config.qualityPassword,
        }

    def get_db_url_dict(self):
        return {
            'production': f'mysql+pymysql://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}?charset=utf8',
            'test': f'mysql+pymysql://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.testDatabase}?charset=utf8',
        }

    def get_apple_push_dict(self):
        return {
            'bundleId': self.config.bundleId,
            'teamId': self.config.teamId,
            'keyId': self.config.keyId,
            'keyPath': self.config.keyPath,
        }

    def get_current_week(self):
        self.current_semester, self.current_week = self.calculate_semester_and_week(self.config.semesterStartDate)
        self.current_semester_id = self.semester.get(self.current_semester, '2020-秋')
        return self.current_week

    def get_current_semester(self):
        self.current_semester, self.current_week = self.calculate_semester_and_week(self.config.semesterStartDate)
        self.current_semester_id = self.semester.get(self.current_semester, '2020-秋')
        return self.current_semester


constantsShared = Constants()
