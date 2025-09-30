from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from app.clasificador.endpoints import classifier_bp
import os

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "classifier-api-key")
    
    # Habilitar CORS para la API
    CORS(app)
    
    # Registrar blueprint del clasificador
    app.register_blueprint(classifier_bp, url_prefix='/api/classifier')
    
    @app.route('/')
    def home():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/api')
    def api_info():
        return jsonify({
            "name": "API de Clasificación de Texto",
            "version": "1.0.0",
            "description": "API para clasificación de texto usando RoBERTa",
            "endpoints": {
                "predict": "/api/classifier/predict",
                "batch_predict": "/api/classifier/batch-predict",
                "health": "/api/classifier/health",
                "categories": "/api/classifier/categories"
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({"status": "ok", "service": "classifier-api"})
    
    return app
