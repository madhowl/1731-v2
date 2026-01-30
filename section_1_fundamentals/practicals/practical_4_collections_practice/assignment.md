# Практическое занятие 4: Использование модуля collections в игровом контексте

## Цель занятия
Изучить возможности модуля collections в Python и научиться применять его структуры данных для решения игровых задач.

## Задачи
1. Использовать namedtuple для представления игровых сущностей (персонажей, предметов, заклинаний)
2. Применить deque для реализации очередей игровых действий, инвентаря, истории команд
3. Использовать Counter для анализа игровой статистики (частота использования заклинаний, популярность предметов)
4. Применить defaultdict для группировки игровых данных (предметы по типам, монстры по уровням)
5. Использовать OrderedDict для реализации системы достижений с сохранением порядка получения

## Ход работы

### 1. Использование namedtuple в игровом контексте

Создайте файл `game_collections.py` и реализуйте следующие структуры:

#### namedtuple для представления персонажа

```python
from collections import namedtuple

# Создайте namedtuple для представления персонажа
Character = namedtuple('Character', ['name', 'level', 'health', 'mana', 'strength', 'agility', 'intelligence'])

# Создайте экземпляр персонажа
hero = Character("Артур", 10, 100, 50, 15, 12, 8)
print(hero.name)  # Артур
print(hero.level)  # 10
```

#### namedtuple для представления предмета

```python
# Создайте namedtuple для представления игрового предмета
Item = namedtuple('Item', ['name', 'item_type', 'value', 'weight'])

# Создайте экземпляр предмета
sword = Item("Меч героя", "weapon", 100, 5.0)
print(sword.name)  # Меч героя
```

---

## 1. Теоретическая часть: Использование структур данных collections в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.1: Создание namedtuple для различных игровых сущностей

Создайте namedtuple для следующих игровых сущностей:
- `Monster` с полями: name, level, health, attack_power, monster_type
- `Spell` с полями: name, mana_cost, damage, spell_type
- `Location` с полями: name, description, danger_level, required_level

```python
from collections import namedtuple

# ВАШ КОД ЗДЕСЬ - создайте необходимые namedtuple
Monster = ...
Spell = ...
Location = ...

# Пример использования:
# goblin = Monster("Гоблин", 1, 20, 5, "common")
# fireball = Spell("Огненный шар", 10, 15, "fire")
# forest = Location("Темный лес", "Густой лес, полный опасностей", 3, 5)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import namedtuple

Monster = namedtuple('Monster', ['name', 'level', 'health', 'attack_power', 'monster_type'])
Spell = namedtuple('Spell', ['name', 'mana_cost', 'damage', 'spell_type'])
Location = namedtuple('Location', ['name', 'description', 'danger_level', 'required_level'])
```

</details>

#### Задание 1.2: Использование deque для очереди игровых действий

Создайте deque для хранения последних совершенных действий игрока:

```python
from collections import deque

def create_action_queue(max_actions=10):
    """
    Создает очередь для хранения последних действий игрока
    
    Args:
        max_actions (int): Максимальное количество действий в очереди
    
    Returns:
        deque: Очередь действий
    """
    # ВАШ КОД ЗДЕСЬ - создайте и верните deque
    pass  # Замените на ваш код

def add_action(action_queue, action):
    """
    Добавляет действие в очередь
    
    Args:
        action_queue (deque): Очередь действий
        action (str): Действие для добавления
    """
    # ВАШ КОД ЗДЕСЬ - добавьте действие в очередь
    pass  # Замените на ваш код

def get_last_actions(action_queue, count=5):
    """
    Возвращает последние совершенные действия
    
    Args:
        action_queue (deque): Очередь действий
        count (int): Количество действий для возврата
    
    Returns:
        list: Список последних действий
    """
    # ВАШ КОД ЗДЕСЬ - верните последние действия
    pass  # Замените на ваш код

# Пример использования:
# actions = create_action_queue(5)
# add_action(actions, "атаковал гоблина")
# add_action(actions, "использовал зелье")
# recent_actions = get_last_actions(actions)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import deque

def create_action_queue(max_actions=10):
    """
    Создает очередь для хранения последних действий игрока
    
    Args:
        max_actions (int): Максимальное количество действий в очереди
    
    Returns:
        deque: Очередь действий
    """
    return deque(maxlen=max_actions)

def add_action(action_queue, action):
    """
    Добавляет действие в очередь
    
    Args:
        action_queue (deque): Очередь действий
        action (str): Действие для добавления
    """
    action_queue.append(action)

def get_last_actions(action_queue, count=5):
    """
    Возвращает последние совершенные действия
    
    Args:
        action_queue (deque): Очередь действий
        count (int): Количество действий для возврата
    
    Returns:
        list: Список последних действий
    """
    return list(action_queue)[-count:]
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Использование Counter для анализа игровой статистики

Создайте систему анализа использования заклинаний и предметов:

```python
from collections import Counter

