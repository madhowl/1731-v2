# Практическое занятие 16: ООП - паттерн Strategy в игровом контексте

## Создание системы выбора алгоритмов, стратегии и контексты

### Цель занятия:
Научиться создавать систему выбора алгоритмов в Python, определять стратегии и контексты, использовать паттерн Strategy для выбора алгоритмов во время выполнения программы в игровом контексте, а также понять, когда и зачем использовать этот паттерн в игровой разработке.

### Задачи:
1. Создать интерфейсы стратегии и контекста
2. Использовать паттерн Strategy для выбора алгоритмов
3. Реализовать различные типы стратегий: простые, параметризованные, асинхронные
4. Применить принципы ООП и паттерн Strategy на практике в игровом контексте

### План работы:
1. Создание простой системы стратегий для игровых действий
2. Определение интерфейсов стратегии и контекста
3. Использование различных типов стратегий для выбора алгоритмов
4. Применение принципов инкапсуляции и наследования в стратегиях
5. Создание экземпляров классов стратегий и контекстов
6. Практические задания в игровом контексте

---
# Практическое занятие 16: ООП - паттерн Strategy в игровом контексте

## Создание системы выбора алгоритмов, стратегии и контексты

### Цель занятия:
Научиться создавать систему выбора алгоритмов в Python, определять стратегии и контексты, использовать паттерн Strategy для выбора алгоритмов во время выполнения программы в игровом контексте, а также понять, когда и зачем использовать этот паттерн в игровой разработке.

### Задачи:
1. Создать интерфейсы стратегии и контекста
2. Использовать паттерн Strategy для выбора алгоритмов
3. Реализовать различные типы стратегий: простые, параметризованные, асинхронные
4. Применить принципы ООП и паттерн Strategy на практике в игровом контексте

---

## 1. Теоретическая часть

### Основные понятия паттерна Strategy

**Паттерн Strategy (Стратегия)** — это поведенческий паттерн проектирования, который определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми. Паттерн Strategy позволяет изменять алгоритмы независимо от клиентов, которые ими пользуются.

**Стратегия (Strategy)** — это интерфейс, определяющий алгоритм, который может быть использован контекстом.

**Конкретная стратегия (Concrete Strategy)** — это класс, реализующий интерфейс стратегии и содержащий конкретный алгоритм.

**Контекст (Context)** — это класс, использующий стратегию. Он делегирует выполнение алгоритма одной из стратегий.

### Пример простой стратегии (уровень 1 - начальный)

```python
from abc import ABC, abstractmethod

class BattleStrategy(ABC):
    """
    Интерфейс боевой стратегии
    """
    @abstractmethod
    def execute_attack(self, attacker, target, environment=None):
        """
        Выполнить атаку с использованием данной стратегии
        """
        pass

    @abstractmethod
    def execute_defense(self, character, incoming_damage, environment=None):
        """
        Выполнить защиту с использованием данной стратегии
        """
        pass

class Character:
    """
    Класс игрового персонажа как контекст для боевых стратегий
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        self.name = name
        self._health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.character_class = character_class
        self.level = 1
        self.is_alive = True
        self._battle_strategy: BattleStrategy = None  # Текущая боевая стратегия

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = max(0, min(self.max_health, value))
        if self._health <= 0:
            self._health = 0
            self.is_alive = False

    def set_battle_strategy(self, strategy: BattleStrategy):
        """Установить боевую стратегию"""
        self._battle_strategy = strategy

    def perform_attack(self, target, environment=None):
        """Выполнить атаку с использованием текущей стратегии"""
        if self._battle_strategy and self.is_alive and target.is_alive:
            return self._battle_strategy.execute_attack(self, target, environment)
        else:
            return f"{self.name} не может атаковать (мертв или нет цели)"

    def perform_defense(self, incoming_damage, environment=None):
        """Выполнить защиту с использованием текущей стратегии"""
        if self._battle_strategy and self.is_alive:
            return self._battle_strategy.execute_defense(self, incoming_damage, environment)
        else:
            # Если нет стратегии, просто получаем урон
            self.health -= incoming_damage
            return f"{self.name} получает {incoming_damage} урона (без стратегии защиты)"

    def get_info(self):
        """Получить информацию о персонаже"""
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({self.character_class}, {status}): Lvl.{self.level}, HP {self.health}/{self.max_health}, ATK {self.attack_power}, DEF {self.defense}"

    def take_damage(self, damage: int):
        """Получить урон"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage


class AggressiveStrategy(BattleStrategy):
    """
    Агрессивная боевая стратегия - наносит максимальный урон, но плохо защищается
    """
    def execute_attack(self, attacker, target, environment=None):
        # Агрессивная стратегия увеличивает урон на 20%
        enhanced_damage = int(attacker.attack_power * 1.2)
        actual_damage = target.take_damage(enhanced_damage)
        return f"{attacker.name} агрессивно атакует {target.name} на {actual_damage} урона!"

    def execute_defense(self, character, incoming_damage, environment=None):
        # Агрессивная стратегия почти не снижает урон
        actual_damage = max(1, incoming_damage - character.defense * 0.5)  # Только 50% обычной защиты
        character.health -= actual_damage
        return f"{character.name} получает {actual_damage} урона (агрессивная стратегия - минимальная защита)"


class DefensiveStrategy(BattleStrategy):
    """
    Защитная боевая стратегия - фокусируется на защите, наносит меньше урона
    """
    def execute_attack(self, attacker, target, environment=None):
        # Защитная стратегия снижает урон на 20% для акцента на защите
        reduced_damage = int(attacker.attack_power * 0.8)
        actual_damage = target.take_damage(reduced_damage)
        return f"{attacker.name} осторожно атакует {target.name} на {actual_damage} урона!"

    def execute_defense(self, character, incoming_damage, environment=None):
        # Защитная стратегия значительно снижает получаемый урон
        actual_damage = max(1, incoming_damage - character.defense * 1.5)  # 150% обычной защиты
        character.health -= actual_damage
        return f"{character.name} защищается, получает {actual_damage} урона (защитная стратегия)"


class BalancedStrategy(BattleStrategy):
    """
    Сбалансированная боевая стратегия - средний урон и средняя защита
    """
    def execute_attack(self, attacker, target, environment=None):
        # Сбалансированная стратегия использует обычный урон
        actual_damage = target.take_damage(attacker.attack_power)
        return f"{attacker.name} сбалансированно атакует {target.name} на {actual_damage} урона!"

    def execute_defense(self, character, incoming_damage, environment=None):
        # Сбалансированная стратегия использует обычную защиту
        actual_damage = max(1, incoming_damage - character.defense)
        character.health -= actual_damage
        return f"{character.name} защищается стандартно, получает {actual_damage} урона"


# Пример использования
print("=== Демонстрация паттерна Strategy для боевых действий ===\n")

# Создаем персонажей
warrior = Character("Конан", health=120, attack_power=25, defense=8, character_class="warrior")
mage = Character("Мерлин", health=80, attack_power=30, defense=3, character_class="mage")

# Устанавливаем разные стратегии
warrior.set_battle_strategy(AggressiveStrategy())
mage.set_battle_strategy(DefensiveStrategy())

print(f"Персонаж 1: {warrior.get_info()}")
print(f"Стратегия: Агрессивная")
print(f"Персонаж 2: {mage.get_info()}")
print(f"Стратегия: Защитная\n")

# Боевая симуляция
print("1. Агрессивный персонаж атакует защитного:")
result = warrior.perform_attack(mage)
print(f"   {result}")

print(f"\nСостояние после атаки:")
print(f"  {warrior.get_info()}")
print(f"  {mage.get_info()}")

print(f"\n2. Защитный персонаж атакует агрессивного:")
result = mage.perform_attack(warrior)
print(f"   {result}")

print(f"\nСостояние после атаки:")
print(f"  {warrior.get_info()}")
print(f"  {mage.get_info()}")

print(f"\n3. Агрессивный персонаж получает урон (использует агрессивную стратегию защиты):")
result = warrior.perform_defense(20)
print(f"   {result}")

print(f"\nСостояние после получения урона:")
print(f"  {warrior.get_info()}")

print(f"\n4. Защитный персонаж получает урон (использует защитную стратегию):")
result = mage.perform_defense(20)
print(f"   {result}")

print(f"\nФинальное состояние:")
print(f"  {warrior.get_info()}")
print(f"  {mage.get_info()}")
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание простой боевой стратегии

Создайте класс `BalancedStrategy`, который реализует сбалансированную боевую стратегию: наносит средний урон и обеспечивает среднюю защиту. Реализуйте методы `execute_attack` и `execute_defense`.

**Шаги выполнения:**
1. Создайте класс `BalancedStrategy`, наследующийся от `BattleStrategy`
2. Реализуйте метод `execute_attack` для нанесения среднего урона
3. Реализуйте метод `execute_defense` для средней защиты
4. Протестируйте работу стратегии

```python
class BalancedStrategy(BattleStrategy):
    # ВАШ КОД ЗДЕСЬ - реализуйте сбалансированную стратегию
    pass


