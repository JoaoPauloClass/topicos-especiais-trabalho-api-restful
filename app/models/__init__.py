"""Reexporta os modelos.

Importar este pacote na factory garante que todas as classes estejam
registradas no metadata antes de o Flask-Migrate comparar com o banco.
"""

from app.models.categoria import Categoria
from app.models.produto import Produto

__all__ = ["Categoria", "Produto"]
