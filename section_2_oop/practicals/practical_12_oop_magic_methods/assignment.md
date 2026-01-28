# Практическое занятие 12: ООП - магические методы в игровом контексте

## Создание классов с магическими методами для игровых сущностей

### Цель занятия:
Научиться использовать магические методы (dunder methods) в Python для придания игровым классам специального поведения, такого как арифметические операции с игровыми параметрами, сравнения для сортировки персонажей, строковое представление игровых объектов и другие.

### Задачи:
1. Создать классы с магическими методами для арифметических операций
2. Реализовать методы сравнения для игровых сущностей
3. Применить методы представления объектов (__str__, __repr__)
4. Использовать методы контейнеров для игровых инвентарей
5. Применить другие специальные методы в игровом контексте

### План работы:
1. Создание классов с арифметическими магическими методами
2. Определение методов сравнения
3. Использование методов представления объектов
4. Применение методов контейнеров
5. Практические задания в игровом контексте

---
# Практическое занятие 12: ООП - магические методы в игровом контексте

## Создание классов с магическими методами для игровых сущностей

### Цель занятия:
Научиться использовать магические методы (dunder methods) в Python для придания игровым классам специального поведения, такого как арифметические операции с игровыми параметрами, сравнения для сортировки персонажей, строковое представление игровых объектов и другие.

### Задачи:
1. Создать классы с магическими методами для арифметических операций
2. Реализовать методы сравнения для игровых сущностей
3. Применить методы представления объектов (__str__, __repr__)
4. Использовать методы контейнеров для игровых инвентарей
5. Применить другие специальные методы в игровом контексте

---

## 1. Теоретическая часть

### Основные понятия магических методов

**Магические методы (dunder methods)** — это специальные методы в Python, которые начинаются и заканчиваются двойным подчеркиванием (например, `__init__`, `__str__`, `__add__`). Они позволяют классам взаимодействовать с встроенными операциями языка, такими как арифметические операции, операции сравнения, доступ к элементам и другие.

**Арифметические магические методы** позволяют определять поведение операторов (`+`, `-`, `*`, `/`, и т.д.) для пользовательских классов. В игровом контексте это может использоваться для объединения характеристик персонажей, вычисления урона и т.д.

**Методы сравнения** (`__eq__`, `__lt__`, `__gt__` и др.) позволяют определять, как сравниваются объекты между собой. Это полезно для сортировки персонажей по уровню, опыту или другим параметрам.

**Методы представления** (`__str__`, `__repr__`) определяют, как объекты будут отображаться при печати или преобразовании в строку. Это важно для отладки и удобного отображения информации об игровых сущностях.

### Пример простого класса с магическими методами (уровень 1 - начальный)

```python
class GameCharacter:
    """
    Класс игрового персонажа с магическими методами
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

    def __str__(self):
        """Строковое представление персонажа"""
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} (Lvl.{self.level}, {status}): HP {self.health}/{self.max_health}, ATK {self.attack}, DEF {self.defense}"

    def __repr__(self):
        """Подробное строковое представление для отладки"""
        return f"GameCharacter(name='{self.name}', health={self.health}, attack={self.attack}, defense={self.defense}, level={self.level})"

# Создание персонажей
warrior = GameCharacter("Конан", 100, 20, 10, 5)
mage = GameCharacter("Мерлин", 70, 15, 5, 4)

print("Исходные персонажи:")
print(warrior)
print(mage)

# Сложение персонажей
combined = warrior + mage
print(f"\nСложенные характеристики: {combined}")

# Вычитание (урон)
damage = warrior - mage
print(f"\nУрон от воина по магу: {damage}")

# Демонстрация repr
print(f"\nПодробное представление воина: {repr(warrior)}")
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание класса с арифметическими операциями

Создайте класс `GameItem` с магическими методами `__add__`, `__mul__`, `__truediv__` для объединения, усиления и разделения игровых предметов. Реализуйте метод `__str__` для строкового представления предмета.

**Шаги выполнения:**
1. Создайте класс `GameItem` с атрибутами: `name`, `power`, `durability`, `weight`
2. Реализуйте метод `__add__` для объединения двух предметов (складываются power и weight, durability усредняется)
3. Реализуйте метод `__mul__` для усиления предмета числовым множителем
4. Реализуйте метод `__truediv__` для разделения предмета на части
5. Создайте метод `__str__` для строкового представления
6. Создайте экземпляры класса и протестируйте магические методы

```python
class GameItem:
    def __init__(self, name, power, durability, weight=1.0):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    def __add__(self, other):
        # ВАШ КОД ЗДЕСЬ - объединение предметов
        pass  # Замените на ваш код

    def __mul__(self, factor):
        # ВАШ КОД ЗДЕСЬ - усиление предмета
        pass  # Замените на ваш код

    def __truediv__(self, divisor):
        # ВАШ КОД ЗДЕСЬ - разделение предмета
        pass  # Замените на ваш код

    def __str__(self):
        # ВАШ КОД ЗДЕСЬ - строковое представление
        pass  # Замените на ваш код

