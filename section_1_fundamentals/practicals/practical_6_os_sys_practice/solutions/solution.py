# Решения для практического задания 6: Работа с модулями os и sys в игровом контексте

# Ниже приведены полные реализации игровых систем с использованием модулей os и sys согласно заданию


import os
import sys
from pathlib import Path
import shutil
from datetime import datetime, timedelta, date
import json
import hashlib
import pytz
import psutil
from collections import deque
import random


# Задание 1.1: Создание менеджера игровых файлов
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


# Задание 1.2: Система конфигурации через переменные окружения
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


# Задание 2.1: Система управления модами
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
        Сканирует каталог на наличие модов
        
        Returns:
            list: Список найденных модов
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
        Загружает указанный мод
        
        Args:
            mod_name (str): Имя мода для загрузки
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
        Выгружает указанный мод
        
        Args:
            mod_name (str): Имя мода для выгрузки
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


# Задание 2.2: Система логирования с файловым выводом
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


# Задание 2.3: Система кулдаунов для способностей
class CooldownManager:
    """
    Система управления кулдаунами способностей
    """
    def __init__(self):
        self.cooldowns = {}  # Словарь для хранения времени последнего использования способности
    
    def use_ability(self, player_id, ability_name, cooldown_seconds):
        """
        Попытка использования способности
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            cooldown_seconds (int): Время кулдауна в секундах
            
        Returns:
            tuple: (успешно ли использовано, время до готовности)
        """
        key = (player_id, ability_name)
        current_time = datetime.now()
        
        if key in self.cooldowns:
            last_used = self.cooldowns[key]
            time_passed = current_time - last_used
            cooldown_period = timedelta(seconds=cooldown_seconds)
            
            if time_passed < cooldown_period:
                remaining = cooldown_period - time_passed
                return False, remaining
            else:
                self.cooldowns[key] = current_time
                return True, timedelta(0)
        else:
            self.cooldowns[key] = current_time
            return True, timedelta(0)
    
    def get_remaining_cooldown(self, player_id, ability_name):
        """
        Возвращает оставшееся время до готовности способности
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            
        Returns:
            timedelta: Оставшееся время до готовности
        """
        key = (player_id, ability_name)
        if key not in self.cooldowns:
            return timedelta(0)
        
        last_used = self.cooldowns[key]
        cooldown_period = timedelta(seconds=30)  # Временно фиксированное значение
        time_passed = datetime.now() - last_used
        
        if time_passed < cooldown_period:
            return cooldown_period - time_passed
        else:
            return timedelta(0)
    
    def is_ready(self, player_id, ability_name):
        """
        Проверяет, готова ли способность к использованию
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            
        Returns:
            bool: Готова ли способность
        """
        remaining = self.get_remaining_cooldown(player_id, ability_name)
        return remaining == timedelta(0)


# Задание 3.1: Система ежедневных заданий
class DailyQuestSystem:
    """
    Система ежедневных заданий
    """
    def __init__(self):
        self.daily_quests = {}
        self.player_progress = {}
        self.last_refresh_date = date.today()
        # Возможные задания
        self.quest_templates = [
            {"id": "kill_5_monsters", "name": "Победить 5 монстров", "target": 5, "reward": 100},
            {"id": "collect_10_items", "name": "Собрать 10 предметов", "target": 10, "reward": 150},
            {"id": "visit_3_locations", "name": "Посетить 3 локации", "target": 3, "reward": 200},
            {"id": "complete_1_quest", "name": "Выполнить 1 задание", "target": 1, "reward": 50},
            {"id": "win_3_battles", "name": "Выиграть 3 битвы", "target": 3, "reward": 180}
        ]
    
    def refresh_daily_quests(self):
        """
        Обновляет список ежедневных заданий
        """
        current_date = date.today()
        if current_date > self.last_refresh_date:
            # Создаем новые задания на сегодня
            selected_quests = random.sample(self.quest_templates, min(3, len(self.quest_templates)))
            self.daily_quests = {quest['id']: quest for quest in selected_quests}
            self.last_refresh_date = current_date
            
            # Сбрасываем прогресс для всех игроков
            for player_id in self.player_progress:
                self.player_progress[player_id] = {
                    quest_id: {"completed": False, "progress": 0, "claimed": False} 
                    for quest_id in self.daily_quests
                }
    
    def assign_daily_quests(self, player_id):
        """
        Назначает ежедневные задания игроку
        
        Args:
            player_id (str): ID игрока
        """
        self.refresh_daily_quests()
        
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {}
        
        for quest_id in self.daily_quests:
            if quest_id not in self.player_progress[player_id]:
                self.player_progress[player_id][quest_id] = {
                    "completed": False, 
                    "progress": 0, 
                    "claimed": False
                }
    
    def complete_quest(self, player_id, quest_id):
        """
        Отмечает выполнение задания
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID задания
        """
        if player_id in self.player_progress and quest_id in self.player_progress[player_id]:
            quest_info = self.player_progress[player_id][quest_id]
            template = self.daily_quests[quest_id]
            
            quest_info["progress"] = template["target"]
            quest_info["completed"] = True
            
            return template["reward"]
        return 0
    
    def get_player_quests(self, player_id):
        """
        Возвращает список заданий игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            list: Список заданий игрока
        """
        self.refresh_daily_quests()
        
        if player_id not in self.player_progress:
            self.assign_daily_quests(player_id)
        
        quests_with_status = []
        for quest_id, progress in self.player_progress[player_id].items():
            if quest_id in self.daily_quests:
                quest_template = self.daily_quests[quest_id]
                quest_with_status = quest_template.copy()
                quest_with_status["progress"] = progress["progress"]
                quest_with_status["completed"] = progress["completed"]
                quest_with_status["claimed"] = progress["claimed"]
                quests_with_status.append(quest_with_status)
        
        return quests_with_status
    
    def time_until_reset(self):
        """
        Возвращает время до следующего сброса заданий
        
        Returns:
            timedelta: Время до сброса
        """
        tomorrow = date.today() + timedelta(days=1)
        reset_time = datetime.combine(tomorrow, datetime.min.time())
        return reset_time - datetime.now()


