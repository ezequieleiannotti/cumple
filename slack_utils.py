import os
from flask import request
import hashlib
import hmac
import time
from google_utils import agregar_cumple, obtener_cumples_proximos

def verificar_slack_request():
    timestamp = request.headers['X-Slack-Request-Timestamp']
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    my_signature = 'v0=' + hmac.new(
        os.getenv("SLACK_SIGNING_SECRET").encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    slack_signature = request.headers['X-Slack-Signature']
    return hmac.compare_digest(my_signature, slack_signature)

def manejar_comando(texto, user_id, user_name, comando):
    if comando == "/cumple":
        return agregar_cumple(user_id, user_name, texto.strip())
    elif comando == "/cumples":
        return obtener_cumples_proximos()
    return "Comando no reconocido."
