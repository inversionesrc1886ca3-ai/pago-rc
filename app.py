import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta principal para que NO de error 404 al entrar al link directo
@app.route('/')
def home():
    return "Servidor de Inversiones RC - Marca Eon: OPERATIVO", 200

# Ruta para el banco (VIVO / PING)
@app.route('/webhook-bnc', methods=['GET', 'POST'])
def webhook_bnc():
    if request.method == 'GET':
        return "OK", 200
    
    # Respuesta para pruebas del banco
    return jsonify({
        "Reference": "PROCESADO",
        "AuthorizationCode": "000000",
        "SwAlreadySent": False
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
