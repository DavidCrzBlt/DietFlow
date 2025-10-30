@echo off
echo "Iniciando DietFlow..."

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Iniciar el servidor web de FastAPI en una nueva ventana
echo "Iniciando servidor web en http://127.0.0.1:8000..."
start "DietFlow Web" cmd /c "uvicorn main:app --reload"

REM Iniciar el planificador diario en esta ventana
echo "Iniciando el planificador diario... (Cierra esta ventana para detenerlo)"
python daily_planner.py