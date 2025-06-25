import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}

SEATABLE = {
    'api_token': os.getenv('SEATABLE_API_TOKEN'),
    'server_url': os.getenv('SEATABLE_SERVER_URL')
}

SHAREPOINT = {
    'client_id': os.getenv('SP_CLIENT_ID'),
    'client_secret': os.getenv('SP_CLIENT_SECRET'),
    'tenant_id': os.getenv('SP_TENANT_ID')
}

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
