# Usa una imagen base de Python
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Define la variable de entorno para Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_ENV=production

# Expone el puerto que usará Flask
EXPOSE 5000

# # Comando para iniciar Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

# Comando para iniciar Gunicorn con 4 workers y bind en 0.0.0.0:5000
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
