# Лекция 6: Модуль os и sys

## Работа с файловой системой, переменные окружения, аргументы командной строки

### План лекции:
1. Введение в модули os и sys
2. Модуль os
3. Модуль sys
4. Работа с путями (os.path)
5. Переменные окружения
6. Аргументы командной строки
7. Практические примеры

---

## 1. Введение в модули os и sys

Модули `os` и `sys` предоставляют интерфейс для взаимодействия с операционной системой и средой выполнения Python.

- `os` - функции для работы с операционной системой (файловая система, процессы, переменные окружения)
- `sys` - доступ к параметрам и функциям интерпретатора Python

```python
import os
import sys
```

---

## 2. Модуль os

Модуль `os` предоставляет способ использования функций операционной системы.

### Основные функции:

```python
import os

# Получение текущей директории
current_dir = os.getcwd()
print(f"Текущая директория: {current_dir}")

# Смена директории
# os.chdir('/path/to/new/directory')

# Список файлов и папок в директории
files_and_dirs = os.listdir('.')
print(f"Файлы и папки: {files_and_dirs}")

# Создание директории
# os.mkdir('new_directory')

# Создание директории с поддиректориями
# os.makedirs('parent/child/grandchild', exist_ok=True)

# Удаление файлов и директорий
# os.remove('file.txt')  # Удалить файл
# os.rmdir('directory')  # Удалить пустую директорию
# os.removedirs('path/to/remove')  # Удалить пустые директории
# os.system('rm -rf directory')  # Удалить директорию рекурсивно (опасно!)

# Информация о файле
file_stat = os.stat('some_file.txt')
print(f"Размер файла: {file_stat.st_size} байт")
print(f"Время последнего изменения: {file_stat.st_mtime}")
```

### Выполнение команд ОС:

```python
# Выполнение команды ОС
exit_code = os.system('echo "Hello from OS"')
print(f"Код завершения: {exit_code}")

# Получение вывода команды (опасный способ!)
import subprocess
result = subprocess.check_output(['ls', '-la'], universal_newlines=True)
print(result)
```

### Управление процессами:

```python
# Получение ID текущего процесса
pid = os.getpid()
print(f"ID процесса: {pid}")

# Получение ID родительского процесса
ppid = os.getppid()
print(f"ID родительского процесса: {ppid}")
```

---

## 3. Модуль sys

Модуль `sys` предоставляет доступ к некоторым переменным, используемым или поддерживаемым интерпретатором Python.

### Основные функции:

```python
import sys

# Версия Python
print(f"Версия Python: {sys.version}")
print(f"Версия Python (кратко): {sys.version_info}")

# Платформа
print(f"Платформа: {sys.platform}")

# Аргументы командной строки
print(f"Аргументы командной строки: {sys.argv}")

# Размер объекта в памяти
obj = [1, 2, 3, 4, 5]
print(f"Размер списка: {sys.getsizeof(obj)} байт")

# Путь к модулям
print(f"Пути поиска модулей: {sys.path}")

# Путь к интерпретатору Python
print(f"Путь к Python: {sys.executable}")

# Выход из программы
# sys.exit(0)  # Нормальный выход
# sys.exit(1)  # Выход с ошибкой
```

### Стандартные потоки ввода-вывода:

```python
import sys

# Стандартный вывод
sys.stdout.write("Привет, мир!\n")

# Стандартная ошибка
sys.stderr.write("Это сообщение об ошибке\n")

# Стандартный ввод
print("Введите что-нибудь:")
user_input = sys.stdin.readline()
print(f"Вы ввели: {user_input}")
```

---

## 4. Работа с путями (os.path)

Модуль `os.path` предоставляет функции для работы с путями к файлам и каталогам.

```python
import os

# Объединение путей (универсально для разных ОС)
path = os.path.join('folder', 'subfolder', 'file.txt')
print(path)  # folder\subfolder\file.txt (в Windows) или folder/subfolder/file.txt (в Unix)

# Разделение пути и имени файла
full_path = '/home/user/documents/file.txt'
directory, filename = os.path.split(full_path)
print(f"Директория: {directory}")  # /home/user/documents
print(f"Имя файла: {filename}")   # file.txt

# Разделение пути и расширения
filename, extension = os.path.splitext('document.pdf')
print(f"Имя файла: {filename}")     # document
print(f"Расширение: {extension}")   # .pdf

# Абсолютный путь
abs_path = os.path.abspath('relative/path')
print(f"Абсолютный путь: {abs_path}")

# Проверка существования файла/каталога
exists = os.path.exists('/path/to/check')
print(f"Существует: {exists}")

# Проверка, является ли путь файлом
is_file = os.path.isfile('/path/to/file')
print(f"Это файл: {is_file}")

# Проверка, является ли путь каталогом
is_dir = os.path.isdir('/path/to/dir')
print(f"Это директория: {is_dir}")

# Размер файла
file_size = os.path.getsize('/path/to/file')
print(f"Размер файла: {file_size} байт")

# Время последнего изменения
mod_time = os.path.getmtime('/path/to/file')
print(f"Время изменения: {mod_time}")
```

---

## 5. Переменные окружения

Переменные окружения - это динамические переменные, которые влияют на поведение процессов в системе.

