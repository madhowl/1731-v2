# Практическое занятие 14: ООП - паттерн Factory в игровом контексте

## Цель занятия
Изучить паттерн проектирования Factory (Фабрика) и научиться реализовывать его в Python для создания игровых объектов без указания их конкретных классов, а также понять, когда и зачем использовать различные варианты паттерна Factory в игровой разработке.

## Задачи

### Задача 1: Простая фабрика для создания игровых персонажей (20 баллов)
Создайте фабрику `CharacterFactory` для создания персонажей:
- Абстрактный класс `GameCharacter` с методом `get_info()`
- Конкретные классы: `Warrior`, `Mage`, `Archer`
- Фабричный метод `create_character(character_type, name)`

```python
from abc import ABC, abstractmethod

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
        self.mana = 100
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


# Пример использования
warrior = CharacterFactory.create_character("warrior", "Конан")
mage = CharacterFactory.create_character("mage", "Мерлин")
archer = CharacterFactory.create_character("archer", "Робин")

print(warrior.get_info())
print(mage.get_info())
print(archer.get_info())

print(warrior.special_ability())
print(mage.special_ability())
```

### Задача 2: Фабричный метод для создания игровых предметов (20 баллов)
Реализуйте паттерн "Фабричный метод" с:
- Абстрактным классом `ItemCreator` с методом `create_item()`
- Конкретными классами: `WeaponCreator`, `PotionCreator`, `ArmorCreator`
- Абстрактным методом `create_item()` и конкретными реализациями

```python
from abc import ABC, abstractmethod

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


# Пример использования
weapon_creator = WeaponCreator()
potion_creator = PotionCreator()
armor_creator = ArmorCreator()

sword = weapon_creator.get_item("Меч короля", damage=25, value=200)
health_potion = potion_creator.get_item("Зелье здоровья", healing_power=50, value=30)
shield = armor_creator.get_item("Щит", defense=15, value=180)

print(sword.get_info())
print(health_potion.get_info())
print(shield.get_info())
```

### Задача 3: Абстрактная фабрика для UI-элементов (20 баллов)
Создайте абстрактную фабрику UI-элементов для игрового интерфейса:
- Интерфейс `UIFactory` с методами для создания кнопок и текстовых полей
- Конкретные фабрики: `FantasyUIFactory`, `SciFiUIFactory`, `MedievalUIFactory`
- Классы элементов: `Button`, `TextField`

```python
from abc import ABC, abstractmethod

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


# Пример использования
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
```

### Задача 4: Параметризованная фабрика для создания монстров (20 баллов)
Реализуйте фабрику `MonsterFactory` с параметрами:
- Возможность создания монстров с определенными свойствами (здоровье, урон, тип)
- Поддержка различных типов монстров: `Goblin`, `Orc`, `Dragon`, `Skeleton`
- Валидация параметров при создании

```python
from abc import ABC, abstractmethod
import random

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


# Пример использования
goblin = MonsterFactory.create_monster("goblin", "Малыш Гоб", difficulty="hard")
orc = MonsterFactory.create_monster("orc", "Орк-берсерк", health=100, attack_power=20)
dragon = MonsterFactory.create_monster("dragon", difficulty="legendary")
skeleton = MonsterFactory.create_monster("skeleton", "Костяной страж", difficulty="normal")

monsters = [goblin, orc, dragon, skeleton]
for monster in monsters:
    print(monster.get_info())
    print(monster.special_attack())
```

### Задача 5: Фабрика с кэшированием игровых объектов (20 баллов)
Создайте фабрику `ObjectPoolFactory`:
- Кэширование созданных объектов для повторного использования
- Методы получения и возврата объектов
- Управление жизненным циклом объектов

