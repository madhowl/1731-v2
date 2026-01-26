# Практическое занятие 45: Виртуальные окружения

## Создание и управление виртуальными окружениями, pipenv

### Цель занятия:
Научиться создавать и использовать виртуальные окружения в Python, устанавливать и управлять зависимостями с помощью pip и pipenv.

### Задачи:
1. Создать виртуальное окружение с помощью venv
2. Установить и управлять пакетами в виртуальном окружении
3. Использовать pipenv для управления зависимостями
4. Работать с файлами зависимостей

### План работы:
1. Основы виртуальных окружений
2. Создание и активация окружений
3. Управление пакетами
4. Использование pipenv
5. Практические задания

---

## 1. Основы виртуальных окружений

Виртуальное окружение (virtual environment) - это изолированное пространство для установки пакетов Python, независимое от глобальной установки Python и других проектов.

### Пример 1: Зачем нужны виртуальные окружения

```bash
# Проблема: разные проекты могут требовать разные версии одного и того же пакета
# Проект 1: requests==2.25.1
# Проект 2: requests==2.28.1

# Без виртуальных окружений:
# pip install requests==2.25.1  # Устанавливает для всей системы
# Теперь проект 2 не может использовать requests==2.28.1

# С виртуальным окружением:
# У каждого проекта свое изолированное окружение
```

### Пример 2: Основные преимущества виртуальных окружений

- Изоляция зависимостей проекта
- Возможность использования разных версий пакетов для разных проектов
- Повторяемость сборки проекта
- Упрощение развертывания
- Безопасность (ограничение влияния установленных пакетов)

---

## 2. Создание и активация окружений

### Пример 3: Создание виртуального окружения с помощью venv

```bash
# Создание виртуального окружения
python -m venv myenv

# В Windows:
myenv\Scripts\activate

# В Linux/Mac:
source myenv/bin/activate

# Проверка активации
which python  # Показывает путь к python в виртуальном окружении
pip list      # Показывает установленные пакеты в окружении
```

### Пример 4: Структура виртуального окружения

```
myenv/
├── bin/              # Linux/Mac
│   ├── python
│   ├── pip
│   └── activate
├── Scripts/          # Windows
│   ├── python.exe
│   ├── pip.exe
│   └── activate.bat
├── include/          # Заголовочные файлы
└── lib/              # Установленные пакеты
    └── python3.x/
        └── site-packages/
```

### Пример 5: Работа с виртуальным окружением

```bash
# Создание окружения с определенной версией Python
python3.9 -m venv myenv

# Активация окружения
source myenv/bin/activate  # Linux/Mac
# или
myenv\Scripts\activate     # Windows

# Проверка версии Python в окружении
python --version

# Установка пакетов в окружение
pip install requests
pip install django==3.2.0

# Список установленных пакетов
pip list

# Создание файла зависимостей
pip freeze > requirements.txt

# Установка зависимостей из файла
pip install -r requirements.txt

# Деактивация окружения
deactivate
```

---

## 3. Управление пакетами

### Пример 6: Установка пакетов

```bash
# Установка конкретного пакета
pip install requests

# Установка конкретной версии
pip install django==3.2.0

# Установка минимальной версии
pip install django>=3.2.0

# Установка максимальной версии
pip install django<4.0.0

# Установка совместимой версии (эквивалентно >=min, <next_major)
pip install django~=3.2.0  # эквивалентно >=3.2.0, ==3.2.*

# Установка из requirements файла
pip install -r requirements.txt

# Установка в editable mode (для разработки)
pip install -e .
```

### Пример 7: Управление пакетами

```bash
# Список установленных пакетов
pip list

# Информация о конкретном пакете
pip show requests

# Поиск пакетов
pip search keyword  # Устарело, используйте pypi.org

# Обновление пакета
pip install --upgrade requests

# Удаление пакета
pip uninstall requests

# Удаление всех пакетов из файла
pip uninstall -r requirements.txt -y

# Проверка обновлений
pip list --outdated

# Установка обновлений
pip install --upgrade $(pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1)
```

