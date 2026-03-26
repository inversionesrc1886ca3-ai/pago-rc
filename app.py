import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN DE CONEXIÓN A GOOGLE
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def anotar_en_excel(datos):
    try:
        # Usamos el archivo de credenciales que ya tienes en GitHub
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # BUSCAMOS TU HOJA POR SU NOMBRE EXACTO
        sheet = client.open("Registro de Pagos Rc").sheet1 
        
        # Preparamos la fila con la información que viene del formulario
        fila = [
            datos.get('Date'),
            datos.get('PaymentType'),
            datos.get('DestinyBankReference'),
            datos.get('Amount'),
            datos.get('ClientID')
        ]
        
        # Agregamos la fila al final de la hoja
        sheet.append_row(fila)
        return True
    except Exception as e:
        print(f"Error al anotar en Registro de Pagos Rc: {e}")
        return False

@app.route('/')
def home():
    return "Servidor Inversiones RC - LISTO PARA REGISTRAR", 200

@app.route('/auth', methods=['POST'])
def auth():
    # Esta ruta permite que el formulario pase la validación
    return "token_valido_rc", 200

@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    datos = request.get_json()
    
    # Intentamos guardar en "Registro de Pagos Rc"
    if anotar_en_excel(datos):
        return jsonify({
            "status": "success",
            "message": f"Referencia {datos.get('DestinyBankReference')} anotada en Excel"
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Servidor activo, pero no pudo escribir en el Excel. Verifica las credenciales."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
