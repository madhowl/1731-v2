# Практическое занятие 14: ООП - паттерн Factory в игровом контексте

## Создание классов фабрик для игровых сущностей, абстрактные фабрики, фабричные методы

### Цель занятия:
Научиться создавать классы фабрик в Python, определять абстрактные фабрики и фабричные методы, использовать паттерн Factory для создания игровых объектов без указания их конкретных классов.

### Задачи:
1. Создать абстрактные классы фабрик и конкретные реализации
2. Использовать фабричные методы для создания объектов
3. Реализовать различные типы фабрик: простая фабрика, фабричный метод, абстрактная фабрика
4. Применить принципы ООП и паттерн Factory на практике в игровом контексте

### План работы:
1. Создание простой фабрики для создания игровых персонажей
2. Определение абстрактных фабрик и фабричных методов
3. Использование различных типов фабрик для создания игровых объектов
4. Применение принципов инкапсуляции и наследования в фабриках
5. Создание экземпляров классов через фабрики
6. Практические задания в игровом контексте

---
# Практическое занятие 14: ООП - паттерн Factory в игровом контексте

## Создание классов фабрик для игровых сущностей, абстрактные фабрики, фабричные методы

### Цель занятия:
Научиться создавать классы фабрик в Python, определять абстрактные фабрики и фабричные методы, использовать паттерн Factory для создания игровых объектов без указания их конкретных классов.

### Задачи:
1. Создать абстрактные классы фабрик и конкретные реализации
2. Использовать фабричные методы для создания объектов
3. Реализовать различные типы фабрик: простая фабрика, фабричный метод, абстрактная фабрика
4. Применить принципы ООП и паттерн Factory на практике в игровом контексте

---

## 1. Теоретическая часть

### Основные понятия паттерна Factory

**Паттерн Factory (Фабрика)** — это порождающий паттерн проектирования, предоставляющий способ создания объектов без указания их конкретных классов. 

**Простая фабрика** — это класс, который содержит метод, создающий объекты определенного типа на основе входных параметров.

**Фабричный метод** — это метод, который делегирует создание объектов подклассам. Это позволяет подклассам выбрать тип создаваемого объекта.

**Абстрактная фабрика** — это интерфейс для создания семейств связанных или зависимых объектов без указания их конкретных классов.

### Пример простой фабрики (уровень 1 - начальный)

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

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание простой фабрики для игровых предметов

Создайте фабрику `ItemFactory` для создания игровых предметов с атрибутами: имя, тип предмета, стоимость. Реализуйте метод `create_item(item_type, name, value)`, который будет создавать разные типы предметов (оружие, броня, зелье) в зависимости от параметра `item_type`.

**Шаги выполнения:**
1. Создайте абстрактный класс `GameItem` с конструктором `__init__`
2. Создайте классы `Weapon`, `Armor`, `Potion`, наследующиеся от `GameItem`
3. Создайте класс `ItemFactory` с методом `create_item(item_type, name, value)`
4. Протестируйте создание разных предметов с помощью фабрики