class GameStatistics:
    """
    Класс для анализа игровой статистики
    """
    def __init__(self):
        self.spell_usage = Counter()  # Счетчик использования заклинаний
        self.item_usage = Counter()  # Счетчик использования предметов
        self.monster_encounters = Counter()  # Счетчик встреч с монстрами
    
    def record_spell_cast(self, spell_name):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
        """
        # ВАШ КОД ЗДЕСЬ - увеличьте счетчик использования заклинания
        pass  # Замените на ваш код
    
    def record_item_use(self, item_name):
        """
        Записывает использование предмета
        
        Args:
            item_name (str): Название предмета
        """
        # ВАШ КОД ЗДЕСЬ - увеличьте счетчик использования предмета
        pass  # Замените на ваш код
    
    def record_monster_encounter(self, monster_name):
        """
        Записывает встречу с монстром
        
        Args:
            monster_name (str): Название монстра
        """
        # ВАШ КОД ЗДЕСЬ - увеличьте счетчик встреч с монстром
        pass  # Замените на ваш код
    
    def get_top_spells(self, n=5):
        """
        Возвращает топ-N самых используемых заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N заклинаний
        """
        # ВАШ КОД ЗДЕСЬ - верните топ-N заклинаний
        pass  # Замените на ваш код
    
    def get_most_used_items(self, n=5):
        """
        Возвращает топ-N самых используемых предметов
        
        Args:
            n (int): Количество предметов для возврата
        
        Returns:
            list: Список топ-N предметов
        """
        # ВАШ КОД ЗДЕСЬ - верните топ-N предметов
        pass  # Замените на ваш код

# Пример использования:
# stats = GameStatistics()
# stats.record_spell_cast("Огненный шар")
# stats.record_spell_cast("Огненный шар")
# stats.record_spell_cast("Лечение")
# top_spells = stats.get_top_spells(3)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import Counter

class GameStatistics:
    """
    Класс для анализа игровой статистики
    """
    def __init__(self):
        self.spell_usage = Counter()  # Счетчик использования заклинаний
        self.item_usage = Counter()  # Счетчик использования предметов
        self.monster_encounters = Counter()  # Счетчик встреч с монстрами
    
    def record_spell_cast(self, spell_name):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
        """
        self.spell_usage[spell_name] += 1
    
    def record_item_use(self, item_name):
        """
        Записывает использование предмета
        
        Args:
            item_name (str): Название предмета
        """
        self.item_usage[item_name] += 1
    
    def record_monster_encounter(self, monster_name):
        """
        Записывает встречу с монстром
        
        Args:
            monster_name (str): Название монстра
        """
        self.monster_encounters[monster_name] += 1
    
    def get_top_spells(self, n=5):
        """
        Возвращает топ-N самых используемых заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N заклинаний
        """
        return self.spell_usage.most_common(n)
    
    def get_most_used_items(self, n=5):
        """
        Возвращает топ-N самых используемых предметов
        
        Args:
            n (int): Количество предметов для возврата
        
        Returns:
            list: Список топ-N предметов
        """
        return self.item_usage.most_common(n)
```

</details>

#### Задание 2.2: Использование defaultdict для группировки игровых данных

Создайте систему группировки предметов и монстров:

```python
from collections import defaultdict

class GameDataOrganizer:
    """
    Класс для организации игровых данных
    """
    def __init__(self):
        # Группировка предметов по типам
        self.items_by_type = defaultdict(list)
        # Группировка монстров по уровням
        self.monsters_by_level = defaultdict(list)
        # Группировка заклинаний по школам
        self.spells_by_school = defaultdict(list)
    
    def add_item(self, item_name, item_type):
        """
        Добавляет предмет в группировку по типу
        
        Args:
            item_name (str): Название предмета
            item_type (str): Тип предмета
        """
        # ВАШ КОД ЗДЕСЬ - добавьте предмет в соответствующую группу
        pass  # Замените на ваш код
    
    def add_monster(self, monster_name, level):
        """
        Добавляет монстра в группировку по уровню
        
        Args:
            monster_name (str): Название монстра
            level (int): Уровень монстра
        """
        # ВАШ КОД ЗДЕСЬ - добавьте монстра в соответствующую группу
        pass  # Замените на ваш код
    
    def add_spell(self, spell_name, school):
        """
        Добавляет заклинание в группировку по школе
        
        Args:
            spell_name (str): Название заклинания
            school (str): Школа магии
        """
        # ВАШ КОД ЗДЕСЬ - добавьте заклинание в соответствующую группу
        pass  # Замените на ваш код
    
    def get_items_of_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        # ВАШ КОД ЗДЕСЬ - верните предметы заданного типа
        pass  # Замените на ваш код
    
    def get_monsters_of_level(self, level):
        """
        Возвращает всех монстров заданного уровня
        
        Args:
            level (int): Уровень монстров для поиска
        
        Returns:
            list: Список монстров заданного уровня
        """
        # ВАШ КОД ЗДЕСЬ - верните монстров заданного уровня
        pass  # Замените на ваш код

# Пример использования:
# organizer = GameDataOrganizer()
# organizer.add_item("Меч", "weapon")
# organizer.add_item("Щит", "armor")
# weapons = organizer.get_items_of_type("weapon")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import defaultdict

