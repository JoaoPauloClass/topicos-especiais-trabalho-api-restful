from flask import Blueprint, jsonify, request

from app.schemas.jogo_schema import jogo_schema, jogos_schema
from app.services import jogo_service

jogos_bp = Blueprint('jogos', __name__)
@jogos_bp.get('')
def listar_jogos():
    categoria_id = request.args.get('categoria_id', type=int)
    jogos = jogo_service.listar(categoria_id=categoria_id)
    return jsonify(jogos_schema.dump(jogos)), 200