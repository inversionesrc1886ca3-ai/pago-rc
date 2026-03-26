import os
import jwt
import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import threading
from functools import wraps

app = Flask(_name_)
CORS(app)

# --- CONFIGURACIÓN DINÁMICA POR ENTORNO ---
# APP_ENV debe ser 'production' o 'development' en Render
ENV_MODE = os.getenv('APP_ENV', 'production')
SHEETDB_URL = os.getenv('SHEETDB_URL') # URL única por entorno
JWT_SECRET = os.getenv('JWT_SECRET_KEY')
BNC_USER = os.getenv('BNC_USER')
BNC_PASS = os.getenv('BNC_PASS')

referencias_procesadas = set()

# --- SEGURIDAD Y PING ---
@app.route('/auth', methods=['POST'])
def auth():
    auth_data = request.json or {}
    if auth_data.get('Login') == BNC_USER and auth_data.get('Password') == BNC_PASS:
        token = jwt.encode({
            'user': BNC_USER,
            'env': ENV_MODE,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, JWT_SECRET, algorithm="HS256")
        
        response = make_response(token, 200)
        response.mimetype = "text/plain"
        return response
    return make_response(f"Error [{ENV_MODE}]: Credenciales invalidas.", 400)

@app.route('/webhook-bnc', methods=['GET', 'POST'])
def webhook_bnc():
    # PING OBLIGATORIO PARA CERTIFICACIÓN
    if request.method == 'GET':
        return make_response("OK", 200)

    # NOTIFICACIÓN REAL (POST)
    auth_header = request.headers.get('Authorization')
    try:
        token = auth_header.split(" ")[1] if auth_header and " " in auth_header else auth_header
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        datos = request.json
        threading.Thread(target=mapear_y_registrar, args=(datos,)).start()
        
        return make_response(jsonify({"status": "SUCCESS", "env": ENV_MODE}), 200)
    except Exception as e:
        return make_response(f"Error de Produccion: {str(e)}", 400)

# --- REGISTRO FINAL EN EXCEL ---
def mapear_y_registrar(datos):
    ref = datos.get('DestinyBankReference') or datos.get('OriginBankReference')
    monto = datos.get('Amount')
    tipo = datos.get('PaymentType', 'REAL')

    try:
        monto_f = float(monto)
        if not ref or monto_f <= 0 or ref in referencias_procesadas:
            return
            
        referencias_procesadas.add(ref)
        
        row_data = {
            "data": [{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Referencia": ref,
                "Monto": monto_f,
                "Tipo": tipo,
                "Ambiente": ENV_MODE.upper() # Para que veas "PRODUCTION" en tu Excel
            }]
        }
        requests.post(SHEETDB_URL, json=row_data)
    except:
        pass

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)
