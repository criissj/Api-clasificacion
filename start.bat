@echo off
REM Script de inicio para Windows

echo 🚀 Iniciando API de Clasificación de Texto...

SET MODE=%1
IF "%MODE%"=="" SET MODE=production

IF "%MODE%"=="dev" GOTO DEV
IF "%MODE%"=="development" GOTO DEV
IF "%MODE%"=="prod" GOTO PROD
IF "%MODE%"=="production" GOTO PROD

echo ❌ Modo no válido: %MODE%
echo Uso: start.bat [dev^|prod]
exit /b 1

:DEV
echo 📝 Modo: DESARROLLO
echo    - Flask dev server
echo    - Hot reload activado
echo    - Debug activado
echo.
python app.py
GOTO END

:PROD
echo 🏭 Modo: PRODUCCIÓN
echo    - Gunicorn WSGI server
echo    - Workers: 4
echo    - Timeout: 120s
echo.
gunicorn -c gunicorn.conf.py wsgi:app
GOTO END

:END
