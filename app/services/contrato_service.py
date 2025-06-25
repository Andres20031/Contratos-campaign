from app.utils.logger import logger

def procesar_contrato(data: dict) -> dict:
    """
    Recibe los datos del contrato y los procesa.
    """

    try:
        logger.info("🔧 Procesando datos del contrato...")

        # Aquí puedes hacer cualquier limpieza o transformación
        contrato = {
            "contrato_id": data.get("Contract No"),
            "nombre": data.get("Full Name"),
            "cliente": data.get("Client"),
            "tipo_contrato": data.get("Contract Type"),
            "fecha_inicio": data.get("Start Date"),
            "fecha_fin": data.get("End Date"),
            "duracion": data.get("Duration (months)"),
            "username": data.get("Username")[0].get("display_value") if data.get("Username") else None,
            "team": data.get("Team"),
        }

        logger.info(f"📄 Datos procesados: {contrato}")

        return contrato

    except Exception as e:
        logger.error("❌ Error al procesar los datos del contrato", exc_info=True)
        raise e
