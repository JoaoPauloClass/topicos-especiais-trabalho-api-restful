import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """Configuração comum a todos os ambientes."""

    SECRET_KEY = os.getenv("SECRET_KEY", "chave-dev-insegura-mude-em-producao")

    user = os.getenv("USER_DB")
    password = os.getenv("PASSWORD_DB")

    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    print("DEBUG >>>", repr(os.getenv("USER_DB")), repr(os.getenv("PASSWORD_DB")), repr(os.getenv("DB_HOST")),
          repr(os.getenv("DB_PORT")), repr(os.getenv("DB_NAME")))

    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{db_host}:{db_port}/{db_name}?client_encoding=utf8'
    # Desligado por padrão desde o Flask-SQLAlchemy 3.x; mantido explícito
    # porque a turma vai ver esse nome em tutoriais antigos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app) -> None:
        """Gancho de validação, chamado pela factory após `from_object`.

        Existe porque `app.config.from_object()` recebe a *classe* e nunca a
        instancia — validação escrita em `__init__` jamais seria executada.
        """

        if app.config.get("TESTING"):
            return

        obrigatorias = {"USER_DB": cls.user, "PASSWORD_DB": cls.password, "DB_NAME": cls.db_name}
        faltantes = [chave for chave, valor in obrigatorias.items() if not valor]

        if faltantes:
            raise RuntimeError(
                f"As seguintes variaveis de ambiente do banco de dados estao ausentes: {', '.join(faltantes)}"
            )


class DevelopmentConfig(Config):
    DEBUG = True
    # Ecoa o SQL gerado no console: útil para mostrar o N+1 e o cascade em aula.
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"


class TestingConfig(Config):
    TESTING = True
    # Banco em memória: cada execução da suíte começa do zero.
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app) -> None:
        if cls.SECRET_KEY == "chave-dev-insegura-mude-em-producao":
            raise RuntimeError(
                "SECRET_KEY não definida. Em produção ela é obrigatória. "
                "Falhar na inicialização é melhor que subir com chave conhecida."
            )


CONFIG_POR_NOME: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(nome: str | None = None) -> type[Config]:
    """Devolve a classe de configuração do ambiente pedido.

    A precedência é: argumento explícito > variável APP_ENV > development.
    """
    nome = nome or os.getenv("APP_ENV", "development")
    try:
        return CONFIG_POR_NOME[nome]
    except KeyError:
        validos = ", ".join(sorted(CONFIG_POR_NOME))
        raise ValueError(
            f"Ambiente '{nome}' desconhecido. Use um destes: {validos}."
        ) from None
