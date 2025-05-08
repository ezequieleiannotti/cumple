import os
from flask import Flask, request, make_response
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slack_utils import verificar_slack_request, manejar_comando

load_dotenv()
app = Flask(__name__)

# Función para acceder a Google Sheets
def obtener_datos_google_sheets():
    # Define el alcance de acceso
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Ruta al archivo JSON de credenciales de Google Cloud
    json_path = "path/to/your/credentials.json"  # Cambia esta ruta a donde guardaste tu archivo JSON

    # Autenticación con el archivo JSON de credenciales
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)

    # Autorizar acceso
    client = gspread.authorize(creds)

    # Abre tu hoja de cálculo por nombre
    spreadsheet = client.open("flow").sheet1  # Cambia esto al nombre correcto de tu hoja

    # Obtiene todos los registros
    data = spreadsheet.get_all_records()

    return data

@app.route("/cumple", methods=["POST"])
def comando_cumple():
    if not verificar_slack_request():
        return make_response("Verificación fallida", 403)

    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")
    text = request.form.get("text")
    comando = request.form.get("command")

    # Aquí puedes obtener datos de Google Sheets si es necesario
    datos_cumple = obtener_datos_google_sheets()
    print(datos_cumple)  # Muestra los datos en consola (opcional)

    respuesta = manejar_comando(text, user_id, user_name, comando)
    return make_response(respuesta, 200)

@app.route("/cumples", methods=["POST"])
def comando_cumples():
    return comando_cumple()  # Usa la misma lógica

@app.route("/", methods=["GET"])
def index():
    return "Bot de cumpleaños activo"

if __name__ == "__main__":
    app.run(debug=True)
