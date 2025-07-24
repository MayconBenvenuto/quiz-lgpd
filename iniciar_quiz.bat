@echo off
echo Iniciando Quiz LGPD - Universidade Belz...
echo.

cd /d "%~dp0"

if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando servidor Flask...
echo.
echo Acesse o quiz em: http://localhost:5000
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.

python app.py

pause
