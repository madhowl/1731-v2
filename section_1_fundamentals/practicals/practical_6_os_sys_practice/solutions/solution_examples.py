# Решения для практического занятия 6: Работа с os и sys

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List
import json
import threading
import time

# Решение задания 1: Работа с файловой системой
class FileSystemManager:
    """Класс для управления файловой системой"""
    def __init__(self):
        self.current_directory = os.getcwd()
        self.lock = threading.Lock()
    
    def get_current_directory_info(self) -> Dict[str, Any]:
        """Получает информацию о текущей директории"""
        with self.lock:
            info = {
                'current_directory': self.current_directory,
                'items': [],
                'total_items': 0,
                'total_size': 0
            }
            
            try:
                items = os.listdir(self.current_directory)
                info['total_items'] = len(items)
                
                for item in items:
                    item_path = os.path.join(self.current_directory, item)
                    is_dir = os.path.isdir(item_path)
                    size = 0 if is_dir else os.path.getsize(item_path)
                    info['total_size'] += size
                    
                    item_info = {
                        'name': item,
                        'type': 'directory' if is_dir else 'file',
                        'size': size,
                        'path': item_path,
                        'modified': os.path.getmtime(item_path)
                    }
                    info['items'].append(item_info)
            except PermissionError as e:
                print(f"Ошибка доступа к директории: {e}")
            
            return info
    
    def create_directory_and_files(self, dir_name: str, file_names: List[str]) -> bool:
        """Создает директорию и файлы в ней"""
        with self.lock:
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"Директория '{dir_name}' создана")
                
                for file_name in file_names:
                    file_path = os.path.join(dir_name, file_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"Содержимое файла {file_name}\n")
                    print(f"Файл '{file_name}' создан")
                
                return True
            except OSError as e:
                print(f"Ошибка при создании директории или файлов: {e}")
                return False
    
    def remove_directory_and_contents(self, dir_name: str) -> bool:
        """Удаляет директорию и все ее содержимое"""
        with self.lock:
            try:
                shutil.rmtree(dir_name)
                print(f"Директория '{dir_name}' и все ее содержимое удалены")
                return True
            except OSError as e:
                print(f"Ошибка при удалении директории: {e}")
                return False

# Решение задания 2: Работа с путями
class PathManager:
    """Класс для работы с путями"""
    @staticmethod
    def join_paths(*path_parts) -> str:
        """Объединяет части пути"""
        return os.path.join(*path_parts)
    
    @staticmethod
    def get_path_components(path: str) -> Dict[str, str]:
        """Разбирает путь на компоненты"""
        return {
            'full_path': path,
            'directory': os.path.dirname(path),
            'filename': os.path.basename(path),
            'extension': os.path.splitext(path)[1],
            'name_without_ext': os.path.splitext(path)[0],
            'absolute_path': os.path.abspath(path),
            'is_absolute': os.path.isabs(path),
            'is_file': os.path.isfile(path),
            'is_directory': os.path.isdir(path)
        }
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """Нормализует путь, убирая .. и ."""
        return os.path.normpath(path)
    
    @staticmethod
    def resolve_path(path: str) -> str:
        """Разрешает символические ссылки и нормализует путь"""
        return os.path.realpath(path)

