import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Esto permite que tu HTML hable con Render

@app.route('/')
def home():
    return "Servidor Inversiones RC - OPERATIVO", 200

# Esta ruta recibe los datos de tu formulario
@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    try:
        datos = request.get_json()
        
        # Imprimimos en la pantalla negra de Render para ver que llegaron
        print(f"PAGO RECIBIDO: {datos}")
        
        # Aquí es donde el programa 'HACE ALGO'
        # Por ahora, le confirmamos al HTML que llegó bien
        return jsonify({
            "status": "success",
            "message": f"Pago {datos.get('DestinyBankReference')} registrado con éxito en Inversiones RC",
            "Reference": "PROCESADO"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