# Задание 3.2: Система мероприятий с часовыми поясами
class MultiTimeZoneEventManager:
    """
    Система управления мероприятиями в разных часовых поясах
    """
    def __init__(self):
        self.events = {}
        self.next_event_id = 1
    
    def create_event(self, name, start_time_utc, duration_hours, timezone_str, description=""):
        """
        Создает мероприятие в определенном часовом поясе
        
        Args:
            name (str): Название мероприятия
            start_time_utc (datetime): Время начала в UTC
            duration_hours (int): Продолжительность в часах
            timezone_str (str): Строковое обозначение часового пояса (например, 'Europe/Moscow')
            description (str): Описание мероприятия
        """
        event_id = self.next_event_id
        self.next_event_id += 1
        
        # Создаем timezone-aware объекты
        utc = pytz.UTC
        tz = pytz.timezone(timezone_str)
        
        # Преобразуем время начала в указанный часовой пояс
        start_time_localized = utc.localize(start_time_utc)
        start_time_in_tz = start_time_localized.astimezone(tz)
        
        event = {
            'id': event_id,
            'name': name,
            'start_time_utc': start_time_localized,
            'start_time_local': start_time_in_tz,
            'end_time_local': start_time_in_tz + timedelta(hours=duration_hours),
            'timezone': tz,
            'description': description,
            'duration': duration_hours
        }
        
        self.events[event_id] = event
        return event_id
    
    def get_event_time_in_timezone(self, event_id, timezone_str):
        """
        Возвращает время мероприятия в заданном часовом поясе
        
        Args:
            event_id (int): ID мероприятия
            timezone_str (str): Часовой пояс
            
        Returns:
            datetime: Время мероприятия в заданном часовом поясе
        """
        if event_id not in self.events:
            return None
        
        event = self.events[event_id]
        target_tz = pytz.timezone(timezone_str)
        
        # Конвертируем время начала из UTC в целевой часовой пояс
        return event['start_time_utc'].astimezone(target_tz)
    
    def get_events_for_user(self, user_timezone_str):
        """
        Возвращает мероприятия, актуальные для пользователя в его часовом поясе
        
        Args:
            user_timezone_str (str): Часовой пояс пользователя
            
        Returns:
            list: Список мероприятий
        """
        user_tz = pytz.timezone(user_timezone_str)
        user_now = datetime.now(user_tz)
        
        relevant_events = []
        for event in self.events.values():
            # Конвертируем время начала события в часовой пояс пользователя
            event_time_in_user_tz = event['start_time_utc'].astimezone(user_tz)
            
            # Проверяем, что событие еще не прошло (или начинается в ближайшие 24 часа)
            if event_time_in_user_tz >= user_now - timedelta(hours=24):
                event_copy = event.copy()
                event_copy['start_time_user_tz'] = event_time_in_user_tz
                relevant_events.append(event_copy)
        
        # Сортируем по времени начала в часовом поясе пользователя
        relevant_events.sort(key=lambda x: x['start_time_user_tz'])
        return relevant_events


