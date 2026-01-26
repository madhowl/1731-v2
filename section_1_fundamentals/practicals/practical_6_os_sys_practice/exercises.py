# Упражнения для практического занятия 6: Работа с os и sys

import os
import sys
import shutil
from pathlib import Path

# Задание 1: Работа с файловой системой
def get_current_directory_info():
    """Получает текущую директорию и выводит информацию о ней"""
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")
    
    # Получаем список файлов и подкаталогов
    items = os.listdir(current_dir)
    print(f"Содержимое директории ({len(items)} элементов):")
    for item in items:
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            print(f"  [DIR]  {item}")
        else:
            size = os.path.getsize(item_path)
            print(f"  [FILE] {item} ({size} bytes)")
    
    return current_dir

def create_directory_and_files(directory_name, file_names):
    """Создает каталог и файлы в нем"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"Каталог '{directory_name}' создан")
        
        for file_name in file_names:
            file_path = os.path.join(directory_name, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Это содержимое файла {file_name}\n")
            print(f"Файл '{file_name}' создан")
        
        return True
    except OSError as e:
        print(f"Ошибка при создании каталога или файлов: {e}")
        return False

def remove_directory_and_contents(directory_name):
    """Удаляет каталог и все его содержимое"""
    try:
        shutil.rmtree(directory_name)
        print(f"Каталог '{directory_name}' и его содержимое удалены")
        return True
    except OSError as e:
        print(f"Ошибка при удалении каталога: {e}")
        return False

# Задание 2: Работа с путями
def join_paths_example(*path_parts):
    """Объединяет части пути с использованием os.path.join()"""
    return os.path.join(*path_parts)

def get_path_components(path):
    """Разбирает путь на компоненты"""
    components = {
        'full_path': path,
        'directory': os.path.dirname(path),
        'filename': os.path.basename(path),
        'extension': os.path.splitext(path)[1],
        'name_without_ext': os.path.splitext(path)[0],
        'absolute': os.path.abspath(path),
        'is_absolute': os.path.isabs(path)
    }
    return components

def normalize_path(path):
    """Нормализует путь, убирая '..' и '.'"""
    return os.path.normpath(path)

# Задание 3: Переменные окружения
def get_environment_variable(var_name, default_value=None):
    """Получает значение переменной окружения"""
    return os.environ.get(var_name, default_value)

def set_environment_variable(var_name, var_value):
    """Устанавливает переменную окружения"""
    os.environ[var_name] = var_value
    print(f"Переменная окружения {var_name} установлена в {var_value}")

def list_all_environment_variables():
    """Выводит список всех переменных окружения"""
    print("Переменные окружения:")
    for key, value in os.environ.items():
        print(f"  {key}={value}")

# Задание 4: Аргументы командной строки
def get_command_line_args():
    """Получает аргументы командной строки"""
    args = sys.argv
    print(f"Количество аргументов: {len(args)}")
    print(f"Имя скрипта: {args[0]}")
    if len(args) > 1:
        print(f"Аргументы: {args[1:]}")
    return args

def simple_cli_utility():
    """Простая утилита командной строки"""
    if len(sys.argv) < 2:
        print("Использование: python script.py <command> [args]")
        print("Команды: echo, add, list_env")
        return
    
    command = sys.argv[1]
    
    if command == "echo":
        if len(sys.argv) < 3:
            print("Использование: python script.py echo <text>")
        else:
            text = " ".join(sys.argv[2:])
            print(f"Вы сказали: {text}")
    
    elif command == "add":
        if len(sys.argv) < 4:
            print("Использование: python script.py add <num1> <num2>")
        else:
            try:
                num1 = float(sys.argv[2])
                num2 = float(sys.argv[3])
                result = num1 + num2
                print(f"{num1} + {num2} = {result}")
            except ValueError:
                print("Ошибка: оба аргумента должны быть числами")
    
    elif command == "list_env":
        list_all_environment_variables()
    
    else:
        print(f"Неизвестная команда: {command}")

# Задание 5: Системная информация
def get_python_version():
    """Получает версию Python"""
    return sys.version

def get_platform_info():
    """Получает информацию о платформе"""
    return {
        'platform': sys.platform,
        'executable': sys.executable,
        'byte_order': sys.byteorder,
        'filesystem_encoding': sys.getfilesystemencoding()
    }

def get_object_size(obj):
    """Получает размер объекта в байтах"""
    return sys.getsizeof(obj)

def get_python_path():
    """Получает пути поиска модулей Python"""
    return sys.path

def system_diagnostic_tool():
    """Утилита системной диагностики"""
    print("=== Системная диагностика ===")
    print(f"Версия Python: {get_python_version()}")
    print(f"Платформа: {sys.platform}")
    
    platform_info = get_platform_info()
    for key, value in platform_info.items():
        print(f"{key}: {value}")
    
    # Примеры размеров объектов
    test_objects = [
        42,
        "Hello, World!",
        [1, 2, 3, 4, 5],
        {"key": "value"},
        (1, 2, 3)
    ]
    
    print("\nРазмеры различных объектов:")
    for obj in test_objects:
        size = get_object_size(obj)
        print(f"  {type(obj).__name__}: {size} байт")
    
    print(f"\nКоличество аргументов командной строки: {len(sys.argv)}")
    print(f"Имя исполняемого файла: {sys.executable}")

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Работа с файловой системой ===")
    current_dir = get_current_directory_info()
    
    # Создаем тестовый каталог и файлы
    test_dir = "test_folder"
    test_files = ["file1.txt", "file2.txt", "file3.txt"]
    create_directory_and_files(test_dir, test_files)
    
    # Удаляем тестовый каталог
    remove_directory_and_contents(test_dir)
    
    print("\n=== Задание 2: Работа с путями ===")
    path1 = join_paths_example("home", "user", "documents", "file.txt")
    print(f"Объединенный путь: {path1}")
    
    path2 = "../folder/../another_folder/./file.txt"
    normalized_path = normalize_path(path2)
    print(f"Нормализованный путь: {normalized_path}")
    
    path_info = get_path_components("/home/user/documents/report.pdf")
    for key, value in path_info.items():
        print(f"  {key}: {value}")
    
    print("\n=== Задание 3: Переменные окружения ===")
    home_dir = get_environment_variable("HOME") or get_environment_variable("USERPROFILE")
    print(f"Домашняя директория: {home_dir}")
    
    path_var = get_environment_variable("PATH")
    print(f"PATH содержит {len(path_var.split(os.pathsep))} путей" if path_var else "PATH не найден")
    
    # Устанавливаем временную переменную
    set_environment_variable("TEST_VAR", "test_value")
    print(f"Значение TEST_VAR: {get_environment_variable('TEST_VAR')}")
    
    print("\n=== Задание 4: Аргументы командной строки ===")
    args = get_command_line_args()
    
    print("\n=== Задание 5: Системная информация ===")
    system_diagnostic_tool()