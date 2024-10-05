import requests
import json
import pandas as pd

# Configuración de la URL de la API y la API Key
base_url = "http://192.168.1.50:8080"  # Asegúrate de que esta URL sea correcta
api_key = "tupassword"  # La API Key confirmada
instance = "Prueba"  # Cambia esto si tu instancia se llama diferente

# Leer el archivo Excel
excel_file_path = r"ruta del excel" # Asegúrate de que esta URL sea correcta
df = pd.read_excel(excel_file_path)

# Encabezados
headers = {
    "Content-Type": "application/json",
    "apikey": api_key  # Usando apikey
}

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    phone_number = f"549{row['telefono']}@s.whatsapp.net"  # Formato del número
    name = row['nombre']
    message_text = row['mensaje']

    # Datos del mensaje
    data = {
        "number": phone_number,  # Número de teléfono
        "options": {
            "delay": 1200,  # Tiempo en milisegundos
            "presence": "composing"  # Estado de "escribiendo"
        },
        "textMessage": {
            "text": f"{name}, {message_text}"  # Mensaje personalizado
        }
    }

    # URL completa del endpoint para enviar texto
    url = f"{base_url}/message/sendText/{instance}"

    # Enviar la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print(f"Mensaje enviado con éxito a {name}: {response.json()}")
    else:
        print(f"Error al enviar el mensaje a {name}: {response.status_code}, {response.text}")
