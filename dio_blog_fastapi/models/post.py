from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from dio_blog_fastapi import metadata


class Base(DeclarativeBase):
    metadata = metadata


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    titulo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )
    publicado: Mapped[bool] = mapped_column(
        nullable=False,
    )
    descricao: Mapped[str] = mapped_column(
        nullable=True,
    )
    criado_em: Mapped[datetime] = mapped_column(
        nullable=False,
    )
