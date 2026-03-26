from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    # Captura el nombre que viene desde el formulario
    nombre_usuario = datos.get('Vendedor', 'Usuario') 
    ref = datos.get('Reference', 'Sin Ref')
    cedula = datos.get('DebtorID', 'N/A')
    monto = datos.get('Amount', '0')
    
    # Este reporte se guarda en tus Logs de Render
    print(f"VALIDACIÓN: {nombre_usuario} verificó Ref: {ref} | CI: {cedula} | Monto: {monto}")

    return jsonify({
        "status": "RECIBIDO",
        # Aquí es donde le responde con SU nombre
        "mensaje": f"RC: {nombre_usuario}, la ref {ref} ha sido registrada con éxito."
    })

if name == 'main':
    app.run(host='0.0.0.0', port=10000)
