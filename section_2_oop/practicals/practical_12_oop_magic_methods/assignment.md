# Практическое занятие 12: ООП - магические методы в игровом контексте

## Цель занятия
Изучить магические методы (dunder methods) в Python и научиться использовать их для придания игровым классам специального поведения, такого как арифметические операции с игровыми параметрами, сравнения для сортировки персонажей, строковое представление игровых объектов и другие.

## Задачи

### Задача 1: Арифметические магические методы для игровых параметров (20 баллов)
Создайте класс `GameCharacter` с:
- Конструктором `__init__()` для инициализации характеристик персонажа (здоровье, атака, защита)
- Методами `__add__()`, `__sub__()` для сложения и вычитания характеристик
- Методом `__mul__()` для увеличения характеристик на множитель
- Методом `__str__()` для строкового представления персонажа

```python
class GameCharacter:
    """
    Класс игрового персонажа
    """
    def __init__(self, name, health, attack, defense, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = 0
        self.is_alive = True

    def __add__(self, other):
        """Сложение характеристик двух персонажей"""
        if isinstance(other, GameCharacter):
            new_health = self.health + other.health
            new_attack = self.attack + other.attack
            new_defense = self.defense + other.defense
            return GameCharacter(f"{self.name}+{other.name}", new_health, new_attack, new_defense)
        else:
            raise TypeError("Можно складывать только с другим персонажем")

    def __sub__(self, other):
        """Вычитание характеристик (например, для вычисления урона)"""
        if isinstance(other, GameCharacter):
            # Для вычитания используем защиту для уменьшения урона
            damage = max(0, self.attack - other.defense)
            return damage
        else:
            raise TypeError("Можно вычитать только характеристики другого персонажа")

    def __mul__(self, factor):
        """Умножение характеристик на множитель (например, для усиления)"""
        if isinstance(factor, (int, float)):
            new_char = GameCharacter(
                f"{self.name}*{factor}", 
                int(self.health * factor), 
                int(self.attack * factor), 
                int(self.defense * factor), 
                self.level
            )
            return new_char
        else:
            raise TypeError("Можно умножать только на число")

    def __str__(self):
        """Строковое представление персонажа"""
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} (Lvl.{self.level}, {status}): HP {self.health}/{self.max_health}, ATK {self.attack}, DEF {self.defense}"

    def __repr__(self):
        """Подробное строковое представление для отладки"""
        return f"GameCharacter(name='{self.name}', health={self.health}, attack={self.attack}, defense={self.defense}, level={self.level})"
```

### Задача 2: Методы сравнения для игровых сущностей (20 баллов)
Реализуйте класс `Player` с:
- Методами `__eq__()`, `__lt__()`, `__le__()`, `__gt__()`, `__ge__()` для сравнения игроков по уровню и опыту
- Методом `__hash__()` для возможности использования в множествах и словарях

```python
class Player:
    """
    Класс игрока для сравнения и сортировки
    """
    def __init__(self, name, level=1, experience=0, guild="None"):
        self.name = name
        self.level = level
        self.experience = experience
        self.guild = guild

    def __eq__(self, other):
        """Проверка равенства игроков по имени и уровню"""
        if isinstance(other, Player):
            return self.name == other.name and self.level == other.level
        return False

    def __lt__(self, other):
        """Сравнение по уровню, затем по опыту"""
        if isinstance(other, Player):
            if self.level != other.level:
                return self.level < other.level
            return self.experience < other.experience
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Player):
            return self < other or self == other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Player):
            if self.level != other.level:
                return self.level > other.level
            return self.experience > other.experience
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Player):
            return self > other or self == other
        return NotImplemented

    def __hash__(self):
        """Хеширование для использования в множествах и словарях"""
        return hash((self.name, self.level, self.experience))

    def __str__(self):
        return f"{self.name} (Lvl.{self.level}, EXP:{self.experience}, Guild:{self.guild})"
```

### Задача 3: Магические методы контейнеров для игрового инвентаря (20 баллов)
Создайте класс `Inventory` с:
- Методами `__getitem__()`, `__setitem__()`, `__delitem__()` для доступа к предметам
- Методом `__len__()` для получения количества предметов
- Методом `__contains__()` для проверки наличия предмета

