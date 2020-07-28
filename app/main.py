import sentry_sdk
import uvicorn
from fastapi import FastAPI

from app import education, quality

app = FastAPI()


@app.get("/")
async def home():
    return {"Hi": "LNTU-API-v1.0"}


app.include_router(
    education.router,
    prefix="/education",
    tags=["education"]
)

app.include_router(
    quality.router,
    prefix="/quality",
    tags=["quality"]
)


# DB Dependency
def get_db():
    from appDB.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Sentry monitor
def get_sentry():
    import yaml
    try:
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
        if config['sentry']['url']:
            sentry_sdk.init(config['sentry']['url'], max_breadcrumbs=50)
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

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