# Задание 3: Работа с переменными окружения
class EnvironmentManager:
    """Класс для работы с переменными окружения"""
    def __init__(self):
        self.lock = threading.Lock()
    
    def get_environment_variable(self, var_name: str, default_value: str = None) -> str:
        """Получает значение переменной окружения"""
        with self.lock:
            return os.environ.get(var_name, default_value)
    
    def set_environment_variable(self, var_name: str, var_value: str) -> bool:
        """Устанавливает переменную окружения"""
        with self.lock:
            try:
                os.environ[var_name] = var_value
                print(f"Переменная окружения {var_name} установлена в {var_value}")
                return True
            except Exception as e:
                print(f"Ошибка при установке переменной окружения: {e}")
                return False
    
    def remove_environment_variable(self, var_name: str) -> bool:
        """Удаляет переменную окружения"""
        with self.lock:
            try:
                if var_name in os.environ:
                    del os.environ[var_name]
                    print(f"Переменная окружения {var_name} удалена")
                    return True
                return False
            except Exception as e:
                print(f"Ошибка при удалении переменной окружения: {e}")
                return False
    
    def get_all_environment_variables(self) -> Dict[str, str]:
        """Получает все переменные окружения"""
        with self.lock:
            return dict(os.environ)
    
    def save_environment_to_file(self, filename: str) -> bool:
        """Сохраняет переменные окружения в файл"""
        with self.lock:
            try:
                env_vars = self.get_all_environment_variables()
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(env_vars, f, indent=2, ensure_ascii=False)
                print(f"Переменные окружения сохранены в {filename}")
                return True
            except Exception as e:
                print(f"Ошибка при сохранении переменных окружения: {e}")
                return False

# Задание 4: Аргументы командной строки
class CommandLineParser:
    """Парсер аргументов командной строки"""
    def __init__(self):
        self.args = sys.argv
        self.parsed_args = {}
    
    def parse_arguments(self) -> Dict[str, Any]:
        """Парсит аргументы командной строки"""
        self.parsed_args = {
            'script_name': self.args[0] if self.args else '',
            'arguments': self.args[1:] if len(self.args) > 1 else [],
            'argument_count': len(self.args) - 1 if self.args else 0,
            'as_dict': {}
        }
        
        # Разбор аргументов в формате --key value
        i = 1
        while i < len(self.args):
            arg = self.args[i]
            if arg.startswith('--'):
                key = arg[2:]
                if i + 1 < len(self.args) and not self.args[i + 1].startswith('--'):
                    value = self.args[i + 1]
                    self.parsed_args['as_dict'][key] = value
                    i += 2
                else:
                    self.parsed_args['as_dict'][key] = True
                    i += 1
            else:
                i += 1
        
        return self.parsed_args
    
    def get_argument(self, key: str, default: Any = None) -> Any:
        """Получает значение аргумента"""
        return self.parsed_args['as_dict'].get(key, default)
    
    def print_help(self):
        """Печатает справку по использованию"""
        print("Использование: python script.py [options]")
        print("Опции:")
        print("  --help     Показать это сообщение")
        print("  --config   Путь к конфигурационному файлу")
        print("  --verbose  Подробный вывод")

