import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Servidor Inversiones RC - ACTIVO", 200

@app.route('/webhook-bnc', methods=['GET', 'POST'])
def webhook_bnc():
    if request.method == 'GET':
        return "OK", 200
    
    return jsonify({
        "Reference": "RECIBIDO",
        "AuthorizationCode": "000000",
        "SwAlreadySent": False
    }), 200

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
[4:11 a.m., 26/3/2026] Eduardo Meza: import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app)

@app.route('/')
def home():
    return "Servidor Inversiones RC - ACTIVO", 200

@app.route('/webhook-bnc', methods=['GET', 'POST'])
def webhook_bnc():
    if request.method == 'GET':
        return "OK", 200
    
    return jsonify({
        "Reference": "RECIBIDO",
        "AuthorizationCode": "000000",
        "SwAlreadySent": False
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
