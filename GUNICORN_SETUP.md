# 🚀 Gunicorn - Configuración de Producción

## 📋 Resumen de Cambios

Se ha integrado **Gunicorn** como servidor WSGI para producción, manteniendo Flask dev server para desarrollo.

---

## ✅ Archivos Nuevos

### 1. `wsgi.py`
Punto de entrada WSGI para Gunicorn.

```python
from app import create_app
app = create_app()
```

### 2. `gunicorn.conf.py`
Configuración optimizada de Gunicorn:
- Workers dinámicos según CPU: `(2 x cores) + 1`
- Timeout: 120 segundos (para modelos ML)
- Reciclaje de workers: 1000 requests
- Logging detallado

### 3. `docker/Dockerfile.dev`
Dockerfile separado para desarrollo con Flask debug.

### 4. `start.sh` / `start.bat`
Scripts de inicio para Linux/macOS y Windows.

### 5. `.env.example`
Plantilla con todas las variables de entorno.

---

## 🔄 Archivos Modificados

### 1. `requirements.txt`
```diff
+ gunicorn>=21.2.0
```

### 2. `docker/Dockerfile`
```diff
- CMD ["python", "app.py"]
+ CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

### 3. `docker-compose.yml`
- Agregadas variables `GUNICORN_WORKERS` y `GUNICORN_TIMEOUT`
- Health check actualizado

### 4. `docker-compose.dev.yml`
- Ahora usa `Dockerfile.dev`

### 5. `README.md`
- Sección completa sobre Gunicorn
- Tabla comparativa desarrollo vs producción
- Comandos actualizados

---

## 🎯 Uso

### Desarrollo (Flask)
```bash
# Opción 1: Script
./start.sh dev          # Linux/macOS
start.bat dev           # Windows

# Opción 2: Manual
python app.py

# Opción 3: Docker
docker-compose -f docker-compose.dev.yml up
```

### Producción (Gunicorn)
```bash
# Opción 1: Script
./start.sh prod         # Linux/macOS
start.bat prod          # Windows

# Opción 2: Manual
gunicorn -c gunicorn.conf.py wsgi:app

# Opción 3: Docker
docker-compose up
```

---

## 📊 Comparación

| Característica | Desarrollo | Producción |
|----------------|------------|------------|
| Servidor | Flask dev | Gunicorn |
| Workers | 1 | 4+ |
| Debug | ✅ | ❌ |
| Hot Reload | ✅ | ❌ |
| Performance | Baja | Alta |
| Concurrencia | No | Sí |
| Estabilidad | Media | Alta |

---

## ⚙️ Configuración de Workers

### Fórmula Recomendada
```
workers = (2 x CPU_CORES) + 1
```

### Ejemplos
- **2 cores:** 5 workers
- **4 cores:** 9 workers
- **8 cores:** 17 workers

### Ajustar Manualmente
```bash
# Variable de entorno
export GUNICORN_WORKERS=8

# Línea de comandos
gunicorn --workers 8 wsgi:app

# Docker
docker-compose up -e GUNICORN_WORKERS=8
```

---

## 🔍 Monitoreo

### Ver Logs
```bash
# Docker
docker-compose logs -f classifier-api

# Local
tail -f gunicorn.log
```

### Formato de Logs
```
[timestamp] [worker_id] [log_level] message
```

Ejemplo:
```
[2024-01-15 10:30:00] [12345] [INFO] Starting gunicorn 21.2.0
[2024-01-15 10:30:01] [12346] [INFO] Booting worker with pid: 12346
```

---

## 🐛 Troubleshooting

### Problema: Workers mueren constantemente
**Causa:** Timeout muy bajo para modelos ML

**Solución:**
```bash
# Aumentar timeout
export GUNICORN_TIMEOUT=180
gunicorn --timeout 180 wsgi:app
```

### Problema: Alto uso de memoria
**Causa:** Demasiados workers

**Solución:**
```bash
# Reducir workers
export GUNICORN_WORKERS=2
gunicorn --workers 2 wsgi:app
```

### Problema: Requests lentos
**Causa:** Pocos workers

**Solución:**
```bash
# Aumentar workers
export GUNICORN_WORKERS=8
gunicorn --workers 8 wsgi:app
```

---

## 📚 Referencias

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)
- [Deploying Flask with Gunicorn](https://flask.palletsprojects.com/en/2.3.x/deploying/gunicorn/)

---

## ✅ Checklist de Migración

- [x] Instalar Gunicorn
- [x] Crear `wsgi.py`
- [x] Crear `gunicorn.conf.py`
- [x] Actualizar `Dockerfile`
- [x] Crear `Dockerfile.dev`
- [x] Actualizar `docker-compose.yml`
- [x] Actualizar `docker-compose.dev.yml`
- [x] Crear scripts de inicio
- [x] Actualizar `.env.example`
- [x] Actualizar `README.md`
- [x] Probar en desarrollo
- [x] Probar en producción
- [x] Verificar health checks
- [x] Verificar logs

---

**🎉 ¡Gunicorn configurado exitosamente!**
