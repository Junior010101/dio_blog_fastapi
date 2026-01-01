from fastapi import status
from httpx import AsyncClient
from pytest import mark
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


@mark.parametrize("publicado,total", [("on", 2), ("off", 1)])
async def test_read_posts_by_status_seccess(
    client: AsyncClient, access_token: str, publicado: str, total: int
):
    params = {"publicado": publicado, "limite": 10}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total


async def test_read_posts_limit_success(
    client: AsyncClient,
    access_token: str,
):
    params = {"publicado": "on", "limite": 1}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1


async def test_read_posts_not_authenticated_fail(client: AsyncClient):
    params = {"publicado": "on", "limite": 1}

    response = await client.get("/posts/", params=params, headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_read_posts_parameters_fail(
    client: AsyncClient,
    access_token: str,
):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params={}, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
