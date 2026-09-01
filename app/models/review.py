from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db
from app.models.jogo import Jogo

class Review(db.Model):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(String(1000), nullable=False)
    jogo_id: Mapped[int] = mapped_column(
        db.ForeignKey("jogos.id", ondelete="CASCADE"),
    )
    jogo: Mapped[Jogo] = relationship(
        "Jogo",
        back_populates="reviews",
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

    def __repr__(self) -> str:
        return f"<Review {self.rating} - {self.titulo} - {self.username}>"
