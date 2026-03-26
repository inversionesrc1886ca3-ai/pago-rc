from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

SHEETDB_URL = 'https://sheetdb.io/api/v1/bhei1rzhpt7os'

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A')
    telefono = datos.get('Phone', 'N/A')
    banco = datos.get('Bank', 'N/A')
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # AQUÍ DEBEN COINCIDIR CON LOS TÍTULOS DE TU EXCEL
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
        requests.post(SHEETDB_URL, json=row_data)
        print(f"Excel Actualizado por {vendedor}")
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, la ref {ref} ha sido registrada correctamente."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
