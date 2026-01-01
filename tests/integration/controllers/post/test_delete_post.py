from fastapi import status
from httpx import AsyncClient
from pytest_asyncio import fixture


@fixture(autouse=True)
async def populate_posts(db):
    from dio_blog_fastapi.schemas.post import PostIn
    from dio_blog_fastapi.services.post import PostService

    service = PostService()

    await service.criar_post(
        PostIn(titulo="post 1", descricao="some content", publicado=True)
    )
    await service.criar_post(
        PostIn(titulo="post 2", descricao="some content", publicado=True)
    )
    await service.criar_post(
        PostIn(titulo="post 3", descricao="some content", publicado=False)
    )


async def test_delete_post_success(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    response = await client.delete(
        f"/posts/{post_id}",
        headers=headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_post_not_authenticated_fail(client: AsyncClient):
    post_id = 1

    response = await client.delete(f"/posts/{post_id}", headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_post_not_found_success(
    client: AsyncClient,
    access_token: str,
):
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 4

    response = await client.delete(
        f"/posts/{post_id}",
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
