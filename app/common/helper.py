from app import  schemas
from app.education import utils, core
from app.quality import core as quality_core


def refresh_helper_message() -> schemas.HelperMessage:
    import yaml
    import os
    try:
        APP_ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(APP_ABSOLUTE_PATH, '../../config.yaml')) as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
        helper_message = schemas.HelperMessage()
        helper_message.notice = config['default']['message']
        helper_message.semester = config['default']['semester']
        helper_message.educationServerStatus = '正常' if core.is_education_online() else '离线'
        helper_message.qualityServerStatus = '正常' if quality_core.is_quality_online() else '离线'
        helper_message.helperServerStatus = '正常'
        helper_message.week = utils.calculate_week(config['default']['semester_start_date'])
        return helper_message
    except FileNotFoundError:
        print("初始化失败，请检查项目根目录下是否有 config.yaml 配置文件")
    except Exception:
        print("初始化失败，请检查 config.yaml 配置文件是否正确")
