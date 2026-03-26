#!/usr/bin/env python3
"""
Практическое занятие 52: Контейнеризация с Docker
Решение упражнений
"""

import os
import subprocess
from typing import Dict, List, Any, Optional


# ==============================================================================
# УПРАЖНЕНИЕ 1: Создание Dockerfile
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Создание Dockerfile")
print("=" * 60)


def create_dockerfile(backend: str = 'python') -> str:
    """Создание Dockerfile на основе языка"""
    
    if backend == 'python':
        return '''# Использование официального образа Python
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
'''
    
    elif backend == 'nodejs':
        return '''FROM node:18-alpine

WORKDIR /app

# Копирование package файлов
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование исходного кода
COPY . .

# Создание пользователя
RUN addgroup -g 1001 -S nodejs && \\
    adduser -S nodejs -u 1001

# Смена владельца
RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

CMD ["node", "server.js"]
'''
    
    elif backend == 'multi-stage':
        return '''# Многоэтапная сборка для уменьшения размера образа

# Этап 1: Сборка
FROM python:3.11-slim as builder

WORKDIR /app

# Установка зависимостей в изолированном окружении
RUN pip install --user --no-cache-dir -r requirements.txt

# Этап 2: Финальный образ
FROM python:3.11-slim

# Создание непривилегированного пользователя
RUN useradd --create-home appuser && \\
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
'''
    
    return ''


# Тестирование
print("Dockerfile для Python:")
print(create_dockerfile('python'))
print("\n" + "=" * 30)


# ==============================================================================
# УПРАЖНЕНИЕ 2: Docker Compose
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Docker Compose")
print("=" * 60)


def create_docker_compose() -> str:
    """Создание docker-compose.yml"""
    return '''version: '3.8'

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
'''


print("docker-compose.yml:")
print(create_docker_compose())


# ==============================================================================
# УПРАЖНЕНИЕ 3: Основные команды Docker
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Основные команды Docker")
print("=" * 60)


class DockerCommands:
    """Класс для демонстрации основных команд Docker"""
    
    @staticmethod
    def build_command(image_name: str, tag: str = 'latest') -> str:
        return f"docker build -t {image_name}:{tag} ."
    
    @staticmethod
    def run_command(image_name: str, port: int = 5000, detach: bool = True) -> str:
        d = '-d' if detach else ''
        return f"docker run {d} --name {image_name} -p {port}:{port} {image_name}:latest"
    
    @staticmethod
    def ps_command(all_containers: bool = False) -> str:
        a = '-a' if all_containers else ''
        return f"docker ps {a}"
    
    @staticmethod
    def logs_command(container_name: str, follow: bool = False) -> str:
        f = '-f' if follow else ''
        return f"docker logs {f} {container_name}"
    
    @staticmethod
    def stop_command(container_name: str) -> str:
        return f"docker stop {container_name}"
    
    @staticmethod
    def start_command(container_name: str) -> str:
        return f"docker start {container_name}"
    
    @staticmethod
    def rm_command(container_name: str, force: bool = False) -> str:
        f = '-f' if force else ''
        return f"docker rm {f} {container_name}"
    
    @staticmethod
    def exec_command(container_name: str, command: str = 'sh') -> str:
        return f"docker exec -it {container_name} {command}"
    
    @staticmethod
    def compose_up_command(detach: bool = True) -> str:
        d = '-d' if detach else ''
        return f"docker-compose up {d}"
    
    @staticmethod
    def compose_down_command(remove_volumes: bool = False) -> str:
        v = '-v' if remove_volumes else ''
        return f"docker-compose down {v}"


# Демонстрация команд
commands = DockerCommands()
print("Основные команды Docker:")
print(f"  Сборка образа: {commands.build_command('myapp')}")
print(f"  Запуск контейнера: {commands.run_command('myapp')}")
print(f"  Просмотр контейнеров: {commands.ps_command()}")
print(f"  Просмотр логов: {commands.logs_command('myapp')}")
print(f"  Остановка: {commands.stop_command('myapp')}")
print(f"  Запуск: {commands.start_command('myapp')}")
print(f"  Удаление: {commands.rm_command('myapp')}")
print(f"  Выполнение команды: {commands.exec_command('myapp')}")