class GameDataOrganizer:
    """
    Класс для организации игровых данных
    """
    def __init__(self):
        # Группировка предметов по типам
        self.items_by_type = defaultdict(list)
        # Группировка монстров по уровням
        self.monsters_by_level = defaultdict(list)
        # Группировка заклинаний по школам
        self.spells_by_school = defaultdict(list)
    
    def add_item(self, item_name, item_type):
        """
        Добавляет предмет в группировку по типу
        
        Args:
            item_name (str): Название предмета
            item_type (str): Тип предмета
        """
        self.items_by_type[item_type].append(item_name)
    
    def add_monster(self, monster_name, level):
        """
        Добавляет монстра в группировку по уровню
        
        Args:
            monster_name (str): Название монстра
            level (int): Уровень монстра
        """
        self.monsters_by_level[level].append(monster_name)
    
    def add_spell(self, spell_name, school):
        """
        Добавляет заклинание в группировку по школе
        
        Args:
            spell_name (str): Название заклинания
            school (str): Школа магии
        """
        self.spells_by_school[school].append(spell_name)
    
    def get_items_of_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        return self.items_by_type[item_type]
    
    def get_monsters_of_level(self, level):
        """
        Возвращает всех монстров заданного уровня
        
        Args:
            level (int): Уровень монстров для поиска
        
        Returns:
            list: Список монстров заданного уровня
        """
        return self.monsters_by_level[level]
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Использование OrderedDict для системы достижений

Создайте систему достижений, которая сохраняет порядок получения:

```python
from collections import OrderedDict

class AchievementSystem:
    """
    Система достижений с сохранением порядка получения
    """
    def __init__(self):
        self.achievements = OrderedDict()  # Словарь достижений с порядком получения
        self.next_id = 1  # Следующий ID для достижения
    
    def add_achievement(self, name, description, points=10):
        """
        Добавляет новое достижение (если его еще нет)
        
        Args:
            name (str): Название достижения
            description (str): Описание достижения
            points (int): Количество очков за достижение
        """
        # ВАШ КОД ЗДЕСЬ - добавьте достижение с уникальным ID
        pass  # Замените на ваш код
    
    def unlock_achievement(self, name, timestamp=None):
        """
        Разблокирует достижение
        
        Args:
            name (str): Название достижения для разблокировки
            timestamp (datetime): Время разблокировки (опционально)
        """
        # ВАШ КОД ЗДЕСЬ - отметьте достижение как разблокированное
        pass  # Замените на ваш код
    
    def get_unlocked_achievements(self):
        """
        Возвращает список разблокированных достижений в порядке получения
        
        Returns:
            list: Список разблокированных достижений
        """
        # ВАШ КОД ЗДЕСЬ - верните разблокированные достижения
        pass  # Замените на ваш код
    
    def get_achievement_progress(self):
        """
        Возвращает прогресс по достижениям (сколько получено, сколько всего)
        
        Returns:
            tuple: (количество разблокированных, общее количество)
        """
        # ВАШ КОД ЗДЕСЬ - верните прогресс по достижениям
        pass  # Замените на ваш код

# Пример использования:
# achievements = AchievementSystem()
# achievements.add_achievement("Первый шаг", "Сделайте первый шаг в мир игры", 5)
# achievements.unlock_achievement("Первый шаг")
# unlocked = achievements.get_unlocked_achievements()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import OrderedDict
import datetime

class AchievementSystem:
    """
    Система достижений с сохранением порядка получения
    """
    def __init__(self):
        self.achievements = OrderedDict()  # Словарь достижений с порядком получения
        self.next_id = 1  # Следующий ID для достижения
    
    def add_achievement(self, name, description, points=10):
        """
        Добавляет новое достижение (если его еще нет)
        
        Args:
            name (str): Название достижения
            description (str): Описание достижения
            points (int): Количество очков за достижение
        """
        if name not in self.achievements:
            achievement_id = self.next_id
            self.next_id += 1
            self.achievements[name] = {
                'id': achievement_id,
                'name': name,
                'description': description,
                'points': points,
                'unlocked': False,
                'timestamp': None
            }
    
    def unlock_achievement(self, name, timestamp=None):
        """
        Разблокирует достижение
        
        Args:
            name (str): Название достижения для разблокировки
            timestamp (datetime): Время разблокировки (опционально)
        """
        if name in self.achievements and not self.achievements[name]['unlocked']:
            self.achievements[name]['unlocked'] = True
            self.achievements[name]['timestamp'] = timestamp or datetime.datetime.now()
    
    def get_unlocked_achievements(self):
        """
        Возвращает список разблокированных достижений в порядке получения
        
        Returns:
            list: Список разблокированных достижений
        """
        return [ach for ach in self.achievements.values() if ach['unlocked']]
    
    def get_achievement_progress(self):
        """
        Возвращает прогресс по достижениям (сколько получено, сколько всего)
        
        Returns:
            tuple: (количество разблокированных, общее количество)
        """
        unlocked_count = sum(1 for ach in self.achievements.values() if ach['unlocked'])
        total_count = len(self.achievements)
        return (unlocked_count, total_count)
```

</details>

#### Задание 3.2: Комплексное использование структур данных

Создайте систему инвентаря, которая использует несколько структур из collections:

