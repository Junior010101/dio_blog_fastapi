from fastapi import Response, status
from sqlalchemy import delete, insert, select, update

from dio_blog_fastapi import database
from dio_blog_fastapi.models import Post
from dio_blog_fastapi.schemas import PostIn, PostUpdate


class PostService:

    async def ler_posts(
        self,
        response: Response,
        publicado: bool,
        limite: int = 10,
        skip: int = 0,
    ):
        query = select(Post).offset(skip).limit(limite)

        if publicado is not None:
            query = query.where(Post.publicado == publicado)

        resultado = await database.fetch_all(query)

        if not resultado:
            response.status_code = status.HTTP_204_NO_CONTENT
            return []

        return resultado

    async def ler_post(self, response: Response, id: int):
        query = select(Post).where(Post.id == id)

        resultado = await database.fetch_one(query)

        if not resultado:
            response.status_code = status.HTTP_204_NO_CONTENT
            return None

        return resultado

    async def criar_post(self, post: PostIn):
        query = insert(Post).values(
            titulo=post.titulo,
            publicado=post.publicado,
            descricao=post.descricao,
            criado_em=post.criado_em,
        )

        return await database.execute(query)

    async def atualizar_post(
        self,
        response: Response,
        id: int,
        post: PostUpdate,
    ):
        if post is None:
            return {"id": id}

        dados = post.model_dump(exclude_unset=True)

        if not dados:
            return {"id": id}

        query = update(Post).where(Post.id == id).values(**dados)
        rows_affected = await database.execute(query)

        if rows_affected == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Post não encontrado"}

        return {"id": id, **dados}

    async def excluir_post(self, response: Response, id: int):
        query = delete(Post).where(Post.id == id).returning(Post.id)

        deleted_id = await database.fetch_val(query)

        if deleted_id is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "Post não encontrado"}

        return {"id": deleted_id, "deleted": True}
