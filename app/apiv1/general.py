#from . import cacao_bp
from ..models import CocoaImage, ClassificationImage, ModelDetection
from flask import request, jsonify
from .. import db
"""
@cacao_bp.post('/cacao')
def create_cacao():
    print("rutaaa")
    cacao_data = request.get_json()
    cacao = CocoaImage(
        imagename = cacao_data["imagename"],
        location = cacao_data["location"],
        prediction = cacao_data["prediction"]
    )
    db.session.add(cacao)
    db.session.commit()
    return {"cacao_id": cacao.id}


@cacao_bp.get('/registros')
def get_register():
    cacaos = CocoaImage.query.all()# devuelve la lista de todos lo usuarios en formato clase
    return jsonify([cacao.to_dict() for cacao in cacaos])
"""
