# Практическое занятие 3: Работа с итераторами и генераторами в игровом контексте

## Цель занятия
Научиться использовать итераторы и генераторы в Python для эффективной обработки последовательностей данных в игровых приложениях.

## Задачи
1. Создать итераторы для перебора игровых сущностей (монстров, предметов, локаций)
2. Реализовать генераторы для динамической генерации контента (лута, квестов, локаций)
3. Применить встроенные функции Python (map, filter, zip, enumerate) для обработки игровых данных
4. Создать генераторы для пошаговой обработки игровых событий
5. Реализовать итераторы с возможностью возврата к предыдущему состоянию

## Ход работы

### 1. Создание итераторов в игровом контексте

Создайте файл `game_iterators.py` и реализуйте следующие итераторы:

#### Итератор для перебора инвентаря игрока

```python
class InventoryIterator:
    """
    Итератор для перебора предметов в инвентаре игрока
    """
    def __init__(self, inventory):
        self.inventory = inventory
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте логику получения следующего предмета
        pass  # Замените на ваш код
```

#### Итератор для перебора монстров в локации

```python
class MonsterRoomIterator:
    """
    Итератор для перебора монстров в комнате/локации
    """
    def __init__(self, monsters):
        self.monsters = monsters
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте логику получения следующего монстра
        pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Создание игровых итераторов и генераторов

### Уровень 1 - Начальный

#### Задание 1.1: Создание простого итератора для списка заклинаний

Создайте итератор, который будет перебирать список заклинаний персонажа:

```python
class SpellBookIterator:
    """
    Итератор для перебора заклинаний в книге заклинаний
    """
    def __init__(self, spells):
        self.spells = spells
        self.index = 0

    def __iter__(self):
        # ВАШ КОД ЗДЕСЬ - верните сам объект
        pass  # Замените на ваш код

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте логику получения следующего заклинания
        pass  # Замените на ваш код

# Пример использования:
# spell_list = ["Огненный шар", "Ледяная стрела", "Целительное прикосновение"]
# spell_iterator = SpellBookIterator(spell_list)
# for spell in spell_iterator:
#     print(f"Заклинание: {spell}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class SpellBookIterator:
    """
    Итератор для перебора заклинаний в книге заклинаний
    """
    def __init__(self, spells):
        self.spells = spells
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.spells):
            raise StopIteration
        spell = self.spells[self.index]
        self.index += 1
        return spell
```

</details>

#### Задание 1.2: Создание генератора для последовательности уровней

Создайте генератор, который будет создавать последовательность номеров уровней:

```python
def level_generator(start_level=1, max_level=100):
    """
    Генератор для последовательности номеров уровней
    
    Args:
        start_level (int): Начальный уровень
        max_level (int): Максимальный уровень
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте генератор уровней
    pass  # Замените на ваш код

# Пример использования:
# levels = level_generator(1, 10)
# for level in levels:
#     print(f"Уровень: {level}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
def level_generator(start_level=1, max_level=100):
    """
    Генератор для последовательности номеров уровней
    
    Args:
        start_level (int): Начальный уровень
        max_level (int): Максимальный уровень
    """
    current_level = start_level
    while current_level <= max_level:
        yield current_level
        current_level += 1
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Итератор для обхода дерева скиллов

Создайте итератор для обхода дерева скиллов персонажа:

```python
class SkillTreeIterator:
    """
    Итератор для обхода дерева скиллов (в глубину)
    """
    def __init__(self, skill_tree):
        self.skill_tree = skill_tree
        self.stack = [skill_tree]  # Используем стек для обхода в глубину
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте обход дерева скиллов
        pass  # Замените на ваш код

# Пример структуры дерева скилов:
# skill_tree = {
#     "name": "Воин",
#     "children": [
#         {"name": "Мечник", "children": [{"name": "Мастер меча", "children": []}]},
#         {"name": "Щитоносец", "children": [{"name": "Танк", "children": []}]}
#     ]
# }
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class SkillTreeIterator:
    """
    Итератор для обхода дерева скиллов (в глубину)
    """
    def __init__(self, skill_tree):
        self.skill_tree = skill_tree
        self.stack = [skill_tree]
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        
        current = self.stack.pop()
        
        # Проверяем, не посещали ли мы этот узел
        if id(current) in self.visited:
            return self.__next__()
        
        self.visited.add(id(current))
        
        # Добавляем детей в стек в обратном порядке, чтобы сохранить порядок
        if 'children' in current and current['children']:
            for child in reversed(current['children']):
                self.stack.append(child)
        
        return current['name']
```

</details>

#### Задание 2.2: Генератор для случайной генерации лута

Создайте генератор, который будет создавать случайные предметы для лута:

```python
import random

def loot_generator(loot_pool, drop_rate=0.5):
    """
    Генератор для случайной генерации лута
    
    Args:
        loot_pool (list): Список возможных предметов для лута
        drop_rate (float): Вероятность выпадения предмета (от 0 до 1)
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте генератор лута
    pass  # Замените на ваш код

