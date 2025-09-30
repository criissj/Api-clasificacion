# 🤖 API de Clasificación de Texto

API REST para clasificación de texto usando modelos RoBERTa fine-tuned. Proporciona endpoints para clasificar textos individuales o por lotes con alta precisión y métricas de confianza.

---

## 🚀 Características

- **🧠 Clasificación con RoBERTa:** Modelo transformer fine-tuned para alta precisión
- **📊 Métricas de Confianza:** Scores de confianza para cada predicción
- **🔄 Procesamiento por Lotes:** Hasta 50 textos por solicitud
- **⚡ API REST:** Endpoints simples y eficientes
- **🐳 Docker Ready:** Contenedorización completa
- **📈 Health Checks:** Monitoreo del estado del modelo
- **🔒 Validación Robusta:** Manejo de errores y validación de entrada

---

## 📁 Estructura del Proyecto

```
api_consultas/
├── app/
│   ├── __init__.py              # Factory Flask
│   └── clasificador/
│       ├── __init__.py
│       ├── endpoints.py         # Endpoints de la API
│       ├── utils.py             # Utilidades
│       └── modelo/              # Modelo RoBERTa
│           ├── config.json
│           ├── labels.json
│           ├── model.safetensors
│           └── ...
├── static/
│   └── index.html               # Documentación web
├── docker/
│   ├── Dockerfile
│   └── .dockerignore
├── app.py                       # Punto de entrada
├── requirements.txt             # Dependencias
├── .env.example                 # Variables de entorno
├── docker-compose.yml           # Producción
├── docker-compose.dev.yml       # Desarrollo
└── README.md
```

---

## ⚙️ Requisitos

- **Python 3.10+**
- **PyTorch 2.0+**
- **Transformers 4.30+**
- **Flask 2.3+**
- **Docker y Docker Compose** (opcional)

---

## 🔐 Configuración

Crea el archivo `.env`:

```bash
# Flask Configuration
FLASK_SECRET_KEY=tu-clave-secreta
FLASK_ENV=development
FLASK_DEBUG=True

# Classifier Configuration
MODEL_PATH=./app/clasificador/modelo
MAX_TEXT_LENGTH=512
```

---

## 🧪 Instalación Local

```bash
# Clonar repositorio
git clone <tu-repositorio>
cd api_consultas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables
cp .env.example .env

# Ejecutar API
python app.py
```

La API estará disponible en: **http://localhost:5000**

---

## 🐳 Uso con Docker

### Producción:
```bash
docker-compose up --build
```

### Desarrollo:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

---

## 📡 Endpoints de la API

### 🔍 Clasificar Texto Individual
```http
POST /api/classifier/predict
Content-Type: application/json

{
  "text": "Tu texto a clasificar aquí"
}
```

**Respuesta:**
```json
{
  "text": "Tu texto a clasificar aquí",
  "predicted_class": 0,
  "categoria": "Categoria_Ejemplo",
  "confidence": 0.8542,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 📊 Clasificación por Lotes
```http
POST /api/classifier/batch-predict
Content-Type: application/json

{
  "texts": ["Texto 1", "Texto 2", "Texto 3"]
}
```

**Respuesta:**
```json
{
  "results": [
    {
      "index": 0,
      "text": "Texto 1",
      "predicted_class": 0,
      "categoria": "Categoria_A",
      "confidence": 0.9123
    }
  ],
  "total_processed": 3,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 🏥 Estado del Clasificador
```http
GET /api/classifier/health
```

### 📋 Categorías Disponibles
```http
GET /api/classifier/categories
```

### 🔍 Estado General
```http
GET /health
```

---

## 💡 Ejemplos de Uso

### cURL
```bash
# Clasificar texto individual
curl -X POST http://localhost:5000/api/classifier/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Este es un texto de ejemplo"}'

# Verificar estado
curl http://localhost:5000/api/classifier/health
```

### Python
```python
import requests

# Clasificar texto
response = requests.post(
    'http://localhost:5000/api/classifier/predict',
    json={'text': 'Tu texto aquí'}
)
result = response.json()
print(f"Categoría: {result['categoria']}")
print(f"Confianza: {result['confidence']}")
```

### JavaScript
```javascript
// Clasificar texto
fetch('/api/classifier/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: 'Tu texto aquí'})
})
.then(response => response.json())
.then(data => {
    console.log('Categoría:', data.categoria);
    console.log('Confianza:', data.confidence);
});
```

---

## 🔧 Configuración del Modelo

### Estructura del Modelo
El modelo debe estar en `./app/clasificador/modelo/` con:
- `config.json` - Configuración del modelo
- `labels.json` - Mapeo de clases a etiquetas
- `model.safetensors` - Pesos del modelo
- `tokenizer_config.json` - Configuración del tokenizer
- `vocab.json` - Vocabulario
- `merges.txt` - Merges del tokenizer

### Formato de labels.json
```json
{
  "0": "Categoria_A",
  "1": "Categoria_B",
  "2": "Categoria_C"
}
```

---

## 📊 Límites y Restricciones

- **Longitud máxima por texto:** 512 caracteres
- **Batch máximo:** 50 textos por solicitud
- **Timeout:** 30 segundos por solicitud
- **Rate limiting:** No implementado (pendiente)

---

## 🚀 Despliegue en Producción

### Variables de Entorno Requeridas:
```bash
FLASK_SECRET_KEY=tu-clave-super-secreta
MODEL_PATH=/app/app/clasificador/modelo
MAX_TEXT_LENGTH=512
FLASK_ENV=production
```

### Plataformas Recomendadas:
- **Railway:** `railway up`
- **Render:** Conectar repositorio
- **DigitalOcean App Platform**
- **AWS ECS/Fargate**
- **Google Cloud Run**

---

## 🔒 Seguridad

- ✅ **Validación de entrada:** Longitud y formato
- ✅ **Manejo de errores:** Respuestas seguras
- ✅ **CORS habilitado:** Para uso desde frontend
- ✅ **Usuario no-root:** En contenedor Docker
- 🔄 **Rate limiting:** Pendiente implementación
- 🔄 **Autenticación:** Pendiente implementación

---

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest requests

# Ejecutar tests
pytest tests/

# Test manual de endpoints
python -c "
import requests
r = requests.post('http://localhost:5000/api/classifier/predict', 
                 json={'text': 'texto de prueba'})
print(r.json())
"
```

---

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.

---

## 📞 Soporte

- 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/api-clasificacion/issues)
- 📧 **Email:** soporte@tu-dominio.com
- 📖 **Docs:** Disponible en `/` cuando la API está ejecutándose

---

**¡API lista para clasificar! 🚀**