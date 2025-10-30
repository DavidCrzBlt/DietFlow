FROM python:3.12.6

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos primero
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de nuestra app
COPY ./app /app

# Exponemos el puerto 8000 para que el mundo exterior pueda hablar con nuestra app
EXPOSE 8000

# El comando para correr la aplicación cuando el contenedor inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]