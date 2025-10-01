
import base64

def load_image(path):
    try:
        with open(path, "rb") as image_file:
            image_data = image_file.read()
            return base64.b64encode(image_data).decode("ascii") 
    except:
        return None
        
  

