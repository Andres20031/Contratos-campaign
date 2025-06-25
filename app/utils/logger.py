import logging
import os

# Asegúrate de que exista la carpeta 'logs'
os.makedirs("logs", exist_ok=True)

# Crear el logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # ✅ Ahora acepta INFO, WARNING, ERROR, CRITICAL

# Handler para guardar en archivo
file_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)  # ✅ Cambiado para guardar también INFO

# (Opcional) Mostrar en consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # ✅ También muestra INFO en consola

# Formato de los mensajes
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Evitar múltiples handlers si ya existen
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