# Пример использования (после реализации)
# balanced_strategy = BalancedStrategy()
# player = Character("Баланс", health=100, attack_power=20, defense=5)
# enemy = Character("Враг", health=100, attack_power=15, defense=3)
# 
# player.set_battle_strategy(balanced_strategy)
# 
# print(f"Игрок: {player.get_info()}")
# print(f"Враг: {enemy.get_info()}")
# 
# # Выполняем атаку
# result = player.perform_attack(enemy)
# print(f"Результат атаки: {result}")
# 
# # Выполняем защиту
# result = player.perform_defense(25)
# print(f"Результат защиты: {result}")
# 
# print(f"\nПосле действий:")
# print(f"Игрок: {player.get_info()}")
# print(f"Враг: {enemy.get_info()}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class BalancedStrategy(BattleStrategy):
    """
    Сбалансированная боевая стратегия - средний урон и средняя защита
    """
    def execute_attack(self, attacker, target, environment=None):
        # Сбалансированная стратегия использует обычный урон
        actual_damage = target.take_damage(attacker.attack_power)
        return f"{attacker.name} сбалансированно атакует {target.name} на {actual_damage} урона!"

    def execute_defense(self, character, incoming_damage, environment=None):
        # Сбалансированная стратегия использует обычную защиту
        actual_damage = max(1, incoming_damage - character.defense)
        character.health -= actual_damage
        return f"{character.name} защищается стандартно, получает {actual_damage} урона"
```

</details>

#### Задание 1.2: Стратегия лечения

Создайте стратегию `HealingStrategy`, которая в бою позволяет персонажу восстанавливать здоровье вместо атаки. Реализуйте методы `execute_attack` и `execute_defense` для этой стратегии.

```python
class HealingStrategy(BattleStrategy):
    # ВАШ КОД ЗДЕСЬ - реализуйте стратегию лечения
    pass


# Пример использования (после реализации)
# healing_strategy = HealingStrategy()
# healer = Character("Лекарь", health=80, attack_power=10, defense=3)
# enemy = Character("Враг", health=100, attack_power=20, defense=2)
# 
# healer.set_battle_strategy(healing_strategy)
# 
# print(f"Лекарь: {healer.get_info()}")
# print(f"Враг: {enemy.get_info()}")
# 
# # Выполняем "атаку" (на самом деле лечение)
# result = healer.perform_attack(enemy)
# print(f"Результат: {result}")
# 
# print(f"\nПосле действия:")
# print(f"Лекарь: {healer.get_info()}")
# print(f"Враг: {enemy.get_info()}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class HealingStrategy(BattleStrategy):
    """
    Стратегия лечения - персонаж восстанавливает здоровье вместо атаки
    """
    def execute_attack(self, attacker, target, environment=None):
        # При "атаке" лекарь лечит себя или союзника
        heal_amount = min(20, attacker.max_health - attacker.health)
        old_health = attacker.health
        attacker.health += heal_amount
        healed = attacker.health - old_health
        return f"{attacker.name} использует лечение и восстанавливает {healed} здоровья!"

    def execute_defense(self, character, incoming_damage, environment=None):
        # При защите дополнительно восстанавливает немного здоровья
        actual_damage = max(1, incoming_damage - character.defense)
        character.health -= actual_damage
        
        # Восстанавливаем немного здоровья при защите
        if character.health < character.max_health:
            heal_amount = min(5, character.max_health - character.health)
            character.health += heal_amount
            return f"{character.name} защищается и восстанавливает {heal_amount} здоровья, получает {actual_damage} урона"
        else:
            return f"{character.name} защищается, получает {actual_damage} урона"
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Система поведения врагов с использованием стратегий

Реализуйте систему поведения врагов с использованием различных стратегий. Создайте класс `Enemy` как контекст и несколько стратегий поведения: `AggressiveAI`, `DefensiveAI`, `RandomAI`.

**Шаги выполнения:**
1. Создайте абстрактный класс `AIStrategy` с методами `decide_action` и `evaluate_threat`
2. Реализуйте несколько конкретных стратегий ИИ
3. Создайте класс `Enemy` как контекст для стратегий ИИ
4. Протестируйте работу системы

