from . import model_bp
from ..models import ModelDetection
from flask import request, jsonify
from .. import db


@model_bp.post("/model")
def post_model():
    payload = request.get_json() # Recibo todo el cuerpo del post 
    """Solución 2"""
    # creo un query de consulta 

    name_exist = ModelDetection.query.filter_by(path_name = payload["path"]).first()
    if name_exist:
        return {"message": f"Path name {payload["path"]} already exist"}
    
    path_name = payload["path"]
    description = payload["description"]
    f1_score = payload["f1_score"]# validar
    #model = db.session.get(ModelDetection, 12)
    
    model = ModelDetection(
        path_name = path_name,
        description = description,
        f1_score = f1_score
    )
    db.session.add(model)      
    db.session.commit()
    return {"message": f"Model id {model.id}  created successfully"}

"""como obtener un dato de la  tabla Model detection"""




@model_bp.get("/model")
@model_bp.get("/model/<int:model_id>")
def get_model(model_id = None):

    if model_id is None:
        models = ModelDetection.query.all()
        return jsonify([model.to_dict() for model in models])
        #return jsonify({'message': 'Missing model_id'}), 400
    
    model = db.session.get(ModelDetection, model_id)
    if model is None:
        return jsonify({'message': f'ModelDetection {model_id} not found'}), 404
    
    #db.session.delete(model)
    #db.session.commit()
    
    return jsonify({"id":model.id, 
            "path_name": model.path_name, 
            "description": model.description,
            "f1_score": model.f1_score})



@model_bp.put("/model")
@model_bp.put("/model/<int:model_id>")
def put_model(model_id = None):
    if model_id is None:
        return jsonify({'message': 'Missing model_id'}), 400
    payload = request.get_json()
    prediction = db.session.get(ModelDetection, model_id)

    if prediction is None:
        return jsonify({'message': f'ModelDetection {model_id} not found'}), 400

    for k,v in payload.items():
        if k == "path_name":
            prediction.path_name = v
        elif k == "description":
            prediction.description = v
        elif k == "f1_score":
            prediction.f1_score = v

    db.session.commit()
    return jsonify({'message': f'ModelDetection {model_id} updated successfully'})


"""como eliminar los datos de una tabla"""



@model_bp.delete("/model/<int:model_id>")
def delete_model(model_id = None):
    if model_id == None:
        return jsonify({'message': 'Missing model_id'}), 400
    
    model = db.session.get(ModelDetection, model_id)

    if model is None:
        return jsonify({'message': f'ModelDetection {model_id} not found'}), 404
    
    db.session.delete(model)
    db.session.commit()
    return jsonify({'message': f'ModelDetection {model_id} deleted successfully'})
