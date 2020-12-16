import sentry_sdk
import uvicorn
from fastapi import FastAPI
from pydantic import ValidationError
from sentry_sdk import capture_exception
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy import create_engine

from app import education, quality, aipao, schemas, exceptions
from app.exceptions import FormException
from appDB.models import Base
from app.constants import constantsShared

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


@app.exception_handler(exceptions.CommonException)
async def common_exception_handler(request: Request, exc: exceptions.CommonException):
    capture_exception(exc)
    response = schemas.ResponseT(
        code=exc.code,
        message=exc.message
    )
    return JSONResponse(
        status_code=response.code,
        content=response.dict()
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    capture_exception(exc)
    response = schemas.ResponseT(
        code=status.HTTP_400_BAD_REQUEST,
        message=str(exc.errors())
    )
    return JSONResponse(
        status_code=response.code,
        content=response.dict()
    )


@app.exception_handler(ValidationError)
async def request_validation_exception_handler(request: Request, exc: ValidationError):
    capture_exception(exc)
    response = schemas.ResponseT(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc.errors())
    )
    return JSONResponse(
        status_code=response.code,
        content=response.dict()
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response = schemas.ResponseT(
        code=exc.status_code,
        message=exc.detail
    )
    return JSONResponse(
        status_code=response.code,
        content=response.dict()
    )


def filter_sentry_alert(event, hint):
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, FormException):
            # 来源于用户的表单错误，不应被埋点记录
            return None
    return event


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

db_url_dict = constantsShared.get_db_url_dict()
engine = create_engine(db_url_dict['production'], pool_recycle=3600)
Base.metadata.create_all(bind=engine)  # 创建数据库
app.add_middleware(DBSessionMiddleware, db_url=db_url_dict['production'], custom_engine=engine)

sentry_url = constantsShared.config.sentryURL
sentry_sdk.init(sentry_url, before_send=filter_sentry_alert, max_breadcrumbs=50)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