# Пример использования (после реализации)
# sword1 = GameItem("Меч", 20, 100, 5.0)
# sword2 = GameItem("Меч", 15, 80, 4.0)
# combined_sword = sword1 + sword2
# print(f"Объединенный меч: {combined_sword}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class GameItem:
    def __init__(self, name, power, durability, weight=1.0):
        self.name = name
        self.power = power
        self.durability = durability
        self.max_durability = durability  # Максимальная прочность
        self.weight = weight

    def __add__(self, other):
        # Объединение предметов: складываем power и weight, durability усредняем
        if isinstance(other, GameItem):
            new_name = f"{self.name}+{other.name}"
            new_power = self.power + other.power
            new_durability = (self.durability + other.durability) // 2  # Средняя прочность
            new_weight = self.weight + other.weight
            return GameItem(new_name, new_power, new_durability, new_weight)
        else:
            raise TypeError("Можно объединять только с другим игровым предметом")

    def __mul__(self, factor):
        # Усиление предмета: увеличиваем power на множитель
        if isinstance(factor, (int, float)):
            new_power = int(self.power * factor)
            new_durability = min(self.max_durability, int(self.durability * 0.9))  # Немного снижаем прочность
            return GameItem(self.name, new_power, new_durability, self.weight)
        else:
            raise TypeError("Можно умножать только на число")

    def __truediv__(self, divisor):
        # Разделение предмета: уменьшаем характеристики пропорционально
        if isinstance(divisor, (int, float)) and divisor != 0:
            new_power = int(self.power / divisor)
            new_durability = int(self.durability / divisor)
            new_weight = self.weight / divisor
            return GameItem(f"Часть {self.name}", new_power, new_durability, new_weight)
        else:
            raise TypeError("Можно делить только на ненулевое число")

    def __str__(self):
        return f"{self.name}: мощность {self.power}, прочность {self.durability}/{self.max_durability}, вес {self.weight}"
```

</details>

#### Задание 1.2: Класс игрока с методами представления

Создайте класс `Player` с атрибутами: имя, уровень, опыт, гильдия. Реализуйте методы `__str__` и `__repr__` для представления игрока в удобочитаемом и отладочном форматах. Также реализуйте метод `__format__` для форматирования вывода в различных стилях (краткий, полный, для таблицы).

```python
class Player:
    def __init__(self, name, level=1, experience=0, guild="None"):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    def __str__(self):
        # ВАШ КОД ЗДЕСЬ - краткое строковое представление
        pass  # Замените на ваш код

    def __repr__(self):
        # ВАШ КОД ЗДЕСЯ - подробное строковое представление для отладки
        pass  # Замените на ваш код

    def __format__(self, format_spec):
        # ВАШ КОД ЗДЕСЯ - форматирование в различных стилях
        pass  # Замените на ваш код

