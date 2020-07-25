import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from appDB.database import config_path

with open(config_path) as f:
    # def TODO yield
    config = yaml.load(f, Loader=yaml.BaseLoader)
    mysql_config = config['test-mysql']
    user = mysql_config['user']
    password = mysql_config['password']
    host = mysql_config['host']
    port = mysql_config['port']
    db_name = mysql_config['name']

DB_URL = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_connect_db():
    # TODO
    pass
