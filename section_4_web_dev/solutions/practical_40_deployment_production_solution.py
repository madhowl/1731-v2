# -*- coding: utf-8 -*-
"""
Практическое занятие 40: Развёртывание и эксплуатация
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по развёртыванию веб-приложений в продакшене.

Примечание: Этот файл содержит примеры конфигурационных файлов
и скриптов для различных аспектов развёртывания.
"""

# ============================================================================
# Упражнение 1: Конфигурация для продакшена (Flask)
# ============================================================================

FLASK_PRODUCTION_CONFIG = '''
# config.py

import os

class Config:
    """Базовый класс конфигурации"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    
    # Отключаем отладку
    DEBUG = False
    TESTING = False
    
    # Настройки сессии
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    
    # Безопасные настройки
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    
    # Логирование
    LOG_LEVEL = 'WARNING'


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    WTF_CSRF_ENABLED = False


def get_config():
    """Функция для получения конфигурации"""
    env = os.environ.get('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    return config_map.get(env, DevelopmentConfig)
'''

# ============================================================================
# Упражнение 2: Конфигурация для продакшена (Django)
# ============================================================================

DJANGO_PRODUCTION_CONFIG = '''
# settings_production.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Статические и медиа файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'error.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
'''

# ============================================================================
# Упражнение 3: Gunicorn конфигурация
# ============================================================================

GUNICORN_CONFIG = '''
# gunicorn_config.py

import multiprocessing

# Количество рабочих процессов
workers = multiprocessing.cpu_count() * 2 + 1

# Тип рабочих процессов
worker_class = 'sync'  # или 'gevent', 'eventlet'

# Привязка
bind = '127.0.0.1:8000'

# Логирование
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Таймауты
timeout = 30
keepalive = 2

# Перезагрузка при изменении кода (только для разработки)
reload = False

# Максимальное количество запросов на worker
max_requests = 1000
max_requests_jitter = 50

# Рабочая директория
chdir = '/path/to/application'

# Пользователь и группа (раскомментируйте для продакшена)
# user = 'www-data'
# group = 'www-data'

# Запуск:
# gunicorn -c gunicorn_config.py app:app
'''

# ============================================================================
# Упражнение 4: Nginx конфигурация
# ============================================================================

NGINX_CONFIG = '''
# /etc/nginx/sites-available/myapp

upstream app_server {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name example.com www.example.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    # Static files
    location /static/ {
        alias /path/to/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/app/media/;
    }
    
    # Application
    location / {
        proxy_pass http://app_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
'''

# ============================================================================
# Упражнение 5: Systemd сервис
# ============================================================================

SYSTEMD_SERVICE = '''
# /etc/systemd/system/myapp.service

[Unit]
Description=My Flask Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/application
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -c /path/to/application/gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Управление сервисом:
# sudo systemctl daemon-reload
# sudo systemctl start myapp
# sudo systemctl enable myapp
# sudo systemctl status myapp
'''

# ============================================================================
# Упражнение 6: Docker конфигурация
# ============================================================================

DOCKERFILE_FLASK = '''
# Dockerfile для Flask приложения

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание пользователя
RUN useradd -m -u 1000 appuser
USER appuser

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Порт
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
'''

DOCKERFILE_DJANGO = '''
# Dockerfile для Django приложения

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Выполнение миграций
RUN python manage.py migrate --noinput

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

# Создание пользователя
RUN useradd -m -u 1000 django
USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
'''

DOCKER_COMPOSE = '''
# docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    restart: unless-stopped
    
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_files:/app/staticfiles
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_files:

# Запуск:
# docker-compose up -d
# docker-compose logs -f
# docker-compose down
'''

# ============================================================================
# Упражнение 7: GitHub Actions CI/CD
# ============================================================================

GITHUB_ACTIONS = '''
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install flake8 black
    
    - name: Lint
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check .
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: myapp:latest
        cache-from: type=registry,ref=myapp:buildcache
        cache-to: type=registry,ref=myapp:buildcache,mode=max
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/app
          docker-compose pull
          docker-compose up -d
'''

# ============================================================================
# Упражнение 8: Требования (requirements.txt)
# ============================================================================

REQUIREMENTS_TXT = '''
# requirements.txt

# Production dependencies
Flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4

# Security
Flask-Talisman==1.1.0
bcrypt==4.1.1

# Monitoring
sentry-sdk[flask]==1.38.0
prometheus-client==0.19.0

# Production
gunicorn[gevent]==21.2.0
greenlet==3.0.1
'''

# ============================================================================
# Упражнение 9: Мониторинг и безопасность
# ============================================================================

MONITORING_EXAMPLES = '''
# === Sentry для мониторинга ошибок ===

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://xxxxx@sentry.io/xxxxx",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True
)

# === Prometheus метрики ===

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

request_count = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# === Безопасность заголовков (Flask-Talisman) ===

from flask_talisman import Talisman

app = Flask(__name__)
talisman = Talisman(
    app,
    content_security_policy=None,
    force_https_permanent=True,
)

# === Логирование ===

import logging
import logging.handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Логирование в файл
file_handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)
'''

# ============================================================================
# Упражнение 10: Скрипт развёртывания
# ============================================================================

DEPLOY_SCRIPT = '''
#!/bin/bash
# deploy.sh - Скрипт развёртывания

set -e

echo "=== Начало развёртывания ==="

# Переменные
APP_DIR="/var/www/myapp"
VENV_DIR="$APP_DIR/venv"
DOMAIN="example.com"

# Обновление системы
echo "Обновление системы..."
sudo apt-get update && sudo apt-get upgrade -y

# Установка необходимых пакетов
echo "Установка пакетов..."
sudo apt-get install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git

# Клонирование репозитория
echo "Клонирование репозитория..."
cd $APP_DIR
git pull origin main

# Создание виртуального окружения
echo "Создание виртуального окружения..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Установка зависимостей
echo "Установка зависимостей..."
pip install -r requirements.txt

# Настройка базы данных
echo "Настройка базы данных..."
sudo -u postgres psql -c "CREATE DATABASE myapp;"
sudo -u postgres psql -c "CREATE USER myuser WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;"

# Применение миграций
echo "Применение миграций..."
python manage.py migrate

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Настройка Nginx
echo "Настройка Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Настройка Gunicorn
echo "Настройка Gunicorn..."
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp

echo "=== Развёртывание завершено! ==="
'''

# ============================================================================
# Вывод информации
# ============================================================================

def main():
    """Вывод информации о развёртывании"""
    print("=" * 70)
    print("Практическое занятие 40: Развёртывание и эксплуатация")
    print("=" * 70)
    print()
    print("Содержание:")
    print()
    print("1. Конфигурация для продакшена")
    print("   - Flask: config.py")
    print("   - Django: settings_production.py")
    print()
    print("2. Gunicorn конфигурация")
    print("   - gunicorn_config.py")
    print()
    print("3. Nginx конфигурация")
    print("   - nginx.conf")
    print()
    print("4. Systemd сервис")
    print("   - myapp.service")
    print()
    print("5. Docker")
    print("   - Dockerfile (Flask и Django)")
    print("   - docker-compose.yml")
    print()
    print("6. CI/CD")
    print("   - .github/workflows/deploy.yml")
    print()
    print("7. Мониторинг")
    print("   - Sentry, Prometheus")
    print()
    print("8. Скрипт развёртывания")
    print("   - deploy.sh")
    print()
    print("=" * 70)
    print("Для изучения скопируйте соответствующие файлы в ваш проект")
    print("=" * 70)


if __name__ == '__main__':
    main()
