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

# Expone el puerto que usará Flask
EXPOSE 5000

# # Comando para iniciar Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
