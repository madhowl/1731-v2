# Практическое занятие 6: Работа с модулями os и sys в игровом контексте

## Цель занятия
Изучить возможности модулей os и sys в Python для взаимодействия с операционной системой, работы с файловой системой, переменными окружения и аргументами командной строки в игровом приложении.

## Задачи
1. Использовать модуль os для работы с файловой системой игрового проекта
2. Применить модуль sys для получения информации о системе и обработки аргументов командной строки
3. Реализовать систему конфигурации игры через переменные окружения
4. Создать инструменты для управления игровыми файлами и каталогами
5. Разработать систему логирования с использованием системных ресурсов

## Ход работы

### 1. Основы работы с модулем os в игровом контексте

Создайте файл `game_file_manager.py` и реализуйте следующие функции:

#### Работа с игровыми каталогами

```python
import os
import sys
from pathlib import Path

def create_game_directories(base_path="game_data"):
    """
    Создает стандартную структуру каталогов для игрового проекта
    
    Args:
        base_path (str): Базовый путь для создания каталогов
    
    Returns:
        dict: Словарь с путями к созданным каталогам
    """
    # ВАШ КОД ЗДЕСЬ - создайте структуру каталогов
    # Пример структуры: saves/, configs/, mods/, logs/, screenshots/
    pass  # Замените на ваш код

def list_game_files(directory_path, file_extension=None):
    """
    Возвращает список файлов в игровом каталоге
    
    Args:
        directory_path (str): Путь к каталогу
        file_extension (str): Расширение файлов для фильтрации (например, ".sav")
    
    Returns:
        list: Список файлов в каталоге
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте получение списка файлов
    pass  # Замените на ваш код

def get_save_files_info(saves_directory="saves"):
    """
    Возвращает информацию о файлах сохранений
    
    Args:
        saves_directory (str): Каталог сохранений
    
    Returns:
        list: Список информации о файлах сохранений
    """
    # ВАШ КОД ЗДЕСЬ - получите информацию о файлах сохранений
    # Включите имя файла, размер, дату изменения
    pass  # Замените на ваш код
```

#### Работа с путями в игровом контексте

```python
def construct_asset_path(asset_type, asset_name, base_dir="assets"):
    """
    Конструирует путь к игровому ресурсу
    
    Args:
        asset_type (str): Тип ресурса (models, textures, sounds, etc.)
        asset_name (str): Имя ресурса
        base_dir (str): Базовый каталог ресурсов
    
    Returns:
        str: Полный путь к ресурсу
    """
    # ВАШ КОД ЗДЕСЬ - постройте путь к ресурсу
    pass  # Замените на ваш код

def validate_game_path(path):
    """
    Проверяет, является ли путь допустимым для игровых файлов
    
    Args:
        path (str): Путь для проверки
    
    Returns:
        bool: Является ли путь допустимым
    """
    # ВАШ КОД ЗДЕСЬ - проверьте, является ли путь безопасным и допустимым
    pass  # Замените на ваш код

def normalize_path(path):
    """
    Нормализует путь к стандартному формату
    
    Args:
        path (str): Путь для нормализации
    
    Returns:
        str: Нормализованный путь
    """
    # ВАШ КОД ЗДЕСЬ - нормализуйте путь
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Использование os и sys в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.1: Создание менеджера игровых файлов

Создайте класс для управления игровыми файлами:

```python
import os
import sys
from pathlib import Path
import shutil
from datetime import datetime

