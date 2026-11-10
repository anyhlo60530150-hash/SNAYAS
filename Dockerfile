# Usamos una imagen oficial y ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema si fuera necesario (opcional)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código al contenedor
COPY . .

# Comando por defecto al iniciar el contenedor (mantiene vivo el contenedor para desarrollo)
CMD ["python", "src/main.py"]