# Пример использования:
# common_loot = ["Зелье здоровья", "Зелье маны", "Монеты", "Меч"]
# rare_loot = ["Эпическое оружие", "Легендарный доспех"]
# 
# for item in loot_generator(common_loot + rare_loot, 0.3):
#     print(f"Выпал предмет: {item}")
#     # Ограничьте количество итераций для тестирования
#     if random.random() < 0.1:  # 10% шанс остановить генерацию
#         break
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import random

def loot_generator(loot_pool, drop_rate=0.5):
    """
    Генератор для случайной генерации лута
    
    Args:
        loot_pool (list): Список возможных предметов для лута
        drop_rate (float): Вероятность выпадения предмета (от 0 до 1)
    """
    while True:
        if random.random() < drop_rate:
            yield random.choice(loot_pool)
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Итератор с возможностью возврата к предыдущему элементу

Создайте итератор, который позволяет перемещаться вперед и назад по списку элементов:

```python
class BidirectionalIterator:
    """
    Двунаправленный итератор с возможностью перемещения вперед и назад
    """
    def __init__(self, items):
        self.items = items
        self.current_index = -1  # Начинаем перед первым элементом

    def __iter__(self):
        return self

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение следующего элемента
        pass  # Замените на ваш код

    def prev(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение предыдущего элемента
        pass  # Замените на ваш код

    def has_next(self):
        # ВАШ КОД ЗДЕСЬ - проверьте, есть ли следующий элемент
        pass  # Замените на ваш код

    def has_prev(self):
        # ВАШ КОД ЗДЕСЬ - проверьте, есть ли предыдущий элемент
        pass  # Замените на ваш код

# Пример использования:
# items = ["Комната 1", "Коридор", "Комната 2", "Сокровищница"]
# iterator = BidirectionalIterator(items)
# 
# print(next(iterator))  # Комната 1
# print(next(iterator))  # Коридор
# print(iterator.prev())  # Комната 1
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class BidirectionalIterator:
    """
    Двунаправленный итератор с возможностью перемещения вперед и назад
    """
    def __init__(self, items):
        self.items = items
        self.current_index = -1  # Начинаем перед первым элементом

    def __iter__(self):
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index >= len(self.items):
            raise StopIteration
        return self.items[self.current_index]

    def prev(self):
        self.current_index -= 1
        if self.current_index < 0:
            raise StopIteration
        return self.items[self.current_index]

    def has_next(self):
        return self.current_index + 1 < len(self.items)

    def has_prev(self):
        return self.current_index > 0
```

</details>

#### Задание 3.2: Генератор для пошаговой битвы

Создайте генератор, который моделирует пошаговую битву между персонажами:

