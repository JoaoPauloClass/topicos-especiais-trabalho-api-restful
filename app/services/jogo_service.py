from app.errors import RecursoNaoEncontrado, ReferenciaInvalida
from app.extensions import db
from app.models.categoria import Categoria
from app.models.jogo import Jogo

def listar(categoria_id: int | None = None) -> list[Jogo]:
    stmt = db.select(Jogo)
    if categoria_id is not None:
        stmt = stmt.where(Jogo.id == categoria_id)

    return list(db.session.scalars(stmt))

def obter(jogo_id: int) -> Jogo:
    jogo = db.session.get(Jogo, jogo_id)
    if jogo is None:
        raise RecursoNaoEncontrado(f'Jogo {jogo_id} não encontrado.')
    return jogo

def criar(dados: dict) -> Jogo:
    _garantir_categoria_existe(dados['categoria_id'])
    jogo = Jogo(**dados)
    db.session.add(jogo)
    db.session.commit()
    return jogo

def atualizar(jogo_id: int, dados: dict) -> Jogo:
    jogo = obter(jogo_id)

    if "categoria_id" in dados:
        _garantir_categoria_existe(dados['categoria_id'])

    for campo, valor in dados.items():
        setattr(jogo, campo, valor)

    db.session.commit()
    return jogo

def remover(jogo_id: int) -> None:
    jogo = obter(jogo_id)
    db.session.delete(jogo)
    db.session.commit()


def _garantir_categoria_existe(categoria_id: int) -> None:
    if db.session.get(Categoria, categoria_id) is None:
        raise ReferenciaInvalida(f"Categoria {categoria_id} não existe.")
