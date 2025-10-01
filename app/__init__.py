from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app,db)
    print("aqui")

    #Agregar autentificación

    #Registrar blue print
    with app.app_context():
        from .apiv1 import prediction_bp, model_bp, image_bp

        print("hola")
        #db.drop_all()
        db.create_all()

        app.register_blueprint(prediction_bp, url_prefix = "/cacaoapi/v1/prediction")
        app.register_blueprint(model_bp, url_prefix = "/cacaoapi/v1/model")
        app.register_blueprint(image_bp, url_prefix = "/cacaoapi/v1/image")
        
        print(type(app))

        return app