# Задание 3.4: Комплексная система управления игровыми ресурсами
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
            resource_list (list): Список ресурсов для предзагрузки
        """
        for resource_type, resource_name in resource_list:
            try:
                resource_path = self.get_resource_path(resource_type, resource_name)
                relative_path = resource_path.relative_to(self.game_directory)
                self.cache_resource(relative_path)
                print(f"Предзагружен ресурс: {resource_type}/{resource_name}")
            except Exception as e:
                print(f"Ошибка предзагрузки ресурса {resource_type}/{resource_name}: {e}")
    
    def cleanup_cache(self, max_size_mb=100):
        """
        Очищает кэш, если он превышает максимальный размер
        
        Args:
            max_size_mb (int): Максимальный размер кэша в МБ
        """
        max_size = max_size_mb * 1024 * 1024
        
        # Простая стратегия очистки: удаляем половину самых старых элементов
        if self.cache_size > max_size:
            items_to_remove = len(self.resource_cache) // 2
            keys_to_remove = list(self.resource_cache.keys())[:items_to_remove]
            
            for key in keys_to_remove:
                data = self.resource_cache.pop(key, None)
                if data:
                    self.cache_size -= len(data)
            
            print(f"Кэш очищен: удалено {len(keys_to_remove)} элементов")


# Пример использования всех систем
if __name__ == "__main__":
    print("=== Демонстрация игровых систем с использованием модулей os и sys ===\n")
    
    # Пример использования GameFileManager
    print("--- Система управления файлами ---")
    file_manager = GameFileManager()
    info = file_manager.get_game_info()
    print(f"Каталоги: {len(info['directories'])}")
    print(f"Общий размер: {info['total_size']} байт")
    print()
    
    # Пример использования GameConfig
    print("--- Система конфигурации ---")
    config = GameConfig()
    config.print_config_summary()
    errors = config.validate_config()
    if errors:
        print(f"Ошибки валидации: {errors}")
    print()
    
    # Пример использования ModManager
    print("--- Система управления модами ---")
    mod_manager = ModManager()
    mods = mod_manager.scan_mods()
    print(f"Найдено модов: {len(mods)}")
    if mods:
        mod_manager.load_mod(mods[0]['name'])
    print()
    
    # Пример использования GameLogger
    print("--- Система логирования ---")
    logger = GameLogger()
    logger.log("INFO", "Игрок вошел в игру", "authentication")
    logger.log("ERROR", "Ошибка загрузки уровня", "level_loader")
    recent_logs = logger.get_recent_logs(1, "INFO")
    print(f"Недавних INFO логов: {len(recent_logs)}")
    print()
    
    # Пример использования CooldownManager
    print("--- Система кулдаунов ---")
    cooldown_mgr = CooldownManager()
    success, remaining = cooldown_mgr.use_ability("player1", "fireball", 30)
    print(f"Использование способности: {success}, осталось: {remaining}")
    ready = cooldown_mgr.is_ready("player1", "fireball")
    print(f"Способность готова: {ready}")
    print()
    
    # Пример использования DailyQuestSystem
    print("--- Система ежедневных заданий ---")
    quest_system = DailyQuestSystem()
    quest_system.assign_daily_quests("player1")
    player_quests = quest_system.get_player_quests("player1")
    print(f"Заданий игрока: {len(player_quests)}")
    reset_time = quest_system.time_until_reset()
    print(f"Время до сброса: {reset_time}")
    print()
    
    # Пример использования MultiTimeZoneEventManager
    print("--- Система мероприятий с часовыми поясами ---")
    event_manager = MultiTimeZoneEventManager()
    event_id = event_manager.create_event(
        "Глобальный турнир", 
        datetime(2023, 10, 15, 0),  # 15:00 UTC
        2, 
        "Europe/Moscow", 
        "Ежемесячный глобальный турнир"
    )
    moscow_time = event_manager.get_event_time_in_timezone(event_id, "Europe/Moscow")
    print(f"Время турнира в Москве: {moscow_time}")
    user_events = event_manager.get_events_for_user("Europe/Moscow")
    print(f"Событий для пользователя: {len(user_events)}")
    print()
    
    # Пример использования ResourceManager
    print("--- Система управления ресурсами ---")
    resource_manager = ResourceManager()
    manifest = resource_manager.build_resource_manifest()
    print(f"Ресурсов в манифесте: {len(manifest)}")
    resource_manager.preload_resources([("textures", "background.png"), ("sounds", "battle.mp3")])
    print()
    
    print("Все игровые системы с использованием модулей os и sys успешно реализованы!")