from asyncio import run
from os import environ
from tempfile import NamedTemporaryFile

from httpx import ASGITransport, AsyncClient
from pytest_asyncio import fixture

tmp = NamedTemporaryFile(suffix=".db")
environ["DATABASE_URL"] = f"sqlite+pysqlite:///{tmp.name}"


@fixture
async def db(request):
    from dio_blog_fastapi import database, engine, metadata
    from dio_blog_fastapi.models import Post  # noqa

    await database.connect()
    metadata.create_all(engine)

    def teardown():
        async def _teardown():
            await database.disconnect()
            metadata.drop_all(engine)

        run(_teardown())

    request.addfinalizer(teardown)


@fixture
async def client(db):
    from dio_blog_fastapi.main import api

    transport = ASGITransport(app=api)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    async with AsyncClient(
        base_url="http://test", transport=transport, headers=headers
    ) as client:
        yield client


@fixture
async def access_token(client: AsyncClient):
    response = await client.post("/auth/login", json={"id_usuario": 1})
    return response.json()["token_acesso"]
