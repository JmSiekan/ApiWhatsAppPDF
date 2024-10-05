import requests
import json
import pandas as pd
import base64
import os

# Configuración de la URL de la API y la API Key
base_url = "http://192.168.1.50:8080"
api_key = "tupassword"
instance = "Prueba"

# Leer el archivo Excel
excel_file_path = r"C:\Users\Asus\Desktop\armada.xlsx"
df = pd.read_excel(excel_file_path)

# Encabezados
headers = {
    "Content-Type": "application/json",
    "apikey": api_key  # Usando apikey
}

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    phone_number = f"549{row['telefono']}@s.whatsapp.net"
    name = row['nombre']
    message_text = row['mensaje']
    file_path = row['ruta']  # Leer la ruta del archivo desde la columna "ruta"

    # Comprobar la extensión del archivo
    file_extension = os.path.splitext(file_path)[1].lower()  # Obtener la extensión del archivo

    # Leer y codificar el archivo en Base64
    try:
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode()
    except Exception as e:
        print(f"Error al leer el archivo para {name}: {str(e)}")
        continue  # Si hay un error, continuar con la siguiente fila

    # Imprimir la longitud del string codificado para verificar
    print(f"Longitud del string codificado para {name}: {len(encoded_file)}")

    # Datos del mensaje para enviar el archivo
    if file_extension == '.pdf':
        data = {
            "number": phone_number,  # Número de teléfono
            "mediaMessage": {
                "mediatype": "document",  # Especifica que es un documento
                "fileName": os.path.basename(file_path),  # Nombre del archivo PDF
                "caption": f"Aquí tienes el documento que solicitaste, {name}.",
                "media": encoded_file  # Usa la cadena Base64
            },
            "options": {
                "delay": 0,
                "presence": "composing",
                "linkPreview": True
            }
        }
    elif file_extension in ['.jpg', '.jpeg', '.png']:  # También puedes agregar otras extensiones de imagen si es necesario
        data = {
            "number": phone_number,  # Número de teléfono
            "mediaMessage": {
                "mediatype": "image",  # Especifica que es una imagen
                "fileName": os.path.basename(file_path),  # Nombre del archivo de imagen
                "caption": f"Aquí tienes la imagen que solicitaste, {name}.",
                "media": encoded_file  # Usa la cadena Base64
            },
            "options": {
                "delay": 0,
                "presence": "composing",
                "linkPreview": True
            }
        }
    else:
        print(f"El archivo {file_path} no es un tipo soportado (PDF o JPG).")
        continue  # Si el tipo de archivo no es soportado, continuar

    # URL completa del endpoint para enviar el archivo
    url = f"{base_url}/message/sendMedia/{instance}"

    # Enviar la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print(f"Archivo enviado con éxito a {name}: {response.json()}")
    else:
        print(f"Error al enviar el archivo a {name}: {response.status_code}, {response.text}")
