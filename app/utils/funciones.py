from dateutil.relativedelta import relativedelta
from datetime import datetime

def eliminar_repetidos(cadena):
    """
    Elimina valores repetidos en una cadena separada por comas.
    Ejemplo: "Shark Ninja, Shark Ninja" → "Shark Ninja"
    """
    if not cadena:
        return ""  # Si la cadena está vacía o es None, retorna una cadena vacía

    # Divide la cadena por comas y elimina espacios extra alrededor de cada parte
    partes = [p.strip() for p in cadena.split(",")]

    # Usa un diccionario para eliminar duplicados y mantener el orden original
    unicos = list(dict.fromkeys(partes))

    # Une los elementos únicos nuevamente en una cadena separada por comas
    return ", ".join(unicos)


def get_spanish_month(month_english):
    """
    Traduce el nombre de un mes en inglés al español.
    Si el mes no está en el diccionario, devuelve el original.
    """
    MES_TRAD = {
        "January": "Enero", "February": "Febrero", "March": "Marzo",
        "April": "Abril", "May": "Mayo", "June": "Junio",
        "July": "Julio", "August": "Agosto", "September": "Septiembre",
        "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }

    # Retorna la traducción del mes si existe, o el original si no está en el diccionario
    return MES_TRAD.get(month_english, month_english)




def calcular_periodo_texto(fecha_inicio, fecha_fin):
    """
    Calcula el período entre dos fechas y lo devuelve en texto legible.
    Ej: "5 meses", "1 año y 2 meses"
    """
    diff = relativedelta(fecha_fin, fecha_inicio)
    partes = []

    if diff.years:
        partes.append(f"{diff.years} año{'s' if diff.years > 1 else ''}")
    if diff.months:
        partes.append(f"{diff.months} mes{'es' if diff.months > 1 else ''}")

    # Si no hay diferencia en meses ni años, se indica 1 mes mínimo
    if not partes:
        partes.append("menos de 1 mes")

    return " y ".join(partes)

def calcular_promedio_interacciones(ig_likes, ig_comments):
    """
    Calcula el promedio de interacciones (likes + comentarios).
    """
    if ig_likes is None:
        ig_likes = 0
    if ig_comments is None:
        ig_comments = 0

    total_interacciones = ig_likes + ig_comments
    promedio = total_interacciones // 2  # Redondeo entero

    return promedio

def extraer_username_instagram(url):
    if isinstance(url, str) and "instagram.com" in url:
        return url.rstrip("/").split("/")[-1]
    return "__________"

def extraer_username_TikTok(url):
    if isinstance(url, str) and "://" in url:
        username = url.rstrip("/").split("/")[-1]
        return username.lstrip("@")
    return "__________"


def calcular_total_interacciones(data):
    """Suma IG Likes, IG Comments, TT Likes y TT Comments."""
    return sum([
        data.get("IG Likes", 0) or 0,
        data.get("IG Comments", 0) or 0,
        data.get("TT likes", 0) or 0,
        data.get("TT Comments", 0) or 0
    ])

def calcular_total_impresiones(data):
    """Suma IG Views y TT Views."""
    return sum([
        data.get("IG Views", 0) or 0,
        data.get("TT Views", 0) or 0
    ])

def generar_contenido_por_periodo(fecha_inicio, fecha_fin, contrato_data):
    meses = []
    actual_inicio = fecha_inicio

    total_ig_stories = contrato_data.get("Agreed IG Stories", 0)
    total_ig_posts = contrato_data.get("Agreed IG Posts", 0)
    total_ig_reels = contrato_data.get("Agreed IG Reels",0)
    total_tt_videos = contrato_data.get("Agreed TT Videos", 0)

    # Calcular todos los cortes mensuales desde la fecha exacta
    fechas_rangos = []
    while actual_inicio < fecha_fin:
        proximo_inicio = actual_inicio + relativedelta(months=1)
        actual_fin = proximo_inicio - relativedelta(days=1)
        if actual_fin > fecha_fin:
            actual_fin = fecha_fin
        fechas_rangos.append((actual_inicio, actual_fin))
        actual_inicio = proximo_inicio

    cantidad_meses = len(fechas_rangos)

    def dividir(valor):
        return round(valor / cantidad_meses) if cantidad_meses > 0 else 0

    for inicio, fin in fechas_rangos:
        meses.append({
            "periodo": f"{inicio.strftime('%d/%m/%Y')} - {fin.strftime('%d/%m/%Y')}",
            "ig_stories": dividir(total_ig_stories),
            "ig_posts": dividir(total_ig_posts),
            "ig_tv": 0,
            "ig_reels": dividir(total_ig_reels),
            "tt_videos": dividir(total_tt_videos),
        })

    return meses

def generar_contexto_base(contrato_data, influencer_data, customer_data, grupos_cliente):
    fecha_inicio = datetime.strptime(contrato_data["Start Date"], "%Y-%m-%d")
    fecha_fin = datetime.strptime(contrato_data["End Date"], "%Y-%m-%d")

    now = datetime.now()
    dia = now.day
    mes = get_spanish_month(now.strftime("%B"))
    anio = now.year

    contexto = {
        "NOMBRE_LEGAL_INFLUENCER": contrato_data.get("Full Name", ""),
        "CIUDAD": influencer_data.get("City") or "__________" if influencer_data else "__________",
        "EMAIL": influencer_data.get("Email") or "__________" if influencer_data else "__________",
        "DOCUMENTO": influencer_data.get("Tax ID") or "__________" if influencer_data else "__________",
        "DIRECCION": influencer_data.get("Address") or "__________" if influencer_data else "__________",
        "NOMBRE_CLIENTE": eliminar_repetidos(contrato_data.get("Client", "__________")),
        "periodo": calcular_periodo_texto(fecha_inicio, fecha_fin),
        "diaEP": f"{fecha_inicio.day:02d}",
        "mesEP": get_spanish_month(fecha_inicio.strftime("%B")),
        "anioEP": fecha_inicio.year,
        "diaTP": f"{fecha_fin.day:02d}",
        "mesTP": get_spanish_month(fecha_fin.strftime("%B")),
        "anioTP": fecha_fin.year,
        "Agreed_IG_Reels": contrato_data.get("Agreed IG Reels", 0),
        "Agreed_IG_Posts": contrato_data.get("Agreed IG Posts", 0),
        "Agreed_IG_Stories": contrato_data.get("Agreed IG Stories", 0),
        "Agreed_TT_Videos": contrato_data.get("Agreed TT Videos", 0),
        "promedio_ig_In": calcular_promedio_interacciones(contrato_data.get("IG Likes", 0), contrato_data.get("IG Comments", 0)),
        "promedio_tt_In": calcular_promedio_interacciones(contrato_data.get("TT likes", 0), contrato_data.get("TT Comments", 0)),
        "promedio_ig_Im": contrato_data.get("IG Views", 0),
        "promedio_tt_Im": contrato_data.get("TT Views", 0),
        "engagement_ig": contrato_data.get("Total IG Engagement", 0),
        "engagement_tt": contrato_data.get("Total TT Engagement", 0),
        "event": contrato_data.get("Event Assistance", 0),
        "industria": customer_data.get("Industry"),
        "Marca_Modelo": eliminar_repetidos(f"{contrato_data.get('Client', '')}: " + ", ".join(p["display_value"] for p in contrato_data.get("Product", []) if "display_value" in p)),
        "NOMBRE_INFLUENCER": contrato_data.get("Full Name", ""),
        "NUMERO": contrato_data.get("Numero", "__________"),
        "SECTOR": contrato_data.get("Sector", "__________"),
        "DIA": dia,
        "MES": mes,
        "ANIO": anio,
        "CAMPANA": contrato_data["Campaign"][0]["display_value"] if contrato_data.get("Campaign") else "__________",
        "User_ig": extraer_username_instagram(influencer_data.get("Instagram", "")),
        "User_tt": extraer_username_TikTok(influencer_data.get("Tik Tok", "")),
        "Vl_compensacion": contrato_data.get("Talent Fee", "__________"),
        "device_cost": contrato_data.get("Device Cost", "__________"),
        "total_interacciones": calcular_total_interacciones(contrato_data),
        "total_impresiones": calcular_total_impresiones(contrato_data),
        "categorias": ", ".join(grupos_cliente),
        "meses_contenido": generar_contenido_por_periodo(fecha_inicio, fecha_fin, contrato_data)
    }

    return contexto
