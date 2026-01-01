from pydantic import BaseModel


class LoginIn(BaseModel):
    id_usuario: int
