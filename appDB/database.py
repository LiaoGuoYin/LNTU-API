from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from appDB.models import Base
from appDB.utils import get_db_url_dict

db_url_dict = get_db_url_dict()
engine = create_engine(db_url_dict['production'], echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