# Пример использования (после реализации)
# player = Player("Артур", 5, 15000, "Рыцари Света")
# print(f"Краткий вид: {player}")
# print(f"Для отладки: {repr(player)}")
# print(f"Полный вид: {player:full}")
# print(f"Для таблицы: {player:table}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Player:
    def __init__(self, name, level=1, experience=0, guild="None"):
        self.name = name
        self.level = level
        self.experience = experience
        self.guild = guild

    def __str__(self):
        # Краткое строковое представление
        return f"{self.name} (Lvl.{self.level}, EXP:{self.experience}, Guild:{self.guild})"

    def __repr__(self):
        # Подробное строковое представление для отладки
        return f"Player(name='{self.name}', level={self.level}, experience={self.experience}, guild='{self.guild}')"

    def __format__(self, format_spec):
        # Форматирование в различных стилях
        if format_spec == 'full':
            return f"Игрок: {self.name}, Уровень: {self.level}, Опыт: {self.experience}, Гильдия: {self.guild}"
        elif format_spec == 'table':
            # Формат для таблицы: выравнивание по ширине
            return f"{self.name:<12} | {self.level:^6} | {self.experience:>8} | {self.guild}"
        elif format_spec == 'short':
            return f"{self.name}({self.level})"
        else:
            # По умолчанию используем стандартное строковое представление
            return str(self)

# Пример использования
player = Player("Артур", 5, 15000, "Рыцари Света")
print(f"Краткий вид: {player}")
print(f"Для отладки: {repr(player)}")
print(f"Полный вид: {player:full}")
print(f"Для таблицы: {player:table}")
print(f"Короткий вид: {player:short}")
```

</details>


### Уровень 2 - Средний

#### Задание 2.1: Класс инвентаря с методами контейнера

Создайте класс `Inventory` с магическими методами контейнера: `__getitem__`, `__setitem__`, `__delitem__`, `__len__`, `__contains__`. Реализуйте метод `__iter__` для итерации по предметам в инвентаре. Добавьте метод `__bool__` для проверки, пуст ли инвентарь.

**Шаги выполнения:**
1. Создайте класс `Inventory` с атрибутом `items` (список предметов) и ограничением `max_size`
2. Реализуйте методы `__getitem__`, `__setitem__`, `__delitem__` для доступа к элементам по индексу
3. Реализуйте метод `__len__` для получения количества предметов
4. Реализуйте метод `__contains__` для проверки наличия предмета
5. Реализуйте метод `__iter__` для итерации по инвентарю
6. Реализуйте метод `__bool__` для проверки, пуст ли инвентарь
7. Создайте метод `add_item` для добавления предметов

```python
class Inventory:
    def __init__(self, max_size=10):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    def __getitem__(self, index):
        # ВАШ КОД ЗДЕСЯ - получение элемента по индексу
        pass  # Замените на ваш код

    def __setitem__(self, index, item):
        # ВАШ КОД ЗДЕСЯ - установка элемента по индексу
        pass  # Замените на ваш код

    def __delitem__(self, index):
        # ВАШ КОД ЗДЕСЯ - удаление элемента по индексу
        pass  # Замените на ваш код

    def __len__(self):
        # ВАШ КОД ЗДЕСЯ - получение длины инвентаря
        pass  # Замените на ваш код

    def __contains__(self, item):
        # ВАШ КОД ЗДЕСЯ - проверка наличия предмета
        pass  # Замените на ваш код

    def __iter__(self):
        # ВАШ КОД ЗДЕСЯ - итерация по инвентарю
        pass  # Замените на ваш код

    def __bool__(self):
        # ВАШ КОД ЗДЕСЯ - проверка, пуст ли инвентарь
        pass  # Замените на ваш код

    def add_item(self, item):
        # ВАШ КОД ЗДЕСЯ - добавление предмета
        pass  # Замените на ваш код

