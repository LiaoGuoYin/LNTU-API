import uvicorn
from fastapi import FastAPI

from app import education, quality
from appDB.database import SessionLocal

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=3900, reload=True)
