# Python GUI Tutorials

Учебный проект по созданию графических пользовательских интерфейсов на Python с использованием Tkinter и PyQt6.

## Содержание

### Практические занятия по Tkinter

- [practical_17_tkinter_app_creation_solution.py](practical_17_tkinter_app_creation_solution.py) - Создание базового окна
- [practical_18_tkinter_ui_elements_solution.py](practical_18_tkinter_ui_elements_solution.py) - UI элементы
- [practical_19_tkinter_event_handling_solution.py](practical_19_tkinter_event_handling_solution.py) - Обработка событий
- [practical_20_tkinter_advanced_elements_solution.py](practical_20_tkinter_advanced_elements_solution.py) - Продвинутые элементы
- [practical_21_tkinter_validation_solution.py](practical_21_tkinter_validation_solution.py) - Валидация ввода
- [practical_22_tkinter_layout_management_solution.py](practical_22_tkinter_layout_management_solution.py) - Управление компоновкой
- [practical_23_tkinter_custom_widgets_solution.py](practical_23_tkinter_custom_widgets_solution.py) - Собственные виджеты
- [practical_24_tkinter_canvas_graphics_solution.py](practical_24_tkinter_canvas_graphics_solution.py) - Графика на Canvas
- [practical_25_tkinter_mvc_pattern_solution.py](practical_25_tkinter_mvc_pattern_solution.py) - Паттерн MVC
- [practical_26_tkinter_multithreading_solution.py](practical_26_tkinter_multithreading_solution.py) - Многопоточность

### Практические занятия по PyQt6

- [practical_27_pyqt_basic_applications_solution.py](practical_27_pyqt_basic_applications_solution.py) - Базовые приложения
- [practical_28_pyqt_signals_slots_solution.py](practical_28_pyqt_signals_slots_solution.py) - Сигналы и слоты
- [practical_29_pyqt_custom_dialogs_solution.py](practical_29_pyqt_custom_dialogs_solution.py) - Собственные диалоги
- [practical_30_pyqt_model_view_solution.py](practical_30_pyqt_model_view_solution.py) - Паттерн Model-View

## Требования

- Python 3.12+
- PyQt6

## Установка

> **Примечание:** Рекомендуется использовать виртуальное окружение для изоляции зависимостей проекта. Для удобной работы рекомендуется использовать менеджер пакетов [uv](https://github.com/astral-sh/uv).

### О менеджере пакетов uv

**uv** — это ультрабыстрый менеджер пакетов для Python, написанный на Rust и разработанный командой Astral. Он объединяет функции управления виртуальными окружениями (как venv) и установки пакетов (как pip) в одном инструменте.

#### Преимущества uv

| Характеристика | uv | pip | poetry |
|----------------|-----|-----|--------|
| Скорость установки | В 10-100 раз быстрее | Базовая | Средняя |
| Управление окружениями | Встроено | Требует venv | Встроено |
|Lock-файлы | uv.lock | — | poetry.lock |
| Совместимость с pyproject.toml | Полная | Частичная | Полная |
| Требует Python | 3.8+ | Любой | Любой |

**Основные возможности:**
- Автоматическое разрешение зависимостей с учётом конфликтов версий
- Работа с `requirements.txt`, `pyproject.toml` и `setup.py`
- Поддержка workspace для монорепозиториев
- Кэширование загрузок для ускорения повторных установок
- Установка глобальных инструментов (аналог `pipx`)

#### Установка uv

```bash
# macOS / Linux (curl)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Через pip
pip install uv

# Через brew
brew install uv
```

#### Основные команды uv

```bash
# Создание виртуального окружения
uv venv                    # Создаёт .venv в текущей директории
uv venv .venv             # Явное указание имени
uv venv --python 3.12    # Указание версии Python

# Активация виртуального окружения
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\Activate     # Windows PowerShell

# Установка зависимостей
uv pip install -r requirements.txt       # Из requirements.txt
uv pip install pyqt6                     # Конкретный пакет
uv pip install -e .                      # Режим разработки (pyproject.toml)
uv pip install "flask>=2.0"              # С указанием версии

# Работа с lock-файлами
uv lock          # Создать/обновить uv.lock
uv sync          # Установить зависимости из lock-файла

# Управление Python
uv python list                    # Список установленных версий Python
uv python install 3.12            # Установить Python 3.12
uv python pin 3.12                # Зафиксировать версию в .python-version

# Удаление пакетов
uv pip uninstall pyqt6

# Просмотр установленных пакетов
uv pip freeze
```

#### Работа с разными версиями Python

uv автоматически определяет версию Python из:
- Файла `.python-version` (создаётся командой `uv python pin`)
- Параметра `requires-python` в `pyproject.toml`
- Указанной версии в команде `uv venv --python`

```bash
# Создать окружение с конкретной версией Python
uv venv --python 3.11

# Установить конкретную версию Python через uv
uv python install 3.12
uv python install 3.11

# Показать доступные и установленные версии
uv python list
```

#### Лучшие практики использования uv

1. **Всегда используйте lock-файлы** — коммитьте `uv.lock` для воспроизводимых сборок
2. **Используйте `uv sync`** вместо `uv pip install` после `uv lock` — это гарантирует установку точных версий
3. **Указывайте минимальные версии** в `pyproject.toml` — uv сам подберёт совместимые версии
4. **Используйте workspace** для больших проектов — это упрощает управление зависимостями
5. **Добавляйте `.venv/` в `.gitignore`** — виртуальное окружение не нужно коммитить

### Требования

- Python 3.12+
- uv (см. инструкцию по установке выше)

### Настройка виртуального окружения

#### Windows (PowerShell)

```powershell
# Создание виртуального окружения
uv venv

# Активация виртуального окружения
.venv\Scripts\Activate

# Установка зависимостей
uv pip install -r requirements.txt
```

#### Windows (CMD)

```cmd
:: Создание виртуального окружения
uv venv

:: Активация виртуального окружения
.venv\Scripts\activate.bat

:: Установка зависимостей
uv pip install -r requirements.txt
```

#### macOS / Linux

```bash
# Создание виртуального окружения
uv venv

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей
uv pip install -r requirements.txt
```

> **Примечание:** Если файл `requirements.txt` отсутствует, но есть `pyproject.toml`, можно использовать:
> ```bash
> uv pip install -e .
> ```

#### Деактивация виртуального окружения

После завершения работы деактивируйте виртуальное окружение:

```bash
deactivate
```

---

## Запуск примеров

```bash
python practical_17_tkinter_app_creation_solution.py
python practical_27_pyqt_basic_applications_solution.py
```