# Решение задания 5: Системная информация
class SystemInfo:
    """Класс для получения системной информации"""
    @staticmethod
    def get_python_info() -> Dict[str, Any]:
        """Получает информацию о Python"""
        return {
            'version': sys.version,
            'version_info': sys.version_info,
            'implementation': platform.python_implementation(),
            'compiler': platform.python_compiler(),
            'build': sys.version.split('\n'),
            'executable': sys.executable,
            'prefix': sys.prefix,
            'exec_prefix': sys.exec_prefix,
            'path': sys.path
        }
    
    @staticmethod
    def get_platform_info() -> Dict[str, str]:
        """Получает информацию о платформе"""
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'architecture': platform.architecture(),
            'node': platform.node(),
            'uname': platform.uname()._asdict()
        }
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Получает информацию о памяти (приблизительно)"""
        try:
            # Попытка получить информацию о памяти
            if platform.system() == "Windows":
                result = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], 
                                      capture_output=True, text=True)
                memory_info = result.stdout
            elif platform.system() in ["Linux", "Darwin"]:
                result = subprocess.run(['free', '-b'], capture_output=True, text=True)
                memory_info = result.stdout
            else:
                memory_info = "Информация недоступна для данной платформы"
            
            return {
                'memory_info': memory_info,
                'byteorder': sys.byteorder,
                'maxsize': sys.maxsize
            }
        except Exception as e:
            return {
                'error': f"Не удалось получить информацию о памяти: {e}",
                'byteorder': sys.byteorder,
                'maxsize': sys.maxsize
            }
    
    @staticmethod
    def get_module_info() -> Dict[str, List[str]]:
        """Получает информацию о загруженных модулях"""
        return {
            'builtin_modules': sys.builtin_module_names,
            'loaded_modules': list(sys.modules.keys()),
            'meta_path': sys.meta_path,
            'path_hooks': sys.path_hooks
        }

class DiagnosticTool:
    """Утилита системной диагностики"""
    def __init__(self):
        self.info = SystemInfo()
    
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """Запускает полную диагностику системы"""
        diagnostic_results = {
            'timestamp': time.time(),
            'python_info': self.info.get_python_info(),
            'platform_info': self.info.get_platform_info(),
            'memory_info': self.info.get_memory_info(),
            'module_info': self.info.get_module_info()
        }
        return diagnostic_results
    
    def print_diagnostic_report(self):
        """Печатает отчет диагностики"""
        results = self.run_full_diagnostic()
        
        print("=== СИСТЕМНАЯ ДИАГНОСТИКА ===")
        print(f"Время диагностики: {time.ctime(results['timestamp'])}")
        
        print("\n--- ИНФОРМАЦИЯ О PYTHON ---")
        python_info = results['python_info']
        print(f"Версия Python: {python_info['version'].split()[0]}")
        print(f"Реализация: {python_info['implementation']}")
        print(f"Компилятор: {python_info['compiler']}")
        print(f"Исполняемый файл: {python_info['executable']}")
        
        print("\n--- ИНФОРМАЦИЯ О ПЛАТФОРМЕ ---")
        platform_info = results['platform_info']
        print(f"Платформа: {platform_info['platform']}")
        print(f"Система: {platform_info['system']}")
        print(f"Версия системы: {platform_info['version']}")
        print(f"Архитектура: {platform_info['machine']}")
        print(f"Процессор: {platform_info['processor']}")
        
        print("\n--- ИНФОРМАЦИЯ О ПАМЯТИ ---")
        memory_info = results['memory_info']
        if 'error' in memory_info:
            print(f"Ошибка: {memory_info['error']}")
        else:
            print(f"Порядок байтов: {memory_info['byteorder']}")
            print(f"Максимальный размер int: {memory_info['maxsize']}")
        
        print("\n--- ЗАГРУЖЕННЫЕ МОДУЛИ ---")
        module_info = results['module_info']
        print(f"Встроенные модули: {len(module_info['builtin_modules'])} шт.")
        print(f"Загруженные модули: {len(module_info['loaded_modules'])} шт.")

# Дополнительные примеры использования модулей os и sys
def demonstrate_os_functions():
    """Демонстрирует различные функции модуля os"""
    print("\n=== Демонстрация функций модуля os ===")
    
    # Информация о текущем процессе
    print(f"PID текущего процесса: {os.getpid()}")
    print(f"UID текущего пользователя: {os.getuid() if hasattr(os, 'getuid') else 'N/A (Windows)'}")
    
    # Работа с директориями
    print(f"Домашняя директория: {os.path.expanduser('~')}")
    print(f"Временная директория: {tempfile.gettempdir()}")
    
    # Создание временного файла
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tmp') as tmp_file:
        tmp_file.write("Временное содержимое")
        temp_filename = tmp_file.name
    
    print(f"Создан временный файл: {temp_filename}")
    
    # Удаление временного файла
    os.unlink(temp_filename)
    print(f"Временный файл удален: {temp_filename}")

def demonstrate_sys_functions():
    """Демонстрирует различные функции модуля sys"""
    print("\n=== Демонстрация функций модуля sys ===")
    
    print(f"Версия Python: {sys.version_info}")
    print(f"Платформа: {sys.platform}")
    print(f"Размер строки 'hello': {sys.getsizeof('hello')} байт")
    print(f"Размер списка [1, 2, 3]: {sys.getsizeof([1, 2, 3])} байт")
    print(f"Максимальная глубина рекурсии: {sys.getrecursionlimit()}")
    
    # Информация о стандартных потоках
    print(f"stdin: {sys.stdin}")
    print(f"stdout: {sys.stdout}")
    print(f"stderr: {sys.stderr}")

def compare_os_sys_implementations():
    """Сравнение различных реализаций работы с os и sys"""
    print("\n=== Сравнение реализаций os и sys ===")
    print("""
    1. Классический подход (os.path):
       + Простота использования
       + Хорошая совместимость
       - Не очень питоновский синтаксис
       - Многословность в некоторых случаях
    
    2. Современный подход (pathlib):
       + Более питоновский синтаксис
       + Объектно-ориентированный подход
       + Лучшая читаемость кода
       - Требует Python 3.4+
       - Может быть медленнее для простых операций
    
    3. Работа с переменными окружения:
       + Простой доступ к системным настройкам
       + Гибкость в конфигурации приложений
       - Безопасность (чувствительные данные в переменных)
       - Зависимость от окружения
    
    4. Обработка аргументов командной строки:
       + Гибкость в настройке приложения
       + Возможность автоматизации
       - Сложность валидации аргументов
       - Необходимость документирования
    
    5. Системная информация:
       + Доступ к важной информации о среде выполнения
       + Возможность адаптации приложения под среду
       - Различия между платформами
       - Некоторые данные могут быть недоступны
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 6 ===")
    
    print("\n1. Решение задания 1: Работа с файловой системой")
    fs_manager = FileSystemManager()
    
    # Получаем информацию о текущей директории
    dir_info = fs_manager.get_current_directory_info()
    print(f"Текущая директория: {dir_info['current_directory']}")
    print(f"Всего элементов: {dir_info['total_items']}")
    print(f"Общий размер: {dir_info['total_size']} байт")
    
    # Создаем тестовую директорию и файлы
    test_dir = "test_fs_operations"
    test_files = ["file1.txt", "file2.txt", "file3.txt"]
    fs_manager.create_directory_and_files(test_dir, test_files)
    
    # Удаляем тестовую директорию
    fs_manager.remove_directory_and_contents(test_dir)
    
    print("\n2. Решение задания 2: Работа с путями")
    path_manager = PathManager()
    
    path1 = path_manager.join_paths("home", "user", "documents", "file.txt")
    print(f"Объединенный путь: {path1}")
    
    path2 = "../folder/../another_folder/./file.txt"
    normalized_path = path_manager.normalize_path(path2)
    print(f"Нормализованный путь: {normalized_path}")
    
    path_info = path_manager.get_path_components("/home/user/documents/report.pdf")
    for key, value in path_info.items():
        print(f"  {key}: {value}")
    
    print("\n3. Решение задания 3: Переменные окружения")
    env_manager = EnvironmentManager()
    
    # Получаем переменную PATH
    path_var = env_manager.get_environment_variable("PATH", "PATH не найден")
    print(f"PATH: {path_var[:50]}..." if len(path_var) > 50 else f"PATH: {path_var}")
    
    # Устанавливаем временную переменную
    env_manager.set_environment_variable("TEST_VAR", "test_value")
    test_value = env_manager.get_environment_variable("TEST_VAR")
    print(f"Значение TEST_VAR: {test_value}")
    
    # Удаляем переменную
    env_manager.remove_environment_variable("TEST_VAR")
    
    print("\n4. Решение задания 4: Аргументы командной строки")
    cmd_parser = CommandLineParser()
    args_info = cmd_parser.parse_arguments()
    print(f"Скрипт: {args_info['script_name']}")
    print(f"Аргументы: {args_info['arguments']}")
    print(f"Количество аргументов: {args_info['argument_count']}")
    
    print("\n5. Решение задания 5: Системная информация")
    diagnostic_tool = DiagnosticTool()
    diagnostic_tool.print_diagnostic_report()
    
    print("\n6. Дополнительные примеры")
    demonstrate_os_functions()
    demonstrate_sys_functions()
    compare_os_sys_implementations()