```python
from abc import ABC, abstractmethod
import random

class AIStrategy(ABC):
    """
    Интерфейс стратегии ИИ врага
    """
    @abstractmethod
    def decide_action(self, enemy, player, environment=None):
        """
        Принять решение о действии для врага
        """
        pass

    @abstractmethod
    def evaluate_threat(self, enemy, player, environment=None):
        """
        Оценить угрозу от игрока
        """
        pass


class Enemy(Character):
    """
    Класс врага как контекст для стратегии ИИ
    """
    def __init__(self, name: str, health: int, attack_power: int, defense: int, enemy_type: str = "common"):
        super().__init__(name, health, attack_power, defense, character_class=enemy_type)
        self.enemy_type = enemy_type
        self._ai_strategy: AIStrategy = None

    def set_ai_strategy(self, strategy: AIStrategy):
        """Установить стратегию ИИ"""
        self._ai_strategy = strategy

    def take_turn(self, player, environment=None):
        """Сделать ход в бою"""
        if self._ai_strategy and self.is_alive and player.is_alive:
            return self._ai_strategy.decide_action(self, player, environment)
        elif not self.is_alive:
            return f"{self.name} мертв и не может действовать"
        elif not player.is_alive:
            return f"{player.name} мертв, {self.name} побеждает"
        else:
            return f"{self.name} не может действовать (нет стратегии ИИ)"

    def evaluate_player_threat(self, player, environment=None):
        """Оценить угрозу от игрока с помощью стратегии ИИ"""
        if self._ai_strategy:
            return self._ai_strategy.evaluate_threat(self, player, environment)
        else:
            return "неизвестно"


class AggressiveAI(AIStrategy):
    """
    Агрессивный ИИ - всегда атакует, если может
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте агрессивный ИИ
    pass


class DefensiveAI(AIStrategy):
    """
    Защитный ИИ - фокусируется на выживании
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте защитный ИИ
    pass


class RandomAI(AIStrategy):
    """
    Случайный ИИ - выбирает случайное действие
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте случайный ИИ
    pass


# Пример использования (после реализации)
# player = Character("Герой", health=150, attack_power=25, defense=10, character_class="warrior")
# 
# aggressive_goblin = Enemy("Агрессивный гоблин", health=50, attack_power=15, defense=2, enemy_type="goblin")
# defensive_orc = Enemy("Оборонительный орк", health=80, attack_power=12, defense=8, enemy_type="orc")
# random_skeleton = Enemy("Случайный скелет", health=40, attack_power=10, defense=3, enemy_type="skeleton")
# 
# # Устанавливаем стратегии ИИ
# aggressive_goblin.set_ai_strategy(AggressiveAI())
# defensive_orc.set_ai_strategy(DefensiveAI())
# random_skeleton.set_ai_strategy(RandomAI())
# 
# enemies = [aggressive_goblin, defensive_orc, random_skeleton]
# 
# print("Информация о врагах:")
# for enemy in enemies:
#     print(f"  {enemy.get_info()}")
# 
# print(f"\nОценка угрозы от врагов:")
# for enemy in enemies:
#     threat_eval = enemy.evaluate_player_threat(player)
#     print(f"  {threat_eval}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class AggressiveAI(AIStrategy):
    """
    Агрессивный ИИ - всегда атакует, если может
    """
    def decide_action(self, enemy, player, environment=None):
        if player.is_alive:
            # Используем боевую стратегию для атаки
            if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                # Если у врага нет боевой стратегии, устанавливаем агрессивную
                enemy.set_battle_strategy(AggressiveStrategy())
            return enemy.perform_attack(player, environment)
        else:
            return f"{enemy.name} осматривается в поисках новых целей..."

    def evaluate_threat(self, enemy, player, environment=None):
        # Агрессивный ИИ фокусируется на атаке, а не на оценке угрозы
        return f"{enemy.name} воспринимает {player.name} как цель для уничтожения"


class DefensiveAI(AIStrategy):
    """
    Защитный ИИ - фокусируется на выживании
    """
    def decide_action(self, enemy, player, environment=None):
        if enemy.health < enemy.max_health * 0.3 and random.random() < 0.6:
            # Если здоровье меньше 30%, пытаемся сбежать
            return f"{enemy.name} пытается сбежать от {player.name}!"
        elif player.is_alive:
            # Атакуем только если игрок близко
            distance = environment.get("distance_to_player", 10) if environment else 10
            if distance <= 2:
                # Устанавливаем защитную боевую стратегию для контратаки
                if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                    enemy.set_battle_strategy(DefensiveStrategy())
                return enemy.perform_attack(player, environment)
            else:
                return f"{enemy.name} укрепляется и ждет подхода {player.name}..."
        else:
            return f"{enemy.name} охраняет территорию..."

    def evaluate_threat(self, enemy, player, environment=None):
        threat_level = "низкий" if player.level < enemy.level else "высокий" if player.level > enemy.level + 2 else "средний"
        return f"{enemy.name} оценивает угрозу от {player.name} как {threat_level}"


class RandomAI(AIStrategy):
    """
    Случайный ИИ - выбирает случайное действие
    """
    def decide_action(self, enemy, player, environment=None):
        actions = ["attack", "defend", "wait", "retreat"]
        chosen_action = random.choice(actions)

        if chosen_action == "attack" and player.is_alive:
            if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                enemy.set_battle_strategy(BalancedStrategy())
            return enemy.perform_attack(player, environment)
        elif chosen_action == "defend":
            # Случайная защита - просто получаем урон
            return f"{enemy.name} сосредотачивается на защите..."
        elif chosen_action == "retreat":
            return f"{enemy.name} отступает!"
        else:
            return f"{enemy.name} ничего не делает..."

    def evaluate_threat(self, enemy, player, environment=None):
        evaluation = random.choice([
            f"{enemy.name} недооценивает {player.name}",
            f"{enemy.name} переоценивает {player.name}",
            f"{enemy.name} не может оценить {player.name}"
        ])
        return evaluation
```

</details>

#### Задание 2.2: Параметризованная стратегия

Создайте параметризованную стратегию `TacticalAI`, которая принимает решения на основе анализа соотношения сил и текущей ситуации.

```python
class TacticalAI(AIStrategy):
    """
    Тактический ИИ - анализирует ситуацию и принимает обдуманные решения
    """
    def __init__(self, aggression_level=0.5, caution_level=0.5):
        """
        Инициализировать тактический ИИ с уровнями агрессии и осторожности
        
        Args:
            aggression_level (float): Уровень агрессии (0.0 - 1.0)
            caution_level (float): Уровень осторожности (0.0 - 1.0)
        """
        self.aggression_level = aggression_level
        self.caution_level = caution_level

    def decide_action(self, enemy, player, environment=None):
        # ВАШ КОД ЗДЕСЬ - реализуйте тактическое принятие решений
        pass

    def evaluate_threat(self, enemy, player, environment=None):
        # ВАШ КОД ЗДЕСЬ - реализуйте оценку угрозы
        pass


# Пример использования (после реализации)
# tactical_dragon = Enemy("Тактический дракон", health=200, attack_power=30, defense=15, enemy_type="dragon")
# tactical_ai = TacticalAI(aggression_level=0.8, caution_level=0.3)
# tactical_dragon.set_ai_strategy(tactical_ai)
# 
# player = Character("Герой", health=150, attack_power=25, defense=10, character_class="warrior")
# 
# print(f"Враг: {tactical_dragon.get_info()}")
# print(f"Оценка угрозы: {tactical_dragon.evaluate_player_threat(player)}")
# 
# # Симуляция боя
# environment = {"distance_to_player": 3}
# for i in range(3):
#     action = tactical_dragon.take_turn(player, environment)
#     print(f"Раунд {i+1} - Действие: {action}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class TacticalAI(AIStrategy):
    """
    Тактический ИИ - анализирует ситуацию и принимает обдуманные решения
    """
    def __init__(self, aggression_level=0.5, caution_level=0.5):
        """
        Инициализировать тактический ИИ с уровнями агрессии и осторожности
        
        Args:
            aggression_level (float): Уровень агрессии (0.0 - 1.0)
            caution_level (float): Уровень осторожности (0.0 - 1.0)
        """
        self.aggression_level = aggression_level
        self.caution_level = caution_level

    def decide_action(self, enemy, player, environment=None):
        # Оцениваем соотношение сил
        enemy_strength = enemy.attack_power + enemy.health + enemy.defense
        player_strength = player.attack_power + player.health + player.defense if player.is_alive else 0

        if player_strength == 0:
            return f"{enemy.name} осматривается в поисках новых целей..."

        # Если враг намного слабее игрока, пытаемся сбежать или проявляем осторожность
        strength_ratio = enemy_strength / (player_strength if player_strength > 0 else 1)
        if strength_ratio < 0.6:
            if random.random() < self.caution_level:
                return f"{enemy.name} понимает превосходство {player.name} и пытается сбежать!"
            else:
                return f"{enemy.name} отступает на более выгодную позицию"

        # Если здоровье врага низкое, используем осторожную тактику
        if enemy.health < enemy.max_health * 0.4:
            if random.random() < self.caution_level:
                if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                    enemy.set_battle_strategy(DefensiveStrategy())
                return f"{enemy.name} использует защитную тактику!"
            else:
                # При высокой агрессии даже при низком здоровье может атаковать
                if random.random() < self.aggression_level:
                    if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                        enemy.set_battle_strategy(AggressiveStrategy())
                    return enemy.perform_attack(player, environment)
                else:
                    return f"{enemy.name} пытается восстановиться"

        # В остальных случаях действуем в соответствии с уровнем агрессии
        if random.random() < self.aggression_level:
            if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                enemy.set_battle_strategy(AggressiveStrategy())
            return enemy.perform_attack(player, environment)
        else:
            # Более осторожное поведение
            distance = environment.get("distance_to_player", 10) if environment else 10
            if distance > 3:
                return f"{enemy.name} наблюдает за {player.name} на расстоянии"
            else:
                if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                    enemy.set_battle_strategy(BalancedStrategy())
                return enemy.perform_attack(player, environment)

    def evaluate_threat(self, enemy, player, environment=None):
        # Оценка угрозы с учетом уровня осторожности
        ratio = (player.attack_power + player.health) / (enemy.attack_power + enemy.health)
        
        if ratio > 1.5:
            threat = "очень высокая"
        elif ratio > 1.1:
            threat = "высокая"
        elif ratio < 0.7:
            threat = "низкая"
        else:
            threat = "средняя"
            
        # Учитываем уровень осторожности
        if self.caution_level > 0.7 and threat == "средняя":
            threat = "выше среднего"
        elif self.caution_level < 0.3 and threat == "средняя":
            threat = "ниже среднего"
            
        return f"{enemy.name} оценивает угрозу как {threat} (соотношение сил: {ratio:.2f})"
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Асинхронная стратегия

Создайте асинхронную систему стратегий, которая может обрабатывать решения в асинхронном режиме. Реализуйте классы `AsyncStrategy` и `AsyncContext`.

**Шаги выполнения:**
1. Создайте абстрактный класс `AsyncStrategy` с асинхронными методами
2. Создайте класс `AsyncContext` с асинхронными методами выполнения стратегий
3. Обработайте ошибки в асинхронных стратегиях
4. Протестируйте систему с несколькими асинхронными стратегиями

```python
import asyncio
from typing import List, Awaitable

