import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# Configuración de Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def anotar_en_excel(datos):
    try:
        # 1. Cargar credenciales desde el archivo en GitHub
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # 2. Abrir la hoja usando el ID que me pasaste
        # Este ID es específico para "Registro de Pagos Rc"
        sheet = client.open_by_key("1sJ2eYiEFOYMjvhrPt-6-kIDN3qi5xmfefNzc4qEAUmQ").sheet1 
        
        # 3. Preparar la fila con los datos del formulario
        fila = [
            datos.get('Date'),
            datos.get('PaymentType'),
            datos.get('DestinyBankReference'),
            datos.get('Amount'),
            datos.get('ClientID')
        ]
        
        # 4. Insertar la fila al final
        sheet.append_row(fila)
        return True
    except Exception as e:
        print(f"Error técnico al anotar en Excel: {e}")
        return False

@app.route('/')
def home():
    return "Servidor Inversiones RC - CONEXIÓN POR ID ACTIVA", 200

@app.route('/auth', methods=['POST'])
def auth():
    # Respuesta simple para validar el formulario
    return "token_valido_rc", 200

@app.route('/webhook-bnc', methods=['POST'])
def webhook_bnc():
    datos = request.get_json()
    
    # Intentar anotar en la hoja de cálculo
    if anotar_en_excel(datos):
        return jsonify({
            "status": "success", 
            "message": f"Referencia {datos.get('DestinyBankReference')} anotada con éxito"
        }), 200
    else:
        return jsonify({
            "status": "error", 
            "message": "Error de conexión con Google Sheets. Revisa permisos del JSON."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
