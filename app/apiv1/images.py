
from . import image_bp
from flask import request, jsonify
from PIL import Image
import base64, os
import random
from datetime import datetime
from .. import db
from ..models import CocoaImage
from sqlalchemy import MetaData
from ..utils.images import load_image



dir_images_path = "images"
dir_images_bk_path = "image_bk"

if not os.path.exists(dir_images_bk_path):
    os.makedirs(dir_images_bk_path)
    print("Directory has been created")
else:
    ("Directory already extist")

if not os.path.exists(dir_images_path):
    os.makedirs(dir_images_path)
    print("Directory has been created")
else:
    ("Directory already extist")


@image_bp.post('/image')
def post_image():
    id_random = random.randint(1000,9999)
    payload = request.get_json() # Recibo todo el cuerpo del post 
    date = datetime.utcnow()

    localization = payload["localization"]
    decode_image64 = base64.b64decode(payload["image"])
    path_name = f"{dir_images_path}/rgb_image_{str(id_random)}.jpg"

    with open(path_name, "wb") as f:
        f.write(decode_image64)
    cacao = CocoaImage(
        path_name = path_name,
        date = date,
        localization = localization
    )

    db.session.add(cacao)      
    db.session.commit()
    return {"cocoa_image_id": cacao.id}


"""como leer los datos de una tabla"""

@image_bp.get('/image/')
@image_bp.get('/image/<int:image_id>')
def get_image(image_id= None):
    include_image = request.args.get("include_image", "false") == "true"


    if image_id is None:

        cacao_image = CocoaImage.query.all()
        # Como retornar todas las imágenes
        if include_image is False:
            return jsonify([cacao.to_dict() for cacao in cacao_image])
        return jsonify([
            {
                "id": cacao.id, 
                "path_name": cacao.path_name,
                "date": cacao.date,
                "localization": cacao.localization,
                "image_base64":load_image(cacao.path_name)
            }
            for cacao in cacao_image
        ])
    

    cacao_image = db.session.get(CocoaImage, image_id)
    if cacao_image is None:
        return jsonify({'message': f'CocoaImage {image_id} not found'}), 404
    #image_path = cacao_image.path_name
    """with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        encode_image64 = base64.b64encode(image_data).decode("ascii")"""


    #cacao = CocoaImage.query.get(image_id)
    #cacao = db.session.get(CocoaImage, image_id)
    return jsonify({"id": cacao_image.id, 
                    "path_name": cacao_image.path_name,
                    "date": cacao_image.date,
                    "localization": cacao_image.localization,
                    "image_base64":load_image(cacao_image.path_name) if include_image else None
                    })


"""como eliminar los datos de una tabla"""

@image_bp.delete('/image/imagedelete/<int:image_id>')

def delete_image(image_id=None):
    #data = request.get_json()
    #user_id = data.get("id")
    if image_id is None:
        return jsonify({'message': 'Missing user_id'}), 400
    
    cacao = db.session.get(CocoaImage, image_id)
    if cacao is None:
        return jsonify({'message': f'CocoaImage {image_id} not found'}), 404
    db.session.delete(cacao)
    db.session.commit()

    return jsonify({'message': f'User {image_id} deleted successfully'})

