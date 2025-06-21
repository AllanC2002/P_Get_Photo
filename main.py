from flask import Flask, request, jsonify, Response
from services.functions import get_userphoto
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")

@app.route("/get-photo", methods=["GET"])
def get_photo():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token missing or invalid"}), 401

    token = auth_header.replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")

        if not user_id:
            return jsonify({"error": "Invalid token data"}), 401

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    try:
        image_data, content_type = get_userphoto(user_id)
        if not image_data:
            return jsonify({"error": "Image not found"}), 404

        return Response(image_data, mimetype=content_type)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
