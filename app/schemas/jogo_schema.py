from datetime import datetime, timezone

from marshmallow import fields, validates,validate, ValidationError

from app.extensions import ma
from app.models import Jogo


class JogoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jogo
        load_instance = True
        dump_only = ("id", "created_at", "updated_at")

    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=2, max=255))
    datapublicao = fields.DateTime(
        required=True,
        format="%d-%m-%Y",
    )
    estoque = fields.Integer(load_default=0, validate=validate.Range(min=0))
    categoria_id = fields.Integer(required=True)

    @validates("datapublicao")
    def validate_datapublicacao(self, value: datetime) -> None:
        """Garante que a data de publicação não esteja no futuro."""
        agora = datetime.now(timezone.utc)
        data_comparacao = value if value.tzinfo else value.replace(tzinfo=timezone.utc)

        if data_comparacao > agora:
            raise ValidationError("A data de publicação não pode ser uma data futura.")

jogo_schema = JogoSchema()
jogos_schema = JogoSchema(many=True)