class AsyncStrategy(ABC):
    """
    Асинхронная стратегия
    """
    @abstractmethod
    async def execute_async(self, context, *args, **kwargs):
        """
        Асинхронное выполнение стратегии
        """
        pass


class AsyncContext:
    """
    Асинхронный контекст для выполнения стратегий
    """
    def __init__(self, name: str):
        self.name = name
        self.state = {}
        self._async_strategy: AsyncStrategy = None
        self._execution_tasks: List[asyncio.Task] = []

    def set_async_strategy(self, strategy: AsyncStrategy):
        """Установить асинхронную стратегию"""
        self._async_strategy = strategy

    async def execute_strategy(self, *args, **kwargs):
        """Асинхронно выполнить текущую стратегию"""
        if self._async_strategy:
            task = asyncio.create_task(self._async_strategy.execute_async(self, *args, **kwargs))
            self._execution_tasks.append(task)
            result = await task
            return result
        else:
            return f"{self.name} не может выполнить стратегию (нет асинхронной стратегии)"

    async def cleanup_tasks(self):
        """Очистить завершенные задачи"""
        self._execution_tasks = [task for task in self._execution_tasks if not task.done()]

    def get_active_task_count(self):
        """Получить количество активных задач"""
        return len([task for task in self._execution_tasks if not task.done()])


class AsyncExplorationStrategy(AsyncStrategy):
    """
    Асинхронная стратегия исследования карты
    """
    async def execute_async(self, context, map_data, exploration_speed=1.0):
        """Асинхронное исследование карты"""
        # ВАШ КОД ЗДЕСЬ - реализуйте асинхронное выполнение
        pass


class AsyncResourceGatheringStrategy(AsyncStrategy):
    """
    Асинхронная стратегия сбора ресурсов
    """
    async def execute_async(self, context, resource_nodes, efficiency=1.0):
        """Асинхронный сбор ресурсов"""
        # ВАШ КОД ЗДЕСЬ - реализуйте асинхронное выполнение
        pass


class AsyncBattleStrategy(AsyncStrategy):
    """
    Асинхронная боевая стратегия
    """
    async def execute_async(self, context, enemies, tactics="aggressive"):
        """Асинхронное выполнение боевой стратегии"""
        # ВАШ КОД ЗДЕСЬ - реализуйте асинхронное выполнение
        pass


# Пример использования (после реализации)
# async def async_strategy_demo():
#     # Создаем асинхронный контекст
#     explorer = AsyncContext("Исследователь")
# 
#     # Подготовим данные для стратегий
#     map_data = {
#         "areas": ["Лес", "Река", "Гора", "Пещера", "Руины", "Озеро", "Холмы", "Болото"]
#     }
# 
#     resource_nodes = [
#         {"type": "дерево", "quantity": 20, "quality": 0.8},
#         {"type": "камень", "quantity": 15, "quality": 1.2},
#         {"type": "железо", "quantity": 10, "quality": 1.5},
#         {"type": "золото", "quantity": 5, "quality": 2.0}
#     ]
# 
#     enemies = [
#         Character("Гоблин", health=30, attack_power=10, character_class="warrior"),
#         Character("Орк", health=50, attack_power=15, character_class="warrior"),
#         Character("Шаман", health=40, attack_power=12, character_class="mage")
#     ]
# 
#     # Выполняем стратегии последовательно
#     print("1. Исследование карты:")
#     explorer.set_async_strategy(AsyncExplorationStrategy())
#     result = await explorer.execute_strategy(map_data, exploration_speed=0.8)
#     print(f"   Результат: {result}")
# 
#     print(f"\nСостояние после исследования: {explorer.state}")
# 
#     print("\n2. Сбор ресурсов:")
#     explorer.set_async_strategy(AsyncResourceGatheringStrategy())
#     result = await explorer.execute_strategy(resource_nodes, efficiency=1.2)
#     print(f"   Результат: {result}")
# 
#     print(f"\nСостояние после сбора: {explorer.state}")
# 
#     print("\n3. Боевая стратегия:")
#     explorer.set_async_strategy(AsyncBattleStrategy())
#     result = await explorer.execute_strategy(enemies, tactics="aggressive")
#     print(f"   Результат: {result}")
# 
#     print(f"\nСостояние после боя: {explorer.state}")
# 
#     # Проверяем количество активных задач
#     print(f"\nАктивных задач выполнения: {explorer.get_active_task_count()}")
# 
#     # Очищаем задачи
#     await explorer.cleanup_tasks()
# 
# # Запуск асинхронной демонстрации
# # asyncio.run(async_strategy_demo())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import asyncio
from typing import List, Awaitable
import random

class AsyncExplorationStrategy(AsyncStrategy):
    """
    Асинхронная стратегия исследования карты
    """
    async def execute_async(self, context, map_data, exploration_speed=1.0):
        """Асинхронное исследование карты"""
        print(f"[ASYNC_EXPLORATION] {context.name} начинает исследование карты...")
        explored_areas = []

        # Имитация длительного процесса исследования
        for i, area in enumerate(map_data.get("areas", [])):
            if i % 3 == 0:  # Делаем паузу каждые 3 области
                print(f"[ASYNC_EXPLORATION] {context.name} делает паузу при исследовании...")
                await asyncio.sleep(0.5 * exploration_speed)  # Пауза для имитации задержки

            explored_areas.append(area)
            print(f"[ASYNC_EXPLORATION] {context.name} исследует область: {area}")

            # Случайно находим сокровище
            if random.random() < 0.2:  # 20% шанс найти сокровище
                treasure = f"сокровище_{random.randint(1, 100)}"
                context.state[f"treasure_{len(explored_areas)}"] = treasure
                print(f"[ASYNC_EXPLORATION] {context.name} находит {treasure} в области {area}!")

        context.state["explored_areas"] = explored_areas
        return f"{context.name} исследовал {len(explored_areas)} областей"


