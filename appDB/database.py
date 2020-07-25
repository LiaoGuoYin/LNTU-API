import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config_path = '../static/config.yaml'

with open(config_path) as f:
    config = yaml.load(f, Loader=yaml.BaseLoader)
    mysql_config = config['mysql']
    user = mysql_config['user']
    password = mysql_config['password']
    host = mysql_config['host']
    port = mysql_config['port']
    db_name = mysql_config['name']

DB_URL = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
