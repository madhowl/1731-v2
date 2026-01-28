# Решения для практического задания 9: ООП - реализация классов

# Ниже приведены игровые классы, которые реализованы согласно заданию

class GameCharacter:
    """
    Класс для представления игрового персонажа
    """
    # Атрибуты класса - общие для всех персонажей
    character_classes = ["warrior", "mage", "archer", "rogue"]
    
    def __init__(self, name, health, attack_power, character_class="warrior"):
        """
        Конструктор класса GameCharacter
        Создает новый объект персонажа с заданными характеристиками
        """
        # Атрибуты экземпляра - уникальны для каждого персонажа
        self.name = name  # Имя персонажа
        self.health = health  # Текущее здоровье
        self.max_health = health  # Максимальное здоровье
        self.attack_power = attack_power  # Сила атаки
        self.character_class = character_class if character_class in GameCharacter.character_classes else "warrior"
        self.level = 1  # Уровень персонажа (по умолчанию 1)
        self.experience = 0  # Опыт (по умолчанию 0)
        self.exp_for_next_level = 100  # Опыт, необходимый для следующего уровня
        self.inventory = []  # Список вещей в инвентаре (пустой)
        print(f"Создан новый персонаж: {self.name}")

    def introduce(self):
        """
        Метод, который позволяет персонажу представиться
        """
        return f"Привет, я {self.name}, {self.character_class} {self.level} уровня"

    def is_alive(self):
        """
        Метод проверяет, жив ли персонаж (здоровье больше 0)
        """
        return self.health > 0

    def take_damage(self, damage):
        """
        Метод, который позволяет персонажу получить урон
        """
        # Здоровье не может быть меньше 0
        self.health = max(0, self.health - damage)
        print(f"{self.name} получил {damage} урона. Осталось здоровья: {self.health}")
        return damage

    def heal(self, amount):
        """
        Метод, который позволяет персонажу восстановить здоровье
        """
        old_health = self.health
        # Здоровье не может превышать максимальное значение
        self.health = min(self.max_health, self.health + amount)
        healed_amount = self.health - old_health
        print(f"{self.name} восстановил {healed_amount} здоровья. Текущее здоровье: {self.health}")
        return healed_amount

    def attack(self, target):
        """Атакует другого персонажа"""
        if self.can_attack(target):
            damage_dealt = target.take_damage(self.attack_power)
            print(f"{self.name} атакует {target.name} и наносит {damage_dealt} урона")
            # Даём немного опыта за успешную атаку
            self.gain_experience(5)
            return damage_dealt
        else:
            print(f"{self.name} не может атаковать {target.name}")
            return 0

    def can_attack(self, target):
        """Проверяет, может ли персонаж атаковать цель"""
        return self.is_alive() and target.is_alive() and self != target

    def gain_experience(self, exp_amount):
        """Получает опыт и повышает уровень при необходимости"""
        self.experience += exp_amount
        print(f"{self.name} получил {exp_amount} опыта. Всего: {self.experience}/{self.exp_for_next_level}")
        
        # Проверяем, нужно ли повысить уровень
        while self.experience >= self.exp_for_next_level:
            self.level_up()

    def level_up(self):
        """Повышает уровень персонажа"""
        self.level += 1
        self.max_health += 20  # Увеличиваем максимальное здоровье
        self.health = self.max_health  # Полностью восстанавливаем здоровье
        self.attack_power += 5  # Увеличиваем силу атаки
        self.exp_for_next_level = int(self.exp_for_next_level * 1.5)  # Увеличиваем требуемый опыт
        print(f"{self.name} достиг {self.level} уровня!")

    def __str__(self):
        """Строковое представление объекта"""
        return f"GameCharacter(name='{self.name}', class='{self.character_class}', level={self.level}, health={self.health}/{self.max_health})"


class Monster:
    """
    Класс для представления игрового монстра
    """
    # Атрибут класса - общий для всех монстров
    total_killed = 0
    common_loot_table = ["gold_coin", "health_potion_minor"]
    
    def __init__(self, name, health, attack_power, monster_type="common"):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.monster_type = monster_type
        self.alive = True
        self.loot = []  # Атрибут экземпляра

    def get_info(self):
        return f'"{self.name}" - {self.monster_type} монстр (здоровье: {self.health}, атака: {self.attack_power})'

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.health = 0
            self.alive = False
            Monster.total_killed += 1  # Увеличиваем счетчик класса
            self.drop_loot()
        return damage

    def drop_loot(self):
        """Выбросить лут при смерти"""
        import random
        self.loot = Monster.common_loot_table.copy()
        if self.monster_type == "rare":
            self.loot.append("rare_item")
        elif self.monster_type == "boss":
            self.loot.extend(["legendary_item", "large_gold_pile"])
        print(f"{self.name} выбросил: {', '.join(self.loot)}")

    @classmethod
    def get_total_killed(cls):
        """Метод класса для получения общего количества убитых монстров"""
        return cls.total_killed

    @staticmethod
    def is_difficult_monster(monster_type):
        """Статический метод для проверки типа монстра"""
        return monster_type in ["rare", "boss"]

    def __str__(self):
        return f"Monster(name='{self.name}', type='{self.monster_type}', health={self.health}/{self.max_health})"