class AsyncResourceGatheringStrategy(AsyncStrategy):
    """
    Асинхронная стратегия сбора ресурсов
    """
    async def execute_async(self, context, resource_nodes, efficiency=1.0):
        """Асинхронный сбор ресурсов"""
        print(f"[ASYNC_GATHERING] {context.name} начинает сбор ресурсов...")
        gathered_resources = {}

        for node in resource_nodes:
            resource_type = node.get("type", "unknown")
            quantity = node.get("quantity", 10)
            quality = node.get("quality", 1.0)

            # Имитация времени, необходимого для сбора
            collection_time = max(0.1, 1.0 / (efficiency * quality))
            print(f"[ASYNC_GATHERING] {context.name} собирает {resource_type} из узла...")
            await asyncio.sleep(collection_time)

            gathered_amount = int(quantity * quality * efficiency)
            if resource_type in gathered_resources:
                gathered_resources[resource_type] += gathered_amount
            else:
                gathered_resources[resource_type] = gathered_amount

            print(f"[ASYNC_GATHERING] {context.name} собрал {gathered_amount} {resource_type}")

        # Добавляем ресурсы в состояние контекста
        if "resources" not in context.state:
            context.state["resources"] = {}
        for resource, amount in gathered_resources.items():
            if resource in context.state["resources"]:
                context.state["resources"][resource] += amount
            else:
                context.state["resources"][resource] = amount

        return f"{context.name} собрал ресурсы: {gathered_resources}"


class AsyncBattleStrategy(AsyncStrategy):
    """
    Асинхронная боевая стратегия
    """
    async def execute_async(self, context, enemies, tactics="aggressive"):
        """Асинхронное выполнение боевой стратегии"""
        print(f"[ASYNC_BATTLE] {context.name} вступает в бой с {len(enemies)} врагами...")
        battle_log = []

        for i, enemy in enumerate(enemies):
            print(f"[ASYNC_BATTLE] Раунд {i+1}: {context.name} против {enemy.name}")

            # Выполняем атаку
            if tactics == "aggressive":
                damage = random.randint(15, 25)
            elif tactics == "defensive":
                damage = random.randint(5, 15)
            else:
                damage = random.randint(10, 20)

            enemy.health -= damage
            battle_log.append(f"{context.name} атакует {enemy.name} на {damage} урона")
            print(f"[ASYNC_BATTLE] {context.name} наносит {damage} урона {enemy.name}")

            # Проверяем, жив ли враг
            if enemy.health <= 0:
                enemy.is_alive = False
                battle_log.append(f"{enemy.name} побежден!")
                print(f"[ASYNC_BATTLE] {enemy.name} побежден!")
                break

            # Враг атакует в ответ
            if enemy.is_alive:
                enemy_damage = random.randint(5, 15)
                # Предполагаем, что у контекста есть атрибуты здоровья
                if not hasattr(context, 'health'):
                    context.health = 100
                    context.max_health = 100
                context.health -= enemy_damage
                battle_log.append(f"{enemy.name} атакует {context.name} на {enemy_damage} урона")
                print(f"[ASYNC_BATTLE] {enemy.name} атакует {context.name} на {enemy_damage} урона")

                if context.health <= 0:
                    battle_log.append(f"{context.name} побежден!")
                    print(f"[ASYNC_BATTLE] {context.name} побежден!")
                    break

            # Делаем паузу между раундами
            await asyncio.sleep(0.3)

        context.state["battle_log"] = battle_log
        return f"{context.name} завершил бой, раундов: {len(battle_log)//2}"


# Пример использования асинхронных стратегий
async def async_strategy_demo():
    print("\n=== Демонстрация асинхронных стратегий ===\n")

    # Создаем асинхронный контекст
    explorer = AsyncContext("Исследователь")

    # Подготовим данные для стратегий
    map_data = {
        "areas": ["Лес", "Река", "Гора", "Пещера", "Руины", "Озеро", "Холмы", "Болото"]
    }

    resource_nodes = [
        {"type": "дерево", "quantity": 20, "quality": 0.8},
        {"type": "камень", "quantity": 15, "quality": 1.2},
        {"type": "железо", "quantity": 10, "quality": 1.5},
        {"type": "золото", "quantity": 5, "quality": 2.0}
    ]

    enemies = [
        Character("Гоблин", health=30, attack_power=10, character_class="warrior"),
        Character("Орк", health=50, attack_power=15, character_class="warrior"),
        Character("Шаман", health=40, attack_power=12, character_class="mage")
    ]

    # Выполняем стратегии последовательно
    print("1. Исследование карты:")
    explorer.set_async_strategy(AsyncExplorationStrategy())
    result = await explorer.execute_strategy(map_data, exploration_speed=0.8)
    print(f"   Результат: {result}")

    print(f"\nСостояние после исследования: {explorer.state}")

    print("\n2. Сбор ресурсов:")
    explorer.set_async_strategy(AsyncResourceGatheringStrategy())
    result = await explorer.execute_strategy(resource_nodes, efficiency=1.2)
    print(f"   Результат: {result}")

    print(f"\nСостояние после сбора: {explorer.state}")

    print("\n3. Боевая стратегия:")
    explorer.set_async_strategy(AsyncBattleStrategy())
    result = await explorer.execute_strategy(enemies, tactics="aggressive")
    print(f"   Результат: {result}")

    print(f"\nСостояние после боя: {explorer.state}")

    # Проверяем количество активных задач
    print(f"\nАктивных задач выполнения: {explorer.get_active_task_count()}")

    # Очищаем задачи
    await explorer.cleanup_tasks()
```

</details>

---

## 1. Создание простой системы стратегий для игровых действий

### Пример 1: Класс Character с боевыми стратегиями

```python
from abc import ABC, abstractmethod

class MovementStrategy(ABC):
    """
    Стратегия перемещения персонажа
    """
    @abstractmethod
    def move(self, character, target_position, environment=None):
        """
        Переместить персонажа в целевую позицию
        """
        pass


class DirectMovementStrategy(MovementStrategy):
    """
    Прямолинейное перемещение - движение по прямой к цели
    """
    def __init__(self, speed=1.0):
        self.speed = speed

    def move(self, character, target_position, environment=None):
        # Вычисляем вектор направления
        dx = target_position[0] - character.position[0] if hasattr(character, 'position') else 0
        dy = target_position[1] - character.position[1] if hasattr(character, 'position') else 0

        # Нормализуем вектор и умножаем на скорость
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return f"{character.name} уже на месте {target_position}"

        move_distance = min(self.speed, distance)
        new_x = character.position[0] + (dx / distance) * move_distance if hasattr(character, 'position') else 0
        new_y = character.position[1] + (dy / distance) * move_distance if hasattr(character, 'position') else 0

        # Устанавливаем новую позицию
        if not hasattr(character, 'position'):
            character.position = (0, 0)
        character.position = (new_x, new_y)

        return f"{character.name} движется к {target_position}, теперь в {character.position}"


