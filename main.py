import os
import json
from flask import Flask, request, make_response
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials  # Cambio importante
from slack_utils import verificar_slack_request, manejar_comando

load_dotenv()
app = Flask(__name__)

# Función para acceder a Google Sheets
def obtener_datos_google_sheets():
    # Cargamos el JSON desde la variable de entorno
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    creds_dict = json.loads(creds_json)

    # Creamos las credenciales
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

    # Autorizamos el acceso
    client = gspread.authorize(creds)

    # Abre la hoja por ID (más seguro que por nombre)
    spreadsheet = client.open_by_key("flow").sheet1  # reemplazá con el ID real

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

    datos_cumple = obtener_datos_google_sheets()
    print(datos_cumple)  # opcional

    respuesta = manejar_comando(text, user_id, user_name, comando)
    return make_response(respuesta, 200)

@app.route("/cumples", methods=["POST"])
def comando_cumples():
    return comando_cumple()

@app.route("/", methods=["GET"])
def index():
    return "Bot de cumpleaños activo"

if __name__ == "__main__":
    app.run(debug=True)

