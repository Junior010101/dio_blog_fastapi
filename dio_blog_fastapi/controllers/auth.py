from fastapi import APIRouter

from dio_blog_fastapi.schemas import LoginIn
from dio_blog_fastapi.security import sign_jwt
from dio_blog_fastapi.views import LoginOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    return sign_jwt(data.id_usuario)
