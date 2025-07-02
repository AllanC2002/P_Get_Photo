import pytest
from unittest.mock import patch, MagicMock
from flask import Response
from io import BytesIO

from main import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_get_photo_success(client):
    mock_token = "mocktoken"
    mock_user_id = "user123"
    fake_image_data = b"fake image content"
    content_type = "image/png"

    with patch("main.jwt.decode") as mock_jwt_decode, \
         patch("services.functions.conection_mongo") as mock_conection_mongo:

        mock_jwt_decode.return_value = {"user_id": mock_user_id}

        # Simulate the database connection and image base64 data
        mock_db = MagicMock()
        mock_images_collection = MagicMock()
        mock_images_collection.find_one.return_value = {
            "image_base64": fake_image_data.hex(),
            "content_type": content_type
        }
        mock_db.__getitem__.return_value = mock_images_collection
        mock_conection_mongo.return_value = mock_db

        response = client.get(
            "/get-photo",
            headers={"Authorization": f"Bearer {mock_token}"}
        )

        assert response.status_code == 200
        assert isinstance(response, Response)
        assert response.content_type == content_type
