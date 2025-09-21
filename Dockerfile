# Multi-stage build para optimizar el tamaño de la imagen
FROM python:3.10-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para building
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.10-slim

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app

# Copiar dependencias instaladas desde builder
COPY --from=builder /root/.local /home/app/.local

# Copiar código fuente
COPY --chown=app:app . .

# Crear directorio para base de datos con permisos
RUN mkdir -p /app/db && chown -R app:app /app

# Cambiar a usuario no-root
USER app

# Configurar PATH para usar las dependencias locales del usuario app
ENV PATH=/home/app/.local/bin:$PATH

# Variables de entorno para producción
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENV=production
ENV PORT=8000

# Exponer puerto (dinámico para Render)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Comando de inicio optimizado para Render
# Cambiar al directorio backend antes de ejecutar para imports relativos
CMD ["sh", "-c", "cd /app/backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]