import os
import requests
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS # Importamos la librería de permisos

app = Flask(__name__)
# ESTA LÍNEA ES LA QUE ARREGLA EL 'FAILED TO FETCH'
CORS(app, resources={r"/*": {"origins": "*"}})

# CONFIGURACIÓN BNC
PWD_PROD = "IRC_Secure_Prod_!99*77"
LOGIN_PROD = "rc_prod_admin"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

@app.route('/webhook-bnc', methods=['POST', 'OPTIONS'])
def webhook_produccion():
    # Responder a la pregunta de seguridad del navegador
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    token_auth = request.headers.get("Authorization")
    try:
        # Si el banco manda el token, lo validamos
        if token_auth:
            token = token_auth.replace("Bearer ", "")
            payload = jwt.decode(token, PWD_PROD, algorithms=["HS256"])
            if payload.get("iss") != LOGIN_PROD:
                return jsonify({"error": "Login incorrecto"}), 401
        
        # Enviamos al Excel
        datos = request.get_json()
        datos['action'] = "registrar"
        datos['Ambiente'] = "BNC PRODUCCIÓN"
        requests.post(SCRIPT_URL, json=datos, timeout=10)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/consultar-pago', methods=['POST', 'OPTIONS'])
def consultar_pago():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        ref = request.get_json().get('referencia')
        res = requests.post(SCRIPT_URL, json={"action": "verificar", "referencia": ref}, timeout=10)
        return res.text, 200
    except:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
