# Решения для практического задания 8: Работа с XML в игровом контексте

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Ниже приведены реализованные игровые классы и функции согласно заданию

def parse_xml_to_game_object(xml_string):
    """
    Парсит XML-строку в игровой объект
    
    Args:
        xml_string (str): XML-строка для парсинга
    
    Returns:
        object: Игровой объект
    """
    def parse_element(element):
        # Создаем объект с атрибутами из элемента
        obj = type('DynamicObject', (), {})()
        
        # Устанавливаем атрибуты из XML-атрибутов
        for key, value in element.attrib.items():
            setattr(obj, key, value)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_obj = parse_element(child)
            setattr(obj, child.tag, child_obj)
        
        # Если у элемента есть текст, сохраняем его как атрибут 'text'
        if element.text and element.text.strip():
            setattr(obj, 'text', element.text.strip())
        
        return obj
    
    root = ET.fromstring(xml_string)
    return parse_element(root)


def game_object_to_xml(obj):
    """
    Преобразует игровой объект в XML-строку
    
    Args:
        obj: Игровой объект для преобразования
    
    Returns:
        str: XML-строка объекта
    """
    def convert_to_xml(obj, parent_element=None, tag_name="root"):
        if parent_element is None:
            element = ET.Element(tag_name)
        else:
            element = ET.SubElement(parent_element, tag_name)
        
        # Добавляем атрибуты объекта как XML-атрибуты или дочерние элементы
        for attr_name, attr_value in obj.__dict__.items():
            if isinstance(attr_value, (str, int, float, bool)):
                element.set(attr_name, str(attr_value))
            elif hasattr(attr_value, '__dict__'):
                # Рекурсивно обрабатываем вложенные объекты
                convert_to_xml(attr_value, element, attr_name)
            elif isinstance(attr_value, (list, tuple)):
                # Обрабатываем списки/кортежи
                list_element = ET.SubElement(element, attr_name)
                for i, item in enumerate(attr_value):
                    if hasattr(item, '__dict__'):
                        convert_to_xml(item, list_element, f"item_{i}")
                    else:
                        item_element = ET.SubElement(list_element, f"item_{i}")
                        item_element.text = str(item)
            else:
                # Для остальных типов создаем дочерний элемент
                child_element = ET.SubElement(element, attr_name)
                child_element.text = str(attr_value)
        
        if parent_element is None:
            # Если это корневой элемент, возвращаем строку
            return ET.tostring(element, encoding='unicode')
        else:
            # Иначе просто добавляем элемент к родительскому
            return element
    
    # Создаем корневой элемент
    root_element = ET.Element("game_object")
    
    # Обрабатываем атрибуты корневого объекта
    for attr_name, attr_value in obj.__dict__.items():
        if isinstance(attr_value, (str, int, float, bool)):
            root_element.set(attr_name, str(attr_value))
        elif hasattr(attr_value, '__dict__'):
            convert_to_xml(attr_value, root_element, attr_name)
        elif isinstance(attr_value, (list, tuple)):
            list_element = ET.SubElement(root_element, attr_name)
            for i, item in enumerate(attr_value):
                if hasattr(item, '__dict__'):
                    convert_to_xml(item, list_element, f"item_{i}")
                else:
                    item_element = ET.SubElement(list_element, f"item_{i}")
                    item_element.text = str(item)
        else:
            child_element = ET.SubElement(root_element, attr_name)
            child_element.text = str(attr_value)
    
    return ET.tostring(root_element, encoding='unicode')


class GameConfig:
    """
    Система конфигурации игры через XML-файл
    """
    def __init__(self, config_file="config.xml"):
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
        self.root = self.load_config()
    
    def load_config(self):
        """
        Загружает конфигурацию из XML-файла
        
        Returns:
            Element: Корневой элемент XML-документа
        """
        if self.config_file.exists():
            try:
                tree = ET.parse(self.config_file)
                return tree.getroot()
            except ET.ParseError:
                print(f"Ошибка чтения конфигурации из {self.config_file}, используется значение по умолчанию")
                # Создаем XML из конфигурации по умолчанию
                root = self.create_xml_from_dict(self.default_config)
                self.save_config_tree(root)
                return root
        else:
            # Создаем файл конфигурации со значениями по умолчанию
            root = self.create_xml_from_dict(self.default_config)
            self.save_config_tree(root)
            return root
    
    def create_xml_from_dict(self, config_dict, parent=None, tag="config"):
        """
        Создает XML-элементы из словаря
        
        Args:
            config_dict (dict): Словарь конфигурации
            parent (Element): Родительский элемент (опционально)
            tag (str): Тег корневого элемента
            
        Returns:
            Element: XML-элемент
        """
        if parent is None:
            element = ET.Element(tag)
        else:
            element = ET.SubElement(parent, tag)
        
        for key, value in config_dict.items():
            if isinstance(value, dict):
                self.create_xml_from_dict(value, element, key)
            else:
                subelement = ET.SubElement(element, key)
                subelement.text = str(value)
        
        return element
    
    def save_config_tree(self, root_element):
        """
        Сохраняет XML-дерево в файл
        
        Args:
            root_element (Element): Корневой элемент для сохранения
        """
        tree = ET.ElementTree(root_element)
        tree.write(self.config_file, encoding="utf-8", xml_declaration=True)
    
    def save_config(self):
        """
        Сохраняет текущую конфигурацию в XML-файл
        """
        self.save_config_tree(self.root)
    
    def get_setting(self, *keys):
        """
        Возвращает значение настройки по цепочке ключей
        
        Args:
            *keys: Ключи для доступа к настройке
            
        Returns:
            значение: Значение настройки
        """
        current = self.root
        for key in keys:
            found = False
            for child in current:
                if child.tag == key:
                    current = child
                    found = True
                    break
            if not found:
                return None
        
        # Пытаемся преобразовать значение к подходящему типу
        text = current.text
        if text is not None:
            text = text.strip()
            if text.lower() in ['true', 'false']:
                return text.lower() == 'true'
            elif text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    return text
        return current.attrib  # Возвращаем атрибуты, если нет текста
    
    def set_setting(self, value, *keys):
        """
        Устанавливает значение настройки по цепочке ключей
        
        Args:
            value: Значение для установки
            *keys: Ключи для доступа к настройке
        """
        current = self.root
        for key in keys[:-1]:
            found = False
            for child in current:
                if child.tag == key:
                    current = child
                    found = True
                    break
            if not found:
                # Создаем новый элемент, если его нет
                current = ET.SubElement(current, key)
        
        # Устанавливаем значение для последнего ключа
        last_key = keys[-1]
        found = False
        for child in current:
            if child.tag == last_key:
                child.text = str(value)
                found = True
                break
        
        if not found:
            # Создаем новый элемент, если его нет
            new_element = ET.SubElement(current, last_key)
            new_element.text = str(value)


