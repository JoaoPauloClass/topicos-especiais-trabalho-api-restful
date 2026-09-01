from app.errors import RecursoNaoEncontrado, ReferenciaInvalida
from app.extensions import db
from app.models.jogo import Jogo
from app.models.review import Review

def listar(jogo_id: int | None = None) -> list[Review]:
    stmt = db.select(Review)
    if jogo_id is not None:
        stmt = stmt.where(Review.jogo_id == jogo_id)

    return list(db.session.scalars(stmt))

def obter(review_id: int) -> Review:
    review = db.session.get(Review, review_id)
    if review is None:
        raise RecursoNaoEncontrado(f'Review {review_id} não encontrada.')
    return review

def criar(dados: dict) -> Review:
    _garantir_jogo_existe(dados['jogo_id'])
    review = Review(**dados)
    db.session.add(review)
    db.session.commit()
    return review

def atualizar(review_id: int, dados: dict) -> Review:
    review = obter(review_id)

    if "jogo_id" in dados:
        _garantir_jogo_existe(dados['jogo_id'])

    for campo, valor in dados.items():
        setattr(review, campo, valor)

    db.session.commit()
    return review

def remover(review_id: int) -> None:
    review = obter(review_id)
    db.session.delete(review)
    db.session.commit()


def _garantir_jogo_existe(jogo_id: int) -> None:
    """Garante que a chave estrangeira aponte para um Jogo válido."""
    if db.session.get(Jogo, jogo_id) is None:
        raise ReferenciaInvalida(f"Jogo {jogo_id} não existe.")