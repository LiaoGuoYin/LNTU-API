from typing import List

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from core.lntuNotice import get_public_notice
from core.spider import get_std_info, get_class_table, get_all_scores, get_all_GPAs
from modelset.schemas import User, Notice, ResponseT

app = FastAPI(
    title="LNTUHelper APIs",
    description="Crawling some websites and structuring the data with JSON for LNTUHelper App",
    version="v1 beta",
    redoc_url="/readme",
)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=3000, log_level="info", reload=True)

responseBase = {'code': 200,
                'msg': 'success',
                'data': ''}


@app.get('/', tags=["public"])
def index(request: Request):
    response = ResponseT(data=str)
    response.data = "Hello LNTUHelper! " + request.client.host
    return response


@app.get('/notice', tags=["public"], response_model=ResponseT)
async def get_notice():
    response = ResponseT(data=List[Notice])
    try:
        response.data = get_public_notice()
    except Exception as e:
        response.code = status.HTTP_404_NOT_FOUND
        response.message = str(e)
    return response


@app.post('/user/info', tags=["user"])
async def get_user_info(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_std_info(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/class-table', tags=["user"])
async def get_user_class_table(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_class_table(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/score', tags=["user"])
async def get_user_all_scores(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_all_scores(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/gpa', tags=["user"])
async def get_user_all_GPAs(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_all_GPAs(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response
