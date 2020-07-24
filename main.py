import traceback
from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from core import notification
from core.spider import get_std_info, get_class_table, get_grades, get_all_GPAs
from core.util import Logger
from modelset import schemas
from modelset.schemas import User, Notice, ResponseT, ClassTable, GPA
from sqlApp import crud
from sqlApp.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="LNTUHelper APIs",
    description="HiLNTU Backend Spider API",
    version="v1.0",
    redoc_url="/readme",
)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=3000, log_level="info", reload=True)


@app.get('/', tags=["public"])
def index(request: Request):
    response = ResponseT(data=str)
    response.data = "Hi LNTUer! " + request.client.host
    return response


@app.get('/notice', tags=["public"], response_model=ResponseT)
async def get_notice(db: Session = Depends(get_db)):
    response = ResponseT(data=List[Notice])
    # try:
    notices = notification.run()
    response.data = notices
    for notice in notices:
        crud.create_notice(db, notice)
    # except Exception as e:
    #     pass
    #     traceback.extract_stack()
    #     response.code = status.HTTP_404_NOT_FOUND
    #     response.message = str(e)
    #     response.data = {}  # TODO validation
    #     Logger.e(tag='notice', content=e)
    return response


@app.post('/user/info', tags=["user"])
async def get_user_info(user: User):
    response = ResponseT(data=dict)
    try:
        response.data = get_std_info(**user.dict())
    except Exception as e:
        response.code = status.HTTP_400_BAD_REQUEST
        response.message = str(e)
        response.data = {}
        Logger.e(tag='info', content=e)
    return response


@app.post('/user/class-table', tags=["user"])
async def get_user_class_table(user: User, semester=626):
    response = ResponseT(data=List[ClassTable])
    try:
        response.data = get_class_table(**user.dict(), semester=semester)
    except Exception as e:
        response.code = status.HTTP_400_BAD_REQUEST
        response.message = str(e)
        response.data = {}
        Logger.e(tag='class-table', content=e)
    return response


@app.post('/user/grades', tags=["user"])
async def get_user_grades(user: schemas.User, db: Session = Depends(get_db)):
    response = ResponseT(data=List[schemas.Grade])
    try:
        grades = get_grades(**user.dict())
        response.data = grades
        for grade in grades:
            crud.create_user(db, user)
            crud.create_grade(db, grade, user)
    except Exception as e:
        response.code = status.HTTP_400_BAD_REQUEST
        response.message = str(e)
        response.data = {}
        Logger.e(tag='grades', content=e)
    return response


@app.get('/user/grades', tags=["user", "db"])
async def get_user_grades(user: schemas.User, db: Session = Depends(get_db)):
    response = ResponseT(data=List[schemas.Grade])
    try:
        # TODO Check password
        response.data = crud.get_user_grades(db, user)
    except Exception as e:
        traceback.format_exc()
        response.code = status.HTTP_400_BAD_REQUEST
        response.message = str(e)
        response.data = {}
        Logger.e(tag='grades', content=e)
    return response


@app.post('/user/gpa', tags=["user"])
async def get_user_all_GPAs(user: User):
    response = ResponseT(data=List[GPA])
    try:
        response.data = get_all_GPAs(**user.dict())
    except Exception as e:
        traceback.print_exc()
        response.code = status.HTTP_400_BAD_REQUEST
        response.message = str(e)
        response.data = {}
        Logger.e(tag='gpa', content=e)
    return response

# @app.post('/user/all')
# async def get_all(user: User, db: Session = Depends(get_db)):
#     response = ResponseT()
#     try:
#         # print(get_std_info(**user.dict()))
#
#         # print(get_class_table(**user.dict()))
#         # grades = get_grades(**user.dict())
#         for grade in get_grades(**user.dict()):
#             crud.create_grade(db, grade)
#     except Exception as e:
#         response.code = status.HTTP_400_BAD_REQUEST
#         response.message = str(e)
#         response.data = {}
#         Logger.e(tag='gpa', content=e)
#     return response
