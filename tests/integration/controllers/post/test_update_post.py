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


async def test_update_post_success(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"titulo": "update title post 1"}
    post_id = 1

    response = await client.patch(
        f"/posts/{post_id}",
        json=data,
        headers=headers,
    )

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["titulo"] == data["titulo"]


async def test_update_post_authenticated_fail(client: AsyncClient):
    post_id = 1

    response = await client.patch(
        f"/posts/{post_id}",
        headers={},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_update_post_not_found_fail(
    client: AsyncClient,
    access_token: str,
):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"titulo": "update title post 1"}
    post_id = 4

    response = await client.patch(
        f"/posts/{post_id}",
        json=data,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
