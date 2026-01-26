# Практическое занятие 46: Настройка виртуальных окружений

## Подробное руководство по созданию и управлению виртуальными окружениями

### Цель занятия:
Освоить продвинутые техники создания и управления виртуальными окружениями в Python, включая использование различных инструментов и подходов к управлению зависимостями.

### Задачи:
1. Научиться создавать виртуальные окружения различными способами
2. Освоить управление зависимостями с использованием разных инструментов
3. Понять различия между инструментами управления окружениями
4. Научиться работать с разными версиями Python

### План работы:
1. Варианты создания виртуальных окружений
2. Управление зависимостями
3. Работа с несколькими версиями Python
4. Инструменты управления окружениями
5. Практические задания

---

## 1. Варианты создания виртуальных окружений

### Пример 1: Создание окружения с venv

```bash
# Создание окружения с указанием конкретной версии Python
python3.9 -m venv myproject_env

# Активация (Windows)
myproject_env\Scripts\activate

# Активация (Linux/Mac)
source myproject_env/bin/activate

# Проверка активации
python --version
which python  # или where python в Windows
```

### Пример 2: Создание окружения с virtualenv

```bash
# Установка virtualenv
pip install virtualenv

# Создание окружения с конкретной версии Python
virtualenv -p python3.9 myproject_env

# Или создание с указанием пути к Python
virtualenv --python=/usr/bin/python3.9 myproject_env

# Активация и деактивация аналогично venv
source myproject_env/bin/activate  # Linux/Mac
myproject_env\Scripts\activate     # Windows
```

### Пример 3: Создание окружения с conda

```bash
# Создание окружения с определенной версией Python
conda create --name myproject python=3.9

# Активация окружения
conda activate myproject

# Установка пакетов в окружение
conda install requests pandas numpy

# Установка пакетов из pip в conda окружении
pip install flask

# Деактивация
conda deactivate

# Удаление окружения
conda env remove --name myproject
```

---

## 2. Управление зависимостями

### Пример 4: Работа с requirements.txt

```bash
# Создание файла зависимостей
pip freeze > requirements.txt

# Создание файла зависимостей без вложенных зависимостей
pip list --not-required > requirements.txt

# Создание файла с конкретными версиями
pip freeze | grep -E "(package1|package2|package3)" > requirements.txt

# Установка зависимостей из файла
pip install -r requirements.txt

# Установка зависимостей без зависимостей зависимостей
pip install --no-deps -r requirements.txt

# Установка зависимостей в определенное окружение
python -m pip install -r requirements.txt
```

### Пример 5: Управление зависимостями разных типов

```bash
# requirements.txt для production
django==3.2.0
psycopg2-binary==2.9.1
gunicorn==20.1.0

# requirements-dev.txt для разработки
-r requirements.txt
pytest==6.2.4
black==21.5b2
flake8==3.9.2
django-debug-toolbar==3.2.2

# Установка production зависимостей
pip install -r requirements.txt

# Установка всех зависимостей (production + dev)
pip install -r requirements-dev.txt
```

### Пример 6: Проверка и обновление зависимостей

```bash
# Проверка устаревших пакетов
pip list --outdated

# Обновление конкретного пакета
pip install --upgrade requests

# Обновление всех пакетов
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

# Проверка конфликтов зависимостей
pip check

# Аудит безопасности пакетов
pip install safety
safety check

# Аудит с игнорированием определенных CVE
safety check --ignore=12345
```

---

## 3. Работа с несколькими версиями Python

### Пример 7: Управление версиями Python

```bash
# Проверка установленных версий Python
python --version
python3 --version
python3.8 --version
python3.9 --version
python3.10 --version

# Создание окружения с конкретной версией
python3.9 -m venv py39_env
python3.10 -m venv py310_env

# Проверка версии в активированном окружении
python --version

# Запуск скрипта с определенной версией Python
python3.9 script.py
python3.10 script.py
```

### Пример 8: pyenv для управления версиями Python

