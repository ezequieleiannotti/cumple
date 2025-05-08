import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime, timedelta

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credenciales.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(os.getenv("SHEET_ID")).worksheet(os.getenv("SHEET_NAME"))

def agregar_cumple(user_id, user_name, fecha_str):
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")  # Valida el formato
        sheet.append_row([user_id, user_name, fecha_str])
        return "✅ Cumpleaños registrado correctamente."
    except ValueError:
        return "❌ Formato inválido. Usá: /cumple 1990-05-08"

def obtener_cumples_proximos():
    hoy = datetime.now()
    en_10_dias = hoy + timedelta(days=10)
    registros = sheet.get_all_records()
    proximos = []

    for r in registros:
        cumple = datetime.strptime(r['fecha'], "%Y-%m-%d")
        cumple_este_anio = cumple.replace(year=hoy.year)
        if hoy <= cumple_este_anio <= en_10_dias:
            proximos.append(f"{r['nombre']} cumple el {cumple_este_anio.strftime('%d/%m')} 🎉")

    return "\n".join(proximos) if proximos else "No hay cumpleaños en los próximos 10 días."