```python
class Inventory:
    """
    Класс инвентаря игрока
    """
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def __getitem__(self, index):
        """Получение предмета по индексу"""
        if 0 <= index < len(self.items):
            return self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __setitem__(self, index, item):
        """Установка предмета по индексу"""
        if 0 <= index < self.max_size:
            if index < len(self.items):
                self.items[index] = item
            else:
                # Если индекс за пределами текущего списка, расширяем его
                self.items.extend([None] * (index - len(self.items)))
                self.items.append(item)
        else:
            raise IndexError("Индекс вне допустимого размера инвентаря")

    def __delitem__(self, index):
        """Удаление предмета по индексу"""
        if 0 <= index < len(self.items):
            del self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __len__(self):
        """Количество предметов в инвентаре"""
        return len(self.items)

    def __contains__(self, item):
        """Проверка наличия предмета в инвентаре"""
        return item in self.items

    def add_item(self, item):
        """Добавление предмета в инвентарь"""
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        else:
            print("Инвентарь полон!")
            return False

    def __str__(self):
        """Строковое представление инвентаря"""
        if not self.items:
            return "Инвентарь пуст"
        return f"Инвентарь ({len(self.items)}/{self.max_size}): {', '.join(map(str, self.items))}"
```

### Задача 4: Методы для вызова и представления игровых объектов (20 баллов)
Реализуйте класс `Skill` с:
- Методом `__call__()` для применения навыка к цели
- Методами `__repr__()` и `__str__()` для различных представлений объекта

```python
class Skill:
    """
    Класс навыка, который можно применить к цели
    """
    def __init__(self, name, power, skill_type="combat"):
        self.name = name
        self.power = power
        self.skill_type = skill_type  # combat, support, magic, etc.
        self.cooldown = 0
        self.max_cooldown = 3  # максимальный кулдаун

    def __call__(self, target, user=None):
        """Применение навыка к цели"""
        if self.cooldown > 0:
            print(f"Навык {self.name} на кулдауне. Осталось {self.cooldown} ходов.")
            return False

        if hasattr(target, 'health') and hasattr(target, 'is_alive') and target.is_alive:
            if self.skill_type == "combat":
                damage = self.power
                if user and hasattr(user, 'attack'):
                    damage += user.attack * 0.5  # Учитываем атаку пользователя
                target.health -= damage
                print(f"{user.name if user else 'Неизвестный'} использует {self.name} и наносит {damage} урона {target.name}")
                if target.health <= 0:
                    target.health = 0
                    target.is_alive = False
                    print(f"{target.name} погибает!")
            elif self.skill_type == "support":
                if hasattr(target, 'max_health'):
                    heal = min(self.power, target.max_health - target.health)
                    target.health += heal
                    print(f"{user.name if user else 'Неизвестный'} использует {self.name} и восстанавливает {heal} здоровья {target.name}")
            elif self.skill_type == "magic":
                # Магические эффекты могут иметь особую логику
                print(f"{user.name if user else 'Неизвестный'} использует магический навык {self.name} на {target.name}")

            # Устанавливаем кулдаун
            self.cooldown = self.max_cooldown
            return True
        else:
            print(f"Навык {self.name} не может быть применен к {target.name}, цель недоступна")
            return False

    def reduce_cooldown(self):
        """Уменьшение кулдауна"""
        if self.cooldown > 0:
            self.cooldown -= 1

    def __repr__(self):
        return f"Skill(name='{self.name}', power={self.power}, type='{self.skill_type}', cooldown={self.cooldown})"

    def __str__(self):
        status = f" (кулдаун: {self.cooldown})" if self.cooldown > 0 else ""
        return f"{self.name}{status} [{self.skill_type}] - сила {self.power}"
```

### Задача 5: Контекстный менеджер для игровой сессии (20 баллов)
Создайте класс `GameSession` с:
- Методами `__enter__()` и `__exit__()` для безопасной работы с игровыми ресурсами
- Обработкой исключений при завершении сессии

