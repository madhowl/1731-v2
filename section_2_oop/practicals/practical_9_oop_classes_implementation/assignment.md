# Практическое занятие 9: ООП - реализация классов

## Создание классов игровых сущностей, атрибуты, методы, конструкторы

### Цель занятия:
Научиться создавать классы в Python, определять атрибуты и методы, использовать конструкторы и деструкторы на примере игровых сущностей.

### Задачи:
1. Создать классы игровых сущностей с атрибутами и методами
2. Использовать конструкторы и деструкторы
3. Реализовать инкапсуляцию
4. Применить принципы ООП на практике в игровом контексте

### План работы:
1. Создание простого класса игровой сущности
2. Определение атрибутов и методов
3. Использование конструктора и деструктора
4. Применение принципов инкапсуляции
5. Создание экземпляров класса
6. Практические задания в игровом контексте

---

## 1. Создание простого класса игровой сущности

### Пример 1: Класс GameCharacter

```python
class GameCharacter:
    """
    Класс для представления игрового персонажа
    """
    def __init__(self, name, health, attack_power, character_class="warrior"):
        """
        Конструктор класса GameCharacter
        
        Args:
            name (str): Имя персонажа
            health (int): Здоровье персонажа
            attack_power (int): Сила атаки персонажа
            character_class (str): Класс персонажа
        """
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.created_at = __import__('datetime').datetime.now()
    
    def introduce(self):
        """
        Метод для представления персонажа
        """
        return f"Привет, я {self.name}, {self.character_class} {self.level} уровня"
    
    def is_alive(self):
        """
        Проверка, жив ли персонаж
        """
        return self.health > 0
    
    def take_damage(self, damage):
        """
        Получить урон
        """
        self.health = max(0, self.health - damage)
        return damage
    
    def heal(self, amount):
        """
        Восстановить здоровье
        """
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health
    
    def gain_experience(self, exp):
        """
        Получить опыт и возможно повысить уровень
        """
        self.experience += exp
        # Проверяем, нужно ли повысить уровень
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """
        Повысить уровень персонажа
        """
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 5
        self.experience = 0
        print(f"{self.name} достиг {self.level} уровня!")
    
    def __str__(self):
        """
        Строковое представление объекта
        """
        return f"GameCharacter(name='{self.name}', class='{self.character_class}', level={self.level}, health={self.health}/{self.max_health})"

# Создание экземпляра класса
hero = GameCharacter("Артур", 100, 20, "warrior")
print(hero.introduce())  # Привет, я Артур, warrior 1 уровня
print(f"Жив: {hero.is_alive()}")  # Жив: True
print(hero)  # GameCharacter(name='Артур', class='warrior', level=1, health=100/100)
```

### Пример 2: Класс GameItem

```python
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
    
    def use(self, target_character):
        """
        Использовать предмет на персонаже
        """
        if self.item_type == "potion":
            if "heal" in self._effects:
                healed = target_character.heal(self._effects["heal"])
                self.durability -= 10
                print(f"{target_character.name} восстановил {healed} здоровья с помощью {self.name}")
                return healed
        elif self.item_type == "weapon":
            if "damage" in self._effects:
                target_character.attack_power += self._effects["damage"]
                print(f"{target_character.name} получил бонус к атаке +{self._effects['damage']} от {self.name}")
        return 0
    
    def is_broken(self):
        """
        Проверить, сломан ли предмет
        """
        return self.durability <= 0
    
    def __del__(self):
        """
        Деструктор класса
        """
        print(f"Предмет {self.name} удален из игры...")

# Пример использования
health_potion = GameItem("Зелье здоровья", "potion", 25, 0.5, 1)
health_potion.add_effect("heal", 30)

sword = GameItem("Меч героя", "weapon", 150, 5.0, 100)
sword.add_effect("damage", 10)

print(f"Тип предмета: {health_potion.item_type}")  # Тип предмета: potion
print(f"Эффекты: {health_potion.get_effects()}")   # Эффекты: {'heal': 30}
```

---

## 2. Атрибуты и методы класса в игровом контексте

### Атрибуты экземпляра vs Атрибуты класса

