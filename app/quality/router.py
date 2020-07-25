from fastapi import APIRouter

router = APIRouter()


@router.get("/", )
async def quality_home():
    return {"API-location": "/quality/"}


@router.get("/report", )
async def quality_home():
    return {"API-location": "/quality/report"}
