from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import os
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de conexión a Google Sheets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(BASE_DIR, "credenciales", "credenciales.json"), scope)
client = gspread.authorize(creds)
sheet = client.open("BD_Alumnos").sheet1


def lista_asistencia(request):
    alumnos = []
    try:
        registros = sheet.get_all_records()
        carrera_filtro = request.GET.get("carrera")

        for registro in registros:
            alumno = {
                "alumno": registro.get("Alumno", ""),
                "num_control": registro.get("Numero de control", ""),
                "telefono": registro.get("Telefono", "") or registro.get("Teléfono", ""),
                "carrera": registro.get("Carrera tecnica", ""),
                "entrada": registro.get("Entrada", ""),
                "salida": registro.get("Salida", ""),
                "veces": registro.get("Veces", ""),   
            }

            if carrera_filtro and carrera_filtro.lower() != "todas":
                if alumno["carrera"] and carrera_filtro.lower() in str(alumno["carrera"]).lower():
                    alumnos.append(alumno)
            else:
                alumnos.append(alumno)

    except Exception as e:
        return render(request, "asistencia/lista.html", {
            "alumnos": [],
            "error": f"Ocurrió un error al abrir la hoja: {e}"
        })

    return render(request, "asistencia/lista.html", {
        "alumnos": alumnos,
        "carrera_filtro": carrera_filtro
    })


# Vista JSON para actualización en tiempo real
def lista_asistencia_json(request):
    registros = sheet.get_all_records()
    alumnos = []
    for registro in registros:
        alumnos.append({
            "alumno": registro.get("Alumno", ""),
            "num_control": registro.get("Numero de control", ""),
            "telefono": registro.get("Telefono", "") or registro.get("Teléfono", ""),
            "carrera": registro.get("Carrera tecnica", ""),
            "entrada": registro.get("Entrada", ""),
            "salida": registro.get("Salida", ""),
            "veces": registro.get("Veces", ""),   
        })
    return JsonResponse({"alumnos": alumnos})


# Vista para descargar el Excel directamente desde Google Sheets
def descargar_excel(request):
    sheet_id = "11B1vWbYto5hD0G0FNMIqUkx7W-HxTeE4fzq1bqLytiU"
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    access_token = creds.get_access_token().access_token
    response = requests.get(export_url, headers={"Authorization": f"Bearer {access_token}"})

    if response.status_code == 200:
        return HttpResponse(
            response.content,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="BD_Alumnos.xlsx"'}
        )
    else:
        return HttpResponse("Error al descargar el archivo desde Google Sheets", status=500)
