# Решения для практического задания 1: Создание структуры проекта игры "Сказочный Квест"

# Ниже приведены полные реализации игровых классов согласно заданию


class SimpleHero:
    """
    Простой класс для представления героя игрока.
    """
    def __init__(self, name):
        """
        Конструктор класса SimpleHero
        Создает нового героя с заданным именем
        """
        # Атрибуты экземпляра
        self.name = name
        self.health = 100

    def introduce(self):
        """
        Метод, который позволяет герою представиться
        """
        return f"Привет, я {self.name}!"

    def __str__(self):
        """Строковое представление объекта"""
        return f"SimpleHero(name='{self.name}', health={self.health})"


class SimpleItem:
    """
    Простой класс для игрового предмета.
    """
    def __init__(self, name, description=""):
        """
        Конструктор игрового предмета
        """
        self.name = name
        self.description = description

    def get_info(self):
        """
        Получить информацию о предмете
        """
        return f"{self.name}: {self.description}"

    def __str__(self):
        """Строковое представление объекта"""
        return f"SimpleItem(name='{self.name}', description='{self.description}')"


class Item:
    """
    Базовый класс для игрового предмета.
    """
    def __init__(self, name, item_type, value=0):
        self.name = name
        self.item_type = item_type
        self.value = value

    def use(self, target):
        """
        Использование предмета на цели.
        """
        return f"Вы использовали {self.name}."

    def __str__(self):
        """Строковое представление объекта"""
        return f"Item(name='{self.name}', type='{self.item_type}', value={self.value})"


class Inventory:
    """
    Класс инвентаря игрока.
    """
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def add_item(self, item):
        """
        Добавляет предмет в инвентарь.
        """
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_name):
        """
        Удаляет предмет из инвентаря по имени.
        """
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def get_items_by_type(self, item_type):
        """
        Возвращает список предметов указанного типа.
        """
        return [item for item in self.items if item.item_type == item_type]
        
    def get_total_value(self):
        """
        Возвращает общую стоимость всех предметов в инвентаре.
        """
        return sum(item.value for item in self.items)

    def has_space(self):
        """
        Проверка наличия свободного места
        """
        return len(self.items) < self.max_size

    def find_item(self, name):
        """
        Поиск предмета по имени
        """
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_items_count(self):
        """
        Получение количества предметов
        """
        return len(self.items)

    def get_available_space(self):
        """
        Получение доступного места
        """
        return self.max_size - len(self.items)

    def __str__(self):
        """Строковое представление объекта"""
        return f"Inventory(items_count={len(self.items)}, max_size={self.max_size})"


class Hero:
    """
    Класс для представления героя игрока.
    """
    def __init__(self, name):
        from src.config import MAX_HEALTH, DEFAULT_ATTACK, STARTING_GOLD
        self.name = name
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.attack = DEFAULT_ATTACK
        self.gold = STARTING_GOLD
        self.level = 1
        self.xp = 0
        self.xp_to_level = 100
        self.inventory = Inventory()
        
    def get_stats(self):
        """
        Возвращает строку с характеристиками героя.
        """
        return f"""
Имя: {self.name}
Уровень: {self.level}
Здоровье: {self.health}/{self.max_health}
Атака: {self.attack}
Золото: {self.gold}
Опыт: {self.xp}/{self.xp_to_level}
        """.strip()

    def is_alive(self):
        """
        Проверяет, жив ли герой.
        """
        return self.health > 0
        
    def take_damage(self, damage):
        """
        Герой получает урон.
        """
        self.health = max(0, self.health - damage)
        return damage

    def heal(self, amount):
        """
        Герой восстанавливает здоровье.
        """
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health

    def __str__(self):
        """Строковое представление объекта"""
        return f"Hero(name='{self.name}', level={self.level}, health={self.health}/{self.max_health})"