class AvoidanceMovementStrategy(MovementStrategy):
    """
    Стратегия перемещения с избеганием препятствий
    """
    def __init__(self, speed=1.0, detection_radius=5.0):
        self.speed = speed
        self.detection_radius = detection_radius

    def move(self, character, target_position, environment=None):
        current_pos = getattr(character, 'position', (0, 0))
        obstacles = environment.get("obstacles", []) if environment else []
        
        # Проверяем, есть ли препятствия на пути
        dx = target_position[0] - current_pos[0]
        dy = target_position[1] - current_pos[1]
        distance = (dx**2 + dy**2)**0.5

        if distance == 0:
            return f"{character.name} уже на месте {target_position}"

        # Нормализуем вектор направления
        dir_x = dx / distance
        dir_y = dy / distance

        # Проверяем препятствия в радиусе обнаружения
        for obstacle in obstacles:
            obs_x, obs_y = obstacle
            dist_to_obs = ((current_pos[0] - obs_x)**2 + (current_pos[1] - obs_y)**2)**0.5

            if dist_to_obs < self.detection_radius:
                # Избегаем препятствие, слегка изменяя направление
                avoidance_factor = 1.0 - (dist_to_obs / self.detection_radius)
                # Смещаемся перпендикулярно направлению к цели
                perp_x = -dir_y * avoidance_factor * self.speed * 0.5
                perp_y = dir_x * avoidance_factor * self.speed * 0.5

                new_x = current_pos[0] + dir_x * self.speed * 0.5 + perp_x
                new_y = current_pos[1] + dir_y * self.speed * 0.5 + perp_y
                
                character.position = (new_x, new_y)
                return f"{character.name} избегает препятствие в {obstacle}, теперь в {character.position}"

        # Если препятствий нет, движемся напрямую
        move_distance = min(self.speed, distance)
        new_x = current_pos[0] + dir_x * move_distance
        new_y = current_pos[1] + dir_y * move_distance
        character.position = (new_x, new_y)

        return f"{character.name} движется к {target_position}, теперь в {character.position}"


class CharacterWithMovement(Character):
    """
    Персонаж с поддержкой стратегий перемещения
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        super().__init__(name, health, attack_power, defense, character_class)
        self.position = (0, 0)  # Добавляем позицию
        self._movement_strategy: MovementStrategy = None

    def set_movement_strategy(self, strategy: MovementStrategy):
        """Установить стратегию перемещения"""
        self._movement_strategy = strategy

    def move_to(self, target_position, environment=None):
        """Переместиться в целевую позицию с использованием стратегии"""
        if self._movement_strategy:
            return self._movement_strategy.move(self, target_position, environment)
        else:
            return f"{self.name} не может двигаться (нет стратегии перемещения)"


# Пример использования
print("=== Демонстрация стратегий перемещения ===\n")

# Создаем персонажа
warrior = CharacterWithMovement("Конан", health=120, attack_power=25, defense=8, character_class="warrior")

# Устанавливаем стратегию перемещения
warrior.set_movement_strategy(DirectMovementStrategy(speed=2.0))

print(f"Персонаж: {warrior.get_info()}")
print(f"Позиция: {warrior.position}")

# Перемещаемся к цели
result = warrior.move_to((10, 10))
print(f"Результат перемещения: {result}")
print(f"Новая позиция: {warrior.position}")

# Меняем стратегию на избегание препятствий
warrior.set_movement_strategy(AvoidanceMovementStrategy(speed=1.5, detection_radius=3.0))

# Перемещаемся с препятствиями
environment_with_obstacles = {"obstacles": [(5, 5), (7, 7)]}
result = warrior.move_to((15, 15), environment_with_obstacles)
print(f"Результат перемещения с избеганием: {result}")
print(f"Финальная позиция: {warrior.position}")
```

### Пример 2: Класс GameEventPublisher с использованием стратегии

```python
class ResourceManagementStrategy(ABC):
    """
    Стратегия управления ресурсами
    """
    @abstractmethod
    def manage_resources(self, entity, resources, environment=None):
        """
        Управление ресурсами сущности
        """
        pass


class ConservativeResourceStrategy(ResourceManagementStrategy):
    """
    Консервативная стратегия управления ресурсами - экономит ресурсы
    """
    def manage_resources(self, entity, resources, environment=None):
        report = []
        for resource, amount in resources.items():
            max_amount = getattr(entity, f'max_{resource}', 100) if hasattr(entity, f'max_{resource}') else 100
            if amount < max_amount * 0.3:  # Если ресурс на уровне менее 30%
                report.append(f"{entity.name} экономит {resource} (текущий запас: {amount})")
            elif amount > max_amount * 0.8:  # Если ресурс на уровне более 80%
                report.append(f"{entity.name} имеет избыток {resource} (запас: {amount})")
            else:
                report.append(f"{entity.name} имеет умеренный запас {resource} (запас: {amount})")
        return "; ".join(report)


class AggressiveResourceStrategy(ResourceManagementStrategy):
    """
    Агрессивная стратегия управления ресурсами - активно использует ресурсы
    """
    def manage_resources(self, entity, resources, environment=None):
        report = []
        for resource, amount in resources.items():
            if resource == "mana" and amount > 10:  # Используем ману для атак
                consumption = min(amount, 10)
                resources[resource] -= consumption
                report.append(f"{entity.name} активно использует {resource} (-{consumption})")
            elif resource == "health" and amount < getattr(entity, 'max_health', 100) * 0.5:  # Лечимся при низком здоровье
                # Имитируем использование зелья лечения
                healing = min(20, getattr(entity, 'max_health', 100) - amount)
                resources[resource] += healing
                actual_heal = healing
                report.append(f"{entity.name} использует лечение для восстановления {actual_heal} здоровья")
            else:
                report.append(f"{entity.name} управляет {resource} агрессивно (запас: {amount})")
        return "; ".join(report)


class ResourcefulCharacter(CharacterWithMovement):
    """
    Персонаж с системой управления ресурсами
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        super().__init__(name, health, attack_power, defense, character_class)
        self.resources = {"health": self.health, "mana": 50, "stamina": 100, "gold": 0}
        self.max_health = health
        self.max_mana = 50
        self.max_stamina = 100
        self._resource_strategy: ResourceManagementStrategy = None

    def set_resource_strategy(self, strategy: ResourceManagementStrategy):
        """Установить стратегию управления ресурсами"""
        self._resource_strategy = strategy

    def manage_resources(self, environment=None):
        """Управление ресурсами с использованием стратегии"""
        if self._resource_strategy:
            return self._resource_strategy.manage_resources(self, self.resources, environment)
        else:
            return f"{self.name} не может управлять ресурсами (нет стратегии управления)"


# Пример использования
print("\n=== Демонстрация стратегий управления ресурсами ===\n")

# Создаем персонажа с ресурсами
mage = ResourcefulCharacter("Мерлин", health=80, attack_power=30, defense=3, character_class="mage")
print(f"Персонаж: {mage.get_info()}")
print(f"Ресурсы: {mage.resources}")

# Устанавливаем консервативную стратегию
mage.set_resource_strategy(ConservativeResourceStrategy())
result = mage.manage_resources()
print(f"Результат консервативного управления: {result}")

# Изменим ресурсы для демонстрации
mage.resources["mana"] = 45
mage.resources["health"] = 20
print(f"\nПосле изменения ресурсов: {mage.resources}")

# Меняем на агрессивную стратегию
mage.set_resource_strategy(AggressiveResourceStrategy())
result = mage.manage_resources()
print(f"Результат агрессивного управления: {result}")
print(f"Финальные ресурсы: {mage.resources}")
```

---

## 2. Стратегии и контексты в игровом контексте

### Стратегии для различных игровых систем

```python
class CombatTacticStrategy(ABC):
    """
    Стратегия боевой тактики
    """
    @abstractmethod
    def select_target(self, entity, possible_targets, environment=None):
        """
        Выбрать цель для атаки
        """
        pass

    @abstractmethod
    def choose_attack_type(self, entity, target, environment=None):
        """
        Выбрать тип атаки
        """
        pass


class PriorityTargetCombatStrategy(CombatTacticStrategy):
    """
    Стратегия боевой тактики с приоритетами целей
    """
    def __init__(self, target_priorities=None):
        self.target_priorities = target_priorities or ["mage", "archer", "warrior", "tank"]

    def select_target(self, entity, possible_targets, environment=None):
        if not possible_targets:
            return None

        # Сортируем цели по приоритету
        def get_priority(target):
            class_priority = getattr(target, 'character_class', 'warrior')
            if class_priority in self.target_priorities:
                return self.target_priorities.index(class_priority)
            else:
                return len(self.target_priorities)  # Последний приоритет для неизвестных классов

        possible_targets.sort(key=get_priority)
        return possible_targets[0]

    def choose_attack_type(self, entity, target, environment=None):
        # Выбираем тип атаки в зависимости от цели
        if hasattr(target, 'character_class'):
            if target.character_class in ["mage", "archer"]:  # Уязвимы к быстрым атакам
                return "быстрая атака"
            elif target.character_class in ["warrior", "tank"]:  # Требуется мощная атака
                return "мощная атака"
        return "стандартная атака"