# Пример использования (после реализации)
# inventory = Inventory(5)
# items = [GameItem("Меч", 20, 100), GameItem("Щит", 10, 150), GameItem("Зелье", 5, 10)]
# for item in items:
#     inventory.add_item(item)
#
# print(f"Количество предметов: {len(inventory)}")
# print(f"Меч в инвентаре: {'Меч' in str(inventory[0])}")
# print("Все предметы в инвентаре:")
# for item in inventory:
#     print(f"  {item}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Inventory:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def __getitem__(self, index):
        # Получение элемента по индексу
        if 0 <= index < len(self.items):
            return self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __setitem__(self, index, item):
        # Установка элемента по индексу
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
        # Удаление элемента по индексу
        if 0 <= index < len(self.items):
            del self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __len__(self):
        # Получение длины инвентаря
        return len(self.items)

    def __contains__(self, item):
        # Проверка наличия предмета
        return item in self.items

    def __iter__(self):
        # Итерация по инвентарю
        return iter(self.items)

    def __bool__(self):
        # Проверка, пуст ли инвентарь
        return bool(self.items)

    def add_item(self, item):
        # Добавление предмета
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        else:
            print("Инвентарь полон!")
            return False

    def __str__(self):
        # Строковое представление инвентаря
        if not self.items:
            return "Инвентарь пуст"
        return f"Инвентарь ({len(self.items)}/{self.max_size}): {', '.join(str(item) for item in self.items)}"

# Пример использования
inventory = Inventory(5)
items = [GameItem("Меч", 20, 100), GameItem("Щит", 10, 150), GameItem("Зелье", 5, 10)]

for item in items:
    inventory.add_item(item)

print(f"Количество предметов: {len(inventory)}")
print(f"Меч в инвентаре: {'Меч' in str(inventory[0])}")
print("Все предметы в инвентаре:")
for item in inventory:
    print(f"  {item}")

print(f"Инвентарь пуст? {not inventory}")
print(f"Строковое представление: {inventory}")
```

</details>

#### Задание 2.2: Класс навыка с методом вызова

Расширьте класс `Skill` из примера выше, добавив магический метод `__call__` для применения навыка к цели. Реализуйте систему кулдаунов и различные типы навыков (атакующие, поддерживающие, магические).

```python
class Skill:
    def __init__(self, name, power, skill_type="combat"):
        # ВАШ КОД ЗДЕСЯ - инициализация атрибутов
        pass  # Замените на ваш код

    def __call__(self, target, user=None):
        # ВАШ КОД ЗДЕСЯ - применение навыка к цели
        pass  # Замените на ваш код

    def reduce_cooldown(self):
        # ВАШ КОД ЗДЕСЯ - уменьшение кулдауна
        pass # Замените на ваш код

    def __str__(self):
        # ВАШ КОД ЗДЕСЯ - строковое представление
        pass  # Замените на ваш код

    def __repr__(self):
        # ВАШ КОД ЗДЕСЯ - отладочное представление
        pass  # Замените на ваш код

# Пример использования (после реализации)
# target = GameCharacter("Гоблин", 50, 5, 2)
# slash = Skill("Рубящий удар", 15, "combat")
# slash(target, GameCharacter("Игрок", 100, 10, 5))  # Применяем навык
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Skill:
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

# Пример использования
target = GameCharacter("Гоблин", 50, 5, 2)
slash = Skill("Рубящий удар", 15, "combat")
heal = Skill("Лечебное прикосновение", 20, "support")
fireball = Skill("Огненный шар", 25, "magic")

print(f"Цель до применения навыков: {target}")

# Применяем навыки
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

</details>


### Уровень 3 - Повышенный

#### Задание 3.1: Контекстный менеджер для игровой сессии

Создайте класс `GameSession` с магическими методами `__enter__` и `__exit__` для безопасной работы с игровыми ресурсами. Реализуйте обработку исключений при завершении сессии, сохранение прогресса и очистку ресурсов. Добавьте методы для отслеживания ходов и игровых событий.

**Шаги выполнения:**
1. Создайте класс `GameSession` с атрибутами: имя игрока, карта, активность сессии, количество ходов, список событий
2. Реализуйте метод `__enter__` для начала сессии
3. Реализуйте метод `__exit__` для завершения сессии с обработкой исключений
4. Добавьте функциональность для отслеживания ходов и событий
5. Продемонстрируйте работу контекстного менеджера в нормальных условиях и при возникновении исключений

