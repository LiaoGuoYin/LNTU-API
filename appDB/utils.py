import os

PROJECT_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_ABSOLUTE_PATH = PROJECT_ABSOLUTE_PATH + '/config.yaml'


def get_db_url_dict(config_path=CONFIG_ABSOLUTE_PATH) -> dict:
    import yaml
    db_url_dict = {}
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
        sql = config['mysql']
        user = sql['user']
        password = sql['password']
        host = sql['host']
        port = sql['port']
        db_name = sql['db_name']
        test_db_name = sql['test_db_name']
        db_url_dict['production'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        db_url_dict['test'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{test_db_name}"
    return db_url_dict
