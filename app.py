from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Tu link de SheetDB
SHEETDB_URL = 'https://sheetdb.io/api/v1/bhei1rzhpt7os'

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A')
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Preparamos los datos para Google Sheets
    # Asegúrate de que los nombres coincidan con los títulos de tu Excel
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
        # Enviamos los datos a SheetDB
        requests.post(SHEETDB_URL, json=row_data)
        print(f"Excel Actualizado: {vendedor} - Ref {ref}")
    except Exception as e:
        print(f"Error guardando en Excel: {e}")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, la ref {ref} ha sido registrada en el Excel."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
