import uvicorn
from fastapi import FastAPI

from core.spider import get_std_info, get_class_table, get_all_scores, get_all_GPAs
from models import User

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=3000, log_level="info", reload=True)


@app.get('/')
def index():
    return {'message': 'You just successfully deployed FastAPI'}


@app.post('/user/info')
async def get_user_info(user: User):
    try:
        results = get_std_info(username=user.username, password=user.password)
    except Exception as e:
        print(e)
        results = {'error': e}
    return {'status': True,
            'results': results}


@app.post('/user/classTable')
async def get_user_class_table(user: User):
    try:
        results = get_class_table(username=user.username, password=user.password)
    except Exception as e:
        results = {'error': e}
    return {'status': True,
            'results': results}


@app.post('/user/score')
async def get_user_all_scores(user: User):
    try:
        results = get_all_scores(username=user.username, password=user.password)
    except Exception as e:
        results = {'error': e}
    return {'status': True,
            'results': results}


@app.post('/user/gpa')
async def get_user_all_GPAs(user: User):
    try:
        results = get_all_GPAs(username=user.username, password=user.password)
    except Exception as e:
        results = {'error': e}
    return {'status': True,
            'results': results}
