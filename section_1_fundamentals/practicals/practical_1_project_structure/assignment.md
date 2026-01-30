# Практическое занятие 1: Создание структуры проекта игры "Сказочный Квест"

## Цель занятия
Научиться создавать правильную структуру проекта Python-приложения на примере разработки текстовой RPG игры, использовать виртуальное окружение и управлять зависимостями проекта.

## Задачи
1. Создать структуру проекта для текстовой RPG игры "Сказочный Квест"
2. Настроить виртуальное окружение
3. Создать и заполнить файл requirements.txt
4. Написать базовую документацию для проекта

## Ход работы

### 1. Создание структуры проекта игры

Создайте следующую структуру директорий и файлов:

```
fantasy_quest/
├── src/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── config.py
│   ├── characters/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   └── npc.py
│   ├── locations/
│   │   ├── __init__.py
│   │   └── world_map.py
│   ├── items/
│   │   ├── __init__.py
│   │   └── inventory.py
│   └── quests/
│       ├── __init__.py
│       └── quest_system.py
├── tests/
│   ├── __init__.py
│   ├── test_characters.py
│   ├── test_locations.py
│   └── test_items.py
├── docs/
│   └── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── README.md
└── LICENSE
```

### 2. Настройка виртуального окружения

1. Создайте виртуальное окружение с именем `venv`:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
   - В Windows:
   ```bash
   venv\Scripts\activate
   ```
   - В Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. Убедитесь, что виртуальное окружение активировано (в командной строке должно появиться `(venv)`)

### 3. Создание requirements.txt

Создайте файл `requirements.txt` и добавьте следующие зависимости:

```
# Основные зависимости
requests==2.28.1
click>=8.0.0

# Зависимости для тестирования
pytest>=7.0.0
pytest-mock>=3.6.1

# Зависимости для разработки
black>=22.0.0
flake8>=4.0.0
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

---

## 1. Теоретическая часть: Создание игрового мира

### Уровень 1 - Начальный

#### Задание 1.1: Создание основного модуля игры

Создайте файл `src/game_engine.py` с основной логикой игры:

```python
"""
Основной модуль игры "Сказочный Квест".
"""

from src.config import GAME_TITLE, VERSION
from src.characters.player import Hero


def main():
    """
    Основная функция приложения игры.
    """
    print(f"{GAME_TITLE} версии {VERSION}")
    
    # Запрашиваем имя игрока
    name = input("Введите имя вашего героя: ")
    hero = Hero(name)
    
    print(f"Добро пожаловать в мир Сказочного Квеста, {hero.name}!")
    
    # Отображаем начальные параметры героя
    print(hero.get_stats())


if __name__ == "__main__":
    main()
```

#### Задание 1.2: Создание конфигурации игры

Создайте файл `src/config.py` с настройками игры:

```python
"""
Конфигурационный файл игры.
"""

GAME_TITLE = "Сказочный Квест"
VERSION = "1.0.0"
DEBUG = True

# Игровые параметры
MAX_HEALTH = 10
STARTING_GOLD = 50
DEFAULT_ATTACK = 10
```

### Уровень 2 - Средний

#### Задание 2.1: Создание системы персонажей

Создайте файл `src/characters/player.py`:

```python
"""
Модуль для работы с персонажем игрока.
"""

from src.config import MAX_HEALTH, DEFAULT_ATTACK, STARTING_GOLD
from src.items.inventory import Inventory


class Hero:
    """
    Класс для представления героя игрока.
    """
    def __init__(self, name):
        self.name = name
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.attack = DEFAULT_ATTACK
        self.gold = STARTING_GOLD
        self.level = 1
        self.xp = 0
        self.xp_to_level = 100
        self.inventory = Inventory()
        
    def get_stats(self):
        """
        Возвращает строку с характеристиками героя.
        """
        return f"""
Имя: {self.name}
Уровень: {self.level}
Здоровье: {self.health}/{self.max_health}
Атака: {self.attack}
Золото: {self.gold}
Опыт: {self.xp}/{self.xp_to_level}
        """.strip()

    def is_alive(self):
        """
        Проверяет, жив ли герой.
        """
        return self.health > 0
        
    def take_damage(self, damage):
        """
        Герой получает урон.
        """
        self.health = max(0, self.health - damage)
        return damage

    def heal(self, amount):
        """
        Герой восстанавливает здоровье.
        """
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health
```

Создайте файл `src/characters/npc.py`:

```python
"""
Модуль для работы с NPC (неигровыми персонажами).
"""

