from app import db
from datetime import datetime

class CocoaImage(db.Model):
    print("dddd")
    __tablename__ = "cocoa_image"
    id = db.Column(db.Integer, primary_key = True)
    path_name = db.Column(db.String, unique = True)
    date = db.Column(db.DateTime(timezone = True), nullable=False, default = datetime.utcnow())# db.Column(db.DateTime, nullable=False)
    localization = db.Column(db.JSON, nullable=False)#db.Column(db.String)

    def to_dict(self):
        return {"id": self.id, 
                "path_name": self.path_name, 
                "date": self.date,
                "localization": self.localization
                }
    

class ClassificationImage(db.Model):# 
    __tablename__ = "classification_image" # actualizar nombre de tabla a predictions
    id = db.Column(db.Integer, primary_key = True)
    id_modelo = db.Column(db.Integer, db.ForeignKey("model_detection.id"), nullable=False)
    id_image = db.Column(db.Integer, db.ForeignKey("cocoa_image.id"), nullable=False)
    instances = db.Column(db.String)
    confidence = db.Column(db.Float)
    x_pb1 = db.Column(db.Float)
    y_pb1 = db.Column(db.Float)
    x_pb2 = db.Column(db.Float)
    y_pb2 = db.Column(db.Float)

    def to_dict(self):
        return {"id": self.id,
                "id_model": self.id_modelo,
                "id_image": self.id_image,
                "instances": self.instances,
                "confidence": self.confidence,
                "x_pb1": self.x_pb1,
                "y_bp1": self.y_pb1,
                "x_bp2": self.x_pb2,
                "y_pb2": self.y_pb2
        }

class ModelDetection(db.Model): # 
    __tablename__ = "model_detection" #cambiar el nombre de la tabla a ML models detection
    id = db.Column(db.Integer, primary_key = True)
    path_name = db.Column(db.String, unique = True)
    description = db.Column(db.String)
    f1_score = db.Column(db.Float) # validar

    def to_dict(self):
        return {"id": self.id, 
                "path_name": self.path_name, 
                "description": self.description,
                "f1_score": self.f1_score}