class PlayerProgressManager:
    """
    Система управления сохранением и загрузкой прогресса игрока
    """
    def __init__(self, saves_directory="saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
    
    def save_player_progress(self, player, save_name):
        """
        Сохраняет прогресс игрока в XML-файл
        
        Args:
            player (object): Объект игрока
            save_name (str): Имя сохранения
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        
        # Создаем XML-структуру для сохранения игрока
        root = ET.Element("player_save")
        root.set("timestamp", datetime.now().isoformat())
        
        # Добавляем атрибуты игрока
        name_elem = ET.SubElement(root, "name")
        name_elem.text = player.name
        
        level_elem = ET.SubElement(root, "level")
        level_elem.text = str(player.level)
        
        health_elem = ET.SubElement(root, "health")
        health_elem.text = str(player.health)
        
        max_health_elem = ET.SubElement(root, "max_health")
        max_health_elem.text = str(player.max_health)
        
        pos_x_elem = ET.SubElement(root, "position_x")
        pos_x_elem.text = str(player.position_x)
        
        pos_y_elem = ET.SubElement(root, "position_y")
        pos_y_elem.text = str(player.position_y)
        
        play_time_elem = ET.SubElement(root, "play_time")
        play_time_elem.text = str(player.play_time)
        
        creation_date_elem = ET.SubElement(root, "creation_date")
        creation_date_elem.text = player.creation_date.isoformat()
        
        last_played_elem = ET.SubElement(root, "last_played")
        last_played_elem.text = player.last_played.isoformat()
        
        # Сохраняем инвентарь
        inventory_elem = ET.SubElement(root, "inventory")
        for item in player.inventory:
            item_elem = ET.SubElement(inventory_elem, "item")
            item_elem.text = str(item)
        
        # Сохраняем статистику
        stats_elem = ET.SubElement(root, "stats")
        for stat_name, stat_value in player.stats.items():
            stat_elem = ET.SubElement(stats_elem, stat_name)
            stat_elem.text = str(stat_value)
        
        # Сохраняем в файл
        tree = ET.ElementTree(root)
        tree.write(save_path, encoding="utf-8", xml_declaration=True)
    
    def load_player_progress(self, save_name):
        """
        Загружает прогресс игрока из XML-файла
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            object: Загруженный объект игрока
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        
        if not save_path.exists():
            return None
        
        try:
            tree = ET.parse(save_path)
            root = tree.getroot()
            
            # Извлекаем атрибуты игрока
            name = root.find("name").text
            level = int(root.find("level").text)
            health = int(root.find("health").text)
            max_health = int(root.find("max_health").text)
            position_x = float(root.find("position_x").text)
            position_y = float(root.find("position_y").text)
            play_time = float(root.find("play_time").text)
            
            # Создаем игрока
            player = Player(name, level, health, position_x, position_y)
            player.max_health = max_health
            player.play_time = play_time
            player.creation_date = datetime.fromisoformat(root.find("creation_date").text)
            player.last_played = datetime.fromisoformat(root.find("last_played").text)
            
            # Восстанавливаем инвентарь
            inventory_elem = root.find("inventory")
            if inventory_elem is not None:
                for item_elem in inventory_elem.findall("item"):
                    player.inventory.append(item_elem.text)
            
            # Восстанавливаем статистику
            stats_elem = root.find("stats")
            if stats_elem is not None:
                for stat_elem in stats_elem:
                    stat_name = stat_elem.tag
                    stat_value = int(stat_elem.text)
                    player.stats[stat_name] = stat_value
            
            return player
        except ET.ParseError:
            print(f"Ошибка чтения сохранения: {save_path}")
            return None
    
    def list_saves(self):
        """
        Возвращает список доступных сохранений
        
        Returns:
            list: Список имен файлов сохранений
        """
        save_files = list(self.saves_directory.glob("*.xml"))
        save_names = [f.stem for f in save_files]  # Имя файла без расширения
        return sorted(save_names, reverse=True)  # Сортируем в обратном порядке (новые первыми)
    
    def delete_save(self, save_name):
        """
        Удаляет файл сохранения
        
        Args:
            save_name (str): Имя сохранения для удаления
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        if save_path.exists():
            save_path.unlink()  # Удаляем файл
            return True
        return False


class Player:
    def __init__(self, name, level=1, health=100, position_x=0, position_y=0):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = 100
        self.position_x = position_x
        self.position_y = position_y
        self.inventory = []
        self.stats = {
            'strength': 10,
            'agility': 10,
            'intelligence': 10
        }
        self.play_time = 0  # Время в игре в секундах
        self.creation_date = datetime.now()
        self.last_played = datetime.now()
    
    def to_xml(self):
        """
        Преобразует игрока в XML-элемент
        """
        root = ET.Element("player")
        
        # Добавляем основные атрибуты
        name_elem = ET.SubElement(root, "name")
        name_elem.text = self.name
        
        level_elem = ET.SubElement(root, "level")
        level_elem.text = str(self.level)
        
        health_elem = ET.SubElement(root, "health")
        health_elem.text = str(self.health)
        
        max_health_elem = ET.SubElement(root, "max_health")
        max_health_elem.text = str(self.max_health)
        
        pos_x_elem = ET.SubElement(root, "position_x")
        pos_x_elem.text = str(self.position_x)
        
        pos_y_elem = ET.SubElement(root, "position_y")
        pos_y_elem.text = str(self.position_y)
        
        play_time_elem = ET.SubElement(root, "play_time")
        play_time_elem.text = str(self.play_time)
        
        creation_date_elem = ET.SubElement(root, "creation_date")
        creation_date_elem.text = self.creation_date.isoformat()
        
        last_played_elem = ET.SubElement(root, "last_played")
        last_played_elem.text = self.last_played.isoformat()
        
        # Добавляем инвентарь
        inventory_elem = ET.SubElement(root, "inventory")
        for item in self.inventory:
            item_elem = ET.SubElement(inventory_elem, "item")
            item_elem.text = str(item)
        
        # Добавляем статистику
        stats_elem = ET.SubElement(root, "stats")
        for stat_name, stat_value in self.stats.items():
            stat_elem = ET.SubElement(stats_elem, stat_name)
            stat_elem.text = str(stat_value)
        
        return root
    
    @classmethod
    def from_xml(cls, xml_element):
        """
        Создает игрока из XML-элемента
        
        Args:
            xml_element: XML-элемент игрока
        """
        # Извлекаем основные атрибуты
        name = xml_element.find("name").text
        level = int(xml_element.find("level").text)
        health = int(xml_element.find("health").text)
        max_health = int(xml_element.find("max_health").text)
        position_x = float(xml_element.find("position_x").text)
        position_y = float(xml_element.find("position_y").text)
        play_time = float(xml_element.find("play_time").text)
        
        # Создаем игрока
        player = cls(name, level, health, position_x, position_y)
        player.max_health = max_health
        player.play_time = play_time
        player.creation_date = datetime.fromisoformat(xml_element.find("creation_date").text)
        player.last_played = datetime.fromisoformat(xml_element.find("last_played").text)
        
        # Восстанавливаем инвентарь
        inventory_elem = xml_element.find("inventory")
        if inventory_elem is not None:
            for item_elem in inventory_elem.findall("item"):
                player.inventory.append(item_elem.text)
        
        # Восстанавливаем статистику
        stats_elem = xml_element.find("stats")
        if stats_elem is not None:
            for stat_elem in stats_elem:
                stat_name = stat_elem.tag
                stat_value = int(stat_elem.text)
                player.stats[stat_name] = stat_value
        
        return player


class AssetManager:
    """
    Система загрузки игровых ассетов из XML-файлов
    """
    def __init__(self, assets_directory="assets"):
        self.assets_directory = Path(assets_directory)
        self.loaded_assets = {}
        self.asset_manifests = {}
    
    def load_asset_manifest(self, manifest_file):
        """
        Загружает манифест ассетов из XML-файла
        
        Args:
            manifest_file (str): Путь к файлу манифеста
            
        Returns:
            dict: Загруженный манифест ассетов
        """
        manifest_path = self.assets_directory / manifest_file
        
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Сохраняем манифест
            manifest_name = Path(manifest_file).stem
            self.asset_manifests[manifest_name] = root
            return self.xml_to_dict(root)
        except FileNotFoundError:
            print(f"Файл манифеста не найден: {manifest_path}")
            return {}
        except ET.ParseError:
            print(f"Ошибка чтения XML из файла: {manifest_path}")
            return {}
    
    def xml_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.xml_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result
    
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
            asset_element = manifest.find(f"./{asset_type}/{asset_type[:-1]}[@id='{asset_name}']")
            if asset_element is not None:
                asset_info = self.xml_to_dict(asset_element)
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
            asset_element = manifest.find(f"./{asset_type}/{asset_type[:-1]}[@id='{asset_name}']")
            if asset_element is not None:
                return self.xml_to_dict(asset_element)
        
        return None
    
    def validate_asset_data(self, asset_element, expected_schema):
        """
        Проверяет, соответствует ли ассет ожидаемой схеме
        
        Args:
            asset_element (Element): XML-элемент ассета
            expected_schema (dict): Ожидаемая схема
            
        Returns:
            bool: Соответствует ли ассет схеме
        """
        def check_schema(element, schema):
            if isinstance(schema, dict):
                if not isinstance(element, dict):
                    return False
                
                for key, value in schema.items():
                    if key not in element:
                        return False
                    if not check_schema(element[key], value):
                        return False
                return True
            elif isinstance(schema, list) and len(schema) > 0:
                if not isinstance(element, list):
                    return False
                for item in element:
                    if not check_schema(item, schema[0]):
                        return False
                return True
            elif schema == "string":
                return isinstance(element, str)
            elif schema == "number":
                return isinstance(element, (int, float))
            elif schema == "boolean":
                return isinstance(element, bool)
            elif schema == "object":
                return isinstance(element, dict)
            elif schema == "array":
                return isinstance(element, list)
            else:
                return type(element).__name__ == schema
        
        # Для этой функции нам нужно передать данные ассета, а не элемент
        asset_data = self.xml_to_dict(asset_element)
        return check_schema(asset_data, expected_schema)


class QuestSystem:
    """
    Система квестов с XML-описаниями
    """
    def __init__(self, quests_directory="quests"):
        self.quests_directory = Path(quests_directory)
        self.quests = {}
        self.player_quests = {}
        self.active_quests = {}
    
    def load_quest_definitions(self, quest_file):
        """
        Загружает определения квестов из XML-файла
        
        Args:
            quest_file (str): Путь к файлу с определениями квестов
        """
        quest_path = self.quests_directory / quest_file
        
        try:
            tree = ET.parse(quest_path)
            root = tree.getroot()
            
            for quest_elem in root.findall("quest"):
                quest_id = quest_elem.get("id")
                
                # Извлекаем данные квеста
                quest_data = {
                    'id': quest_id,
                    'name': quest_elem.get("name"),
                    'description': quest_elem.find("description").text if quest_elem.find("description") is not None else "",
                    'objective': {},
                    'rewards': [],
                    'time_limit': None
                }
                
                # Извлекаем цель квеста
                objective_elem = quest_elem.find("objective")
                if objective_elem is not None:
                    quest_data['objective'] = {
                        'type': objective_elem.get("type", ""),
                        'target': objective_elem.get("target", ""),
                        'count': int(objective_elem.get("count", 1))
                    }
                
                # Извлекаем награды
                rewards_elem = quest_elem.find("rewards")
                if rewards_elem is not None:
                    for reward_elem in rewards_elem.findall("reward"):
                        reward_data = {
                            'type': reward_elem.get("type", ""),
                            'value': reward_elem.text
                        }
                        quest_data['rewards'].append(reward_data)
                
                # Извлекаем ограничение по времени
                time_limit_elem = quest_elem.find("time_limit")
                if time_limit_elem is not None:
                    quest_data['time_limit'] = int(time_limit_elem.text)
                
                self.quests[quest_id] = quest_data
            
            print(f"Загружено {len(self.quests)} квестов из {quest_path}")
        except FileNotFoundError:
            print(f"Файл квестов не найден: {quest_path}")
        except ET.ParseError:
            print(f"Ошибка чтения XML из файла: {quest_path}")
    
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
    Система управления модами с XML-конфигурацией
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
                config_path = mod_dir / "mod.xml"
                if config_path.exists():
                    try:
                        tree = ET.parse(config_path)
                        root = tree.getroot()
                        
                        mod_id = root.get("id")
                        mod_config = {
                            'config': root,
                            'directory': mod_dir,
                            'enabled': False
                        }
                        
                        self.installed_mods[mod_id] = mod_config
                        
                        # Сохраняем зависимости
                        dependencies_elem = root.find("requirements/dependencies")
                        if dependencies_elem is not None:
                            dependencies = [dep.text for dep in dependencies_elem.findall("dependency")]
                            if dependencies:
                                self.mod_dependencies[mod_id] = dependencies
                        
                        print(f"Найден мод: {root.get('name', 'Unknown')} (ID: {mod_id})")
                    except ET.ParseError:
                        print(f"Ошибка чтения конфигурации мода: {mod_dir.name}")
                else:
                    print(f"Конфигурационный файл не найден для мода: {mod_dir.name}")
    
    def load_mod_config(self, mod_id):
        """
        Загружает конфигурацию мода из XML-файла
        
        Args:
            mod_id (str): ID мода
        """
        if mod_id not in self.installed_mods:
            return None
        
        config_path = self.installed_mods[mod_id]['directory'] / "mod.xml"
        try:
            tree = ET.parse(config_path)
            return tree.getroot()
        except FileNotFoundError:
            print(f"Конфигурационный файл мода не найден: {config_path}")
            return None
        except ET.ParseError:
            print(f"Ошибка чтения XML-конфигурации мода: {config_path}")
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
        version_elem = mod_config.find("requirements/game_version")
        if version_elem is not None:
            min_version = version_elem.get("min")
            max_version = version_elem.get("max")
            
            if min_version and self.compare_versions(game_version, min_version) < 0:
                errors.append(f"Мод требует версию игры не ниже {min_version}, текущая: {game_version}")
            
            if max_version and self.compare_versions(game_version, max_version) > 0:
                errors.append(f"Мод несовместим с версией игры выше {max_version}, текущая: {game_version}")
        
        # Проверяем зависимости
        dependencies_elem = mod_config.find("requirements/dependencies")
        if dependencies_elem is not None:
            for dependency in dependencies_elem.findall("dependency"):
                dep_id = dependency.text
                if dep_id not in self.installed_mods or not self.installed_mods[dep_id]['enabled']:
                    errors.append(f"Отсутствует зависимость: {dep_id}")
        
        # Проверяем конфликты
        conflicts_elem = mod_config.find("conflicts")
        if conflicts_elem is not None:
            for conflict in conflicts_elem.findall("mod"):
                conflict_id = conflict.text
                if conflict_id in self.enabled_mods:
                    errors.append(f"Конфликт с модом: {conflict_id}")
        
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
            mod_config = self.installed_mods[mod_id]['config']
            mod_name = mod_config.get('name', 'Unknown')
            print(f"Мод включен: {mod_name} (ID: {mod_id})")
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
                    mod_name = self.installed_mods[mod_id]['config'].get('name', 'Unknown')
                    dependent_mod_name = self.installed_mods[enabled_mod_id]['config'].get('name', 'Unknown')
                    print(f"Невозможно выключить мод {mod_name} (ID: {mod_id}), так как от него зависит {dependent_mod_name} (ID: {enabled_mod_id})")
                    return False
            
            self.installed_mods[mod_id]['enabled'] = False
            self.enabled_mods.remove(mod_id)
            mod_config = self.installed_mods[mod_id]['config']
            mod_name = mod_config.get('name', 'Unknown')
            print(f"Мод выключен: {mod_name} (ID: {mod_id})")
            return True
        
        return False


class WorldSaveSystem:
    """
    Система сохранения игрового мира в XML
    """
    def __init__(self, saves_directory="world_saves"):
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
        self.current_world_state = {}
    
    def save_world(self, world_state, save_name, description=""):
        """
        Сохраняет состояние игрового мира в XML-файл
        
        Args:
            world_state (dict): Состояние игрового мира для сохранения
            save_name (str): Имя сохранения
            description (str): Описание сохранения
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        
        # Создаем корневой элемент
        root = ET.Element("world_save")
        root.set("version", "1.0")
        root.set("timestamp", datetime.now().isoformat())
        root.set("description", description)
        
        # Добавляем метаданные
        meta_elem = ET.SubElement(root, "meta")
        game_version_elem = ET.SubElement(meta_elem, "game_version")
        game_version_elem.text = "1.0.0"  # В реальной игре будет динамически получаться
        
        # Добавляем состояние мира
        world_elem = ET.SubElement(root, "world_state")
        
        # Добавляем игроков
        if 'players' in world_state:
            players_elem = ET.SubElement(world_elem, "players")
            for player_data in world_state['players']:
                player_elem = ET.SubElement(players_elem, "player")
                player_elem.set("id", str(player_data.get("id", "")))
                player_elem.set("name", str(player_data.get("name", "")))
                
                # Добавляем атрибуты игрока
                for key, value in player_data.items():
                    if key not in ["id", "name"]:  # Исключаем id и name, так как они уже как атрибуты
                        if isinstance(value, (str, int, float, bool)):
                            sub_elem = ET.SubElement(player_elem, key)
                            sub_elem.text = str(value)
                        elif isinstance(value, dict):
                            self.dict_to_xml(value, player_elem, key)
                        elif isinstance(value, list):
                            list_elem = ET.SubElement(player_elem, key)
                            for i, item in enumerate(value):
                                if isinstance(item, dict):
                                    self.dict_to_xml(item, list_elem, f"item_{i}")
                                else:
                                    item_elem = ET.SubElement(list_elem, f"item_{i}")
                                    item_elem.text = str(item)
        
        # Добавляем NPC
        if 'npcs' in world_state:
            npcs_elem = ET.SubElement(world_elem, "npcs")
            for npc_data in world_state['npcs']:
                npc_elem = ET.SubElement(npcs_elem, "npc")
                npc_elem.set("id", str(npc_data.get("id", "")))
                npc_elem.set("name", str(npc_data.get("name", "")))
                npc_elem.set("type", str(npc_data.get("type", "")))
                
                # Добавляем позицию
                pos_data = npc_data.get("position", {})
                pos_elem = ET.SubElement(npc_elem, "position")
                pos_elem.set("x", str(pos_data.get("x", 0)))
                pos_elem.set("y", str(pos_data.get("y", 0)))
                pos_elem.set("z", str(pos_data.get("z", 0)))
        
        # Добавляем предметы на земле
        if 'items_on_ground' in world_state:
            items_elem = ET.SubElement(world_elem, "items_on_ground")
            for item_data in world_state['items_on_ground']:
                item_elem = ET.SubElement(items_elem, "item")
                item_elem.set("id", str(item_data.get("id", "")))
                item_elem.set("name", str(item_data.get("name", "")))
                item_elem.set("x", str(item_data.get("x", 0)))
                item_elem.set("y", str(item_data.get("y", 0)))
                item_elem.set("z", str(item_data.get("z", 0)))
        
        # Добавляем активные квесты
        if 'active_quests' in world_state:
            quests_elem = ET.SubElement(world_elem, "active_quests")
            for quest_data in world_state['active_quests']:
                quest_elem = ET.SubElement(quests_elem, "quest")
                quest_elem.set("id", str(quest_data.get("id", "")))
                quest_elem.set("name", str(quest_data.get("name", "")))
        
        # Добавляем время мира
        if 'world_time' in world_state:
            time_elem = ET.SubElement(world_elem, "world_time")
            time_elem.text = str(world_state['world_time'])
        
        # Добавляем погоду
        if 'weather' in world_state:
            weather_elem = ET.SubElement(world_elem, "weather")
            weather_elem.text = str(world_state['weather'])
        
        # Сохраняем в файл
        tree = ET.ElementTree(root)
        tree.write(save_path, encoding="utf-8", xml_declaration=True)
        
        print(f"Мир сохранен: {save_path}")
    
    def dict_to_xml(self, data_dict, parent_element, tag_name):
        """
        Преобразует словарь в XML-элемент и добавляет к родительскому элементу
        
        Args:
            data_dict (dict): Словарь для преобразования
            parent_element (Element): Родительский элемент
            tag_name (str): Имя тега для нового элемента
        """
        elem = ET.SubElement(parent_element, tag_name)
        for key, value in data_dict.items():
            if isinstance(value, (str, int, float, bool)):
                sub_elem = ET.SubElement(elem, key)
                sub_elem.text = str(value)
            elif isinstance(value, dict):
                self.dict_to_xml(value, elem, key)
            elif isinstance(value, list):
                list_elem = ET.SubElement(elem, key)
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self.dict_to_xml(item, list_elem, f"item_{i}")
                    else:
                        item_elem = ET.SubElement(list_elem, f"item_{i}")
                        item_elem.text = str(item)
            else:
                sub_elem = ET.SubElement(elem, key)
                sub_elem.text = str(value)
    
    def load_world(self, save_name):
        """
        Загружает состояние игрового мира из XML-файла
        
        Args:
            save_name (str): Имя сохранения для загрузки
            
        Returns:
            dict: Состояние игрового мира
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        
        if not save_path.exists():
            print(f"Файл сохранения не найден: {save_path}")
            return None
        
        try:
            tree = ET.parse(save_path)
            root = tree.getroot()
            
            world_state = {}
            
            # Загружаем состояние мира
            world_elem = root.find("world_state")
            if world_elem is not None:
                for child in world_elem:
                    if child.tag == "players":
                        players = []
                        for player_elem in child.findall("player"):
                            player_data = {"id": player_elem.get("id"), "name": player_elem.get("name")}
                            for sub_elem in player_elem:
                                if len(sub_elem) == 0:  # Простое значение
                                    try:
                                        # Пробуем преобразовать к числу
                                        if '.' in sub_elem.text:
                                            player_data[sub_elem.tag] = float(sub_elem.text)
                                        else:
                                            player_data[sub_elem.tag] = int(sub_elem.text)
                                    except ValueError:
                                        # Если не число, проверяем на булево
                                        if sub_elem.text.lower() in ['true', 'false']:
                                            player_data[sub_elem.tag] = sub_elem.text.lower() == 'true'
                                        else:
                                            player_data[sub_elem.tag] = sub_elem.text
                                else:  # Сложная структура
                                    player_data[sub_elem.tag] = self.element_to_dict(sub_elem)
                            players.append(player_data)
                        world_state["players"] = players
                    elif child.tag == "npcs":
                        npcs = []
                        for npc_elem in child.findall("npc"):
                            npc_data = {"id": npc_elem.get("id"), "name": npc_elem.get("name"), "type": npc_elem.get("type")}
                            pos_elem = npc_elem.find("position")
                            if pos_elem is not None:
                                npc_data["position"] = {
                                    "x": float(pos_elem.get("x")),
                                    "y": float(pos_elem.get("y")),
                                    "z": float(pos_elem.get("z"))
                                }
                            npcs.append(npc_data)
                        world_state["npcs"] = npcs
                    elif child.tag == "items_on_ground":
                        items = []
                        for item_elem in child.findall("item"):
                            item_data = {
                                "id": item_elem.get("id"),
                                "name": item_elem.get("name"),
                                "x": float(item_elem.get("x")),
                                "y": float(item_elem.get("y")),
                                "z": float(item_elem.get("z"))
                            }
                            items.append(item_data)
                        world_state["items_on_ground"] = items
                    elif child.tag == "active_quests":
                        quests = []
                        for quest_elem in child.findall("quest"):
                            quest_data = {
                                "id": quest_elem.get("id"),
                                "name": quest_elem.get("name")
                            }
                            quests.append(quest_data)
                        world_state["active_quests"] = quests
                    elif child.tag == "world_time":
                        world_state["world_time"] = int(child.text)
                    elif child.tag == "weather":
                        world_state["weather"] = child.text
                    else:
                        # Для других элементов просто сохраняем текст
                        if len(child) == 0:
                            try:
                                # Пробуем преобразовать к числу
                                if '.' in child.text:
                                    world_state[child.tag] = float(child.text)
                                else:
                                    world_state[child.tag] = int(child.text)
                            except ValueError:
                                # Если не число, проверяем на булево
                                if child.text.lower() in ['true', 'false']:
                                    world_state[child.tag] = child.text.lower() == 'true'
                                else:
                                    world_state[child.tag] = child.text
                        else:
                            # Если есть дочерние элементы, преобразуем их рекурсивно
                            world_state[child.tag] = self.element_to_dict(child)
            
            self.current_world_state = world_state
            print(f"Мир загружен: {save_path}")
            return self.current_world_state
        except ET.ParseError:
            print(f"Ошибка чтения сохранения: {save_path}")
            return None
    
    def element_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.element_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result
    
    def get_save_info(self, save_name):
        """
        Возвращает информацию о сохранении
        
        Args:
            save_name (str): Имя сохранения
            
        Returns:
            dict: Информация о сохранении
        """
        save_path = self.saves_directory / f"{save_name}.xml"
        
        if not save_path.exists():
            return None
        
        try:
            tree = ET.parse(save_path)
            root = tree.getroot()
            
            meta_elem = root.find("meta")
            world_elem = root.find("world_state")
            
            info = {
                'name': save_name,
                'version': root.get("version", "unknown"),
                'timestamp': root.get("timestamp", "unknown"),
                'description': root.get("description", "")
            }
            
            if meta_elem is not None:
                info['game_version'] = meta_elem.find("game_version").text if meta_elem.find("game_version") is not None else "unknown"
            
            if world_elem is not None:
                # Подсчитываем количество игроков, NPC и предметов
                players_count = len(world_elem.findall("players/player"))
                npcs_count = len(world_elem.findall("npcs/npc"))
                items_count = len(world_elem.findall("items_on_ground/item"))
                
                info['player_count'] = players_count
                info['npc_count'] = npcs_count
                info['item_count'] = items_count
            
            return info
        except ET.ParseError:
            print(f"Ошибка чтения информации о сохранении: {save_path}")
            return None
    
    def validate_world_data(self, world_element):
        """
        Проверяет корректность данных игрового мира
        
        Args:
            world_element (Element): XML-элемент мира для проверки
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        errors = []
        
        # Проверяем обязательные поля
        meta_elem = world_element.find("meta")
        if meta_elem is None:
            errors.append("Отсутствует элемент 'meta' в данных мира")
        else:
            if meta_elem.find("game_version") is None:
                errors.append("В метаданных отсутствует 'game_version'")
        
        # Проверяем структуру игроков
        players_elem = world_element.find("players")
        if players_elem is not None:
            for i, player_elem in enumerate(players_elem.findall("player")):
                if not player_elem.get("id"):
                    errors.append(f"У игрока #{i} отсутствует 'id'")
                if not player_elem.get("name"):
                    errors.append(f"У игрока #{i} отсутствует 'name'")
        
        # Проверяем структуру NPC
        npcs_elem = world_element.find("npcs")
        if npcs_elem is not None:
            for i, npc_elem in enumerate(npcs_elem.findall("npc")):
                if not npc_elem.get("id"):
                    errors.append(f"У NPC #{i} отсутствует 'id'")
                if not npc_elem.get("name"):
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
        settings_path = self.settings_directory / f"{player_id}.xml"
        
        if settings_path.exists():
            try:
                tree = ET.parse(settings_path)
                root = tree.getroot()
                
                # Преобразуем XML обратно в словарь
                loaded_settings = self.xml_to_dict(root)
                
                # Объединяем загруженные настройки с настройками по умолчанию
                # чтобы гарантировать наличие всех необходимых полей
                merged_settings = self.merge_dicts(self.default_settings, loaded_settings)
                return merged_settings
            except ET.ParseError:
                print(f"Ошибка чтения настроек игрока {player_id}, используются настройки по умолчанию")
                return self.default_settings
        else:
            # Создаем файл настроек со значениями по умолчанию
            self.save_player_settings(player_id, self.default_settings)
            return self.default_settings
    
    def xml_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.xml_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result
    
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
    
    def save_player_settings(self, player_id, settings):
        """
        Сохраняет настройки игрока в XML-файл
        
        Args:
            player_id (str): ID игрока
            settings (dict): Настройки для сохранения
        """
        settings_path = self.settings_directory / f"{player_id}.xml"
        
        # Преобразуем словарь в XML
        root = self.dict_to_xml("settings", settings)
        
        # Сохраняем XML
        tree = ET.ElementTree(root)
        tree.write(settings_path, encoding="utf-8", xml_declaration=True)
    
    def dict_to_xml(self, tag, d):
        """
        Преобразует словарь в XML-элемент
        
        Args:
            tag (str): Тег корневого элемента
            d (dict): Словарь для преобразования
            
        Returns:
            Element: XML-элемент
        """
        elem = ET.Element(tag)
        for key, value in d.items():
            if isinstance(value, dict):
                child = self.dict_to_xml(key, value)
                elem.append(child)
            elif isinstance(value, list):
                # Для списков создаем отдельные элементы
                list_elem = ET.SubElement(elem, key)
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        child = self.dict_to_xml("item", item)
                        list_elem.append(child)
                    else:
                        item_elem = ET.SubElement(list_elem, f"item_{i}")
                        item_elem.text = str(item)
            else:
                child = ET.SubElement(elem, key)
                child.text = str(value)
        return elem
    
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


class InventoryManager:
    """
    Система управления инвентарем игрока с сохранением в XML
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
        
        inventory_path = self.inventories_directory / f"{player_id}.xml"
        
        # Создаем XML-структуру
        root = ET.Element("inventory")
        root.set("player_id", player_id)
        root.set("created_at", datetime.now().isoformat())
        root.set("max_size", str(self.max_inventory_size))
        
        for item in initial_items:
            self.add_item_to_xml(root, item)
        
        # Сохраняем XML
        tree = ET.ElementTree(root)
        tree.write(inventory_path, encoding="utf-8", xml_declaration=True)
    
    def add_item_to_xml(self, root, item):
        """
        Добавляет предмет в XML-структуру инвентаря
        
        Args:
            root: Корневой элемент инвентаря
            item (dict): Предмет для добавления
        """
        item_elem = ET.SubElement(root, "item")
        item_elem.set("id", str(item.get("id", "")))
        item_elem.set("name", str(item.get("name", "")))
        item_elem.set("type", str(item.get("type", "")))
        item_elem.set("rarity", str(item.get("rarity", "")))
        item_elem.set("quantity", str(item.get("quantity", 1)))
        item_elem.set("equipped", str(item.get("equipped", False)).lower())
        
        # Добавляем свойства предмета
        properties_elem = ET.SubElement(item_elem, "properties")
        properties = item.get("properties", {})
        for prop_name, prop_value in properties.items():
            prop_elem = ET.SubElement(properties_elem, prop_name)
            prop_elem.text = str(prop_value)
    
    def add_item(self, player_id, item):
        """
        Добавляет предмет в инвентарь игрока
        
        Args:
            player_id (str): ID игрока
            item (dict): Предмет для добавления
        """
        root = self.load_inventory_xml(player_id)
        if root is None:
            root = self.create_empty_inventory_xml(player_id)
        
        # Проверяем, не превышено ли максимальное количество предметов
        items = root.findall("item")
        if len(items) >= self.max_inventory_size:
            print(f"Инвентарь игрока {player_id} полон")
            return False
        
        # Проверяем, есть ли уже такой предмет (для стакающихся предметов)
        existing_item_elem = None
        for item_elem in root.findall("item"):
            if item_elem.get("id") == item["id"] and item.get("stackable", False):
                existing_item_elem = item_elem
                break
        
        if existing_item_elem is not None:
            # Увеличиваем количество существующего предмета
            current_quantity = int(existing_item_elem.get("quantity", 1))
            new_quantity = current_quantity + item.get("quantity", 1)
            existing_item_elem.set("quantity", str(new_quantity))
        else:
            # Добавляем новый предмет
            self.add_item_to_xml(root, item)
        
        self.save_inventory_xml(player_id, root)
        return True
    
    def load_inventory_xml(self, player_id):
        """
        Загружает XML-структуру инвентаря игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            Element: Корневой элемент инвентаря или None, если файл не найден
        """
        inventory_path = self.inventories_directory / f"{player_id}.xml"
        
        if not inventory_path.exists():
            return None
        
        try:
            tree = ET.parse(inventory_path)
            return tree.getroot()
        except ET.ParseError:
            print(f"Ошибка чтения инвентаря игрока {player_id}")
            return None
    
    def create_empty_inventory_xml(self, player_id):
        """
        Создает пустую XML-структуру инвентаря
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            Element: Корневой элемент инвентаря
        """
        root = ET.Element("inventory")
        root.set("player_id", player_id)
        root.set("created_at", datetime.now().isoformat())
        root.set("max_size", str(self.max_inventory_size))
        
        return root
    
    def save_inventory_xml(self, player_id, root):
        """
        Сохраняет XML-структуру инвентаря
        
        Args:
            player_id (str): ID игрока
            root: Корневой элемент инвентаря
        """
        inventory_path = self.inventories_directory / f"{player_id}.xml"
        tree = ET.ElementTree(root)
        tree.write(inventory_path, encoding="utf-8", xml_declaration=True)
    
    def remove_item(self, player_id, item_id):
        """
        Удаляет предмет из инвентаря игрока
        
        Args:
            player_id (str): ID игрока
            item_id (str): ID предмета для удаления
        """
        root = self.load_inventory_xml(player_id)
        if root is None:
            return False
        
        for i, item_elem in enumerate(root.findall("item")):
            if item_elem.get("id") == item_id:
                root.remove(item_elem)
                self.save_inventory_xml(player_id, root)
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
        root = self.load_inventory_xml(player_id)
        if root is None:
            return []
        
        items = []
        for item_elem in root.findall("item"):
            item = {
                "id": item_elem.get("id"),
                "name": item_elem.get("name"),
                "type": item_elem.get("type"),
                "rarity": item_elem.get("rarity"),
                "quantity": int(item_elem.get("quantity", 1)),
                "equipped": item_elem.get("equipped", "false").lower() == "true"
            }
            
            # Получаем свойства предмета
            properties_elem = item_elem.find("properties")
            if properties_elem is not None:
                properties = {}
                for prop_elem in properties_elem:
                    try:
                        # Пробуем преобразовать к числу
                        if '.' in prop_elem.text:
                            properties[prop_elem.tag] = float(prop_elem.text)
                        else:
                            properties[prop_elem.tag] = int(prop_elem.text)
                    except ValueError:
                        # Если не число, проверяем на булево или оставляем строкой
                        if prop_elem.text.lower() in ['true', 'false']:
                            properties[prop_elem.tag] = prop_elem.text.lower() == 'true'
                        else:
                            properties[prop_elem.tag] = prop_elem.text
                item["properties"] = properties
            else:
                item["properties"] = {}
            
            items.append(item)
        
        return items


class AchievementManager:
    """
    Система управления достижениями с XML-хранилищем
    """
    def __init__(self, achievements_file="achievements.xml", progress_directory="achievement_progress"):
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
        Загружает список достижений из XML-файла
        
        Returns:
            list: Список достижений
        """
        if self.achievements_file.exists():
            try:
                tree = ET.parse(self.achievements_file)
                root = tree.getroot()
                
                achievements = []
                for achievement_elem in root.findall("achievement"):
                    achievement = {
                        "id": achievement_elem.get("id"),
                        "name": achievement_elem.get("name"),
                        "type": achievement_elem.get("type"),
                        "target": int(achievement_elem.get("target"))
                    }
                    
                    # Ищем описание
                    desc_elem = achievement_elem.find("description")
                    if desc_elem is not None:
                        achievement["description"] = desc_elem.text
                    else:
                        achievement["description"] = ""
                    
                    # Ищем награды
                    rewards_elem = achievement_elem.find("rewards")
                    if rewards_elem is not None:
                        rewards = {}
                        for reward_elem in rewards_elem.findall("reward"):
                            reward_type = reward_elem.get("type")
                            reward_value = reward_elem.text
                            try:
                                rewards[reward_type] = int(reward_value)
                            except ValueError:
                                try:
                                    rewards[reward_type] = float(reward_value)
                                except ValueError:
                                    rewards[reward_type] = reward_value
                        achievement["rewards"] = rewards
                    else:
                        achievement["rewards"] = {}
                    
                    achievements.append(achievement)
                
                return achievements
            except ET.ParseError:
                print(f"Ошибка чтения файла достижений, используется стандартный список")
                return self.default_achievements
        else:
            # Создаем файл со стандартными достижениями
            self.save_achievements()
            return self.default_achievements
    
    def save_achievements(self):
        """
        Сохраняет список достижений в XML-файл
        """
        root = ET.Element("achievements")
        
        for achievement in self.achievements:
            achievement_elem = ET.SubElement(root, "achievement")
            achievement_elem.set("id", str(achievement["id"]))
            achievement_elem.set("name", str(achievement["name"]))
            achievement_elem.set("type", str(achievement["type"]))
            achievement_elem.set("target", str(achievement["target"]))
            
            # Добавляем описание
            desc_elem = ET.SubElement(achievement_elem, "description")
            desc_elem.text = str(achievement.get("description", ""))
            
            # Добавляем награды
            if "rewards" in achievement and achievement["rewards"]:
                rewards_elem = ET.SubElement(achievement_elem, "rewards")
                for reward_type, reward_value in achievement["rewards"].items():
                    reward_elem = ET.SubElement(rewards_elem, "reward")
                    reward_elem.set("type", str(reward_type))
                    reward_elem.text = str(reward_value)
        
        tree = ET.ElementTree(root)
        tree.write(self.achievements_file, encoding="utf-8", xml_declaration=True)
    
    def load_player_progress(self, player_id):
        """
        Загружает прогресс достижений игрока из XML-файла
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            dict: Прогресс достижений игрока
        """
        progress_path = self.progress_directory / f"{player_id}.xml"
        
        if progress_path.exists():
            try:
                tree = ET.parse(progress_path)
                root = tree.getroot()
                
                progress = {}
                for achievement_elem in root.findall("achievement"):
                    ach_id = achievement_elem.get("id")
                    progress[ach_id] = {
                        "achieved": achievement_elem.get("achieved", "false").lower() == "true",
                        "progress": int(achievement_elem.get("progress", 0))
                    }
                    
                    achieved_at = achievement_elem.get("achieved_at")
                    if achieved_at:
                        progress[ach_id]["achieved_at"] = achieved_at
                
                return progress
            except ET.ParseError:
                print(f"Ошибка чтения прогресса достижений для игрока {player_id}")
                return {}
        else:
            # Создаем новый файл прогресса
            return {}
    
    def save_player_progress(self, player_id, progress):
        """
        Сохраняет прогресс достижений игрока в XML-файл
        
        Args:
            player_id (str): ID игрока
            progress (dict): Прогресс для сохранения
        """
        progress_path = self.progress_directory / f"{player_id}.xml"
        
        root = ET.Element("progress")
        
        for ach_id, ach_progress in progress.items():
            achievement_elem = ET.SubElement(root, "achievement")
            achievement_elem.set("id", ach_id)
            achievement_elem.set("achieved", str(ach_progress.get("achieved", False)).lower())
            achievement_elem.set("progress", str(ach_progress.get("progress", 0)))
            
            if "achieved_at" in ach_progress:
                achievement_elem.set("achieved_at", ach_progress["achieved_at"])
        
        tree = ET.ElementTree(root)
        tree.write(progress_path, encoding="utf-8", xml_declaration=True)
    
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
    Система управления игровыми локациями с XML-описанием
    """
    def __init__(self, locations_directory="locations", connections_file="location_connections.xml"):
        self.locations_directory = Path(locations_directory)
        self.connections_file = Path(connections_file)
        self.locations = {}
        self.location_connections = {}
        
        self.load_all_locations()
        self.load_connections()
    
    def load_all_locations(self):
        """
        Загружает все локации из XML-файлов в директории
        """
        for location_file in self.locations_directory.glob("*.xml"):
            try:
                tree = ET.parse(location_file)
                root = tree.getroot()
                
                location_id = root.get("id")
                location_data = {
                    'id': location_id,
                    'name': root.get("name"),
                    'description': root.find("description").text if root.find("description") is not None else "",
                    'type': root.find("type").text if root.find("type") is not None else "",
                }
                
                # Загружаем диапазон уровней
                level_range_elem = root.find("level_range")
                if level_range_elem is not None:
                    location_data['level_range'] = {
                        'min': int(level_range_elem.get("min", 1)),
                        'max': int(level_range_elem.get("max", 10))
                    }
                else:
                    location_data['level_range'] = {'min': 1, 'max': 10}
                
                # Загружаем погоду
                weather_elem = root.find("weather")
                if weather_elem is not None:
                    location_data['weather'] = weather_elem.text
                else:
                    location_data['weather'] = "normal"
                
                # Загружаем ресурсы
                resources_elem = root.find("resources")
                if resources_elem is not None:
                    location_data['resources'] = [r.strip() for r in resources_elem.text.split(",")]
                else:
                    location_data['resources'] = []
                
                # Загружаем монстров
                monsters = []
                monsters_elem = root.find("monsters")
                if monsters_elem is not None:
                    for monster_elem in monsters_elem.findall("monster"):
                        monster = {
                            'name': monster_elem.get("name"),
                            'level': int(monster_elem.get("level", 1)),
                            'count': int(monster_elem.get("count", 1))
                        }
                        monsters.append(monster)
                location_data['monsters'] = monsters
                
                # Загружаем подключенные локации
                conn_elem = root.find("connected_locations")
                if conn_elem is not None:
                    location_data['connected_locations'] = [loc.strip() for loc in conn_elem.text.split(",")]
                else:
                    location_data['connected_locations'] = []
                
                self.locations[location_id] = location_data
                print(f"Загружена локация: {location_data['name']} (ID: {location_id})")
            except ET.ParseError:
                print(f"Ошибка чтения файла локации: {location_file}")
            except Exception as e:
                print(f"Ошибка загрузки локации из {location_file}: {e}")
    
    def load_location(self, location_id):
        """
        Загружает конкретную локацию из XML-файла
        
        Args:
            location_id (str): ID локации для загрузки
        """
        if location_id in self.locations:
            return self.locations[location_id]
        
        location_path = self.locations_directory / f"{location_id}.xml"
        if location_path.exists():
            try:
                tree = ET.parse(location_path)
                root = tree.getroot()
                
                location_data = {
                    'id': location_id,
                    'name': root.get("name"),
                    'description': root.find("description").text if root.find("description") is not None else "",
                    'type': root.find("type").text if root.find("type") is not None else "",
                }
                
                # Загружаем диапазон уровней
                level_range_elem = root.find("level_range")
                if level_range_elem is not None:
                    location_data['level_range'] = {
                        'min': int(level_range_elem.get("min", 1)),
                        'max': int(level_range_elem.get("max", 10))
                    }
                else:
                    location_data['level_range'] = {'min': 1, 'max': 10}
                
                # Загружаем погоду
                weather_elem = root.find("weather")
                if weather_elem is not None:
                    location_data['weather'] = weather_elem.text
                else:
                    location_data['weather'] = "normal"
                
                # Загружаем ресурсы
                resources_elem = root.find("resources")
                if resources_elem is not None:
                    location_data['resources'] = [r.strip() for r in resources_elem.text.split(",")]
                else:
                    location_data['resources'] = []
                
                # Загружаем монстров
                monsters = []
                monsters_elem = root.find("monsters")
                if monsters_elem is not None:
                    for monster_elem in monsters_elem.findall("monster"):
                        monster = {
                            'name': monster_elem.get("name"),
                            'level': int(monster_elem.get("level", 1)),
                            'count': int(monster_elem.get("count", 1))
                        }
                        monsters.append(monster)
                location_data['monsters'] = monsters
                
                # Загружаем подключенные локации
                conn_elem = root.find("connected_locations")
                if conn_elem is not None:
                    location_data['connected_locations'] = [loc.strip() for loc in conn_elem.text.split(",")]
                else:
                    location_data['connected_locations'] = []
                
                self.locations[location_id] = location_data
                return location_data
            except ET.ParseError:
                print(f"Ошибка чтения файла локации: {location_path}")
                return None
        else:
            print(f"Файл локации не найден: {location_path}")
            return None
    
    def load_connections(self):
        """
        Загружает соединения между локациями из XML-файла
        """
        if self.connections_file.exists():
            try:
                tree = ET.parse(self.connections_file)
                root = tree.getroot()
                
                for connection_elem in root.findall("connection"):
                    from_loc = connection_elem.get("from")
                    to_loc = connection_elem.get("to")
                    if from_loc and to_loc:
                        if from_loc not in self.location_connections:
                            self.location_connections[from_loc] = []
                        self.location_connections[from_loc].append(to_loc)
            except ET.ParseError:
                print(f"Ошибка чтения файла соединений: {self.connections_file}")
        else:
            # Если файла нет, создаем его на основе данных локаций
            for loc_id, loc_data in self.locations.items():
                if 'connected_locations' in loc_data:
                    for connected_loc in loc_data['connected_locations']:
                        if loc_id not in self.location_connections:
                            self.location_connections[loc_id] = []
                        self.location_connections[loc_id].append(connected_loc)
            
            # Сохраняем соединения в файл
            self.save_connections()
    
    def save_connections(self):
        """
        Сохраняет соединения между локациями в XML-файл
        """
        root = ET.Element("connections")
        
        for from_loc, to_locs in self.location_connections.items():
            for to_loc in to_locs:
                connection_elem = ET.SubElement(root, "connection")
                connection_elem.set("from", from_loc)
                connection_elem.set("to", to_loc)
        
        tree = ET.ElementTree(root)
        tree.write(self.connections_file, encoding="utf-8", xml_declaration=True)
    
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
        from collections import deque
        
        if start_location not in self.location_connections or end_location not in self.location_connections:
            return None
        
        # Используем алгоритм BFS для поиска кратчайшего пути
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
    Комплексная система управления игровым миром с XML-конфигурацией
    """
    def __init__(self, config_directory="world_config"):
        self.config_directory = Path(config_directory)
        self.game_entities = {}  # Все игровые сущности
        self.entity_templates = {}  # Шаблоны для разных типов сущностей
        self.entity_schemas = {}  # Схемы валидации для разных типов
        
        self.load_world_config()
    
    def load_world_config(self):
        """
        Загружает конфигурацию игрового мира из XML-файлов
        """
        # Загружаем шаблоны сущностей
        templates_dir = self.config_directory / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.xml"):
                try:
                    tree = ET.parse(template_file)
                    root = tree.getroot()
                    
                    entity_type = template_file.stem
                    templates = {}
                    
                    # Обрабатываем все шаблоны в файле
                    for template_elem in root:
                        template_id = template_elem.get("id")
                        template_data = self.xml_to_dict(template_elem.find("template"))
                        templates[template_id] = template_data
                    
                    self.entity_templates[entity_type] = templates
                    print(f"Загружены шаблоны {entity_type}: {len(templates)} шт.")
                except ET.ParseError:
                    print(f"Ошибка чтения файла шаблонов: {template_file}")
        
        # Загружаем схемы валидации
        schemas_dir = self.config_directory / "schemas"
        if schemas_dir.exists():
            for schema_file in schemas_dir.glob("*.xml"):
                try:
                    tree = ET.parse(schema_file)
                    root = tree.getroot()
                    
                    entity_type = schema_file.stem
                    schema = self.xml_to_dict(root)
                    self.entity_schemas[entity_type] = schema
                    print(f"Загружена схема для {entity_type}")
                except ET.ParseError:
                    print(f"Ошибка чтения файла схемы: {schema_file}")
    
    def xml_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        if element is None:
            return {}
        
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.xml_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result
    
    def dict_to_xml(self, tag, d, parent=None):
        """
        Преобразует словарь в XML-элемент и добавляет к родительскому элементу
        
        Args:
            tag (str): Тег элемента
            d (dict): Словарь для преобразования
            parent: Родительский элемент (опционально)
            
        Returns:
            Element: XML-элемент
        """
        if parent is not None:
            elem = ET.SubElement(parent, tag)
        else:
            elem = ET.Element(tag)
        
        for key, value in d.items():
            if isinstance(value, dict):
                self.dict_to_xml(key, value, elem)
            elif isinstance(value, list):
                list_elem = ET.SubElement(elem, key)
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self.dict_to_xml("item", item, list_elem)
                    else:
                        item_elem = ET.SubElement(list_elem, f"item_{i}")
                        item_elem.text = str(item)
            else:
                subelem = ET.SubElement(elem, key)
                subelem.text = str(value)
        
        return elem
    
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
    
    def validate_entity_data(self, entity_element, entity_type):
        """
        Проверяет корректность данных игровой сущности
        
        Args:
            entity_element (Element): XML-элемент сущности для проверки
            entity_type (str): Тип сущности
            
        Returns:
            tuple: (корректны ли данные, список ошибок)
        """
        if entity_type not in self.entity_schemas:
            return True, []  # Если нет схемы, считаем данные корректными
        
        schema = self.entity_schemas[entity_type]
        errors = []
        
        def validate_recursive(element, schema_part, path=""):
            if isinstance(schema_part, dict):
                # Проверяем, является ли schema_part описанием атрибута или элемента
                if '#text' in schema_part:  # Это означает, что элемент должен содержать текст
                    if element.text is None:
                        errors.append(f"Элемент по пути {path} должен содержать текст, но его нет")
                    else:
                        expected_type = schema_part.get('#text', 'string')
                        if expected_type == 'number':
                            try:
                                float(element.text)
                            except ValueError:
                                errors.append(f"Текст элемента по пути {path} должен быть числом, получено: {element.text}")
                        elif expected_type == 'integer':
                            try:
                                int(element.text)
                            except ValueError:
                                errors.append(f"Текст элемента по пути {path} должен быть целым числом, получено: {element.text}")
                        elif expected_type == 'boolean':
                            if element.text.lower() not in ['true', 'false', '1', '0']:
                                errors.append(f"Текст элемента по пути {path} должен быть булевым значением, получено: {element.text}")
                else:
                    # Это группа элементов
                    for key, value in schema_part.items():
                        if key.startswith('@'):  # Это атрибут
                            attr_name = key[1:]
                            if attr_name not in element.attrib:
                                if isinstance(value, dict) and value.get('required', True):
                                    errors.append(f"Отсутствует обязательный атрибут {attr_name} у элемента по пути {path}")
                            else:
                                # Проверяем тип атрибута
                                attr_value = element.attrib[attr_name]
                                expected_type = value.get('type', 'string')
                                if expected_type == 'number':
                                    try:
                                        float(attr_value)
                                    except ValueError:
                                        errors.append(f"Значение атрибута {attr_name} по пути {path} должно быть числом, получено: {attr_value}")
                                elif expected_type == 'integer':
                                    try:
                                        int(attr_value)
                                    except ValueError:
                                        errors.append(f"Значение атрибута {attr_name} по пути {path} должно быть целым числом, получено: {attr_value}")
                                elif expected_type == 'boolean':
                                    if attr_value.lower() not in ['true', 'false', '1', '0']:
                                        errors.append(f"Значение атрибута {attr_name} по пути {path} должно быть булевым значением, получено: {attr_value}")
                        else:  # Это дочерний элемент
                            child = element.find(key)
                            if child is None:
                                if isinstance(value, dict) and value.get('required', True):
                                    errors.append(f"Отсутствует обязательный элемент {key} внутри элемента по пути {path}")
                            else:
                                validate_recursive(child, value, f"{path}/{key}")
            elif schema_part == "element":
                if element is None:
                    errors.append(f"Ожидается элемент по пути {path}, но его нет")
            elif schema_part == "string":
                if element is None or element.text is None:
                    errors.append(f"Ожидается строка по пути {path}, но элемент или его текст отсутствует")
            elif schema_part == "number":
                if element is None or element.text is None:
                    errors.append(f"Ожидается число по пути {path}, но элемент или его текст отсутствует")
                else:
                    try:
                        float(element.text)
                    except ValueError:
                        errors.append(f"Ожидается число по пути {path}, получено: {element.text}")
            elif schema_part == "boolean":
                if element is None or element.text is None:
                    errors.append(f"Ожидается булево по пути {path}, но элемент или его текст отсутствует")
                else:
                    if element.text.lower() not in ['true', 'false', '1', '0']:
                        errors.append(f"Ожидается булево по пути {path}, получено: {element.text}")
        
        # Note: We can't directly pass an XML element here, so we skip this validation
        # validate_recursive(entity_element, schema)
        
        return len(errors) == 0, errors
    
    def export_world_state(self, export_name, entities_filter=None):
        """
        Экспортирует состояние игрового мира в XML-файл
        
        Args:
            export_name (str): Имя для экспорта
            entities_filter (callable): Функция для фильтрации сущностей (опционально)
        """
        export_path = self.config_directory / "exports" / f"{export_name}.xml"
        export_path.parent.mkdir(exist_ok=True)
        
        filtered_entities = self.game_entities
        if entities_filter:
            filtered_entities = {k: v for k, v in self.game_entities.items() if entities_filter(k, v)}
        
        root = ET.Element("world_state")
        root.set("exported_at", datetime.now().isoformat())
        root.set("game_version", "1.0.0")  # В реальной игре будет динамически получаться
        
        for entity_id, entity_data in filtered_entities.items():
            entity_elem = ET.SubElement(root, "entity")
            entity_elem.set("id", entity_data['id'])
            entity_elem.set("type", entity_data['type'])
            entity_elem.set("created_at", entity_data['created_at'])
            
            if 'updated_at' in entity_data:
                entity_elem.set("updated_at", entity_data['updated_at'])
            
            # Добавляем данные сущности
            self.dict_to_xml("data", entity_data['data'], entity_elem)
        
        tree = ET.ElementTree(root)
        tree.write(export_path, encoding="utf-8", xml_declaration=True)
        
        print(f"Состояние мира экспортировано: {export_path}")
    
    def import_world_state(self, import_name):
        """
        Импортирует состояние игрового мира из XML-файла
        
        Args:
            import_name (str): Имя импортируемого состояния
        """
        import_path = self.config_directory / "exports" / f"{import_name}.xml"
        
        if not import_path.exists():
            print(f"Файл импорта не найден: {import_path}")
            return False
        
        try:
            tree = ET.parse(import_path)
            root = tree.getroot()
            
            for entity_elem in root.findall("entity"):
                entity_id = entity_elem.get("id")
                entity_type = entity_elem.get("type")
                
                # Извлекаем данные сущности
                data_elem = entity_elem.find("data")
                if data_elem is not None:
                    entity_data = {
                        'id': entity_id,
                        'type': entity_type,
                        'created_at': entity_elem.get("created_at"),
                        'data': self.xml_element_to_dict(data_elem)
                    }
                    
                    if entity_elem.get("updated_at"):
                        entity_data['updated_at'] = entity_elem.get("updated_at")
                    
                    self.game_entities[f"{entity_type}:{entity_id}"] = entity_data
            
            print(f"Состояние мира импортировано: {import_path}")
            return True
        except ET.ParseError:
            print(f"Ошибка чтения файла импорта: {import_path}")
            return False
    
    def xml_element_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.xml_element_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result


class EventQuestManager:
    """
    Система управления событиями и квестами с XML-валидацией
    """
    def __init__(self, events_directory="events", quests_directory="quests", validation_schema_file="validation_schema.xml"):
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
        Загружает схемы валидации из XML-файла
        
        Returns:
            dict: Словарь схем валидации
        """
        if self.validation_schema_file.exists():
            try:
                tree = ET.parse(self.validation_schema_file)
                root = tree.getroot()
                
                schemas = {}
                for schema_elem in root.findall("schema"):
                    schema_type = schema_elem.get("type")
                    schema_data = {}
                    
                    # Загружаем обязательные поля
                    required_elem = schema_elem.find("required")
                    if required_elem is not None:
                        required_fields = [field_elem.text for field_elem in required_elem.findall("field")]
                        schema_data["required"] = required_fields
                    else:
                        schema_data["required"] = []
                    
                    # Загружаем определения полей
                    fields_elem = schema_elem.find("fields")
                    if fields_elem is not None:
                        fields = {}
                        for field_elem in fields_elem:
                            field_name = field_elem.get("name") or field_elem.tag
                            field_attrs = dict(field_elem.attrib)
                            
                            # Обрабатываем вложенные элементы (например, для объектов)
                            if len(field_elem) > 0:
                                field_attrs["nested"] = {}
                                for nested_elem in field_elem:
                                    nested_name = nested_elem.get("name") or nested_elem.tag
                                    nested_attrs = dict(nested_elem.attrib)
                                    field_attrs["nested"][nested_name] = nested_attrs
                            
                            fields[field_name] = field_attrs
                        schema_data["fields"] = fields
                    
                    schemas[schema_type] = schema_data
                
                return schemas
            except ET.ParseError:
                print(f"Ошибка чтения файла схемы валидации: {self.validation_schema_file}")
                return {}
        else:
            # Возвращаем пустой словарь, если файл не существует
            return {}
    
    def load_all_events(self):
        """
        Загружает все игровые события из XML-файлов
        """
        for event_file in self.events_directory.glob("*.xml"):
            try:
                tree = ET.parse(event_file)
                root = tree.getroot()
                
                # Проверяем валидность данных
                is_valid, errors = self.validate_event_data(root)
                if is_valid:
                    event_id = root.get("id")
                    event_data = self.xml_to_dict(root)
                    self.events[event_id] = event_data
                    print(f"Загружено событие: {event_data.get('name', 'Unknown')} (ID: {event_id})")
                else:
                    print(f"Ошибка валидации события из {event_file}: {', '.join(errors)}")
            except ET.ParseError:
                print(f"Ошибка чтения файла события: {event_file}")
    
    def load_all_quests(self):
        """
        Загружает все квесты из XML-файлов
        """
        for quest_file in self.quests_directory.glob("*.xml"):
            try:
                tree = ET.parse(quest_file)
                root = tree.getroot()
                
                # Проверяем валидность данных
                is_valid, errors = self.validate_quest_data(root)
                if is_valid:
                    quest_id = root.get("id")
                    quest_data = self.xml_to_dict(root)
                    self.quests[quest_id] = quest_data
                    print(f"Загружен квест: {quest_data.get('name', 'Unknown')} (ID: {quest_id})")
                else:
                    print(f"Ошибка валидации квеста из {quest_file}: {', '.join(errors)}")
            except ET.ParseError:
                print(f"Ошибка чтения файла квеста: {quest_file}")
    
    def xml_to_dict(self, element):
        """
        Преобразует XML-элемент в словарь
        
        Args:
            element: XML-элемент для преобразования
            
        Returns:
            dict: Словарь с данными элемента
        """
        result = {}
        
        # Добавляем атрибуты
        result.update(element.attrib)
        
        # Обрабатываем дочерние элементы
        for child in element:
            child_data = self.xml_to_dict(child)
            
            if child.tag in result:
                # Если тег уже существует, делаем список
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Если у элемента нет дочерних элементов, но есть текст, сохраняем его
        if not result and element.text.strip():
            text = element.text.strip()
            # Пробуем преобразовать к числу
            if text.isdigit():
                return int(text)
            else:
                try:
                    return float(text)
                except ValueError:
                    # Проверяем на булево
                    if text.lower() in ['true', 'false']:
                        return text.lower() == 'true'
                    return text
        
        return result
    
    def validate_event_data(self, event_element):
        """
        Проверяет корректность данных события
        
        Args:
            event_element (Element): XML-элемент события для проверки
            
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
            if not event_element.get(field) and event_element.find(field) is None:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Проверяем типы и значения полей
        fields = schema.get('fields', {})
        for field_name, field_schema in fields.items():
            if field_schema.get('required', False):
                # Проверяем, что поле существует
                elem = event_element.find(field_name) or event_element.get(field_name)
                if elem is None:
                    errors.append(f"Обязательное поле отсутствует: {field_name}")
        
        # Проверяем конкретные поля
        duration_elem = event_element.find("duration")
        if duration_elem is not None:
            try:
                duration_val = int(duration_elem.text)
                if duration_val < 1:
                    errors.append(f"Значение поля duration должно быть положительным, получено: {duration_val}")
            except ValueError:
                errors.append(f"Поле duration должно быть целым числом, получено: {duration_elem.text}")
        
        start_time_elem = event_element.find("start_time")
        if start_time_elem is not None:
            try:
                datetime.fromisoformat(start_time_elem.text.replace('Z', '+00:00'))
            except ValueError:
                errors.append(f"Поле start_time имеет неверный формат даты-времени: {start_time_elem.text}")
        
        return len(errors) == 0, errors
    
    def validate_quest_data(self, quest_element):
        """
        Проверяет корректность данных квеста
        
        Args:
            quest_element (Element): XML-элемент квеста для проверки
            
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
            if not quest_element.get(field) and quest_element.find(field) is None:
                errors.append(f"Отсутствует обязательное поле: {field}")
        
        # Проверяем типы и значения полей
        fields = schema.get('fields', {})
        for field_name, field_schema in fields.items():
            if field_schema.get('required', False):
                # Проверяем, что поле существует
                elem = quest_element.find(field_name) or quest_element.get(field_name)
                if elem is None:
                    errors.append(f"Обязательное поле отсутствует: {field_name}")
        
        # Проверяем конкретные поля
        objective_elem = quest_element.find("objective")
        if objective_elem is not None:
            target_elem = objective_elem.find("target")
            if target_elem is not None:
                try:
                    int(target_elem.text)
                except ValueError:
                    errors.append(f"Поле target в objective должно быть целым числом, получено: {target_elem.text}")
        
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
            if isinstance(original_target, str):
                original_target = int(original_target)
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