class GameItem:
    """
    Класс игрового предмета
    """
    item_types = ["weapon", "armor", "potion", "quest_item"]  # Атрибут класса
    
    def __init__(self, name, item_type, value=0, weight=1.0, durability=100):
        """
        Конструктор игрового предмета
        
        Args:
            name (str): Название предмета
            item_type (str): Тип предмета
            value (int): Стоимость предмета
            weight (float): Вес предмета
            durability (int): Прочность предмета
        """
        self.name = name  # Атрибут экземпляра
        self.item_type = item_type if item_type in GameItem.item_types else "misc"
        self.value = value
        self.weight = weight
        self.durability = durability
        self._effects = {}  # Защищенный атрибут (инкапсуляция)
        self.created_at = __import__('datetime').datetime.now()

    def add_effect(self, effect_name, effect_value):
        """
        Добавить эффект к предмету
        
        Args:
            effect_name (str): Название эффекта
            effect_value (any): Значение эффекта
        """
        self._effects[effect_name] = effect_value

    def get_effects(self):
        """
        Получить все эффекты предмета
        """
        return self._effects.copy()

    def use_on(self, character):
        if self.item_type == "potion" and "здоровье" in self.name.lower():
            # Простое восстановление здоровья на 20 единиц
            old_health = character.health
            character.health = min(character.max_health, character.health + 20)
            healed = character.health - old_health
            print(f"{character.name} восстановил {healed} здоровья с помощью {self.name}")
            return healed
        elif self.item_type == "weapon":
            if "damage" in self._effects:
                character.attack_power += self._effects["damage"]
                print(f"{character.name} получил бонус к атаке +{self._effects['damage']} от {self.name}")
        return 0

    def get_description(self):
        return f"{self.name} - {self.item_type}, стоимость: {self.value} золота"

    def __del__(self):
        """
        Деструктор класса
        """
        print(f"Предмет {self.name} удален из игры...")

    def __str__(self):
        return f"GameItem(name='{self.name}', type='{self.item_type}', value={self.value})"


class Shop:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.items = []  # Список товаров в магазине

    def add_item(self, item):
        self.items.append(item)
        print(f"Предмет {item.name} добавлен в {self.name}")

    def sell_item(self, item_name, buyer):
        # Поиск товара по имени
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                # Удаляем товар из магазина
                sold_item = self.items.pop(i)
                print(f"{buyer.name} купил {sold_item.name} за {sold_item.value} золота")
                return sold_item

        print(f"Предмет {item_name} не найден в {self.name}")
        return None

    def show_inventory(self):
        if not self.items:
            print(f"{self.name} пустой")
        else:
            print(f"Ассортимент {self.name}:")
            for item in self.items:
                print(f"- {item.get_description()}")

    def __str__(self):
        return f"Shop(name='{self.name}', owner='{self.owner}', items_count={len(self.items)})"


class Quest:
    def __init__(self, name, description, reward, target_count=1, target_type="default"):
        self.name = name
        self.description = description
        self.reward = reward
        self.target_count = target_count
        self.target_type = target_type
        self.current_progress = 0  # Текущий прогресс выполнения квеста
        self.completed = False  # Статус выполнения квеста
        self.accepted = False  # Принят ли квест игроком

    def update_progress(self, amount=1):
        """Обновляет прогресс выполнения квеста"""
        if not self.completed and self.accepted:
            self.current_progress = min(self.target_count, self.current_progress + amount)
            if self.current_progress >= self.target_count:
                self.completed = True
                print(f"Квест '{self.name}' выполнен!")

    def get_status(self):
        """Возвращает строку со статусом квеста"""
        if not self.accepted:
            return "Не принят"
        elif self.completed:
            return "Выполнен"
        else:
            return f"В процессе: {self.current_progress}/{self.target_count}"

    def __str__(self):
        return f"Quest(name='{self.name}', reward={self.reward}, status={self.get_status()})"