class GameFileManager:
    """
    Класс для управления игровыми файлами и каталогами
    """
    def __init__(self, game_root="game_data"):
        self.game_root = Path(game_root)
        self.create_standard_directories()
    
    def create_standard_directories(self):
        """
        Создает стандартные игровые каталоги
        """
        # ВАШ КОД ЗДЕСЬ - создайте стандартные каталоги:
        # saves, configs, mods, logs, screenshots, assets/models, assets/textures, etc.
        pass  # Замените на ваш код
    
    def get_game_info(self):
        """
        Возвращает информацию о структуре игровых файлов
        
        Returns:
            dict: Информация о каталогах и файлах
        """
        # ВАШ КОД ЗДЕСЬ - верните информацию о структуре
        pass  # Замените на ваш код
    
    def backup_save_files(self, backup_dir="backups"):
        """
        Создает резервную копию файлов сохранений
        
        Args:
            backup_dir (str): Каталог для резервных копий
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте резервное копирование
        pass  # Замените на ваш код

# Пример использования:
# file_manager = GameFileManager()
# info = file_manager.get_game_info()
# file_manager.backup_save_files()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import sys
from pathlib import Path
import shutil
from datetime import datetime

class GameFileManager:
    """
    Класс для управления игровыми файлами и каталогами
    """
    def __init__(self, game_root="game_data"):
        self.game_root = Path(game_root)
        self.create_standard_directories()
    
    def create_standard_directories(self):
        """
        Создает стандартные игровые каталоги
        """
        standard_dirs = [
            "saves",
            "configs", 
            "mods",
            "logs",
            "screenshots",
            "assets/models",
            "assets/textures", 
            "assets/sounds",
            "assets/shaders"
        ]
        
        for dir_path in standard_dirs:
            full_path = self.game_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
    
    def get_game_info(self):
        """
        Возвращает информацию о структуре игровых файлов
        
        Returns:
            dict: Информация о каталогах и файлах
        """
        info = {
            'root_path': str(self.game_root.absolute()),
            'directories': [],
            'files_count': {},
            'total_size': 0
        }
        
        for root, dirs, files in os.walk(self.game_root):
            rel_path = os.path.relpath(root, self.game_root)
            info['directories'].append(rel_path)
            
            file_count = len(files)
            info['files_count'][rel_path] = file_count
            
            for file in files:
                file_path = os.path.join(root, file)
                info['total_size'] += os.path.getsize(file_path)
        
        return info
    
    def backup_save_files(self, backup_dir="backups"):
        """
        Создает резервную копию файлов сохранений
        
        Args:
            backup_dir (str): Каталог для резервных копий
        """
        saves_path = self.game_root / "saves"
        if not saves_path.exists():
            print("Каталог сохранений не найден")
            return False
        
        backup_root = self.game_root / backup_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_root / f"saves_backup_{timestamp}"
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copytree(saves_path, backup_path / "saves", dirs_exist_ok=True)
            print(f"Резервная копия создана: {backup_path}")
            return True
        except Exception as e:
            print(f"Ошибка при создании резервной копии: {e}")
            return False
```

</details>

#### Задание 1.2: Система конфигурации через переменные окружения

Создайте систему конфигурации игры с использованием переменных окружения:

```python
import os

class GameConfig:
    """
    Система конфигурации игры через переменные окружения
    """
    def __init__(self):
        # Установите значения по умолчанию
        self.resolution_width = int(os.getenv("GAME_RESOLUTION_WIDTH", 1920))
        self.resolution_height = int(os.getenv("GAME_RESOLUTION_HEIGHT", 1080))
        self.fullscreen = os.getenv("GAME_FULLSCREEN", "False").lower() == "true"
        self.volume_master = float(os.getenv("GAME_VOLUME_MASTER", 1.0))
        self.volume_music = float(os.getenv("GAME_VOLUME_MUSIC", 0.8))
        self.volume_sfx = float(os.getenv("GAME_VOLUME_SFX", 1.0))
        self.graphics_quality = os.getenv("GAME_GRAPHICS_QUALITY", "high")
        self.language = os.getenv("GAME_LANGUAGE", "en")
    
    def get_config_as_dict(self):
        """
        Возвращает конфигурацию в виде словаря
        
        Returns:
            dict: Словарь с параметрами конфигурации
        """
        # ВАШ КОД ЗДЕСЬ - верните конфигурацию в виде словаря
        pass  # Замените на ваш код
    
    def validate_config(self):
        """
        Проверяет корректность параметров конфигурации
        
        Returns:
            list: Список ошибок валидации
        """
        # ВАШ КОД ЗДЕСЬ - проверьте корректность параметров
        pass  # Замените на ваш код
    
    def print_config_summary(self):
        """
        Выводит сводку по текущей конфигурации
        """
        # ВАШ КОД ЗДЕСЬ - выведите сводку по конфигурации
        pass  # Замените на ваш код

# Пример использования:
# config = GameConfig()
# config_summary = config.print_config_summary()
# validation_errors = config.validate_config()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os

class GameConfig:
    """
    Система конфигурации игры через переменные окружения
    """
    def __init__(self):
        # Установка значений по умолчанию из переменных окружения
        self.resolution_width = int(os.getenv("GAME_RESOLUTION_WIDTH", 1920))
        self.resolution_height = int(os.getenv("GAME_RESOLUTION_HEIGHT", 1080))
        self.fullscreen = os.getenv("GAME_FULLSCREEN", "False").lower() == "true"
        self.volume_master = min(max(float(os.getenv("GAME_VOLUME_MASTER", 1.0)), 0.0), 1.0)  # Ограничиваем от 0 до 1
        self.volume_music = min(max(float(os.getenv("GAME_VOLUME_MUSIC", 0.8)), 0.0), 1.0)
        self.volume_sfx = min(max(float(os.getenv("GAME_VOLUME_SFX", 1.0)), 0.0), 1.0)
        self.graphics_quality = os.getenv("GAME_GRAPHICS_QUALITY", "high").lower()
        self.language = os.getenv("GAME_LANGUAGE", "en").lower()
    
    def get_config_as_dict(self):
        """
        Возвращает конфигурацию в виде словаря
        
        Returns:
            dict: Словарь с параметрами конфигурации
        """
        return {
            'resolution_width': self.resolution_width,
            'resolution_height': self.resolution_height,
            'fullscreen': self.fullscreen,
            'volume_master': self.volume_master,
            'volume_music': self.volume_music,
            'volume_sfx': self.volume_sfx,
            'graphics_quality': self.graphics_quality,
            'language': self.language
        }
    
    def validate_config(self):
        """
        Проверяет корректность параметров конфигурации
        
        Returns:
            list: Список ошибок валидации
        """
        errors = []
        
        # Проверяем разрешение
        if self.resolution_width < 800 or self.resolution_width > 7680:
            errors.append(f"Некорректная ширина разрешения: {self.resolution_width} (допустимо 800-7680)")
        
        if self.resolution_height < 600 or self.resolution_height > 4320:
            errors.append(f"Некорректная высота разрешения: {self.resolution_height} (допустимо 600-4320)")
        
        # Проверяем громкость
        if not 0.0 <= self.volume_master <= 1.0:
            errors.append(f"Некорректная общая громкость: {self.volume_master} (допустимо 0.0-1.0)")
        
        if not 0.0 <= self.volume_music <= 1.0:
            errors.append(f"Некорректная громкость музыки: {self.volume_music} (допустимо 0.0-1.0)")
        
        if not 0.0 <= self.volume_sfx <= 1.0:
            errors.append(f"Некорректная громкость эффектов: {self.volume_sfx} (допустимо 0.0-1.0)")
        
        # Проверяем качество графики
        valid_qualities = ["low", "medium", "high", "ultra"]
        if self.graphics_quality not in valid_qualities:
            errors.append(f"Некорректное качество графики: {self.graphics_quality} (допустимо: {', '.join(valid_qualities)})")
        
        # Проверяем язык
        valid_languages = ["en", "ru", "es", "fr", "de", "ja", "ko", "zh"]
        if self.language not in valid_languages:
            errors.append(f"Некорректный язык: {self.language} (допустимо: {', '.join(valid_languages)})")
        
        return errors
    
    def print_config_summary(self):
        """
        Выводит сводку по текущей конфигурации
        """
        print("=== Текущая конфигурация игры ===")
        print(f"Разрешение: {self.resolution_width}x{self.resolution_height}")
        print(f"Полноэкранный режим: {self.fullscreen}")
        print(f"Громкость (общая/музыка/эффекты): {self.volume_master:.1f}/{self.volume_music:.1f}/{self.volume_sfx:.1f}")
        print(f"Качество графики: {self.graphics_quality}")
        print(f"Язык: {self.language}")
        print("=================================")
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Система модов для игры

Создайте систему управления модами игры:

```python
import os
from pathlib import Path

class ModManager:
    """
    Система управления модами игры
    """
    def __init__(self, mods_directory="mods"):
        self.mods_directory = Path(mods_directory)
        self.mods_directory.mkdir(exist_ok=True)
        self.active_mods = []
        self.mod_manifests = {}
    
    def scan_mods(self):
        """
        Сканирует каталог модов и возвращает список доступных модов
        
        Returns:
            list: Список доступных модов
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте сканирование модов
        pass  # Замените на ваш код
    
    def load_mod(self, mod_name):
        """
        Загружает мод в игру
        
        Args:
            mod_name (str): Название мода для загрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте загрузку мода
        pass  # Замените на ваш код
    
    def unload_mod(self, mod_name):
        """
        Выгружает мод из игры
        
        Args:
            mod_name (str): Название мода для выгрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте выгрузку мода
        pass  # Замените на ваш код
    
    def get_mod_dependencies(self, mod_name):
        """
        Возвращает зависимости указанного мода
        
        Args:
            mod_name (str): Название мода
            
        Returns:
            list: Список зависимостей
        """
        # ВАШ КОД ЗДЕСЬ - верните зависимости мода
        pass  # Замените на ваш код

# Пример использования:
# mod_manager = ModManager()
# available_mods = mod_manager.scan_mods()
# mod_manager.load_mod("texture_overhaul")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import json
from pathlib import Path

class ModManager:
    """
    Система управления модами игры
    """
    def __init__(self, mods_directory="mods"):
        self.mods_directory = Path(mods_directory)
        self.mods_directory.mkdir(exist_ok=True)
        self.active_mods = []
        self.mod_manifests = {}
    
    def scan_mods(self):
        """
        Сканирует каталог модов и возвращает список доступных модов
        
        Returns:
            list: Список доступных модов
        """
        available_mods = []
        
        for mod_dir in self.mods_directory.iterdir():
            if mod_dir.is_dir():
                manifest_path = mod_dir / "mod.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                        
                        mod_info = {
                            'name': manifest.get('name', mod_dir.name),
                            'version': manifest.get('version', '1.0.0'),
                            'author': manifest.get('author', 'Unknown'),
                            'description': manifest.get('description', ''),
                            'dependencies': manifest.get('dependencies', []),
                            'directory': mod_dir
                        }
                        
                        self.mod_manifests[mod_dir.name] = mod_info
                        available_mods.append(mod_info)
                    except json.JSONDecodeError:
                        print(f"Ошибка чтения манифеста для мода {mod_dir.name}")
                else:
                    # Создаем минимальный манифест для мода без него
                    mod_info = {
                        'name': mod_dir.name,
                        'version': '1.0.0',
                        'author': 'Unknown',
                        'description': '',
                        'dependencies': [],
                        'directory': mod_dir
                    }
                    
                    self.mod_manifests[mod_dir.name] = mod_info
                    available_mods.append(mod_info)
        
        return available_mods
    
    def load_mod(self, mod_name):
        """
        Загружает мод в игру
        
        Args:
            mod_name (str): Название мода для загрузки
        """
        if mod_name not in self.mod_manifests:
            print(f"Мод {mod_name} не найден")
            return False
        
        mod_info = self.mod_manifests[mod_name]
        
        # Проверяем зависимости
        for dependency in mod_info['dependencies']:
            if dependency not in self.active_mods:
                print(f"Мод {mod_name} требует {dependency}, который не активен")
                return False
        
        if mod_name not in self.active_mods:
            self.active_mods.append(mod_name)
            print(f"Мод {mod_name} успешно загружен")
            return True
        
        return False
    
    def unload_mod(self, mod_name):
        """
        Выгружает мод из игры
        
        Args:
            mod_name (str): Название мода для выгрузки
        """
        if mod_name in self.active_mods:
            # Проверяем, не зависят ли другие активные моды от этого
            for active_mod in self.active_mods:
                if active_mod != mod_name and mod_name in self.mod_manifests[active_mod]['dependencies']:
                    print(f"Невозможно выгрузить {mod_name}, так как от него зависит {active_mod}")
                    return False
            
            self.active_mods.remove(mod_name)
            print(f"Мод {mod_name} успешно выгружен")
            return True
        
        return False
    
    def get_mod_dependencies(self, mod_name):
        """
        Возвращает зависимости указанного мода
        
        Args:
            mod_name (str): Название мода
            
        Returns:
            list: Список зависимостей
        """
        if mod_name in self.mod_manifests:
            return self.mod_manifests[mod_name]['dependencies']
        return []
