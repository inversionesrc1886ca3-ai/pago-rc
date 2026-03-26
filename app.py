import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URL de tu Google Sheets (No cambia)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def enviar_a_google(datos, ambiente):
    datos['Ambiente'] = ambiente 
    try:
        respuesta = requests.post(SCRIPT_URL, json=datos, timeout=15)
        return respuesta.text
    except Exception as e:
        return "error_conexion"

# RUTA DE PRODUCCIÓN
@app.route('/webhook-bnc', methods=['POST'])
def webhook_produccion():
    # COMPARACIÓN: Aquí leemos la variable que el banco colocará
    api_key_del_banco = request.headers.get("x-api-key")
    
    datos = request.get_json()
    
    # Procesamos el envío al Excel de Inversiones RC
    resultado = enviar_a_google(datos, "PRODUCCIÓN")
    
    if "Duplicada" in resultado:
        return jsonify({"status": "error", "message": "Referencia ya registrada"}), 400
    
    # Respondemos 200 OK al banco para que sepan que recibimos bien la llave
    return jsonify({"status": "success", "info": "Recibido con llave"}), 200

# RUTA DE DESARROLLO
@app.route('/webhook-bnc-dev', methods=['POST'])
def webhook_desarrollo():
    # También leemos la llave en desarrollo por si el banco la envía ahí
    api_key_del_banco = request.headers.get("x-api-key")
    
    datos = request.get_json()
    resultado = enviar_a_google(datos, "DESARROLLO")
    return jsonify({"status": "success", "message": "Prueba de desarrollo recibida"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
