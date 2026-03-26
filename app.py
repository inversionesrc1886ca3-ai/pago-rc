from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(_name_)
CORS(app)

# Tu link de SheetDB
SHEETDB_URL = 'https://sheetdb.io/api/v1/bhei1rzhpt7os'

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    
    # --- CORRECCIÓN AQUÍ ---
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A') # Antes podía haber confusión con el nombre
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Los nombres a la izquierda (ej: "Cedula") deben ser IGUALES 
    # a los títulos que pusiste en la fila 1 de tu Excel.
    row_data = {
        "data": [
            {
                "Fecha": fecha,
                "Vendedor": vendedor,
                "Cedula": cedula, 
                "Referencia": ref,
                "Monto": monto
            }
        ]
    }

    try:
        requests.post(SHEETDB_URL, json=row_data)
        print(f"Excel Actualizado: {vendedor} - CI: {cedula}")
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, la ref {ref} y CI {cedula} han sido registradas."
    })

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)
