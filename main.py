import uvicorn
from fastapi import FastAPI

from core.lntuNotice import get_public_notice
from core.spider import get_std_info, get_class_table, get_all_scores, get_all_GPAs
from models import User

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=3000, log_level="info", reload=True)

responseBase = {'code': 200,
                'msg': 'success',
                'data': ''}


@app.get('/')
def index():
    response = responseBase.copy()
    response['data'] = 'You just successfully deployed FastAPI'
    return responseBase


@app.get('/notice')
async def get_notice():
    response = responseBase.copy()
    try:
        results = get_public_notice()
        response['data'] = results
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/info')
async def get_user_info(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_std_info(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/classtable')
async def get_user_class_table(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_class_table(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/score')
async def get_user_all_scores(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_all_scores(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response


@app.post('/user/gpa')
async def get_user_all_GPAs(user: User):
    response = responseBase.copy()
    try:
        response['data'] = get_all_GPAs(username=user.username, password=user.password)
    except Exception as e:
        response['code'] = 500
        response['msg'] = str(e)
    return response
