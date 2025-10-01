from pathlib import Path
import os


basedir = Path(__file__).resolve().parent # Obtener la ruta donde se corre el archivo .py
print(basedir)

"""Crear configuración base de una aplicación robusta
"""

class Config:
    TITLE = "CACAO APP"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "CAMBIAME"#Trabajar variables de ambiente

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    TITLE = "CACAO APP DEV"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@localhost:5432/{os.environ.get('POSTGRES_DB')}?client_encoding=utf8"
    )


"""Crear diccionario de configuraciones"""

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@localhost:5432/{os.environ.get('POSTGRES_DB')}_prod?client_encoding=utf8"
    )


    @classmethod
    def init_app(cls,app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig

}