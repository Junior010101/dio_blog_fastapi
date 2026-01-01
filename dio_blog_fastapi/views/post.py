from datetime import datetime

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    titulo: str
    descricao: str
    criado_em: datetime
