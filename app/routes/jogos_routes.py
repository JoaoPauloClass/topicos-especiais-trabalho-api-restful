from flask import Blueprint, jsonify, request

from app.schemas.jogo_schema import jogo_schema, jogos_schema
from app.services import jogo_service

jogos_bp = Blueprint('jogos', __name__)
@jogos_bp.get('')
def listar_jogos():
    categoria_id = request.args.get('categoria_id', type=int)
    jogos = jogo_service.listar(categoria_id=categoria_id)
    return jsonify(jogos_schema.dump(jogos)), 200

@jogos_bp.get('/<int:jogo_id>')
def obter_jogo(jogo_id: int):
    jogo = jogo_service.obter(jogo_id=jogo_id)
    return jsonify(jogo_schema.dump(jogo)), 200

@jogos_bp.post('/')
def criar_jogo():
    dados = jogo_schema.load(request.get_json())
    jogo = jogo_service.criar(dados)
    return jsonify(jogo_schema.dump(jogo)), 201

@jogos_bp.put('/<int:jogo_id>')
def substituir_jogo(jogo_id: int):
    dados = jogo_schema.load(request.get_json(), partial=False)
    jogo = jogo_service.atualizar(jogo_id=jogo_id, dados=dados)
    return jsonify(jogo_schema.dump(jogo)), 200

@jogos_bp.patch('/<int:jogo_id>')
def atualizar_jogo(jogo_id: int):
    dados = jogo_schema.load(request.get_json(), partial=True)
    jogo = jogo_service.atualizar(jogo_id=jogo_id, dados=dados)
    return jsonify(jogo_schema.dump(jogo)), 200

@jogos_bp.delete('/<int:jogo_id>')
def remover_jogo(jogo_id: int):
    jogo_service.remover(jogo_id=jogo_id)
