import base64
import requests
from conections.mongo import conection_mongo

def get_userphoto(user_id):
    db = conection_mongo()
    images_collection = db["Images"]

    user_image = images_collection.find_one({"Id_User": user_id})

    if user_image:
        img_data = base64.b64decode(user_image["image_base64"])
        content_type = user_image.get("content_type", "application/octet-stream")
        return img_data, content_type

    default_image = images_collection.find_one({"url": {"$exists": True}})
    if default_image:
        url = default_image["url"]
        resp = requests.get(url)
        if resp.status_code == 200:
            content_type = resp.headers.get("Content-Type", "image/png")
            return resp.content, content_type

    return None, None
