from flask import Flask
from app.routes.contratos import bp as contrato_bp

app = Flask(__name__)

# Registrar las rutas
app.register_blueprint(contrato_bp)

@app.route('/')
def home():
    return 'API SeaTable funcionando ✅'

if __name__ == '__main__':
    
    app.run(debug=True)

