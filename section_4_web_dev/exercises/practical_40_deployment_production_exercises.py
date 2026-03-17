"""
Упражнения к практической работе 40: Деплоймент и production

Выполните упражнения по деплою и работе в продакшене.
"""

# Упражнение 1: Конфигурация для production
def exercise_production_config():
    """
    Настройте конфигурацию для production среды.
    """
    # settings.py
    import os
    
    DEBUG = False
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    
    # Безопасность
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # База данных
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': '5432',
        }
    }


# Упражнение 2: WSGI конфигурация
def exercise_wsgi_config():
    """
    Настройте WSGI для production.
    """
    # wsgi.py
    import os
    from django.core.wsgi import get_wsgi_application
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.production')
    application = get_wsgi_application()


# Упражнение 3: Gunicorn
def exercise_gunicorn():
    """
    Настройте Gunicorn для запуска Django.
    """
    # gunicorn_config.py
    bind = "127.0.0.1:8000"
    workers = 4
    worker_class = "sync"
    worker_connections = 1000
    timeout = 30
    keepalive = 2
    max_requests = 1000
    max_requests_jitter = 100
    preload_app = True
    daemon = False


# Упражнение 4: Nginx конфигурация
def exercise_nginx_config():
    """
    Настройте Nginx как reverse proxy.
    """
    # nginx.conf
    nginx_conf = """
    upstream app_server {
        server 127.0.0.1:8000 fail_timeout=0;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        location /static/ {
            alias /path/to/static/files/;
        }

        location /media/ {
            alias /path/to/media/files/;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://app_server;
        }
    }
    """


# Упражнение 5: Docker
def exercise_docker():
    """
    Создайте Dockerfile для приложения.
    """
    dockerfile_content = """
    FROM python:3.9-slim
    
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    
    COPY . .
    
    EXPOSE 8000
    CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
    """


if __name__ == "__main__":
    print("Упражнения по деплою и production")