```bash
# Установка pyenv (Linux/Mac)
curl https://pyenv.run | bash

# Установка Python версии через pyenv
pyenv install 3.9.7
pyenv install 3.10.0

# Установка глобальной версии Python
pyenv global 3.9.7

# Установка локальной версии для проекта
pyenv local 3.10.0

# Список установленных версий
pyenv versions

# Запуск команды с определенной версией
pyenv exec python script.py

# Создание виртуального окружения с pyenv
pyenv virtualenv 3.9.7 myproject
pyenv activate myproject
```

---

## 4. Инструменты управления окружениями

### Пример 9: Работа с pipenv

```bash
# Установка pipenv
pip install pipenv

# Создание проекта с автоматическим окружением
mkdir myproject && cd myproject
pipenv install

# Установка пакетов
pipenv install requests flask

# Установка dev зависимостей
pipenv install pytest black --dev

# Проверка уязвимостей
pipenv check

# Просмотр дерева зависимостей
pipenv graph

# Активация оболочки
pipenv shell

# Запуск команд в окружении
pipenv run python script.py

# Установка из Pipfile
pipenv install --dev

# Генерация requirements.txt
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# Удаление окружения
pipenv --rm
```

### Пример 10: Poetry для управления зависимостями

```bash
# Установка poetry
curl -sSL https://install.python-poetry.org | python3 -

# Инициализация проекта
poetry init

# Установка зависимостей
poetry add requests flask

# Установка dev зависимостей
poetry add --group dev pytest black

# Установка всех зависимостей
poetry install

# Установка без dev зависимостей
poetry install --no-dev

# Активация оболочки
poetry shell

# Запуск команд в окружении
poetry run python script.py

# Проверка зависимостей
poetry check

# Просмотр дерева зависимостей
poetry show --tree

# Удаление пакета
poetry remove requests
```

### Пример 11: Сравнение инструментов

| Характеристика | venv | virtualenv | pipenv | poetry |
|----------------|------|------------|--------|--------|
| Управление версиями | Нет | Нет | Нет | Да |
| Блокировка зависимостей | Нет | Нет | Да (Pipfile.lock) | Да (poetry.lock) |
| Управление dev зависимостями | Нет | Нет | Да | Да |
| Активация оболочки | Ручная | Автоматическая | Автоматическая |
| Управление проектом | Нет | Нет | Ограниченное | Полное |
| Установка | Встроенный | pip install | pip install | Скрипт установки |

---

## 5. Практические задания

### Задание 1: Создание окружений разными способами
Создайте одно и то же окружение, используя:
- venv
- virtualenv
- pipenv
- poetry

Сравните структуру и особенности каждого подхода.

### Задание 2: Управление зависимостями
Создайте проект с:
- Тремя основными зависимостями
- Пятью зависимостями для разработки
- Файлами requirements.txt и requirements-dev.txt
- Pipfile и pyproject.toml

### Задание 3: Работа с версиями Python
Установите и протестируйте работу с разными версиями Python:
- Создайте окружения для Python 3.8, 3.9, 3.10
- Установите в каждое окружение пакеты с разными требованиями к версии Python
- Протестируйте совместимость

### Задание 4: Миграция проекта
Создайте простой Python-проект и продемонстрируйте его миграцию:
- Из простого venv в pipenv
- Из pipenv в poetry
- Из poetry обратно в venv с requirements.txt

### Задание 5: Безопасность и аудит
Выполните аудит безопасности для созданного окружения:
- Используйте safety для проверки уязвимостей
- Используйте pip-audit
- Обновите уязвимые пакеты

---

## 6. Дополнительные задания

### Задание 6: Docker и виртуальные окружения
Создайте Dockerfile, который использует виртуальное окружение для установки зависимостей.

### Задание 7: CI/CD и окружения
Создайте GitHub Actions workflow, который использует разные виртуальные окружения для тестирования на разных версиях Python.

### Задание 8: Управление окружениями в команде
Разработайте стратегию управления виртуальными окружениями в командной разработке.

---

## Контрольные вопросы:
1. В чем различие между venv и virtualenv?
2. Какие преимущества дает использование pipenv перед pip?
3. Как работает Poetry и в чем его особенности?
4. Почему важно использовать виртуальные окружения в проектах?
5. Как обеспечить воспроизводимость окружения в разных системах?