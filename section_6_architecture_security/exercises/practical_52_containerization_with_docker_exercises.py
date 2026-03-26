"""
Упражнения к практической работе 52: Контейнеризация с Docker

Выполните упражнения по контейнеризации приложений с Docker.
"""

# Упражнение 1: Создание Dockerfile
def exercise_create_dockerfile():
    """
    Создайте Dockerfile для Python приложения.
    """
    # Определите базовый образ
    # Добавьте инструкции по установке зависимостей
    # Настройте рабочую директорию и команду запуска
    pass


# Упражнение 2: Docker Compose
def exercise_docker_compose():
    """
    Создайте docker-compose.yml для многоконтейнерного приложения.
    """
    # Определите сервисы: web, database, cache
    # Настройте переменные окружения
    # Настройте volumes для персистентности данных
    pass


# Упражнение 3: Оптимизация образов
def exercise_image_optimization():
    """
    Оптимизируйте Docker образы.
    """
    # Используйте многоэтапную сборку
    # Минимизируйте количество слоёв
    # Используйте .dockerignore
    pass


# Упражнение 4: Работа с сетями
def exercise_docker_networking():
    """
    Настройте сети между контейнерами.
    """
    # Создайте пользовательскую сеть
    # Настройте DNS между контейнерами
    # Откройте порты для внешнего доступа
    pass


# Упражнение 5: Управление данными
def exercise_docker_volumes():
    """
    Управляйте данными в Docker.
    """
    # Создайте volumes для базы данных
    # Настройте backup и restore
    pass


if __name__ == "__main__":
    print("Упражнения по контейнеризации с Docker")
    exercise_create_dockerfile()
    exercise_docker_compose()
    exercise_image_optimization()
    exercise_docker_networking()
    exercise_docker_volumes()
