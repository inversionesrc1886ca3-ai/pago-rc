[3:52 a.m., 26/3/2026] Eduardo Meza: import os
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

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
[3:56 a.m., 26/3/2026] Eduardo Meza: import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app)

# ESTA ES LA RUTA QUE TE ESTÁ DANDO 404 (La estamos creando aquí)
@app.route('/')
def home():
    return "Servidor Inversiones RC - Eon: ACTIVO", 200

# ESTA ES LA RUTA PARA EL BANCO (VIVO / PING)
@app.route('/webhook-bnc', methods=['GET', 'POST'])
def webhook_bnc():
    if request.method == 'GET':
        return "OK", 200
    
    # Respuesta estándar para el POST del banco
    return jsonify({
        "Reference": "RECIBIDO",
        "AuthorizationCode": "000000",
        "SwAlreadySent": False
    }), 200

if __name__ == '__main__':
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
