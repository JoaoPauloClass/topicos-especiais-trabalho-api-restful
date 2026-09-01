from datetime import datetime, timezone

from marshmallow import fields, validates,validate, ValidationError

from app.extensions import ma
from app.models import Jogo


class JogoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jogo
        load_instance = False
        dump_only = ("id", "created_at", "updated_at")

    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=2, max=255))
    datapublicacao = fields.DateTime(
        required=True,
        format="%d-%m-%Y",
        error_messages={
            "required": "A data de publicação é obrigatória.",
            "invalid": "Formato de data inválido. Use o padrão DD-MM-YYYY.",
        },
    )
    categoria_id = fields.Integer(required=True)

    @validates("datapublicacao")
    def validate_datapublicacao(self, value: datetime, **kwargs) -> None:
        """Garante que a data de publicação não esteja no futuro."""
        agora = datetime.now(timezone.utc)
        data_comparacao = value if value.tzinfo else value.replace(tzinfo=timezone.utc)

        if data_comparacao > agora:
            raise ValidationError("A data de publicação não pode ser uma data futura.")

jogo_schema = JogoSchema()
jogos_schema = JogoSchema(many=True)