```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import datetime

# Определите namedtuple для предмета инвентаря
InventoryItem = namedtuple('InventoryItem', ['name', 'item_type', 'quantity', 'added_date'])

class AdvancedInventory:
    """
    Улучшенная система инвентаря с использованием различных структур данных
    """
    def __init__(self, max_size=20):
        self.max_size = max_size
        # Используем OrderedDict для хранения предметов сохранением порядка добавления
        self.items = OrderedDict()
        # Используем Counter для подсчета общего количества каждого типа предметов
        self.item_type_counts = Counter()
        # Используем defaultdict для группировки предметов по типам
        self.items_by_type = defaultdict(list)
        # Используем deque для хранения истории действий с инвентарем
        self.action_history = deque(maxlen=10)
    
    def add_item(self, name, item_type, quantity=1):
        """
        Добавляет предмет в инвентарь
        
        Args:
            name (str): Название предмета
            item_type (str): Тип предмета
            quantity (int): Количество предметов
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте добавление предмета
        pass  # Замените на ваш код
    
    def remove_item(self, name, quantity=1):
        """
        Удаляет предмет из инвентаря
        
        Args:
            name (str): Название предмета
            quantity (int): Количество предметов для удаления
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте удаление предмета
        pass  # Замените на ваш код
    
    def get_items_by_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        # ВАШ КОД ЗДЕСЬ - верните предметы заданного типа
        pass  # Замените на ваш код
    
    def get_most_common_types(self, n=3):
        """
        Возвращает n самых распространенных типов предметов
        
        Args:
            n (int): Количество типов для возврата
        
        Returns:
            list: Список самых распространенных типов
        """
        # ВАШ КОД ЗДЕСЬ - верните наиболее распространенные типы
        pass  # Замените на ваш код
    
    def get_inventory_size(self):
        """
        Возвращает текущий размер инвентаря
        
        Returns:
            int: Количество уникальных предметов в инвентаре
        """
        # ВАШ КОД ЗДЕСЬ - верните размер инвентаря
        pass  # Замените на ваш код

# Пример использования:
# inventory = AdvancedInventory()
# inventory.add_item("Зелье здоровья", "consumable", 5)
# inventory.add_item("Меч", "weapon", 1)
# consumables = inventory.get_items_by_type("consumable")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import datetime

# Определите namedtuple для предмета инвентаря
InventoryItem = namedtuple('InventoryItem', ['name', 'item_type', 'quantity', 'added_date'])

class AdvancedInventory:
    """
    Улучшенная система инвентаря с использованием различных структур данных
    """
    def __init__(self, max_size=20):
        self.max_size = max_size
        # Используем OrderedDict для хранения предметов с сохранением порядка добавления
        self.items = OrderedDict()
        # Используем Counter для подсчета общего количества каждого типа предметов
        self.item_type_counts = Counter()
        # Используем defaultdict для группировки предметов по типам
        self.items_by_type = defaultdict(list)
        # Используем deque для хранения истории действий с инвентарем
        self.action_history = deque(maxlen=10)
    
    def add_item(self, name, item_type, quantity=1):
        """
        Добавляет предмет в инвентарь
        
        Args:
            name (str): Название предмета
            item_type (str): Тип предмета
            quantity (int): Количество предметов
        """
        if name in self.items:
            # Предмет уже есть в инвентаре, увеличиваем количество
            current_item = self.items[name]
            new_quantity = current_item.quantity + quantity
            self.items[name] = InventoryItem(name, item_type, new_quantity, current_item.added_date)
        else:
            # Новый предмет
            if len(self.items) >= self.max_size:
                # Удаляем самый старый предмет, если инвентарь полон
                oldest_key = next(iter(self.items))
                del self.items[oldest_key]
            
            new_item = InventoryItem(name, item_type, quantity, datetime.datetime.now())
            self.items[name] = new_item
        
        # Обновляем счетчики
        self.item_type_counts[item_type] += quantity
        if name not in self.items_by_type[item_type]:
            self.items_by_type[item_type].append(name)
        
        # Добавляем действие в историю
        self.action_history.append(f"Добавлено {quantity}x {name}")
    
    def remove_item(self, name, quantity=1):
        """
        Удаляет предмет из инвентаря
        
        Args:
            name (str): Название предмета
            quantity (int): Количество предметов для удаления
        """
        if name not in self.items:
            return False
        
        current_item = self.items[name]
        new_quantity = current_item.quantity - quantity
        
        if new_quantity <= 0:
            # Удаляем предмет полностью
            item_type = current_item.item_type
            del self.items[name]
            self.item_type_counts[item_type] -= current_item.quantity
            if self.item_type_counts[item_type] <= 0:
                del self.item_type_counts[item_type]
            if name in self.items_by_type[item_type]:
                self.items_by_type[item_type].remove(name)
        else:
            # Обновляем количество
            self.items[name] = InventoryItem(name, current_item.item_type, new_quantity, current_item.added_date)
            self.item_type_counts[current_item.item_type] -= quantity
        
        # Добавляем действие в историю
        self.action_history.append(f"Удалено {quantity}x {name}")
        return True
    
    def get_items_by_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        result = []
        for item_name in self.items_by_type[item_type]:
            if item_name in self.items:
                result.append(self.items[item_name])
        return result
    
    def get_most_common_types(self, n=3):
        """
        Возвращает n самых распространенных типов предметов
        
        Args:
            n (int): Количество типов для возврата
        
        Returns:
            list: Список самых распространенных типов
        """
        return [item_type for item_type, count in self.item_type_counts.most_common(n)]
    
    def get_inventory_size(self):
        """
        Возвращает текущий размер инвентаря
        
        Returns:
            int: Количество уникальных предметов в инвентаре
        """
        return len(self.items)
```