class DefensiveCombatStrategy(CombatTacticStrategy):
    """
    Защитная боевая стратегия - фокусируется на выживании
    """
    def select_target(self, entity, possible_targets, environment=None):
        if not possible_targets:
            return None

        # Выбираем самую слабую цель для быстрой победы
        possible_targets.sort(key=lambda t: getattr(t, 'health', 100))
        return possible_targets[0]

    def choose_attack_type(self, entity, target, environment=None):
        # Выбираем осторожную атаку, чтобы не потерять здоровье
        return "осторожная атака"


class SmartCombatCharacter(ResourcefulCharacter):
    """
    Персонаж с интеллектуальной боевой системой
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        super().__init__(name, health, attack_power, defense, character_class)
        self._combat_strategy: CombatTacticStrategy = None

    def set_combat_strategy(self, strategy: CombatTacticStrategy):
        """Установить боевую стратегию"""
        self._combat_strategy = strategy

    def select_combat_target(self, possible_targets, environment=None):
        """Выбрать цель для атаки"""
        if self._combat_strategy:
            return self._combat_strategy.select_target(self, possible_targets, environment)
        else:
            # Если стратегии нет, выбираем первую доступную цель
            return possible_targets[0] if possible_targets else None

    def choose_attack_type(self, target, environment=None):
        """Выбрать тип атаки"""
        if self._combat_strategy:
            return self._combat_strategy.choose_attack_type(self, target, environment)
        else:
            return "стандартная атака"


# Пример использования
print("\n=== Демонстрация боевых стратегий ===\n")

# Создаем персонажей
tank = Character("Танк", health=200, attack_power=15, defense=15, character_class="tank")
archer = Character("Лучник", health=70, attack_power=25, defense=5, character_class="archer")
mage = Character("Маг", health=60, attack_power=30, defense=3, character_class="mage")

# Создаем умного персонажа
smart_warrior = SmartCombatCharacter("Разумный воин", health=150, attack_power=20, defense=10, character_class="warrior")

# Устанавливаем стратегию с приоритетами целей
smart_warrior.set_combat_strategy(PriorityTargetCombatStrategy(target_priorities=["mage", "archer", "tank"]))

targets = [tank, archer, mage]
print("Доступные цели:")
for target in targets:
    print(f"  {target.get_info()}")

selected_target = smart_warrior.select_combat_target(targets)
if selected_target:
    attack_type = smart_warrior.choose_attack_type(selected_target)
    print(f"\nВыбранная цель: {selected_target.name} ({selected_target.character_class})")
    print(f"Тип атаки: {attack_type}")

# Меняем стратегию на защитную
smart_warrior.set_combat_strategy(DefensiveCombatStrategy())
selected_target = smart_warrior.select_combat_target(targets)
if selected_target:
    attack_type = smart_warrior.choose_attack_type(selected_target)
    print(f"\nС защитной стратегией выбрана цель: {selected_target.name} ({selected_target.character_class})")
    print(f"Тип атаки: {attack_type}")
```

---

## 3. Практические задания в игровом контексте

### Задание 1: Система развития персонажа с использованием стратегий

Создайте систему развития персонажа, где различные стратегии определяют, как персонаж распределяет очки характеристик при повышении уровня.

```python
class CharacterDevelopmentStrategy(ABC):
    """
    Стратегия развития персонажа
    """
    @abstractmethod
    def develop_character(self, character, experience_points: int):
        """
        Развить персонажа с учетом опыта
        """
        pass


class BalancedDevelopmentStrategy(CharacterDevelopmentStrategy):
    """
    Сбалансированная стратегия развития - равномерно распределяет очки
    """
    def develop_character(self, character, experience_points: int):
        # При получении опыта начисляем очки развития
        skill_points_gained = experience_points // 100  # 1 очко за каждые 100 опыта
        
        if skill_points_gained > 0:
            # Равномерно распределяем очки между основными характеристиками
            points_per_attribute = skill_points_gained // 3
            remainder = skill_points_gained % 3
            
            # Увеличиваем характеристики
            character.max_health += points_per_attribute * 5
            character.attack_power += points_per_attribute
            character.defense += points_per_attribute
            
            # Добавляем остаток к случайной характеристике
            if remainder > 0:
                import random
                attributes = ['max_health', 'attack_power', 'defense']
                for i in range(remainder):
                    attr = random.choice(attributes)
                    if attr == 'max_health':
                        setattr(character, attr, getattr(character, attr) + 5)
                    else:
                        setattr(character, attr, getattr(character, attr) + 1)
            
            # Полностью восстанавливаем здоровье
            character.health = character.max_health
            
            return f"{character.name} получил {skill_points_gained} очков развития и улучшил характеристики"
        else:
            return f"{character.name} получил {experience_points} опыта, но недостаточно для развития"


class SpecializedDevelopmentStrategy(CharacterDevelopmentStrategy):
    """
    Специализированная стратегия развития - фокусируется на одной характеристике
    """
    def __init__(self, primary_attribute: str = "attack_power"):
        self.primary_attribute = primary_attribute

    def develop_character(self, character, experience_points: int):
        # При получении опыта начисляем очки развития
        skill_points_gained = experience_points // 100  # 1 очко за каждые 100 опыта
        
        if skill_points_gained > 0:
            # Большинство очков идет в основную характеристику
            primary_points = int(skill_points_gained * 0.6)
            secondary_points = skill_points_gained - primary_points
            
            # Увеличиваем основную характеристику
            if self.primary_attribute == "max_health":
                character.max_health += primary_points * 5
            elif self.primary_attribute == "attack_power":
                character.attack_power += primary_points
            elif self.primary_attribute == "defense":
                character.defense += primary_points
            
            # Оставшиеся очки распределяем между другими
            if self.primary_attribute != "max_health":
                character.max_health += (secondary_points // 2) * 5
            if self.primary_attribute != "attack_power":
                character.attack_power += secondary_points // 2
            if self.primary_attribute != "defense":
                character.defense += secondary_points - (secondary_points // 2)
            
            # Полностью восстанавливаем здоровье
            character.health = character.max_health
            
            return f"{character.name} получил {skill_points_gained} очков развития и усилил {self.primary_attribute}"
        else:
            return f"{character.name} получил {experience_points} опыта, но недостаточно для развития"


class Player(Character):
    """
    Класс игрока с системой развития
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        super().__init__(name, health, attack_power, defense, character_class)
        self._development_strategy: CharacterDevelopmentStrategy = None
        self.experience = 0

    def set_development_strategy(self, strategy: CharacterDevelopmentStrategy):
        """Установить стратегию развития"""
        self._development_strategy = strategy

    def gain_experience(self, exp: int):
        """Получить опыт и развиться по стратегии"""
        self.experience += exp
        if self._development_strategy:
            return self._development_strategy.develop_character(self, exp)
        else:
            return f"{self.name} получил {exp} опыта, но нет стратегии развития"


# Тестирование системы развития
print("\n=== Система развития персонажа ===\n")

# Создаем двух игроков
balanced_player = Player("Баланс", health=100, attack_power=20, defense=5, character_class="warrior")
specialized_player = Player("Специалист", health=100, attack_power=20, defense=5, character_class="warrior")

