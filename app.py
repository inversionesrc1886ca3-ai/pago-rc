from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(name)
CORS(app)

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    referencia = datos.get('Reference', 'N/A')
    # Mensaje temporal hasta tener las llaves del BNC
    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: Pago con ref {referencia} en proceso de validación."
    })

if name == 'main':
    app.run(host='0.0.0.0', port=10000)