```python
class GameSession:
    def __init__(self, player_name, game_map="Tutorial"):
        # ВАШ КОД ЗДЕСЯ - инициализация атрибутов
        pass # Замените на ваш код

    def __enter__(self):
        # ВАШ КОД ЗДЕСЯ - начало сессии
        pass  # Замените на ваш код

    def __exit__(self, exc_type, exc_value, traceback):
        # ВАШ КОД ЗДЕСЯ - завершение сессии
        pass  # Замените на ваш код

# Пример использования (после реализации)
# with GameSession("Артур", "Лес Чудес") as session:
#     session.turn_count = 5
#     session.events = ["Найден меч", "Побежден гоблин", "Открыт сундук"]
#
# print()
#
# # Демонстрация работы с исключением
# try:
#     with GameSession("Ланселот", "Подземелье Теней") as session:
#         session.turn_count = 3
#         session.events = ["Встречен дракон", "Получен урон"]
#         raise ValueError("Игрок покинул игру")
# except ValueError as e:
#     print(f"Перехвачено исключение: {e}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

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

</details>

#### Задание 3.2: Продвинутый класс персонажа с дополнительными магическими методами

Создайте расширенный класс `AdvancedCharacter` с дополнительными магическими методами: `__eq__`, `__lt__`, `__hash__`, `__copy__`, `__deepcopy__`. Реализуйте возможность сравнения персонажей по уровню и опыту, использование в множествах и словарях, копирования персонажа. Добавьте методы для сериализации и десериализации состояния персонажа.

```python
import copy
from typing import Dict, Any

class AdvancedCharacter:
    def __init__(self, name, health, attack, defense, level=1, experience=0):
        # ВАШ КОД ЗДЕСЯ - инициализация атрибутов
        pass  # Замените на ваш код

    def __eq__(self, other):
        # ВАШ КОД ЗДЕСЯ - проверка равенства
        pass  # Замените на ваш код

    def __lt__(self, other):
        # ВАШ КОД ЗДЕСЯ - сравнение по уровню и опыту
        pass  # Замените на ваш код

    def __hash__(self):
        # ВАШ КОД ЗДЕСЯ - хеширование
        pass  # Замените на ваш код

    def __copy__(self):
        # ВАШ КОД ЗДЕСЯ - поверхностное копирование
        pass  # Замените на ваш код

    def __deepcopy__(self, memo):
        # ВАШ КОД ЗДЕСЯ - глубокое копирование
        pass  # Замените на ваш код

    def to_dict(self) -> Dict[str, Any]:
        # ВАШ КОД ЗДЕСЯ - сериализация в словарь
        pass  # Замените на ваш код

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # ВАШ КОД ЗДЕСЯ - создание из словаря
        pass  # Замените на ваш код

# Пример использования (после реализации)
# char1 = AdvancedCharacter("Артур", 100, 20, 10, 5, 15000)
# char2 = AdvancedCharacter("Ланселот", 120, 18, 12, 5, 18000)
# print(f"char1 == char2: {char1 == char2}")
# print(f"char1 < char2: {char1 < char2}")
# print(f"Можно использовать в множестве: {len({char1, char2})}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import copy
from typing import Dict, Any

