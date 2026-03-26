# Решения для практического занятия 46: Настройка виртуальных окружений

"""
Этот файл содержит примеры и инструкции по работе с виртуальными окружениями в Python.

Для выполнения практических заданий используйте команды в терминале.
Примеры команд приведены ниже.
"""

import os
import sys
import subprocess


# =============================================================================
# Задание 1: Создание окружений разными инструментами
# =============================================================================

def create_venv_example():
    """
    Пример создания виртуального окружения с использованием venv.
    
    Команды для терминала:
    
    # Создание окружения
    python -m venv myproject_env
    
    # Активация (Windows)
    myproject_env\\Scripts\\activate
    
    # Активация (Linux/Mac)
    source myproject_env/bin/activate
    
    # Проверка
    python --version
    pip --version
    
    # Деактивация
    deactivate
    """
    print("Создание окружения venv:")
    print("python -m venv myproject_env")
    print("source myproject_env/bin/activate  # Linux/Mac")
    print("myproject_env\\Scripts\\activate  # Windows")


def create_virtualenv_example():
    """
    Пример создания виртуального окружения с использованием virtualenv.
    
    Команды для терминала:
    
    # Установка virtualenv
    pip install virtualenv
    
    # Создание окружения
    virtualenv myproject_env
    
    # Активация
    source myproject_env/bin/activate  # Linux/Mac
    myproject_env\\Scripts\\activate  # Windows
    """
    print("Создание окружения virtualenv:")
    print("pip install virtualenv")
    print("virtualenv myproject_env")


def create_pipenv_example():
    """
    Пример создания виртуального окружения с использованием pipenv.
    
    Команды для терминала:
    
    # Установка pipenv
    pip install pipenv
    
    # Создание проекта
    mkdir myproject && cd myproject
    pipenv install
    
    # Установка пакетов
    pipenv install requests flask
    
    # Активация оболочки
    pipenv shell
    
    # Запуск команд
    pipenv run python script.py
    """
    print("Создание окружения pipenv:")
    print("pip install pipenv")
    print("pipenv install")
    print("pipenv shell")


def create_poetry_example():
    """
    Пример создания виртуального окружения с использованием Poetry.
    
    Команды для терминала:
    
    # Установка poetry
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Инициализация проекта
    poetry init
    
    # Установка зависимостей
    poetry add requests flask
    
    # Установка всех зависимостей
    poetry install
    
    # Активация оболочки
    poetry shell
    
    # Запуск команд
    poetry run python script.py
    """
    print("Создание окружения Poetry:")
    print("curl -sSL https://install.python-poetry.org | python3 -")
    print("poetry init")
    print("poetry install")


# =============================================================================
# Задание 2: Управление зависимостями
# =============================================================================

def requirements_example():
    """
    Пример управления зависимостями с requirements.txt.
    
    Команды для терминала:
    
    # Создание файла зависимостей
    pip freeze > requirements.txt
    
    # Установка зависимостей
    pip install -r requirements.txt
    
    # Только основные зависимости (без зависимостей зависимостей)
    pip freeze | grep -E "(package1|package2)" > requirements.txt
    """
    print("Управление зависимостями:")
    print("pip freeze > requirements.txt")
    print("pip install -r requirements.txt")


def pipenv_dependencies_example():
    """
    Пример управления зависимостями с Pipfile.
    
    Команды для терминала:
    
    # Установка пакета
    pipenv install requests
    
    # Установка dev зависимостей
    pipenv install pytest --dev
    
    # Генерация requirements.txt
    pipenv requirements > requirements.txt
    """
    print("Зависимости в Pipenv:")
    print("pipenv install requests")
    print("pipenv install pytest --dev")


def poetry_dependencies_example():
    """
    Пример управления зависимостями с Poetry.
    
    Команды для терминала:
    
    # Добавление зависимости
    poetry add requests
    
    # Добавление dev зависимостей
    poetry add pytest --group dev
    
    # Установка всех зависимостей
    poetry install
    
    # Установка без dev
    poetry install --no-dev
    """
    print("Зависимости в Poetry:")
    print("poetry add requests")
    print("poetry add pytest --group dev")


# =============================================================================
# Задание 3: Работа с версиями Python
# =============================================================================

def python_versions_example():
    """
    Пример работы с разными версиями Python.
    
    Команды для терминала:
    
    # Проверка версий
    python --version
    python3 --version
    python3.8 --version
    python3.9 --version
    python3.10 --version
    
    # Создание окружения с конкретной версией
    python3.9 -m venv py39_env
    python3.10 -m venv py310_env
    """
    print("Работа с версиями Python:")
    print("python --version")
    print("python3.9 -m venv py39_env")


def pyenv_example():
    """
    Пример работы с pyenv для управления версиями Python.
    
    Команды для терминала:
    
    # Установка pyenv (Linux/Mac)
    curl https://pyenv.run | bash
    
    # Установка Python версии
    pyenv install 3.9.7
    pyenv install 3.10.0
    
    # Установка глобальной версии
    pyenv global 3.9.7
    
    # Установка локальной версии для проекта
    pyenv local 3.10.0
    
    # Создание виртуального окружения
    pyenv virtualenv 3.9.7 myproject
    pyenv activate myproject
    """
    print("Работа с pyenv:")
    print("pyenv install 3.9.7")
    print("pyenv global 3.9.7")


