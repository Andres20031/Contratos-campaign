import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from app.utils import eliminar_repetidos, get_spanish_month,calcular_periodo_texto,calcular_promedio_interacciones,generar_contexto_base,logger
# Rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                     # app/generar_plantillas
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))           # raíz del proyecto
TEMPLATE_DIR = os.path.join(ROOT_DIR, "app", "generar_plantillas", "plantillasHTML")
OUTPUT_DIR = os.path.join(ROOT_DIR, "app", "contratos_pdf", "contrato_In-kind_partnership")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ruta del ejecutable wkhtmltopdf
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # AJUSTA esto si está en otra ruta
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)


def GenerarNonPaidPdf(contrato_data, influencer_data,customer_data,grupos_cliente):
    logger.info("👍Contrato in-kind partnership")

    logger.info(grupos_cliente)
    try:
        logger.info("📝 Generando contrato in-kind partnership")

        # Preparar contexto dinámico con función reutilizable
        contexto = generar_contexto_base(contrato_data, influencer_data, customer_data,grupos_cliente)

        # Cargar plantilla HTML
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = env.get_template("nonPaid_Campaign.html")
        html_final = template.render(contexto)

        # Guardar PDF
        contract_id = contrato_data.get("Contract No", "SIN_ID")
        output_path = os.path.join(OUTPUT_DIR, f"contrato_{contract_id}.pdf")
        pdfkit.from_string(html_final, output_path, configuration=config)

        logger.info(f"✅ PDF generado: {output_path}")
        return {
            "output_pdf": output_path,
            "status": "PDF generado correctamente"
        }

    except Exception as e:
        logger.error(f"❌ Error generando PDF: {e}", exc_info=True)
        return {"error": str(e)}