```python
from abc import ABC, abstractmethod

class GameItem(ABC):
    def __init__(self, name, item_type, value, weight=1.0):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты
        pass  # Замените на ваш код

    @abstractmethod
    def use(self, character):
        """
        Использовать предмет на персонаже
        """
        pass

    def get_info(self):
        return f"{self.name} ({self.item_type}): стоимость {self.value}, вес {self.weight}"


class Weapon(GameItem):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


class Armor(GameItem):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


class Potion(GameItem):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


class ItemFactory:
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику
    pass


# Пример использования (после реализации)
# weapon = ItemFactory.create_item("weapon", "Меч", 100)
# armor = ItemFactory.create_item("armor", "Щит", 150)
# potion = ItemFactory.create_item("potion", "Зелье", 25)
# print(weapon.get_info())
# print(armor.get_info())
# print(potion.get_info())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

class GameItem(ABC):
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
    def __init__(self, name, value=100, weight=3.0, damage=10):
        super().__init__(name, "weapon", value, weight)
        self.damage = damage

    def use(self, character):
        if hasattr(character, 'attack_power'):
            character.attack_power += self.damage
            return f"{character.name} экипировал {self.name}, атака увеличена на {self.damage}"
        else:
            return f"{character.name} не может использовать {self.name} как оружие"


class Armor(GameItem):
    def __init__(self, name, value=150, weight=10.0, defense=5):
        super().__init__(name, "armor", value, weight)
        self.defense = defense

    def use(self, character):
        if hasattr(character, 'defense'):
            character.defense += self.defense
            return f"{character.name} экипировал {self.name}, защита увеличена на {self.defense}"
        else:
            return f"{character.name} не может использовать {self.name} как броню"


class Potion(GameItem):
    def __init__(self, name, value=25, weight=0.5, healing_power=30):
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


class ItemFactory:
    @staticmethod
    def create_item(item_type, name, value=0, **kwargs):
        """
        Создать предмет по типу
        """
        if item_type.lower() == "weapon":
            damage = kwargs.get('damage', 10)
            return Weapon(name, value, kwargs.get('weight', 3.0), damage)
        elif item_type.lower() == "armor":
            defense = kwargs.get('defense', 5)
            return Armor(name, value, kwargs.get('weight', 10.0), defense)
        elif item_type.lower() == "potion":
            healing_power = kwargs.get('healing_power', 30)
            return Potion(name, value, kwargs.get('weight', 0.5), healing_power)
        else:
            raise ValueError(f"Неизвестный тип предмета: {item_type}")
```

</details>

#### Задание 1.2: Фабрика монстров

Создайте фабрику `MonsterFactory` для создания игровых монстров с атрибутами: имя, здоровье, сила атаки, тип монстра. Реализуйте метод `create_monster(monster_type, name, health, attack_power)`, который будет создавать разные типы монстров (гоблин, орк, дракон).

```python
class Monster(ABC):
    # ВАШ КОД ЗДЕСЬ - реализуйте абстрактный класс монстра
    pass


class Goblin(Monster):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс гоблина
    pass


class Orc(Monster):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс орка
    pass


class Dragon(Monster):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс дракона
    pass


class MonsterFactory:
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику монстров
    pass


# Пример использования (после реализации)
# goblin = MonsterFactory.create_monster("goblin", "Гоблин-воин", 30, 8)
# orc = MonsterFactory.create_monster("orc", "Орк-берсерк", 70, 15)
# dragon = MonsterFactory.create_monster("dragon", "Молодой дракон", 200, 30)
# print(f"Монстр: {goblin.name}, здоровье: {goblin.health}, атака: {goblin.attack_power}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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


class MonsterFactory:
    """
    Фабрика для создания монстров
    """
    @staticmethod
    def create_monster(monster_type, name, health, attack_power):
        """
        Создать монстра по типу
        """
        if monster_type.lower() == "goblin":
            return Goblin(name, health, attack_power)
        elif monster_type.lower() == "orc":
            return Orc(name, health, attack_power)
        elif monster_type.lower() == "dragon":
            return Dragon(name, health, attack_power)
        else:
            raise ValueError(f"Неизвестный тип монстра: {monster_type}")
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Фабричный метод для создания UI-элементов

Создайте систему UI-элементов с использованием паттерна "Фабричный метод". Реализуйте абстрактный класс `UIElementFactory` с методами для создания кнопок и текстовых полей. Создайте конкретные фабрики для разных стилей: `FantasyUIFactory`, `SciFiUIFactory`, `MedievalUIFactory`.

**Шаги выполнения:**
1. Создайте абстрактные классы `Button` и `TextField`
2. Создайте абстрактную фабрику `UIElementFactory`
3. Создайте конкретные реализации фабрик
4. Протестируйте создание UI-элементов разных стилей

```python
class Button(ABC):
    # ВАШ КОД ЗДЕСЬ - реализуйте абстрактный класс кнопки
    pass


class TextField(ABC):
    # ВАШ КОД ЗДЕСЬ - реализуйте абстрактный класс текстового поля
    pass


class UIElementFactory(ABC):
    # ВАШ КОД ЗДЕСЬ - реализуйте абстрактную фабрику
    pass