class NPC:
    """
    Класс для представления неигрового персонажа.
    """
    def __init__(self, name, role="unknown"):
        self.name = name
        self.role = role
        self.dialogues = []
        
    def add_dialogue(self, dialogue):
        """
        Добавляет диалог к NPC.
        """
        self.dialogues.append(dialogue)
        
    def speak(self):
        """
        NPC говорит первый доступный диалог.
        """
        if self.dialogues:
            return self.dialogues[0]
        return f"{self.name} молчит."
```

### Уровень 3 - Повышенный

#### Задание 3.1: Создание системы предметов инвентаря

Создайте файл `src/items/inventory.py`:

```python
"""
Модуль для работы с инвентарем игрока.
"""

class Item:
    """
    Базовый класс для игрового предмета.
    """
    def __init__(self, name, item_type, value=0):
        self.name = name
        self.item_type = item_type
        self.value = value

    def use(self, target):
        """
        Использование предмета на цели.
        """
        return f"Вы использовали {self.name}."


class Inventory:
    """
    Класс инвентаря игрока.
    """
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def add_item(self, item):
        """
        Добавляет предмет в инвентарь.
        """
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_name):
        """
        Удаляет предмет из инвентаря по имени.
        """
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def get_items_by_type(self, item_type):
        """
        Возвращает список предметов указанного типа.
        """
        return [item for item in self.items if item.item_type == item_type]
        
    def get_total_value(self):
        """
        Возвращает общую стоимость всех предметов в инвентаре.
        """
        return sum(item.value for item in self.items)
```

Создайте файл `src/locations/world_map.py`:

```python
"""
Модуль для работы с игровой картой.
"""

class Location:
    """
    Класс для представления игровой локации.
    """
    def __init__(self, name, description, dangerous=False):
        self.name = name
        self.description = description
        self.dangerous = dangerous
        self.npcs = []
        self.items = []
        self.connections = []  # Список связанных локаций

    def add_npc(self, npc):
        """
        Добавляет NPC в локацию.
        """
        self.npcs.append(npc)

    def add_connection(self, location):
        """
        Добавляет связь с другой локацией.
        """
        if location not in self.connections:
            self.connections.append(location)

    def describe(self):
        """
        Описывает локацию.
        """
        danger_text = " (ОПАСНО)" if self.dangerous else ""
        return f"{self.name}{danger_text}\n{self.description}"


class WorldMap:
    """
    Класс для представления всей игровой карты.
    """
    def __init__(self):
        self.locations = {}
        self.start_location = None

    def add_location(self, location):
        """
        Добавляет локацию на карту.
        """
        self.locations[location.name] = location
        if self.start_location is None:
            self.start_location = location

    def get_location(self, name):
        """
        Возвращает локацию по имени.
        """
        return self.locations.get(name)
```

---

## 2. Практические задания в игровом контексте

### Уровень 1 - Начальный

#### Задание 1.3: Создание простого героя

Создайте класс `SimpleHero` в файле `src/characters/player.py` (в дополнение к уже созданному Hero) с минимальным функционалом:

```python
class SimpleHero:
    def __init__(self, name):
        # ВАШ КОД ЗДЕСЬ - добавьте базовые атрибуты героя
        pass  # Замените на ваш код

    def introduce(self):
        # ВАШ КОД ЗДЕСЬ - метод представления героя
        pass  # Замените на ваш код

# Пример использования (после реализации)
# hero = SimpleHero("Иван")
# print(hero.introduce())  # Должно вывести: "Привет, я Иван!"
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class SimpleHero:
    def __init__(self, name):
        self.name = name
        self.health = 100

    def introduce(self):
        return f"Привет, я {self.name}!"
```

</details>

#### Задание 1.4: Создание простого предмета

Создайте класс `SimpleItem` в файле `src/items/inventory.py`:

```python
class SimpleItem:
    def __init__(self, name, description=""):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты предмета
        pass  # Замените на ваш код

    def get_info(self):
        # ВАШ КОД ЗДЕСЬ - метод получения информации о предмете
        pass  # Замените на ваш код

