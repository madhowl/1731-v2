"""
Решение для практического задания 14: Паттерн Factory в игровом контексте
"""

from abc import ABC, abstractmethod
import random

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
    Класс воина
    """
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=20, character_class="warrior")
        self.armor = 10

    def special_ability(self):
        return f"{self.name} использует яростную атаку!"


class Mage(GameCharacter):
    """
    Класс мага
    """
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=25, character_class="mage")
        self.mana = 10
        self.max_mana = 100

    def special_ability(self):
        if self.mana >= 30:
            self.mana -= 30
            return f"{self.name} произносит мощное заклинание! Осталось маны: {self.mana}/{self.max_mana}"
        else:
            return f"{self.name} недостаточно маны для заклинания"


class Archer(GameCharacter):
    """
    Класс лучника
    """
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=18, character_class="archer")
        self.arrows = 30

    def special_ability(self):
        if self.arrows > 0:
            self.arrows -= 1
            return f"{self.name} делает меткий выстрел! Осталось стрел: {self.arrows}"
        else:
            return f"{self.name} закончились стрелы!"


class CharacterFactory:
    """
    Фабрика для создания игровых персонажей
    """
    @staticmethod
    def create_character(character_type, name):
        """
        Создать персонажа по типу
        """
        if character_type.lower() == "warrior":
            return Warrior(name)
        elif character_type.lower() == "mage":
            return Mage(name)
        elif character_type.lower() == "archer":
            return Archer(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа: {character_type}")


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
    def __init__(self, name, damage, value=100, weight=3.0):
        super().__init__(name, "weapon", value, weight)
        self.damage = damage

    def use(self, character):
        if hasattr(character, 'attack_power'):
            character.attack_power += self.damage
            return f"{character.name} экипировал {self.name}, атака увеличена на {self.damage}"
        else:
            return f"{character.name} не может использовать {self.name} как оружие"


class Potion(GameItem):
    """
    Класс зелья
    """
    def __init__(self, name, healing_power, value=25, weight=0.5):
        super().__init__(name, "potion", value, weight)
        self.healing_power = healing_power

    def use(self, character):
        if hasattr(character, 'health') and hasattr(character, 'max_health'):
            old_health = character.health
            character.health = min(character.max_health, character.health + self.healing_power)
            healed = character.health - old_health
            return f"{character.name} использовал {self.name} и восстановил {healed} здоровья"
        else:
            return f"{character.name} не может использовать {self.name} как зелье"


class Armor(GameItem):
    """
    Класс брони
    """
    def __init__(self, name, defense, value=150, weight=10.0):
        super().__init__(name, "armor", value, weight)
        self.defense = defense

    def use(self, character):
        if hasattr(character, 'defense'):
            character.defense += self.defense
            return f"{character.name} экипировал {self.name}, защита увеличена на {self.defense}"
        else:
            return f"{character.name} не может использовать {self.name} как броню"


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
    def create_item(self, name, damage=10, value=100, weight=3.0):
        return Weapon(name, damage, value, weight)


class PotionCreator(ItemCreator):
    """
    Создатель зелий
    """
    def create_item(self, name, healing_power=30, value=25, weight=0.5):
        return Potion(name, healing_power, value, weight)


class ArmorCreator(ItemCreator):
    """
    Создатель брони
    """
    def create_item(self, name, defense=5, value=150, weight=10.0):
        return Armor(name, defense, value, weight)


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


class FantasyButton(Button):
    """
    Кнопка в фэнтезийном стиле
    """
    def render(self):
        return f"✨ Фэнтезийная кнопка '{self.text}' ({self.width}x{self.height}) с рунами"


class FantasyTextField(TextField):
    """
    Текстовое поле в фэнтезийном стиле
    """
    def render(self):
        return f"📜 Фэнтезийное текстовое поле '{self.placeholder}' ({self.width}x{self.height}) с магической каймой"


class FantasyUIFactory(UIFactory):
    """
    Фабрика UI-элементов в фэнтезийном стиле
    """
    def create_button(self, text, width=100, height=30):
        return FantasyButton(text, width, height)

    def create_text_field(self, placeholder="", width=200, height=30):
        return FantasyTextField(placeholder, width, height)


class SciFiButton(Button):
    """
    Кнопка в стиле sci-fi
    """
    def render(self):
        return f" futuristic кнопка '{self.text}' ({self.width}x{self.height}) с голограммой"


class SciFiTextField(TextField):
    """
    Текстовое поле в стиле sci-fi
    """
    def render(self):
        return f" futuristic текстовое поле '{self.placeholder}' ({self.width}x{self.height}) с цифровым интерфейсом"


class SciFiUIFactory(UIFactory):
    """
    Фабрика UI-элементов в стиле sci-fi
    """
    def create_button(self, text, width=100, height=30):
        return SciFiButton(text, width, height)

    def create_text_field(self, placeholder="", width=200, height=30):
        return SciFiTextField(placeholder, width, height)


class MedievalButton(Button):
    """
    Кнопка в средневековом стиле
    """
    def render(self):
        return f"🛡️ Средневековая кнопка '{self.text}' ({self.width}x{self.height}) с гербом"


class MedievalTextField(TextField):
    """
    Текстовое поле в средневековом стиле
    """
    def render(self):
        return f"📜 Средневековое текстовое поле '{self.placeholder}' ({self.width}x{self.height}) на пергаменте"


class MedievalUIFactory(UIFactory):
    """
    Фабрика UI-элементов в средневековом стиле
    """
    def create_button(self, text, width=100, height=30):
        return MedievalButton(text, width, height)

    def create_text_field(self, placeholder="", width=200, height=30):
        return MedievalTextField(placeholder, width, height)


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


class Goblin(Monster):
    """
    Класс гоблина
    """
    def __init__(self, name, health=30, attack_power=8, monster_type="goblin"):
        super().__init__(name, health, attack_power, monster_type)
        self.speed = 8  # Гоблины быстрые

    def special_attack(self):
        return f"{self.name} быстро наносит двойной удар!"


class Orc(Monster):
    """
    Класс орка
    """
    def __init__(self, name, health=70, attack_power=15, monster_type="orc"):
        super().__init__(name, health, attack_power, monster_type)
        self.armor = 5  # Орки крепкие

    def special_attack(self):
        return f"{self.name} яростно атакует с дополнительным уроном!"


class Dragon(Monster):
    """
    Класс дракона
    """
    def __init__(self, name, health=200, attack_power=30, monster_type="dragon"):
        super().__init__(name, health, attack_power, monster_type)
        self.fire_damage = 15  # Дракон дышит огнем

    def special_attack(self):
        return f"{self.name} испускает огненное дыхание!"


class Skeleton(Monster):
    """
    Класс скелета
    """
    def __init__(self, name, health=40, attack_power=12, monster_type="skeleton"):
        super().__init__(name, health, attack_power, monster_type)
        self.resistance = "holy"  # Сопротивление святому урону

    def special_attack(self):
        return f"{self.name} восстанавливает часть здоровья!"


class MonsterFactory:
    """
    Фабрика для создания монстров с параметрами
    """
    @staticmethod
    def create_monster(monster_type, name=None, health=None, attack_power=None, difficulty="normal"):
        """
        Создать монстра с указанными параметрами
        """
        # Если имя не указано, генерируем случайное
        if name is None:
            names = {
                "goblin": ["Гоблин-вор", "Гоблин-шаман", "Гоблин-воин"],
                "orc": ["Орк-берсерк", "Орк-маг", "Орк-вождь"],
                "dragon": ["Молодой дракон", "Древний дракон", "Огненный дракон"],
                "skeleton": ["Скелет-воин", "Скелет-лучник", "Скелет-маг"]
            }
            name = random.choice(names.get(monster_type, [f"{monster_type.capitalize()}"]))

        # Устанавливаем базовые параметры в зависимости от типа
        base_stats = {
            "goblin": {"health": 30, "attack": 8},
            "orc": {"health": 70, "attack": 15},
            "dragon": {"health": 200, "attack": 30},
            "skeleton": {"health": 40, "attack": 12}
        }

        # Применяем модификаторы сложности
        difficulty_multipliers = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.5,
            "legendary": 2.0
        }

        multiplier = difficulty_multipliers.get(difficulty, 1.0)

        # Используем указанные параметры или базовые с учетом сложности
        if health is None:
            base_health = base_stats[monster_type]["health"]
            health = int(base_health * multiplier)
        else:
            # Валидация параметров
            if health <= 0:
                raise ValueError("Здоровье монстра должно быть положительным числом")

        if attack_power is None:
            base_attack = base_stats[monster_type]["attack"]
            attack_power = int(base_attack * multiplier)
        else:
            # Валидация параметров
            if attack_power <= 0:
                raise ValueError("Сила атаки монстра должна быть положительным числом")

        # Создаем монстра по типу
        if monster_type == "goblin":
            return Goblin(name, health, attack_power)
        elif monster_type == "orc":
            return Orc(name, health, attack_power)
        elif monster_type == "dragon":
            return Dragon(name, health, attack_power)
        elif monster_type == "skeleton":
            return Skeleton(name, health, attack_power)
        else:
            raise ValueError(f"Неизвестный тип монстра: {monster_type}")


# Демонстрация работы всех уровней
if __name__ == "__main__":
    print("=== Демонстрация паттерна Factory ===\n")

    # Тестирование уровня 1
    print("--- Уровень 1: Простая фабрика персонажей ---")
    warrior = CharacterFactory.create_character("warrior", "Конан")
    mage = CharacterFactory.create_character("mage", "Мерлин")
    archer = CharacterFactory.create_character("archer", "Робин")

    print(warrior.get_info())
    print(mage.get_info())
    print(archer.get_info())

    print(warrior.special_ability())
    print(mage.special_ability())
    print(archer.special_ability())
    print()

    # Тестирование уровня 2
    print("--- Уровень 2: Фабричный метод для предметов ---")
    weapon_creator = WeaponCreator()
    potion_creator = PotionCreator()
    armor_creator = ArmorCreator()

    sword = weapon_creator.get_item("Меч короля", damage=25, value=200)
    health_potion = potion_creator.get_item("Зелье здоровья", healing_power=50, value=30)
    shield = armor_creator.get_item("Щит", defense=15, value=180)

    print(sword.get_info())
    print(health_potion.get_info())
    print(shield.get_info())

    # Применение предметов к персонажу
    print(sword.use(warrior))
    print(health_potion.use(mage))
    print(shield.use(archer))
    print()

    # Тестирование уровня 3
    print("--- Уровень 3: Абстрактная фабрика UI-элементов ---")
    fantasy_factory = FantasyUIFactory()
    scifi_factory = SciFiUIFactory()
    medieval_factory = MedievalUIFactory()

    # Создаем UI-элементы для разных стилей
    fantasy_button = fantasy_factory.create_button("Начать приключение", 150, 40)
    fantasy_field = fantasy_factory.create_text_field("Введите имя героя", 250, 35)

    scifi_button = scifi_factory.create_button("Активировать щит", 120, 35)
    scifi_field = scifi_factory.create_text_field("Код доступа", 200, 30)

    medieval_button = medieval_factory.create_button("Войти в замок", 140, 45)
    medieval_field = medieval_factory.create_text_field("Логин рыцаря", 220, 35)

    print(fantasy_button.render())
    print(fantasy_field.render())
    print(fantasy_button.click())

    print(scifi_button.render())
    print(scifi_field.render())
    print(scifi_field.input_text("ABCD1234"))

    print(medieval_button.render())
    print(medieval_field.render())
    print(medieval_button.click())
    print()

    # Тестирование фабрики монстров
    print("--- Уровень 3: Параметризованная фабрика монстров ---")
    goblin = MonsterFactory.create_monster("goblin", "Малыш Гоб", difficulty="hard")
    orc = MonsterFactory.create_monster("orc", "Орк-берсерк", health=100, attack_power=20)
    dragon = MonsterFactory.create_monster("dragon", difficulty="legendary")
    skeleton = MonsterFactory.create_monster("skeleton", "Костяной страж", difficulty="normal")

    monsters = [goblin, orc, dragon, skeleton]
    for monster in monsters:
        print(monster.get_info())
        print(monster.special_attack())