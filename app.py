from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(name)
CORS(app)

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    vendedor = datos.get('Vendedor', 'Desconocido')
    cedula = datos.get('DebtorID', 'N/A')
    ref = datos.get('Reference', 'Sin Ref')
    monto = datos.get('Amount', '0')
    
    # Este es el reporte que verás en los Logs de Render
    print(f"REPORT: {vendedor} validó a CI: {cedula} | Ref: {ref} | Monto: {monto} Bs.")

    return jsonify({
        "status": "RECIBIDO",
        "mensaje": f"RC: {vendedor}, la ref {ref} ha sido registrada con éxito."
    })

if name == 'main':
    app.run(host='0.0.0.0', port=10000)

