from datetime import datetime, timezone

from pydantic import BaseModel, Field


class PostIn(BaseModel):
    titulo: str
    publicado: bool = False
    descricao: str | None = None
    criado_em: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class PostUpdate(PostIn):
    titulo: str | None = None