class QuestGiver:
    def __init__(self, name):
        self.name = name
        self.available_quests = []  # Список доступных квестов
        self.active_quests = {}  # Активные квесты у игроков: {player_id: [quests]}

    def add_quest(self, quest):
        """Добавляет квест в список доступных"""
        self.available_quests.append(quest)

    def give_quest(self, quest_name, player):
        """Выдает квест игроку"""
        for quest in self.available_quests:
            if quest.name.lower() == quest_name.lower() and not quest.accepted:
                quest.accepted = True
                if player.name not in self.active_quests:
                    self.active_quests[player.name] = []
                self.active_quests[player.name].append(quest)
                print(f"{player.name} принял квест: {quest.name}")
                return quest
        print(f"Квест '{quest_name}' недоступен для {player.name}")
        return None

    def complete_quest(self, quest_name, player):
        """Завершает квест для игрока"""
        if player.name in self.active_quests:
            for quest in self.active_quests[player.name]:
                if quest.name.lower() == quest_name.lower() and quest.completed:
                    # Выдаем награду игроку (в реальной игре это может быть добавление золота и т.п.)
                    print(f"{player.name} завершил квест '{quest.name}' и получил {quest.reward} золота!")
                    self.active_quests[player.name].remove(quest)
                    return True
        print(f"Невозможно завершить квест '{quest_name}' для {player.name}")
        return False

    def __str__(self):
        return f"QuestGiver(name='{self.name}', quests_count={len(self.available_quests)})"


class QuestSystem:
    def __init__(self):
        self.all_quests = []  # Все квесты в игре
        self.completed_quests = set()  # Уже выполненные квесты (чтобы не повторялись)

    def track_progress(self, quest, target_type, target_count=1):
        """Отслеживает прогресс выполнения квеста"""
        if quest.target_type == target_type:
            quest.update_progress(target_count)

    def finish_quest(self, quest, player):
        """Завершает квест для игрока"""
        if quest.completed:
            # В реальной игре здесь происходило бы начисление награды
            player.gain_experience(quest.reward)  # В качестве примера - опыт как награда
            print(f"Квест '{quest.name}' успешно завершен игроком {player.name}!")
            return True
        else:
            print(f"Квест '{quest.name}' еще не выполнен!")
            return False

    def __str__(self):
        return f"QuestSystem(quests_count={len(self.all_quests)}, completed_count={len(self.completed_quests)})"


class Weapon:
    """
    Класс для представления оружия
    """
    weapon_types = ["melee", "ranged", "magic"]
    rarity_levels = ["common", "uncommon", "rare", "epic", "legendary"]

    def __init__(self, name, weapon_type, base_damage, durability, rarity="common"):
        if weapon_type not in Weapon.weapon_types:
            raise ValueError(f"Тип оружия должен быть одним из: {Weapon.weapon_types}")
        if rarity not in Weapon.rarity_levels:
            raise ValueError(f"Редкость должна быть одной из: {Weapon.rarity_levels}")

        self.name = name
        self.weapon_type = weapon_type
        self.base_damage = base_damage
        self.durability = durability
        self.max_durability = durability
        self.rarity = rarity
        self.upgrade_level = 0

    def get_info(self):
        return f"{self.name} ({self.rarity} {self.weapon_type}): {self.get_damage()} урона, прочность {self.durability}/{self.max_durability}"

    def is_usable(self):
        return self.durability > 0

    def upgrade(self):
        self.upgrade_level += 1
        self.base_damage *= 1.2  # Увеличиваем урон на 20%
        self.durability = self.max_durability # Восстанавливаем прочность при улучшении
        print(f"{self.name} улучшен до уровня {self.upgrade_level}! Новый урон: {self.get_damage():.1f}")

    def get_damage(self):
        """Возвращает текущий урон с учетом уровня улучшения"""
        return self.base_damage * (1 + self.upgrade_level * 0.1)

    def __str__(self):
        return f"Weapon(name='{self.name}', type='{self.weapon_type}', damage={self.get_damage():.1f})"


class Inventory:
    """
    Класс для представления инвентаря игрока
    """
    def __init__(self, max_capacity=10, max_weight=100):
        self.items = []
        self.max_capacity = max_capacity
        self.max_weight = max_weight

    def add_item(self, item):
        if len(self.items) >= self.max_capacity:
            print("Инвентарь полон")
            return False
        if self.get_total_weight() + item.weight > self.max_weight:
            print("Превышен максимальный вес инвентаря")
            return False
        self.items.append(item)
        print(f"Предмет {item.name} добавлен в инвентарь")
        return True

    def remove_item(self, item_name):
        for i, item in enumerate(self.items):
            if item.name == item_name:
                removed_item = self.items.pop(i)
                print(f"Предмет {item_name} удален из инвентаря")
                return removed_item
        print(f"Предмет {item_name} не найден в инвентаре")
        return None

    def get_items_by_type(self, item_type):
        return [item for item in self.items if item.item_type == item_type]

    def get_total_weight(self):
        return sum(item.weight for item in self.items)

    def get_total_value(self):
        """Возвращает общую стоимость всех предметов в инвентаре"""
        return sum(item.value for item in self.items)

    def __str__(self):
        return f"Inventory(items_count={len(self.items)}, total_weight={self.get_total_weight()}, total_value={self.get_total_value()})"


