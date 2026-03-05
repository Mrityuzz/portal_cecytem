from django.shortcuts import render
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter

# Configuración de conexión a Google Sheets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(BASE_DIR, "credenciales", "credenciales.json"), scope)
client = gspread.authorize(creds)
sheet = client.open("BD_Alumnos").sheet1


def reporte_general(request):
    try:
        # Obtener todos los registros desde la hoja
        registros = sheet.get_all_records()

        # --- Alumnos por carrera ---
        carreras = [registro.get("Carrera tecnica") for registro in registros if registro.get("Carrera tecnica")]
        conteo_carreras = Counter(carreras)

        contexto = {
            "conteo_carreras": dict(conteo_carreras),
            "total_alumnos": len(registros),  
        }
        return render(request, "reportes/reporte_general.html", contexto)

    except Exception as e:
        return render(request, "reportes/reporte_general.html", {
            "conteo_carreras": {},
            "total_alumnos": 0,
            "error": f"Ocurrió un error al abrir la hoja: {e}"
        })
