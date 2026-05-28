# ===== BUILD STAGE =====
FROM python:3.12-slim as builder

WORKDIR /app

# Устанавливаем зависимости для компиляции
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-пакеты
RUN pip install --no-cache-dir --user -r requirements.txt

# ===== RUNTIME STAGE =====
FROM python:3.12-slim

# Создаём не-root пользователя для безопасности
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid 1000 --create-home appuser

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /root/.local /home/appuser/.local

# Добавляем .local/bin в PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Копируем приложение
COPY --chown=appuser:appgroup . .

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Создаём директорию для базы данных
RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

# Переключаемся на не-root пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]