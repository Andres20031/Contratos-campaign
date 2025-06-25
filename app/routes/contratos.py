from flask import Blueprint, request, jsonify
from app.utils.logger import logger
from app.generar_plantillas.paidCampaign import generarPaidPdf
from app.generar_plantillas.nonPaidCampaign import GenerarNonPaidPdf

bp = Blueprint("contrato", __name__)

@bp.route('/api/contrato', methods=['POST'])
def recibir_contrato():
    """
    Endpoint que recibe datos de contrato desde Seatable,
    redirige a la función correspondiente según el tipo de contrato
    y devuelve una respuesta indicando éxito o error.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se recibió información"}), 400

        contrato_data = data.get("contrato_data")
        influencer_data = data.get("influencer_data")

        if not contrato_data:
            return jsonify({"error": "Falta 'contrato_data'"}), 400

        tipo = contrato_data.get("Contract Type")  # Ahora está dentro de contrato_data

        # Aún si falta el tipo, puedes dejar pasar y tratar con un valor por defecto
        if not tipo:
            tipo = "Paid Campaign"  # o simplemente omitir validación si ya no es obligatorio

        # Lógica basada en tipo de contrato
        if tipo == "Paid Campaign":
            resultado = generarPaidPdf(contrato_data, influencer_data)
        elif tipo == "In-kind partnership":
            resultado = GenerarNonPaidPdf(contrato_data, influencer_data)
        else:
            return jsonify({"error": f"Tipo de contrato no soportado: {tipo}"}), 400

        return jsonify({"message": "✅ Contrato procesado correctamente", "data": resultado}), 200

    except Exception as e:
        logger.error("❌ Error al procesar el contrato", exc_info=True)
        return jsonify({"error": str(e)}), 500