</details>

---

## 2. Практические задания в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.3: Использование Counter для анализа битв

Создайте систему анализа битв, которая отслеживает количество побед над разными типами монстров:

```python
from collections import Counter

def create_battle_analyzer():
    """
    Создает анализатор битв
    
    Returns:
        Counter: Счетчик побед над монстрами
    """
    # ВАШ КОД ЗДЕСЬ - создайте и верните Counter
    pass  # Замените на ваш код

def record_victory(analyzer, monster_type):
    """
    Записывает победу над монстром
    
    Args:
        analyzer (Counter): Анализатор битв
        monster_type (str): Тип побежденного монстра
    """
    # ВАШ КОД ЗДЕСЬ - увеличьте счетчик побед для типа монстра
    pass  # Замените на ваш код

def get_victory_statistics(analyzer):
    """
    Возвращает статистику побед
    
    Args:
        analyzer (Counter): Анализатор битв
    
    Returns:
        dict: Статистика побед
    """
    # ВАШ КОД ЗДЕСЬ - верните статистику побед
    pass  # Замените на ваш код

# Пример использования:
# battle_stats = create_battle_analyzer()
# record_victory(battle_stats, "гоблин")
# record_victory(battle_stats, "орк")
# record_victory(battle_stats, "гоблин")
# stats = get_victory_statistics(battle_stats)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import Counter

def create_battle_analyzer():
    """
    Создает анализатор битв
    
    Returns:
        Counter: Счетчик побед над монстрами
    """
    return Counter()

def record_victory(analyzer, monster_type):
    """
    Записывает победу над монстром
    
    Args:
        analyzer (Counter): Анализатор битв
        monster_type (str): Тип побежденного монстра
    """
    analyzer[monster_type] += 1

def get_victory_statistics(analyzer):
    """
    Возвращает статистику побед
    
    Args:
        analyzer (Counter): Анализатор битв
    
    Returns:
        dict: Статистика побед
    """
    total_victories = sum(analyzer.values())
    return {
        'total_victories': total_victories,
        'victories_by_type': dict(analyzer),
        'most_defeated': analyzer.most_common(1)[0] if analyzer else None
    }
```

</details>

#### Задание 1.4: Использование deque для системы чата

Создайте систему хранения сообщений в игровом чате:

```python
from collections import deque

def create_chat_system(max_messages=50):
    """
    Создает систему чата
    
    Args:
        max_messages (int): Максимальное количество сообщений в истории
    
    Returns:
        deque: Очередь сообщений чата
    """
    # ВАШ КОД ЗДЕСЬ - создайте и верните deque
    pass  # Замените на ваш код

def send_message(chat, player_name, message):
    """
    Отправляет сообщение в чат
    
    Args:
        chat (deque): Система чата
        player_name (str): Имя игрока
        message (str): Сообщение
    """
    # ВАШ КОД ЗДЕСЬ - добавьте сообщение в чат
    pass  # Замените на ваш код

def get_recent_messages(chat, count=10):
    """
    Возвращает последние сообщения
    
    Args:
        chat (deque): Система чата
        count (int): Количество сообщений для возврата
    
    Returns:
        list: Список последних сообщений
    """
    # ВАШ КОД ЗДЕСЬ - верните последние сообщения
    pass  # Замените на ваш код

# Пример использования:
# chat = create_chat_system(20)
# send_message(chat, "Игрок1", "Привет всем!")
# send_message(chat, "Игрок2", "Привет!")
# recent_msgs = get_recent_messages(chat, 5)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import deque
import datetime

def create_chat_system(max_messages=50):
    """
    Создает систему чата
    
    Args:
        max_messages (int): Максимальное количество сообщений в истории
    
    Returns:
        deque: Очередь сообщений чата
    """
    return deque(maxlen=max_messages)

def send_message(chat, player_name, message):
    """
    Отправляет сообщение в чат
    
    Args:
        chat (deque): Система чата
        player_name (str): Имя игрока
        message (str): Сообщение
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    chat.append(f"[{timestamp}] {player_name}: {message}")

def get_recent_messages(chat, count=10):
    """
    Возвращает последние сообщения
    
    Args:
        chat (deque): Система чата
        count (int): Количество сообщений для возврата
    
    Returns:
        list: Список последних сообщений
    """
    return list(chat)[-count:]
```

</details>

### Уровень 2 - Средний

#### Задание 2.3: Использование defaultdict для системы крафта

Создайте систему крафта, которая группирует рецепты по категориям:

