import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URL de tu Google Sheets (No cambia)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def enviar_a_google(datos, ambiente):
    datos['Ambiente'] = ambiente # Esto ayuda a RC a saber si es prueba o real
    try:
        respuesta = requests.post(SCRIPT_URL, json=datos, timeout=15)
        return respuesta.text
    except Exception as e:
        return "error_conexion"

# RUTA DE PRODUCCIÓN
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    datos = request.get_json()
    # Aquí el BNC pondrá su APIKEY en el header automáticamente
    resultado = enviar_a_google(datos, "PRODUCCIÓN")
    
    if "Duplicada" in resultado:
        return jsonify({"status": "error", "message": "Referencia ya registrada"}), 400
    return jsonify({"status": "success"}), 200

# RUTA DE DESARROLLO
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    datos = request.get_json()
    resultado = enviar_a_google(datos, "DESARROLLO")
    return jsonify({"status": "success", "message": "Prueba recibida"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