```python
import threading
from collections import defaultdict

class GameObject:
    """
    Базовый класс игрового объекта
    """
    def __init__(self, obj_id, obj_type):
        self.id = obj_id
        self.type = obj_type
        self.active = False  # Объект активен или в пуле
        self.position = (0, 0)
        self.rotation = 0

    def activate(self, x=0, y=0, rotation=0):
        """Активировать объект с заданными параметрами"""
        self.active = True
        self.position = (x, y)
        self.rotation = rotation
        print(f"Объект {self.id} ({self.type}) активирован на позиции {self.position}")

    def deactivate(self):
        """Деактивировать объект и вернуть в пул"""
        self.active = False
        self.position = (0, 0)
        self.rotation = 0
        print(f"Объект {self.id} ({self.type}) деактивирован и возвращен в пул")


class ObjectPoolFactory:
    """
    Фабрика с пулом объектов для повторного использования
    """
    def __init__(self, initial_pool_size=5):
        self.pools = defaultdict(list)  # Пул для каждого типа объектов
        self.id_counter = 0
        self.lock = threading.Lock()  # Для потокобезопасности
        self.initial_pool_size = initial_pool_size

    def initialize_pool(self, obj_type, size=None):
        """Инициализировать пул объектов определенного типа"""
        pool_size = size or self.initial_pool_size
        with self.lock:
            for i in range(pool_size):
                obj_id = f"{obj_type}_{self.id_counter}"
                self.id_counter += 1
                obj = GameObject(obj_id, obj_type)
                self.pools[obj_type].append(obj)

    def get_object(self, obj_type, **params):
        """Получить объект из пула или создать новый при необходимости"""
        with self.lock:
            # Проверяем, есть ли свободные объекты в пуле
            available_objects = [obj for obj in self.pools[obj_type] if not obj.active]
            
            if available_objects:
                obj = available_objects[0]
            else:
                # Создаем новый объект, если пул пуст
                obj_id = f"{obj_type}_{self.id_counter}"
                self.id_counter += 1
                obj = GameObject(obj_id, obj_type)
                self.pools[obj_type].append(obj)
                print(f"Создан новый объект {obj.id} типа {obj_type}")

            # Активируем объект с параметрами
            x = params.get('x', 0)
            y = params.get('y', 0)
            rotation = params.get('rotation', 0)
            obj.activate(x, y, rotation)
            return obj

    def return_object(self, obj):
        """Вернуть объект в пул"""
        with self.lock:
            if obj.active:
                obj.deactivate()
            else:
                print(f"Объект {obj.id} уже находится в пуле")

    def get_pool_status(self):
        """Получить статус пулов"""
        status = {}
        with self.lock:
            for obj_type, pool in self.pools.items():
                active_count = sum(1 for obj in pool if obj.active)
                total_count = len(pool)
                status[obj_type] = {
                    "total": total_count,
                    "active": active_count,
                    "available": total_count - active_count
                }
        return status

    def clear_pool(self, obj_type=None):
        """Очистить пул (все или конкретного типа)"""
        with self.lock:
            if obj_type:
                # Очищаем пул конкретного типа
                for obj in self.pools[obj_type]:
                    if obj.active:
                        obj.deactivate()
                self.pools[obj_type] = []
            else:
                # Очищаем все пулы
                for pool_type in list(self.pools.keys()):
                    for obj in self.pools[pool_type]:
                        if obj.active:
                            obj.deactivate()
                    self.pools[pool_type] = []


# Пример использования
factory = ObjectPoolFactory(initial_pool_size=3)

# Инициализируем пулы для разных типов объектов
factory.initialize_pool("enemy", 3)
factory.initialize_pool("projectile", 5)
factory.initialize_pool("pickup", 2)

print("Статус пулов после инициализации:")
print(factory.get_pool_status())

# Получаем объекты из пула
enemy1 = factory.get_object("enemy", x=100, y=200)
enemy2 = factory.get_object("enemy", x=150, y=250)
projectile1 = factory.get_object("projectile", x=50, y=50, rotation=45)

print("\nСтатус пулов после получения объектов:")
print(factory.get_pool_status())

# Возвращаем объект в пул
factory.return_object(enemy1)

print("\nСтатус пулов после возврата объекта:")
print(factory.get_pool_status())

# Получаем новый объект, который может быть из пула
enemy3 = factory.get_object("enemy", x=300, y=300)
print(f"Получен объект: {enemy3.id}")

print("\nФинальный статус пулов:")
print(factory.get_pool_status())
```