# Пример использования (после реализации)
# sword = SimpleItem("Меч", "Острый меч новобранца")
# print(sword.get_info())  # Должно вывести: "Меч: Острый меч новобранца"
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class SimpleItem:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def get_info(self):
        return f"{self.name}: {self.description}"
```

</details>

### Уровень 2 - Средний

#### Задание 2.2: Улучшенная система инвентаря

Расширьте класс `Inventory` в файле `src/items/inventory.py`, добавив методы для поиска предметов и проверки места:

```python
class Inventory:
    # ... (предыдущий код остается без изменений)
    
    def has_space(self):
        # ВАШ КОД ЗДЕСЬ - проверка наличия свободного места
        pass  # Замените на ваш код

    def find_item(self, name):
        # ВАШ КОД ЗДЕСЬ - поиск предмета по имени
        pass  # Замените на ваш код

    def get_items_count(self):
        # ВАШ КОД ЗДЕСЬ - получение количества предметов
        pass  # Замените на ваш код

    def get_available_space(self):
        # ВАШ КОД ЗДЕСЬ - получение доступного места
        pass  # Замените на ваш код
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Inventory:
    # ... (предыдущий код остается без изменений)
    
    def has_space(self):
        return len(self.items) < self.max_size

    def find_item(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_items_count(self):
        return len(self.items)

    def get_available_space(self):
        return self.max_size - len(self.items)
```

</details>

#### Задание 2.3: Система квестов

Создайте файл `src/quests/quest_system.py`:

```python
"""
Модуль для работы с системой квестов.
"""

class Quest:
    """
    Класс для представления квеста.
    """
    def __init__(self, title, description, reward_xp=10, reward_gold=5):
        self.title = title
        self.description = description
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.completed = False

    def complete(self):
        """
        Помечает квест как выполненный.
        """
        self.completed = True
        return {"xp": self.reward_xp, "gold": self.reward_gold}


class QuestLog:
    """
    Класс для ведения журнала квестов игрока.
    """
    def __init__(self):
        self.quests = []
        self.completed_quests = []

    def add_quest(self, quest):
        # ВАШ КОД ЗДЕСЬ - добавление квеста в журнал
        pass  # Замените на ваш код

    def complete_quest(self, title):
        # ВАШ КОД ЗДЕСЬ - завершение квеста по названию
        pass  # Замените на ваш код

    def get_active_quests(self):
        # ВАШ КОД ЗДЕСЬ - получение списка активных квестов
        pass  # Замените на ваш код
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class QuestLog:
    """
    Класс для ведения журнала квестов игрока.
    """
    def __init__(self):
        self.quests = []
        self.completed_quests = []

    def add_quest(self, quest):
        if quest not in self.quests and not quest.completed:
            self.quests.append(quest)

    def complete_quest(self, title):
        for i, quest in enumerate(self.quests):
            if quest.title.lower() == title.lower():
                completed_quest = self.quests.pop(i)
                reward = completed_quest.complete()
                self.completed_quests.append(completed_quest)
                return reward
        return None

    def get_active_quests(self):
        return [quest for quest in self.quests if not quest.completed]
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.2: Система сохранения игры

Создайте файл `src/save_system.py`:

```python
"""
Модуль для сохранения и загрузки игры.
"""
import json
import os
from datetime import datetime


class SaveSystem:
    """
    Система сохранения и загрузки игры.
    """
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, game_state, filename):
        """
        Сохраняет состояние игры в файл.
        
        Args:
            game_state (dict): Состояние игры для сохранения
            filename (str): Имя файла для сохранения
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте сохранение игры в JSON
        pass  # Замените на ваш код

    def load_game(self, filename):
        """
        Загружает состояние игры из файла.
        
        Args:
            filename (str): Имя файла для загрузки
            
        Returns:
            dict: Состояние игры или None, если файл не найден
        """
        # ВАШ КОД ЗДЕСЯ - реализуйте загрузку игры из JSON
        pass  # Замените на ваш код

    def get_save_list(self):
        """
        Возвращает список доступных сохранений.
        
        Returns:
            list: Список имен файлов сохранений
        """
        # ВАШ КОД ЗДЕСЬ - получите список файлов в директории сохранений
        pass  # Замените на ваш код
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class SaveSystem:
    """
    Система сохранения и загрузки игры.
    """
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, game_state, filename):
        """
        Сохраняет состояние игры в файл.
        
        Args:
            game_state (dict): Состояние игры для сохранения
            filename (str): Имя файла для сохранения
        """
        filepath = os.path.join(self.save_dir, filename)
        game_state['saved_at'] = datetime.now().isoformat()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, ensure_ascii=False, indent=2)
        return filepath

    def load_game(self, filename):
        """
        Загружает состояние игры из файла.
        
        Args:
            filename (str): Имя файла для загрузки
            
        Returns:
            dict: Состояние игры или None, если файл не найден
        """
        filepath = os.path.join(self.save_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_save_list(self):
        """
        Возвращает список доступных сохранений.
        
        Returns:
            list: Список имен файлов сохранений
        """
        saves = []
        for file in os.listdir(self.save_dir):
            if file.endswith('.json'):
                saves.append(file)
        return saves
```

</details>

#### Задание 3.3: Интеграция всех систем

Обновите файл `src/game_engine.py`, чтобы объединить все созданные системы:

```python
"""
Основной модуль игры "Сказочный Квест".
"""

from src.config import GAME_TITLE, VERSION
from src.characters.player import Hero
from src.locations.world_map import WorldMap, Location
from src.quests.quest_system import Quest, QuestLog
from src.save_system import SaveSystem


def main():
    """
    Основная функция приложения игры.
    """
    print(f"{GAME_TITLE} версии {VERSION}")
    
    # Запрашиваем имя игрока
    name = input("Введите имя вашего героя: ")
    hero = Hero(name)
    
    print(f"Добро пожаловать в мир Сказочного Квеста, {hero.name}!")
    
    # Создаем игровой мир
    world = WorldMap()
    village = Location("Деревня", "Маленькая деревня с уютными домиками.")
    forest = Location("Лес", "Густой лес, полный опасностей и сокровищ.", dangerous=True)
    
    world.add_location(village)
    world.add_location(forest)
    village.add_connection(forest)
    forest.add_connection(village)
    
    # Создаем квесты
    quest_log = QuestLog()
    tutorial_quest = Quest("Обучение", "Поговорите с главой деревни", 20, 10)
    quest_log.add_quest(tutorial_quest)
    
    # Отображаем начальные параметры героя
    print(hero.get_stats())
    
    # Показываем доступные квесты
    print("\nВаши квесты:")
    for quest in quest_log.get_active_quests():
        print(f"- {quest.title}: {quest.description}")
    
    # Позволяем игроку выбрать локацию
    print(f"\nВы находитесь в: {world.start_location.name}")
    print(world.start_location.describe())
    
    # Система сохранения
    save_system = SaveSystem()
    
    # Пример сохранения игры
    game_state = {
        "hero": {
            "name": hero.name,
            "level": hero.level,
            "health": hero.health,
            "gold": hero.gold
        },
        "location": world.start_location.name,
        "completed_quests": len(quest_log.completed_quests)
    }
    
    save_filename = f"{hero.name}_save.json"
    save_path = save_system.save_game(game_state, save_filename)
    print(f"\nИгра сохранена в: {save_path}")


if __name__ == "__main__":
    main()
```

---

## 3. Дополнительные задания

### Задание 4: Система боевых действий

Разработайте модуль `src/battle_system.py` с классами для боевой системы:

1. Класс `Battle` для управления боем между персонажами
2. Класс `Combatant` как базовый класс для всех участников боя
3. Механизмы атаки, защиты и использования предметов во время боя

### Задание 5: Система улучшений

Реализуйте систему улучшения характеристик героя:

1. Добавьте систему очков улучшений
2. Реализуйте возможность распределения очков между различными характеристиками
3. Создайте визуальное отображение прогресса героя

---

## Контрольные вопросы:
1. В каких случаях следует использовать виртуальное окружение в Python?
2. Какие файлы обязательно должны быть включены в .gitignore для игрового проекта?
3. Почему важна правильная структура проекта в контексте разработки игр?
4. Какие элементы должны быть включены в README.md игрового проекта?
5. Как обеспечить масштабируемость структуры проекта при добавлении новых игровых механик?