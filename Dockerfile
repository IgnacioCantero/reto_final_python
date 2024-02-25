# Imágen Python
FROM python:3.9-slim

# Directorio de trabajo del contenedor
WORKDIR /app

# Copiar el contenido del directorio actual en 'app'
COPY . /app

# Instalar los paquetes necesarios especificados en 'requirements.txt'
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Puerto expuesto fuera del contenedor
EXPOSE 5000

# Definir variable de entorno
ENV FLASK_ENV=development

# Ejecutar 'app.py' cuando se inicie el contenedor
CMD ["python", "run.py"]
