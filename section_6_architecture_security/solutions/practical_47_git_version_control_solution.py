# Решения для практического занятия 47: Система контроля версий Git

"""
Этот файл содержит примеры и инструкции по работе с Git.

Для выполнения практических заданий используйте команды в терминале.
"""


# =============================================================================
# Задание 1: Основы Git
# =============================================================================

def git_basics_example():
    """
    Пример основных команд Git.
    
    Команды для терминала:
    
    # Инициализация репозитория
    git init
    
    # Настройка пользователя
    git config --global user.name "Ваше Имя"
    git config --global user.email "ваш-email@example.com"
    
    # Проверка состояния
    git status
    
    # Просмотр истории
    git log
    git log --oneline
    """
    print("Основы Git:")
    print("git init                    # Инициализация репозитория")
    print("git config user.name        # Настройка имени")
    print("git config user.email       # Настройка email")
    print("git status                 # Проверка состояния")
    print("git log                    # История коммитов")


# =============================================================================
# Задание 2: Работа с файлами
# =============================================================================

def git_file_operations_example():
    """
    Пример работы с файлами в Git.
    
    Команды для терминала:
    
    # Добавление файлов
    git add filename.txt           # Конкретный файл
    git add .                      # Все файлы
    git add *.py                   # Файлы по шаблону
    
    # Создание коммита
    git commit -m "Описание изменений"
    git commit -am "Описание"       # Добавить и закоммитить
    
    # Просмотр изменений
    git diff                       # Изменения в рабочей директории
    git diff --staged              # Изменения в staging
    git diff HEAD~1                # Изменения между коммитами
    """
    print("Работа с файлами:")
    print("git add .                  # Добавить все файлы")
    print("git commit -m 'Коммит'    # Создать коммит")
    print("git diff                   # Просмотр изменений")


def gitignore_example():
    """
    Пример файла .gitignore
    """
    return """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Virtual environments
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
"""


# =============================================================================
# Задание 3: Ветвление
# =============================================================================

def git_branching_example():
    """
    Пример работы с ветками.
    
    Команды для терминала:
    
    # Просмотр веток
    git branch                    # Локальные ветки
    git branch -a                # Все ветки
    
    # Создание ветки
    git branch feature-login     # Создать ветку
    git checkout -b feature-login  # Создать и переключиться
    git switch -c feature-login     # Альтернатива (Git 2.23+)
    
    # Переключение веток
    git checkout main
    git switch main
    
    # Удаление ветки
    git branch -d feature-login    # Безопасное удаление
    git branch -D feature-login   # Принудительное удаление
    """
    print("Работа с ветками:")
    print("git branch                  # Список веток")
    print("git checkout -b feature    # Создать и переключиться")
    print("git switch main            # Переключиться на main")
    print("git branch -d feature     # Удалить ветку")


# =============================================================================
# Задание 4: Слияние
# =============================================================================

def git_merging_example():
    """
    Пример слияния веток.
    
    Команды для терминала:
    
    # Переключение на основную ветку
    git checkout main
    
    # Слияние ветки
    git merge feature-login
    
    # Fast-forward merge
    git merge --ff-only feature
    
    # Merge с созданием коммита
    git merge --no-ff feature
    
    # Разрешение конфликтов
    # После возникновения конфликта:
    # 1. Отредактируйте файлы с конфликтами
    # 2. git add <file>
    # 3. git commit
    """
    print("Слияние веток:")
    print("git checkout main")
    print("git merge feature          # Слияние ветки")
    print("git merge --no-ff feature # Слияние с коммитом")


def git_rebase_example():
    """
    Пример использования rebase.
    
    Команды для терминала:
    
    # Перебазирование
    git checkout feature
    git rebase main
    
    # Интерактивный rebase
    git rebase -i HEAD~3
    
    # Cherry-pick
    git cherry-pick <commit-hash>
    """
    print("Работа с rebase:")
    print("git checkout feature")
    print("git rebase main           # Перебазировать на main")
    print("git cherry-pick <hash>   # Применить коммит")


# =============================================================================
# Задание 5: Удаленные репозитории
# =============================================================================

def git_remote_example():
    """
    Пример работы с удаленными репозиториями.
    
    Команды для терминала:
    
    # Добавление удаленного репозитория
    git remote add origin https://github.com/username/repo.git
    
    # Просмотр удаленных
    git remote -v
    
    # Отправка изменений
    git push origin main
    git push -u origin main   # С upstream
    
    # Получение изменений
    git fetch origin           # Только получить
    git pull origin main       # Получить и слить
    
    # Удаление удаленного репозитория
    git remote remove origin
    """
    print("Работа с удаленными репозиториями:")
    print("git remote add origin <url>  # Добавить remote")
    print("git push origin main         # Отправить")
    print("git pull origin main        # Получить и слить")
    print("git fetch origin             # Только получить")


# =============================================================================
# Задание 6: Теги
# =============================================================================