```

</details>

#### Задание 2.2: Система логирования с файловым выводом

Создайте систему логирования с выводом в файлы:

```python
import os
import sys
from datetime import datetime
from pathlib import Path

class GameLogger:
    """
    Система логирования игровых событий
    """
    def __init__(self, log_directory="logs", max_file_size_mb=10):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.max_file_size = max_file_size_mb * 1024 * 1024  # в байтах
        self.current_log_file = self._get_new_log_file()
    
    def _get_new_log_file(self):
        """
        Создает новый файл лога с меткой времени
        
        Returns:
            Path: Путь к новому файлу лога
        """
        # ВАШ КОД ЗДЕСЬ - создайте новый файл лога с меткой времени
        pass  # Замените на ваш код
    
    def _rotate_log_if_needed(self):
        """
        Проверяет, нужно ли создать новый файл лога из-за размера
        """
        # ВАШ КОД ЗДЕСЬ - проверьте размер файла и при необходимости смените файл
        pass  # Замените на ваш код
    
    def log(self, level, message, module="general"):
        """
        Записывает сообщение в лог
        
        Args:
            level (str): Уровень сообщения (INFO, WARNING, ERROR, DEBUG)
            message (str): Текст сообщения
            module (str): Модуль, от которого пришло сообщение
        """
        # ВАШ КОД ЗДЕСЬ - запишите сообщение в лог с форматированием
        pass  # Замените на ваш код
    
    def get_recent_logs(self, hours=1, level_filter=None):
        """
        Возвращает недавние сообщения из лога
        
        Args:
            hours (int): Количество часов назад
            level_filter (str): Фильтр по уровню (опционально)
            
        Returns:
            list: Список недавних сообщений
        """
        # ВАШ КОД ЗДЕСЬ - верните недавние сообщения из лога
        pass  # Замените на ваш код

# Пример использования:
# logger = GameLogger()
# logger.log("INFO", "Игрок вошел в игру", "authentication")
# logger.log("ERROR", "Ошибка загрузки уровня", "level_loader")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import sys
from datetime import datetime
from pathlib import Path

