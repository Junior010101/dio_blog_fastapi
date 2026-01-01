from pydantic import BaseModel


class LoginOut(BaseModel):
    token_acesso: str
