from fastapi import FastAPI

from core.spider import get_std_info, get_class_table
from models import User

app = FastAPI()


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

#
# @app.post('/login')
# async def login(user: User):
#     print(user.dict())
#     return user

# @app.post('/user/course')
# async def get_user_courses(user: User):
#     # results = get_user_courses(username=user.username, password=user.password)
#     results = 'TODO'
#     return {'status': True, 'results': results}
