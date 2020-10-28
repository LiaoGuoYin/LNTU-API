import sentry_sdk
import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from sqlalchemy import create_engine

from app import education, quality, aipao, schemas
from app.exceptions import FormException, StatusCodeEnum
from appDB.models import Base
from appDB.utils import get_db_url_dict

tags_metadata = [
    {
        "name": "Education",
        "description": "API for [LNTU Course Management Information System.](http://202.199.224.119:8080/eams/loginExt.action)",
    },
    {
        "name": "Quality",
        "description": "API for [LNTU Students Quality Expansion Activity Management System.](http://202.199.224.19:8080/)",
    },
    {
        "name": "AiPao",
        "description": "API for [AiPao](http://client3.aipao.me/)",
    },
]

app = FastAPI(
    title="LNTU-API",
    description="An elegant backend API of LNTU. You can find more on [GitHub/LiaoGuoYin/LNTU-API](https://github.com/LiaoGuoYin/LNTU-API)",
    version="v1.0",
    docs_url="/",
    redoc_url="/readme",
    openapi_tags=tags_metadata
)

db_url_dict = get_db_url_dict()
engine = create_engine(db_url_dict['production'], pool_recycle=3600)
Base.metadata.create_all(bind=engine)  # 创建数据库
app.add_middleware(DBSessionMiddleware, db_url=db_url_dict['production'], custom_engine=engine)

app.include_router(
    education.router,
    prefix="/education",
    tags=["Education"]
)

app.include_router(
    quality.router,
    prefix="/quality",
    tags=["Quality"]
)

app.include_router(
    aipao.router,
    prefix="/aipao",
    tags=["AiPao"]
)


def filter_sentry_alert(event, hint):
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, FormException):
            # 来源于用户的表单错误，不应被埋点记录
            return None
    return event


# Sentry monitor
def get_sentry():
    import yaml
    try:
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
        if config['sentry']['url']:
            sentry_sdk.init(
                config['sentry']['url'],
                before_send=filter_sentry_alert,
                max_breadcrumbs=50)
            return True
        else:
            return False
    except FileNotFoundError:
        return "初始化失败，请检查项目根目录下是否有 config.yaml 配置文件"
    except Exception:
        return "初始化失败，请检查 config.yaml 配置文件是否正确"


if get_sentry() is True:
    print("初始化 Sentry 成功")
else:
    print("初始化 Sentry 失败")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response = schemas.ResponseT()
    response.code = StatusCodeEnum.INVALID_REQUEST.value
    response.message = str(exc.errors())
    return JSONResponse(response.dict())


@app.exception_handler(StarletteHTTPException)
async def validation_exception_handler(request, exc):
    response = schemas.ResponseT()
    response.code = exc.status_code
    response.message = exc.detail
    return JSONResponse(response.dict())


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
