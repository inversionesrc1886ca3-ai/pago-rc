import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Usuarios permitidos para el formulario
USER_AUTH = {"admin_rc": "123456"}

@app.route('/')
def home():
    return "Servidor Inversiones RC - OPERATIVO", 200

# Esta ruta valida al usuario del formulario
@app.route('/auth', methods=['POST'])
def auth():
    auth_data = request.get_json()
    login = auth_data.get("Login")
    password = auth_data.get("Password")
    
    if USER_AUTH.get(login) == password:
        return "token_valido_rc", 200
    return "No autorizado", 401

# Esta ruta recibe los pagos
@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    try:
        datos = request.get_json()
        print(f"PAGO RECIBIDO EN INVERSIONES RC: {datos}")
        
        return jsonify({
            "status": "success",
            "message": f"Referencia {datos.get('DestinyBankReference')} registrada con éxito",
            "Reference": "PROCESADO"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
