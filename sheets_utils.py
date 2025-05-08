import os
import json
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
import gspread

load_dotenv()

cred_json = os.getenv("GOOGLE_CREDENTIALS")
if not cred_json:
    raise ValueError("La variable GOOGLE_CREDENTIALS no está definida.")

info = json.loads(cred_json)
creds = service_account.Credentials.from_service_account_info(info)
client = gspread.authorize(creds)

SHEET_ID = "1hQZegngYYGgAX-N5_qcXNb5h5wyA_N6Z4zVxMBHFit0"
sheet = client.open_by_key(SHEET_ID).sheet1

def get_upcoming_birthdays():
    rows = sheet.get_all_records()
    hoy = datetime.date.today()
    diez_dias = hoy + datetime.timedelta(days=10)
    resultados = []

    for row in rows:
        nombre = row["Nombre"]
        fecha_str = row["Fecha de nacimiento"]
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            fecha_this_year = fecha.replace(year=hoy.year)
            if hoy <= fecha_this_year <= diez_dias:
                resultados.append((nombre, fecha_this_year.strftime("%Y-%m-%d")))
        except Exception:
            continue

    return resultados

def add_birthday(nombre, fecha_str):
    # validación rápida de formato
    datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
    sheet.append_row([nombre, fecha_str])