```python
class Monster:
    """
    Класс для представления монстра
    """
    # Атрибут класса - общий для всех монстров
    total_killed = 0
    common_loot_table = ["gold_coin", "health_potion_minor"]
    
    def __init__(self, name, health, attack_power, monster_type="common"):
        self.name = name  # Атрибут экземпляра
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.monster_type = monster_type
        self.alive = True
        self.loot = []  # Атрибут экземпляра
    
    def take_damage(self, damage):
        """
        Получить урон
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            Monster.total_killed += 1  # Увеличиваем счетчик класса
            self.drop_loot()
        return damage
    
    def drop_loot(self):
        """
        Выбросить лут при смерти
        """
        import random
        self.loot = Monster.common_loot_table.copy()
        if self.monster_type == "rare":
            self.loot.append("rare_item")
        elif self.monster_type == "boss":
            self.loot.extend(["legendary_item", "large_gold_pile"])
        print(f"{self.name} выбросил: {', '.join(self.loot)}")
    
    @classmethod
    def get_total_killed(cls):
        """
        Метод класса для получения общего количества убитых монстров
        """
        return cls.total_killed
    
    @staticmethod
    def is_difficult_monster(monster_type):
        """
        Статический метод для проверки типа монстра
        """
        return monster_type in ["rare", "boss"]

# Пример использования
goblin = Monster("Гоблин", 30, 8, "common")
orc = Monster("Орк", 60, 15, "rare")
dragon = Monster("Дракон", 300, 50, "boss")

print(f"Всего убито монстров: {Monster.get_total_killed()}")  # Всего убито монстров: 0

# Убиваем монстров
goblin.take_damage(30)
orc.take_damage(60)

print(f"Всего убито монстров: {Monster.get_total_killed()}")  # Всего убито монстров: 2
print(f"Орк редкий?: {Monster.is_difficult_monster('rare')}")  # Орк редкий?: True
```

---

## 3. Инкапсуляция в игровом контексте

### Уровни доступа в Python

```python
class Player:
    """
    Класс для представления игрока
    """
    def __init__(self, name, level=1, gold=0):
        self.name = name  # Публичный атрибут
        self.level = level  # Публичный атрибут
        self._experience = 0  # Защищенный атрибут (соглашение)
        self.__password_hash = self.__hash_password("default_password")  # Приватный атрибут (сильное соглашение)
        self.__account_balance = gold  # Приватный атрибут для игровой валюты
        self.__login_attempts = 0  # Приватный атрибут для отслеживания попыток входа
    
    def __hash_password(self, password):
        """Приватный метод для хеширования пароля"""
        return sum(ord(c) for c in password) % 1000000 # Простой хеш для примера
    
    # Методы для доступа к приватным атрибутам
    def get_account_balance(self):
        return self.__account_balance
    
    def add_gold(self, amount):
        if amount > 0:
            self.__account_balance += amount
            print(f"Добавлено {amount} золота. Всего: {self.__account_balance}")
        else:
            print("Количество золота должно быть положительным")
    
    def change_password(self, old_password, new_password):
        """Изменить пароль с проверкой старого пароля"""
        if self.__hash_password(old_password) == self.__password_hash:
            self.__password_hash = self.__hash_password(new_password)
            print("Пароль успешно изменен")
            return True
        else:
            print("Неверный старый пароль")
            self.__login_attempts += 1
            return False
    
    # Использование property
    @property
    def experience(self):
        """Свойство для получения опыта"""
        return self._experience
    
    @experience.setter
    def experience(self, value):
        """Свойство для установки опыта с проверкой"""
        if value < 0:
            raise ValueError("Опыт не может быть отрицательным")
        old_level = self.level
        self._experience = value
        # Проверяем, нужно ли повысить уровень
        exp_needed = self.level * 100
        while self._experience >= exp_needed:
            self.level_up()
            exp_needed = self.level * 100
    
    def level_up(self):
        """Повысить уровень игрока"""
        self.level += 1
        print(f"{self.name} достиг {self.level} уровня!")
    
    @property
    def security_level(self):
        """Свойство для получения уровня безопасности аккаунта"""
        if self.__login_attempts == 0:
            return "Высокий"
        elif self.__login_attempts < 3:
            return "Средний"
        else:
            return "Низкий"

# Пример использования
player = Player("Иван", level=1, gold=100)

print(f"Имя: {player.name}")  # Публичный - доступен
print(f"Уровень: {player.level}")  # Публичный - доступен
print(f"Баланс: {player.get_account_balance()}")  # Через метод

# Работа с опытом через свойства
print(f"Опыт: {player.experience}")  # 0
player.experience = 150  # Это вызовет повышение уровня до 2
print(f"Уровень после опыта: {player.level}")  # 2

# Изменение пароля
player.change_password("default_password", "new_secure_password")
print(f"Уровень безопасности: {player.security_level}")
```

---

## 4. Практические задания в игровом контексте

### Задание 1: Класс Weapon

Создайте класс `Weapon` с атрибутами: название, тип оружия, урон, прочность, редкость.
Реализуйте методы:
- `get_info()` - возвращает информацию о оружии
- `is_usable()` - проверяет, пригодно ли оружие к использованию
- `upgrade()` - улучшает оружие (увеличивает урон и уменьшает прочность)

