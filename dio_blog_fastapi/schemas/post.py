from datetime import datetime, timezone

from pydantic import BaseModel, Field


class PostIn(BaseModel):
    titulo: str
    publicado: bool = False
    descricao: str | None = " "
    criado_em: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class PostUpdate(BaseModel):
    titulo: str | None = None
    publicado: bool | None = None
    descricao: str | None = None