### Пример 8: Формат файла requirements.txt

```
# Комментарии начинаются с #
# Основные зависимости
requests==2.28.1
django>=3.2,<4.0
psycopg2-binary==2.9.3

# Зависимости для разработки
pytest>=6.0
black==22.3.0
flake8==4.0.1

# Зависимости с дополнительными спецификациями
numpy[arrays]==1.21.0
scipy[extra]==1.7.0

# Зависимости из Git репозитория
-e git+https://github.com/user/repo.git@v1.0#egg=package-name

# Зависимости из локального пути
-e ./local-package/
```

---

## 4. Использование pipenv

Pipenv - это инструмент, который объединяет pip и virtualenv, автоматически управляет виртуальными окружениями и зависимостями.

### Пример 9: Установка pipenv

```bash
# Установка pipenv
pip install pipenv

# Проверка установки
pipenv --version
```

### Пример 10: Основные команды pipenv

```bash
# Создание проекта с автоматическим созданием виртуального окружения
mkdir myproject && cd myproject
pipenv install

# Установка пакетов
pipenv install requests
pipenv install django==3.2.0

# Установка dev зависимостей
pipenv install pytest black --dev

# Активация оболочки
pipenv shell

# Запуск команды в окружении
pipenv run python script.py
pipenv run python -m pytest

# Установка зависимостей из Pipfile
pipenv install

# Установка всех зависимостей (включая dev)
pipenv install --dev

# Генерация requirements.txt из Pipfile
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# Удаление пакета
pipenv uninstall requests

# Удаление всего окружения
pipenv --rm

# Проверка уязвимостей
pipenv check

# Просмотр дерева зависимостей
pipenv graph
```

### Пример 11: Файлы Pipfile и Pipfile.lock

```toml
# Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
django = ">=3.2,<4.0"
psycopg2-binary = "~=2.9"

[dev-packages]
pytest = "*"
black = "*"
flake8 = "*"

[requires]
python_version = "3.9"

[scripts]
test = "pytest"
lint = "flake8 ."
format = "black ."
```

```json
# Pipfile.lock (генерируется автоматически)
{
    "_meta": {
        "hash": {
            "sha256": "..."
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.9"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "requests": {
            "hashes": [
                "sha256:..."
            ],
            "index": "pypi",
            "version": "==2.28.1"
        }
    },
    "develop": {
        "pytest": {
            "hashes": [
                "sha256:..."
            ],
            "index": "pypi",
            "version": "*"
        }
    }
}
```

---

## 5. Практические задания

### Задание 1: Создание виртуального окружения
Создайте виртуальное окружение с именем "myproject", активируйте его и проверьте версию Python.

### Задание 2: Установка пакетов
Установите в окружение следующие пакеты:
- requests
- flask
- numpy
- pandas
Проверьте список установленных пакетов.

### Задание 3: Файл зависимостей
Создайте файл requirements.txt с установленными пакетами, затем удалите окружение и создайте новое, установив зависимости из файла.

### Задание 4: Работа с версиями
Установите конкретные версии пакетов:
- django==3.2.13
- celery>=5.2,<6.0
- redis~=4.3.0
Проверьте, что версии установлены корректно.

### Задание 5: Pipenv
Установите pipenv, создайте новый проект, установите в него несколько пакетов, используя Pipfile, и выполните команды pipenv.

---

## 6. Дополнительные задания

### Задание 6: Управление несколькими окружениями
Создайте два разных проекта с разными зависимостями и убедитесь, что они изолированы друг от друга.

### Задание 7: Установка из Git
Установите пакет из Git-репозитория в виртуальное окружение.

### Задание 8: Virtualenv
Попробуйте использовать virtualenv вместо venv для создания виртуальных окружений.

---

## Контрольные вопросы:
1. Что такое виртуальное окружение и зачем оно нужно?
2. Как создать виртуальное окружение с помощью venv?
3. В чем разница между pip freeze и pip list?
4. Что такое Pipfile и Pipfile.lock?
5. Какие преимущества дает использование pipenv?