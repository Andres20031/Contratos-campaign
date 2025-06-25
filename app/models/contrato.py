from flask import Blueprint, request, jsonify
from app.utils.logger import logger

# Crear Blueprint
bp = Blueprint("contrato", __name__)

@bp.route('/api/contrato', methods=['POST'])
def recibir_contrato():
    try:
        fila = request.json  # Recibir datos enviados por SeaTable

        if not fila:
            logger.warning("⚠️ No se recibió contenido en el body")
            return jsonify({"error": "No se recibió ninguna fila"}), 400

        logger.info("✅ Fila recibida desde SeaTable")
        logger.info(fila)

        # Aquí puedes hacer lo que necesites con la fila:
        # Guardar en DB, procesar datos, generar PDF, etc.

        return jsonify({"message": "Fila procesada correctamente"}), 200

    except Exception as e:
        logger.error("❌ Error procesando fila", exc_info=True)
        return jsonify({"error": str(e)}), 500
