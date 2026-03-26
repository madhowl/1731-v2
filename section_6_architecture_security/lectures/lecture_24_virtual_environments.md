# Лекция 24: Виртуальные окружения

## Создание и управление виртуальными окружениями, pipenv

### Цель лекции:
- Познакомиться с концепцией виртуальных окружений
- Изучить способы создания и управления виртуальными окружениями
- Освоить использование pipenv

### План лекции:
1. Что такое виртуальное окружение
2. Создание виртуального окружения
3. Управление пакетами в виртуальном окружении
4. Использование pipenv

---

## 1. Что такое виртуальное окружение

Виртуальное окружение — это изолированное пространство для установки пакетов Python, независимое от системного Python и других проектов.

### Проблемы, которые решает:
- Конфликты версий пакетов между проектами
- Зависимости от конкретных версий пакетов
- Управление зависимостями проекта
- Повторяемость сборки проекта

### Основные преимущества:
- Изоляция зависимостей проекта
- Возможность использовать разные версии пакетов
- Простота развертывания
- Упрощение тестирования

---

## 2. Создание виртуального окружения

### Использование venv (встроенный модуль):
```bash
# Создание виртуального окружения
python -m venv myenv

# Активация (Windows)
myenv\Scripts\activate

# Активация (Linux/Mac)
source myenv/bin/activate

# Деактивация
deactivate
```

### Структура виртуального окружения:
```
myenv/
    bin/          # Linux/Mac
    Scripts/      # Windows
        python
        pip
        activate
    lib/
        site-packages/  # Установленные пакеты
```

### Пример использования:
```bash
# Создание окружения
python -m venv project_env

# Активация
source project_env/bin/activate  # Linux/Mac
# или
project_env\Scripts\activate     # Windows

# Установка пакетов
pip install requests flask

# Список установленных пакетов
pip list

# Сохранение списка зависимостей
pip freeze > requirements.txt

# Деактивация
deactivate
```

---

## 3. Управление пакетами в виртуальном окружении

### Установка пакетов:
```bash
# Установка одного пакета
pip install package_name

# Установка с указанием версии
pip install package_name==1.2.3

# Установка из requirements.txt
pip install -r requirements.txt
```

### Удаление пакетов:
```bash
# Удаление пакета
pip uninstall package_name

# Удаление всех пакетов из списка
pip uninstall -r requirements.txt -y
```

### Проверка установленных пакетов:
```bash
# Список установленных пакетов
pip list

# Информация о конкретном пакете
pip show package_name

# Проверка обновлений
pip list --outdated
```

### Сохранение и восстановление зависимостей:
```bash
# Сохранение текущих зависимостей
pip freeze > requirements.txt

# Установка зависимостей из файла
pip install -r requirements.txt
```

### Пример requirements.txt:
```
requests==2.28.1
flask==2.2.2
numpy>=1.21.0
pandas~=1.5.0
```

---

## 4. Использование pipenv

Pipenv — инструмент, который объединяет pip и virtualenv, автоматически управляет виртуальными окружениями и зависимостями.

### Установка pipenv:
```bash
pip install pipenv
```

### Основные команды:
```bash
# Установка пакетов и создание Pipfile
pipenv install requests flask

# Установка dev-зависимостей
pipenv install pytest black --dev

# Активация оболочки
pipenv shell

# Запуск команды в окружении
pipenv run python script.py

# Установка зависимостей из Pipfile
pipenv install

# Установка всех зависимостей (включая dev)
pipenv install --dev
```

### Pipfile и Pipfile.lock:
```toml
# Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
flask = "*"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.9"
```

### Преимущества pipenv:
- Автоматическое создание и управление виртуальным окружением
- Автоматическая генерация Pipfile и Pipfile.lock
- Лучшая безопасность благодаря проверке уязвимостей
- Легкая интеграция с CI/CD