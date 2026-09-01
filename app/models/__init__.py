"""Reexporta os modelos.

Importar este pacote na factory garante que todas as classes estejam
registradas no metadata antes de o Flask-Migrate comparar com o banco.
"""

from app.models.categoria import Categoria
from app.models.jogo import Jogo
from app.models.review import Review

__all__ = ["Categoria", "Jogo", "Review"]
