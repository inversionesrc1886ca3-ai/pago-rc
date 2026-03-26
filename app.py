from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Nombre del archivo donde se guardarán los pagos
ARCHIVO_PAGOS = 'registro_ventas_rc.csv'

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A')
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar en el "Excel" (archivo CSV)
    file_exists = os.path.isfile(ARCHIVO_PAGOS)
    with open(ARCHIVO_PAGOS, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Si el archivo es nuevo, escribe los títulos de las columnas
        if not file_exists:
            writer.writerow(['Fecha', 'Vendedor', 'Cedula Cliente', 'Referencia', 'Monto Bs'])
        
        writer.writerow([fecha, vendedor, cedula, ref, monto])

    print(f"REGISTRADO EN EXCEL: {vendedor} - Ref: {ref}")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, la ref {ref} ha sido registrada en el sistema."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