```python
def battle_generator(player, enemies):
    """
    Генератор для пошаговой битвы
    
    Args:
        player (object): Объект игрока с атрибутами health, attack и т.д.
        enemies (list): Список вражеских персонажей
    """
    round_number = 1
    
    while player.health > 0 and any(enemy.health > 0 for enemy in enemies):
        yield f"Раунд {round_number}:"
        
        # Ход игрока
        if player.health > 0:
            active_enemy = next((enemy for enemy in enemies if enemy.health > 0), None)
            if active_enemy:
                damage = player.attack
                active_enemy.health -= damage
                yield f"Игрок атакует {active_enemy.name} на {damage} урона"
                if active_enemy.health <= 0:
                    yield f"{active_enemy.name} побежден!"
        
        # Ход врагов
        for enemy in enemies:
            if enemy.health > 0 and player.health > 0:
                damage = enemy.attack
                player.health -= damage
                yield f"{enemy.name} атакует игрока на {damage} урона"
        
        round_number += 1
    
    if player.health > 0:
        yield "Игрок победил!"
    else:
        yield "Игрок потерпел поражение!"

# Для этого задания вам также понадобится определить классы Player и Enemy
# class Player:
#     def __init__(self, name, health, attack):
#         self.name = name
#         self.health = health
#         self.attack = attack
#
# class Enemy:
#     def __init__(self, name, health, attack):
#         self.name = name
#         self.health = health
#         self.attack = attack
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
def battle_generator(player, enemies):
    """
    Генератор для пошаговой битвы
    
    Args:
        player (object): Объект игрока с атрибутами health, attack и т.д.
        enemies (list): Список вражеских персонажей
    """
    round_number = 1
    
    while player.health > 0 and any(enemy.health > 0 for enemy in enemies):
        yield f"Раунд {round_number}:"
        
        # Ход игрока
        if player.health > 0:
            active_enemy = next((enemy for enemy in enemies if enemy.health > 0), None)
            if active_enemy:
                damage = player.attack
                active_enemy.health -= damage
                yield f"Игрок атакует {active_enemy.name} на {damage} урона"
                if active_enemy.health <= 0:
                    yield f"{active_enemy.name} побежден!"
        
        # Ход врагов
        for enemy in enemies:
            if enemy.health > 0 and player.health > 0:
                damage = enemy.attack
                player.health -= damage
                yield f"{enemy.name} атакует игрока на {damage} урона"
        
        round_number += 1
    
    if player.health > 0:
        yield "Игрок победил!"
    else:
        yield "Игрок потерпел поражение!"
```

</details>

---

## 2. Практические задания в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.3: Создание генератора для последовательности ходов игрока

Создайте генератор, который будет создавать последовательность возможных действий игрока:

```python
def player_turn_generator(actions):
    """
    Генератор для последовательности действий игрока
    
    Args:
        actions (list): Список возможных действий
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте генератор действий
    pass  # Замените на ваш код

# Пример использования:
# actions = ["атаковать", "защититься", "использовать предмет", "побежать"]
# turn_gen = player_turn_generator(actions)
# for i, action in enumerate(turn_gen):
#     print(f"Ход {i+1}: {action}")
#     if i >= 10: # Ограничим количество для тестирования
#         break
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
def player_turn_generator(actions):
    """
    Генератор для последовательности действий игрока
    
    Args:
        actions (list): Список возможных действий
    """
    while True:
        for action in actions:
            yield action
```

</details>

#### Задание 1.4: Итератор для обхода комнат в подземелье

Создайте итератор, который будет перебирать комнаты в подземелье:

```python
class DungeonRoomIterator:
    """
    Итератор для обхода комнат в подземелье
    """
    def __init__(self, dungeon_rooms):
        self.dungeon_rooms = dungeon_rooms
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте логику получения следующей комнаты
        pass  # Замените на ваш код

# Пример использования:
# rooms = ["Вход", "Зал с сокровищами", "Комната с ловушкой", "Финальная битва"]
# room_iterator = DungeonRoomIterator(rooms)
# for room in room_iterator:
#     print(f"Комната: {room}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class DungeonRoomIterator:
    """
    Итератор для обхода комнат в подземелье
    """
    def __init__(self, dungeon_rooms):
        self.dungeon_rooms = dungeon_rooms
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.dungeon_rooms):
            raise StopIteration
        room = self.dungeon_rooms[self.index]
        self.index += 1
        return room
```

</details>

### Уровень 2 - Средний

#### Задание 2.3: Генератор для процедурной генерации мира

Создайте генератор, который будет создавать случайные клетки игрового мира:

```python
import random

def world_generator(width, height, cell_types=["grass", "water", "forest", "mountain"]):
    """
    Генератор для процедурной генерации игрового мира
    
    Args:
        width (int): Ширина мира
        height (int): Высота мира
        cell_types (list): Типы клеток для генерации
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте генератор мира
    pass  # Замените на ваш код

# Пример использования:
# world_gen = world_generator(5, 5)
# for row in world_gen:
#     print(row)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import random

def world_generator(width, height, cell_types=["grass", "water", "forest", "mountain"]):
    """
    Генератор для процедурной генерации игрового мира
    
    Args:
        width (int): Ширина мира
        height (int): Высота мира
        cell_types (list): Типы клеток для генерации
    """
    for y in range(height):
        row = []
        for x in range(width):
            row.append(random.choice(cell_types))
        yield row
```

</details>

#### Задание 2.4: Итератор для обхода инвентаря по типам предметов

Создайте итератор, который будет перебирать предметы в инвентаре по заданному типу:

