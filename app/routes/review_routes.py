from flask import Blueprint, jsonify, request

from app.schemas.review_schema import review_schema, reviews_schema
from app.services import review_service

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.get("")
def listar_reviews():
    jogo_id = request.args.get("jogo_id", type=int)
    reviews = review_service.listar(jogo_id=jogo_id)
    return jsonify(reviews_schema.dump(reviews)), 200


@reviews_bp.get("/<int:review_id>")
def obter_review(review_id: int):
    review = review_service.obter(review_id=review_id)
    return jsonify(review_schema.dump(review)), 200


@reviews_bp.post("/")
def criar_review():
    dados = review_schema.load(request.get_json())
    review = review_service.criar(dados)
    return jsonify(review_schema.dump(review)), 201


@reviews_bp.put("/<int:review_id>")
def substituir_review(review_id: int):
    dados = review_schema.load(request.get_json(), partial=False)
    review = review_service.atualizar(review_id=review_id, dados=dados)
    return jsonify(review_schema.dump(review)), 200


@reviews_bp.patch("/<int:review_id>")
def atualizar_review(review_id: int):
    dados = review_schema.load(request.get_json(), partial=True)
    review = review_service.atualizar(review_id=review_id, dados=dados)
    return jsonify(review_schema.dump(review)), 200


@reviews_bp.delete("/<int:review_id>")
def remover_review(review_id: int):
    review_service.remover(review_id=review_id)
    return "", 204