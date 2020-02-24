import configparser
import os


def load():
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CONFIG_PATH = BASE_DIR + '/static/config.ini'
        print(CONFIG_PATH)
    except Exception:
        raise ValueError
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    database_config = dict()
    database_config['HOST'] = config["DATABASE"]["HOST"]
    database_config['PORT'] = config["DATABASE"]["PORT"]
    database_config['ENGINE'] = config["DATABASE"]["ENGINE"]
    database_config['NAME'] = config["DATABASE"]["NAME"]
    database_config['USER'] = config["DATABASE"]["USER"]
    database_config['PASSWORD'] = config["DATABASE"]["PASSWORD"]
    return database_config


if __name__ == '__main__':
    load()
