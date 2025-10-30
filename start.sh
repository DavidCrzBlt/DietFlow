#Linux (Para poder ejecutarlo, primero dale permisos con el comando: chmod +x start.sh)
#!/bin/bash
echo "Iniciando DietFlow..."

# Activar el entorno virtual
source venv/bin/activate

# Iniciar el servidor web de FastAPI en segundo plano
echo "Iniciando servidor web en http://127.0.0.1:8000..."
uvicorn main:app --reload &

# Guardar el ID del proceso del servidor para poder detenerlo después
UVICORN_PID=$!

# Iniciar el planificador diario en primer plano
echo "Iniciando el planificador diario... (Presiona Ctrl+C para detener todo)"
python daily_planner.py

# Cuando el planificador se detiene (con Ctrl+C), detenemos también el servidor
echo "Deteniendo el servidor web..."
kill $UVICORN_PID
echo "DietFlow detenido."