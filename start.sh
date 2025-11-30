#!/bin/bash
# Script de inicio para la API de Clasificación

set -e

echo "🚀 Iniciando API de Clasificación de Texto..."

# Detectar modo
MODE=${1:-production}

if [ "$MODE" = "dev" ] || [ "$MODE" = "development" ]; then
    echo "📝 Modo: DESARROLLO"
    echo "   - Flask dev server"
    echo "   - Hot reload activado"
    echo "   - Debug activado"
    echo ""
    python app.py
elif [ "$MODE" = "prod" ] || [ "$MODE" = "production" ]; then
    echo "🏭 Modo: PRODUCCIÓN"
    echo "   - Gunicorn WSGI server"
    echo "   - Workers: 4"
    echo "   - Timeout: 120s"
    echo ""
    gunicorn -c gunicorn.conf.py wsgi:app
else
    echo "❌ Modo no válido: $MODE"
    echo "Uso: ./start.sh [dev|prod]"
    exit 1
fi
