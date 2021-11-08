from fastapi import APIRouter

router = APIRouter(
    tags=['Basic']
)


@router.get("/")
async def root():
    return {"message": "HelloWorld!"}