def git_tags_example():
    """
    Пример работы с тегами.
    
    Команды для терминала:
    
    # Создание тега
    git tag v1.0.0                    # Легковесный
    git tag -a v1.0.0 -m "Релиз 1.0"  # Аннотированный
    
    # Просмотр тегов
    git tag
    git tag -l "v1.*"
    
    # Отправка тегов
    git push origin v1.0.0
    git push origin --tags
    
    # Создание ветки из тега
    git checkout -b release v1.0.0
    """
    print("Работа с тегами:")
    print("git tag v1.0.0              # Создать тег")
    print("git push origin v1.0.0      # Отправить тег")
    print("git checkout -b release v1.0  # Ветка из тега")


# =============================================================================
# Задание 7: Stash
# =============================================================================

def git_stash_example():
    """
    Пример работы с stash.
    
    Команды для терминала:
    
    # Сохранение изменений
    git stash
    git stash save "work in progress"
    
    # Просмотр stash
    git stash list
    git stash show stash@{0}
    
    # Применение stash
    git stash pop                    # Применить и удалить
    git stash apply                 # Применить, не удалять
    
    # Удаление stash
    git stash drop stash@{0}
    git stash clear
    """
    print("Работа со stash:")
    print("git stash                   # Сохранить изменения")
    print("git stash pop               # Применить и удалить")
    print("git stash list              # Просмотр stash")


# =============================================================================
# Пример скрипта для автоматизации
# =============================================================================

def git_workflow_script():
    """
    Пример скрипта для типичного рабочего процесса.
    """
    return '''
#!/bin/bash

# Скрипт для типичного рабочего процесса

echo "=== Начало рабочего процесса ==="

# Проверка статуса
echo "Текущий статус:"
git status

# Получение последних изменений
echo ""
echo "=== Получение изменений ==="
git pull origin main

# Создание ветки для новой функции
FEATURE_NAME=${1:-"feature"}
echo "=== Создание ветки $FEATURE_NAME ==="
git checkout -b $FEATURE_NAME

echo ""
echo "=== Готово! ==="
echo "Внесите изменения и выполните:"
echo "  git add ."
echo "  git commit -m 'Описание изменений'"
echo "  git push -u origin $FEATURE_NAME"
'''


def git_hook_example():
    """
    Пример Git hook для автоматического тестирования.
    """
    return '''
#!/bin/bash
# .git/hooks/pre-commit

# Запуск тестов перед коммитом

echo "Запуск тестов..."

# Запуск pytest
pytest tests/ --tb=short

# Проверка кода линтером
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Если тесты не прошли, отменяем коммит
if [ $? -ne 0 ]; then
    echo "Ошибка! Тесты не прошли."
    exit 1
fi

echo "Все проверки пройдены!"
exit 0
'''


# =============================================================================
# Git Flow пример
# =============================================================================

def git_flow_example():
    """
    Пример использования Git Flow.
    """
    return '''
# Git Flow - модель ветвления

## Основные ветки
- main/master     - production код
- develop        - development код

## Вспки
- featureомогательные вет/*      - новые функции
- release/*      - подготовка к релизу
- hotfix/*      - срочные исправления

## Команды

# Начало новой функции
git checkout develop
git checkout -b feature/my-feature

# Завершение функции
git checkout develop
git merge --no-ff feature/my-feature
git branch -d feature/my-feature

# Начало релиза
git checkout develop
git checkout -b release/v1.0.0

# Завершение релиза
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Релиз 1.0.0"
git checkout develop
git merge --no-ff release/v1.0.0
git branch -d release/v1.0.0

# Начало hotfix
git checkout main
git checkout -b hotfix/fix-bug

# Завершение hotfix
git checkout main
git merge --no-ff hotfix/fix-bug
git tag -a v1.0.1 -m "Hotfix 1.0.1"
git checkout develop
git merge --no-ff hotfix/fix-bug
git branch -d hotfix/fix-bug
'''


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Демонстрация решений"""
    print("=" * 70)
    print("Решения для практического занятия 47: Система контроля версий Git")
    print("=" * 70)
    print()
    
    print("Задание 1: Основы Git")
    print("-" * 50)
    git_basics_example()
    print()
    
    print("Задание 2: Работа с файлами")
    print("-" * 50)
    git_file_operations_example()
    print()
    print("Пример .gitignore:")
    print(gitignore_example())
    print()
    
    print("Задание 3: Ветвление")
    print("-" * 50)
    git_branching_example()
    print()
    
    print("Задание 4: Слияние")
    print("-" * 50)
    git_merging_example()
    print()
    git_rebase_example()
    print()
    
    print("Задание 5: Удаленные репозитории")
    print("-" * 50)
    git_remote_example()
    print()
    
    print("Задание 6: Теги")
    print("-" * 50)
    git_tags_example()
    print()
    
    print("Задание 7: Stash")
    print("-" * 50)
    git_stash_example()
    print()
    
    print("=" * 70)
    print("Дополнительные примеры:")
    print("=" * 70)
    print("Git Workflow скрипт:")
    print(git_workflow_script())
    print()
    print("Git Flow:")
    print(git_flow_example())


if __name__ == "__main__":
    main()
