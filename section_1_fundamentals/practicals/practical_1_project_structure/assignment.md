# Практическое занятие 1: Создание структуры проекта

## Цель занятия
Научиться создавать правильную структуру проекта Python-приложения, использовать виртуальное окружение и управлять зависимостями проекта.

## Задачи
1. Создать структуру проекта для типичного Python-приложения
2. Настроить виртуальное окружение
3. Создать и заполнить файл requirements.txt
4. Написать базовую документацию для проекта

## Ход работы

### 1. Создание структуры проекта

Создайте следующую структуру директорий и файлов:

```
my_app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── docs/
│   └── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── README.md
└── LICENSE
```

### 2. Настройка виртуального окружения

1. Создайте виртуальное окружение с именем `venv`:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
   - В Windows:
   ```bash
   venv\Scripts\activate
   ```
   - В Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. Убедитесь, что виртуальное окружение активировано (в командной строке должно появиться `(venv)`)

### 3. Создание requirements.txt

Создайте файл `requirements.txt` и добавьте следующие зависимости:

```
# Основные зависимости
requests==2.28.1
click>=8.0.0

# Зависимости для тестирования
pytest>=7.0.0
pytest-mock>=3.6.1

# Зависимости для разработки
black>=22.0.0
flake8>=4.0.0
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

### 4. Написание базовых файлов

Создайте следующие файлы:

**src/main.py**:
```python
"""
Основной модуль приложения.
"""

from src.config import APP_NAME, VERSION
from src.utils.helpers import greet_user


def main():
    """
    Основная функция приложения.
    """
    print(f"{APP_NAME} версии {VERSION}")
    name = input("Введите ваше имя: ")
    greeting = greet_user(name)
    print(greeting)


if __name__ == "__main__":
    main()
```

**src/config.py**:
```python
"""
Конфигурационный файл приложения.
"""

APP_NAME = "Мое приложение"
VERSION = "1.0.0"
DEBUG = True
```

**src/utils/helpers.py**:
```python
"""
Вспомогательные функции.
"""


def greet_user(name):
    """
    Возвращает приветствие для пользователя.
    
    Args:
        name (str): Имя пользователя
        
    Returns:
        str: Приветствие
    """
    if not name:
        return "Привет, незнакомец!"
    return f"Привет, {name}!"


def calculate_square(number):
    """
    Вычисляет квадрат числа.
    
    Args:
        number (int or float): Число
        
    Returns:
        int or float: Квадрат числа
    """
    return number ** 2
```

**tests/test_main.py**:
```python
"""
Тесты для основного модуля.
"""
import pytest
from unittest.mock import patch
from src.main import main


def test_main_runs_without_error():
    """
    Тест проверяет, что основная функция запускается без ошибок.
    """
    # Этот тест проверяет, что main() не вызывает исключений
    # при работе с mock-объектами
    pass
```

**tests/test_utils.py**:
```python
"""
Тесты для вспомогательных функций.
"""
import pytest
from src.utils.helpers import greet_user, calculate_square


def test_greet_user_with_name():
    """
    Тест приветствия пользователя с указанным именем.
    """
    result = greet_user("Иван")
    assert result == "Привет, Иван!"


def test_greet_user_without_name():
    """
    Тест приветствия пользователя без имени.
    """
    result = greet_user("")
    assert result == "Привет, незнакомец!"


def test_calculate_square_positive():
    """
    Тест вычисления квадрата положительного числа.
    """
    result = calculate_square(5)
    assert result == 25


def test_calculate_square_negative():
    """
    Тест вычисления квадрата отрицательного числа.
    """
    result = calculate_square(-3)
    assert result == 9


def test_calculate_square_zero():
    """
    Тест вычисления квадрата нуля.
    """
    result = calculate_square(0)
    assert result == 0
```

**setup.py**:
```python
"""
Файл установки пакета.
"""
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="my_app",
    version="1.0.0",
    author="Ваше имя",
    author_email="your.email@example.com",
    description="Описание вашего приложения",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_app",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
```

**README.md**:
```markdown
# Мое приложение

Это пример структуры проекта для Python-приложения.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/my_app.git
cd my_app
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Linux/Mac
# или
venv\Scripts\activate  # На Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

Запустите приложение:
```bash
python src/main.py
```

## Тестирование

Запустите тесты:
```bash
pytest
```

## Лицензия

MIT License
```

**LICENSE**:
```
MIT License

Copyright (c) 2023 Ваше имя

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 5. Настройка .gitignore

Создайте файл `.gitignore` со следующим содержимым:

```
# Byte-compiled / optimized / DLL files
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
share/python-wheels/
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
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
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
```

## Контрольные вопросы

1. Какова цель использования виртуального окружения в Python?
2. Какие файлы обычно включаются в .gitignore для Python-проекта?
3. Почему важно правильно структурировать проект?
4. Какие элементы должны быть включены в README.md?

## Дополнительное задание

1. Добавьте файл `CONTRIBUTING.md` с инструкциями для участников проекта.
2. Создайте файл `Makefile` с часто используемыми командами (запуск тестов, установка зависимостей и т.д.).
