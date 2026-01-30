# Решения для практического задания 7: Работа с JSON в игровом контексте

import json
from datetime import datetime
from pathlib import Path

# Ниже приведены реализованные игровые классы и функции согласно заданию

def serialize_game_object(obj):
    """
    Сериализует игровой объект в JSON-совместимый формат
    
    Args:
        obj: Объект для сериализации
    
    Returns:
        str: JSON-строка объекта
    """
    def serialize_helper(obj):
        if hasattr(obj, '__dict__'):
            # Если это объект с атрибутами, сериализуем его словарь
            return {key: serialize_helper(value) for key, value in obj.__dict__.items()}
        elif isinstance(obj, (list, tuple)):
            # Если это список или кортеж, рекурсивно сериализуем элементы
            return [serialize_helper(item) for item in obj]
        elif isinstance(obj, dict):
            # Если это словарь, рекурсивно сериализуем значения
            return {key: serialize_helper(value) for key, value in obj.items()}
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            # Базовые типы остаются без изменений
            return obj
        elif isinstance(obj, datetime):
            # Дату-время преобразуем в строку ISO формата
            return obj.isoformat()
        else:
            # Для прочих типов пытаемся преобразовать к строке
            return str(obj)
    
    serialized_obj = serialize_helper(obj)
    return json.dumps(serialized_obj, indent=2, ensure_ascii=False)


def deserialize_game_object(json_str):
    """
    Десериализует JSON-строку в игровой объект
    
    Args:
        json_str (str): JSON-строка для десериализации
    
    Returns:
        объект: Десериализованный игровой объект
    """
    def deserialize_helper(data):
        if isinstance(data, dict):
            # Проверяем, является ли это датой
            if 'isoformat' in str(data) and len(data) == 1:
                # Пробуем определить, является ли это датой
                for key, value in data.items():
                    if isinstance(value, str):
                        try:
                            return datetime.fromisoformat(value)
                        except ValueError:
                            pass
            # Создаем объект с атрибутами из словаря
            obj = type('DynamicObject', (), {})()
            for key, value in data.items():
                setattr(obj, key, deserialize_helper(value))
            return obj
        elif isinstance(data, list):
            # Если это список, рекурсивно десериализуем элементы
            return [deserialize_helper(item) for item in data]
        else:
            # Базовые типы остаются без изменений
            return data
    
    parsed_json = json.loads(json_str)
    return deserialize_helper(parsed_json)