```python
import os

# Получение переменной окружения
home_dir = os.environ.get('HOME')  # В Unix/Linux
# home_dir = os.environ.get('USERPROFILE')  # В Windows

# Если переменная не существует, можно указать значение по умолчанию
path_var = os.environ.get('PATH', 'Не найдено')

print(f"Домашняя директория: {home_dir}")
print(f"PATH: {path_var}")

# Установка переменной окружения
os.environ['MY_VAR'] = 'my_value'

# Получение всех переменных окружения
all_env_vars = dict(os.environ)
print(f"Количество переменных окружения: {len(all_env_vars)}")

# Удаление переменной окружения
if 'MY_VAR' in os.environ:
    del os.environ['MY_VAR']
```

### Практический пример работы с переменными окружения:

```python
import os

def get_config():
    """Получение конфигурации из переменных окружения"""
    config = {
        'host': os.environ.get('HOST', 'localhost'),
        'port': int(os.environ.get('PORT', 8000)),
        'debug': os.environ.get('DEBUG', 'False').lower() == 'true',
        'database_url': os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    }
    return config

config = get_config()
print(config)
```

---

## 6. Аргументы командной строки

Аргументы командной строки передаются в программу при запуске и доступны через `sys.argv`.

```python
import sys

def parse_args():
    """Простой парсер аргументов командной строки"""
    if len(sys.argv) < 2:
        print("Использование: python script.py <аргумент1> <аргумент2> ...")
        sys.exit(1)
    
    # sys.argv[0] - имя скрипта
    script_name = sys.argv[0]
    arguments = sys.argv[1:]  # Все остальные аргументы
    
    print(f"Скрипт: {script_name}")
    print(f"Аргументы: {arguments}")
    
    return arguments

# args = parse_args()
```

### Использование argparse для более сложных случаев:

```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Пример использования argparse')
    
    # Позиционный аргумент
    parser.add_argument('input_file', help='Входной файл для обработки')
    
    # Опциональный аргумент
    parser.add_argument('-o', '--output', help='Выходной файл', default='output.txt')
    
    # Аргумент с выбором из нескольких вариантов
    parser.add_argument('-f', '--format', choices=['json', 'xml', 'csv'], 
                       default='json', help='Формат вывода')
    
    # Флаг (булевый аргумент)
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Подробный вывод')
    
    return parser

# Пример использования:
# parser = create_parser()
# args = parser.parse_args()
# print(f"Входной файл: {args.input_file}")
# print(f"Выходной файл: {args.output}")
# print(f"Формат: {args.format}")
# print(f"Подробный вывод: {args.verbose}")
```

---

## 7. Практические примеры

### Пример 1: Поиск файлов по расширению

```python
import os

def find_files_by_extension(directory, extension):
    """Поиск файлов с определенным расширением в директории и поддиректориях"""
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    
    return found_files

# Поиск всех .py файлов в текущей директории
python_files = find_files_by_extension('.', '.py')
print(f"Найдено .py файлов: {len(python_files)}")
```

### Пример 2: Информация о системе

```python
import os
import sys
import platform

def system_info():
    """Сбор информации о системе"""
    info = {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'hostname': platform.node(),
        'processor': platform.processor(),
        'python_version': sys.version_info,
        'python_executable': sys.executable,
        'current_working_directory': os.getcwd(),
        'number_of_cpu': os.cpu_count(),
        'total_memory': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') if os.name == 'posix' else 'N/A'
    }
    return info

info = system_info()
for key, value info.items():
    print(f"{key}: {value}")
```

### Пример 3: Копирование файлов с резервным копированием

```python
import os
import shutil
from datetime import datetime

def backup_copy(source, destination):
    """Создание резервной копии файла при копировании"""
    if os.path.exists(destination):
        # Создаем резервную копию существующего файла
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{destination}.backup_{timestamp}"
        shutil.copy2(destination, backup_name)
        print(f"Создана резервная копия: {backup_name}")
    
    # Копируем новый файл
    shutil.copy2(source, destination)
    print(f"Файл скопирован: {source} -> {destination}")

# Пример использования:
# backup_copy('source.txt', 'destination.txt')
```

### Пример 4: Аргументы командной строки для обработки файлов

```python
import sys
import os

def process_files_cli():
    """Обработка файлов через командную строку"""
    if len(sys.argv) < 2:
        print("Использование: python script.py <файл1> <файл2> ...")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            continue
            
        size = os.path.getsize(file_path)
        mod_time = os.path.getmtime(file_path)
        
        print(f"Файл: {file_path}")
        print(f"  Размер: {size} байт")
        print(f"  Последнее изменение: {mod_time}")
        print()

# process_files_cli()
```

---

## Заключение

Модули `os` и `sys` предоставляют мощные инструменты для взаимодействия с операционной системой и средой выполнения Python. Они позволяют управлять файлами и каталогами, получать информацию о системе, работать с переменными окружения и аргументами командной строки.

## Контрольные вопросы:
1. В чем разница между os и sys?
2. Как объединять пути к файлам кроссплатформенно?
3. Как получить аргументы командной строки в Python?
4. Как проверить существование файла?
5. Как работать с переменными окружения?