```python
class Weapon:
    """
    Класс для представления оружия
    """
    weapon_types = ["melee", "ranged", "magic"]
    rarity_levels = ["common", "uncommon", "rare", "epic", "legendary"]
    
    def __init__(self, name, weapon_type, base_damage, durability, rarity="common"):
        # ВАШ КОД ЗДЕСЬ
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
        # ВАШ КОД ЗДЕСЬ
        return f"{self.name} ({self.rarity} {self.weapon_type}): {self.get_damage()} урона, прочность {self.durability}/{self.max_durability}"
    
    def is_usable(self):
        # ВАШ КОД ЗДЕСЬ
        return self.durability > 0
    
    def upgrade(self):
        # ВАШ КОД ЗДЕСЬ
        self.upgrade_level += 1
        self.base_damage *= 1.2  # Увеличиваем урон на 20%
        self.durability = self.max_durability # Восстанавливаем прочность при улучшении
        print(f"{self.name} улучшен до уровня {self.upgrade_level}! Новый урон: {self.get_damage():.1f}")
    
    def get_damage(self):
        """Возвращает текущий урон с учетом уровня улучшения"""
        return self.base_damage * (1 + self.upgrade_level * 0.1)

# Тестирование
sword = Weapon("Меч героя", "melee", 25, 100, "rare")
print(sword.get_info())
print(f"Пригодно к использованию: {sword.is_usable()}")
sword.upgrade()
print(sword.get_info())
```

### Задание 2: Класс Inventory

Создайте класс `Inventory`, который хранит список предметов и предоставляет методы:
- `add_item(item)` - добавляет предмет в инвентарь
- `remove_item(item_name)` - удаляет предмет по имени
- `get_items_by_type(item_type)` - находит предметы по типу
- `get_total_weight()` - возвращает общий вес инвентаря

```python
class Inventory:
    """
    Класс для представления инвентаря игрока
    """
    def __init__(self, max_capacity=10, max_weight=100):
        # ВАШ КОД ЗДЕСЬ
        self.items = []
        self.max_capacity = max_capacity
        self.max_weight = max_weight
    
    def add_item(self, item):
        # ВАШ КОД ЗДЕСЬ
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
        # ВАШ КОД ЗДЕСЬ
        for i, item in enumerate(self.items):
            if item.name == item_name:
                removed_item = self.items.pop(i)
                print(f"Предмет {item_name} удален из инвентаря")
                return removed_item
        print(f"Предмет {item_name} не найден в инвентаре")
        return None
    
    def get_items_by_type(self, item_type):
        # ВАШ КОД ЗДЕСЬ
        return [item for item in self.items if item.item_type == item_type]
    
    def get_total_weight(self):
        # ВАШ КОД ЗДЕСЬ
        return sum(item.weight for item in self.items)
    
    def get_total_value(self):
        """Возвращает общую стоимость всех предметов в инвентаре"""
        return sum(item.value for item in self.items)
```

### Задание 3: Класс GameLocation

Создайте класс `GameLocation` с атрибутами: название, тип локации, уровень опасности, список NPC, список монстров.
Реализуйте методы:
- `enter_location(player)` - позволяет игроку войти в локацию
- `spawn_monster()` - создает нового монстра в локации
- `get_safe()` - снижает уровень опасности
- `get_age()` - возвращает возраст локации

```python
class GameLocation:
    """
    Класс для представления игровой локации
    """
    location_types = ["town", "dungeon", "forest", "mountain", "castle", "cave"]
    
    def __init__(self, name, location_type, danger_level=1):
        # ВАШ КОД ЗДЕСЬ
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
        # ВАШ КОД ЗДЕСЬ
        print(f"{player.name} входит в {self.name} (уровень опасности: {self.danger_level})")
        if self.danger_level > player.level:
            print("Внимание! Уровень опасности выше вашего уровня!")
        else:
            print("Уровень опасности приемлем для вас.")
    
    def spawn_monster(self, monster_name, monster_health, monster_attack, monster_type="common"):
        # ВАШ КОД ЗДЕСЬ
        from random import randint
        monster = Monster(monster_name, monster_health, monster_attack, monster_type)
        self.monsters.append(monster)
        print(f"Появился {monster_name} в {self.name}!")
        return monster
    
    def get_safe(self):
        # ВАШ КОД ЗДЕСЬ
        if self.danger_level > 1:
            self.danger_level -= 1
            print(f"Уровень опасности в {self.name} снижен до {self.danger_level}")
        else:
            print(f"{self.name} уже безопасен (минимальный уровень опасности)")
    
    def get_age(self):
        # ВАШ КОД ЗДЕСЬ
        import datetime
        current_time = datetime.datetime.now()
        age = current_time - self.created_at
        return age.days

# Тестирование
location = GameLocation("Темный лес", "forest", 5)
print(f"Возраст локации: {location.get_age()} дней")
player = Player("Алекс", level=3)
location.enter_location(player)
```

---

## 5. Дополнительные задания

### Задание 4: Класс для управления квестами

Создайте класс `QuestManager`, который позволяет:
- Добавлять квесты с описанием и наградой
- Отмечать квесты как выполненные
- Получать список активных квестов
- Получать квесты по сложности

### Задание 5: Класс для игровой экономики

Создайте класс `EconomySystem`, который реализует основные экономические операции в игре и хранит историю транзакций.

---

## Контрольные вопросы:
1. В чем разница между атрибутами класса и атрибутами экземпляра в игровом контексте?
2. Какие уровни доступа к атрибутам существуют в Python и как они применяются в играх?
3. Что такое конструктор и деструктор в Python и как они используются в игровых объектах?
4. Как использовать property в игровых классах для контроля параметров?
5. В чем преимущество инкапсуляции в игровых системах?