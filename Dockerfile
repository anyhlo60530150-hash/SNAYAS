# Usamos una imagen oficial y ligera de Python
FROM python:3.12

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. Instalamos git Y las librerías gráficas necesarias para PySide6 (libGL y glib)
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código al contenedor
COPY . .

# Comando por defecto al iniciar el contenedor (mantiene vivo el contenedor para desarrollo)
CMD ["python", "app/src/main.py"]