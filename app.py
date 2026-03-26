import os
import requests
import jwt  # Requiere PyJWT en el archivo requirements.txt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE ACCESOS BNC (Inversiones RC) ---
# Los Login se mantienen, los Passwords son nuevos y diferentes

# Ambiente: PRODUCCIÓN
LOGIN_PROD = "rc_prod_admin"
PWD_PROD = "IRC_Secure_Prod_!99*77"  # <--- Nuevo Password Producción

# Ambiente: DESARROLLO
LOGIN_DEV = "rc_dev_user"
PWD_DEV = "IRC_Test_Dev_#44_2026"     # <--- Nuevo Password Desarrollo

# URL de tu Google Sheets (Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def validar_y_procesar(token_auth, login_esperado, pwd_esperado, ambiente_nombre):
    try:
        # 1. Extraemos el token del header Authorization (Bearer)
        token = token_auth.replace("Bearer ", "") if token_auth else ""
        
        # 2. Validamos el JWT con el Password correspondiente (HS256)
        payload = jwt.decode(token, pwd_esperado, algorithms=["HS256"])
        
        # 3. Validamos que el Login (iss) coincida
        if payload.get("iss") != login_esperado:
            return False, "Login (iss) no coincide"
            
        # 4. Enviamos los datos al Excel
        datos = request.get_json()
        datos['Ambiente'] = ambiente_nombre
        requests.post(SCRIPT_URL, json=datos, timeout=15)
        return True, "Ok"
    except Exception as e:
        return False, str(e)

# 🚀 ENDPOINT DE PRODUCCIÓN
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_PROD, PWD_PROD, "PRODUCCIÓN")
    
    if exito:
        return jsonify({"status": "success", "msg": "Pago Real Registrado"}), 200
    return jsonify({"status": "error", "message": msg}), 401

# 🧪 ENDPOINT DE DESARROLLO
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    token_auth = request.headers.get("Authorization")
    exito, msg = validar_y_procesar(token_auth, LOGIN_DEV, PWD_DEV, "DESARROLLO")
    
    if exito:
        return jsonify({"status": "success", "msg": "Prueba Registrada"}), 200
    return jsonify({"status": "error", "message": msg}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