class NPC:
    """
    Класс для представления неигрового персонажа.
    """
    def __init__(self, name, role="unknown"):
        self.name = name
        self.role = role
        self.dialogues = []
        
    def add_dialogue(self, dialogue):
        """
        Добавляет диалог к NPC.
        """
        self.dialogues.append(dialogue)
        
    def speak(self):
        """
        NPC говорит первый доступный диалог.
        """
        if self.dialogues:
            return self.dialogues[0]
        return f"{self.name} молчит."

    def __str__(self):
        """Строковое представление объекта"""
        return f"NPC(name='{self.name}', role='{self.role}')"


class Location:
    """
    Класс для представления игровой локации.
    """
    def __init__(self, name, description, dangerous=False):
        self.name = name
        self.description = description
        self.dangerous = dangerous
        self.npcs = []
        self.items = []
        self.connections = []  # Список связанных локаций

    def add_npc(self, npc):
        """
        Добавляет NPC в локацию.
        """
        self.npcs.append(npc)

    def add_connection(self, location):
        """
        Добавляет связь с другой локацией.
        """
        if location not in self.connections:
            self.connections.append(location)

    def describe(self):
        """
        Описывает локацию.
        """
        danger_text = " (ОПАСНО)" if self.dangerous else ""
        return f"{self.name}{danger_text}\n{self.description}"

    def __str__(self):
        """Строковое представление объекта"""
        return f"Location(name='{self.name}', dangerous={self.dangerous})"


class WorldMap:
    """
    Класс для представления всей игровой карты.
    """
    def __init__(self):
        self.locations = {}
        self.start_location = None

    def add_location(self, location):
        """
        Добавляет локацию на карту.
        """
        self.locations[location.name] = location
        if self.start_location is None:
            self.start_location = location

    def get_location(self, name):
        """
        Возвращает локацию по имени.
        """
        return self.locations.get(name)

    def __str__(self):
        """Строковое представление объекта"""
        return f"WorldMap(locations_count={len(self.locations)})"


class Quest:
    """
    Класс для представления квеста.
    """
    def __init__(self, title, description, reward_xp=10, reward_gold=5):
        self.title = title
        self.description = description
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.completed = False

    def complete(self):
        """
        Помечает квест как выполненный.
        """
        self.completed = True
        return {"xp": self.reward_xp, "gold": self.reward_gold}

    def __str__(self):
        """Строковое представление объекта"""
        return f"Quest(title='{self.title}', completed={self.completed})"


class QuestLog:
    """
    Класс для ведения журнала квестов игрока.
    """
    def __init__(self):
        self.quests = []
        self.completed_quests = []

    def add_quest(self, quest):
        """
        Добавление квеста в журнал
        """
        if quest not in self.quests and not quest.completed:
            self.quests.append(quest)

    def complete_quest(self, title):
        """
        Завершение квеста по названию
        """
        for i, quest in enumerate(self.quests):
            if quest.title.lower() == title.lower():
                completed_quest = self.quests.pop(i)
                reward = completed_quest.complete()
                self.completed_quests.append(completed_quest)
                return reward
        return None

    def get_active_quests(self):
        """
        Получение списка активных квестов
        """
        return [quest for quest in self.quests if not quest.completed]

    def __str__(self):
        """Строковое представление объекта"""
        return f"QuestLog(active_quests={len(self.quests)}, completed_quests={len(self.completed_quests)})"


