import os
import requests
import jwt  # Recuerda añadir PyJWT==2.8.0 a tu archivo requirements.txt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE ACCESOS BNC (Diferenciados) ---

# Ambiente: PRODUCCIÓN
LOGIN_PROD = "LOGIN_REAL_BNC"
PWD_PROD = "PASSWORD_REAL_BNC"

# Ambiente: DESARROLLO
LOGIN_DEV = "LOGIN_PRUEBAS_BNC"
PWD_DEV = "PASSWORD_PRUEBAS_BNC"

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def validar_y_procesar(token_completo, login_esperado, pwd_esperado, ambiente):
    try:
        # 1. El BNC suele enviar "Bearer [TOKEN]", limpiamos el texto si es necesario
        token = token_completo.replace("Bearer ", "") if token_completo else ""
        
        # 2. Decodificamos el JWT con el Password y Login del ambiente
        payload = jwt.decode(token, pwd_esperado, algorithms=["HS256"])
        
        if payload.get("iss") != login_esperado:
            return False, "Login (iss) no coincide"
            
        # 3. Si todo es correcto, enviamos al Excel
        datos = request.get_json()
        datos['Ambiente'] = ambiente
        requests.post(SCRIPT_URL, json=datos, timeout=15)
        return True, "Ok"
    except Exception as e:
        return False, str(e)

# 🚀 URL DE NOTIFICACIÓN: PRODUCCIÓN
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_PROD, PWD_PROD, "PRODUCCIÓN")
    
    if exito:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": msg}), 401

# 🧪 URL DE NOTIFICACIÓN: DESARROLLO
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_DEV, PWD_DEV, "DESARROLLO")
    
    if exito:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": msg}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