```python
class TypedInventoryIterator:
    """
    Итератор для перебора предметов в инвентаре по типу
    """
    def __init__(self, inventory, item_type):
        self.inventory = inventory
        self.item_type = item_type
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте фильтрацию по типу предметов
        pass  # Замените на ваш код

# Для этого задания предположим, что у нас есть класс Item:
# class Item:
#     def __init__(self, name, item_type):
#         self.name = name
#         self.type = item_type
# 
# inventory = [Item("Меч", "weapon"), Item("Щит", "armor"), Item("Зелье", "consumable")]
# weapon_iterator = TypedInventoryIterator(inventory, "weapon")
# for item in weapon_iterator:
#     print(f"Оружие: {item.name}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class TypedInventoryIterator:
    """
    Итератор для перебора предметов в инвентаре по типу
    """
    def __init__(self, inventory, item_type):
        self.inventory = inventory
        self.item_type = item_type
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.inventory):
            item = self.inventory[self.index]
            self.index += 1
            if item.type == self.item_type:
                return item
        raise StopIteration
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.3: Генератор для системы квестов

Создайте генератор, который будет создавать цепочки квестов:

```python
def quest_chain_generator(available_quests, max_chain_length=5):
    """
    Генератор для создания цепочек квестов
    
    Args:
        available_quests (list): Список доступных квестов
        max_chain_length (int): Максимальная длина цепочки
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте генератор цепочек квестов
    pass  # Замените на ваш код

# Для этого задания предположим, что у нас есть класс Quest:
# class Quest:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
# 
# quests = [Quest(f"Квест {i}", f"Описание квеста {i}") for i in range(10)]
# quest_chain_gen = quest_chain_generator(quests)
# for chain in quest_chain_gen:
#     print(f"Цепочка квестов: {[q.name for q in chain]}")
#     # Ограничьте количество для тестирования
#     break
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
def quest_chain_generator(available_quests, max_chain_length=5):
    """
    Генератор для создания цепочек квестов
    
    Args:
        available_quests (list): Список доступных квестов
        max_chain_length (int): Максимальная длина цепочки
    """
    import random
    while True:
        chain_length = random.randint(1, max_chain_length)
        selected_quests = random.sample(available_quests, min(chain_length, len(available_quests)))
        yield selected_quests
```

</details>

#### Задание 3.4: Итератор с фильтрацией и преобразованием

Создайте итератор, который объединяет фильтрацию и преобразование данных:

```python
class FilteredTransformIterator:
    """
    Итератор с фильтрацией и преобразованием данных
    """
    def __init__(self, items, filter_func=None, transform_func=None):
        self.items = items
        self.filter_func = filter_func
        self.transform_func = transform_func
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте фильтрацию и преобразование
        pass  # Замените на ваш код

# Пример использования:
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # Итератор, который возвращает квадраты четных чисел
# iterator = FilteredTransformIterator(
#     numbers, 
#     filter_func=lambda x: x % 2 == 0, 
#     transform_func=lambda x: x ** 2
# )
# for item in iterator:
#     print(item)  # 4, 16, 36, 64, 100
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class FilteredTransformIterator:
    """
    Итератор с фильтрацией и преобразованием данных
    """
    def __init__(self, items, filter_func=None, transform_func=None):
        self.items = items
        self.filter_func = filter_func
        self.transform_func = transform_func
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            
            # Применяем фильтр, если он задан
            if self.filter_func is None or self.filter_func(item):
                # Применяем преобразование, если оно задано
                if self.transform_func is not None:
                    item = self.transform_func(item)
                return item
        
        raise StopIteration
```

</details>

---

## 3. Дополнительные задания

### Задание 4: Комбинированный итератор

Реализуйте итератор, который объединяет несколько источников данных:

1. Создайте итератор, который поочередно возвращает элементы из нескольких коллекций
2. Добавьте возможность указания приоритета для каждой коллекции
3. Реализуйте методы для добавления и удаления коллекций во время итерации

### Задание 5: Генератор для системы улучшений

Разработайте генератор для системы улучшения предметов:

1. Создайте генератор, который моделирует процесс заточки предмета
2. Реализуйте шансы на успех, частичный успех и катастрофу
3. Добавьте возможность получения бонусов при удачной заточке

---

## Контрольные вопросы:
1. В чем разница между итератором и генератором?
2. Какие преимущества дают генераторы по сравнению с обычными функциями?
3. Как работает протокол итерации в Python?
4. Какие игровые задачи хорошо решаются с помощью итераторов и генераторов?
5. Какие встроенные функции Python можно эффективно использовать с итераторами и генераторами?