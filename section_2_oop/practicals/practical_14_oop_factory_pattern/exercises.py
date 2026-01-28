"""
Практическое задание 14: Паттерн Factory в игровом контексте

Цель: Реализовать паттерн Factory для создания игровых объектов без указания их конкретных классов.
"""

from abc import ABC, abstractmethod

# Уровень 1 - Начальный
# Задание 1.1: Создать простую фабрику для создания игровых персонажей

class GameCharacter(ABC):
    """
    Абстрактный класс игрового персонажа
    """
    def __init__(self, name, health, attack_power, character_class="unknown"):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.character_class = character_class
        self.level = 1
        self.is_alive = True

    @abstractmethod
    def special_ability(self):
        """
        Специальная способность персонажа
        """
        pass

    def get_info(self):
        """
        Получить информацию о персонаже
        """
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({self.character_class}, {status}): Lvl.{self.level}, HP {self.health}/{self.max_health}, ATK {self.attack_power}"

    def take_damage(self, damage):
        """Получить урон"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def restore_health(self, amount):
        """Восстановить здоровье"""
        self.health = min(self.max_health, self.health + amount)


class Warrior(GameCharacter):
    """
    Класс воина - реализуйте конструктор и специальную способность
    """
    # TODO: Реализуйте конструктор, вызывающий родительский конструктор
    # TODO: Реализуйте метод special_ability()
    pass


class Mage(GameCharacter):
    """
    Класс мага - реализуйте конструктор и специальную способность
    """
    # TODO: Реализуйте конструктор, вызывающий родительский конструктор
    # TODO: Реализуйте метод special_ability()
    pass


class Archer(GameCharacter):
    """
    Класс лучника - реализуйте конструктор и специальную способность
    """
    # TODO: Реализуйте конструктор, вызывающий родительский конструктор
    # TODO: Реализуйте метод special_ability()
    pass


class CharacterFactory:
    """
    Фабрика для создания игровых персонажей
    """
    @staticmethod
    def create_character(character_type, name):
        """
        Создать персонажа по типу
        """
        # TODO: Реализуйте фабричный метод для создания персонажей разных типов
        pass


# Уровень 2 - Средний
# Задание 2.1: Реализовать паттерн "Фабричный метод" для создания игровых предметов

class GameItem(ABC):
    """
    Абстрактный класс игрового предмета
    """
    def __init__(self, name, item_type, value, weight=1.0):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.weight = weight

    @abstractmethod
    def use(self, character):
        """
        Использовать предмет на персонаже
        """
        pass

    def get_info(self):
        return f"{self.name} ({self.item_type}): стоимость {self.value}, вес {self.weight}"


class Weapon(GameItem):
    """
    Класс оружия
    """
    # TODO: Реализуйте конструктор и метод use()
    pass


class Potion(GameItem):
    """
    Класс зелья
    """
    # TODO: Реализуйте конструктор и метод use()
    pass


class Armor(GameItem):
    """
    Класс брони
    """
    # TODO: Реализуйте конструктор и метод use()
    pass


class ItemCreator(ABC):
    """
    Абстрактный создатель предметов
    """
    @abstractmethod
    def create_item(self, name, **kwargs):
        pass

    def get_item(self, name, **kwargs):
        """Шаблонный метод для получения предмета"""
        item = self.create_item(name, **kwargs)
        return item


class WeaponCreator(ItemCreator):
    """
    Создатель оружия
    """
    # TODO: Реализуйте метод create_item()
    pass


class PotionCreator(ItemCreator):
    """
    Создатель зелий
    """
    # TODO: Реализуйте метод create_item()
    pass


class ArmorCreator(ItemCreator):
    """
    Создатель брони
    """
    # TODO: Реализуйте метод create_item()
    pass


# Уровень 3 - Повышенный
# Задание 3.1: Реализовать абстрактную фабрику для UI-элементов

class Button(ABC):
    """
    Абстрактный класс кнопки
    """
    def __init__(self, text, width=100, height=30):
        self.text = text
        self.width = width
        self.height = height

    @abstractmethod
    def render(self):
        pass

    def click(self):
        return f"Кнопка '{self.text}' нажата"


class TextField(ABC):
    """
    Абстрактный класс текстового поля
    """
    def __init__(self, placeholder="", width=200, height=30):
        self.placeholder = placeholder
        self.width = width
        self.height = height
        self.content = ""

    @abstractmethod
    def render(self):
        pass

    def input_text(self, text):
        self.content = text
        return f"Введено '{text}' в поле '{self.placeholder}'"


class UIFactory(ABC):
    """
    Абстрактная фабрика UI-элементов
    """
    @abstractmethod
    def create_button(self, text, width=100, height=30):
        pass

    @abstractmethod
    def create_text_field(self, placeholder="", width=200, height=30):
        pass


class FantasyUIFactory(UIFactory):
    """
    Фабрика UI-элементов в фэнтезийном стиле
    """
    # TODO: Реализуйте методы create_button() и create_text_field()
    pass


class SciFiUIFactory(UIFactory):
    """
    Фабрика UI-элементов в стиле sci-fi
    """
    # TODO: Реализуйте методы create_button() и create_text_field()
    pass


class MedievalUIFactory(UIFactory):
    """
    Фабрика UI-элементов в средневековом стиле
    """
    # TODO: Реализуйте методы create_button() и create_text_field()
    pass


# Задание 3.2: Параметризованная фабрика для создания монстров
class Monster(ABC):
    """
    Абстрактный класс монстра
    """
    def __init__(self, name, health, attack_power, monster_type="common"):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.monster_type = monster_type
        self.is_alive = True

    @abstractmethod
    def special_attack(self):
        pass

    def get_info(self):
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({self.monster_type}, {status}): HP {self.health}/{self.max_health}, ATK {self.attack_power}"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def attack(self, target):
        if self.is_alive and target.is_alive:
            target.take_damage(self.attack_power)
            return f"{self.name} атакует {target.name} на {self.attack_power} урона"
        else:
            return f"{self.name} не может атаковать"


class MonsterFactory:
    """
    Фабрика для создания монстров с параметрами
    """
    @staticmethod
    def create_monster(monster_type, name=None, health=None, attack_power=None, difficulty="normal"):
        """
        Создать монстра с указанными параметрами
        """
        # TODO: Реализуйте фабричный метод для создания монстров с параметрами
        pass


# Тестирование реализации (раскомментируйте после реализации)
"""
# Тестирование уровня 1
warrior = CharacterFactory.create_character("warrior", "Конан")
mage = CharacterFactory.create_character("mage", "Мерлин")
archer = CharacterFactory.create_character("archer", "Робин")

print(warrior.get_info())
print(mage.get_info())
print(archer.get_info())

print(warrior.special_ability())
print(mage.special_ability())

# Тестирование уровня 2
weapon_creator = WeaponCreator()
potion_creator = PotionCreator()
armor_creator = ArmorCreator()

sword = weapon_creator.get_item("Меч короля", damage=25, value=200)
health_potion = potion_creator.get_item("Зелье здоровья", healing_power=50, value=30)
shield = armor_creator.get_item("Щит", defense=15, value=180)

print(sword.get_info())
print(health_potion.get_info())
print(shield.get_info())

# Тестирование уровня 3
fantasy_factory = FantasyUIFactory()
scifi_factory = SciFiUIFactory()

fantasy_button = fantasy_factory.create_button("Начать приключение", 150, 40)
scifi_button = scifi_factory.create_button("Активировать щит", 120, 35)

print(fantasy_button.render())
print(scifi_button.render())
print(fantasy_button.click())

# Тестирование фабрики монстров
goblin = MonsterFactory.create_monster("goblin", "Малыш Гоб", difficulty="hard")
dragon = MonsterFactory.create_monster("dragon", difficulty="legendary")

print(goblin.get_info())
print(dragon.get_info())
"""