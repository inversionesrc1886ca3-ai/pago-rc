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
    
    # Extraemos todos los campos del formulario
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A')
    telefono = datos.get('Phone', 'N/A') # Captura el teléfono
    banco = datos.get('Bank', 'N/A')    # Captura el banco
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Los nombres a la izquierda deben ser EXACTOS a tus títulos en Excel
    row_data = {
        "data": [
            {
                "Fecha": fecha,
                "Vendedor": vendedor,
                "Cedula": cedula,
                "Telefono": telefono, 
                "Banco": banco,
                "Referencia": ref,
                "Monto": monto
            }
        ]
    }

    try:
        # Enviamos la fila completa a Google Sheets
        requests.post(SHEETDB_URL, json=row_data)
        print(f"Registro completo: {vendedor} | Tel: {telefono} | Banco: {banco}")
    except Exception as e:
        print(f"Error enviando a SheetDB: {e}")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, el pago de {monto} Bs. ha sido registrado en el Excel."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
