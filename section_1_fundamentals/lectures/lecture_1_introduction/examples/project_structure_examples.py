# Примеры структуры проекта Python

"""
Этот файл содержит примеры различных структур проектов Python
для различных типов приложений.
"""

import os
import sys
from pathlib import Path

def create_basic_project_structure(project_name):
    """
    Создание базовой структуры проекта
    
    Args:
        project_name (str): Название проекта
    """
    print(f"Создание базовой структуры проекта: {project_name}")
    
    # Создание основной директории проекта
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    
    # Создание поддиректорий
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    (project_dir / "examples").mkdir(exist_ok=True)
    
    # Создание основных файлов
    files_to_create = [
        project_dir / "README.md",
        project_dir / "requirements.txt",
        project_dir / ".gitignore",
        project_dir / "setup.py",
        project_dir / "src" / "__init__.py",
        project_dir / "src" / "main.py",
        project_dir / "tests" / "__init__.py",
        project_dir / "docs" / "index.md"
    ]
    
    for file_path in files_to_create:
        file_path.touch(exist_ok=True)
    
    # Заполнение основных файлов
    readme_content = f"""# {project_name}

## Описание
Описание проекта {project_name}

## Установка
```bash
pip install -r requirements.txt
```

## Использование
```python
from {project_name} import main

if __name__ == "__main__":
    main()
```

## Авторы
Ваше имя

## Лицензия
MIT
"""
    
    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    requirements_content = """# Зависимости проекта
# Добавьте сюда зависимости вашего проекта
"""
    
    with open(project_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# VSCode
.vscode/

# PyCharm
.idea/

# Virtual environments
venv/
env/
ENV/
.venv/

# OS generated files
.DS_Store
Thumbs.db
"""
    
    with open(project_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    setup_content = f'''from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{project_name}",
    version="0.1.0",
    author="Ваше имя",
    author_email="your.email@example.com",
    description="Краткое описание проекта",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ваш_аккаунт/{project_name}",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        # Добавьте зависимости здесь
    ],
)
'''
    
    with open(project_dir / "setup.py", "w", encoding="utf-8") as f:
        f.write(setup_content)
    
    main_content = f'''"""
Основной модуль приложения {project_name}
"""

def main():
    """
    Основная функция приложения
    """
    print("Привет из приложения {project_name}!")
    
    # Добавьте основную логику приложения здесь
    pass

if __name__ == "__main__":
    main()
'''
    
    with open(project_dir / "src" / "main.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    
    print(f"Базовая структура проекта {project_name} создана")

def create_web_project_structure(project_name):
    """
    Создание структуры проекта для веб-приложения
    
    Args:
        project_name (str): Название проекта
    """
    print(f"\nСоздание структуры веб-проекта: {project_name}")
    
    # Создание основной директории
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    
    # Создание структуры веб-проекта
    (project_dir / "app").mkdir(exist_ok=True)
    (project_dir / "app" / "static").mkdir(exist_ok=True)
    (project_dir / "app" / "templates").mkdir(exist_ok=True)
    (project_dir / "app" / "routes").mkdir(exist_ok=True)
    (project_dir / "app" / "models").mkdir(exist_ok=True)
    (project_dir / "app" / "utils").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "migrations").mkdir(exist_ok=True)
    (project_dir / "config").mkdir(exist_ok=True)
    
    # Создание файлов для веб-проекта
    web_files = [
        project_dir / "app.py",
        project_dir / "requirements.txt",
        project_dir / "README.md",
        project_dir / "config" / "development.py",
        project_dir / "config" / "production.py",
        project_dir / "app" / "__init__.py",
        project_dir / "app" / "routes" / "__init__.py",
        project_dir / "app" / "models" / "__init__.py",
        project_dir / "app" / "utils" / "__init__.py",
        project_dir / "app" / "static" / "styles.css",
        project_dir / "app" / "static" / "script.js",
        project_dir / "app" / "templates" / "base.html",
        project_dir / "app" / "templates" / "index.html",
        project_dir / "tests" / "test_app.py"
    ]
    
    for file_path in web_files:
        file_path.touch(exist_ok=True)
    
    # Заполнение файла app.py для Flask-приложения
    app_content = '''from flask import Flask, render_template
from config import Config

def create_app(config_class=Config):
    """
    Создание и настройка приложения Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Регистрация маршрутов
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Регистрация моделей
    from app.models import db
    db.init_app(app)
    
    return app

# Пример основного маршрута
from app import routes
'''
    
    with open(project_dir / "app.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    
    # Заполнение базового шаблона
    base_html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ config.APP_NAME|default("Мое веб-приложение") }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <!-- Навигация -->
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <!-- Подвал -->
    </footer>
    
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
'''
    
    with open(project_dir / "app" / "templates" / "base.html", "w", encoding="utf-8") as f:
        f.write(base_html_content)
    
    print(f"Структура веб-проекта {project_name} создана")

def create_gui_project_structure(project_name):
    """
    Создание структуры проекта для GUI-приложения
    
    Args:
        project_name (str): Название проекта
    """
    print(f"\nСоздание структуры GUI-проекта: {project_name}")
    
    # Создание основной директории
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    
    # Создание структуры GUI-проекта
    (project_dir / "ui").mkdir(exist_ok=True)
    (project_dir / "ui" / "widgets").mkdir(exist_ok=True)
    (project_dir / "ui" / "windows").mkdir(exist_ok=True)
    (project_dir / "models").mkdir(exist_ok=True)
    (project_dir / "controllers").mkdir(exist_ok=True)
    (project_dir / "utils").mkdir(exist_ok=True)
    (project_dir / "resources").mkdir(exist_ok=True)
    (project_dir / "resources" / "icons").mkdir(exist_ok=True)
    (project_dir / "resources" / "images").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    
    # Создание файлов для GUI-проекта
    gui_files = [
        project_dir / "main.py",
        project_dir / "requirements.txt",
        project_dir / "README.md",
        project_dir / "app" / "__init__.py",
        project_dir / "models" / "__init__.py",
        project_dir / "controllers" / "__init__.py",
        project_dir / "utils" / "__init__.py",
        project_dir / "ui" / "__init__.py",
        project_dir / "ui" / "main_window.py",
        project_dir / "ui" / "widgets" / "__init__.py",
        project_dir / "ui" / "windows" / "__init__.py",
        project_dir / "tests" / "test_ui.py",
        project_dir / "resources" / "config.json"
    ]
    
    for file_path in gui_files:
        file_path.touch(exist_ok=True)
    
    # Заполнение файла main.py для GUI-приложения
    main_gui_content = '''import tkinter as tk
from ui.main_window import MainWindow

def main():
    """
    Основная функция GUI-приложения
    """
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''
    
    with open(project_dir / "main.py", "w", encoding="utf-8") as f:
        f.write(main_gui_content)
    
    # Заполнение примера главного окна
    main_window_content = '''import tkinter as tk
from tkinter import ttk

class MainWindow:
    """
    Главное окно приложения
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Мое GUI-приложение")
        self.root.geometry("800x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Настройка пользовательского интерфейса
        """
        # Создание основного фрейма
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Добавление элементов интерфейса
        title_label = ttk.Label(main_frame, text="Добро пожаловать!", font=("Arial", 16))
        title_label.pack(pady=20)
        
        # Кнопка для демонстрации
        demo_button = ttk.Button(main_frame, text="Демонстрационная кнопка", 
                                command=self.on_demo_click)
        demo_button.pack(pady=10)
    
    def on_demo_click(self):
        """
        Обработчик нажатия демонстрационной кнопки
        """
        print("Кнопка была нажата!")
'''
    
    with open(project_dir / "ui" / "main_window.py", "w", encoding="utf-8") as f:
        f.write(main_window_content)
    
    print(f"Структура GUI-проекта {project_name} создана")

def demonstrate_project_structures():
    """
    Демонстрация различных структур проектов
    """
    print("=== Демонстрация структур проектов ===\n")
    
    # Пример создания базовой структуры
    print("1. Создание базовой структуры проекта:")
    create_basic_project_structure("my_basic_app")
    
    # Пример создания веб-проекта
    print("\n2. Создание структуры веб-проекта:")
    create_web_project_structure("my_web_app")
    
    # Пример создания GUI-проекта
    print("\n3. Создание структуры GUI-проекта:")
    create_gui_project_structure("my_gui_app")
    
    print("\n=== Все структуры проектов созданы ===")

# Показ примера содержимого для основных файлов
def show_file_examples():
    """
    Показ примеров содержимого для основных файлов проекта
    """
    print("\n=== Примеры содержимого файлов ===")
    
    # Пример requirements.txt для веб-приложения
    web_requirements = '''# Зависимости для веб-приложения
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
requests==2.31.0
python-dotenv==1.0.0
'''
    
    print("Пример содержимого requirements.txt для веб-приложения:")
    print(web_requirements)
    
    # Пример конфигурационного файла
    config_example = '''import os

class Config:
    """
    Базовая конфигурация приложения
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки приложения
    APP_NAME = 'Мое веб-приложение'
    VERSION = '1.0.0'
    
class DevelopmentConfig(Config):
    """
    Конфигурация для разработки
    """
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """
    Конфигурация для продакшена
    """
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """
    Конфигурация для тестирования
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
'''
    
    print("Пример конфигурационного файла:")
    print(config_example)

if __name__ == "__main__":
    demonstrate_project_structures()
    show_file_examples()
