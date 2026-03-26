# Практическое занятие 52: Контейнеризация с Docker

## Основы Docker, создание образов, работа с контейнерами, Docker Compose

### Цель занятия:
Изучить основы контейнеризации с Docker, научиться создавать Docker образы, управлять контейнерами и использовать Docker Compose для оркестрации.

### Задачи:
1. Понять основные концепции Docker
2. Научиться создавать Dockerfile
3. Освоить основные команды Docker
4. Изучить Docker Compose для многоконтейнерных приложений

### План работы:
1. Введение в контейнеризацию
2. Основные концепции Docker
3. Создание Dockerfile
4. Управление контейнерами
5. Docker Compose
6. Практические задания

---

## 1. Введение в контейнеризацию

Контейнеризация - это метод виртуализации, который позволяет упаковывать приложения со всеми их зависимостями в изолированные контейнеры.

### Преимущества контейнеризации:

1. **Изоляция** - приложения работают в изолированных средах
2. **Портативность** - контейнер работает одинаково в любой среде
3. **Эффективность** - меньше накладных расходов, чем у виртуальных машин
4. **Масштабируемость** - лёгкое создание и удаление контейнеров
5. **Воспроизводимость** - гарантированное воспроизведение окружения

### Docker vs Виртуальные машины:

| Docker | Виртуальные машины |
|--------|-------------------|
| Общая ОС хоста | Отдельная ОС для каждой ВМ |
| Легковесные (MB) | Тяжёлые (GB) |
| Быстрый запуск | Медленный запуск |
| Изоляция на уровне процессов | Изоляция на уровне оборудования |

---

## 2. Основные концепции Docker

### Основные термины:

- **Image (образ)** - шаблон для создания контейнера
- **Container (контейнер)** - запущенный экземпляр образа
- **Dockerfile** - файл с инструкциями для создания образа
- **Registry** - хранилище образов (Docker Hub, GitHub Container Registry)
- **Volume** - способ сохранения данных вне контейнера
- **Network** - виртуальная сеть для коммуникации контейнеров

### Пример 1: Базовая структура проекта

