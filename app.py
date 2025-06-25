from flask import Flask, request, jsonify
from utils.auth import token_required, generate_token
from utils.logger import logger

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    user = request.json.get('user')
    password = request.json.get('password')
    if user == "admin" and password == "1234":
        token = generate_token(user)
        logger.info(f"Inicio de sesión exitoso para el usuario '{user}'.")
        return jsonify({"token": token})
    logger.warning(f"Intento de inicio de sesión fallido para usuario: {user}")
    return jsonify({"message": "Credenciales inválidas"}), 401

@app.route('/contract-created', methods=['POST'])
@token_required
def syncdata():
    payload = request.get_json()
    table = payload.get("table")
    columns = payload.get("columns")
    data = payload.get("data")
    mode = payload.get("mode", "incremental")
    final_batch = payload.get("final_batch", False)  # ✅ AQUI

    logger.debug(f"Petición recibida - Tabla: {table}, Modo: {mode}, Registros: {len(data)}, Final: {final_batch}")

    if not all([table, columns, data]):
        logger.error("Payload incompleto, faltan parámetros.")
        return jsonify({"message": "Faltan parámetros"}), 400

    try:
        logger.info(f"Sincronizando tabla '{table}' en modo '{mode}'")
        sync_data(table, columns, data, mode, final_batch)  # ✅ AQUI
        logger.info("Sincronización completada con éxito.")
        return jsonify({"message": "Sincronización completada correctamente"}), 200
    except Exception as e:
        logger.exception("Error durante la ejecución de sincronización.")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Iniciando servicio Flask para Insert API")
    app.run(debug=True)
