import os
import jwt
import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
from datetime import datetime as dt

app = Flask(__name__)
CORS(app)

ENV_MODE = os.getenv('APP_ENV', 'production')
SHEETDB_URL = os.getenv('SHEETDB_URL') 
JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'rc_secret_2026')
BNC_USER = os.getenv('BNC_USER', 'admin_rc')
BNC_PASS = os.getenv('BNC_PASS', '123456')

@app.route('/auth', methods=['POST'])
def auth():
    auth_data = request.json or {}
    if auth_data.get('Login') == BNC_USER and auth_data.get('Password') == BNC_PASS:
        token = jwt.encode({
            'user': BNC_USER,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, JWT_SECRET, algorithm="HS256")
        if isinstance(token, bytes): token = token.decode('utf-8')
        return make_response(token, 200)
    return make_response("Credenciales inválidas", 400)

@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    auth_header = request.headers.get('Authorization')
    try:
        token = auth_header.split(" ")[1] if auth_header and " " in auth_header else auth_header
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        datos = request.json
        ref = str(datos.get('DestinyBankReference'))

        # --- BLOQUEO DE DUPLICADOS REAL ---
        # Buscamos en SheetDB si la referencia ya existe
        check_res = requests.get(f"{SHEETDB_URL}/search?Referencia={ref}")
        existentes = check_res.json()

        if existentes:
            return jsonify({"status": "ERROR", "message": "Esta referencia ya fue registrada anteriormente."}), 409

        # Si no existe, procedemos a registrar
        row_data = {
            "data": [{
                "Fecha": dt.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Referencia": ref,
                "Monto": float(datos.get('Amount')),
                "Tipo": datos.get('PaymentType'),
                "Cliente": datos.get('ClientID'),
                "Ambiente": ENV_MODE.upper()
            }]
        }
        
        reg_res = requests.post(SHEETDB_URL, json=row_data)
        
        if reg_res.status_code == 201:
            return jsonify({"status": "SUCCESS", "message": "Pago registrado con éxito"}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Error al conectar con la base de datos"}), 500

    except Exception as e:
        return make_response(jsonify({"status": "ERROR", "message": str(e)}), 400)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

  