```python
from collections import defaultdict

class CraftingSystem:
    """
    Система крафта с группировкой рецептов
    """
    def __init__(self):
        # Группировка рецептов по категориям
        self.recipes_by_category = defaultdict(list)
        # Хранение всех рецептов
        self.all_recipes = {}
    
    def add_recipe(self, name, category, ingredients, result):
        """
        Добавляет рецепт в систему
        
        Args:
            name (str): Название рецепта
            category (str): Категория рецепта
            ingredients (dict): Ингредиенты {название: количество}
            result (str): Результат крафта
        """
        # ВАШ КОД ЗДЕСЬ - добавьте рецепт в систему
        pass  # Замените на ваш код
    
    def get_recipes_by_category(self, category):
        """
        Возвращает все рецепты в заданной категории
        
        Args:
            category (str): Категория рецептов
        
        Returns:
            list: Список рецептов в категории
        """
        # ВАШ КОД ЗДЕСЯ - верните рецепты в категории
        pass # Замените на ваш код
    
    def can_craft(self, recipe_name, inventory):
        """
        Проверяет, можно ли создать предмет по рецепту
        
        Args:
            recipe_name (str): Название рецепта
            inventory (dict): Инвентарь игрока {предмет: количество}
        
        Returns:
            bool: Можно ли создать предмет
        """
        # ВАШ КОД ЗДЕСЬ - проверьте, можно ли создать предмет
        pass  # Замените на ваш код

# Пример использования:
# crafting = CraftingSystem()
# crafting.add_recipe("Деревянный меч", "оружие", {"дерево": 3}, "меч")
# weapons = crafting.get_recipes_by_category("оружие")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import defaultdict

class CraftingSystem:
    """
    Система крафта с группировкой рецептов
    """
    def __init__(self):
        # Группировка рецептов по категориям
        self.recipes_by_category = defaultdict(list)
        # Хранение всех рецептов
        self.all_recipes = {}
    
    def add_recipe(self, name, category, ingredients, result):
        """
        Добавляет рецепт в систему
        
        Args:
            name (str): Название рецепта
            category (str): Категория рецепта
            ingredients (dict): Ингредиенты {название: количество}
            result (str): Результат крафта
        """
        recipe = {
            'name': name,
            'category': category,
            'ingredients': ingredients,
            'result': result
        }
        self.recipes_by_category[category].append(recipe)
        self.all_recipes[name] = recipe
    
    def get_recipes_by_category(self, category):
        """
        Возвращает все рецепты в заданной категории
        
        Args:
            category (str): Категория рецептов
        
        Returns:
            list: Список рецептов в категории
        """
        return self.recipes_by_category[category]
    
    def can_craft(self, recipe_name, inventory):
        """
        Проверяет, можно ли создать предмет по рецепту
        
        Args:
            recipe_name (str): Название рецепта
            inventory (dict): Инвентарь игрока {предмет: количество}
        
        Returns:
            bool: Можно ли создать предмет
        """
        if recipe_name not in self.all_recipes:
            return False
        
        recipe = self.all_recipes[recipe_name]
        ingredients = recipe['ingredients']
        
        for ingredient, required_amount in ingredients.items():
            if inventory.get(ingredient, 0) < required_amount:
                return False
        
        return True
```

</details>

#### Задание 2.4: Использование Counter для анализа эффективности заклинаний

Создайте систему анализа эффективности заклинаний:

```python
from collections import Counter

class SpellEffectivenessAnalyzer:
    """
    Анализатор эффективности заклинаний
    """
    def __init__(self):
        # Счетчик успешных использований заклинаний
        self.successful_casts = Counter()
        # Счетчик неудачных использований заклинаний
        self.failed_casts = Counter()
        # Общее количество использований
        self.total_casts = Counter()
    
    def record_cast(self, spell_name, success=True):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
            success (bool): Успешно ли было использование
        """
        # ВАШ КОД ЗДЕСЬ - запишите использование заклинания
        pass  # Замените на ваш код
    
    def get_effectiveness(self, spell_name):
        """
        Возвращает эффективность заклинания (в процентах)
        
        Args:
            spell_name (str): Название заклинания
        
        Returns:
            float: Эффективность в процентах
        """
        # ВАШ КОД ЗДЕСЬ - вычислите и верните эффективность
        pass  # Замените на ваш код
    
    def get_top_effective_spells(self, n=5):
        """
        Возвращает топ-N самых эффективных заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N эффективных заклинаний
        """
        # ВАШ КОД ЗДЕСЬ - верните топ-N эффективных заклинаний
        pass  # Замените на ваш код

# Пример использования:
# analyzer = SpellEffectivenessAnalyzer()
# analyzer.record_cast("Огненный шар", True)
# analyzer.record_cast("Огненный шар", False)
# effectiveness = analyzer.get_effectiveness("Огненный шар")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import Counter

class SpellEffectivenessAnalyzer:
    """
    Анализатор эффективности заклинаний
    """
    def __init__(self):
        # Счетчик успешных использований заклинаний
        self.successful_casts = Counter()
        # Счетчик неудачных использований заклинаний
        self.failed_casts = Counter()
        # Общее количество использований
        self.total_casts = Counter()
    
    def record_cast(self, spell_name, success=True):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
            success (bool): Успешно ли было использование
        """
        self.total_casts[spell_name] += 1
        if success:
            self.successful_casts[spell_name] += 1
        else:
            self.failed_casts[spell_name] += 1
    
    def get_effectiveness(self, spell_name):
        """
        Возвращает эффективность заклинания (в процентах)
        
        Args:
            spell_name (str): Название заклинания
        
        Returns:
            float: Эффективность в процентах
        """
        total = self.total_casts[spell_name]
        if total == 0:
            return 0.0
        successful = self.successful_casts[spell_name]
        return (successful / total) * 100
    
    def get_top_effective_spells(self, n=5):
        """
        Возвращает топ-N самых эффективных заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N эффективных заклинаний
        """
        effectiveness_list = []
        for spell in self.total_casts:
            eff = self.get_effectiveness(spell)
            uses = self.total_casts[spell]
            # Учитываем только заклинания, которые использовались хотя бы 3 раза
            if uses >= 3:
                effectiveness_list.append((spell, eff, uses))
        
        # Сортируем по эффективности (в убывающем порядке)
        effectiveness_list.sort(key=lambda x: x[1], reverse=True)
        return effectiveness_list[:n]
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.3: Система рангов игроков с использованием OrderedDict

Создайте систему отслеживания рангов игроков, которая сохраняет порядок достижения рангов:

```python
from collections import OrderedDict