class FantasyUIFactory(UIElementFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику фэнтезийного стиля
    pass


class SciFiUIFactory(UIElementFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику Sci-Fi стиля
    pass


class MedievalUIFactory(UIElementFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику средневекового стиля
    pass


# Пример использования (после реализации)
# fantasy_factory = UIElementFactory.create_factory("fantasy")
# scifi_factory = UIElementFactory.create_factory("scifi")
# 
# fantasy_button = fantasy_factory.create_button("Начать игру", 150, 40)
# scifi_button = scifi_factory.create_button("Активировать", 120, 35)
# 
# print(fantasy_button.render())
# print(scifi_button.render())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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


class UIElementFactory(ABC):
    """
    Абстрактная фабрика UI-элементов
    """
    @abstractmethod
    def create_button(self, text, width=100, height=30):
        pass

    @abstractmethod
    def create_text_field(self, placeholder="", width=200, height=30):
        pass

    @staticmethod
    def create_factory(style):
        """
        Статический метод для создания фабрики по стилю
        """
        if style.lower() == "fantasy":
            return FantasyUIFactory()
        elif style.lower() == "scifi":
            return SciFiUIFactory()
        elif style.lower() == "medieval":
            return MedievalUIFactory()
        else:
            raise ValueError(f"Неизвестный стиль UI: {style}")


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


class FantasyUIFactory(UIElementFactory):
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


class SciFiUIFactory(UIElementFactory):
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


class MedievalUIFactory(UIElementFactory):
    """
    Фабрика UI-элементов в средневековом стиле
    """
    def create_button(self, text, width=100, height=30):
        return MedievalButton(text, width, height)

    def create_text_field(self, placeholder="", width=200, height=30):
        return MedievalTextField(placeholder, width, height)
```

</details>

#### Задание 2.2: Параметризованная фабрика

Улучшите фабрику `CharacterFactory` из примера выше, добавив возможность создания персонажей с параметрами по умолчанию, а также метод для регистрации новых типов персонажей.

```python
class CharacterFactory:
    # ДОБАВЬТЕ СЛОВАРЬ ДЛЯ ХРАНЕНИЯ ТИПОВ ПЕРСОНАЖЕЙ
    _character_types = {}

    @classmethod
    def register_character_type(cls, character_type, character_class):
        # ВАШ КОД ЗДЕСЬ - зарегистрируйте новый тип персонажа
        pass

    @classmethod
    def create_character(cls, character_type, name, **kwargs):
        # ВАШ КОД ЗДЕСЬ - создайте персонажа с использованием зарегистрированных типов
        pass


# Пример использования (после реализации)
# CharacterFactory.register_character_type("warrior", Warrior)
# CharacterFactory.register_character_type("mage", Mage)
# CharacterFactory.register_character_type("archer", Archer)
# 
# warrior = CharacterFactory.create_character("warrior", "Конан", health=130)
# print(warrior.get_info())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class CharacterFactory:
    """
    Расширяемая фабрика для создания игровых персонажей
    """
    _character_types = {}

    @classmethod
    def register_character_type(cls, character_type, character_class):
        """
        Зарегистрировать новый тип персонажа
        """
        cls._character_types[character_type.lower()] = character_class

    @classmethod
    def create_character(cls, character_type, name, **kwargs):
        """
        Создать персонажа по зарегистрированному типу
        """
        if character_type.lower() not in cls._character_types:
            raise ValueError(f"Неизвестный тип персонажа: {character_type}")
        
        character_class = cls._character_types[character_type.lower()]
        
        # Создаем персонажа, передавая дополнительные параметры
        return character_class(name, **kwargs)

# Регистрация типов
CharacterFactory.register_character_type("warrior", Warrior)
CharacterFactory.register_character_type("mage", Mage)
CharacterFactory.register_character_type("archer", Archer)
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Абстрактная фабрика для игровых миров

Создайте систему абстрактной фабрики для создания игровых миров с разными темами (фэнтези, научная фантастика, постапокалипсис). Каждый мир должен включать в себя персонажей, монстров и предметы в соответствующем стиле.

**Шаги выполнения:**
1. Создайте абстрактную фабрику `WorldFactory`
2. Создайте конкретные фабрики для разных миров
3. Реализуйте создание согласованных наборов объектов для каждого мира
4. Протестируйте создание объектов в разных мирах

```python
class WorldFactory(ABC):
    # ВАШ КОД ЗДЕСЬ - реализуйте абстрактную фабрику мира
    pass


class FantasyWorldFactory(WorldFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику фэнтезийного мира
    pass


class SciFiWorldFactory(WorldFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику Sci-Fi мира
    pass


class PostApocalypticWorldFactory(WorldFactory):
    # ВАШ КОД ЗДЕСЬ - реализуйте фабрику постапокалиптического мира
    pass


# Пример использования (после реализации)
# fantasy_world = FantasyWorldFactory()
# sci_fi_world = SciFiWorldFactory()
# 
# fantasy_warrior = fantasy_world.create_character("warrior", "Артур")
# sci_fi_soldier = sci_fi_world.create_character("soldier", "Капитан Джексон")
# 
# fantasy_weapon = fantasy_world.create_item("weapon", "Эльфийский меч")
# sci_fi_weapon = sci_fi_world.create_item("weapon", "Плазменный резак")
# 
# print(f"Фэнтезийный персонаж: {fantasy_warrior.get_info()}")
# print(f"Sci-Fi персонаж: {sci_fi_soldier.get_info()}")
# print(f"Фэнтезийное оружие: {fantasy_weapon.get_info()}")
# print(f"Sci-Fi оружие: {sci_fi_weapon.get_info()}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class WorldFactory(ABC):
    """
    Абстрактная фабрика для создания игровых миров
    """
    @abstractmethod
    def create_character(self, char_type, name):
        pass

    @abstractmethod
    def create_monster(self, monster_type, name):
        pass

    @abstractmethod
    def create_item(self, item_type, name):
        pass


class FantasyWarrior(GameCharacter):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=22, character_class="fantasy_warrior")
        self.armor = 12
        self.knightly_honor = True

    def special_ability(self):
        return f"{self.name} призывает силу древних рун!"


class FantasyMage(GameCharacter):
    def __init__(self, name):
        super().__init__(name, health=85, attack_power=28, character_class="fantasy_mage")
        self.mana = 120
        self.max_mana = 120

    def special_ability(self):
        if self.mana >= 35:
            self.mana -= 35
            return f"{self.name} сотворяет мощное заклинание! Осталось маны: {self.mana}/{self.max_mana}"
        else:
            return f"{self.name} недостаточно маны для заклинания"


class SciFiSoldier(GameCharacter):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=25, character_class="scifi_soldier")
        self.energy_shield = 30
        self.armor = 15

    def special_ability(self):
        return f"{self.name} активирует энергетический щит!"


class SciFiEngineer(GameCharacter):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=20, character_class="scifi_engineer")
        self.nanobots = 5

    def special_ability(self):
        if self.nanobots > 0:
            self.nanobots -= 1
            self.health = min(self.max_health, self.health + 25)
            return f"{self.name} использует наноботов для восстановления здоровья! Осталось: {self.nanobots}"
        else:
            return f"{self.name} исчерпал запас наноботов!"


class FantasySword(GameItem):
    def __init__(self, name="Эльфийский меч"):
        super().__init__(name, "weapon", 200, weight=2.5)
        self.damage = 30
        self.magical_enchantment = "fire"

    def use(self, character):
        if hasattr(character, 'attack_power'):
            character.attack_power += self.damage
            return f"{character.name} экипировал {self.name}, атака увеличена на {self.damage}. Эффект: магия огня!"
        else:
            return f"{character.name} не может использовать {self.name} как оружие"


class SciFiPlasmaGun(GameItem):
    def __init__(self, name="Плазменный резак"):
        super().__init__(name, "weapon", 250, weight=3.0)
        self.damage = 35
        self.ammo = 50

    def use(self, character):
        if self.ammo > 0:
            self.ammo -= 5
            if hasattr(character, 'attack_power'):
                character.attack_power += self.damage
                return f"{character.name} стреляет из {self.name}, атака увеличена на {self.damage}. Боезапас: {self.ammo}"
        else:
            return f"{self.name} разряжен!"


class FantasyDragon(Monster):
    def __init__(self, name="Древний дракон"):
        super().__init__(name, health=250, attack_power=40, monster_type="fantasy_dragon")
        self.magic_resistance = 0.5
        self.treasure_hoard = ["золото", "драгоценные камни", "магические артефакты"]

    def special_attack(self):
        return f"{self.name} испускает поток магического огня!"


class SciFiRobot(Monster):
    def __init__(self, name="Боевой дрон"):
        super().__init__(name, health=150, attack_power=30, monster_type="scifi_robot")
        self.armor = 20
        self.system_integrity = 100

    def special_attack(self):
        return f"{self.name} активирует лазерную пушку!"


class FantasyWorldFactory(WorldFactory):
    """
    Фабрика для создания объектов фэнтезийного мира
    """
    def create_character(self, char_type, name):
        if char_type.lower() == "warrior":
            return FantasyWarrior(name)
        elif char_type.lower() == "mage":
            return FantasyMage(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа для фэнтезийного мира: {char_type}")

    def create_monster(self, monster_type, name):
        if monster_type.lower() == "dragon":
            return FantasyDragon(name)
        else:
            raise ValueError(f"Неизвестный тип монстра для фэнтезийного мира: {monster_type}")

    def create_item(self, item_type, name):
        if item_type.lower() == "weapon":
            return FantasySword(name)
        else:
            raise ValueError(f"Неизвестный тип предмета для фэнтезийного мира: {item_type}")


class SciFiWorldFactory(WorldFactory):
    """
    Фабрика для создания объектов Sci-Fi мира
    """
    def create_character(self, char_type, name):
        if char_type.lower() == "soldier":
            return SciFiSoldier(name)
        elif char_type.lower() == "engineer":
            return SciFiEngineer(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа для Sci-Fi мира: {char_type}")

    def create_monster(self, monster_type, name):
        if monster_type.lower() == "robot":
            return SciFiRobot(name)
        else:
            raise ValueError(f"Неизвестный тип монстра для Sci-Fi мира: {monster_type}")

    def create_item(self, item_type, name):
        if item_type.lower() == "weapon":
            return SciFiPlasmaGun(name)
        else:
            raise ValueError(f"Неизвестный тип предмета для Sci-Fi мира: {item_type}")


class PostApocalypticWorldFactory(WorldFactory):
    """
    Фабрика для создания объектов постапокалиптического мира
    """
    def create_character(self, char_type, name):
        # Реализуйте создание персонажей для постапокалиптического мира
        raise NotImplementedError("Постапокалиптический мир еще не реализован")

    def create_monster(self, monster_type, name):
        # Реализуйте создание монстров для постапокалиптического мира
        raise NotImplementedError("Постапокалиптический мир еще не реализован")

    def create_item(self, item_type, name):
        # Реализуйте создание предметов для постапокалиптического мира
        raise NotImplementedError("Постапокалиптический мир еще не реализован")
```

</details>

---

## 1. Создание простой фабрики для игровых сущностей

### Пример 1: Класс CharacterFactory

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


class CharacterFactory:
    """
    Фабрика для создания игровых персонажей
    """
    @staticmethod
    def create_character(character_type, name):
        """
        Создать персонажа по типу
        
        Args:
            character_type (str): Тип персонажа (warrior, mage, etc.)
            name (str): Имя персонажа
        """
        if character_type.lower() == "warrior":
            return Warrior(name)
        elif character_type.lower() == "mage":
            return Mage(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа: {character_type}")


# Создание персонажей через фабрику
warrior = CharacterFactory.create_character("warrior", "Конан")
mage = CharacterFactory.create_character("mage", "Мерлин")

print(warrior.get_info())  # Конан (warrior, жив): Lvl.1, HP 120/120, ATK 20
print(mage.get_info())     # Мерлин (mage, жив): Lvl.1, HP 80/80, ATK 25
print(warrior.special_ability())  # Конан использует яростную атаку!
print(mage.special_ability())     # Мерлин произносит мощное заклинание! Осталось маны: 70/100
```

### Пример 2: Класс ItemFactory

```python
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
            print(f"{character.name} использовал {self.name} и восстановил {healed} здоровья")
            return healed
        else:
            return f"{character.name} не может использовать {self.name} как зелье"


class ItemFactory:
    """
    Фабрика для создания игровых предметов
    """
    @staticmethod
    def create_item(item_type, name, **kwargs):
        """
        Создать предмет по типу
        
        Args:
            item_type (str): Тип предмета (weapon, potion, etc.)
            name (str): Название предмета
            **kwargs: Дополнительные параметры для предмета
        """
        if item_type.lower() == "weapon":
            damage = kwargs.get('damage', 10)
            value = kwargs.get('value', 100)
            weight = kwargs.get('weight', 3.0)
            return Weapon(name, damage, value, weight)
        elif item_type.lower() == "potion":
            healing_power = kwargs.get('healing_power', 30)
            value = kwargs.get('value', 25)
            weight = kwargs.get('weight', 0.5)
            return Potion(name, healing_power, value, weight)
        else:
            raise ValueError(f"Неизвестный тип предмета: {item_type}")


# Пример использования
sword = ItemFactory.create_item("weapon", "Меч короля", damage=25, value=200)
health_potion = ItemFactory.create_item("potion", "Зелье здоровья", healing_power=50, value=30)

print(sword.get_info())         # Меч короля (weapon): стоимость 200, вес 3.0
print(health_potion.get_info()) # Зелье здоровья (potion): стоимость 30, вес 0.5
print(sword.use(warrior))       # Конан экипировал Меч короля, атака увеличена на 25
```

---

## 2. Абстрактные фабрики и фабричные методы в игровом контексте

### Фабричный метод vs Абстрактная фабрика

```python
class CharacterCreator(ABC):
    """
    Абстрактный создатель персонажей (фабричный метод)
    """
    @abstractmethod
    def create_character(self, name):
        """
        Абстрактный метод для создания персонажа
        """
        pass

    def get_character(self, name):
        """
        Шаблонный метод, который использует фабричный метод
        """
        character = self.create_character(name)
        # Можно добавить дополнительную логику, например, приветствие
        print(f"Создан персонаж: {character.name}")
        return character


class WarriorCreator(CharacterCreator):
    """
    Конкретный создатель воинов
    """
    def create_character(self, name):
        return Warrior(name)


class MageCreator(CharacterCreator):
    """
    Конкретный создатель магов
    """
    def create_character(self, name):
        return Mage(name)


# Пример использования фабричного метода
warrior_creator = WarriorCreator()
mage_creator = MageCreator()

conan = warrior_creator.get_character("Конан")
merlin = mage_creator.get_character("Мерлин")

print(conan.get_info())
print(merlin.get_info())


class GameWorldFactory(ABC):
    """
    Абстрактная фабрика для создания игрового мира
    """
    @abstractmethod
    def create_character(self, char_type, name):
        pass

    @abstractmethod
    def create_item(self, item_type, name):
        pass

    @abstractmethod
    def create_monster(self, monster_type, name):
        pass


class FantasyWorldFactory(GameWorldFactory):
    """
    Конкретная фабрика для фэнтезийного мира
    """
    def create_character(self, char_type, name):
        if char_type.lower() == "warrior":
            return FantasyWarrior(name)
        elif char_type.lower() == "mage":
            return FantasyMage(name)
        else:
            raise ValueError(f"Неизвестный тип персонажа: {char_type}")

    def create_item(self, item_type, name):
        if item_type.lower() == "weapon":
            return FantasySword(name)
        else:
            raise ValueError(f"Неизвестный тип предмета: {item_type}")

    def create_monster(self, monster_type, name):
        if monster_type.lower() == "dragon":
            return FantasyDragon(name)
        else:
            raise ValueError(f"Неизвестный тип монстра: {monster_type}")


# Пример использования абстрактной фабрики
fantasy_factory = FantasyWorldFactory()

fantasy_warrior = fantasy_factory.create_character("warrior", "Артур")
fantasy_sword = fantasy_factory.create_item("weapon", "Экскалибур")
dragon = fantasy_factory.create_monster("dragon", "Смауг")

print(fantasy_warrior.get_info())
print(fantasy_sword.get_info())
print(dragon.get_info())
print(dragon.special_attack())
```

---

## 3. Практические задания в игровом контексте

### Задание 1: Фабрика игровых локаций

Создайте фабрику `LocationFactory` с методом `create_location(location_type, name, **properties)`, который создает разные типы игровых локаций (лес, пещера, замок, деревня) с определенными свойствами.

```python
class GameLocation:
    """
    Класс игровой локации
    """
    location_types = ["forest", "cave", "castle", "village", "dungeon", "tower"]
    
    def __init__(self, name, location_type, danger_level=1, resource_density=1):
        if location_type not in GameLocation.location_types:
            raise ValueError(f"Тип локации должен быть одним из: {GameLocation.location_types}")
            
        self.name = name
        self.location_type = location_type
        self.danger_level = danger_level
        self.resource_density = resource_density
        self.npcs = []
        self.monsters = []
        self.discovered = False

    def get_info(self):
        return f"{self.name} ({self.location_type}): опасность {self.danger_level}, ресурсы {self.resource_density}"


class LocationFactory:
    """
    Фабрика для создания игровых локаций
    """
    @staticmethod
    def create_location(location_type, name, **properties):
        """
        Создать локацию с заданными свойствами
        
        Args:
            location_type (str): Тип локации
            name (str): Название локации
            **properties: Дополнительные свойства (danger_level, resource_density, etc.)
        """
        # ВАШ КОД ЗДЕСЬ
        pass


# Тестирование
# forest = LocationFactory.create_location("forest", "Темный лес", danger_level=3, resource_density=4)
# cave = LocationFactory.create_location("cave", "Пещера гоблинов", danger_level=5)
# print(forest.get_info())
# print(cave.get_info())
```

### Задание 2: Параметрическая фабрика с кэшированием

Создайте фабрику `CachedCharacterFactory`, которая кэширует созданные объекты и позволяет повторно использовать их при необходимости.

```python
class CachedCharacterFactory:
    """
    Фабрика с кэшированием созданных персонажей
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - инициализируйте кэш
        pass

    def create_or_get_character(self, character_type, name, **kwargs):
        """
        Создать новый персонаж или вернуть существующий из кэша
        """
        # ВАШ КОД ЗДЕСЬ
        pass

    def clear_cache(self):
        """
        Очистить кэш
        """
        # ВАШ КОД ЗДЕСЬ
        pass

    def get_cache_size(self):
        """
        Получить размер кэша
        """
        # ВАШ КОД ЗДЕСЬ
        pass


# Тестирование
# factory = CachedCharacterFactory()
# warrior1 = factory.create_or_get_character("warrior", "Конан")
# warrior2 = factory.create_or_get_character("warrior", "Конан")  # Должен вернуть тот же объект
# print(f"Кэш содержит {factory.get_cache_size()} объектов")
# print(f"Это один и тот же объект? {warrior1 is warrior2}")
```

### Задание 3: Фабрика с поддержкой плагинов

Создайте расширяемую фабрику `ExtensibleFactory`, которая позволяет регистрировать новые типы создаваемых объектов.

```python
class ExtensibleFactory:
    """
    Расширяемая фабрика, позволяющая регистрировать новые типы
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - инициализируйте хранилище типов
        pass

    def register_type(self, type_name, constructor_func):
        """
        Зарегистрировать новый тип
        
        Args:
            type_name (str): Название типа
            constructor_func (callable): Функция-конструктор для создания объекта
        """
        # ВАШ КОД ЗДЕСЬ
        pass

    def create(self, type_name, *args, **kwargs):
        """
        Создать объект зарегистрированного типа
        """
        # ВАШ КОД ЗДЕСЬ
        pass

    def unregister_type(self, type_name):
        """
        Отменить регистрацию типа
        """
        # ВАШ КОД ЗДЕСЬ
        pass


# Пример использования
# factory = ExtensibleFactory()
# 
# # Регистрация типов
# factory.register_type("warrior", lambda name: Warrior(name))
# factory.register_type("mage", lambda name: Mage(name))
# 
# # Создание объектов
# warrior = factory.create("warrior", "Конан")
# mage = factory.create("mage", "Мерлин")
# 
# print(warrior.get_info())
# print(mage.get_info())
```

---

## 4. Дополнительные задания

### Задание 4: Комбинированная фабрика

Создайте фабрику, которая объединяет несколько паттернов (например, Factory Method + Prototype), для создания и клонирования игровых объектов.

### Задание 5: Фабрика с валидацией параметров

Создайте фабрику, которая валидирует входные параметры перед созданием объектов, используя декораторы или специальные классы валидации.

---

## Контрольные вопросы:
1. В чем разница между простой фабрикой, фабричным методом и абстрактной фабрикой в игровом контексте?
2. Какие преимущества дает использование паттерна Factory в игровой разработке?
3. Как обеспечить расширяемость фабрик при добавлении новых типов объектов?
4. Как использовать валидацию параметров в фабриках?
5. Какие проблемы могут возникнуть при использовании фабрик и как их решать?