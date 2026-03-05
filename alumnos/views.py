from django.shortcuts import render, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Configuración de conexión a Google Sheets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(BASE_DIR, "credenciales", "credenciales.json"), scope)
client = gspread.authorize(creds)
sheet = client.open("BD_Alumnos").sheet1


def lista_alumnos(request):
    try:
        registros = sheet.get_all_records()
        alumnos = []
        for i, registro in enumerate(registros, start=2):  
            alumnos.append({
                "id": i,
                "nombre": registro.get("Alumno", ""),
                # Ajuste: aceptar ambas variantes de encabezado
                "num_control": registro.get("Numero de control", "") or registro.get("Número de control", ""),
                "telefono": registro.get("Telefono", "") or registro.get("Teléfono", ""),
                "carrera": registro.get("Carrera tecnica", "") or registro.get("Carrera técnica", ""),
                "entrada": registro.get("Entrada", ""),
                "salida": registro.get("Salida", ""),
                "veces": registro.get("Veces", ""),
            })
    except Exception as e:
        return render(request, "alumnos/lista.html", {
            "alumnos": [],
            "error": str(e)
        })

    return render(request, "alumnos/lista.html", {"alumnos": alumnos})


def agregar_alumno(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        num_control = request.POST.get("num_control")
        telefono = request.POST.get("telefono")
        carrera = request.POST.get("carrera")

        try:
            # Agregar nueva fila en Google Sheets
            sheet.append_row([nombre, num_control, telefono, carrera, "", "", ""])
        except Exception as e:
            return render(request, "alumnos/agregar.html", {
                "error": str(e)
            })

        return redirect("lista_alumnos")

    return render(request, "alumnos/agregar.html")


def editar_alumno(request, fila_id):
    if request.method == "POST":
        sheet.update_cell(fila_id, 1, request.POST.get("nombre"))
        sheet.update_cell(fila_id, 2, request.POST.get("num_control"))
        sheet.update_cell(fila_id, 3, request.POST.get("telefono"))
        sheet.update_cell(fila_id, 4, request.POST.get("carrera"))
        return redirect("lista_alumnos")

    alumno = {
        "id": fila_id,
        "nombre": sheet.cell(fila_id, 1).value,
        "num_control": sheet.cell(fila_id, 2).value,
        "telefono": sheet.cell(fila_id, 3).value,
        "carrera": sheet.cell(fila_id, 4).value,
    }
    return render(request, "alumnos/editar.html", {"alumno": alumno})


def eliminar_alumno(request, fila_id):
    sheet.delete_rows(fila_id)
    return redirect("lista_alumnos")
