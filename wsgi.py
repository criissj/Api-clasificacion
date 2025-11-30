"""
WSGI Entry Point para Gunicorn
Punto de entrada para servidor de producción
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
