# 🤖 API de Clasificación de Texto con RoBERTa

API REST para clasificación automática de texto usando modelos RoBERTa fine-tuned. Sistema completo que incluye entrenamiento del modelo, API de inferencia y documentación interactiva.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.30+-orange.svg)](https://huggingface.co/transformers/)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos](#️-requisitos)
- [Instalación](#-instalación)
- [Entrenamiento del Modelo](#-entrenamiento-del-modelo)
- [Uso de la API](#-uso-de-la-api)
- [Endpoints](#-endpoints)
- [Despliegue](#-despliegue)
- [Configuración](#️-configuración)
- [Ejemplos](#-ejemplos)

---

## 🚀 Características

### 🧠 Modelo de IA
- **RoBERTa Fine-tuned:** Modelo transformer especializado en español (RoBERTalex)
- **Alta Precisión:** Entrenamiento con pesos de clase balanceados
- **Métricas Detalladas:** F1-score, matriz de confusión y reportes completos
- **Inferencia Rápida:** Optimizado para producción

### ⚡ API REST
- **Clasificación Individual:** Endpoint para textos únicos
- **Procesamiento por Lotes:** Hasta 50 textos simultáneos
- **Scores de Confianza:** Probabilidades para cada predicción
- **Health Checks:** Monitoreo del estado del servicio
- **CORS Habilitado:** Listo para integraciones frontend

### 🐳 DevOps
- **Docker Ready:** Contenedorización completa
- **Docker Compose:** Configuración para desarrollo y producción
- **Usuario No-Root:** Seguridad en contenedores
- **Health Checks:** Verificación automática de disponibilidad

### 📊 Documentación
- **Interfaz Web:** Documentación interactiva en `/`
- **Jupyter Notebook:** Proceso completo de entrenamiento documentado
- **README Completo:** Guías paso a paso

---

## 📁 Arquitectura del Proyecto

```
Api-clasificacion/
├── 📂 app/                          # Aplicación Flask
│   ├── __init__.py                  # Factory de la aplicación
│   └── clasificador/                # Módulo de clasificación
│       ├── __init__.py
│       ├── endpoints.py             # Endpoints de la API
│       ├── utils.py                 # Funciones auxiliares
│       └── modelo/                  # Modelo entrenado (no en Git)
│           ├── config.json          # Configuración del modelo
│           ├── labels.json          # Mapeo de categorías
│           ├── model.safetensors    # Pesos del modelo
│           ├── tokenizer_config.json
│           ├── vocab.json
│           └── merges.txt
│
├── 📂 docker/                       # Configuración Docker
│   ├── Dockerfile                   # Imagen de producción
│   └── .dockerignore               # Archivos excluidos
│
├── 📂 static/                       # Archivos estáticos
│   ├── index.html                   # Documentación web
│   └── utem.png                     # Logo
│
├── 📂 data/                         # Datos de entrenamiento (crear)
│   └── consultas_modelo_ia.xlsx    # Dataset
│
├── 📄 app.py                        # Punto de entrada
├── 📄 requirements.txt              # Dependencias Python
├── 📄 docker-compose.yml            # Orquestación producción
├── 📄 docker-compose.dev.yml        # Orquestación desarrollo
├── 📄 MODELO_DE_CLASIFICACION.ipynb # Notebook de entrenamiento
├── 📄 .gitignore                    # Archivos ignorados
├── 📄 .env.example                  # Plantilla de variables
└── 📄 README.md                     # Este archivo
```

---

## ⚙️ Requisitos

### Software Necesario
- **Python:** 3.10 o superior
- **pip:** Gestor de paquetes de Python
- **Docker:** (Opcional) Para contenedorización
- **Docker Compose:** (Opcional) Para orquestación

### Dependencias Principales
```
flask>=2.3.0              # Framework web
flask-cors>=4.0.0         # CORS para API
torch>=2.0.0              # PyTorch para ML
transformers>=4.30.0      # Modelos Hugging Face
tokenizers>=0.13.0        # Tokenización rápida
numpy>=1.24.0             # Operaciones numéricas
scipy>=1.10.0             # Funciones científicas
```

### Hardware Recomendado
- **RAM:** Mínimo 4GB (8GB recomendado)
- **CPU:** 2+ cores
- **GPU:** (Opcional) Para entrenamiento más rápido
- **Disco:** 2GB libres para modelo y dependencias

---

## 🔧 Instalación

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Api-clasificacion.git
cd Api-clasificacion
```

### 2️⃣ Crear Entorno Virtual

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tus valores
nano .env  # o usa tu editor preferido
```

**Contenido de `.env`:**
```bash
# Flask Configuration
FLASK_SECRET_KEY=tu-clave-secreta-super-segura
FLASK_ENV=development
FLASK_DEBUG=True

# Classifier Configuration
MODEL_PATH=./app/clasificador/modelo
MAX_TEXT_LENGTH=512
```

### 5️⃣ Preparar Estructura de Carpetas

```bash
# Crear carpeta para datos
mkdir -p data

# Crear carpeta para el modelo (si no existe)
mkdir -p app/clasificador/modelo
```

---

## 🎓 Entrenamiento del Modelo

### Preparación de Datos

1. **Coloca tu dataset** en `data/consultas_modelo_ia.xlsx`
2. El archivo debe tener las columnas:
   - `cns_descripcion`: Texto a clasificar
   - `clasificaciones`: Categoría/etiqueta

### Ejecutar Notebook de Entrenamiento

```bash
# Instalar Jupyter (si no lo tienes)
pip install jupyter notebook

# Abrir notebook
jupyter notebook MODELO_DE_CLASIFICACION.ipynb
```

### Proceso de Entrenamiento

El notebook incluye:

1. **📥 Carga de Datos:** Lectura local del Excel
2. **🧹 Preprocesamiento:** Limpieza y normalización de texto
3. **✂️ División:** Train (80%), Validación (10%), Test (10%)
4. **🔤 Tokenización:** Con RoBERTalex tokenizer
5. **⚖️ Balanceo:** Cálculo de pesos de clase
6. **🏋️ Entrenamiento:** 12 épocas con early stopping
7. **📊 Evaluación:** Métricas y matriz de confusión
8. **💾 Guardado:** Modelo en `app/clasificador/modelo/`

### Resultados Esperados

Después del entrenamiento tendrás:
- ✅ Modelo entrenado en `app/clasificador/modelo/`
- ✅ Archivo `labels.json` con categorías
- ✅ Reporte de métricas (F1-score, precisión, recall)
- ✅ Matriz de confusión visualizada
- ✅ Archivo `predicciones.xlsx` con resultados de test

---

## 🚀 Uso de la API

### Iniciar Servidor Local

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Ejecutar API
python app.py
```

La API estará disponible en: **http://localhost:5000**

### Verificar Estado

```bash
curl http://localhost:5000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "service": "classifier-api"
}
```

### Documentación Interactiva

Abre en tu navegador: **http://localhost:5000**

---

## 📡 Endpoints

### 1. Clasificar Texto Individual

**Endpoint:** `POST /api/classifier/predict`

**Request:**
```json
{
  "text": "Buenos días, necesito información sobre inscripción de ramos"
}
```

**Response:**
```json
{
  "text": "Buenos días, necesito información sobre inscripción de ramos",
  "predicted_class": 1,
  "categoria": "Jefe Carrera",
  "confidence": 0.9234,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

**Códigos de Estado:**
- `200`: Clasificación exitosa
- `400`: Datos inválidos
- `503`: Modelo no disponible

---

### 2. Clasificación por Lotes

**Endpoint:** `POST /api/classifier/batch-predict`

**Request:**
```json
{
  "texts": [
    "Consulta sobre horarios",
    "Problema con mi matrícula",
    "Solicitud de certificado"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "index": 0,
      "text": "Consulta sobre horarios",
      "predicted_class": 1,
      "categoria": "Jefe Carrera",
      "confidence": 0.8756
    },
    {
      "index": 1,
      "text": "Problema con mi matrícula",
      "predicted_class": 3,
      "categoria": "SISEI",
      "confidence": 0.9123
    },
    {
      "index": 2,
      "text": "Solicitud de certificado",
      "predicted_class": 2,
      "categoria": "Otro",
      "confidence": 0.7845
    }
  ],
  "total_processed": 3,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

**Límites:**
- Máximo 50 textos por solicitud
- Máximo 512 caracteres por texto

---

### 3. Estado del Clasificador

**Endpoint:** `GET /api/classifier/health`

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_path": "./app/clasificador/modelo",
  "categories_count": 4
}
```

---

### 4. Obtener Categorías

**Endpoint:** `GET /api/classifier/categories`

**Response:**
```json
{
  "categories": {
    "0": "Docencia",
    "1": "Jefe Carrera",
    "2": "Otro",
    "3": "SISEI"
  },
  "count": 4
}
```

---

### 5. Información de la API

**Endpoint:** `GET /api`

**Response:**
```json
{
  "name": "API de Clasificación de Texto",
  "version": "1.0.0",
  "description": "API para clasificación de texto usando RoBERTa",
  "endpoints": {
    "predict": "/api/classifier/predict",
    "batch_predict": "/api/classifier/batch-predict",
    "health": "/api/classifier/health",
    "categories": "/api/classifier/categories"
  }
}
```

---

## 🐳 Despliegue

### Opción 1: Docker Compose (Recomendado)

**Producción:**
```bash
docker-compose up -d --build
```

**Desarrollo:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Ver logs:**
```bash
docker-compose logs -f classifier-api
```

**Detener:**
```bash
docker-compose down
```

---

### Opción 2: Docker Manual

**Construir imagen:**
```bash
docker build -t classifier-api:latest -f docker/Dockerfile .
```

**Ejecutar contenedor:**
```bash
docker run -d \
  --name classifier-api \
  -p 5000:5000 \
  -e FLASK_SECRET_KEY=tu-clave-secreta \
  -e MODEL_PATH=/app/app/clasificador/modelo \
  classifier-api:latest
```

---

### Opción 3: Servidor de Producción (Gunicorn)

**Instalar Gunicorn:**
```bash
pip install gunicorn
```

**Ejecutar:**
```bash
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

---

## 🛠️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `FLASK_SECRET_KEY` | Clave secreta de Flask | `classifier-api-key` |
| `FLASK_ENV` | Entorno de Flask | `development` |
| `FLASK_DEBUG` | Modo debug | `True` |
| `MODEL_PATH` | Ruta del modelo | `./app/clasificador/modelo` |
| `MAX_TEXT_LENGTH` | Longitud máxima de texto | `512` |

### Estructura del Modelo

El directorio `app/clasificador/modelo/` debe contener:

```
modelo/
├── config.json              # Configuración del modelo RoBERTa
├── labels.json              # Mapeo de clases a etiquetas
├── model.safetensors        # Pesos del modelo (formato seguro)
├── tokenizer_config.json    # Configuración del tokenizer
├── vocab.json               # Vocabulario del tokenizer
├── merges.txt               # Merges BPE del tokenizer
└── special_tokens_map.json  # Tokens especiales
```

**Formato de `labels.json`:**
```json
{
  "0": "Docencia",
  "1": "Jefe Carrera",
  "2": "Otro",
  "3": "SISEI"
}
```

---

## 💡 Ejemplos

### Python

```python
import requests

# URL de la API
API_URL = "http://localhost:5000/api/classifier"

# Clasificar un texto
def clasificar_texto(texto):
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": texto}
    )
    return response.json()

# Ejemplo de uso
resultado = clasificar_texto("Necesito ayuda con mi inscripción de ramos")
print(f"Categoría: {resultado['categoria']}")
print(f"Confianza: {resultado['confidence']:.2%}")

# Clasificación por lotes
def clasificar_lote(textos):
    response = requests.post(
        f"{API_URL}/batch-predict",
        json={"texts": textos}
    )
    return response.json()

# Ejemplo de lote
textos = [
    "Consulta sobre horarios",
    "Problema con certificado",
    "Solicitud de reunión"
]
resultados = clasificar_lote(textos)
for r in resultados['results']:
    print(f"{r['text']} -> {r['categoria']} ({r['confidence']:.2%})")
```

---

### JavaScript/Node.js

```javascript
// Clasificar texto individual
async function clasificarTexto(texto) {
    const response = await fetch('http://localhost:5000/api/classifier/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: texto })
    });
    return await response.json();
}

// Uso
clasificarTexto('Necesito información sobre mi matrícula')
    .then(resultado => {
        console.log(`Categoría: ${resultado.categoria}`);
        console.log(`Confianza: ${(resultado.confidence * 100).toFixed(2)}%`);
    });

// Clasificación por lotes
async function clasificarLote(textos) {
    const response = await fetch('http://localhost:5000/api/classifier/batch-predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texts: textos })
    });
    return await response.json();
}
```

---

### cURL

```bash
# Clasificar texto
curl -X POST http://localhost:5000/api/classifier/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Consulta sobre inscripción de asignaturas"}'

# Clasificación por lotes
curl -X POST http://localhost:5000/api/classifier/batch-predict \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Problema con mi horario",
      "Solicitud de certificado",
      "Consulta académica"
    ]
  }'

# Verificar estado
curl http://localhost:5000/api/classifier/health

# Obtener categorías
curl http://localhost:5000/api/classifier/categories
```

---

## 🧪 Testing

### Tests Manuales

```bash
# Test de clasificación
python -c "
import requests
r = requests.post(
    'http://localhost:5000/api/classifier/predict',
    json={'text': 'Necesito ayuda con mi inscripción'}
)
print(r.json())
"

# Test de health check
python -c "
import requests
r = requests.get('http://localhost:5000/api/classifier/health')
print(r.json())
"
```

### Tests Automatizados (Opcional)

```bash
# Instalar pytest
pip install pytest requests

# Crear archivo test_api.py
# Ejecutar tests
pytest tests/ -v
```

---

## 📊 Límites y Restricciones

| Límite | Valor |
|--------|-------|
| Longitud máxima por texto | 512 caracteres |
| Textos por batch | 50 máximo |
| Timeout por request | 30 segundos |
| Tamaño del modelo | ~500 MB |
| RAM requerida | 4 GB mínimo |

---

## 🔒 Seguridad

### Implementado ✅
- Validación de entrada (longitud, formato)
- Manejo seguro de errores
- CORS configurado
- Usuario no-root en Docker
- Variables de entorno para secretos
- Health checks automáticos

### Pendiente 🔄
- Rate limiting
- Autenticación JWT
- Logging avanzado
- Monitoreo con Prometheus
- SSL/TLS en producción

---

## 🐛 Troubleshooting

### Problema: Modelo no se carga

**Síntoma:** Error 503 al hacer requests

**Solución:**
```bash
# Verificar que existe el modelo
ls -la app/clasificador/modelo/

# Verificar permisos
chmod -R 755 app/clasificador/modelo/

# Verificar logs
docker-compose logs classifier-api
```

---

### Problema: Error de memoria

**Síntoma:** `RuntimeError: CUDA out of memory`

**Solución:**
```python
# En endpoints.py, reducir batch size o usar CPU
device = torch.device("cpu")  # Forzar CPU
```

---

### Problema: Puerto 5000 ocupado

**Síntoma:** `Address already in use`

**Solución:**
```bash
# Cambiar puerto en app.py
app.run(port=5001)

# O matar proceso
lsof -ti:5000 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :5000   # Windows
```

---

## 📚 Recursos Adicionales

- **Documentación Flask:** https://flask.palletsprojects.com/
- **Transformers Hugging Face:** https://huggingface.co/docs/transformers/
- **RoBERTalex:** https://huggingface.co/PlanTL-GOB-ES/RoBERTalex
- **Docker Docs:** https://docs.docker.com/

---

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.

---

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [GitHub](https://github.com/tu-usuario)

---

## 🙏 Agradecimientos

- Modelo base: [RoBERTalex](https://huggingface.co/PlanTL-GOB-ES/RoBERTalex) por PlanTL-GOB-ES
- Framework: [Hugging Face Transformers](https://huggingface.co/transformers/)
- Universidad Tecnológica Metropolitana (UTEM)

---

## 📞 Soporte

- 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/Api-clasificacion/issues)
- 📧 **Email:** tu-email@ejemplo.com
- 📖 **Docs:** http://localhost:5000 (cuando la API está ejecutándose)

---

<div align="center">

**🚀 ¡API lista para clasificar texto con IA! 🤖**

Hecho con ❤️ para la comunidad UTEM

</div>
