import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Esta es la URL de tu Google Script que me acabas de pasar
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxxI1SPoPIVyMmcvqKhURDD5vf94seZOrtRKeD39x5TNT2mEtRVkXWCgy2a_cJ4VoDg7A/exec"

def anotar_en_excel(datos):
    try:
        # Enviamos los datos directamente al Script de Google
        respuesta = requests.post(SCRIPT_URL, json=datos, timeout=10)
        if "Éxito" in respuesta.text:
            return True
        print(f"Respuesta del script: {respuesta.text}")
        return False
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

@app.route('/')
def home():
    return "Servidor Inversiones RC - CONEXIÓN POR SCRIPT ACTIVA", 200

@app.route('/auth', methods=['POST'])
def auth():
    return "token_valido_rc", 200

@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    datos = request.get_json()
    
    # Intentar anotar en la hoja de cálculo vía Script
    if anotar_en_excel(datos):
        return jsonify({
            "status": "success", 
            "message": f"Referencia {datos.get('DestinyBankReference')} anotada con éxito"
        }), 200
    else:
        return jsonify({
            "status": "error", 
            "message": "Error al comunicar con el Excel. Revisa el Script."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