## Методические указания
1. Используйте абстрактные классы для определения общего интерфейса фабрик и создаваемых объектов
2. Применяйте принципы SOLID при проектировании фабрик для игровых объектов
3. Обеспечьте гибкость и расширяемость системы создания объектов
4. Обрабатывайте ошибки при создании объектов с недопустимыми параметрами
5. Рассмотрите использование паттерна Factory Method для специализированных создателей объектов

## Требования к отчету
- Исходный код всех реализаций фабрик с игровой тематикой
- Примеры использования каждой фабрики в игровом контексте
- Сравнение различных подходов к реализации фабрик в игровых приложениях

## Критерии оценки
- Корректная реализация паттерна Factory в игровом контексте: 50%
- Понимание различных вариантов применения в игровой разработке: 30%
- Качество кода и документация в игровом контексте: 20%

## Практические задания

### Задание 1: Фабрика игровых локаций

Создайте фабрику `LocationFactory` для создания различных игровых локаций (лес, пещера, замок, деревня и т.д.). Каждая локация должна иметь свои характеристики (опасность, количество монстров, ресурсы и т.п.).

```python
class GameLocation:
    """
    Абстрактный класс игровой локации
    """
    def __init__(self, name, location_type, danger_level=1, resource_density=1):
        self.name = name
        self.location_type = location_type
        self.danger_level = danger_level
        self.resource_density = resource_density
        self.npcs = []
        self.monsters = []
        self.discovered = False

    @abstractmethod
    def generate_content(self):
        """Генерация содержимого локации"""
        pass

    def get_info(self):
        return f"{self.name} ({self.location_type}): опасность {self.danger_level}, ресурсы {self.resource_density}"


class Forest(GameLocation):
    """
    Лесная локация
    """
    def __init__(self, name, danger_level=2, resource_density=3):
        super().__init__(name, "forest", danger_level, resource_density)
        self.tree_density = 10  # Количество деревьев на единицу площади

    def generate_content(self):
        # Генерация содержимого леса
        import random
        monster_types = ["goblin", "wolf", "ent"]
        self.monsters = [MonsterFactory.create_monster(mt, difficulty="easy") for mt in random.choices(monster_types, k=self.danger_level)]
        print(f"Сгенерировано {len(self.monsters)} монстров в лесу {self.name}")


class Cave(GameLocation):
    """
    Пещерная локация
    """
    def __init__(self, name, danger_level=4, resource_density=5):
        super().__init__(name, "cave", danger_level, resource_density)
        self.depth = 100  # Глубина пещеры в метрах

    def generate_content(self):
        # Генерация содержимого пещеры
        import random
        monster_types = ["goblin", "skeleton", "bat", "spider"]
        self.monsters = [MonsterFactory.create_monster(mt, difficulty="normal") for mt in random.choices(monster_types, k=self.danger_level)]
        print(f"Сгенерировано {len(self.monsters)} монстров в пещере {self.name}")


class Castle(GameLocation):
    """
    Замковая локация
    """
    def __init__(self, name, danger_level=5, resource_density=2):
        super().__init__(name, "castle", danger_level, resource_density)
        self.defenses = 10  # Уровень защиты замка

    def generate_content(self):
        # Генерация содержимого замка
        import random
        monster_types = ["skeleton", "ghost", "knight"]
        self.monsters = [MonsterFactory.create_monster(mt, difficulty="hard") for mt in random.choices(monster_types, k=self.danger_level)]
        print(f"Сгенерировано {len(self.monsters)} монстров в замке {self.name}")


class Village(GameLocation):
    """
    Деревенская локация
    """
    def __init__(self, name, danger_level=1, resource_density=4):
        super().__init__(name, "village", danger_level, resource_density)
        self.population = 50  # Количество жителей

    def generate_content(self):
        # Генерация содержимого деревни
        import random
        npc_names = ["Кузнец", "Торговец", "Мудрец", "Оружейник", "Лекарь"]
        self.npcs = random.sample(npc_names, min(len(npc_names), self.resource_density))
        print(f"Сгенерировано {len(self.npcs)} NPC в деревне {self.name}")


class LocationFactory:
    """
    Фабрика для создания игровых локаций
    """
    @staticmethod
    def create_location(location_type, name, danger_level=None, resource_density=None):
        if location_type.lower() == "forest":
            return Forest(name, danger_level or 2, resource_density or 3)
        elif location_type.lower() == "cave":
            return Cave(name, danger_level or 4, resource_density or 5)
        elif location_type.lower() == "castle":
            return Castle(name, danger_level or 5, resource_density or 2)
        elif location_type.lower() == "village":
            return Village(name, danger_level or 1, resource_density or 4)
        else:
            raise ValueError(f"Неизвестный тип локации: {location_type}")


# Пример использования
forest = LocationFactory.create_location("forest", "Темный лес", danger_level=3)
cave = LocationFactory.create_location("cave", "Пещера гоблинов")
castle = LocationFactory.create_location("castle", "Замок призраков", resource_density=1)
village = LocationFactory.create_location("village", "Деревня ремесленников")

locations = [forest, cave, castle, village]
for loc in locations:
    print(loc.get_info())
    loc.generate_content()
```