```python
class GameSession:
    """
    Класс игровой сессии как контекстный менеджер
    """
    def __init__(self, player_name, game_map="Tutorial"):
        self.player_name = player_name
        self.game_map = game_map
        self.session_active = False
        self.turn_count = 0
        self.events = []

    def __enter__(self):
        """Начало игровой сессии"""
        print(f"=== Начало игровой сессии для {self.player_name} ===")
        print(f"Карта: {self.game_map}")
        self.session_active = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Завершение игровой сессии"""
        self.session_active = False
        print(f"=== Завершение игровой сессии для {self.player_name} ===")
        print(f"Всего ходов: {self.turn_count}")
        print(f"Событий зарегистрировано: {len(self.events)}")
        if exc_type:
            print(f"Сессия завершена с ошибкой: {exc_type.__name__}: {exc_value}")
        else:
            print("Сессия завершена успешно.")
        return False # Не подавлять исключения, если они были
```

## Методические указания
1. Используйте магические методы для реализации специального поведения игровых классов
2. Обеспечьте корректную обработку типов данных и граничных условий
3. Используйте аннотации типов для лучшей читаемости кода
4. Следите за тем, чтобы парные методы (например, __eq__ и __ne__) работали согласованно
5. Для контекстных менеджеров правильно реализуйте __enter__ и __exit__

## Требования к отчету
- Исходный код программ с игровыми классами
- Примеры использования магических методов в игровом контексте
- Объяснение, зачем нужны те или иные магические методы в игровых системах

## Критерии оценки
- Правильная реализация магических методов: 50%
- Корректная работа игровых классов: 30%
- Качество кода и документация в игровом контексте: 20%

## Практические задания

### Задание 1: Применение арифметических магических методов

Создайте несколько игровых персонажей и продемонстрируйте работу арифметических операций с их характеристиками. Реализуйте методы для:
- Сложения характеристик персонажей
- Вычитания (например, для вычисления урона)
- Умножения (для усиления или ослабления)

```python
# Создаем персонажей
warrior = GameCharacter("Конан", 100, 20, 10, 5)
mage = GameCharacter("Мерлин", 70, 15, 5, 4)

print("Исходные персонажи:")
print(warrior)
print(mage)

# Сложение персонажей
combined = warrior + mage
print(f"\nСложенные характеристики: {combined}")

# Умножение характеристик (усиление)
boosted_warrior = warrior * 1.5
print(f"\nУсиленный воин: {boosted_warrior}")

# Вычитание (урон)
damage = warrior - mage
print(f"\nУрон от воина по магу: {damage}")

# Демонстрация repr
print(f"\nПодробное представление воина: {repr(warrior)}")
```

### Задание 2: Сравнение игровых персонажей

Создайте несколько игроков и реализуйте их сортировку по уровню и опыту. Продемонстрируйте работу методов сравнения использование игроков в коллекциях.

```python
# Создаем игроков
players = [
    Player("Артур", 10, 15000, "Рыцари Света"),
    Player("Ланселот", 12, 23000, "Рыцари Света"),
    Player("Мерлин", 8, 18000, "Хранители Тайн"),
    Player("Робин", 10, 12000, "Лесные Бродяги")
]

print("Исходный список игроков:")
for p in players:
    print(f"  {p}")

# Сортировка игроков
sorted_players = sorted(players)
print("\nОтсортированные игроки по уровню/опыту:")
for p in sorted_players:
    print(f"  {p}")

# Использование в множестве (благодаря __hash__)
player_set = set(players)
print(f"\nКоличество уникальных игроков в множестве: {len(player_set)}")

# Сравнение
print(f"\nАртур < Ланселот: {players[0] < players[1]}")
print(f"Артур == Робин (одинаковый уровень): {players[0] == players[3]}")
```

### Задание 3: Работа с игровым инвентарем

Создайте инвентарь и продемонстрируйте работу магических методов контейнера. Реализуйте добавление, удаление и доступ к предметам в инвентаре.

