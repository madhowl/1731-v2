# factory_example.py

from abc import ABC, abstractmethod

class Character(ABC):
    """Абстрактный класс игрового персонажа"""
    def __init__(self, name, health=100, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.level = level
        self.experience = 0

    @abstractmethod
    def special_ability(self):
        """Абстрактный метод специальной способности"""
        pass

    def take_damage(self, damage):
        """Получить урон"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        """Проверить, жив ли персонаж"""
        return self.health > 0

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}: Уровень {self.level}, Здоровье {self.health}/{self.max_health}"


class Warrior(Character):
    """Класс воина"""
    def __init__(self, name):
        super().__init__(name, health=150, level=1)
        self.strength = 20
        self.armor = 10

    def special_ability(self):
        """Специальная способность воина - яростная атака"""
        damage = self.strength * 2
        print(f"{self.name} использует яростную атаку и наносит {damage} урона!")
        return damage


class Mage(Character):
    """Класс мага"""
    def __init__(self, name):
        super().__init__(name, health=80, level=1)
        self.intelligence = 25
        self.mana = 100
        self.max_mana = 100

    def special_ability(self):
        """Специальная способность мага - огненный шар"""
        if self.mana >= 20:
            self.mana -= 20
            damage = self.intelligence * 1.5
            print(f"{self.name} произносит заклинание огненного шара и наносит {damage} урона!")
            print(f"Осталось маны: {self.mana}/{self.max_mana}")
            return damage
        else:
            print(f"{self.name} недостаточно маны для заклинания!")
            return 0


class Archer(Character):
    """Класс лучника"""
    def __init__(self, name):
        super().__init__(name, health=100, level=1)
        self.dexterity = 22
        self.arrows = 30

    def special_ability(self):
        """Специальная способность лучника - меткий выстрел"""
        if self.arrows > 0:
            self.arrows -= 1
            damage = self.dexterity * 1.8
            print(f"{self.name} делает меткий выстрел и наносит {damage} урона! Осталось стрел: {self.arrows}")
            return damage
        else:
            print(f"У {self.name} закончились стрелы!")
            return 0


class Enemy(Character):
    """Класс врага"""
    def __init__(self, name, health=50, level=1, enemy_type="common"):
        super().__init__(name, health, level)
        self.enemy_type = enemy_type
        self.attack_power = 10 + (level * 2)

    def special_ability(self):
        """Способность врага"""
        damage = self.attack_power
        print(f"{self.name} атакует и наносит {damage} урона!")
        return damage


class CharacterFactory:
    """Простая фабрика для создания персонажей"""
    @staticmethod
    def create_character(char_type, name):
        """Создать персонажа по типу"""
        if char_type.lower() == "warrior":
            return Warrior(name)
        elif char_type.lower() == "mage":
            return Mage(name)
        elif char_type.lower() == "archer":
            return Archer(name)
        elif char_type.lower() == "enemy":
            return Enemy(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа: {char_type}")


# Пример использования простой фабрики
print("=== Простая фабрика для создания персонажей ===")

# Создание персонажей через фабрику
warrior = CharacterFactory.create_character("warrior", "Конан")
mage = CharacterFactory.create_character("mage", "Мерлин")
archer = CharacterFactory.create_character("archer", "Робин")
goblin = CharacterFactory.create_character("enemy", "Гоблин")

characters = [warrior, mage, archer, goblin]

for char in characters:
    print(char)
    char.special_ability()
    print()


class Item(ABC):
    """Абстрактный класс предмета"""
    def __init__(self, name, value=0, weight=1.0):
        self.name = name
        self.value = value
        self.weight = weight

    @abstractmethod
    def use(self, target):
        """Абстрактный метод использования предмета"""
        pass


class Weapon(Item):
    """Класс оружия"""
    def __init__(self, name, value, weight, damage, weapon_type="обычное"):
        super().__init__(name, value, weight)
        self.damage = damage
        self.weapon_type = weapon_type

    def use(self, target):
        """Использование оружия (не применимо в прямом смысле, но для совместимости)"""
        print(f"{self.name} - оружие уроном {self.damage} типа {self.weapon_type}")
        return self.damage


class Potion(Item):
    """Класс зелья"""
    def __init__(self, name, value, weight, effect_type, effect_value):
        super().__init__(name, value, weight)
        self.effect_type = effect_type
        self.effect_value = effect_value

    def use(self, target):
        """Использование зелья на цели"""
        if self.effect_type == "heal":
            old_health = target.health
            target.health = min(target.max_health, target.health + self.effect_value)
            healed = target.health - old_health
            print(f"{target.name} восстановил {healed} здоровья с помощью {self.name}")
            return healed
        elif self.effect_type == "mana":
            if hasattr(target, 'mana'):
                old_mana = target.mana
                target.mana = min(target.max_mana, target.mana + self.effect_value)
                restored = target.mana - old_mana
                print(f"{target.name} восстановил {restored} маны с помощью {self.name}")
                return restored
        return 0


class Armor(Item):
    """Класс брони"""
    def __init__(self, name, value, weight, protection, armor_type="обычная"):
        super().__init__(name, value, weight)
        self.protection = protection
        self.armor_type = armor_type

    def use(self, target):
        """Использование брони (экипировка)"""
        print(f"{target.name} экипировал {self.name}, получив {self.protection} защиты")
        return self.protection


class ItemFactory(ABC):
    """Абстрактная фабрика для создания предметов"""
    @abstractmethod
    def create_item(self, name, **kwargs):
        pass


class WeaponFactory(ItemFactory):
    """Фабрика для создания оружия"""
    def create_item(self, name, **kwargs):
        damage = kwargs.get('damage', 10)
        weapon_type = kwargs.get('weapon_type', 'обычное')
        value = kwargs.get('value', 50)
        weight = kwargs.get('weight', 3.0)
        return Weapon(name, value, weight, damage, weapon_type)


class PotionFactory(ItemFactory):
    """Фабрика для создания зелий"""
    def create_item(self, name, **kwargs):
        effect_type = kwargs.get('effect_type', 'heal')
        effect_value = kwargs.get('effect_value', 20)
        value = kwargs.get('value', 25)
        weight = kwargs.get('weight', 0.5)
        return Potion(name, value, weight, effect_type, effect_value)


class ArmorFactory(ItemFactory):
    """Фабрика для создания брони"""
    def create_item(self, name, **kwargs):
        protection = kwargs.get('protection', 5)
        armor_type = kwargs.get('armor_type', 'обычная')
        value = kwargs.get('value', 40)
        weight = kwargs.get('weight', 5.0)
        return Armor(name, value, weight, protection, armor_type)


class GameItemFactory:
    """Фабрика фабрик - позволяет создавать разные типы фабрик"""
    @staticmethod
    def get_factory(factory_type):
        if factory_type.lower() == "weapon":
            return WeaponFactory()
        elif factory_type.lower() == "potion":
            return PotionFactory()
        elif factory_type.lower() == "armor":
            return ArmorFactory()
        else:
            raise ValueError(f"Неизвестный тип фабрики: {factory_type}")


# Пример использования фабричного метода
print("\n=== Фабричный метод для создания предметов ===")

# Создание фабрик
weapon_factory = GameItemFactory.get_factory("weapon")
potion_factory = GameItemFactory.get_factory("potion")
armor_factory = GameItemFactory.get_factory("armor")

# Создание предметов через фабрики
sword = weapon_factory.create_item(
    "Экскалибур", 
    damage=35, 
    weapon_type="меч", 
    value=200, 
    weight=4.5
)

health_potion = potion_factory.create_item(
    "Зелье здоровья", 
    effect_type="heal", 
    effect_value=50, 
    value=30, 
    weight=0.3
)

dragon_armor = armor_factory.create_item(
    "Драконья броня", 
    protection=25, 
    armor_type="эпическая", 
    value=500, 
    weight=15.0
)

items = [sword, health_potion, dragon_armor]

for item in items:
    print(f"Предмет: {item.name}, Тип: {type(item).__name__}, Вес: {item.weight}, Стоимость: {item.value}")


class World(ABC):
    """Абстрактный класс игрового мира"""
    def __init__(self, name):
        self.name = name
        self.enemies = []
        self.items = []
        self.npcs = []

    @abstractmethod
    def create_enemy(self, name):
        pass

    @abstractmethod
    def create_item(self, name):
        pass

    @abstractmethod
    def create_npc(self, name):
        pass


class MedievalWorld(World):
    """Мир средневековья"""
    def create_enemy(self, name):
        enemies = {
            "goblin": lambda n: Enemy(n, health=40, level=1, enemy_type="goblin"),
            "orc": lambda n: Enemy(n, health=80, level=3, enemy_type="orc"),
            "dragon": lambda n: Enemy(n, health=300, level=10, enemy_type="dragon")
        }
        enemy_type = name.split()[0].lower() if " " in name else name.lower()
        return enemies.get(enemy_type, enemies["goblin"])(name)

    def create_item(self, name):
        items = {
            "sword": lambda n: Weapon(n, value=100, weight=3.0, damage=25, weapon_type="меч"),
            "potion": lambda n: Potion(n, value=20, weight=0.5, effect_type="heal", effect_value=30),
            "armor": lambda n: Armor(n, value=150, weight=10.0, protection=15, armor_type="броня")
        }
        item_type = name.split()[0].lower() if " " in name else name.lower()
        return items.get(item_type, items["potion"])(name)

    def create_npc(self, name):
        return CharacterFactory.create_character("warrior", name)  # Для примера


class SciFiWorld(World):
    """Мир научной фантастики"""
    def create_enemy(self, name):
        enemies = {
            "robot": lambda n: Enemy(n, health=60, level=2, enemy_type="робот"),
            "alien": lambda n: Enemy(n, health=120, level=5, enemy_type="пришелец"),
            "cyborg": lambda n: Enemy(n, health=200, level=8, enemy_type="киборг")
        }
        enemy_type = name.split()[0].lower() if " " in name else name.lower()
        return enemies.get(enemy_type, enemies["robot"])(name)

    def create_item(self, name):
        items = {
            "laser": lambda n: Weapon(n, value=150, weight=2.0, damage=40, weapon_type="лазер"),
            "nanokit": lambda n: Potion(n, value=50, weight=0.2, effect_type="heal", effect_value=70),
            "shield": lambda n: Armor(n, value=200, weight=5.0, protection=20, armor_type="энергетический")
        }
        item_type = name.split()[0].lower() if " " in name else name.lower()
        return items.get(item_type, items["nanokit"])(name)

    def create_npc(self, name):
        return CharacterFactory.create_character("mage", name) # Для примера


class WorldFactory(ABC):
    """Абстрактная фабрика для создания миров"""
    @abstractmethod
    def create_world(self, name):
        pass

    @abstractmethod
    def create_enemy(self, world, name):
        pass

    @abstractmethod
    def create_item(self, world, name):
        pass

    @abstractmethod
    def create_npc(self, world, name):
        pass


class MedievalWorldFactory(WorldFactory):
    """Фабрика для создания средневекового мира"""
    def create_world(self, name):
        return MedievalWorld(name)

    def create_enemy(self, world, name):
        return world.create_enemy(name)

    def create_item(self, world, name):
        return world.create_item(name)

    def create_npc(self, world, name):
        return world.create_npc(name)


class SciFiWorldFactory(WorldFactory):
    """Фабрика для создания научно-фантастического мира"""
    def create_world(self, name):
        return SciFiWorld(name)

    def create_enemy(self, world, name):
        return world.create_enemy(name)

    def create_item(self, world, name):
        return world.create_item(name)

    def create_npc(self, world, name):
        return world.create_npc(name)


def create_game_scenario(factory, world_name):
    """Функция для создания игровой сценарий с использованием фабрики"""
    world = factory.create_world(world_name)
    
    # Создание объектов для мира
    knight = factory.create_npc(world, "Рыцарь Артур")
    dragon = factory.create_enemy(world, "Огненный Дракон")
    sword = factory.create_item(world, "Меч Света")
    potion = factory.create_item(world, "Зелье Могущества")
    
    print(f"\n--- Создан мир: {world.name} ---")
    print(f"NPC: {knight}")
    print(f"Враг: {dragon}")
    print(f"Предметы: {sword.name}, {potion.name}")
    
    return world, knight, dragon, sword, potion


# Пример использования абстрактной фабрики
print("\n=== Абстрактная фабрика для игровых миров ===")

medieval_factory = MedievalWorldFactory()
scifi_factory = SciFiWorldFactory()

# Создание сценариев для разных миров
medieval_world_data = create_game_scenario(medieval_factory, "Королевство Вальдара")
scifi_world_data = create_game_scenario(scifi_factory, "Космическая станция Орион")