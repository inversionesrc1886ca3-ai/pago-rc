from flask import Flask, request, jsonify
from flask_cors import CORS

# Esta línea es la que tiene los guiones bajos correctos
app = Flask(__name__)
CORS(app)

@app.route('/verificar', methods=['POST'])
def verificar():
    datos = request.json
    # Captura el nombre que el vendedor escribió en el formulario
    nombre_usuario = datos.get('Vendedor', 'Usuario') 
    ref = datos.get('Reference', 'Sin Ref')
    cedula = datos.get('DebtorID', 'N/A')
    monto = datos.get('Amount', '0')
    
    # Este reporte se guarda en tus Logs de Render
    print(f"VALIDACIÓN RC: {nombre_usuario} verificó Ref: {ref} | CI: {cedula} | Monto: {monto}")

    return jsonify({
        "status": "RECIBIDO",
        # Aquí el sistema responde con el nombre que el usuario puso
        "mensaje": f"RC: {nombre_usuario}, la ref {ref} ha sido registrada con éxito."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