class RankingSystem:
    """
    Система рангов игроков с сохранением порядка
    """
    def __init__(self):
        # Хранит игроков в порядке их достижения ранга
        self.player_rankings = OrderedDict()
        self.next_rank = 1
    
    def add_player(self, player_name, score):
        """
        Добавляет игрока в систему рангов
        
        Args:
            player_name (str): Имя игрока
            score (int): Очки игрока
        """
        # ВАШ КОД ЗДЕСЬ - добавьте игрока в систему
        pass  # Замените на ваш код
    
    def update_score(self, player_name, new_score):
        """
        Обновляет счет игрока и пересчитывает рейтинги
        
        Args:
            player_name (str): Имя игрока
            new_score (int): Новый счет
        """
        # ВАШ КОД ЗДЕСЬ - обновите счет и пересчитайте рейтинги
        pass  # Замените на ваш код
    
    def get_leaderboard(self, top_n=10):
        """
        Возвращает таблицу лидеров
        
        Args:
            top_n (int): Количество игроков для возврата
        
        Returns:
            list: Таблица лидеров
        """
        # ВАШ КОД ЗДЕСЬ - верните таблицу лидеров
        pass  # Замените на ваш код
    
    def get_player_rank(self, player_name):
        """
        Возвращает ранг игрока
        
        Args:
            player_name (str): Имя игрока
        
        Returns:
            int: Ранг игрока (1 - лучший)
        """
        # ВАШ КОД ЗДЕСЬ - верните ранг игрока
        pass  # Замените на ваш код

# Пример использования:
# ranking = RankingSystem()
# ranking.add_player("Игрок1", 1500)
# ranking.add_player("Игрок2", 2000)
# leaderboard = ranking.get_leaderboard(5)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import OrderedDict

class RankingSystem:
    """
    Система рангов игроков с сохранением порядка
    """
    def __init__(self):
        # Хранит игроков в порядке их достижения ранга
        self.player_rankings = OrderedDict()
        self.next_rank = 1
    
    def add_player(self, player_name, score):
        """
        Добавляет игрока в систему рангов
        
        Args:
            player_name (str): Имя игрока
            score (int): Очки игрока
        """
        self.player_rankings[player_name] = score
        # Пересчитываем рейтинги
        self._recalculate_rankings()
    
    def update_score(self, player_name, new_score):
        """
        Обновляет счет игрока и пересчитывает рейтинги
        
        Args:
            player_name (str): Имя игрока
            new_score (int): Новый счет
        """
        if player_name in self.player_rankings:
            self.player_rankings[player_name] = new_score
            # Пересчитываем рейтинги
            self._recalculate_rankings()
    
    def _recalculate_rankings(self):
        """
        Пересчитывает рейтинги на основе очков
        """
        # Сортируем игроков по очкам в убывающем порядке
        sorted_players = sorted(self.player_rankings.items(), key=lambda x: x[1], reverse=True)
        # Обновляем OrderedDict с правильным порядком
        self.player_rankings = OrderedDict(sorted_players)
    
    def get_leaderboard(self, top_n=10):
        """
        Возвращает таблицу лидеров
        
        Args:
            top_n (int): Количество игроков для возврата
        
        Returns:
            list: Таблица лидеров
        """
        leaderboard = []
        rank = 1
        for player_name, score in self.player_rankings.items():
            if rank > top_n:
                break
            leaderboard.append((rank, player_name, score))
            rank += 1
        return leaderboard
    
    def get_player_rank(self, player_name):
        """
        Возвращает ранг игрока
        
        Args:
            player_name (str): Имя игрока
        
        Returns:
            int: Ранг игрока (1 - лучший)
        """
        if player_name not in self.player_rankings:
            return -1  # Игрок не найден
        
        rank = 1
        for name in self.player_rankings.keys():
            if name == player_name:
                return rank
            rank += 1
        return -1  # Игрок не найден
```

</details>

#### Задание 3.4: Комплексная игровая статистика

Создайте комплексную систему игровой статистики, объединяющую все структуры из collections:

```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import datetime

# Определите namedtuple для игрового события
GameEvent = namedtuple('GameEvent', ['timestamp', 'event_type', 'player', 'details'])

