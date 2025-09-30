from flask import Blueprint, request, jsonify
import torch
import json
from transformers import RobertaForSequenceClassification, RobertaTokenizer
import os
import logging
from datetime import datetime

classifier_bp = Blueprint("classifier", __name__)

# ==== Configuración ====
MODEL_PATH = os.getenv("MODEL_PATH", "./app/clasificador/modelo")
LABELS_PATH = os.path.join(MODEL_PATH, "labels.json")
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "512"))

# ==== Variables globales ====
model = None
tokenizer = None
categorias = None
model_loaded = False

def load_model():
    """Carga el modelo y tokenizer de forma segura"""
    global model, tokenizer, categorias, model_loaded
    
    try:
        if not os.path.exists(MODEL_PATH):
            logging.error(f"Modelo no encontrado en {MODEL_PATH}")
            return False
            
        if not os.path.exists(LABELS_PATH):
            logging.error(f"Archivo de etiquetas no encontrado en {LABELS_PATH}")
            return False
        
        logging.info(f"Cargando modelo desde {MODEL_PATH}...")
        
        model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH)
        tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH)
        model.eval()
        
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            categorias = json.load(f)
        
        model_loaded = True
        logging.info(f"✅ Modelo cargado exitosamente con {len(categorias)} categorías")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error cargando modelo: {e}")
        model_loaded = False
        return False

# Cargar modelo al inicializar
load_model()


# ==== Endpoints ====
@classifier_bp.route("/predict", methods=["POST"])
def predict():
    """Clasifica un texto usando el modelo RoBERTa"""
    if not model_loaded:
        return jsonify({
            "error": "Modelo no disponible",
            "details": "El modelo de clasificación no se pudo cargar"
        }), 503
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400
    
    if "text" not in data:
        return jsonify({"error": "Campo 'text' requerido"}), 400
    
    text = data["text"].strip()
    if not text:
        return jsonify({"error": "El texto no puede estar vacío"}), 400
    
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            "error": f"Texto demasiado largo. Máximo {MAX_TEXT_LENGTH} caracteres"
        }), 400
    
    try:
        # Tokenización
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=128
        )
        
        # Inference sin gradientes
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
        
        predicted_class = torch.argmax(outputs.logits, axis=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Obtener categoría predicha
        if isinstance(categorias, dict):
            categoria_predicha = categorias.get(str(predicted_class), "Desconocida")
        else:
            categoria_predicha = categorias[predicted_class] if predicted_class < len(categorias) else "Desconocida"
        
        return jsonify({
            "text": text,
            "predicted_class": predicted_class,
            "categoria": categoria_predicha,
            "confidence": round(confidence, 4),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error en predicción: {e}")
        return jsonify({"error": "Error interno en la clasificación"}), 500


@classifier_bp.route("/health", methods=["GET"])
def health_check():
    """Verifica el estado del clasificador"""
    return jsonify({
        "status": "ok" if model_loaded else "error",
        "model_loaded": model_loaded,
        "model_path": MODEL_PATH,
        "categories_count": len(categorias) if categorias else 0
    })


@classifier_bp.route("/categories", methods=["GET"])
def get_categories():
    """Obtiene las categorías disponibles"""
    if not model_loaded:
        return jsonify({"error": "Modelo no disponible"}), 503
    
    return jsonify({
        "categories": categorias,
        "count": len(categorias) if categorias else 0
    })


@classifier_bp.route("/batch-predict", methods=["POST"])
def batch_predict():
    """Clasifica múltiples textos de una vez"""
    if not model_loaded:
        return jsonify({"error": "Modelo no disponible"}), 503
    
    data = request.get_json()
    if not data or "texts" not in data:
        return jsonify({"error": "Campo 'texts' (lista) requerido"}), 400
    
    texts = data["texts"]
    if not isinstance(texts, list):
        return jsonify({"error": "'texts' debe ser una lista"}), 400
    
    if len(texts) > 50:  # Límite de batch
        return jsonify({"error": "Máximo 50 textos por batch"}), 400
    
    results = []
    
    try:
        for i, text in enumerate(texts):
            if not text or not text.strip():
                results.append({
                    "index": i,
                    "error": "Texto vacío"
                })
                continue
            
            text = text.strip()
            if len(text) > MAX_TEXT_LENGTH:
                results.append({
                    "index": i,
                    "error": f"Texto demasiado largo (máximo {MAX_TEXT_LENGTH} caracteres)"
                })
                continue
            
            # Procesar texto
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
            
            with torch.no_grad():
                outputs = model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=-1)
            
            predicted_class = torch.argmax(outputs.logits, axis=1).item()
            confidence = probabilities[0][predicted_class].item()
            
            if isinstance(categorias, dict):
                categoria_predicha = categorias.get(str(predicted_class), "Desconocida")
            else:
                categoria_predicha = categorias[predicted_class] if predicted_class < len(categorias) else "Desconocida"
            
            results.append({
                "index": i,
                "text": text,
                "predicted_class": predicted_class,
                "categoria": categoria_predicha,
                "confidence": round(confidence, 4)
            })
        
        return jsonify({
            "results": results,
            "total_processed": len(results),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error en batch prediction: {e}")
        return jsonify({"error": "Error interno en la clasificación por lotes"}), 500