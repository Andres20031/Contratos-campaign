import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from app.utils.logger import logger

# Rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                     # app/generar_plantillas
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))           # raíz del proyecto
TEMPLATE_DIR = os.path.join(ROOT_DIR, "app", "generar_plantillas")
OUTPUT_DIR = os.path.join(ROOT_DIR, "app", "contratos_pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ruta del ejecutable wkhtmltopdf
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # AJUSTA esto si está en otra ruta
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# Traducción de meses
MES_TRAD = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}



def GenerarNonPaidPdf(contrato_data, influencer_data):

    logger.info("👍Contrato in kind partnership")
    fecha_inicio = datetime.strptime(contrato_data["Start Date"], "%Y-%m-%d")
    fecha_fin = datetime.strptime(contrato_data["End Date"], "%Y-%m-%d")

    try:
        logger.info("📝 Generando contrato Paid Campaign")
        logger.info(contrato_data)
        # Fecha actual
        now = datetime.now()
        dia = now.day
        mes = MES_TRAD[now.strftime("%B")]
        anio = now.year

        # Preparar contexto dinámico
        contexto = {
            # Datos del contrato (contrato_data)
            "NOMBRE_LEGAL_INFLUENCER": contrato_data.get("Full Name", ""),
            "NOMBRE_INFLUENCER": contrato_data.get("Full Name", ""),
            "DOCUMENTO": influencer_data.get("MetaId", "") if influencer_data else "",
            "DIRECCION": contrato_data.get("Direccion", "__________"),
            "NUMERO": contrato_data.get("Numero", "__________"),
            "SECTOR": contrato_data.get("Sector", "__________"),
            "EMAIL": influencer_data.get("Email", "") if influencer_data else "",
            "CIUDAD": influencer_data.get("City", "") if influencer_data else "",
            "DIA": dia,
            "MES": mes,
            "ANIO": anio,
            "NOMBRE_CLIENTE": eliminar_repetidos(contrato_data.get("Client", "")), 
            "Marca_Modelo": eliminar_repetidos(f"{contrato_data.get('Client', '')}: " + ", ".join(p["display_value"] for p in contrato_data.get("Product", []) if "display_value" in p)),
            "CAMPANA": contrato_data["Campaign"][0]["display_value"] if contrato_data.get("Campaign") else "",
            "diaEP": f"{fecha_inicio.day:02d}",
            "mesEP": MES_TRAD[fecha_inicio.strftime("%B")],
            "anioEP": fecha_inicio.year,
            "diaTP": f"{fecha_fin.day:02d}",
            "mesTP": MES_TRAD[fecha_fin.strftime("%B")],
            "anioTP": fecha_fin.year,       
              # Contenidos acordados
            "Agreed_IG_Reels": contrato_data.get("Agreed IG Reels", 0),
            "Agreed_IG_Posts": contrato_data.get("Agreed IG Posts", 0),
            "Agreed_IG_Stories": contrato_data.get("Agreed IG Stories", 0),
            "Agreed_TT_Videos": contrato_data.get("Agreed TT Videos", 0),
            # Nuevos campos desde influencer_data
            "META_ID": influencer_data.get("MetaId", "") if influencer_data else "",
            "INFLUENCER_NOMBRE": influencer_data.get("First Name", "") if influencer_data else "",
            "INFLUENCER_APELLIDO": influencer_data.get("Last Name", "") if influencer_data else "",
            "INFLUENCER_EMAIL": influencer_data.get("Email", "") if influencer_data else "",
            "INFLUENCER_CIUDAD": influencer_data.get("City", "") if influencer_data else "",
            "INFLUENCER_SITIO_WEB": influencer_data.get("Website", "") if influencer_data else "",
            "INFLUENCER_INSTAGRAM": influencer_data.get("Instagram", "") if influencer_data else "",
            "INFLUENCER_TIKTOK": influencer_data.get("TikTok", "") if influencer_data else "",
            "INFLUENCER_YOUTUBE": influencer_data.get("Youtube", "") if influencer_data else "",
            "INFLUENCER_GENERO": influencer_data.get("Gender", "") if influencer_data else "",
            "INFLUENCER_CUMPLEANOS": influencer_data.get("Birthday", "") if influencer_data else "",
            "INFLUENCER_TALLA": influencer_data.get("Tshirt Size", "") if influencer_data else "",
            "RELACION_ESTADO": influencer_data.get("Relationship Status", "") if influencer_data else "",
            "RELACION_DESCRIPCION": influencer_data.get("Relationship Description", "") if influencer_data else "",
            "RELACION_SCORE": influencer_data.get("Relationship Score", "") if influencer_data else "",
            "TRACKED": influencer_data.get("Tracked", "") if influencer_data else ""
        }

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

def eliminar_repetidos(cadena):
    """
    Elimina valores repetidos en una cadena separada por comas.
    Ejemplo: "Shark Ninja, Shark Ninja" → "Shark Ninja"
    """
    if not cadena:
        return ""
    partes = [p.strip() for p in cadena.split(",")]
    unicos = list(dict.fromkeys(partes))  # mantiene orden y elimina duplicados
    return ", ".join(unicos)