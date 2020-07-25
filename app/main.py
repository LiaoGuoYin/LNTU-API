import uvicorn
from fastapi import FastAPI

from appDB.database import SessionLocal

app = FastAPI()


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return {"Hi": "LNTU-API-v1.0"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=3900, reload=True)