class ComprehensiveGameStats:
    """
    Комплексная система игровой статистики
    """
    def __init__(self):
        # Хранение всех событий с сохранением порядка
        self.events = deque(maxlen=1000)
        # Счетчик типов событий
        self.event_counts = Counter()
        # Группировка событий по игрокам
        self.events_by_player = defaultdict(list)
        # Статистика по типам событий
        self.stats_by_event_type = defaultdict(Counter)
        # Хронология событий конкретного игрока
        self.player_timeline = OrderedDict()
    
    def log_event(self, event_type, player, details=""):
        """
        Логирует игровое событие
        
        Args:
            event_type (str): Тип события
            player (str): Имя игрока
            details (str): Детали события
        """
        # ВАШ КОД ЗДЕСЬ - добавьте событие в систему
        pass  # Замените на ваш код
    
    def get_player_stats(self, player):
        """
        Возвращает статистику по игроку
        
        Args:
            player (str): Имя игрока
        
        Returns:
            dict: Статистика игрока
        """
        # ВАШ КОД ЗДЕСЬ - верните статистику по игроку
        pass  # Замените на ваш код
    
    def get_top_players_by_activity(self, n=5):
        """
        Возвращает топ-N самых активных игроков
        
        Args:
            n (int): Количество игроков для возврата
        
        Returns:
            list: Список самых активных игроков
        """
        # ВАШ КОД ЗДЕСЬ - верните топ-N активных игроков
        pass  # Замените на ваш код
    
    def get_recent_events(self, n=10):
        """
        Возвращает последние n событий
        
        Args:
            n (int): Количество событий для возврата
        
        Returns:
            list: Список последних событий
        """
        # ВАШ КОД ЗДЕСЬ - верните последние события
        pass # Замените на ваш код

# Пример использования:
# stats = ComprehensiveGameStats()
# stats.log_event("battle_won", "Игрок1", "Победа над драконом")
# stats.log_event("item_found", "Игрок1", "Меч легенд")
# player_stats = stats.get_player_stats("Игрок1")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import datetime

# Определите namedtuple для игрового события
GameEvent = namedtuple('GameEvent', ['timestamp', 'event_type', 'player', 'details'])

class ComprehensiveGameStats:
    """
    Комплексная система игровой статистики
    """
    def __init__(self):
        # Хранение всех событий с сохранением порядка
        self.events = deque(maxlen=1000)
        # Счетчик типов событий
        self.event_counts = Counter()
        # Группировка событий по игрокам
        self.events_by_player = defaultdict(list)
        # Статистика по типам событий
        self.stats_by_event_type = defaultdict(Counter)
        # Хронология событий конкретного игрока
        self.player_timeline = OrderedDict()
    
    def log_event(self, event_type, player, details=""):
        """
        Логирует игровое событие
        
        Args:
            event_type (str): Тип события
            player (str): Имя игрока
            details (str): Детали события
        """
        event = GameEvent(datetime.datetime.now(), event_type, player, details)
        self.events.append(event)
        self.event_counts[event_type] += 1
        self.events_by_player[player].append(event)
        
        # Обновляем статистику по типам событий для игрока
        self.stats_by_event_type[event_type][player] += 1
        
        # Обновляем временную шкалу игрока
        if player not in self.player_timeline:
            self.player_timeline[player] = OrderedDict()
        self.player_timeline[player][event.timestamp] = event
    
    def get_player_stats(self, player):
        """
        Возвращает статистику по игроку
        
        Args:
            player (str): Имя игрока
        
        Returns:
            dict: Статистика игрока
        """
        if player not in self.events_by_player:
            return {}
        
        player_events = self.events_by_player[player]
        event_types = Counter([event.event_type for event in player_events])
        
        return {
            'total_events': len(player_events),
            'event_types': dict(event_types),
            'first_event': min(player_events, key=lambda x: x.timestamp).timestamp if player_events else None,
            'last_event': max(player_events, key=lambda x: x.timestamp).timestamp if player_events else None
        }
    
    def get_top_players_by_activity(self, n=5):
        """
        Возвращает топ-N самых активных игроков
        
        Args:
            n (int): Количество игроков для возврата
        
        Returns:
            list: Список самых активных игроков
        """
        player_activity = Counter({player: len(events) for player, events in self.events_by_player.items()})
        return player_activity.most_common(n)
    
    def get_recent_events(self, n=10):
        """
        Возвращает последние n событий
        
        Args:
            n (int): Количество событий для возврата
        
        Returns:
            list: Список последних событий
        """
        return list(self.events)[-n:]
```

</details>

---

## 3. Дополнительные задания

### Задание 4: Игровой журнал событий

Реализуйте систему ведения журнала событий с возможностью фильтрации:
1. Создайте систему, которая хранит события с метками времени
2. Реализуйте фильтрацию по типу события, игроку и временному периоду
3. Добавьте экспорт журнала в различные форматы

### Задание 5: Система рекомендаций

Разработайте систему рекомендаций для игроков:
1. Создайте анализатор поведения игрока с использованием Counter
2. Реализуйте рекомендации на основе предпочтений игрока
3. Используйте OrderedDict для сохранения истории рекомендаций

---

## Контрольные вопросы:
1. В чем преимущества использования namedtuple по сравнению с обычными классами?
2. Какие особенности имеет deque по сравнению с обычным списком?
3. Как работает Counter и в каких случаях его лучше использовать?
4. Чем defaultdict отличается от обычного словаря?
5. Какие преимущества дает OrderedDict по сравнению с обычным dict?