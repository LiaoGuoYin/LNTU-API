from configparser import NoSectionError

from UUIA import Uuia
from UUIA.exception.config_error_exception import Config_error_exception


def load_config(config_path='static/config.ini'):
    """load static/config.ini"""
    from configparser import ConfigParser
    conf = ConfigParser()
    try:
        conf.read(config_path)
        config_dict = {}
        for k, v in conf.items('UUIA-config'):
            config_dict.update({k: v})
        return config_dict
    except NoSectionError:
        raise Config_error_exception("Please confirm static/config.ini:UUIA-config")


uuia = Uuia(
    **load_config()
)


# 使用uuia实例的bind_action_callback_funcion并传入groups和actions注册相应动作的回调函数
# 基础功能1：获取需绑定账户的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["bindType"])
def get_bind_types(uuid, request_args):
    ret = {
        "accountTypes": [{
            "comment": "教务处",
            "code": "001",
            "ref": "000",
            "isSkip": False
        },
            {
                "comment": "一卡通",
                "code": "002",
                "ref": "001",
                "isSkip": True
            }
        ]
    }
    return ret
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能2：绑定账户的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["bind"])
def bind_account(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能3：获取用户成绩的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["score"])
def get_score(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能4：查询课表的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["schedule"])
def get_schedule(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能5：获取用户信息的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["userInfo"])
def get_user_info(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能6：获取用户一卡通信息的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["eCard"])
def get_campus_card(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 基础功能7：获取用户考试安排的回调函数
@uuia.bind_action_callback_function(groups=["base"], actions=["exam"])
def get_exams_arrangements(uuid, request_args):
    pass
    # TODO :请在这里完成数据获取操作，并将结果以dict返回


# 如果您还有其他功能的回调函数，按照上面的格式，根据group和action注册实现功能的回调函数即可

if __name__ == '__main__':
    # 调用uuia的run方法，启动项目，并开启flask_debug
    uuia.run(
        flask_debug=True
    )