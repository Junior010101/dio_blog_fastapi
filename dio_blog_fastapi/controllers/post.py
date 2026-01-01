from typing import Optional

from fastapi import APIRouter, Depends, Response, status

from dio_blog_fastapi.schemas import PostIn, PostUpdate
from dio_blog_fastapi.security import login_required
from dio_blog_fastapi.services import PostService
from dio_blog_fastapi.views import PostOut

router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])
service = PostService()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PostOut],
)
async def ler_posts(
    response: Response, publicado: bool, limite: int = 10, skip: int = 0
):
    return await service.ler_posts(
        response,
        publicado=publicado,
        limite=limite,
        skip=skip,
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PostOut | None,
)
async def ler_post(response: Response, id: int):
    return await service.ler_post(response, id=id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostOut,
)
async def criar_post(post: PostIn):
    return {**post.model_dump(), "id": await service.criar_post(post=post)}


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def atualizar_post(
    response: Response, id: int, post: Optional[PostUpdate] = None
):
    return await service.atualizar_post(response, id=id, post=post)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def excluir_post(response: Response, id: int):
    return await service.excluir_post(response, id=id)
