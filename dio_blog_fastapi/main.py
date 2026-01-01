from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from dio_blog_fastapi import database, engine, metadata
from dio_blog_fastapi.controllers import auth_route, post_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    try:
        metadata.create_all(engine)
        yield
    finally:
        await database.disconnect()


api = FastAPI(lifespan=lifespan)
api.include_router(post_route)
api.include_router(auth_route)


if __name__ == "__main__":
    run("main:api", reload=True)
