@echo off
cd /d "%~dp0"
echo Verificando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo No se pudieron instalar las dependencias.
    echo Revisa tu conexion a internet o que Python este instalado.
    echo El archivo TXT puede funcionar sin pandas.
    echo.
)
echo Iniciando el programa...
python main.py
pause