print(f"Игрок 1 (до): {balanced_player.get_info()}")
print(f"Игрок 2 (до): {specialized_player.get_info()}")

# Устанавливаем разные стратегии развития
balanced_player.set_development_strategy(BalancedDevelopmentStrategy())
specialized_player.set_development_strategy(SpecializedDevelopmentStrategy("attack_power"))

# Игроки получают опыт
result1 = balanced_player.gain_experience(150)
result2 = specialized_player.gain_experience(150)

print(f"\nРезультаты развития:")
print(f"Игрок 1: {result1}")
print(f"Игрок 2: {result2}")

print(f"\nИгрок 1 (после): {balanced_player.get_info()}")
print(f"Игрок 2 (после): {specialized_player.get_info()}")
```

### Задание 2: Система торговли с использованием стратегий

Создайте систему торговли, где различные стратегии определяют, как рассчитываются цены и какие товары предлагаются.

```python
class TradingStrategy(ABC):
    """
    Стратегия торговли
    """
    @abstractmethod
    def calculate_price(self, item, base_price: float, environment=None):
        """
        Рассчитать цену товара
        """
        pass

    @abstractmethod
    def select_items_for_sale(self, merchant, environment=None):
        """
        Выбрать товары для продажи
        """
        pass


class EconomicTradingStrategy(TradingStrategy):
    """
    Экономическая стратегия торговли - цены зависят от спроса и предложения
    """
    def __init__(self):
        self.price_modifiers = {}  # Модификаторы цен для разных товаров в разных регионах

    def calculate_price(self, item, base_price: float, environment=None):
        # Рассчитываем модификатор цены на основе спроса/предложения
        region = getattr(environment, 'region', 'default') if environment else 'default'
        item_type = getattr(item, 'item_type', 'unknown')

        # Получаем модификатор цены для региона и типа товара
        region_modifiers = self.price_modifiers.get(region, {})
        price_modifier = region_modifiers.get(item_type, 1.0)

        # Также учитываем редкость предмета
        rarity_multiplier = getattr(item, 'rarity_multiplier', 1.0)

        return base_price * price_modifier * rarity_multiplier

    def select_items_for_sale(self, merchant, environment=None):
        # В реальной игре здесь был бы сложный алгоритм выбора товаров
        # В упрощенном варианте возвращаем все возможные товары
        possible_items = [
            {"name": "Меч", "type": "weapon", "base_value": 100},
            {"name": "Щит", "type": "armor", "base_value": 80},
            {"name": "Зелье здоровья", "type": "potion", "base_value": 25},
            {"name": "Магическая книга", "type": "spellbook", "base_value": 150}
        ]
        return possible_items


class Merchant:
    """
    Класс торговца с системой торговли
    """
    def __init__(self, name: str, trading_strategy: TradingStrategy = None):
        self.name = name
        self.inventory = []
        self.gold = 1000
        self._trading_strategy = trading_strategy

    def set_trading_strategy(self, strategy: TradingStrategy):
        """Установить стратегию торговли"""
        self._trading_strategy = strategy

    def calculate_item_price(self, item, base_price: float, environment=None):
        """Рассчитать цену товара по стратегии"""
        if self._trading_strategy:
            return self._trading_strategy.calculate_price(item, base_price, environment)
        else:
            return base_price  # Без стратегии цена остается базовой

    def get_available_items(self, environment=None):
        """Получить доступные для продажи товары"""
        if self._trading_strategy:
            return self._trading_strategy.select_items_for_sale(self, environment)
        else:
            return []  # Без стратегии нет доступных товаров


# Тестирование системы торговли
print("\n=== Система торговли ===\n")

# Создаем торговца
merchant = Merchant("Купец Джон")

# Создаем экономическую стратегию
economic_strategy = EconomicTradingStrategy()
merchant.set_trading_strategy(economic_strategy)

# Добавляем модификаторы цен для разных регионов
economic_strategy.price_modifiers = {
    "горы": {"weapon": 1.2, "armor": 1.1, "potion": 0.9},
    "лес": {"weapon": 1.0, "armor": 0.9, "potion": 1.1},
    "равнина": {"weapon": 0.9, "armor": 1.0, "potion": 1.0}
}

# Создаем товар
class Item:
    def __init__(self, name, item_type, base_value, rarity_multiplier=1.0):
        self.name = name
        self.item_type = item_type
        self.base_value = base_value
        self.rarity_multiplier = rarity_multiplier

sword = Item("Меч героя", "weapon", 100, 1.5)

# Рассчитываем цены в разных регионах
environments = [{"region": "горы"}, {"region": "лес"}, {"region": "равнина"}]

print(f"Базовая цена меча: {sword.base_value}")
for env in environments:
    calculated_price = merchant.calculate_item_price(sword, sword.base_value, env)
    print(f"Цена в регионе '{env['region']}': {calculated_price:.2f}")

# Получаем доступные товары
available_items = merchant.get_available_items()
print(f"\nДоступные товары: {len(available_items)}")
for item in available_items[:3]:  # Показываем первые 3
    print(f"  - {item['name']} ({item['type']}), базовая цена: {item['base_value']}")
```

### Задание 3: Сравнение различных реализаций Strategy

Создайте таблицу сравнения различных типов Strategy (обычная, параметризованная, асинхронная) по критериям: сложность реализации, производительность, гибкость, применимость в игровой разработке. Приведите примеры, когда каждый тип стратегии наиболее эффективен в игровом контексте.

```python
def compare_strategies():
    """
    Сравнение различных типов Strategy
    """
    comparison = {
        "Обычная Strategy": {
            "Сложность реализации": "Низкая",
            "Производительность": "Высокая",
            "Гибкость": "Средняя",
            "Применимость в играх": "Простые алгоритмы поведения, боевые тактики, развитие персонажа"
        },
        "Параметризованная Strategy": {
            "Сложность реализации": "Средняя",
            "Производительность": "Средняя",
            "Гибкость": "Высокая",
            "Применимость в играх": "Адаптивные системы, зависящие от параметров окружения или персонажа"
        },
        "Асинхронная Strategy": {
            "Сложность реализации": "Высокая",
            "Производительность": "Высокая (для I/O операций)",
            "Гибкость": "Высокая",
            "Применимость в играх": "Длительные операции (исследование, сбор ресурсов, сетевые вызовы)"
        }
    }

    print("Сравнение типов Strategy в игровой разработке:")
    print("-" * 80)
    print(f"{'Тип Strategy':<20} {'Сложность':<12} {'Произв.':<10} {'Гибкость':<10} {'Применимость':<30}")
    print("-" * 80)

    for strategy_type, props in comparison.items():
        print(f"{strategy_type:<20} {props['Сложность реализации']:<12} {props['Производительность']:<10} {props['Гибкость']:<10} {props['Применимость в играх']:<30}")

compare_strategies()
```

---

## 4. Дополнительные задания

### Задание 4: Интеграция с другими паттернами

Создайте пример интеграции паттерна Strategy с другими паттернами (например, Observer, Factory), чтобы создать более сложную и гибкую игровую систему.

### Задание 5: Система модификаций

Реализуйте систему модификаций предметов, где разные стратегии модификаций применяются к различным типам предметов (оружие, броня, зелья и т.д.).

---

## Контрольные вопросы:
1. В чем разница между паттернами Strategy и State в игровом контексте?
2. Как обеспечить потокобезопасность стратегий в многопоточной игровой среде?
3. Какие преимущества дает использование Strategy в системах боевой тактики?
4. Как обрабатывать ошибки в стратегиях, чтобы не прерывать выполнение других компонентов?
5. Как использовать Strategy для создания адаптивного ИИ в играх?