```
myapp/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Пример 2: Простой Flask приложение

```python
# app/main.py
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Docker!',
        'environment': os.environ.get('ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

```text
# app/requirements.txt
Flask==3.0.0
gunicorn==21.2.0
```

---

## 3. Создание Dockerfile

### Пример 3: Dockerfile для Flask приложения

```dockerfile
# Использование официального образа Python
FROM python:3.11-slim

# Установка метаданных
LABEL maintainer="developer@example.com"
LABEL version="1.0"
LABEL description="Flask application for Docker training"

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Переменные окружения
ENV PORT=5000
ENV ENVIRONMENT=production

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]
```

### Пример 4: Оптимизированный Dockerfile

```dockerfile
# Многоэтапная сборка для уменьшения размера образа

# Этап 1: Сборка
FROM python:3.11-slim as builder

WORKDIR /app

# Установка зависимостей в изолированном окружении
RUN pip install --user --no-cache-dir -r requirements.txt

# Этап 2: Финальный образ
FROM python:3.11-slim

# Создание непривилегированного пользователя
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /home/appuser

WORKDIR /app

# Копирование только зависимостей из этапа сборки
COPY --from=builder /root/.local /home/appuser/.local

# Копирование исходного кода
COPY --chown=appuser:appuser . .

# Переключение на пользователя
USER appuser

# Добавление локальных бинарных пакетов в PATH
ENV PATH=/home/appuser/.local/bin:$PATH

ENV PORT=5000
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
```

### Пример 5: Dockerfile для Node.js приложения

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Копирование package файлов
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование исходного кода
COPY . .

# Создание пользователя
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Смена владельца
RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## 4. Управление контейнерами

### Пример 6: Основные команды Docker

```bash
# Сборка образа
docker build -t myapp:latest .

# Запуск контейнера в фоновом режиме
docker run -d --name myapp -p 5000:5000 myapp:latest

# Просмотр работающих контейнеров
docker ps

# Просмотр всех контейнеров
docker ps -a

# Просмотр логов контейнера
docker logs myapp
docker logs -f myapp  # следование за логами

# Остановка/запуск контейнера
docker stop myapp
docker start myapp

# Удаление контейнера
docker rm myapp

# Просмотр образов
docker images

# Удаление образа
docker rmi myapp:latest

# Запуск команды внутри контейнера
docker exec -it myapp sh

# Просмотр использования ресурсов
docker stats myapp

# Просмотр информации о контейнере
docker inspect myapp
```

### Пример 7: Работа с томами (volumes)

```bash
# Монтирование тома для сохранения данных
docker run -d \
  --name myapp \
  -p 5000:5000 \
  -v /path/on/host:/path/in/container \
  myapp:latest

# Именованные тома
docker volume create mydata
docker run -d -v mydata:/data myapp:latest

# Просмотр томов
docker volume ls

# Монтирование только для чтения
docker run -v /path:/path:ro myapp:latest
```

### Пример 8: Работа с сетями

```bash
# Создание сети
docker network create mynetwork

# Запуск контейнера в сети
docker run -d --network mynetwork --name app1 myapp:latest

# Подключение контейнера к сети
docker network connect mynetwork app2

# Просмотр сетей
docker network ls

# Просмотр информации о сети
docker network inspect mynetwork
```

---

## 5. Docker Compose

### Пример 9: docker-compose.yml для Flask приложения с БД

```yaml
version: '3.8'

services:
  # Flask приложение
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db
      - redis
    networks:
      - frontend
      - backend
    volumes:
      - ./app:/app
    restart: unless-stopped

  # PostgreSQL база данных
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped

  # Redis кэш
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped

  # Nginx прокси
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - frontend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### Пример 10: Расширенный docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - BUILD_VERSION=1.0.0
    image: myapp:${BUILD_VERSION:-latest}
    container_name: myapp
    environment:
      - NODE_ENV=${NODE_ENV:-production}
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${DB_USER:-user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-password}
      - POSTGRES_DB=${DB_NAME:-myapp}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-user}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD:-secret}
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  app-data:
```

### Пример 11: Команды Docker Compose

```bash
# Запуск всех сервисов
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Пересборка образов
docker-compose up --build

# Остановка всех сервисов
docker-compose down

# Остановка с удалением томов
docker-compose down -v

# Просмотр логов
docker-compose logs -f

# Просмотр статуса сервисов
docker-compose ps

# Масштабирование сервиса
docker-compose up -d --scale app=3

# Выполнение команды в сервисе
docker-compose exec app sh

# Просмотр использования ресурсов
docker-compose top
```

---

## 6. Практические задания

### Задание 1: Создание Dockerfile

Создайте Dockerfile для простого Python веб-приложения:
- Используйте официальный образ Python
- Добавьте все необходимые зависимости
- Настройте запуск с использованием Gunicorn
- Оптимизируйте размер образа

### Задание 2: Docker Compose стек

Создайте Docker Compose файл для следующего стека:
- Flask приложение
- PostgreSQL база данных
- Redis кэш
- Nginx обратный прокси

### Задание 3: Многоэтапная сборка

Создайте Dockerfile с многоэтапной сборкой для Node.js приложения:
- Этап сборки: установка зависимостей и сборка
- Этап production: только необходимые файлы
- Используйте непривилегированного пользователя

### Задание 4: Мониторинг контейнеров

Настройте мониторинг для Docker контейнеров:
- Добавьте healthcheck в docker-compose.yml
- Настройте сбор метрик
- Создайте дашборд для отображения состояния

### Задание 5: CI/CD с Docker

Настройте автоматическую сборку и деплой:
- Автоматическая сборка образа при пуше в git
- Тегирование образов
- Деплей на сервер с использованием Docker Compose

---

## Контрольные вопросы:

1. В чём преимущества контейнеризации перед виртуализацией?
2. Что такое Dockerfile и какие инструкции в нём используются?
3. Зачем нужен Docker Compose?
4. Как обеспечить сохранность данных в контейнерах?
5. Что такое многоэтапная сборка и зачем она нужна?

---

## Дополнительные материалы:

- Docker Documentation: https://docs.docker.com/
- Docker Compose Documentation: https://docs.docker.com/compose/
- Best practices for writing Dockerfiles: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
