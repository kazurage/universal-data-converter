# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Создаем пользователя для запуска приложения (безопасность)
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Открываем порт
EXPOSE 5000

# Устанавливаем переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Команда для запуска приложения
CMD ["python", "app.py"]
