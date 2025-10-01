from flask import Blueprint



prediction_bp = Blueprint("prediction", __name__)
model_bp = Blueprint("model", __name__)
image_bp = Blueprint("image", __name__)

from . import images, general, ml_models, predictions ## su error estaba aquí