# =============================================================================
# Задание 4: Безопасность и аудит
# =============================================================================

def security_audit_example():
    """
    Пример проверки безопасности зависимостей.
    
    Команды для терминала:
    
    # Установка safety
    pip install safety
    
    # Проверка уязвимостей
    safety check
    
    # Проверка с игнорированием CVE
    safety check --ignore=12345
    
    # Установка pip-audit
    pip install pip-audit
    
    # Аудит пакетов
    pip-audit
    """
    print("Аудит безопасности:")
    print("pip install safety")
    print("safety check")
    print("pip install pip-audit")
    print("pip-audit")


# =============================================================================
# Пример скрипта для автоматизации
# =============================================================================

def create_venv_script():
    """
    Пример скрипта для автоматического создания виртуального окружения.
    """
    script = '''
import os
import sys
import subprocess
import shutil

def create_virtual_environment(env_name="venv", requirements_file=None):
    """Создает виртуальное окружение и устанавливает зависимости."""
    
    # Удаление существующего окружения
    if os.path.exists(env_name):
        print(f"Удаление существующего окружения {env_name}...")
        shutil.rmtree(env_name)
    
    # Создание нового окружения
    print(f"Создание виртуального окружения {env_name}...")
    subprocess.run([sys.executable, "-m", "venv", env_name])
    
    # Определение пути к pip
    if sys.platform == "win32":
        pip_path = os.path.join(env_name, "Scripts", "pip")
    else:
        pip_path = os.path.join(env_name, "bin", "pip")
    
    # Обновление pip
    print("Обновление pip...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"])
    
    # Установка зависимостей
    if requirements_file and os.path.exists(requirements_file):
        print(f"Установка зависимостей из {requirements_file}...")
        subprocess.run([pip_path, "install", "-r", requirements_file])
    
    print("Готово!")
    print(f"Активируйте окружение:")
    if sys.platform == "win32":
        print(f"{env_name}\\\\Scripts\\\\activate")
    else:
        print(f"source {env_name}/bin/activate")

if __name__ == "__main__":
    env_name = input("Введите имя окружения (по умолчанию venv): ") or "venv"
    requirements = input("Введите имя файла зависимостей (или Enter): ")
    create_virtual_environment(env_name, requirements if requirements else None)
'''
    return script


# =============================================================================
# Пример файлов конфигурации
# =============================================================================

def generate_requirements_txt_example():
    """Пример содержимого файла requirements.txt"""
    return """
# Требования для проекта
# Установите: pip install -r requirements.txt

# Основные зависимости
Flask==2.3.0
SQLAlchemy==2.0.0
requests==2.31.0

# Дополнительные зависимости
Pillow==10.0.0
python-dotenv==1.0.0
"""


def generate_pipfile_example():
    """Пример содержимого файла Pipfile"""
    return """
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
requests = "*"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.10"
"""


def generate_pyproject_toml_example():
    """Пример содержимого файла pyproject.toml для Poetry"""
    return """
[tool.poetry]
name = "myproject"
version = "0.1.0"
description = "Описание проекта"
authors = ["Имя автора <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
flask = "^2.3.0"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^23.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""


def generate_dockerfile_example():
    """Пример Dockerfile с виртуальным окружением"""
    return """
FROM python:3.10-slim

WORKDIR /app

# Создание виртуального окружения
RUN python -m venv /app/venv

# Активация виртуального окружения
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Запуск приложения
CMD ["python", "app.py"]
"""


# =============================================================================
# Главная функция для демонстрации
# =============================================================================

def main():
    """Демонстрация решений"""
    print("=" * 70)
    print("Решения для практического занятия 46: Настройка виртуальных окружений")
    print("=" * 70)
    print()
    
    print("Задание 1: Создание окружений разными инструментами")
    print("-" * 50)
    create_venv_example()
    print()
    create_virtualenv_example()
    print()
    create_pipenv_example()
    print()
    create_poetry_example()
    print()
    
    print("Задание 2: Управление зависимостями")
    print("-" * 50)
    requirements_example()
    print()
    pipenv_dependencies_example()
    print()
    poetry_dependencies_example()
    print()
    
    print("Задание 3: Работа с версиями Python")
    print("-" * 50)
    python_versions_example()
    print()
    pyenv_example()
    print()
    
    print("Задание 4: Безопасность и аудит")
    print("-" * 50)
    security_audit_example()
    print()
    
    print("=" * 70)
    print("Примеры файлов конфигурации:")
    print("=" * 70)
    print("requirements.txt:")
    print(generate_requirements_txt_example())
    print()
    print("Pipfile:")
    print(generate_pipfile_example())
    print()
    print("pyproject.toml:")
    print(generate_pyproject_toml_example())
    print()
    print("Dockerfile:")
    print(generate_dockerfile_example())


if __name__ == "__main__":
    main()