class GameLogger:
    """
    Система логирования игровых событий
    """
    def __init__(self, log_directory="logs", max_file_size_mb=10):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        self.max_file_size = max_file_size_mb * 1024 * 1024  # в байтах
        self.current_log_file = self._get_new_log_file()
    
    def _get_new_log_file(self):
        """
        Создает новый файл лога с меткой времени
        
        Returns:
            Path: Путь к новому файлу лога
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_directory / f"game_log_{timestamp}.txt"
        return log_file
    
    def _rotate_log_if_needed(self):
        """
        Проверяет, нужно ли создать новый файл лога из-за размера
        """
        if self.current_log_file.exists() and self.current_log_file.stat().st_size > self.max_file_size:
            self.current_log_file = self._get_new_log_file()
    
    def log(self, level, message, module="general"):
        """
        Записывает сообщение в лог
        
        Args:
            level (str): Уровень сообщения (INFO, WARNING, ERROR, DEBUG)
            message (str): Текст сообщения
            module (str): Модуль, от которого пришло сообщение
        """
        self._rotate_log_if_needed()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level.upper()}] [{module}] {message}\n"
        
        with open(self.current_log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def get_recent_logs(self, hours=1, level_filter=None):
        """
        Возвращает недавние сообщения из лога
        
        Args:
            hours (int): Количество часов назад
            level_filter (str): Фильтр по уровню (опционально)
            
        Returns:
            list: Список недавних сообщений
        """
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        recent_logs = []
        try:
            with open(self.current_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Парсим строку лога
                    if "] [" in line and "] [" in line.split("] [", 2)[2]:
                        try:
                            parts = line.strip().split("] [", 3)
                            if len(parts) >= 3:
                                timestamp_str = parts[0].strip('[')
                                level = parts[1]
                                module_msg = parts[2]
                                
                                # Извлекаем время из строки
                                log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                                
                                # Проверяем, подходит ли по времени
                                if log_time >= time_threshold:
                                    # Проверяем фильтр по уровню
                                    if level_filter is None or level.upper() == level_filter.upper():
                                        recent_logs.append({
                                            'timestamp': log_time,
                                            'level': level,
                                            'module': module_msg.split('] ')[0],
                                            'message': '] '.join(module_msg.split('] ')[1:])
                                        })
                        except ValueError:
                            continue  # Пропускаем неправильно отформатированные строки
        except FileNotFoundError:
            print(f"Файл лога не найден: {self.current_log_file}")
        
        return recent_logs
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Система обновления игры

Создайте систему обновления игры с проверкой целостности файлов:

```python
import os
import hashlib
import json
from pathlib import Path

class GameUpdater:
    """
    Система обновления игры
    """
    def __init__(self, game_directory=".", manifest_file="file_manifest.json"):
        self.game_directory = Path(game_directory)
        self.manifest_file = Path(manifest_file)
        self.current_manifest = {}
    
    def generate_file_manifest(self, exclude_patterns=None):
        """
        Генерирует манифест файлов игры с хэшами
        
        Args:
            exclude_patterns (list): Паттерны для исключения файлов из манифеста
            
        Returns:
            dict: Словарь с хэшами файлов
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте генерацию манифеста файлов
        pass  # Замените на ваш код
    
    def save_manifest(self, manifest, file_path=None):
        """
        Сохраняет манифест в файл
        
        Args:
            manifest (dict): Манифест для сохранения
            file_path (str): Путь для сохранения (опционально)
        """
        # ВАШ КОД ЗДЕСЬ - сохраните манифест в файл
        pass  # Замените на ваш код
    
    def load_manifest(self, file_path=None):
        """
        Загружает манифест из файла
        
        Args:
            file_path (str): Путь к файлу манифеста (опционально)
            
        Returns:
            dict: Загруженный манифест
        """
        # ВАШ КОД ЗДЕСЬ - загрузите манифест из файла
        pass  # Замените на ваш код
    
    def verify_file_integrity(self, manifest=None):
        """
        Проверяет целостность файлов игры
        
        Args:
            manifest (dict): Манифест для проверки (опционально, использует текущий)
            
        Returns:
            dict: Результаты проверки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте проверку целостности файлов
        pass  # Замените на ваш код
    
    def download_update(self, update_url, temp_directory="temp_updates"):
        """
        Скачивает обновление из указанного источника
        
        Args:
            update_url (str): URL для скачивания обновления
            temp_directory (str): Временный каталог для обновления
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте скачивание обновления
        pass  # Замените на ваш код
    
    def apply_update(self, update_directory):
        """
        Применяет обновление к игре
        
        Args:
            update_directory (str): Каталог с файлами обновления
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте применение обновления
        pass  # Замените на ваш код

# Пример использования:
# updater = GameUpdater()
# manifest = updater.generate_file_manifest()
# updater.save_manifest(manifest)
# verification_results = updater.verify_file_integrity()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import hashlib
import json
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

class GameUpdater:
    """
    Система обновления игры
    """
    def __init__(self, game_directory=".", manifest_file="file_manifest.json"):
        self.game_directory = Path(game_directory)
        self.manifest_file = Path(manifest_file)
        self.current_manifest = {}
        
        # Загружаем текущий манифест, если он существует
        if self.manifest_file.exists():
            self.current_manifest = self.load_manifest()
    
    def generate_file_manifest(self, exclude_patterns=None):
        """
        Генерирует манифест файлов игры с хэшами
        
        Args:
            exclude_patterns (list): Паттерны для исключения файлов из манифеста
            
        Returns:
            dict: Словарь с хэшами файлов
        """
        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', '*.tmp', '*.log', 'temp*', 'cache*']
        
        manifest = {}
        
        for root, dirs, files in os.walk(self.game_directory):
            # Пропускаем каталоги, соответствующие паттернам исключения
            dirs[:] = [d for d in dirs if not any(pattern.lstrip('*') in d or d.startswith(pattern.lstrip('*')) for pattern in exclude_patterns)]
            
            for file in files:
                if not any(pattern.lstrip('*') in file or file.startswith(pattern.lstrip('*')) for pattern in exclude_patterns):
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(self.game_directory)
                    
                    # Вычисляем хэш файла
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    manifest[str(relative_path)] = file_hash
        
        return manifest
    
    def save_manifest(self, manifest, file_path=None):
        """
        Сохраняет манифест в файл
        
        Args:
            manifest (dict): Манифест для сохранения
            file_path (str): Путь для сохранения (опционально)
        """
        if file_path is None:
            file_path = self.manifest_file
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def load_manifest(self, file_path=None):
        """
        Загружает манифест из файла
        
        Args:
            file_path (str): Путь к файлу манифеста (опционально)
            
        Returns:
            dict: Загруженный манифест
        """
        if file_path is None:
            file_path = self.manifest_file
        
        if not file_path.exists():
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def verify_file_integrity(self, manifest=None):
        """
        Проверяет целостность файлов игры
        
        Args:
            manifest (dict): Манифест для проверки (опционально, использует текущий)
            
        Returns:
            dict: Результаты проверки
        """
        if manifest is None:
            manifest = self.current_manifest
        
        results = {
            'valid': [],
            'missing': [],
            'corrupted': [],
            'extra': []
        }
        
        # Проверяем файлы из манифеста
        for file_path, expected_hash in manifest.items():
            full_path = self.game_directory / file_path
            
            if not full_path.exists():
                results['missing'].append(file_path)
            else:
                with open(full_path, 'rb') as f:
                    actual_hash = hashlib.sha256(f.read()).hexdigest()
                
                if actual_hash == expected_hash:
                    results['valid'].append(file_path)
                else:
                    results['corrupted'].append(file_path)
        
        # Проверяем лишние файлы
        current_files = set()
        for root, dirs, files in os.walk(self.game_directory):
            for file in files:
                file_path = Path(root).relative_to(self.game_directory) / file
                current_files.add(str(file_path))
        
        manifest_files = set(manifest.keys())
        results['extra'] = list(current_files - manifest_files)
        
        return results
    
    def download_update(self, update_url, temp_directory="temp_updates"):
        """
        Скачивает обновление из указанного источника
        
        Args:
            update_url (str): URL для скачивания обновления
            temp_directory (str): Временный каталог для обновления
        """
        temp_dir = Path(temp_directory)
        temp_dir.mkdir(exist_ok=True)
        
        # Создаем временный файл для загрузки
        temp_file = temp_dir / "update.zip"
        
        print(f"Загрузка обновления с {update_url}...")
        urllib.request.urlretrieve(update_url, temp_file)
        print("Загрузка завершена.")
        
        # Распаковываем архив
        update_dir = temp_dir / "extracted"
        update_dir.mkdir(exist_ok=True)
        
        with ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(update_dir)
        
        return update_dir
    
    def apply_update(self, update_directory):
        """
        Применяет обновление к игре
        
        Args:
            update_directory (str): Каталог с файлами обновления
        """
        update_path = Path(update_directory)
        
        for root, dirs, files in os.walk(update_path):
            for file in files:
                source_file = Path(root) / file
                relative_path = source_file.relative_to(update_path)
                dest_file = self.game_directory / relative_path
                
                # Создаем каталоги при необходимости
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Копируем файл
                import shutil
                shutil.copy2(source_file, dest_file)
                print(f"Обновлен файл: {relative_path}")
```

</details>

#### Задание 3.2: Система аргументов командной строки для игры

Создайте систему обработки аргументов командной строки для запуска игры:

```python
import sys
import argparse
from pathlib import Path

class GameArgumentParser:
    """
    Система обработки аргументов командной строки для игры
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Игра 'Сказочный Квест'",
            prog="fantasy_quest"
        )
        self._setup_arguments()
        self.args = None
    
    def _setup_arguments(self):
        """
        Настраивает аргументы командной строки
        """
        # ВАШ КОД ЗДЕСЬ - настройте аргументы командной строки
        # Например: --config, --windowed, --debug, --player-name и т.д.
        pass  # Замените на ваш код
    
    def parse_arguments(self, argv=None):
        """
        Парсит аргументы командной строки
        
        Args:
            argv (list): Список аргументов (опционально, по умолчанию sys.argv)
            
        Returns:
            Namespace: Пространство имен с аргументами
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте парсинг аргументов
        pass  # Замените на ваш код
    
    def validate_arguments(self):
        """
        Проверяет корректность аргументов
        
        Returns:
            tuple: (успешно ли, список ошибок)
        """
        # ВАШ КОД ЗДЕСЬ - проверьте корректность аргументов
        pass  # Замените на ваш код
    
    def get_startup_config(self):
        """
        Возвращает конфигурацию запуска на основе аргументов
        
        Returns:
            dict: Словарь с параметрами запуска
        """
        # ВАШ КОД ЗДЕСЬ - верните конфигурацию запуска
        pass  # Замените на ваш код

# Пример использования:
# arg_parser = GameArgumentParser()
# args = arg_parser.parse_arguments()
# startup_config = arg_parser.get_startup_config()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
import argparse
from pathlib import Path

class GameArgumentParser:
    """
    Система обработки аргументов командной строки для игры
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Игра 'Сказочный Квест'",
            prog="fantasy_quest"
        )
        self._setup_arguments()
        self.args = None
    
    def _setup_arguments(self):
        """
        Настраивает аргументы командной строки
        """
        self.parser.add_argument(
            "--config",
            type=str,
            default="default_config.json",
            help="Путь к файлу конфигурации (по умолчанию: default_config.json)"
        )
        
        self.parser.add_argument(
            "--windowed",
            action="store_true",
            help="Запуск в оконном режиме"
        )
        
        self.parser.add_argument(
            "--fullscreen",
            action="store_true",
            help="Запуск в полноэкранном режиме"
        )
        
        self.parser.add_argument(
            "--resolution",
            type=str,
            default="1920x1080",
            help="Разрешение экрана (например, 1920x1080)"
        )
        
        self.parser.add_argument(
            "--debug",
            action="store_true",
            help="Включить режим отладки"
        )
        
        self.parser.add_argument(
            "--player-name",
            type=str,
            default="Игрок",
            help="Имя игрока"
        )
        
        self.parser.add_argument(
            "--language",
            type=str,
            choices=["en", "ru", "es", "fr", "de"],
            default="en",
            help="Язык игры"
        )
        
        self.parser.add_argument(
            "--skip-intro",
            action="store_true",
            help="Пропустить заставку при запуске"
        )
        
        self.parser.add_argument(
            "--data-dir",
            type=str,
            default="./data",
            help="Каталог с игровыми данными"
        )
    
    def parse_arguments(self, argv=None):
        """
        Парсит аргументы командной строки
        
        Args:
            argv (list): Список аргументов (опционально, по умолчанию sys.argv)
            
        Returns:
            Namespace: Пространство имен с аргументами
        """
        if argv is None:
            argv = sys.argv[1:]  # Исключаем имя скрипта
        
        self.args = self.parser.parse_args(argv)
        return self.args
    
    def validate_arguments(self):
        """
        Проверяет корректность аргументов
        
        Returns:
            tuple: (успешно ли, список ошибок)
        """
        errors = []
        
        # Проверяем разрешение
        if self.args.resolution:
            try:
                width, height = map(int, self.args.resolution.split('x'))
                if width < 800 or height < 600:
                    errors.append(f"Слишком маленькое разрешение: {width}x{height} (минимум 800x600)")
                if width > 7680 or height > 4320:
                    errors.append(f"Слишком большое разрешение: {width}x{height} (максимум 7680x4320)")
            except ValueError:
                errors.append(f"Некорректный формат разрешения: {self.args.resolution} (ожидается ШИРИНАxВЫСОТА)")
        
        # Проверяем каталог с данными
        if not Path(self.args.data_dir).exists():
            errors.append(f"Каталог с данными не существует: {self.args.data_dir}")
        
        # Проверяем конфигурационный файл
        if not Path(self.args.config).exists():
            errors.append(f"Файл конфигурации не существует: {self.args.config}")
        
        return len(errors) == 0, errors
    
    def get_startup_config(self):
        """
        Возвращает конфигурацию запуска на основе аргументов
        
        Returns:
            dict: Словарь с параметрами запуска
        """
        if self.args is None:
            self.args = self.parse_arguments()
        
        # Разбор разрешения
        resolution = (1920, 1080)  # Значение по умолчанию
        if self.args.resolution:
            try:
                width, height = map(int, self.args.resolution.split('x'))
                resolution = (width, height)
            except ValueError:
                pass  # Используем значение по умолчанию
        
        return {
            'config_file': self.args.config,
            'windowed_mode': self.args.windowed or (not self.args.fullscreen),
            'fullscreen_mode': self.args.fullscreen,
            'resolution': resolution,
            'debug_mode': self.args.debug,
            'player_name': self.args.player_name,
            'language': self.args.language,
            'skip_intro': self.args.skip_intro,
            'data_directory': Path(self.args.data_dir).resolve()
        }