class GameConfig:
    """
    Система конфигурации игры через JSON-файл
    """
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.default_config = {
            "resolution": {
                "width": 1920,
                "height": 1080
            },
            "graphics": {
                "quality": "high",
                "vsync": True,
                "anti_aliasing": "4x"
            },
            "audio": {
                "master_volume": 0.8,
                "music_volume": 0.7,
                "sfx_volume": 1.0
            },
            "controls": {
                "mouse_sensitivity": 5.0,
                "key_bindings": {
                    "move_forward": "W",
                    "move_backward": "S",
                    "move_left": "A",
                    "move_right": "D",
                    "jump": "SPACE",
                    "inventory": "TAB"
                }
            },
            "gameplay": {
                "difficulty": "normal",
                "language": "en",
                "subtitles": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """
        Загружает конфигурацию из файла
        
        Returns:
            dict: Словарь конфигурации
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Объединяем загруженную конфигурацию с конфигурацией по умолчанию
                # чтобы гарантировать наличие всех необходимых полей
                merged_config = self.merge_configs(self.default_config, loaded_config)
                return merged_config
            except json.JSONDecodeError:
                print(f"Ошибка чтения конфигурации из {self.config_file}, используется значение по умолчанию")
                return self.default_config
        else:
            # Создаем файл конфигурации со значениями по умолчанию
            self.save_config()
            return self.default_config
    
    def save_config(self):
        """
        Сохраняет текущую конфигурацию в файл
        """
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_setting(self, *keys):
        """
        Возвращает значение настройки по цепочке ключей
        
        Args:
            *keys: Ключи для доступа к настройке
            
        Returns:
            значение: Значение настройки
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def set_setting(self, value, *keys):
        """
        Устанавливает значение настройки по цепочке ключей
        
        Args:
            value: Значение для установки
            *keys: Ключи для доступа к настройке
        """
        config_ref = self.config
        for key in keys[:-1]:
            if key not in config_ref or not isinstance(config_ref[key], dict):
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = value
    
    def merge_configs(self, default, override):
        """
        Объединяет конфигурации, заполняя отсутствующие поля значениями по умолчанию
        
        Args:
            default (dict): Конфигурация по умолчанию
            override (dict): Переопределяющая конфигурация
            
        Returns:
            dict: Объединенная конфигурация
        """
        result = default.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result


class PlayerProgressManager:
    """
    Система управления сохранением и загрузкой прогресса игрока
    """
    def __init__(self, saves_directory="saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
    
    def save_player_progress(self, player, save_name):
        """
        Сохраняет прогресс игрока в JSON-файл
        
        Args:
            player (object): Объект игрока
            save_name (str): Имя сохранения
        """
        save_path = self.saves_directory / f"{save_name}.json"
        
        # Подготовим данные игрока для сохранения
        player_data = player.to_dict()
        player_data['save_date'] = datetime.now().isoformat()
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(player_data, f, indent=2, ensure_ascii=False)
    
    def load_player_progress(self, save_name):
        """
        Загружает прогресс игрока из JSON-файла
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            object: Загруженный объект игрока
        """
        save_path = self.saves_directory / f"{save_name}.json"
        
        if not save_path.exists():
            return None
        
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
            
            # Обновим время последней игры
            player_data['last_played'] = datetime.now()
            
            return Player.from_dict(player_data)
        except json.JSONDecodeError:
            print(f"Ошибка чтения сохранения: {save_path}")
            return None
    
    def list_saves(self):
        """
        Возвращает список доступных сохранений
        
        Returns:
            list: Список имен файлов сохранений
        """
        save_files = list(self.saves_directory.glob("*.json"))
        save_names = [f.stem for f in save_files]  # Имя файла без расширения
        return sorted(save_names, reverse=True)  # Сортируем в обратном порядке (новые первыми)
    
    def delete_save(self, save_name):
        """
        Удаляет файл сохранения
        
        Args:
            save_name (str): Имя сохранения для удаления
        """
        save_path = self.saves_directory / f"{save_name}.json"
        if save_path.exists():
            save_path.unlink()  # Удаляем файл
            return True
        return False


class Player:
    def __init__(self, name, level=1, health=100, position=(0, 0)):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = 100
        self.position = position
        self.inventory = []
        self.stats = {
            'strength': 10,
            'agility': 10,
            'intelligence': 10
        }
        self.play_time = 0  # Время в игре в секундах
        self.creation_date = datetime.now()
        self.last_played = datetime.now()
    
    def to_dict(self):
        """
        Преобразует игрока в словарь для сохранения в JSON
        """
        return {
            'name': self.name,
            'level': self.level,
            'health': self.health,
            'max_health': self.max_health,
            'position': self.position,
            'inventory': self.inventory,
            'stats': self.stats,
            'play_time': self.play_time,
            'creation_date': self.creation_date.isoformat(),
            'last_played': self.last_played.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Создает игрока из словаря
        
        Args:
            data (dict): Словарь с данными игрока
        """
        # Преобразуем строковые даты обратно в объекты datetime
        creation_date = datetime.fromisoformat(data['creation_date'])
        last_played = datetime.fromisoformat(data['last_played'])
        
        player = cls(
            name=data['name'],
            level=data['level'],
            health=data['health'],
            position=tuple(data['position'])  # Преобразуем обратно в кортеж
        )
        
        # Восстановим остальные атрибуты
        player.max_health = data['max_health']
        player.inventory = data['inventory']
        player.stats = data['stats']
        player.play_time = data['play_time']
        player.creation_date = creation_date
        player.last_played = last_played
        
        return player


class AssetManager:
    """
    Система загрузки игровых ассетов из JSON-файлов
    """
    def __init__(self, assets_directory="assets"):
        self.assets_directory = Path(assets_directory)
        self.loaded_assets = {}
        self.asset_manifests = {}
    
    def load_asset_manifest(self, manifest_file):
        """
        Загружает манифест ассетов из JSON-файла
        
        Args:
            manifest_file (str): Путь к файлу манифеста
            
        Returns:
            dict: Загруженный манифест ассетов
        """
        manifest_path = self.assets_directory / manifest_file
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Сохраняем манифест
            manifest_name = Path(manifest_file).stem
            self.asset_manifests[manifest_name] = manifest
            return manifest
        except FileNotFoundError:
            print(f"Файл манифеста не найден: {manifest_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON из файла: {manifest_path}")
            return {}
    
    def load_asset(self, asset_type, asset_name):
        """
        Загружает указанный ассет
        
        Args:
            asset_type (str): Тип ассета (models, textures, sounds, etc.)
            asset_name (str): Имя ассета для загрузки
            
        Returns:
            object: Загруженный ассет
        """
        # Проверяем, загружен ли ассет в кэш
        cache_key = f"{asset_type}:{asset_name}"
        if cache_key in self.loaded_assets:
            return self.loaded_assets[cache_key]
        
        # Ищем информацию об ассете в манифестах
        for manifest in self.asset_manifests.values():
            if asset_type in manifest and asset_name in manifest[asset_type]:
                asset_info = manifest[asset_type][asset_name]
                asset_path = self.assets_directory / asset_info['path']
                
                if asset_path.exists():
                    # Загружаем ассет в зависимости от типа
                    if asset_path.suffix.lower() in ['.obj', '.fbx', '.dae', '.gltf']:
                        # Загрузка 3D модели
                        with open(asset_path, 'r', encoding='utf-8') as f:
                            asset_data = f.read()
                    elif asset_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tga']:
                        # Загрузка текстуры (в реальном приложении это будет бинарные данные)
                        with open(asset_path, 'rb') as f:
                            asset_data = f.read()
                    elif asset_path.suffix.lower() in ['.wav', '.mp3', '.ogg']:
                        # Загрузка звука (в реальном приложении это будет бинарные данные)
                        with open(asset_path, 'rb') as f:
                            asset_data = f.read()
                    else:
                        # Для других файлов просто читаем как текст
                        with open(asset_path, 'r', encoding='utf-8') as f:
                            asset_data = f.read()
                    
                    # Сохраняем в кэш
                    self.loaded_assets[cache_key] = {
                        'data': asset_data,
                        'info': asset_info
                    }
                    
                    return self.loaded_assets[cache_key]
                else:
                    print(f"Файл ассета не найден: {asset_path}")
                    return None
        
        print(f"Ассет не найден: {asset_type}/{asset_name}")
        return None
    
    def get_asset_info(self, asset_type, asset_name):
        """
        Возвращает информацию об ассете
        
        Args:
            asset_type (str): Тип ассета
            asset_name (str): Имя ассета
            
        Returns:
            dict: Информация об ассете
        """
        for manifest in self.asset_manifests.values():
            if asset_type in manifest and asset_name in manifest[asset_type]:
                return manifest[asset_type][asset_name]
        
        return None
    
    def validate_asset_data(self, asset_data, expected_schema):
        """
        Проверяет, соответствует ли ассет ожидаемой схеме
        
        Args:
            asset_data (dict): Данные ассета
            expected_schema (dict): Ожидаемая схема
            
        Returns:
            bool: Соответствует ли ассет схеме
        """
        def check_schema(data, schema):
            if isinstance(schema, dict):
                if not isinstance(data, dict):
                    return False
                
                for key, value in schema.items():
                    if key not in data:
                        return False
                    if not check_schema(data[key], value):
                        return False
                return True
            elif isinstance(schema, list) and len(schema) > 0:
                if not isinstance(data, list):
                    return False
                for item in data:
                    if not check_schema(item, schema[0]):
                        return False
                return True
            elif schema == "string":
                return isinstance(data, str)
            elif schema == "number":
                return isinstance(data, (int, float))
            elif schema == "boolean":
                return isinstance(data, bool)
            elif schema == "object":
                return isinstance(data, dict)
            elif schema == "array":
                return isinstance(data, list)
            else:
                return type(data).__name__ == schema
        
        return check_schema(asset_data, expected_schema)


class QuestSystem:
    """
    Система квестов с JSON-описаниями
    """
    def __init__(self, quests_directory="quests"):
        self.quests_directory = Path(quests_directory)
        self.quests = {}
        self.player_quests = {}
        self.active_quests = {}
    
    def load_quest_definitions(self, quest_file):
        """
        Загружает определения квестов из JSON-файла
        
        Args:
            quest_file (str): Путь к файлу с определениями квестов
        """
        quest_path = self.quests_directory / quest_file
        
        try:
            with open(quest_path, 'r', encoding='utf-8') as f:
                quest_definitions = json.load(f)
            
            for quest_def in quest_definitions:
                self.quests[quest_def['id']] = quest_def
            
            print(f"Загружено {len(quest_definitions)} квестов из {quest_path}")
        except FileNotFoundError:
            print(f"Файл квестов не найден: {quest_path}")
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON из файла: {quest_path}")
    
    def assign_quest_to_player(self, player_id, quest_id):
        """
        Назначает квест игроку
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID квеста для назначения
        """
        if quest_id not in self.quests:
            print(f"Квест не найден: {quest_id}")
            return False
        
        if player_id not in self.player_quests:
            self.player_quests[player_id] = {}
        
        quest_definition = self.quests[quest_id]
        
        # Создаем экземпляр квеста для игрока
        player_quest_instance = {
            'definition': quest_definition,
            'assigned_at': datetime.now(),
            'progress': 0,
            'completed': False,
            'rewards_claimed': False
        }
        
        self.player_quests[player_id][quest_id] = player_quest_instance
        
        # Добавляем в активные квесты
        if player_id not in self.active_quests:
            self.active_quests[player_id] = []
        self.active_quests[player_id].append(quest_id)
        
        return True
    
    def update_quest_progress(self, player_id, quest_id, progress_change=1):
        """
        Обновляет прогресс выполнения квеста
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID квеста
            progress_change (int): Изменение прогресса
        """
        if player_id in self.player_quests and quest_id in self.player_quests[player_id]:
            quest_instance = self.player_quests[player_id][quest_id]
            
            if not quest_instance['completed']:
                quest_instance['progress'] += progress_change
                
                # Проверяем, завершен ли квест
                required_progress = quest_instance['definition']['objective']['count']
                if quest_instance['progress'] >= required_progress:
                    quest_instance['completed'] = True
                    # Убираем из активных квестов
                    if player_id in self.active_quests and quest_id in self.active_quests[player_id]:
                        self.active_quests[player_id].remove(quest_id)
                
                return True
        
        return False
    
    def complete_quest(self, player_id, quest_id):
        """
        Завершает квест для игрока
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID квеста для завершения
        """
        if player_id in self.player_quests and quest_id in self.player_quests[player_id]:
            quest_instance = self.player_quests[player_id][quest_id]
            
            if not quest_instance['completed']:
                required_progress = quest_instance['definition']['objective']['count']
                quest_instance['progress'] = required_progress
                quest_instance['completed'] = True
                
                # Убираем из активных квестов
                if player_id in self.active_quests and quest_id in self.active_quests[player_id]:
                    self.active_quests[player_id].remove(quest_id)
                
                return True
        
        return False
    
    def get_player_active_quests(self, player_id):
        """
        Возвращает активные квесты игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            list: Список активных квестов игрока
        """
        if player_id not in self.active_quests:
            return []
        
        active_quests_info = []
        for quest_id in self.active_quests[player_id]:
            if quest_id in self.player_quests[player_id]:
                quest_instance = self.player_quests[player_id][quest_id]
                active_quests_info.append({
                    'id': quest_id,
                    'name': quest_instance['definition']['name'],
                    'description': quest_instance['definition']['description'],
                    'progress': quest_instance['progress'],
                    'target': quest_instance['definition']['objective']['count'],
                    'completed': quest_instance['completed']
                })
        
        return active_quests_info


class ModManager:
    """
    Система управления модами с JSON-конфигурацией
    """
    def __init__(self, mods_directory="mods"):
        self.mods_directory = Path(mods_directory)
        self.installed_mods = {}
        self.enabled_mods = []
        self.mod_dependencies = {}
    
    def scan_mods(self):
        """
        Сканирует директорию на наличие модов и загружает их конфигурацию
        """
        for mod_dir in self.mods_directory.iterdir():
            if mod_dir.is_dir():
                config_path = mod_dir / "mod.json"
                if config_path.exists():
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            mod_config = json.load(f)
                        
                        mod_id = mod_config['id']
                        self.installed_mods[mod_id] = {
                            'config': mod_config,
                            'directory': mod_dir,
                            'enabled': False
                        }
                        
                        # Сохраняем зависимости
                        if 'dependencies' in mod_config:
                            self.mod_dependencies[mod_id] = mod_config['dependencies']
                        
                        print(f"Найден мод: {mod_config['name']} (ID: {mod_id})")
                    except json.JSONDecodeError:
                        print(f"Ошибка чтения конфигурации мода: {mod_dir.name}")
                else:
                    print(f"Конфигурационный файл не найден для мода: {mod_dir.name}")
    
    def load_mod_config(self, mod_id):
        """
        Загружает конфигурацию мода из JSON-файла
        
        Args:
            mod_id (str): ID мода
        """
        if mod_id not in self.installed_mods:
            return None
        
        config_path = self.installed_mods[mod_id]['directory'] / "mod.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Конфигурационный файл мода не найден: {config_path}")
            return None
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON-конфигурации мода: {config_path}")
            return None
    
    def validate_mod_compatibility(self, mod_id):
        """
        Проверяет совместимость мода с текущей версией игры и другими модами
        
        Args:
            mod_id (str): ID мода для проверки
            
        Returns:
            tuple: (совместим ли мод, список ошибок)
        """
        if mod_id not in self.installed_mods:
            return False, ["Мод не найден"]
        
        mod_config = self.installed_mods[mod_id]['config']
        errors = []
        
        # Проверяем версию игры
        game_version = "1.5.0"  # В реальной игре это будет динамически получаться
        if 'game_version_min' in mod_config:
            if self.compare_versions(game_version, mod_config['game_version_min']) < 0:
                errors.append(f"Мод требует версию игры не ниже {mod_config['game_version_min']}, текущая: {game_version}")
        
        if 'game_version_max' in mod_config:
            if self.compare_versions(game_version, mod_config['game_version_max']) > 0:
                errors.append(f"Мод несовместим с версией игры выше {mod_config['game_version_max']}, текущая: {game_version}")
        
        # Проверяем зависимости
        if 'dependencies' in mod_config:
            for dependency in mod_config['dependencies']:
                if dependency not in self.installed_mods or not self.installed_mods[dependency]['enabled']:
                    errors.append(f"Отсутствует зависимость: {dependency}")
        
        # Проверяем конфликты
        if 'conflicts' in mod_config:
            for conflict in mod_config['conflicts']:
                if conflict in self.enabled_mods:
                    errors.append(f"Конфликт с модом: {conflict}")
        
        return len(errors) == 0, errors
    
    def compare_versions(self, version1, version2):
        """
        Сравнивает две версии в формате X.Y.Z
        
        Args:
            version1 (str): Первая версия
            version2 (str): Вторая версия
            
        Returns:
            int: -1 если version1 < version2, 0 если равны, 1 если version1 > version2
        """
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        for i in range(min(len(v1_parts), len(v2_parts))):
            if v1_parts[i] < v2_parts[i]:
                return -1
            elif v1_parts[i] > v2_parts[i]:
                return 1
        
        if len(v1_parts) < len(v2_parts):
            return -1
        elif len(v1_parts) > len(v2_parts):
            return 1
        else:
            return 0
    
    def enable_mod(self, mod_id):
        """
        Включает мод в игру
        
        Args:
            mod_id (str): ID мода для включения
        """
        is_compatible, errors = self.validate_mod_compatibility(mod_id)
        if not is_compatible:
            print(f"Невозможно включить мод {mod_id}: {', '.join(errors)}")
            return False
        
        if mod_id in self.installed_mods:
            self.installed_mods[mod_id]['enabled'] = True
            if mod_id not in self.enabled_mods:
                self.enabled_mods.append(mod_id)
            print(f"Мод включен: {self.installed_mods[mod_id]['config']['name']}")
            return True
        
        return False
    
    def disable_mod(self, mod_id):
        """
        Выключает мод из игры
        
        Args:
            mod_id (str): ID мода для выключения
        """
        if mod_id in self.installed_mods and mod_id in self.enabled_mods:
            # Проверяем, не зависят ли другие включенные моды от этого
            for enabled_mod_id in self.enabled_mods:
                if enabled_mod_id != mod_id and mod_id in self.mod_dependencies.get(enabled_mod_id, []):
                    print(f"Невозможно выключить мод {mod_id}, так как от него зависит {enabled_mod_id}")
                    return False
            
            self.installed_mods[mod_id]['enabled'] = False
            self.enabled_mods.remove(mod_id)
            print(f"Мод выключен: {self.installed_mods[mod_id]['config']['name']}")
            return True
        
        return False


class WorldSaveSystem:
    """
    Система сохранения игрового мира в JSON
    """
    def __init__(self, saves_directory="world_saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
        self.current_world_state = {}
    
    def save_world(self, world_state, save_name, description=""):
        """
        Сохраняет состояние игрового мира в JSON-файл
        
        Args:
            world_state (dict): Состояние игрового мира для сохранения
            save_name (str): Имя сохранения
            description (str): Описание сохранения
        """
        save_path = self.saves_directory / f"{save_name}.json"
        
        # Добавляем метаданные к сохранению
        save_data = {
            'meta': {
                'version': '1.0',
                'timestamp': datetime.now().isoformat(),
                'description': description,
                'game_version': '1.0.0'  # В реальной игре будет динамически получаться
            },
            'world_state': world_state
        }
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"Мир сохранен: {save_path}")
    
    def load_world(self, save_name):
        """
        Загружает состояние игрового мира из JSON-файла
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            dict: Состояние игрового мира
        """
        save_path = self.saves_directory / f"{save_name}.json"
        
        if not save_path.exists():
            print(f"Файл сохранения не найден: {save_path}")
            return None
        
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.current_world_state = save_data.get('world_state', {})
            print(f"Мир загружен: {save_path}")
            return self.current_world_state
        except json.JSONDecodeError:
            print(f"Ошибка чтения сохранения: {save_path}")
            return None
    
    def get_save_info(self, save_name):
        """
        Возвращает информацию о сохранении
        
        Args:
            save_name (str): Имя сохранения
            
        Returns:
            dict: Информация о сохранении
        """
        save_path = self.saves_directory / f"{save_name}.json"
        
        if not save_path.exists():
            return None
        
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            meta = save_data.get('meta', {})
            world_state = save_data.get('world_state', {})
            
            return {
                'name': save_name,
                'version': meta.get('version', 'unknown'),
                'timestamp': meta.get('timestamp', 'unknown'),
                'description': meta.get('description', ''),
                'game_version': meta.get('game_version', 'unknown'),
                'player_count': len(world_state.get('players', [])),
                'npc_count': len(world_state.get('npcs', [])),
                'item_count': len(world_state.get('items_on_ground', []))
            }
        except json.JSONDecodeError:
            print(f"Ошибка чтения информации о сохранении: {save_path}")
            return None
    
    def validate_world_data(self, world_data):
        """
        Проверяет корректность данных игрового мира
        
        Args:
            world_data (dict): Данные игрового мира для проверки
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        errors = []
        
        # Проверяем обязательные поля
        if 'meta' not in world_data:
            errors.append("Отсутствует поле 'meta' в данных мира")
        else:
            meta = world_data['meta']
            if 'version' not in meta:
                errors.append("В метаданных отсутствует 'version'")
            if 'timestamp' not in meta:
                errors.append("В метаданных отсутствует 'timestamp'")
        
        # Проверяем структуру игроков
        players = world_data.get('players', [])
        for i, player in enumerate(players):
            if 'id' not in player:
                errors.append(f"У игрока #{i} отсутствует 'id'")
            if 'name' not in player:
                errors.append(f"У игрока #{i} отсутствует 'name'")
            if 'position' not in player:
                errors.append(f"У игрока #{i} отсутствует 'position'")
        
        # Проверяем структуру NPC
        npcs = world_data.get('npcs', [])
        for i, npc in enumerate(npcs):
            if 'id' not in npc:
                errors.append(f"У NPC #{i} отсутствует 'id'")
            if 'name' not in npc:
                errors.append(f"У NPC #{i} отсутствует 'name'")
        
        return len(errors) == 0, errors


class PlayerSettingsManager:
    """
    Система управления индивидуальными настройками игроков
    """
    def __init__(self, settings_directory="player_settings"):
        self.settings_directory = Path(settings_directory)
        self.settings_directory.mkdir(exist_ok=True)
        self.default_settings = {
            "graphics": {
                "resolution": [1920, 1080],
                "quality": "high",
                "vsync": True,
                "fov": 90
            },
            "audio": {
                "master_volume": 0.8,
                "music_volume": 0.7,
                "sfx_volume": 1.0,
                "voice_enabled": True
            },
            "gameplay": {
                "difficulty": "normal",
                "language": "en",
                "subtitles": True,
                "auto_save": True
            },
            "interface": {
                "ui_scale": 1.0,
                "show_hud": True,
                "minimap_size": "medium"
            }
        }
    
    def load_player_settings(self, player_id):
        """
        Загружает настройки конкретного игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            dict: Настройки игрока
        """
        settings_path = self.settings_directory / f"{player_id}.json"
        
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # Объединяем загруженные настройки с настройками по умолчанию
                # чтобы гарантировать наличие всех необходимых полей
                merged_settings = self.merge_dicts(self.default_settings, loaded_settings)
                return merged_settings
            except json.JSONDecodeError:
                print(f"Ошибка чтения настроек игрока {player_id}, используются настройки по умолчанию")
                return self.default_settings
        else:
            # Создаем файл настроек со значениями по умолчанию
            self.save_player_settings(player_id, self.default_settings)
            return self.default_settings
    
    def save_player_settings(self, player_id, settings):
        """
        Сохраняет настройки игрока в JSON-файл
        
        Args:
            player_id (str): ID игрока
            settings (dict): Настройки для сохранения
        """
        settings_path = self.settings_directory / f"{player_id}.json"
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    
    def get_player_setting(self, player_id, *keys):
        """
        Возвращает значение настройки игрока по цепочке ключей
        
        Args:
            player_id (str): ID игрока
            *keys: Ключи для доступа к настройке
            
        Returns:
            значение: Значение настройки
        """
        settings = self.load_player_settings(player_id)
        value = settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def set_player_setting(self, player_id, value, *keys):
        """
        Устанавливает значение настройки игрока по цепочке ключей
        
        Args:
            player_id (str): ID игрока
            value: Значение для установки
            *keys: Ключи для доступа к настройке
        """
        settings = self.load_player_settings(player_id)
        settings_ref = settings
        for key in keys[:-1]:
            if key not in settings_ref or not isinstance(settings_ref[key], dict):
                settings_ref[key] = {}
            settings_ref = settings_ref[key]
        
        settings_ref[keys[-1]] = value
        self.save_player_settings(player_id, settings)
    
    def merge_dicts(self, default, override):
        """
        Объединяет два словаря, заполняя отсутствующие поля значениями по умолчанию
        
        Args:
            default (dict): Словарь по умолчанию
            override (dict): Переопределяющий словарь
            
        Returns:
            dict: Объединенный словарь
        """
        result = default.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result


class InventoryManager:
    """
    Система управления инвентарем игрока с сохранением в JSON
    """
    def __init__(self, inventories_directory="inventories"):
        self.inventories_directory = Path(inventories_directory)
        self.inventories_directory.mkdir(exist_ok=True)
        self.max_inventory_size = 50  # Максимальное количество предметов в инвентаре
    
    def create_inventory(self, player_id, initial_items=None):
        """
        Создает новый инвентарь для игрока
        
        Args:
            player_id (str): ID игрока
            initial_items (list): Начальные предметы (опционально)
        """
        if initial_items is None:
            initial_items = []
        
        inventory_path = self.inventories_directory / f"{player_id}.json"
        
        inventory_data = {
            'player_id': player_id,
            'created_at': datetime.now().isoformat(),
            'items': initial_items,
            'max_size': self.max_inventory_size
        }
        
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(inventory_data, f, indent=2, ensure_ascii=False)
    
    def add_item(self, player_id, item):
        """
        Добавляет предмет в инвентарь игрока
        
        Args:
            player_id (str): ID игрока
            item (dict): Предмет для добавления
        """
        inventory = self.get_inventory(player_id)
        if inventory is None:
            inventory = []
        
        # Проверяем, не превышено ли максимальное количество предметов
        if len(inventory) >= self.max_inventory_size:
            print(f"Инвентарь игрока {player_id} полон")
            return False
        
        # Проверяем, есть ли уже такой предмет (для стакающихся предметов)
        existing_item_idx = None
        for i, inv_item in enumerate(inventory):
            if inv_item['id'] == item['id'] and inv_item.get('stackable', False):
                existing_item_idx = i
                break
        
        if existing_item_idx is not None:
            # Увеличиваем количество существующего предмета
            inventory[existing_item_idx]['quantity'] += item.get('quantity', 1)
        else:
            # Добавляем новый предмет
            inventory.append(item)
        
        self.save_inventory(player_id, inventory)
        return True
    
    def remove_item(self, player_id, item_id):
        """
        Удаляет предмет из инвентаря игрока
        
        Args:
            player_id (str): ID игрока
            item_id (str): ID предмета для удаления
        """
        inventory = self.get_inventory(player_id)
        if inventory is None:
            return False
        
        for i, item in enumerate(inventory):
            if item['id'] == item_id:
                inventory.pop(i)
                self.save_inventory(player_id, inventory)
                return True
        
        return False  # Предмет не найден
    
    def get_inventory(self, player_id):
        """
        Возвращает инвентарь игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            list: Список предметов в инвентаре
        """
        inventory_path = self.inventories_directory / f"{player_id}.json"
        
        if not inventory_path.exists():
            return []
        
        try:
            with open(inventory_path, 'r', encoding='utf-8') as f:
                inventory_data = json.load(f)
            return inventory_data.get('items', [])
        except json.JSONDecodeError:
            print(f"Ошибка чтения инвентаря игрока {player_id}")
            return []
    
    def save_inventory(self, player_id, inventory):
        """
        Сохраняет инвентарь игрока
        
        Args:
            player_id (str): ID игрока
            inventory (list): Инвентарь для сохранения
        """
        inventory_path = self.inventories_directory / f"{player_id}.json"
        
        inventory_data = {
            'player_id': player_id,
            'updated_at': datetime.now().isoformat(),
            'items': inventory,
            'max_size': self.max_inventory_size
        }
        
        with open(inventory_path, 'w', encoding='utf-8') as f:
            json.dump(inventory_data, f, indent=2, ensure_ascii=False)


class AchievementManager:
    """
    Система управления достижениями с JSON-хранилищем
    """
    def __init__(self, achievements_file="achievements.json", progress_directory="achievement_progress"):
        self.achievements_file = Path(achievements_file)
        self.progress_directory = Path(progress_directory)
        self.progress_directory.mkdir(exist_ok=True)
        
        # Стандартные достижения
        self.default_achievements = [
            {
                "id": "first_steps",
                "name": "Первые шаги",
                "description": "Сделайте первые шаги в игрое",
                "type": "exploration",
                "target": 1,
                "rewards": {"xp": 100, "coins": 50}
            },
            {
                "id": "veteran_player",
                "name": "Опытный игрок",
                "description": "Играть в течение 10 часов",
                "type": "playtime",
                "target": 36000,  # 10 часов в секундах
                "rewards": {"xp": 1000, "special_title": "Ветеран"}
            },
            {
                "id": "monster_hunter",
                "name": "Охотник на монстров",
                "description": "Победить 100 монстров",
                "type": "combat",
                "target": 100,
                "rewards": {"xp": 500, "rare_item": "hunter_medal"}
            }
        ]
        
        self.achievements = self.load_achievements()
    
    def load_achievements(self):
        """
        Загружает список достижений из JSON-файла
        
        Returns:
            list: Список достижений
        """
        if self.achievements_file.exists():
            try:
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла достижений, используется стандартный список")
                return self.default_achievements
        else:
            # Создаем файл со стандартными достижениями
            self.save_achievements()
            return self.default_achievements
    
    def save_achievements(self):
        """
        Сохраняет список достижений в JSON-файл
        """
        with open(self.achievements_file, 'w', encoding='utf-8') as f:
            json.dump(self.achievements, f, indent=2, ensure_ascii=False)
    
    def load_player_progress(self, player_id):
        """
        Загружает прогресс достижений игрока из JSON-файла
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            dict: Прогресс достижений игрока
        """
        progress_path = self.progress_directory / f"{player_id}.json"
        
        if progress_path.exists():
            try:
                with open(progress_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Ошибка чтения прогресса достижений для игрока {player_id}")
                return {}
        else:
            # Создаем новый файл прогресса
            return {}
    
    def save_player_progress(self, player_id, progress):
        """
        Сохраняет прогресс достижений игрока в JSON-файл
        
        Args:
            player_id (str): ID игрока
            progress (dict): Прогресс для сохранения
        """
        progress_path = self.progress_directory / f"{player_id}.json"
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    
    def grant_achievement(self, player_id, achievement_id):
        """
        Выдает достижение игроку
        
        Args:
            player_id (str): ID игрока
            achievement_id (str): ID достижения для выдачи
        """
        player_progress = self.load_player_progress(player_id)
        
        # Проверяем, существует ли достижение
        achievement_exists = any(ach['id'] == achievement_id for ach in self.achievements)
        if not achievement_exists:
            print(f"Достижение не найдено: {achievement_id}")
            return False
        
        # Обновляем прогресс
        if achievement_id not in player_progress:
            player_progress[achievement_id] = {
                "achieved": False,
                "progress": 0
            }
        
        achievement_def = next(ach for ach in self.achievements if ach['id'] == achievement_id)
        player_progress[achievement_id]["achieved"] = True
        player_progress[achievement_id]["progress"] = achievement_def["target"]
        player_progress[achievement_id]["achieved_at"] = datetime.now().isoformat()
        
        self.save_player_progress(player_id, player_progress)
        print(f"Достижение получено игроком {player_id}: {achievement_id}")
        return True
    
    def update_achievement_progress(self, player_id, achievement_id, progress_increment=1):
        """
        Обновляет прогресс по достижению
        
        Args:
            player_id (str): ID игрока
            achievement_id (str): ID достижения
            progress_increment (int): Прирост прогресса
        """
        player_progress = self.load_player_progress(player_id)
        
        # Проверяем, существует ли достижение
        achievement_exists = any(ach['id'] == achievement_id for ach in self.achievements)
        if not achievement_exists:
            print(f"Достижение не найдено: {achievement_id}")
            return False
        
        achievement_def = next(ach for ach in self.achievements if ach['id'] == achievement_id)
        
        # Обновляем прогресс
        if achievement_id not in player_progress:
            player_progress[achievement_id] = {
                "achieved": False,
                "progress": 0
            }
        
        current_progress = player_progress[achievement_id]["progress"]
        new_progress = min(current_progress + progress_increment, achievement_def["target"])
        player_progress[achievement_id]["progress"] = new_progress
        
        # Проверяем, достигнута ли цель
        if new_progress >= achievement_def["target"] and not player_progress[achievement_id]["achieved"]:
            player_progress[achievement_id]["achieved"] = True
            player_progress[achievement_id]["achieved_at"] = datetime.now().isoformat()
            print(f"Достижение выполнено игроком {player_id}: {achievement_id}")
        
        self.save_player_progress(player_id, player_progress)
        return True


class LocationManager:
    """
    Система управления игровыми локациями с JSON-описанием
    """
    def __init__(self, locations_directory="locations", connections_file="location_connections.json"):
        self.locations_directory = Path(locations_directory)
        self.connections_file = Path(connections_file)
        self.locations = {}
        self.location_connections = {}
        
        self.load_all_locations()
        self.load_connections()
    
    def load_all_locations(self):
        """
        Загружает все локации из JSON-файлов в директории
        """
        for location_file in self.locations_directory.glob("*.json"):
            try:
                with open(location_file, 'r', encoding='utf-8') as f:
                    location_data = json.load(f)
                
                location_id = location_data['id']
                self.locations[location_id] = location_data
                print(f"Загружена локация: {location_data['name']} (ID: {location_id})")
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла локации: {location_file}")
            except KeyError:
                print(f"Отсутствует ID в файле локации: {location_file}")
    
    def load_location(self, location_id):
        """
        Загружает конкретную локацию из JSON-файла
        
        Args:
            location_id (str): ID локации для загрузки
        """
        if location_id in self.locations:
            return self.locations[location_id]
        
        location_path = self.locations_directory / f"{location_id}.json"
        if location_path.exists():
            try:
                with open(location_path, 'r', encoding='utf-8') as f:
                    location_data = json.load(f)
                
                self.locations[location_id] = location_data
                return location_data
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла локации: {location_path}")
                return None
        else:
            print(f"Файл локации не найден: {location_path}")
            return None
    
    def get_connected_locations(self, location_id):
        """
        Возвращает список подключенных локаций
        
        Args:
            location_id (str): ID локации
            
        Returns:
            list: Список подключенных локаций
        """
        return self.location_connections.get(location_id, [])
    
    def find_path(self, start_location, end_location):
        """
        Находит путь между двумя локациями
        
        Args:
            start_location (str): ID начальной локации
            end_location (str): ID конечной локации
            
        Returns:
            list: Список локаций в пути (или None, если путь не найден)
        """
        if start_location not in self.location_connections or end_location not in self.location_connections:
            return None
        
        # Используем алгоритм BFS для поиска кратчайшего пути
        from collections import deque
        queue = deque([(start_location, [start_location])])
        visited = {start_location}
        
        while queue:
            current_loc, path = queue.popleft()
            
            if current_loc == end_location:
                return path
            
            for neighbor in self.location_connections.get(current_loc, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None  # Путь не найден


class GameWorldManager:
    """
    Комплексная система управления игровым миром с JSON-конфигурацией
    """
    def __init__(self, config_directory="world_config"):
        self.config_directory = Path(config_directory)
        self.game_entities = {}  # Все игровые сущности
        self.entity_templates = {}  # Шаблоны для разных типов сущностей
        self.entity_schemas = {}  # Схемы валидации для разных типов
        
        self.load_world_config()
    
    def load_world_config(self):
        """
        Загружает конфигурацию игрового мира из JSON-файлов
        """
        # Загружаем шаблоны сущностей
        templates_dir = self.config_directory / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.json"):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        templates = json.load(f)
                    
                    entity_type = template_file.stem
                    self.entity_templates[entity_type] = templates
                    print(f"Загружены шаблоны {entity_type}: {len(templates)} шт.")
                except json.JSONDecodeError:
                    print(f"Ошибка чтения файла шаблонов: {template_file}")
        
        # Загружаем схемы валидации
        schemas_dir = self.config_directory / "schemas"
        if schemas_dir.exists():
            for schema_file in schemas_dir.glob("*.json"):
                try:
                    with open(schema_file, 'r', encoding='utf-8') as f:
                        schema = json.load(f)
                    
                    entity_type = schema_file.stem
                    self.entity_schemas[entity_type] = schema
                    print(f"Загружена схема для {entity_type}")
                except json.JSONDecodeError:
                    print(f"Ошибка чтения файла схемы: {schema_file}")
    
    def create_entity_from_template(self, entity_type, entity_id, **properties):
        """
        Создает игровую сущность из шаблона с дополнительными свойствами
        
        Args:
            entity_type (str): Тип сущности
            entity_id (str): ID сущности
            **properties: Дополнительные свойства для переопределения
        
        Returns:
            dict: Созданная игровая сущность
        """
        if entity_type not in self.entity_templates:
            print(f"Неизвестный тип сущности: {entity_type}")
            return None
        
        # Получаем базовый шаблон
        if entity_id not in self.entity_templates[entity_type]:
            print(f"Шаблон не найден для {entity_type}: {entity_id}")
            return None
        
        base_template = self.entity_templates[entity_type][entity_id].copy()
        
        # Применяем переопределенные свойства
        self.apply_properties(base_template, properties)
        
        # Добавляем системные поля
        entity = {
            'id': entity_id,
            'type': entity_type,
            'created_at': datetime.now().isoformat(),
            'data': base_template
        }
        
        self.game_entities[f"{entity_type}:{entity_id}"] = entity
        return entity
    
    def apply_properties(self, target_dict, updates_dict):
        """
        Рекурсивно применяет обновления к словарю
        
        Args:
            target_dict (dict): Целевой словарь
            updates_dict (dict): Словарь с обновлениями
        """
        for key, value in updates_dict.items():
            if key in target_dict and isinstance(target_dict[key], dict) and isinstance(value, dict):
                self.apply_properties(target_dict[key], value)
            else:
                target_dict[key] = value
    
    def update_entity(self, entity_id_with_type, **updates):
        """
        Обновляет свойства игровой сущности
        
        Args:
            entity_id_with_type (str): ID сущности в формате "type:id"
            **updates: Обновляемые свойства
        """
        if entity_id_with_type not in self.game_entities:
            print(f"Сущность не найдена: {entity_id_with_type}")
            return False
        
        entity = self.game_entities[entity_id_with_type]
        self.apply_properties(entity['data'], updates)
        entity['updated_at'] = datetime.now().isoformat()
        
        return True
    
    def validate_entity_data(self, entity_data, entity_type):
        """
        Проверяет корректность данных игровой сущности
        
        Args:
            entity_data (dict): Данные сущности для проверки
            entity_type (str): Тип сущности
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        if entity_type not in self.entity_schemas:
            return True, []  # Если нет схемы, считаем данные корректными
        
        schema = self.entity_schemas[entity_type]
        errors = []
        
        def validate_recursive(data, schema_part, path=""):
            if isinstance(schema_part, dict):
                if not isinstance(data, dict):
                    errors.append(f"Ожидается объект по пути {path}, получено: {type(data).__name__}")
                    return
                
                for key, value in schema_part.items():
                    if key not in data and value.get('required', False):
                        errors.append(f"Обязательное поле отсутствует по пути {path}.{key}")
                    elif key in data:
                        validate_recursive(data[key], value, f"{path}.{key}")
            elif isinstance(schema_part, list) and len(schema_part) > 0:
                if not isinstance(data, list):
                    errors.append(f"Ожидается массив по пути {path}, получено: {type(data).__name__}")
                    return
                
                for i, item in enumerate(data):
                    validate_recursive(item, schema_part[0], f"{path}[{i}]")
            elif schema_part == "string":
                if not isinstance(data, str):
                    errors.append(f"Ожидается строка по пути {path}, получено: {type(data).__name__}")
            elif schema_part == "number":
                if not isinstance(data, (int, float)):
                    errors.append(f"Ожидается число по пути {path}, получено: {type(data).__name__}")
            elif schema_part == "boolean":
                if not isinstance(data, bool):
                    errors.append(f"Ожидается булево по пути {path}, получено: {type(data).__name__}")
            elif schema_part == "object":
                if not isinstance(data, dict):
                    errors.append(f"Ожидается объект по пути {path}, получено: {type(data).__name__}")
            elif schema_part == "array":
                if not isinstance(data, list):
                    errors.append(f"Ожидается массив по пути {path}, получено: {type(data).__name__}")
        
        validate_recursive(entity_data, schema)
        return len(errors) == 0, errors
    
    def export_world_state(self, export_name, entities_filter=None):
        """
        Экспортирует состояние игрового мира в JSON-файл
        
        Args:
            export_name (str): Имя для экспорта
            entities_filter (callable): Функция для фильтрации сущностей (опционально)
        """
        export_path = self.config_directory / "exports" / f"{export_name}.json"
        export_path.parent.mkdir(exist_ok=True)
        
        filtered_entities = self.game_entities
        if entities_filter:
            filtered_entities = {k: v for k, v in self.game_entities.items() if entities_filter(k, v)}
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'game_version': '1.0.0',  # В реальной игре будет динамически получаться
            'entities': filtered_entities
        }
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Состояние мира экспортировано: {export_path}")
    
    def import_world_state(self, import_name):
        """
        Импортирует состояние игрового мира из JSON-файла
        
        Args:
            import_name (str): Имя импортируемого состояния
        """
        import_path = self.config_directory / "exports" / f"{import_name}.json"
        
        if not import_path.exists():
            print(f"Файл импорта не найден: {import_path}")
            return False
        
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            self.game_entities.update(import_data.get('entities', {}))
            print(f"Состояние мира импортировано: {import_path}")
            return True
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла импорта: {import_path}")
            return False


class EventQuestManager:
    """
    Система управления событиями и квестами с JSON-валидацией
    """
    def __init__(self, events_directory="events", quests_directory="quests", validation_schema_file="validation_schema.json"):
        self.events_directory = Path(events_directory)
        self.quests_directory = Path(quests_directory)
        self.validation_schema_file = Path(validation_schema_file)
        
        self.events = {}
        self.quests = {}
        self.player_events = {}
        self.player_quests = {}
        
        self.validation_schemas = self.load_validation_schemas()
        
        self.load_all_events()
        self.load_all_quests()
    
    def load_validation_schemas(self):
        """
        Загружает схемы валидации из JSON-файла
        
        Returns:
            dict: Словарь схем валидации
        """
        if self.validation_schema_file.exists():
            try:
                with open(self.validation_schema_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла схемы валидации: {self.validation_schema_file}")
                return {}
        else:
            # Возвращаем пустой словарь, если файл не существует
            return {}
    
    def load_all_events(self):
        """
        Загружает все игровые события из JSON-файлов
        """
        for event_file in self.events_directory.glob("*.json"):
            try:
                with open(event_file, 'r', encoding='utf-8') as f:
                    event_data = json.load(f)
                
                # Проверяем валидность данных
                is_valid, errors = self.validate_event_data(event_data)
                if is_valid:
                    event_id = event_data['id']
                    self.events[event_id] = event_data
                    print(f"Загружено событие: {event_data['name']} (ID: {event_id})")
                else:
                    print(f"Ошибка валидации события из {event_file}: {', '.join(errors)}")
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла события: {event_file}")
    
    def load_all_quests(self):
        """
        Загружает все квесты из JSON-файлов
        """
        for quest_file in self.quests_directory.glob("*.json"):
            try:
                with open(quest_file, 'r', encoding='utf-8') as f:
                    quest_data = json.load(f)
                
                # Проверяем валидность данных
                is_valid, errors = self.validate_quest_data(quest_data)
                if is_valid:
                    quest_id = quest_data['id']
                    self.quests[quest_id] = quest_data
                    print(f"Загружен квест: {quest_data['name']} (ID: {quest_id})")
                else:
                    print(f"Ошибка валидации квеста из {quest_file}: {', '.join(errors)}")
            except json.JSONDecodeError:
                print(f"Ошибка чтения файла квеста: {quest_file}")
    
    def validate_event_data(self, event_data):
        """
        Проверяет корректность данных события
        
        Args:
            event_data (dict): Данные события для проверки
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        if 'event' not in self.validation_schemas:
            return True, []  # Если нет схемы, считаем данные корректными
        
        schema = self.validation_schemas['event']
        errors = []
        
        # Проверяем обязательные поля
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in event_data:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Проверяем типы и значения полей
        properties = schema.get('properties', {})
        for field, field_schema in properties.items():
            if field in event_data:
                value = event_data[field]
                field_type = field_schema.get('type')
                
                # Проверяем тип
                if field_type == 'string' and not isinstance(value, str):
                    errors.append(f"Поле {field} должно быть строкой, получено: {type(value).__name__}")
                elif field_type == 'number' and not isinstance(value, (int, float)):
                    errors.append(f"Поле {field} должно быть числом, получено: {type(value).__name__}")
                elif field_type == 'boolean' and not isinstance(value, bool):
                    errors.append(f"Поле {field} должно быть булевым, получено: {type(value).__name__}")
                elif field_type == 'object' and not isinstance(value, dict):
                    errors.append(f"Поле {field} должно быть объектом, получено: {type(value).__name__}")
                elif field_type == 'array' and not isinstance(value, list):
                    errors.append(f"Поле {field} должно быть массивом, получено: {type(value).__name__}")
                
                # Проверяем минимальные/максимальные значения
                if 'minimum' in field_schema and isinstance(value, (int, float)):
                    if value < field_schema['minimum']:
                        errors.append(f"Значение поля {field} меньше минимально допустимого: {field_schema['minimum']}")
                
                if 'maximum' in field_schema and isinstance(value, (int, float)):
                    if value > field_schema['maximum']:
                        errors.append(f"Значение поля {field} больше максимально допустимого: {field_schema['maximum']}")
                
                # Проверяем формат даты-времени
                if 'format' in field_schema and field_schema['format'] == 'date-time':
                    try:
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        errors.append(f"Поле {field} имеет неверный формат даты-времени: {value}")
        
        return len(errors) == 0, errors
    
    def validate_quest_data(self, quest_data):
        """
        Проверяет корректность данных квеста
        
        Args:
            quest_data (dict): Данные квеста для проверки
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        if 'quest' not in self.validation_schemas:
            return True, []  # Если нет схемы, считаем данные корректными
        
        schema = self.validation_schemas['quest']
        errors = []
        
        # Проверяем обязательные поля
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in quest_data:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Проверяем типы и значения полей
        properties = schema.get('properties', {})
        for field, field_schema in properties.items():
            if field in quest_data:
                value = quest_data[field]
                field_type = field_schema.get('type')
                
                # Проверяем тип
                if field_type == 'string' and not isinstance(value, str):
                    errors.append(f"Поле {field} должно быть строкой, получено: {type(value).__name__}")
                elif field_type == 'number' and not isinstance(value, (int, float)):
                    errors.append(f"Поле {field} должно быть числом, получено: {type(value).__name__}")
                elif field_type == 'boolean' and not isinstance(value, bool):
                    errors.append(f"Поле {field} должно быть булевым, получено: {type(value).__name__}")
                elif field_type == 'object' and not isinstance(value, dict):
                    errors.append(f"Поле {field} должно быть объектом, получено: {type(value).__name__}")
                elif field_type == 'array' and not isinstance(value, list):
                    errors.append(f"Поле {field} должно быть массивом, получено: {type(value).__name__}")
        
        return len(errors) == 0, errors
    
    def schedule_event_for_player(self, player_id, event_id, custom_params=None):
        """
        Назначает событие игроку с возможностью кастомизации
        
        Args:
            player_id (str): ID игрока
            event_id (str): ID события
            custom_params (dict): Кастомные параметры для события (опционально)
        """
        if event_id not in self.events:
            print(f"Событие не найдено: {event_id}")
            return False
        
        if player_id not in self.player_events:
            self.player_events[player_id] = {}
        
        # Копируем событие и применяем кастомные параметры
        scheduled_event = self.events[event_id].copy()
        if custom_params:
            for param, value in custom_params.items():
                if param in scheduled_event:
                    scheduled_event[param] = value
        
        # Добавляем время назначения
        scheduled_event['scheduled_at'] = datetime.now().isoformat()
        
        self.player_events[player_id][event_id] = scheduled_event
        return True
    
    def assign_quest_to_player(self, player_id, quest_id, difficulty_multiplier=1.0):
        """
        Назначает квест игроку с возможностью изменения сложности
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID квеста
            difficulty_multiplier (float): Множитель сложности (опционально)
        """
        if quest_id not in self.quests:
            print(f"Квест не найден: {quest_id}")
            return False
        
        if player_id not in self.player_quests:
            self.player_quests[player_id] = {}
        
        # Копируем квест и применяем множитель сложности
        assigned_quest = self.quests[quest_id].copy()
        
        # Модифицируем цель квеста в зависимости от сложности
        if 'objective' in assigned_quest and 'target' in assigned_quest['objective']:
            original_target = assigned_quest['objective']['target']
            assigned_quest['objective']['target'] = int(original_target * difficulty_multiplier)
            assigned_quest['difficulty_multiplier'] = difficulty_multiplier
        
        # Добавляем время назначения
        assigned_quest['assigned_at'] = datetime.now().isoformat()
        assigned_quest['progress'] = 0
        assigned_quest['completed'] = False
        
        self.player_quests[player_id][quest_id] = assigned_quest
        return True


# Примеры использования классов
if __name__ == "__main__":
    print("=== Примеры использования игровых классов ===\n")
    
    # Пример использования класса GameConfig
    print("--- Класс GameConfig ---")
    config = GameConfig()
    current_resolution = config.get_setting("resolution", "width")
    print(f"Текущее разрешение по ширине: {current_resolution}")
    config.set_setting(1280, "resolution", "width")
    config.save_config()
    print()
    
    # Пример использования класса Player
    print("--- Класс Player ---")
    player = Player("Алекс", 5, 150, (10.5, 20.3))
    print(f"Игрок: {player.name}, уровень: {player.level}, здоровье: {player.health}")
    print()
    
    # Пример использования системы сохранения игрока
    print("--- Система сохранения прогресса игрока ---")
    manager = PlayerProgressManager()
    manager.save_player_progress(player, "save1")
    loaded_player = manager.load_player_progress("save1")
    if loaded_player:
        print(f"Загруженный игрок: {loaded_player.name}, уровень: {loaded_player.level}")
    print()
    
    # Пример использования класса InventoryManager
    print("--- Класс InventoryManager ---")
    inv_manager = InventoryManager()
    sample_item = {
        "id": "sword_001",
        "name": "Стальной меч",
        "type": "weapon",
        "rarity": "common",
        "properties": {
            "damage": 15,
            "durability": 100,
            "durability_max": 100
        },
        "quantity": 1,
        "equipped": False
    }
    inv_manager.add_item("player1", sample_item)
    inventory = inv_manager.get_inventory("player1")
    print(f"Инвентарь игрока: {inventory}")
    print()
    
    # Пример использования класса AchievementManager
    print("--- Класс AchievementManager ---")
    ach_manager = AchievementManager()
    ach_manager.update_achievement_progress("player1", "first_steps", 1)
    ach_manager.grant_achievement("player1", "first_steps")
    print()
    
    print("Все игровые классы успешно реализованы и готовы к использованию!")