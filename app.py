import os
import requests
import jwt  # Necesitas instalarlo: pip install PyJWT
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- LLAVES SECRETAS PARA JWT (Proporcionadas por el BNC) ---
# El Token JWT se firma con una "Secret Key". Estas no deben ser iguales.
JWT_SECRET_PROD = "SECRETO_REAL_DEL_BANCO"
JWT_SECRET_DEV = "SECRETO_PRUEBAS_DEL_BANCO"

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def validar_jwt(token, secreto):
    try:
        # El banco envía el token, nosotros lo verificamos con el secreto
        decoded = jwt.decode(token, secreto, algorithms=["HS256"])
        return True, decoded
    except Exception as e:
        return False, str(e)

# 🚀 RUTA DE PRODUCCIÓN (JWT)
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    # El BNC suele enviar el JWT en el header 'Authorization' o 'x-api-key'
    token = request.headers.get("x-api-key")
    
    esta_bien, datos_token = validar_jwt(token, JWT_SECRET_PROD)
    
    if not esta_bien:
        return jsonify({"status": "error", "message": "JWT Producción Inválido"}), 401

    datos = request.get_json()
    respuesta_excel = requests.post(SCRIPT_URL, json={**datos, "Ambiente": "PRODUCCIÓN"})
    return jsonify({"status": "success"}), 200

# 🧪 RUTA DE DESARROLLO (JWT)
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    token = request.headers.get("x-api-key")
    
    esta_bien, datos_token = validar_jwt(token, JWT_SECRET_DEV)
    
    if not esta_bien:
        return jsonify({"status": "error", "message": "JWT Desarrollo Inválido"}), 401

    datos = request.get_json()
    requests.post(SCRIPT_URL, json={**datos, "Ambiente": "DESARROLLO"})
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
   
   