### Задание 2: Фабрика игровых эффектов

Создайте фабрику `EffectFactory` для создания различных визуальных и аудиоэффектов в игре (вспышки, взрывы, звуковые эффекты и т.п.).

```python
class GameEffect(ABC):
    """
    Абстрактный класс игрового эффекта
    """
    def __init__(self, name, duration=1.0, intensity=1.0):
        self.name = name
        self.duration = duration  # Продолжительность эффекта в секундах
        self.intensity = intensity  # Интенсивность эффекта
        self.active = False

    @abstractmethod
    def play(self, x, y):
        """Воспроизвести эффект в позиции (x, y)"""
        pass

    @abstractmethod
    def stop(self):
        """Остановить эффект"""
        pass

    def get_info(self):
        status = "активен" if self.active else "неактивен"
        return f"{self.name} ({status}): длительность {self.duration}s, интенсивность {self.intensity}"


class VisualEffect(GameEffect):
    """
    Визуальный эффект
    """
    def __init__(self, name, duration=1.0, intensity=1.0, color="white", particle_count=10):
        super().__init__(name, duration, intensity)
        self.color = color
        self.particle_count = particle_count

    def play(self, x, y):
        self.active = True
        print(f"Воспроизводится визуальный эффект '{self.name}' в точке ({x}, {y})")
        print(f"  Цвет: {self.color}, частиц: {self.particle_count}, интенсивность: {self.intensity}")

    def stop(self):
        self.active = False
        print(f"Визуальный эффект '{self.name}' остановлен")


class AudioEffect(GameEffect):
    """
    Аудиоэффект
    """
    def __init__(self, name, duration=1.0, intensity=1.0, sound_type="sfx", volume=1.0):
        super().__init__(name, duration, intensity)
        self.sound_type = sound_type  # Тип звука: sfx, music, voice
        self.volume = volume

    def play(self, x, y):
        self.active = True
        print(f"Воспроизводится аудиоэффект '{self.name}' (тип: {self.sound_type})")
        print(f"  Громкость: {self.volume}, интенсивность: {self.intensity}")

    def stop(self):
        self.active = False
        print(f"Аудиоэффект '{self.name}' остановлен")


class ParticleEffect(VisualEffect):
    """
    Эффект частиц
    """
    def __init__(self, name, duration=1.0, intensity=1.0, color="white", particle_count=50, particle_lifetime=2.0):
        super().__init__(name, duration, intensity, color, particle_count)
        self.particle_lifetime = particle_lifetime  # Время жизни частиц

    def play(self, x, y):
        self.active = True
        print(f"Воспроизводится эффект частиц '{self.name}' в точке ({x}, {y})")
        print(f"  Цвет: {self.color}, частиц: {self.particle_count}, время жизни: {self.particle_lifetime}s")


class EffectFactory:
    """
    Фабрика для создания игровых эффектов
    """
    @staticmethod
    def create_effect(effect_type, name, **params):
        duration = params.get('duration', 1.0)
        intensity = params.get('intensity', 1.0)

        if effect_type.lower() == "visual":
            color = params.get('color', 'white')
            particle_count = params.get('particle_count', 10)
            return VisualEffect(name, duration, intensity, color, particle_count)
        elif effect_type.lower() == "audio":
            sound_type = params.get('sound_type', 'sfx')
            volume = params.get('volume', 1.0)
            return AudioEffect(name, duration, intensity, sound_type, volume)
        elif effect_type.lower() == "particle":
            color = params.get('color', 'white')
            particle_count = params.get('particle_count', 50)
            particle_lifetime = params.get('particle_lifetime', 2.0)
            return ParticleEffect(name, duration, intensity, color, particle_count, particle_lifetime)
        else:
            raise ValueError(f"Неизвестный тип эффекта: {effect_type}")


# Пример использования
flash = EffectFactory.create_effect("visual", "Вспышка", color="yellow", intensity=2.0, particle_count=20)
explosion = EffectFactory.create_effect("particle", "Взрыв", color="orange", intensity=3.0, particle_count=100, particle_lifetime=1.5)
sound = EffectFactory.create_effect("audio", "Звук удара", sound_type="sfx", volume=0.8, intensity=1.5)

effects = [flash, explosion, sound]
for effect in effects:
    print(effect.get_info())
    effect.play(100, 200)
    effect.stop()
```