```

</details>

---

## 2. Практические задания в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.3: Система сохранения игры

Создайте систему сохранения игры с использованием модуля os:

```python
import os
import json
from datetime import datetime
from pathlib import Path

class GameSaveManager:
    """
    Система управления сохранениями игры
    """
    def __init__(self, saves_directory="saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
    
    def create_save(self, save_name, game_state):
        """
        Создает новое сохранение игры
        
        Args:
            save_name (str): Имя сохранения
            game_state (dict): Состояние игры для сохранения
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте создание сохранения
        pass  # Замените на ваш код
    
    def load_save(self, save_name):
        """
        Загружает сохранение игры
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            dict: Состояние игры или None, если сохранение не найдено
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте загрузку сохранения
        pass  # Замените на ваш код
    
    def list_saves(self):
        """
        Возвращает список доступных сохранений
        
        Returns:
            list: Список имен сохранений
        """
        # ВАШ КОД ЗДЕСЬ - верните список сохранений
        pass  # Замените на ваш код
    
    def delete_save(self, save_name):
        """
        Удаляет сохранение игры
        
        Args:
            save_name (str): Имя сохранения для удаления
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте удаление сохранения
        pass  # Замените на ваш код

# Пример использования:
# save_manager = GameSaveManager()
# save_manager.create_save("quick_save", {"level": 5, "health": 80, "position": [100, 200]})
# saves = save_manager.list_saves()
# game_state = save_manager.load_save("quick_save")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import json
from datetime import datetime
from pathlib import Path

class GameSaveManager:
    """
    Система управления сохранениями игры
    """
    def __init__(self, saves_directory="saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
    
    def create_save(self, save_name, game_state):
        """
        Создает новое сохранение игры
        
        Args:
            save_name (str): Имя сохранения
            game_state (dict): Состояние игры для сохранения
        """
        # Добавляем метаданные к состоянию игры
        save_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'save_name': save_name,
                'game_version': '1.0.0'
            },
            'game_state': game_state
        }
        
        save_file = self.saves_directory / f"{save_name}.json"
        with open(save_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
    
    def load_save(self, save_name):
        """
        Загружает сохранение игры
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            dict: Состояние игры или None, если сохранение не найдено
        """
        save_file = self.saves_directory / f"{save_name}.json"
        if not save_file.exists():
            return None
        
        with open(save_file, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        return save_data.get('game_state', {})
    
    def list_saves(self):
        """
        Возвращает список доступных сохранений
        
        Returns:
            list: Список имен сохранений
        """
        saves = []
        for file in self.saves_directory.glob("*.json"):
            save_name = file.stem  # Имя файла без расширения
            saves.append(save_name)
        return sorted(saves, reverse=True)  # Сортируем в обратном порядке (новые первыми)
    
    def delete_save(self, save_name):
        """
        Удаляет сохранение игры
        
        Args:
            save_name (str): Имя сохранения для удаления
        """
        save_file = self.saves_directory / f"{save_name}.json"
        if save_file.exists():
            save_file.unlink()  # Удаляем файл
            return True
        return False
```

</details>

#### Задание 1.4: Система скриншотов

Создайте систему для создания и управления игровыми скриншотами:

```python
import os
from pathlib import Path
from datetime import datetime

class ScreenshotManager:
    """
    Система управления скриншотами
    """
    def __init__(self, screenshots_directory="screenshots"):
        self.screenshots_directory = Path(screenshots_directory)
        self.screenshots_directory.mkdir(exist_ok=True)
    
    def save_screenshot(self, image_data, custom_name=None):
        """
        Сохраняет скриншот
        
        Args:
            image_data (bytes): Данные изображения
            custom_name (str): Пользовательское имя файла (опционально)
            
        Returns:
            str: Имя сохраненного файла
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте сохранение скриншота
        pass  # Замените на ваш код
    
    def get_screenshot_info(self, screenshot_name):
        """
        Возвращает информацию о скриншоте
        
        Args:
            screenshot_name (str): Имя файла скриншота
            
        Returns:
            dict: Информация о скриншоте
        """
        # ВАШ КОД ЗДЕСЬ - верните информацию о скриншоте
        pass  # Замените на ваш код
    
    def get_recent_screenshots(self, count=10):
        """
        Возвращает последние скриншоты
        
        Args:
            count (int): Количество скриншотов для возврата
            
        Returns:
            list: Список последних скриншотов
        """
        # ВАШ КОД ЗДЕСЬ - верните последние скриншоты
        pass  # Замените на ваш код
    
    def cleanup_old_screenshots(self, days_to_keep=30):
        """
        Удаляет старые скриншоты
        
        Args:
            days_to_keep (int): Количество дней хранения
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте очистку старых скриншотов
        pass  # Замените на ваш код

# Пример использования:
# screenshot_manager = ScreenshotManager()
# screenshot_name = screenshot_manager.save_screenshot(b"image_bytes", "victory_moment")
# recent_screenshots = screenshot_manager.get_recent_screenshots(5)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
from pathlib import Path
from datetime import datetime, timedelta

class ScreenshotManager:
    """
    Система управления скриншотами
    """
    def __init__(self, screenshots_directory="screenshots"):
        self.screenshots_directory = Path(screenshots_directory)
        self.screenshots_directory.mkdir(exist_ok=True)
    
    def save_screenshot(self, image_data, custom_name=None):
        """
        Сохраняет скриншот
        
        Args:
            image_data (bytes): Данные изображения
            custom_name (str): Пользовательское имя файла (опционально)
            
        Returns:
            str: Имя сохраненного файла
        """
        if custom_name:
            filename = f"{custom_name}.png"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screenshot_{timestamp}.png"
        
        filepath = self.screenshots_directory / filename
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filename
    
    def get_screenshot_info(self, screenshot_name):
        """
        Возвращает информацию о скриншоте
        
        Args:
            screenshot_name (str): Имя файла скриншота
            
        Returns:
            dict: Информация о скриншоте
        """
        filepath = self.screenshots_directory / screenshot_name
        if not filepath.exists():
            return None
        
        stat = filepath.stat()
        return {
            'name': screenshot_name,
            'size': stat.st_size,
            'created_at': datetime.fromtimestamp(stat.st_ctime),
            'modified_at': datetime.fromtimestamp(stat.st_mtime),
            'full_path': str(filepath.absolute())
        }
    
    def get_recent_screenshots(self, count=10):
        """
        Возвращает последние скриншоты
        
        Args:
            count (int): Количество скриншотов для возврата
            
        Returns:
            list: Список последних скриншотов
        """
        screenshots = []
        for file in self.screenshots_directory.glob("*.png"):
            stat = file.stat()
            screenshots.append({
                'name': file.name,
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime),
                'full_path': str(file.absolute())
            })
        
        # Сортируем по времени создания (новые первыми)
        screenshots.sort(key=lambda x: x['created_at'], reverse=True)
        return screenshots[:count]
    
    def cleanup_old_screenshots(self, days_to_keep=30):
        """
        Удаляет старые скриншоты
        
        Args:
            days_to_keep (int): Количество дней хранения
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        deleted_count = 0
        for file in self.screenshots_directory.glob("*.png"):
            stat = file.stat()
            file_date = datetime.fromtimestamp(stat.st_ctime)
            
            if file_date < cutoff_date:
                file.unlink()
                deleted_count += 1
        
        return deleted_count
```

</details>

### Уровень 2 - Средний

#### Задание 2.3: Система модулей игры

Создайте систему динамической загрузки игровых модулей:

```python
import os
import sys
import importlib
from pathlib import Path

class ModuleLoader:
    """
    Система загрузки игровых модулей
    """
    def __init__(self, modules_directory="modules"):
        self.modules_directory = Path(modules_directory)
        self.loaded_modules = {}
        self.module_metadata = {}
    
    def scan_modules(self):
        """
        Сканирует каталог на наличие модулей
        
        Returns:
            list: Список найденных модулей
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте сканирование модулей
        pass  # Замените на ваш код
    
    def load_module(self, module_name):
        """
        Загружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для загрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте загрузку модуля
        pass  # Замените на ваш код
    
    def unload_module(self, module_name):
        """
        Выгружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для выгрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте выгрузку модуля
        pass  # Замените на ваш код
    
    def reload_module(self, module_name):
        """
        Перезагружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для перезагрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте перезагрузку модуля
        pass  # Замените на ваш код

# Пример использования:
# loader = ModuleLoader()
# available_modules = loader.scan_modules()
# loader.load_module("combat_system")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import sys
import importlib
import importlib.util
from pathlib import Path

class ModuleLoader:
    """
    Система загрузки игровых модулей
    """
    def __init__(self, modules_directory="modules"):
        self.modules_directory = Path(modules_directory)
        self.loaded_modules = {}
        self.module_metadata = {}
    
    def scan_modules(self):
        """
        Сканирует каталог на наличие модулей
        
        Returns:
            list: Список найденных модулей
        """
        modules = []
        
        # Добавляем каталог модулей в sys.path, если его там нет
        modules_path = str(self.modules_directory.absolute())
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        for file in self.modules_directory.glob("*.py"):
            if file.name != "__init__.py":  # Пропускаем __init__.py
                module_name = file.stem  # Имя файла без расширения
                modules.append(module_name)
        
        return modules
    
    def load_module(self, module_name):
        """
        Загружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для загрузки
        """
        module_path = self.modules_directory / f"{module_name}.py"
        if not module_path.exists():
            print(f"Модуль {module_name} не найден по пути: {module_path}")
            return None
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            
            # Выполняем модуль
            spec.loader.exec_module(module)
            
            # Сохраняем ссылку на модуль
            self.loaded_modules[module_name] = module
            
            # Получаем метаданные модуля, если они есть
            metadata = {
                'name': module_name,
                'path': str(module_path.absolute()),
                'loaded_at': datetime.now(),
                'functions': [name for name in dir(module) if callable(getattr(module, name)) and not name.startswith('_')],
                'classes': [name for name in dir(module) if isinstance(getattr(module, name), type) and not name.startswith('_')]
            }
            self.module_metadata[module_name] = metadata
            
            print(f"Модуль {module_name} успешно загружен")
            return module
        except Exception as e:
            print(f"Ошибка загрузки модуля {module_name}: {e}")
            return None
    
    def unload_module(self, module_name):
        """
        Выгружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для выгрузки
        """
        if module_name in self.loaded_modules:
            # Удаляем модуль из кэша импорта
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            # Удаляем ссылки на модуль
            del self.loaded_modules[module_name]
            if module_name in self.module_metadata:
                del self.module_metadata[module_name]
            
            print(f"Модуль {module_name} успешно выгружен")
            return True
        
        return False
    
    def reload_module(self, module_name):
        """
        Перезагружает указанный модуль
        
        Args:
            module_name (str): Имя модуля для перезагрузки
        """
        # Сначала выгружаем модуль
        self.unload_module(module_name)
        
        # Затем загружаем заново
        return self.load_module(module_name)
```

</details>

#### Задание 2.4: Система производительности игры

Создайте систему мониторинга производительности игры:

```python
import os
import psutil
import time
from datetime import datetime

class PerformanceMonitor:
    """
    Система мониторинга производительности игры
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.metrics_history = []
    
    def get_current_metrics(self):
        """
        Возвращает текущие метрики производительности
        
        Returns:
            dict: Словарь с метриками
        """
        # ВАШ КОД ЗДЕСЬ - получите текущие метрики
        pass  # Замените на ваш код
    
    def start_monitoring(self, interval=1.0):
        """
        Начинает мониторинг производительности
        
        Args:
            interval (float): Интервал между измерениями в секундах
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте постоянный мониторинг
        pass  # Замените на ваш код
    
    def stop_monitoring(self):
        """
        Останавливает мониторинг производительности
        """
        # ВАШ КОД ЗДЕСЬ - остановите мониторинг
        pass  # Замените на ваш код
    
    def get_performance_report(self, minutes_back=5):
        """
        Возвращает отчет о производительности за последние минуты
        
        Args:
            minutes_back (int): Количество минут для анализа
            
        Returns:
            dict: Отчет о производительности
        """
        # ВАШ КОД ЗДЕСЬ - сгенерируйте отчет о производительности
        pass  # Замените на ваш код

# Пример использования:
# perf_monitor = PerformanceMonitor()
# current_metrics = perf_monitor.get_current_metrics()
# perf_monitor.start_monitoring(0.5)  # Мониторинг каждые 0.5 секунды
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import psutil
import time
from datetime import datetime, timedelta

class PerformanceMonitor:
    """
    Система мониторинга производительности игры
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.metrics_history = []
        self.monitoring = False
        self.monitor_thread = None
    
    def get_current_metrics(self):
        """
        Возвращает текущие метрики производительности
        
        Returns:
            dict: Словарь с метриками
        """
        cpu_percent = self.process.cpu_percent()
        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()
        disk_io = self.process.io_counters() if hasattr(self.process, 'io_counters') else None
        network_io = psutil.net_io_counters()
        
        metrics = {
            'timestamp': datetime.now(),
            'cpu_percent': cpu_percent,
            'memory_rss': memory_info.rss,  # Resident Set Size
            'memory_vms': memory_info.vms,  # Virtual Memory Size
            'memory_percent': memory_percent,
            'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
            'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
            'network_bytes_sent': network_io.bytes_sent,
            'network_bytes_recv': network_io.bytes_recv
        }
        
        return metrics
    
    def start_monitoring(self, interval=1.0):
        """
        Начинает мониторинг производительности
        
        Args:
            interval (float): Интервал между измерениями в секундах
        """
        import threading
        
        def monitoring_loop():
            while self.monitoring:
                metrics = self.get_current_metrics()
                self.metrics_history.append(metrics)
                
                # Ограничиваем историю последними 1000 измерениями
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                time.sleep(interval)
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """
        Останавливает мониторинг производительности
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)  # Ждем завершения потока
    
    def get_performance_report(self, minutes_back=5):
        """
        Возвращает отчет о производительности за последние минуты
        
        Args:
            minutes_back (int): Количество минут для анализа
            
        Returns:
            dict: Отчет о производительности
        """
        cutoff_time = datetime.now() - timedelta(minutes=minutes_back)
        recent_metrics = [m for m in self.metrics_history if m['timestamp'] >= cutoff_time]
        
        if not recent_metrics:
            return {"error": "Нет данных за указанный период"}
        
        # Вычисляем средние значения
        avg_cpu = sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
        avg_memory_percent = sum(m['memory_percent'] for m in recent_metrics) / len(recent_metrics)
        max_memory_rss = max(m['memory_rss'] for m in recent_metrics)
        
        # Находим пики
        peak_cpu = max(m['cpu_percent'] for m in recent_metrics)
        peak_memory_percent = max(m['memory_percent'] for m in recent_metrics)
        
        report = {
            'period_minutes': minutes_back,
            'sample_count': len(recent_metrics),
            'average_cpu_percent': round(avg_cpu, 2),
            'average_memory_percent': round(avg_memory_percent, 2),
            'peak_cpu_percent': peak_cpu,
            'peak_memory_percent': peak_memory_percent,
            'max_memory_usage_bytes': max_memory_rss,
            'trend_cpu': 'increasing' if len(recent_metrics) > 1 and recent_metrics[-1]['cpu_percent'] > recent_metrics[0]['cpu_percent'] else 'decreasing',
            'trend_memory': 'increasing' if len(recent_metrics) > 1 and recent_metrics[-1]['memory_percent'] > recent_metrics[0]['memory_percent'] else 'decreasing'
        }
        
        return report
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.3: Система инсталлятора игры