```python
class Item:
    """Простой класс предмета для демонстрации"""
    def __init__(self, name, item_type="usual"):
        self.name = name
        self.item_type = item_type

    def __str__(self):
        return f"{self.name}({self.item_type})"

    def __repr__(self):
        return f"Item('{self.name}', '{self.item_type}')"

# Создаем инвентарь
inventory = Inventory(5)

# Добавляем предметы
items = [Item("Меч"), Item("Щит"), Item("Зелье"), Item("Шлем")]
for item in items:
    inventory.add_item(item)

print(f"Инвентарь: {inventory}")

# Доступ к элементам через индекс (__getitem__)
print(f"Первый предмет: {inventory[0]}")
print(f"Третий предмет: {inventory[2]}")

# Изменение элемента (__setitem__)
inventory[1] = Item("Броня")
print(f"После замены второго предмета: {inventory}")

# Проверка на вхождение (__contains__)
print(f"Щит в инвентаре: {'Щит' in str(inventory[0])}")

# Длина (__len__)
print(f"Количество предметов: {len(inventory)}")

# Удаление (__delitem__)
del inventory[2]  # Удаляем зелье
print(f"После удаления зелья: {inventory}")
```

### Задание 4: Применение навыков в бою

Создайте навыки и продемонстрируйте их применение к игровым целям. Реализуйте систему кулдаунов и различные типы навыков.

```python
# Создаем персонажей для демонстрации
target = GameCharacter("Гоблин", 50, 5, 2)

# Создаем навыки
slash = Skill("Рубящий удар", 15, "combat")
heal = Skill("Лечебное прикосновение", 20, "support")
fireball = Skill("Огненный шар", 25, "magic")

print(f"Цель до применения навыков: {target}")

# Применяем навыки (__call__)
slash(target, GameCharacter("Игрок", 100, 10, 5))
print(f"После рубящего удара: {target}")

heal(target, None)  # Лечение без пользователя
print(f"После лечения: {target}")

# Показываем строковые представления
print(f"\nНавыки:")
print(f"  {slash}")
print(f"  {heal}")
print(f"  {repr(fireball)}")

# Демонстрируем кулдауны
print(f"\nПробуем использовать рубящий удар снова:")
slash(target, GameCharacter("Игрок", 100, 10, 5))
print(f"Цель: {target}")

# Уменьшаем кулдаун и пробуем снова
slash.reduce_cooldown()
print(f"После уменьшения кулдауна:")
slash(target, GameCharacter("Игрок", 100, 10, 5))
```

### Задание 5: Управление игровой сессией

Создайте игровую сессию с использованием контекстного менеджера и продемонстрируйте его работу в нормальных условиях и при возникновении исключений.

```python
# Использование контекстного менеджера для нормальной сессии
print("=== Демонстрация нормальной сессии ===")
with GameSession("Артур", "Лес Чудес") as session:
    session.turn_count = 5
    session.events = ["Найден меч", "Побежден гоблин", "Открыт сундук", "Получен опыт", "Уровень повышен"]

print()

# Использование контекстного менеджера с исключением
print("=== Демонстрация сессии с исключением ===")
try:
    with GameSession("Ланселот", "Подземелье Теней") as session:
        session.turn_count = 3
        session.events = ["Встречен дракон", "Получен урон", "Использовано зелье"]
        raise ValueError("Игрок покинул игру")
except ValueError as e:
    print(f"Перехвачено исключение: {e}")

print()

# Дополнительный пример использования контекстного менеджера
print("=== Демонстрация сессии с событиями ===")
with GameSession("Эльза", "Замок Льда") as session:
    session.turn_count = 7
    for i in range(session.turn_count):
        session.events.append(f"Ход {i+1}: исследование")
    session.events.append("Найден секретный проход")
    session.events.append("Получено редкое снаряжение")
```

## Дополнительные задания

### Задание 6: Комбинирование магических методов

Создайте класс `GameTeam`, который будет использовать сразу несколько магических методов для управления командой игроков. Реализуйте:
- Сложение команд
- Сравнение команд по среднему уровню
- Доступ к игрокам по индексу
- Итерацию по команде

### Задание 7: Продвинутый инвентарь

Расширьте класс инвентаря, добавив возможность:
- Сортировки предметов по типу
- Поиска предметов по названию
- Группировки одинаковых предметов

## Контрольные вопросы:
1. В чем разница между методами `__str__()` и `__repr__()` в игровом контексте?
2. Какие арифметические магические методы можно использовать для игровых расчетов?
3. Почему важно реализовать метод `__hash__()` для игровых сущностей?
4. Как использовать магические методы контейнеров для реализации игрового инвентаря?
5. Какие преимущества дает использование контекстных менеджеров в игровых сессиях?