class AdvancedCharacter:
    def __init__(self, name, health, attack, defense, level=1, experience=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.is_alive = True
        self.inventory = []  # Простой инвентарь

    def __eq__(self, other):
        """Проверка равенства персонажей по имени, уровню и опыту"""
        if isinstance(other, AdvancedCharacter):
            return self.name == other.name and self.level == other.level and self.experience == other.experience
        return False

    def __lt__(self, other):
        """Сравнение по уровню, затем по опыту"""
        if isinstance(other, AdvancedCharacter):
            if self.level != other.level:
                return self.level < other.level
            return self.experience < other.experience
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, AdvancedCharacter):
            return self < other or self == other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, AdvancedCharacter):
            if self.level != other.level:
                return self.level > other.level
            return self.experience > other.experience
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, AdvancedCharacter):
            return self > other or self == other
        return NotImplemented

    def __hash__(self):
        """Хеширование для использования в множествах и словарях"""
        return hash((self.name, self.level, self.experience))

    def __str__(self):
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} (Lvl.{self.level}, {status}): HP {self.health}/{self.max_health}, ATK {self.attack}, DEF {self.defense}"

    def __copy__(self):
        """Поверхностное копирование персонажа"""
        # Создаем новый объект с теми же атрибутами
        new_char = AdvancedCharacter(self.name, self.health, self.attack, self.defense, self.level, self.experience)
        new_char.is_alive = self.is_alive
        # Копируем ссылки на объекты (поверхностное копирование)
        new_char.inventory = self.inventory[:]  # Копируем список инвентаря
        return new_char

    def __deepcopy__(self, memo):
        """Глубокое копирование персонажа"""
        # Создаем новый объект
        new_char = AdvancedCharacter(self.name, self.health, self.attack, self.defense, self.level, self.experience)
        new_char.is_alive = self.is_alive
        # Глубоко копируем составные объекты
        new_char.inventory = copy.deepcopy(self.inventory, memo)
        return new_char

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация персонажа в словарь"""
        return {
            'name': self.name,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'level': self.level,
            'experience': self.experience,
            'is_alive': self.is_alive,
            'inventory': [item.to_dict() if hasattr(item, 'to_dict') else str(item) for item in self.inventory]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Создание персонажа из словаря"""
        char = cls(data['name'], data['health'], data['attack'], data['defense'], data['level'], data['experience'])
        char.max_health = data['max_health']
        char.is_alive = data['is_alive']
        # В реальном приложении здесь нужно десериализовать инвентарь
        char.inventory = data['inventory']
        return char

# Пример использования
char1 = AdvancedCharacter("Артур", 100, 20, 10, 5, 15000)
char2 = AdvancedCharacter("Ланселот", 120, 18, 12, 5, 18000)
char3 = AdvancedCharacter("Артур", 100, 20, 10, 5, 15000)  # Тот же самый персонаж

print(f"char1 == char3: {char1 == char3}")  # Должно быть True
print(f"char1 == char2: {char1 == char2}")  # Должно быть False
print(f"char1 < char2: {char1 < char2}")    # Должно быть True (меньше по опыту при равных уровнях)

# Использование в множестве
char_set = {char1, char2, char3}  # char3 не добавится, т.к. равен char1
print(f"Количество уникальных персонажей в множестве: {len(char_set)}")

# Сортировка
chars = [char1, char2]
sorted_chars = sorted(chars)
print("Отсортированные персонажи:")
for ch in sorted_chars:
    print(f"  {ch}")

# Копирование
char_copy = copy.copy(char1)
print(f"Копия: {char_copy}")

char_deep_copy = copy.deepcopy(char1)
print(f"Глубокая копия: {char_deep_copy}")

# Сериализация
char_dict = char1.to_dict()
print(f"Словарь персонажа: {char_dict}")

# Десериализация
new_char = AdvancedCharacter.from_dict(char_dict)
print(f"Восстановленный персонаж: {new_char}")
```

</details>

---

## 1. Создание классов с арифметическими магическими методами

### Пример 1: Базовые арифметические операции

```python
class GameItem:
    """
    Класс игрового предмета с арифметическими операциями
    """
    def __init__(self, name, power, durability, weight=1.0):
        self.name = name
        self.power = power
        self.durability = durability
        self.max_durability = durability
        self.weight = weight

    def __add__(self, other):
        """Объединение двух предметов"""
        if isinstance(other, GameItem):
            new_name = f"{self.name}+{other.name}"
            new_power = self.power + other.power
            new_durability = (self.durability + other.durability) // 2
            new_weight = self.weight + other.weight
            return GameItem(new_name, new_power, new_durability, new_weight)
        else:
            raise TypeError("Можно объединять только с другим игровым предметом")

    def __mul__(self, factor):
        """Усиление предмета числовым множителем"""
        if isinstance(factor, (int, float)):
            new_power = int(self.power * factor)
            new_durability = min(self.max_durability, int(self.durability * 0.9))  # Немного снижаем прочность
            return GameItem(self.name, new_power, new_durability, self.weight)
        else:
            raise TypeError("Можно умножать только на число")

    def __sub__(self, other):
        """Вычитание одного предмета из другого (например, для улучшения)"""
        if isinstance(other, GameItem):
            power_diff = max(0, self.power - other.power)
            durability_diff = max(0, self.durability - other.durability)
            return GameItem(f"Улучшенный {self.name}", power_diff, durability_diff, self.weight)
        else:
            raise TypeError("Можно вычитать только другой игровой предмет")

    def __str__(self):
        return f"{self.name}: мощность {self.power}, прочность {self.durability}/{self.max_durability}, вес {self.weight}"

