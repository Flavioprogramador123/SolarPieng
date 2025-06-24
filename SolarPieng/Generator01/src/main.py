# ===== Procfile =====
# Arquivo: Procfile (sem extensão)
web: python src/main.py

# ===== runtime.txt =====
# Arquivo: runtime.txt
python-3.11.0

# ===== requirements.txt ATUALIZADO =====
# Arquivo: requirements.txt
blinker==1.9.0
cffi==1.17.1
charset-normalizer==3.4.2
click==8.2.1
cryptography==45.0.4
Flask==3.1.1
flask-cors==6.0.0
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
packaging==25.0
pdfminer.six==20250506
pdfplumber==0.11.7
pillow==11.2.1
pycparser==2.22
pypdfium2==4.30.1
pytesseract==0.3.13
SQLAlchemy==2.0.41
typing_extensions==4.14.0
Werkzeug==3.1.3
gunicorn==21.2.0

# ===== main.py MODIFICADO PARA HEROKU =====
# Arquivo: src/main.py
import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.api import api_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'pieng_solar_generator_secret_key_2024'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(api_bp, url_prefix='/api')

# Configuração do banco de dados (opcional para este projeto)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Configurações de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Criar diretórios necessários se não existirem
os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('logs', exist_ok=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.errorhandler(413)
def too_large(e):
    return "Arquivo muito grande. Tamanho máximo: 16MB", 413

@app.errorhandler(404)
def not_found(e):
    return "Endpoint não encontrado", 404

@app.errorhandler(500)
def internal_error(e):
    return f"Erro interno do servidor: {str(e)}", 500

@app.route('/health')
def health_check():
    """Health check para Heroku"""
    return {"status": "OK", "version": "1.0"}

if __name__ == '__main__':
    # Para desenvolvimento local
    print("🚀 Iniciando PIENG Solar Generator...")
    print("📱 Interface disponível em: http://localhost:5000")
    print("🔧 API disponível em: http://localhost:5000/api")
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Para produção no Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# ===== .gitignore =====
# Arquivo: .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
uploads/*
!uploads/.gitkeep
output/*
!output/.gitkeep
logs/*
!logs/.gitkeep
*.db
.env
.DS_Store
Thumbs.db

# ===== app.json (para Heroku) =====
# Arquivo: app.json
{
  "name": "PIENG Solar Generator",
  "description": "Sistema para geração de propostas de energia solar",
  "repository": "https://github.com/seu-usuario/pieng-solar",
  "keywords": ["python", "flask", "solar", "energy"],
  "env": {
    "SECRET_KEY": {
      "description": "Secret key for Flask sessions",
      "value": "pieng_solar_generator_secret_key_2024"
    }
  },
  "formation": {
    "web": {
      "quantity": 1,
      "size": "basic"
    }
  },
  "buildpacks": [
    {
      "url": "heroku/python"
    },
    {
      "url": "https://github.com/heroku/heroku-buildpack-apt"
    }
  ]
}