### Задание 3: Сравнение различных фабрик

Создайте таблицу сравнения различных типов фабрик (Simple Factory, Factory Method, Abstract Factory, Object Pool) по критериям: сложность реализации, гибкость, производительность, применимость в игровой разработке. Приведите примеры, когда каждый тип фабрики наиболее эффективен в игровом контексте.

```python
def compare_factories():
    """
    Сравнение различных типов фабрик
    """
    comparison = {
        "Simple Factory": {
            "Сложность реализации": "Низкая",
            "Гибкость": "Средняя",
            "Производительность": "Высокая",
            "Применимость в играх": "Создание персонажей, предметов с известными типами"
        },
        "Factory Method": {
            "Сложность реализации": "Средняя",
            "Гибкость": "Высокая",
            "Производительность": "Высокая",
            "Применимость в играх": "Создание специализированных объектов (оружие, броня, зелья)"
        },
        "Abstract Factory": {
            "Сложность реализации": "Высокая",
            "Гибкость": "Очень высокая",
            "Производительность": "Средняя",
            "Применимость в играх": "Создание наборов связанных объектов (UI-элементы для разных стилей)"
        },
        "Object Pool": {
            "Сложность реализации": "Средняя",
            "Гибкость": "Средняя",
            "Производительность": "Очень высокая (для повторно используемых объектов)",
            "Применимость в играх": "Создание часто используемых объектов (пули, эффекты, монстры)"
        }
    }

    print("Сравнение типов фабрик в игровой разработке:")
    print("-" * 80)
    print(f"{'Тип фабрики':<20} {'Сложность':<12} {'Гибкость':<10} {'Произв.':<10} {'Применимость':<30}")
    print("-" * 80)

    for factory_type, props in comparison.items():
        print(f"{factory_type:<20} {props['Сложность реализации']:<12} {props['Гибкость']:<10} {props['Производительность']:<10} {props['Применимость в играх']:<30}")

compare_factories()
```

## Дополнительные задания

### Задание 4: Фабрика игровых событий

Создайте `EventFactory` для создания различных игровых событий (сражения, квесты, погодные явления и т.д.) с возможностью параметризации и кастомизации.

### Задание 5: Комбинированная фабрика

Реализуйте фабрику, которая комбинирует несколько паттернов (например, Factory Method + Object Pool) для создания и управления игровыми объектами с оптимизацией производительности и гибкостью настройки.

## Контрольные вопросы:
1. В чем разница между Simple Factory, Factory Method и Abstract Factory в игровом контексте?
2. Как использовать Factory Method для создания специализированных игровых объектов?
3. Когда целесообразно использовать Object Pool вместо простой фабрики в играх?
4. Какие преимущества дает использование абстрактных фабрик для создания UI-элементов в разных стилях?
5. Как обеспечить потокобезопасность фабрик в многопоточных игровых приложениях?