Создайте систему инсталляции игры с проверкой зависимостей:

```python
import os
import sys
import subprocess
from pathlib import Path

class GameInstaller:
    """
    Система инсталляции игры
    """
    def __init__(self, installer_directory="installer"):
        self.installer_directory = Path(installer_directory)
        self.install_path = None
        self.dependencies = []
    
    def check_system_requirements(self):
        """
        Проверяет системные требования
        
        Returns:
            dict: Результаты проверки системных требований
        """
        # ВАШ КОД ЗДЕСЬ - проверьте системные требования
        pass  # Замените на ваш код
    
    def select_install_path(self, suggested_path=None):
        """
        Выбирает путь для установки игры
        
        Args:
            suggested_path (str): Предлагаемый путь для установки
            
        Returns:
            str: Выбранный путь для установки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте выбор пути установки
        pass  # Замените на ваш код
    
    def install_dependencies(self):
        """
        Устанавливает зависимости игры
        
        Returns:
            bool: Успешно ли установлены зависимости
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте установку зависимостей
        pass  # Замените на ваш код
    
    def install_game_files(self):
        """
        Устанавливает игровые файлы
        
        Returns:
            bool: Успешно ли установлены файлы
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте установку файлов
        pass  # Замените на ваш код
    
    def create_shortcuts(self):
        """
        Создает ярлыки для запуска игры
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте создание ярлыков
        pass  # Замените на ваш код
    
    def run_post_install_script(self):
        """
        Выполняет пост-установочный скрипт
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте выполнение пост-установочного скрипта
        pass  # Замените на ваш код

# Пример использования:
# installer = GameInstaller()
# requirements_ok = installer.check_system_requirements()
# install_path = installer.select_install_path("C:/Games/FantasyQuest")
# deps_ok = installer.install_dependencies()
# files_ok = installer.install_game_files()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path

class GameInstaller:
    """
    Система инсталляции игры
    """
    def __init__(self, installer_directory="installer"):
        self.installer_directory = Path(installer_directory)
        self.install_path = None
        self.dependencies = [
            {"name": "Python", "version": "3.8", "required": True},
            {"name": "Pygame", "version": "2.0", "required": True},
            {"name": "NumPy", "version": "1.19", "required": True},
            {"name": "Pillow", "version": "8.0", "required": False}
        ]
    
    def check_system_requirements(self):
        """
        Проверяет системные требования
        
        Returns:
            dict: Результаты проверки системных требований
        """
        results = {
            'os_compatible': True,
            'python_version': sys.version_info[:2],
            'disk_space_available': 0,
            'dependencies_met': [],
            'issues': []
        }
        
        # Проверяем ОС
        current_os = platform.system().lower()
        if current_os not in ['windows', 'linux', 'darwin']:
            results['os_compatible'] = False
            results['issues'].append(f"ОС {current_os} не поддерживается")
        
        # Проверяем место на диске (минимум 5 ГБ)
        if hasattr(shutil, 'disk_usage'):
            disk_usage = shutil.disk_usage(self.installer_directory.anchor)
            available_gb = disk_usage.free / (1024**3)
            results['disk_space_available'] = available_gb
            if available_gb < 5:
                results['issues'].append(f"Недостаточно места на диске: доступно {available_gb:.1f} ГБ, требуется 5 ГБ")
        
        # Проверяем зависимости
        for dep in self.dependencies:
            try:
                if dep['name'] == 'Python':
                    # Уже проверили версию выше
                    if sys.version_info[:2] >= tuple(map(int, dep['version'].split('.'))):
                        results['dependencies_met'].append(dep['name'])
                    else:
                        if dep['required']:
                            results['issues'].append(f"Требуется Python {dep['version']} или выше")
                else:
                    # Проверяем установленную библиотеку
                    import importlib
                    module = importlib.import_module(dep['name'].lower())
                    if hasattr(module, '__version__'):
                        installed_version = tuple(map(int, module.__version__.split('.')[:2]))
                        required_version = tuple(map(int, dep['version'].split('.')))
                        if installed_version >= required_version:
                            results['dependencies_met'].append(dep['name'])
                        else:
                            if dep['required']:
                                results['issues'].append(f"Требуется {dep['name']} {dep['version']} или выше, установлена {module.__version__}")
                    else:
                        results['dependencies_met'].append(dep['name'])
            except ImportError:
                if dep['required']:
                    results['issues'].append(f"Требуемая зависимость {dep['name']} не установлена")
        
        return results
    
    def select_install_path(self, suggested_path=None):
        """
        Выбирает путь для установки игры
        
        Args:
            suggested_path (str): Предлагаемый путь для установки
            
        Returns:
            str: Выбранный путь для установки
        """
        if suggested_path:
            install_dir = Path(suggested_path)
        else:
            # Используем стандартную директорию
            if platform.system() == "Windows":
                base_dir = Path.home() / "AppData" / "Local"
            else:
                base_dir = Path.home() / ".local" / "games"
            
            install_dir = base_dir / "FantasyQuest"
        
        # Создаем директорию, если не существует
        install_dir.mkdir(parents=True, exist_ok=True)
        self.install_path = install_dir.resolve()
        return str(self.install_path)
    
    def install_dependencies(self):
        """
        Устанавливает зависимости игры
        
        Returns:
            bool: Успешно ли установлены зависимости
        """
        required_deps = [dep for dep in self.dependencies if dep['required']]
        missing_deps = []
        
        for dep in required_deps:
            try:
                import importlib
                importlib.import_module(dep['name'].lower())
            except ImportError:
                missing_deps.append(f"{dep['name']}>={dep['version']}")
        
        if missing_deps:
            print(f"Устанавливаю зависимости: {', '.join(missing_deps)}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_deps)
                print("Зависимости успешно установлены")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Ошибка установки зависимостей: {e}")
                return False
        else:
            print("Все зависимости уже установлены")
            return True
    
    def install_game_files(self):
        """
        Устанавливает игровые файлы
        
        Returns:
            bool: Успешно ли установлены файлы
        """
        if not self.install_path:
            print("Путь установки не выбран")
            return False
        
        try:
            # Копируем игровые файлы из директории инсталлятора в директорию установки
            source_dir = self.installer_directory
            dest_dir = self.install_path
            
            # Убедимся, что копируем только игровые файлы, а не весь инсталлятор
            for item in source_dir.iterdir():
                if item.name not in ['.git', '__pycache__', 'installer.py', 'install.log']:
                    dest_item = dest_dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest_item, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest_item)
            
            print(f"Игровые файлы установлены в {self.install_path}")
            return True
        except Exception as e:
            print(f"Ошибка установки файлов: {e}")
            return False
    
    def create_shortcuts(self):
        """
        Создает ярлыки для запуска игры
        """
        if not self.install_path:
            return False
        
        try:
            # Создаем ярлык для запуска игры
            launcher_script = self.install_path / "launch_game.py"
            with open(launcher_script, 'w', encoding='utf-8') as f:
                f.write(f'''#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Запуск основного модуля игры
if __name__ == "__main__":
    try:
        import main  # Предполагаем, что основной файл игры называется main.py
        main.run()
    except ImportError:
        print("Ошибка: не найден основной модуль игры")
        input("Нажмите Enter для выхода...")
''')
            
            # Делаем скрипт исполняемым (на Unix-подобных системах)
            if platform.system() != "Windows":
                os.chmod(launcher_script, 0o755)
            
            print(f"Ярлык запуска создан: {launcher_script}")
            return True
        except Exception as e:
            print(f"Ошибка создания ярлыка: {e}")
            return False
    
    def run_post_install_script(self):
        """
        Выполняет пост-установочный скрипт
        """
        post_install_script = self.install_path / "post_install.py"
        
        if post_install_script.exists():
            try:
                # Выполняем пост-установочный скрипт
                result = subprocess.run([sys.executable, str(post_install_script)], 
                                      cwd=self.install_path, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("Пост-установочный скрипт успешно выполнен")
                    return True
                else:
                    print(f"Ошибка выполнения пост-установочного скрипта: {result.stderr}")
                    return False
            except Exception as e:
                print(f"Ошибка запуска пост-установочного скрипта: {e}")
                return False
        else:
            print("Пост-установочный скрипт не найден")
            return True  # Не ошибка, просто нет скрипта
```

