import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE TOKENS (API KEYS) ---
# Aquí colocarás los valores que el BNC te asigne. No deben ser iguales.
TOKEN_PRODUCCION = "VALOR_QUE_TE_DE_EL_BANCO_REAL"
TOKEN_DESARROLLO = "VALOR_QUE_TE_DE_EL_BANCO_PRUEBAS"

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def enviar_a_google(datos, ambiente):
    datos['Ambiente'] = ambiente 
    try:
        respuesta = requests.post(SCRIPT_URL, json=datos, timeout=15)
        return respuesta.text
    except Exception as e:
        return "error_conexion"

# 🚀 RUTA DE PRODUCCIÓN
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    # El BNC envía el token en 'x-api-key'
    token_recibido = request.headers.get("x-api-key")
    
    # Validación: Si el token no coincide con el de Producción, rechazamos
    if token_recibido != TOKEN_PRODUCCION:
        return jsonify({"status": "error", "message": "Token de Producción Inválido"}), 401

    datos = request.get_json()
    resultado = enviar_a_google(datos, "PRODUCCIÓN")
    
    if "Duplicada" in resultado:
        return jsonify({"status": "error", "message": "Referencia Duplicada"}), 400
    return jsonify({"status": "success"}), 200

# 🧪 RUTA DE DESARROLLO
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    token_recibido = request.headers.get("x-api-key")
    
    # Validación: Si el token no coincide con el de Desarrollo, rechazamos
    if token_recibido != TOKEN_DESARROLLO:
        return jsonify({"status": "error", "message": "Token de Desarrollo Inválido"}), 401

    datos = request.get_json()
    resultado = enviar_a_google(datos, "DESARROLLO")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
