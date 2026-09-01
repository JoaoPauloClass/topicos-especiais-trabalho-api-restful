from flask import Flask

from app.config import get_config
from app.errors import register_error_handlers
from app.extensions import db, ma, migrate



def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    config_cls = get_config(config_name)
    app.config.from_object(config_cls)
    config_cls.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app import models  # noqa: F401
    from app.routes.categoria_routes import categoria_bp
    from app.routes.jogos_routes import jogos_bp
    from app.routes.review_routes import reviews_bp

    app.register_blueprint(categoria_bp, url_prefix="/api/categorias")
    app.register_blueprint(jogos_bp, url_prefix="/api/jogos")
    app.register_blueprint(reviews_bp, url_prefix="/api/reviews")

    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app