</details>

#### Задание 3.4: Комплексная система управления игровыми ресурсами

Создайте комплексную систему управления всеми игровыми ресурсами:

```python
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

class ResourceManager:
    """
    Комплексная система управления игровыми ресурсами
    """
    def __init__(self, game_directory=".", config_file="config.json"):
        self.game_directory = Path(game_directory)
        self.config_file = Path(config_file)
        self.resource_cache = {}
        self.resource_manifest = {}
        
        # Загружаем конфигурацию
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Загружает конфигурацию системы ресурсов
        
        Returns:
            dict: Конфигурация
        """
        # ВАШ КОД ЗДЕСЬ - загрузите конфигурацию из файла
        pass  # Замените на ваш код
    
    def build_resource_manifest(self):
        """
        Строит манифест всех игровых ресурсов
        
        Returns:
            dict: Манифест ресурсов
        """
        # ВАШ КОД ЗДЕСЬ - постройте манифест ресурсов
        pass  # Замените на ваш код
    
    def cache_resource(self, resource_path):
        """
        Кэширует ресурс в памяти
        
        Args:
            resource_path (str): Путь к ресурсу
            
        Returns:
            bytes: Данные ресурса
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте кэширование ресурса
        pass  # Замените на ваш код
    
    def get_resource_path(self, resource_type, resource_name):
        """
        Возвращает путь к ресурсу определенного типа
        
        Args:
            resource_type (str): Тип ресурса (models, textures, sounds, etc.)
            resource_name (str): Имя ресурса
            
        Returns:
            Path: Путь к ресурсу
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте получение пути к ресурсу
        pass  # Замените на ваш код
    
    def preload_resources(self, resource_list):
        """
        Предзагружает указанные ресурсы в кэш
        
        Args:
            resource_list (list): Список ресурсов для предзагрузки
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте предзагрузку ресурсов
        pass  # Замените на ваш код
    
    def cleanup_cache(self, max_size_mb=100):
        """
        Очищает кэш, если он превышает максимальный размер
        
        Args:
            max_size_mb (int): Максимальный размер кэша в МБ
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте очистку кэша
        pass  # Замените на ваш код

# Пример использования:
# resource_manager = ResourceManager()
# manifest = resource_manager.build_resource_manifest()
# resource_manager.preload_resources([("textures", "background.png"), ("sounds", "battle.mp3")])
# texture_data = resource_manager.cache_resource("assets/textures/background.png")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

class ResourceManager:
    """
    Комплексная система управления игровыми ресурсами
    """
    def __init__(self, game_directory=".", config_file="config.json"):
        self.game_directory = Path(game_directory)
        self.config_file = Path(config_file)
        self.resource_cache = {}  # Кэш ресурсов в памяти
        self.resource_manifest = {}  # Манифест всех ресурсов
        self.cache_size = 0  # Текущий размер кэша в байтах
        self.max_cache_size = 100 * 1024 * 1024  # 100 МБ по умолчанию
        
        # Загружаем конфигурацию
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Загружает конфигурацию системы ресурсов
        
        Returns:
            dict: Конфигурация
        """
        default_config = {
            "asset_directories": {
                "models": "assets/models",
                "textures": "assets/textures", 
                "sounds": "assets/sounds",
                "music": "assets/music",
                "shaders": "assets/shaders"
            },
            "cache_max_size_mb": 100,
            "preload_resources": []
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Объединяем с настройками по умолчанию
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except json.JSONDecodeError:
                print(f"Ошибка чтения конфигурации, используется значение по умолчанию")
                return default_config
        else:
            # Создаем файл конфигурации со значениями по умолчанию
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config
    
    def build_resource_manifest(self):
        """
        Строит манифест всех игровых ресурсов
        
        Returns:
            dict: Манифест ресурсов
        """
        manifest = {}
        
        for resource_type, resource_dir in self.config['asset_directories'].items():
            dir_path = self.game_directory / resource_dir
            if dir_path.exists():
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = Path(root) / file
                        relative_path = file_path.relative_to(self.game_directory)
                        
                        # Вычисляем хэш файла
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.sha256(f.read()).hexdigest()
                        
                        # Получаем информацию о файле
                        stat = file_path.stat()
                        
                        manifest[str(relative_path)] = {
                            'type': resource_type,
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'hash': file_hash,
                            'full_path': str(file_path.absolute())
                        }
        
        self.resource_manifest = manifest
        return manifest
    
    def cache_resource(self, resource_path):
        """
        Кэширует ресурс в памяти
        
        Args:
            resource_path (str): Путь к ресурсу
            
        Returns:
            bytes: Данные ресурса
        """
        resource_path = Path(resource_path)
        full_path = self.game_directory / resource_path
        
        if str(resource_path) in self.resource_cache:
            # Ресурс уже в кэше
            return self.resource_cache[str(resource_path)]
        
        if not full_path.exists():
            raise FileNotFoundError(f"Ресурс не найден: {full_path}")
        
        # Проверяем, не превысит ли кэш максимальный размер
        file_size = full_path.stat().st_size
        if (self.cache_size + file_size) > self.max_cache_size:
            # Очищаем кэш, если он слишком большой
            self.cleanup_cache()
        
        with open(full_path, 'rb') as f:
            data = f.read()
        
        # Добавляем в кэш
        self.resource_cache[str(resource_path)] = data
        self.cache_size += len(data)
        
        return data
    
    def get_resource_path(self, resource_type, resource_name):
        """
        Возвращает путь к ресурсу определенного типа
        
        Args:
            resource_type (str): Тип ресурса (models, textures, sounds, etc.)
            resource_name (str): Имя ресурса
            
        Returns:
            Path: Путь к ресурсу
        """
        if resource_type in self.config['asset_directories']:
            base_dir = self.config['asset_directories'][resource_type]
            return self.game_directory / base_dir / resource_name
        else:
            raise ValueError(f"Неизвестный тип ресурса: {resource_type}")
    
    def preload_resources(self, resource_list):
        """
        Предзагружает указанные ресурсы в кэш
        
        Args:
            resource_list (list): Список ресурсов для предзагрузки в формате (тип, имя)
        """
        for resource_type, resource_name in resource_list:
            try:
                resource_path = self.get_resource_path(resource_type, resource_name)
                relative_path = resource_path.relative_to(self.game_directory)
                self.cache_resource(relative_path)
                print(f"Предзагружен ресурс: {resource_type}/{resource_name}")
            except Exception as e:
                print(f"Ошибка предзагрузки ресурса {resource_type}/{resource_name}: {e}")
    
    def cleanup_cache(self, max_size_mb=None):
        """
        Очищает кэш, если он превышает максимальный размер
        
        Args:
            max_size_mb (int): Максимальный размер кэша в МБ (опционально)
        """
        if max_size_mb is None:
            max_size = self.max_cache_size
        else:
            max_size = max_size_mb * 1024 * 1024
        
        # Простая стратегия очистки: удаляем половину самых старых элементов
        if self.cache_size > max_size:
            # Сортируем ключи по времени последнего обращения (в реальной системе нужно отслеживать это)
            items_to_remove = len(self.resource_cache) // 2
            keys_to_remove = list(self.resource_cache.keys())[:items_to_remove]
            
            for key in keys_to_remove:
                data = self.resource_cache.pop(key, None)
                if data:
                    self.cache_size -= len(data)
            
            print(f"Кэш очищен: удалено {len(keys_to_remove)} элементов")
```

</details>

---

## 3. Дополнительные задания

### Задание 4: Система архивации игровых данных

Реализуйте систему архивации игровых данных:
1. Создайте систему архивации сохранений и других игровых данных
2. Реализуйте сжатие данных с различными алгоритмами
3. Добавьте возможность шифрования архивов

### Задание 5: Система обновления ресурсов

Разработайте систему динамического обновления игровых ресурсов:
1. Создайте систему проверки обновлений ресурсов
2. Реализуйте фоновую загрузку обновлений
3. Добавьте возможность горячей замены ресурсов без перезапуска игры

---

## Контрольные вопросы:
1. Какие основные функции предоставляет модуль os для работы с файловой системой?
2. Как использовать модуль sys для получения информации о системе и аргументах?
3. Как работать с путями в разных операционных системах?
4. Какие возможности дает библиотека pathlib для работы с файловыми путями?
5. Какие игровые системы наиболее эффективно использовать с модулями os и sys?