from marshmallow import fields, validate, validates, ValidationError
from app.extensions import db, ma
from app.models.jogo import Jogo
from app.models.review import Review

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = False
        dump_only = ("id", "created_at", "updated_at")

    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=2, max=255))
    username = fields.String(required=True, validate=validate.Length(min=2, max=255))

    rating = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=10.0, error="O rating deve ser entre 0.0 e 10.0.")
    )

    review = fields.String(required=True, validate=validate.Length(min=1, max=1000))


    jogo_id = fields.Integer(required=True)

    @validates("jogo_id")
    def validate_jogo_id(self, value: int, **kwargs) -> None:
        """Garante a integridade referencial verificando se o jogo existe no banco."""
        if not db.session.get(Jogo, value):
            raise ValidationError("O jogo informado não existe.")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)