# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.1.0] - 2024-01-XX

### ✨ Agregado
- **Gunicorn** como servidor WSGI para producción
- Archivo `wsgi.py` como punto de entrada WSGI
- Archivo `gunicorn.conf.py` con configuración optimizada
- `Dockerfile.dev` separado para desarrollo
- Scripts de inicio `start.sh` (Linux/macOS) y `start.bat` (Windows)
- Archivo `.env.example` con todas las variables de entorno
- Sección completa sobre Gunicorn en README
- Variables de entorno para configuración de Gunicorn

### 🔄 Cambiado
- `Dockerfile` ahora usa Gunicorn en lugar de Flask dev server
- `docker-compose.yml` actualizado con variables de Gunicorn
- `docker-compose.dev.yml` ahora usa `Dockerfile.dev`
- `requirements.txt` incluye Gunicorn
- README actualizado con documentación completa de Gunicorn
- Health check en Docker usa `curl` en lugar de Python

### 🎯 Mejorado
- **Performance:** Gunicorn maneja múltiples workers concurrentes
- **Estabilidad:** Reciclaje automático de workers
- **Escalabilidad:** Configuración dinámica según CPU
- **Logging:** Formato detallado de logs con timestamps
- **Separación:** Desarrollo y producción claramente diferenciados

## [1.0.0] - 2024-01-XX

### ✨ Inicial
- API REST para clasificación de texto con RoBERTa
- Endpoints de predicción individual y por lotes
- Notebook de entrenamiento documentado
- Dockerización completa
- Documentación interactiva