print("\nКоманды Docker Compose:")
print(f"  Запуск: {commands.compose_up_command()}")
print(f"  Остановка: {commands.compose_down_command()}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Работа с томами
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Работа с томами")
print("=" * 60)


class VolumeManager:
    """Управление томами Docker"""
    
    @staticmethod
    def create_volume_command(volume_name: str) -> str:
        return f"docker volume create {volume_name}"
    
    @staticmethod
    def run_with_volume(container_name: str, volume_name: str, port: int = 5000) -> str:
        return f"docker run -d -v {volume_name}:/data --name {container_name} -p {port}:{port} myapp:latest"
    
    @staticmethod
    def run_with_bind_mount(host_path: str, container_path: str) -> str:
        return f"docker run -d -v {host_path}:{container_path}:ro myapp:latest"
    
    @staticmethod
    def list_volumes_command() -> str:
        return "docker volume ls"
    
    @staticmethod
    def inspect_volume_command(volume_name: str) -> str:
        return f"docker volume inspect {volume_name}"


volume_manager = VolumeManager()
print("Работа с томами:")
print(f"  Создание тома: {volume_manager.create_volume_command('mydata')}")
print(f"  Запуск с томом: {volume_manager.run_with_volume('myapp', 'mydata')}")
print(f"  Запуск с bind mount: {volume_manager.run_with_bind_mount('./data', '/app/data')}")
print(f"  Список томов: {volume_manager.list_volumes_command()}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Работа с сетями
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Работа с сетями")
print("=" * 60)


class NetworkManager:
    """Управление сетями Docker"""
    
    @staticmethod
    def create_network_command(network_name: str) -> str:
        return f"docker network create {network_name}"
    
    @staticmethod
    def run_in_network(container_name: str, network_name: str, port: int = 5000) -> str:
        return f"docker run -d --network {network_name} --name {container_name} -p {port}:{port} myapp:latest"
    
    @staticmethod
    def connect_to_network(container_name: str, network_name: str) -> str:
        return f"docker network connect {network_name} {container_name}"
    
    @staticmethod
    def list_networks_command() -> str:
        return "docker network ls"
    
    @staticmethod
    def inspect_network_command(network_name: str) -> str:
        return f"docker network inspect {network_name}"


network_manager = NetworkManager()
print("Работа с сетями:")
print(f"  Создание сети: {network_manager.create_network_command('mynetwork')}")
print(f"  Запуск в сети: {network_manager.run_in_network('app1', 'mynetwork')}")
print(f"  Подключение к сети: {network_manager.connect_to_network('app2', 'mynetwork')}")
print(f"  Список сетей: {network_manager.list_networks_command()}")


# ==============================================================================
# УПРАЖНЕНИЕ 6: Оптимизация Docker образов
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 6: Оптимизация Docker образов")
print("=" * 60)


OPTIMIZATION_TIPS = [
    "Используйте официальные минимальные образы (alpine)",
    "Используйте многоэтапную сборку (multi-stage build)",
    "Объединяйте RUN команды для уменьшения слоёв",
    "Копируйте только необходимые файлы",
    "Используйте .dockerignore для исключения ненужных файлов",
    "Не устанавливайте dev зависимости в production образе",
    "Используйте непривилегированных пользователей",
    "Используйте конкретные версии зависимостей",
    "Очищайте кэш пакетного менеджера",
    "Используйте COPY вместо ADD когда возможно"
]

print("Советы по оптимизации:")
for i, tip in enumerate(OPTIMIZATION_TIPS, 1):
    print(f"  {i}. {tip}")


# ==============================================================================
# УПРАЖНЕНИЕ 7: Healthcheck
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 7: Healthcheck")
print("=" * 60)


def create_healthcheck(backend: str = 'python') -> str:
    """Создание healthcheck инструкции"""
    
    if backend == 'python':
        return '''HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \\
  CMD curl -f http://localhost:5000/health || exit 1
'''
    elif backend == 'nodejs':
        return '''HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \\
  CMD node -e require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))
'''
    elif backend == 'curl':
        return '''HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost/health || exit 1
'''
    
    return ''


print("Healthcheck для Python:")
print(create_healthcheck('python'))


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