class SaveSystem:
    """
    Система сохранения и загрузки игры.
    """
    def __init__(self, save_dir="saves"):
        import os
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, game_state, filename):
        """
        Сохраняет состояние игры в файл.
        
        Args:
            game_state (dict): Состояние игры для сохранения
            filename (str): Имя файла для сохранения
        """
        import json
        import os
        from datetime import datetime
        
        filepath = os.path.join(self.save_dir, filename)
        game_state['saved_at'] = datetime.now().isoformat()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, ensure_ascii=False, indent=2)
        return filepath

    def load_game(self, filename):
        """
        Загружает состояние игры из файла.
        
        Args:
            filename (str): Имя файла для загрузки
            
        Returns:
            dict: Состояние игры или None, если файл не найден
        """
        import json
        import os
        
        filepath = os.path.join(self.save_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_save_list(self):
        """
        Возвращает список доступных сохранений.
        
        Returns:
            list: Список имен файлов сохранений
        """
        import os
        
        saves = []
        for file in os.listdir(self.save_dir):
            if file.endswith('.json'):
                saves.append(file)
        return saves

    def __str__(self):
        """Строковое представление объекта"""
        return f"SaveSystem(dir='{self.save_dir}')"


# Примеры использования классов
if __name__ == "__main__":
    print("=== Примеры использования игровых классов ===\n")
    
    # Пример использования класса SimpleHero
    print("--- Класс SimpleHero ---")
    hero = SimpleHero("Алекс")
    print(hero.introduce())
    print(str(hero))
    print()
    
    # Пример использования класса SimpleItem
    print("--- Класс SimpleItem ---")
    sword = SimpleItem("Меч", "Острый меч новобранца")
    print(sword.get_info())
    print(str(sword))
    print()
    
    # Пример использования класса Item
    print("--- Класс Item ---")
    health_potion = Item("Зелье здоровья", "potion", 25)
    print(health_potion.use(hero))
    print(str(health_potion))
    print()
    
    # Пример использования класса Inventory
    print("--- Класс Inventory ---")
    inventory = Inventory(max_size=5)
    inventory.add_item(health_potion)
    inventory.add_item(sword)
    print(f"Количество предметов в инвентаре: {inventory.get_items_count()}")
    print(f"Общая стоимость: {inventory.get_total_value()}")
    print(str(inventory))
    print()
    
    # Пример использования класса Hero
    print("--- Класс Hero ---")
    player = Hero("Иван")
    print(player.get_stats())
    print(f"Жив ли герой: {player.is_alive()}")
    print(str(player))
    print()
    
    # Пример использования класса NPC
    print("--- Класс NPC ---")
    merchant = NPC("Торговец", "merchant")
    merchant.add_dialogue("Добро пожаловать в мой магазин!")
    print(merchant.speak())
    print(str(merchant))
    print()
    
    # Пример использования класса Location
    print("--- Класс Location ---")
    village = Location("Деревня", "Маленькая деревня с уютными домиками.")
    print(village.describe())
    village.add_npc(merchant)
    print(f"NPC в локации: {len(village.npcs)}")
    print(str(village))
    print()
    
    # Пример использования класса WorldMap
    print("--- Класс WorldMap ---")
    world = WorldMap()
    world.add_location(village)
    forest = Location("Лес", "Густой лес, полный опасностей и сокровищ.", dangerous=True)
    world.add_location(forest)
    village.add_connection(forest)
    forest.add_connection(village)
    print(f"Количество локаций на карте: {len(world.locations)}")
    print(str(world))
    print()
    
    # Пример использования системы квестов
    print("--- Система квестов ---")
    quest_log = QuestLog()
    tutorial_quest = Quest("Обучение", "Поговорите с главой деревни", 20, 10)
    quest_log.add_quest(tutorial_quest)
    print(f"Активные квесты: {len(quest_log.get_active_quests())}")
    reward = quest_log.complete_quest("Обучение")
    if reward:
        print(f"Квест выполнен! Награда: {reward['xp']} XP, {reward['gold']} золота")
    print(str(quest_log))
    print()
    
    # Пример использования системы сохранения
    print("--- Система сохранения ---")
    save_system = SaveSystem()
    game_state = {
        "hero": {
            "name": player.name,
            "level": player.level,
            "health": player.health,
            "gold": player.gold
        },
        "location": world.start_location.name,
        "completed_quests": len(quest_log.completed_quests)
    }
    
    save_filename = f"{player.name}_save.json"
    save_path = save_system.save_game(game_state, save_filename)
    print(f"Игра сохранена в: {save_path}")
    
    loaded_game = save_system.load_game(save_filename)
    if loaded_game:
        print(f"Игра загружена: {loaded_game['hero']['name']}")
    
    print(str(save_system))
    print()
    
    print("Все игровые классы успешно реализованы и готовы к использованию!")