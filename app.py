import os
import requests
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Esto es vital para que no dé "Failed to fetch" en el celular
CORS(app, resources={r"/*": {"origins": "*"}})

# CONFIGURACIÓN BNC
PWD_PROD = "IRC_Secure_Prod_!99*77"
LOGIN_PROD = "rc_prod_admin"
# REEMPLAZA ESTO CON TU URL DE GOOGLE APPS SCRIPT
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

@app.route('/webhook-bnc', methods=['POST', 'OPTIONS'])
def webhook_produccion():
    if request.method == 'OPTIONS': return jsonify({"ok": True}), 200
    token_auth = request.headers.get("Authorization")
    try:
        token = token_auth.replace("Bearer ", "")
        payload = jwt.decode(token, PWD_PROD, algorithms=["HS256"])
        if payload.get("iss") == LOGIN_PROD:
            datos = request.get_json()
            datos['action'] = "registrar"
            requests.post(SCRIPT_URL, json=datos, timeout=10)
            return jsonify({"status": "success"}), 200
    except:
        return jsonify({"status": "error"}), 401

@app.route('/consultar-pago', methods=['POST', 'OPTIONS'])
def consultar_pago():
    if request.method == 'OPTIONS': return jsonify({"ok": True}), 200
    try:
        ref = request.get_json().get('referencia')
        res = requests.post(SCRIPT_URL, json={"action": "verificar", "referencia": ref}, timeout=10)
        return res.text, 200
    except:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
