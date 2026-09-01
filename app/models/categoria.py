from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db



class Categoria(db.Model):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    jogos: Mapped[list["Jogo"]] = relationship(
        "Jogo",
        back_populates="categoria",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Categoria {self.nome}>"
