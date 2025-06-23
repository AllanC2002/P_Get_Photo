import requests

BASE_URL = "http://174.129.238.113:8080/get-photo"

# Login first
login_data = {
    "User_mail": "ascorread3",
    "password": "1234"
}
login_response = requests.post("http://52.203.72.116:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Login error:", login_response.status_code, login_response.text)
    exit()

token = login_response.json()["token"]
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(BASE_URL, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    # Guardar la imagen recibida a un archivo local para verificarla
    content_type = response.headers.get('Content-Type', '')
    ext = ''
    if 'jpeg' in content_type:
        ext = 'jpg'
    elif 'png' in content_type:
        ext = 'png'
    else:
        ext = 'bin'

    filename = f"user_photo.{ext}"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Photo saved as {filename}")
else:
    print("Error response:", response.json())
