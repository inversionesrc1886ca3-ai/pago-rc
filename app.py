import os
import requests
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- Esto es lo que arregla el "Failed to fetch"

app = Flask(__name__)
# Esta línea permite que tu formulario naranja pueda hablar con el servidor de Render
CORS(app, resources={r"/*": {"origins": "*"}})

# --- CONFIGURACIÓN DE ACCESOS BNC ---
LOGIN_PROD = "rc_prod_admin"
PWD_PROD = "IRC_Secure_Prod_!99*77"
LOGIN_DEV = "rc_dev_user"
PWD_DEV = "IRC_Test_Dev_#44_2026"

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def validar_y_procesar(token_auth, login_esperado, pwd_esperado, ambiente_nombre):
    try:
        # Si el pago viene de tu formulario (sin token), saltamos la validación JWT
        # para que puedas registrar pagos manualmente también.
        if not token_auth:
            datos = request.get_json()
            datos['Ambiente'] = f"{ambiente_nombre} (MANUAL)"
            requests.post(SCRIPT_URL, json=datos, timeout=15)
            return True, "Ok"

        # Validación para el Banco (JWT)
        token = token_auth.replace("Bearer ", "")
        payload = jwt.decode(token, pwd_esperado, algorithms=["HS256"])
        if payload.get("iss") != login_esperado:
            return False, "Login no coincide"
            
        datos = request.get_json()
        datos['Ambiente'] = ambiente_nombre
        requests.post(SCRIPT_URL, json=datos, timeout=15)
        return True, "Ok"
    except Exception as e:
        return False, str(e)

@app.route('/webhook-bnc', methods=['POST', 'OPTIONS'])
def webhook_produccion():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_PROD, PWD_PROD, "PRODUCCIÓN")
    return (jsonify({"status": "success"}), 200) if exito else (jsonify({"error": msg}), 401)

@app.route('/webhook-bnc-dev', methods=['POST', 'OPTIONS'])
def webhook_desarrollo():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_DEV, PWD_DEV, "DESARROLLO")
    return (jsonify({"status": "success"}), 200) if exito else (jsonify({"error": msg}), 401)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
