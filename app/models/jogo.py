from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models import Categoria


class Jogo(db.Model):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    datapublicacao: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    desenvolvedor: Mapped[str] = mapped_column(String(255), nullable=False)
    distribuidora: Mapped[str] = mapped_column(String(255), nullable=False)
    categoria_id: Mapped[int] = mapped_column(
        db.ForeignKey("categorias.id", ondelete="CASCADE"),
    )
    categoria: Mapped[Categoria] = relationship(
        "Categoria",
        back_populates="jogos",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="jogo",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Jogo {self.titulo} - {self.desenvolvedor} - {self.distribuidora}>"
