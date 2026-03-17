# Практическое занятие 40: Развёртывание и эксплуатация

## Развёртывание веб-приложений в продакшене

### Цель занятия:
Научиться развёртывать веб-приложения на Python, настраивать production-серверы, работать с контейнерами Docker, настраивать CI/CD и мониторинг.

### Задачи:
1. Подготовить приложение к развёртыванию
2. Настроить веб-сервер (Nginx, Gunicorn)
3. Использовать Docker для контейнеризации
4. Настроить CI/CD
5. Настроить мониторинг и логирование

### План работы:
1. Подготовка к развёртыванию
2. Настройка веб-сервера
3. Docker и контейнеризация
4. CI/CD
5. Мониторинг и безопасность
6. Практические задания

---

## 1. Подготовка к развёртыванию

### Пример 1: Настройка приложения для продакшена

```python
# config.py

import os

class Config:
    """Базовый класс конфигурации"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    
    # Отключаем отладку
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    
    # Безопасные настройки
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    
    # Кэширование
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Логирование
    LOG_LEVEL = 'WARNING'

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    WTF_CSRF_ENABLED = False

# Функция для получения конфигурации
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
    }
    return config_map.get(env, DevelopmentConfig)
```

### Пример 2: Настройка Django для продакшена

```python
# settings.py

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
```

### Пример 3: Требования для продакшена (requirements.txt)

```
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
```

---

## 2. Настройка веб-сервера

### Пример 4: Gunicorn для Flask

```bash
# Установка
pip install gunicorn

# Запуск
gunicorn -w 4 -b 127.0.0.1:8000 app:app

# С конфигурационным файлом
gunicorn -c gunicorn_config.py app:app
```

```python
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

# Пользователь и группа
# user = 'www-data'
# group = 'www-data'
```

### Пример 5: Nginx конфигурация

```nginx
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
```

### Пример 6: Systemd сервис

```ini
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
```

```bash
# Управление сервисом
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp
sudo systemctl status myapp
```

---

## 3. Docker и контейнеризация

### Пример 7: Dockerfile для Flask-приложения

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
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
```

### Пример 8: Docker Compose для Flask + PostgreSQL + Redis

```yaml
# docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql@db:543://user:password2/myapp
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
```

### Пример 9: Dockerfile для Django

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
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
```

---

## 4. CI/CD

### Пример 10: GitHub Actions для Flask

```yaml
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
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
        pytest --cov=app tests/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/application
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          gunicorn --restart config/gunicorn.conf.py
          sudo systemctl restart myapp
```

### Пример 11: GitLab CI для Django

```yaml
# .gitlab-ci.yml

stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_password
    DATABASE_URL: postgresql://test_user:test_password@postgres:5432/test_db
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest --cov=.
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push myapp:$CI_COMMIT_SHA

deploy:
  stage: deploy
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y openssh-client
  script:
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "cd /app && docker-compose pull && docker-compose up -d"
  only:
    - main
```

---

## 5. Мониторинг и безопасность

### Пример 12: Мониторинг с Sentry

```python
# app.py

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,
    environment="production",
    release="myapp@1.0.0"
)

app = Flask(__name__)
```

### Пример 13: Мониторинг с Prometheus

```python
# metrics.py

from prometheus_client import Counter, Histogram, generate_lest, CONTENT_TYPE_LATEST
from flask import Response

# Счётчики запросов
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Гистограмма времени ответа
http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Метрики для приложения
app_views = Counter('app_views_total', 'Total app views')
user_logins = Counter('user_logins_total', 'Total user logins')
```

```python
# Добавление в Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Эндпоинт для метрик
@app.route('/metrics')
def metrics():
    return Response(generate_lest(), mimetype=CONTENT_TYPE_LATEST)
```

### Пример 14: Безопасность

```python
# Flask-Talisman для безопасности заголовков

from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

Talisman(
    app,
    content_security_policy=None,  # или настройте CSP
    force_https=True,
    force_https_permanent=True,
    frame_deny=True,
    strict_transport_security='max-age=31536000; includeSubDomains',
    x_content_type_options=True,
    x_xss_protection=True,
)

# Проверка безопасности пароля
from werkzeug.security import check_password_hash

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

# CSRF защита
from flask_wtf import CSRFProtect
csrf = CSRFProtect(app)
```

---

## 6. Практические задания

### Задание 1: Docker-контейнер
Создайте Dockerfile и docker-compose.yml для Flask-приложения с PostgreSQL.

### Задание 2: Nginx + Gunicorn
Настройте связку Nginx + Gunicorn для Flask-приложения.

### Задание 3: CI/CD
Настройте GitHub Actions для автоматического тестирования и деплоя.

### Задание 4: Мониторинг
Добавьте Sentry для отслеживания ошибок в приложении.

### Задание 5: SSL-сертификат
Настройте Let's Encrypt для HTTPS.

---

## Дополнительные задания

### Задание 6: Автоматическое масштабирование
Настройте auto-scaling для Docker-контейнеров.

### Задание 7: Бэкапы
Настройте автоматическое резервное копирование базы данных.

### Задание 8: Мониторинг ресурсов
Добавьте мониторинг CPU, RAM, диска с Grafana.

---

## Контрольные вопросы:
1. Чем отличается разработка от продакшена?
2. Что такое Gunicorn и зачем он нужен?
3. Как работает Nginx как обратный прокси?
4. Что такое Docker и какие преимущества он даёт?
5. Как настроить CI/CD?
6. Что такое Sentry и для чего он используется?
7. Как обеспечить безопасность веб-приложения?
8. Что такое SSL/TLS и как его настроить?