# Пример использования
sword1 = GameItem("Меч", 20, 100, 5.0)
sword2 = GameItem("Меч", 15, 80, 4.0)

print(f"Исходные мечи:")
print(f"  {sword1}")
print(f"  {sword2}")

combined_sword = sword1 + sword2
print(f"\nОбъединенный меч: {combined_sword}")

enhanced_sword = sword1 * 1.5
print(f"Усиленный меч: {enhanced_sword}")
```

### Пример 2: Арифметика с персонажами

```python
class GameCharacter:
    """
    Класс игрового персонажа с арифметическими операциями
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

# Создание персонажей
warrior = GameCharacter("Конан", 100, 20, 10, 5)
mage = GameCharacter("Мерлин", 70, 15, 5, 4)

print("Исходные персонажи:")
print(f"  {warrior}")
print(f"  {mage}")

# Сложение персонажей
combined = warrior + mage
print(f"\nСложенные характеристики: {combined}")

# Умножение характеристик (усиление)
boosted_warrior = warrior * 1.5
print(f"Усиленный воин: {boosted_warrior}")

# Вычитание (урон)
damage = warrior - mage
print(f"Урон от воина по магу: {damage}")
```

---

## 2. Методы сравнения в игровом контексте

### Использование методов сравнения для сортировки персонажей

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

---

## 3. Магические методы контейнеров для игровых инвентарей

### Использование методов контейнера для реализации инвентаря

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

    def __iter__(self):
        """Итерация по инвентарю"""
        return iter(self.items)

    def __bool__(self):
        """Проверка, пуст ли инвентарь"""
        return bool(self.items)

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
        return f"Инвентарь ({len(self.items)}/{self.max_size}): {', '.join(str(item) for item in self.items)}"

# Создаем инвентарь
inventory = Inventory(5)

# Добавляем предметы
items = [GameItem("Меч", 20, 100), GameItem("Щит", 10, 150), GameItem("Зелье", 5, 10)]
for item in items:
    inventory.add_item(item)

print(f"Инвентарь: {inventory}")

# Доступ к элементам через индекс (__getitem__)
print(f"Первый предмет: {inventory[0]}")
print(f"Третий предмет: {inventory[2]}")

# Изменение элемента (__setitem__)
inventory[1] = GameItem("Броня", 15, 200)
print(f"После замены второго предмета: {inventory}")

# Проверка на вхождение (__contains__)
print(f"Меч в инвентаре: {items[0] in inventory}")

# Длина (__len__)
print(f"Количество предметов: {len(inventory)}")

# Итерация (__iter__)
print("Все предметы в инвентаре:")
for item in inventory:
    print(f"  {item}")

# Проверка, пуст ли инвентарь (__bool__)
print(f"Инвентарь пуст? {not inventory}")

# Удаление (__delitem__)
del inventory[2]  # Удаляем зелье
print(f"После удаления зелья: {inventory}")
```

---

## 4. Практические задания в игровом контексте

### Задание 1: Класс умений с магическими методами

Создайте класс `Skill` с магическими методами `__call__`, `__str__`, `__repr__` для реализации игровых умений. Добавьте систему кулдаунов и возможность применения умений к целям с различными эффектами (урон, лечение, баффы).

```python
class Skill:
    """
    Класс навыка, который можно применить к цели
    """
    def __init__(self, name, power, skill_type="combat"):
        # ВАШ КОД ЗДЕСЯ - инициализация атрибутов
        pass  # Замените на ваш код

    def __call__(self, target, user=None):
        # ВАШ КОД ЗДЕСЯ - применение навыка
        pass  # Замените на ваш код

    def reduce_cooldown(self):
        # ВАШ КОД ЗДЕСЯ - уменьшение кулдауна
        pass  # Замените на ваш код

    def __str__(self):
        # ВАШ КОД ЗДЕСЯ - строковое представление
        pass  # Замените на ваш код

    def __repr__(self):
        # ВАШ КОД ЗДЕСЯ - отладочное представление
        pass  # Замените на ваш код

class CombatSkills:
    """
    Класс для группировки боевых умений
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЯ - инициализация умений
        pass  # Замените на ваш код

    def __getitem__(self, skill_name):
        # ВАШ КОД ЗДЕСЯ - получение умения по имени
        pass  # Замените на ваш код

    def __iter__(self):
        # ВАШ КОД ЗДЕСЯ - итерация по умениям
        pass  # Замените на ваш код

    def __len__(self):
        # ВАШ КОД ЗДЕСЯ - количество умений
        pass  # Замените на ваш код

