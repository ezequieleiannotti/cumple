import os
from flask import Flask, request, make_response
from dotenv import load_dotenv
from slack_utils import verificar_slack_request, manejar_comando

load_dotenv()
app = Flask(__name__)

@app.route("/cumple", methods=["POST"])
def comando_cumple():
    if not verificar_slack_request():
        return make_response("Verificación fallida", 403)

    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")
    text = request.form.get("text")
    comando = request.form.get("command")

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
