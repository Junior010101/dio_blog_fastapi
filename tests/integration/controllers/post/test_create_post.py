from fastapi import status
from httpx import AsyncClient


async def test_create_post_success(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "titulo": "post 1",
        "descricao": "some content",
        "publicado": True,
        "criado_em": "2024-04-12T04:33:14.403Z",
    }

    response = await client.post("/posts/", json=data, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None


async def test_create_post_invalid_payload_fall(
    client: AsyncClient,
    access_token: str,
):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "descricao": "some content",
        "publicado": True,
        "criado_em": "2024-04-12T04:33:14.403Z",
    }

    response = await client.post("/posts/", json=data, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert content["detail"][0]["loc"] == ["body", "titulo"]


async def test_create_post_not_authenticated_fail(client: AsyncClient):
    data = {
        "descricao": "some content",
        "publicado": True,
        "criado_em": "2024-04-12T04:33:14.403Z",
    }

    response = await client.post("/posts/", json=data, headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