# Тестирование
skills = CombatSkills()
target = GameCharacter("Гоблин", 50, 5, 2)

# Применение умений
# skills["slash"](target, GameCharacter("Игрок", 100, 10, 5))
```

### Задание 2: Класс артефакта с методами преобразования

Создайте класс `Artifact` с магическими методами `__int__`, `__float__`, `__bool__`, `__complex__` для преобразования артефакта в различные типы данных. Артефакт может представлять собой магический объект силой, и его можно использовать в арифметических выражениях по-разному в зависимости от контекста.

```python
class Artifact:
    """
    Класс артефакта с методами преобразования типов
    """
    def __init__(self, name, power, rarity="common"):
        # ВАШ КОД ЗДЕСЯ - инициализация атрибутов
        pass  # Замените на ваш код

    def __int__(self):
        # ВАШ КОД ЗДЕСЯ - преобразование в целое число
        pass  # Замените на ваш код

    def __float__(self):
        # ВАШ КОД ЗДЕСЯ - преобразование в вещественное число
        pass  # Замените на ваш код

    def __bool__(self):
        # ВАШ КОД ЗДЕСЯ - логическое значение
        pass  # Замените на ваш код

    def __complex__(self):
        # ВАШ КОД ЗДЕСЯ - преобразование в комплексное число
        pass  # Замените на ваш код

    def __str__(self):
        # ВАШ КОД ЗДЕСЯ - строковое представление
        pass  # Замените на ваш код

    def __repr__(self):
        # ВАШ КОД ЗДЕСЯ - отладочное представление
        pass  # Замените на ваш код

class TreasureChest:
    """
    Класс сокровищницы с артефактами
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЯ - инициализация содержимого
        pass  # Замените на ваш код

    def __contains__(self, artifact_name):
        # ВАШ КОД ЗДЕСЯ - проверка наличия артефакта по имени
        pass  # Замените на ваш код

    def __len__(self):
        # ВАШ КОД ЗДЕСЯ - количество артефактов
        pass  # Замените на ваш код

    def __iter__(self):
        # ВАШ КОД ЗДЕСЯ - итерация по артефактам
        pass  # Замените на ваш код

    def __add__(self, other_chest):
        # ВАШ КОД ЗДЕСЯ - объединение сокровищниц
        pass # Замените на ваш код

# Тестирование
chest = TreasureChest()
print(f"Количество артефактов в сокровищнице: {len(chest)}")
print(f"Содержит 'Магический кристалл'? {'Магический кристалл' in chest}")

# Использование артефактов в выражениях
# artifact = Artifact("Магический кристалл", 50, "rare")
# power_as_int = int(artifact)  # Сила как целое число
# power_as_float = float(artifact)  # Сила как вещественное число
# print(f"Сила артефакта: {power_as_int} (целое), {power_as_float} (вещественное)")
```

### Задание 3: Класс заклинания с контекстным управлением

Создайте класс `Spell` с магическими методами `__enter__` и `__exit__` для реализации заклинания как контекстного менеджера. При входе в контекст заклинание активируется, при выходе - деактивируется, восстанавливая предыдущее состояние персонажа. Реализуйте обработку исключений внутри контекста заклинания.

```python