
from . import prediction_bp
from ..models import ModelDetection, ClassificationImage, CocoaImage
from flask import request, jsonify
from sqlalchemy import desc
from .. import db

@prediction_bp.post("/prediction")
def get_prediction():
    payload = request.get_json()
    instances = payload["instances"]
    confidence = payload["confidence"]
    x_bp1 = payload["x_bp1"]
    y_bp1 = payload["y_bp1"]
    x_bp2 = payload["x_bp2"]
    y_bp2 = payload["y_bp2"]
    id_model = payload["id_model"]
    id_image = payload["id_image"]
    
    #id_image = CocoaImage.query.order_by(desc(CocoaImage.id)).first()
    model_classification = db.session.get(ModelDetection, id_model)
    if model_classification is None:
        return jsonify({'message': 'Missing id_model'}), 400

    model_image = db.session.get(CocoaImage, id_image)
    if model_image is None:
        return jsonify({'message': 'Missing id_image'}), 400
    #db.session.query(CocoaImage).order_by(desc(CocoaImage.id)).first()
    #id_modelo = ModelDetection.query.order_by(desc(ModelDetection.id)).first()

    classification = ClassificationImage(
        id_modelo = model_classification.id,
        id_image = model_image.id,
        instances = instances,
        confidence =confidence,
        x_pb1 = x_bp1,
        y_pb1 = y_bp1,
        x_pb2 = x_bp2,
        y_pb2 = y_bp2,
    )
    
    db.session.add(classification)
    db.session.commit()

    return jsonify({'message': f'Classification {classification.id} created successfully'})


@prediction_bp.delete("/prediction/<int:pred_id>")
def delet_predict(pred_id = None):

    if pred_id is None:
        return jsonify({'message': 'Missing pred_id'}), 400
    prediction = db.session.get(ClassificationImage, pred_id)

    if prediction is None:
        return jsonify({'message': f'CocoaImage {pred_id} not found'}), 404
    db.session.delete(prediction)
    db.session.commit()

    return jsonify({'message': f'Prediction {pred_id} deleted successfully'})


@prediction_bp.get("/prediction")
@prediction_bp.get("/prediction/<int:pred_id>")
def get_predict(pred_id = None):

    if pred_id is None:
        prediction = ClassificationImage.query.all()
        return jsonify([pred.to_dict() for pred in prediction])
    
    prediction = db.session.get(ClassificationImage, pred_id)

    if prediction is None:
        return jsonify({'message': f'Prediction {pred_id} not found'}), 404
    
    return jsonify({"id": prediction.id,
                "id_model": prediction.id_modelo,
                "id_image": prediction.id_image,
                "instances": prediction.instances,
                "confidence": prediction.confidence,
                "x_pb1": prediction.x_pb1,
                "y_bp1": prediction.y_pb1,
                "x_bp2": prediction.x_pb2,
                "y_pb2": prediction.y_pb2
        })


"""Actualizar un dato en la tabla model detection"""

@prediction_bp.put("/prediction")
@prediction_bp.put("/prediction/<int:pred_id>")
def put_predict(pred_id = None):
    payload = request.get_json()

    if pred_id is None:
        return jsonify({'message': 'Missing pred_id'}), 400
    
    prediction = db.session.get(ClassificationImage, pred_id)

    if prediction is None:
        return jsonify({'message': f'ClassificationImage {pred_id} not found'}), 404
    
    for k,v in payload.items():
        if k == "instances":
            prediction.instances = v
        elif k == "confidence":
            prediction.confidence = v
        elif k == "x_bp1":
            prediction.x_pb1 = v
        elif k == "y_bp1":
            prediction.y_pb1 = v
        elif k == "x_bp2":
            prediction.x_pb2 = v
        elif k == "y_bp2":
            prediction.y_pb2 = v

    
    db.session.commit()
    return jsonify({'message': f'ClassificationImage {pred_id} updated successfully'})