class GameLocation:
    """
    Класс для представления игровой локации
    """
    location_types = ["town", "dungeon", "forest", "mountain", "castle", "cave"]

    def __init__(self, name, location_type, danger_level=1):
        if location_type not in GameLocation.location_types:
            raise ValueError(f"Тип локации должен быть одним из: {GameLocation.location_types}")
        if not 1 <= danger_level <= 10:
            raise ValueError("Уровень опасности должен быть от 1 до 10")

        self.name = name
        self.location_type = location_type
        self.danger_level = danger_level
        self.npcs = []
        self.monsters = []
        self.created_at = __import__('datetime').datetime.now()

    def enter_location(self, player):
        print(f"{player.name} входит в {self.name} (уровень опасности: {self.danger_level})")
        if self.danger_level > player.level:
            print("Внимание! Уровень опасности выше вашего уровня!")
        else:
            print("Уровень опасности приемлем для вас.")

    def spawn_monster(self, monster_name, monster_health, monster_attack, monster_type="common"):
        from random import randint
        monster = Monster(monster_name, monster_health, monster_attack, monster_type)
        self.monsters.append(monster)
        print(f"Появился {monster_name} в {self.name}!")
        return monster

    def get_safe(self):
        if self.danger_level > 1:
            self.danger_level -= 1
            print(f"Уровень опасности в {self.name} снижен до {self.danger_level}")
        else:
            print(f"{self.name} уже безопасен (минимальный уровень опасности)")

    def get_age(self):
        import datetime
        current_time = datetime.datetime.now()
        age = current_time - self.created_at
        return age.days

    def __str__(self):
        return f"GameLocation(name='{self.name}', type='{self.location_type}', danger_level={self.danger_level})"


# Примеры использования классов
if __name__ == "__main__":
    print("=== Примеры использования игровых классов ===\n")
    
    # Пример использования класса GameCharacter
    print("--- Класс GameCharacter ---")
    hero = GameCharacter("Артур", 100, 20, "warrior")
    print(hero.introduce())
    print(f"Жив: {hero.is_alive()}")
    print(str(hero))
    print()
    
    # Пример использования класса Monster
    print("--- Класс Monster ---")
    goblin = Monster("Гоблин", 30, 8, "common")
    print(goblin.get_info())
    print(f"Жив: {goblin.is_alive()}")
    print(str(goblin))
    print()
    
    # Пример использования класса GameItem
    print("--- Класс GameItem ---")
    health_potion = GameItem("Зелье здоровья", "potion", 25, 0.5, 1)
    health_potion.add_effect("heal", 30)
    print(f"Тип предмета: {health_potion.item_type}")
    print(f"Эффекты: {health_potion.get_effects()}")
    print(health_potion.get_description())
    print(str(health_potion))
    print()
    
    # Пример использования класса Shop
    print("--- Класс Shop ---")
    shop = Shop("Лавка Алхимика", "Альберт")
    shop.add_item(health_potion)
    shop.show_inventory()
    print(str(shop))
    print()
    
    # Пример использования класса Weapon
    print("--- Класс Weapon ---")
    sword = Weapon("Меч героя", "melee", 25, 100, "rare")
    print(sword.get_info())
    print(f"Пригодно к использованию: {sword.is_usable()}")
    print(str(sword))
    print()
    
    # Пример использования класса GameLocation
    print("--- Класс GameLocation ---")
    forest = GameLocation("Темный лес", "forest", 5)
    print(f"Возраст локации: {forest.get_age()} дней")
    forest.enter_location(hero)
    print(str(forest))
    print()
    
    # Пример использования системы квестов
    print("--- Система квестов ---")
    quest_system = QuestSystem()
    blacksmith = QuestGiver("Кузнец Гром")
    kill_quest = Quest("Истребитель гоблинов", "Убейте 3 гоблина", 50, 3, "kill_monster")
    blacksmith.add_quest(kill_quest)
    print(f"Квест: {kill_quest.name}, Награда: {kill_quest.reward} золота")
    print(f"Статус: {kill_quest.get_status()}")
    print(str(kill_quest))
    print(str(blacksmith))
    print(str(quest_system))
    print()
    
    # Пример использования инвентаря
    print("--- Класс Inventory ---")
    inventory = Inventory(max_capacity=5, max_weight=50)
    inventory.add_item(health_potion)
    print(f"Общий вес инвентаря: {inventory.get_total_weight()}")
    print(f"Общая стоимость: {inventory.get_total_value()}")
    print(str(inventory))
    print()
    
    print("Все игровые классы успешно реализованы и готовы к использованию!")