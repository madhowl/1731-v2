# Практическое занятие 16: ООП - паттерн Strategy в игровом контексте

## Цель занятия
Изучить паттерн проектирования Strategy (Стратегия) и научиться реализовывать его в Python для выбора алгоритмов во время выполнения программы в игровом контексте, а также понять, когда и зачем использовать этот паттерн в игровой разработке.

## Задачи

### Задача 1: Базовая реализация Strategy для боевых действий (20 баллов)
Создайте систему боевых стратегий:
- Интерфейс `BattleStrategy` с методом `execute_attack()`
- Класс `Character` как контекст, использующий стратегию
- Конкретные стратегии: `AggressiveStrategy`, `DefensiveStrategy`, `BalancedStrategy`

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

### Задача 2: Использование стратегии для ИИ врагов (20 баллов)
Реализуйте систему поведения врагов с использованием различных стратегий:
- `AggressiveAI`, `DefensiveAI`, `RandomAI`, `TacticalAI`
- Класс `Enemy` как контекст
- Методы для принятия решений в бою

```python
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


class TacticalAI(AIStrategy):
    """
    Тактический ИИ - анализирует ситуацию и принимает обдуманные решения
    """
    def decide_action(self, enemy, player, environment=None):
        # Оцениваем соотношение сил
        enemy_strength = enemy.attack_power + enemy.health
        player_strength = player.attack_power + player.health if player.is_alive else 0

        if player_strength == 0:
            return f"{enemy.name} осматривается в поисках новых целей..."

        # Если враг намного слабее игрока, пытаемся сбежать
        if enemy_strength < player_strength * 0.6:
            return f"{enemy.name} понимает превосходство {player.name} и пытается сбежать!"

        # Если здоровье врага низкое, используем защитную тактику
        if enemy.health < enemy.max_health * 0.4:
            if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                enemy.set_battle_strategy(DefensiveStrategy())
            return f"{enemy.name} использует защитную тактику!"
        else:
            # Иначе атакуем
            if not hasattr(enemy, '_battle_strategy') or enemy._battle_strategy is None:
                enemy.set_battle_strategy(AggressiveStrategy())
            return enemy.perform_attack(player, environment)

    def evaluate_threat(self, enemy, player, environment=None):
        ratio = (player.attack_power + player.health) / (enemy.attack_power + enemy.health)
        if ratio > 1.5:
            threat = "очень высокая"
        elif ratio > 1.1:
            threat = "высокая"
        elif ratio < 0.7:
            threat = "низкая"
        else:
            threat = "средняя"
        return f"{enemy.name} оценивает угрозу как {threat} (соотношение сил: {ratio:.2f})"


# Пример использования системы ИИ врагов
print("\n=== Демонстрация паттерна Strategy для ИИ врагов ===\n")

# Создаем врагов с разными стратегиями ИИ
aggressive_goblin = Enemy("Агрессивный гоблин", health=50, attack_power=15, defense=2, enemy_type="goblin")
defensive_orc = Enemy("Оборонительный орк", health=80, attack_power=12, defense=8, enemy_type="orc")
random_skeleton = Enemy("Случайный скелет", health=40, attack_power=10, defense=3, enemy_type="skeleton")
tactical_dragon = Enemy("Тактический дракон", health=200, attack_power=30, defense=15, enemy_type="dragon")

# Создаем игрока
player = Character("Герой", health=150, attack_power=25, defense=10, character_class="warrior")

# Устанавливаем стратегии ИИ
aggressive_goblin.set_ai_strategy(AggressiveAI())
defensive_orc.set_ai_strategy(DefensiveAI())
random_skeleton.set_ai_strategy(RandomAI())
tactical_dragon.set_ai_strategy(TacticalAI())

enemies = [aggressive_goblin, defensive_orc, random_skeleton, tactical_dragon]

print("Информация о врагах:")
for enemy in enemies:
    print(f"  {enemy.get_info()}")

print(f"\nОценка угрозы от врагов:")
for enemy in enemies:
    threat_eval = enemy.evaluate_player_threat(player)
    print(f"  {threat_eval}")

# Симуляция боевых действий
print(f"\n--- Боевая симуляция ---")
environment = {"distance_to_player": 3}  # Начальное расстояние

for i in range(3):  # Три раунда
    print(f"\nРаунд {i+1}:")
    for enemy in enemies:
        if enemy.is_alive:
            action_result = enemy.take_turn(player, environment)
            print(f"  {action_result}")

    # Игрок атакует в ответ (только живых врагов)
    alive_enemies = [e for e in enemies if e.is_alive]
    if alive_enemies:
        target = alive_enemies[0]  # Атакуем первого живого врага
        player.set_battle_strategy(AggressiveStrategy())
        attack_result = player.perform_attack(target)
        print(f"  {attack_result}")

    print(f"\nСостояние после раунда {i+1}:")
    print(f"  {player.get_info()}")
    for enemy in enemies:
        if enemy.is_alive:
            print(f"  {enemy.get_info()}")
```

### Задача 3: Параметризованные стратегии для игровых механик (20 баллов)
Создайте систему с параметризованными стратегиями:
- Возможность настройки параметров стратегии
- Классы `MovementStrategy`, `ResourceManagementStrategy`, `CombatTacticStrategy`
- Контекст `GameEntity`

```python
class MovementStrategy(ABC):
    """
    Стратегия перемещения игрового объекта
    """
    @abstractmethod
    def move(self, entity, target_position, environment=None):
        """
        Переместить сущность в целевую позицию
        """
        pass

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

class GameEntity:
    """
    Игровая сущность как контекст для различных стратегий
    """
    def __init__(self, name: str, position=(0, 0), resources: dict = None):
        self.name = name
        self.position = position
        self.resources = resources or {"health": 100, "mana": 50, "gold": 0}
        self.max_resources = {"health": 100, "mana": 50, "gold": 1000}
        self.is_alive = True

        # Стратегии
        self._movement_strategy: MovementStrategy = None
        self._resource_strategy: ResourceManagementStrategy = None
        self._combat_strategy: CombatTacticStrategy = None

    def set_movement_strategy(self, strategy: MovementStrategy):
        self._movement_strategy = strategy

    def set_resource_strategy(self, strategy: ResourceManagementStrategy):
        self._resource_strategy = strategy

    def set_combat_strategy(self, strategy: CombatTacticStrategy):
        self._combat_strategy = strategy

    def move_to(self, target_position, environment=None):
        if self._movement_strategy:
            return self._movement_strategy.move(self, target_position, environment)
        else:
            return f"{self.name} не может двигаться (нет стратегии перемещения)"

    def manage_resources(self, environment=None):
        if self._resource_strategy:
            return self._resource_strategy.manage_resources(self, self.resources, environment)
        else:
            return f"{self.name} не может управлять ресурсами (нет стратегии управления)"

    def select_combat_target(self, possible_targets, environment=None):
        if self._combat_strategy:
            return self._combat_strategy.select_target(self, possible_targets, environment)
        else:
            return None

    def choose_attack(self, target, environment=None):
        if self._combat_strategy:
            return self._combat_strategy.choose_attack_type(self, target, environment)
        else:
            return "атака по умолчанию"


class DirectMovementStrategy(MovementStrategy):
    """
    Прямолинейное перемещение - движение по прямой к цели
    """
    def __init__(self, speed=1.0, ignore_obstacles=False):
        self.speed = speed
        self.ignore_obstacles = ignore_obstacles

    def move(self, entity, target_position, environment=None):
        # Вычисляем вектор направления
        dx = target_position[0] - entity.position[0]
        dy = target_position[1] - entity.position[1]

        # Нормализуем вектор и умножаем на скорость
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return f"{entity.name} уже на месте {target_position}"

        move_distance = min(self.speed, distance)
        new_x = entity.position[0] + (dx / distance) * move_distance
        new_y = entity.position[1] + (dy / distance) * move_distance

        entity.position = (new_x, new_y)

        # Проверяем препятствия в окружающей среде
        obstacles = environment.get("obstacles", []) if environment else []
        if not self.ignore_obstacles and entity.position in obstacles:
            return f"{entity.name} столкнулся с препятствием в {entity.position} и остановился"

        return f"{entity.name} движется к {target_position}, теперь в {entity.position}"


class AvoidanceMovementStrategy(MovementStrategy):
    """
    Стратегия перемещения с избеганием препятствий
    """
    def __init__(self, speed=1.0, detection_radius=5.0):
        self.speed = speed
        self.detection_radius = detection_radius

    def move(self, entity, target_position, environment=None):
        obstacles = environment.get("obstacles", []) if environment else []
        current_x, current_y = entity.position

        # Проверяем, есть ли препятствия на пути
        dx = target_position[0] - current_x
        dy = target_position[1] - current_y
        distance = (dx**2 + dy**2)**0.5

        if distance == 0:
            return f"{entity.name} уже на месте {target_position}"

        # Нормализуем вектор направления
        dir_x = dx / distance
        dir_y = dy / distance

        # Проверяем препятствия в радиусе обнаружения
        for obstacle in obstacles:
            obs_x, obs_y = obstacle
            dist_to_obs = ((current_x - obs_x)**2 + (current_y - obs_y)**2)**0.5

            if dist_to_obs < self.detection_radius:
                # Избегаем препятствие, слегка изменяя направление
                avoidance_factor = 1.0 - (dist_to_obs / self.detection_radius)
                # Смещаемся перпендикулярно направлению к цели
                perp_x = -dir_y * avoidance_factor * self.speed * 0.5
                perp_y = dir_x * avoidance_factor * self.speed * 0.5

                new_x = current_x + dir_x * self.speed * 0.5 + perp_x
                new_y = current_y + dir_y * self.speed * 0.5 + perp_y
                entity.position = (new_x, new_y)
                return f"{entity.name} избегает препятствие, теперь в {entity.position}"

        # Если препятствий нет, движемся напрямую
        move_distance = min(self.speed, distance)
        new_x = current_x + dir_x * move_distance
        new_y = current_y + dir_y * move_distance
        entity.position = (new_x, new_y)

        return f"{entity.name} движется к {target_position}, теперь в {entity.position}"


class ConservativeResourceStrategy(ResourceManagementStrategy):
    """
    Консервативная стратегия управления ресурсами - экономит ресурсы
    """
    def manage_resources(self, entity, resources, environment=None):
        report = []
        for resource, amount in resources.items():
            max_amount = entity.max_resources.get(resource, 0)
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
            elif resource == "health" and amount < entity.max_resources[resource] * 0.5:  # Лечимся при низком здоровье
                # Имитируем использование зелья лечения
                healing = min(20, entity.max_resources[resource] - amount)
                resources[resource] += healing
                report.append(f"{entity.name} использует лечение для восстановления {healing} здоровья")
            else:
                report.append(f"{entity.name} управляет {resource} агрессивно (запас: {amount})")
        return "; ".join(report)


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


# Пример использования параметризованных стратегий
print("\n=== Демонстрация параметризованных стратегий ===\n")

# Создаем игровую сущность
entity = GameEntity("Рыцарь", position=(0, 0), resources={"health": 80, "mana": 30, "gold": 100})

# Создаем и устанавливаем стратегии
direct_move = DirectMovementStrategy(speed=2.0, ignore_obstacles=False)
avoidance_move = AvoidanceMovementStrategy(speed=1.5, detection_radius=3.0)
conservative_res = ConservativeResourceStrategy()
aggressive_res = AggressiveResourceStrategy()
priority_combat = PriorityTargetCombatStrategy(target_priorities=["mage", "archer", "warrior"])
defensive_combat = DefensiveCombatStrategy()

entity.set_movement_strategy(direct_move)
entity.set_resource_strategy(conservative_res)
entity.set_combat_strategy(priority_combat)

print(f"Сущность: {entity.name}, позиция: {entity.position}, ресурсы: {entity.resources}")

# Перемещение с препятствиями
environment = {"obstacles": [(3, 3), (5, 5), (7, 2)]}
print(f"\n1. Перемещение к (10, 10) с препятствиями:")
for i in range(5):
    result = entity.move_to((10, 10), environment)
    print(f"   {result}")

# Управление ресурсами
print(f"\n2. Управление ресурсами:")
result = entity.manage_resources(environment)
print(f"   {result}")

# Создаем цели для боевой стратегии
targets = [
    Character("Маг", health=70, attack_power=25, character_class="mage"),
    Character("Воин", health=120, attack_power=20, character_class="warrior"),
    Character("Лучник", health=60, attack_power=18, character_class="archer")
]

print(f"\n3. Выбор цели с приоритетной стратегией:")
selected_target = entity.select_combat_target(targets, environment)
if selected_target:
    attack_type = entity.choose_attack(selected_target, environment)
    print(f"   Выбрана цель: {selected_target.name} ({selected_target.character_class})")
    print(f"   Тип атаки: {attack_type}")

# Меняем стратегию на защитную
entity.set_combat_strategy(defensive_combat)
print(f"\n4. Выбор цели с защитной стратегией:")
selected_target = entity.select_combat_target(targets, environment)
if selected_target:
    attack_type = entity.choose_attack(selected_target, environment)
    print(f"   Выбрана цель: {selected_target.name} ({selected_target.character_class})")
    print(f"   Тип атаки: {attack_type}")

# Меняем стратегию перемещения
entity.set_movement_strategy(avoidance_move)
entity.position = (2, 2)
print(f"\n5. Перемещение с избеганием препятствий:")
for i in range(3):
    result = entity.move_to((8, 8), environment)
    print(f"   {result}")
```

### Задача 4: Асинхронная стратегия для игровых действий (20 баллов)
Реализуйте асинхронные стратегии:
- Использование asyncio для асинхронного выполнения стратегий
- Классы `AsyncStrategy` и `AsyncContext`
- Обработка действий в отдельных задачах

```python
import asyncio

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


# Запуск асинхронной демонстрации
# asyncio.run(async_strategy_demo())
```

### Задача 5: Практическое применение Strategy в игровой системе (20 баллов)
Создайте комплексную систему, где стратегии применяются для:
- Системы развития персонажа
- Системы торговли
- Системы квестов
- Контекста `GameSystem`

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

class TradingStrategy(ABC):
    """
    Стратегия торговли
    """
    @abstractmethod
    def execute_trade(self, trader, customer, item, price):
        """
        Выполнить торговую операцию
        """
        pass

class QuestStrategy(ABC):
    """
    Стратегия выполнения квестов
    """
    @abstractmethod
    def assign_quest(self, player, quest):
        """
        Назначить квест игроку
        """
        pass

    @abstractmethod
    def evaluate_quest_completion(self, player, quest, environment=None):
        """
        Оценить выполнение квеста
        """
        pass

class GameSystem:
    """
    Игровая система как контекст для различных стратегий
    """
    def __init__(self, name: str):
        self.name = name
        self._dev_strategy: CharacterDevelopmentStrategy = None
        self._trading_strategy: TradingStrategy = None
        self._quest_strategy: QuestStrategy = None

    def set_development_strategy(self, strategy: CharacterDevelopmentStrategy):
        self._dev_strategy = strategy

    def set_trading_strategy(self, strategy: TradingStrategy):
        self._trading_strategy = strategy

    def set_quest_strategy(self, strategy: QuestStrategy):
        self._quest_strategy = strategy

    def develop_character(self, character, experience_points: int):
        if self._dev_strategy:
            return self._dev_strategy.develop_character(character, experience_points)
        else:
            return f"Невозможно развить {character.name} - нет стратегии развития"

    def execute_trade(self, trader, customer, item, price):
        if self._trading_strategy:
            return self._trading_strategy.execute_trade(trader, customer, item, price)
        else:
            return f"Невозможно выполнить торговлю - нет стратегии торговли"

    def assign_quest(self, player, quest):
        if self._quest_strategy:
            return self._quest_strategy.assign_quest(player, quest)
        else:
            return f"Невозможно назначить квест - нет стратегии квестов"

    def evaluate_quest_completion(self, player, quest, environment=None):
        if self._quest_strategy:
            return self._quest_strategy.evaluate_quest_completion(player, quest, environment)
        else:
            return f"Невозможно оценить выполнение квеста - нет стратегии квестов"


class SkillPointDevelopmentStrategy(CharacterDevelopmentStrategy):
    """
    Стратегия развития через распределение очков навыков
    """
    def develop_character(self, character, experience_points: int):
        # При получении опыта начисляем очки развития
        skill_points_gained = experience_points // 100  # 1 очко за каждые 100 опыта
        if skill_points_gained > 0:
            if not hasattr(character, 'skill_points'):
                character.skill_points = 0
            character.skill_points += skill_points_gained

            # Повышаем уровень
            levels_gained = experience_points // (character.level * 100)
            if levels_gained > 0:
                old_level = character.level
                character.level += levels_gained
                # Увеличиваем характеристики пропорционально новому уровню
                character.max_health += levels_gained * 20
                character.health = character.max_health  # Восстанавливаем здоровье
                character.attack_power += levels_gained * 3
                character.defense += levels_gained * 1

            return f"{character.name} получил {skill_points_gained} очков навыков и повысил уровень с {old_level} до {character.level}"
        else:
            return f"{character.name} получил {experience_points} опыта, но недостаточно для развития"


class EconomicTradingStrategy(TradingStrategy):
    """
    Экономическая стратегия торговли - цены зависят от спроса и предложения
    """
    def __init__(self):
        self.price_modifiers = {}  # Модификаторы цен для разных товаров в разных регионах

    def execute_trade(self, trader, customer, item, base_price):
        # Рассчитываем модификатор цены на основе спроса/предложения
        region = getattr(customer, 'region', 'default')
        item_type = getattr(item, 'item_type', 'unknown')

        # Получаем модификатор цены для региона и типа товара
        region_modifiers = self.price_modifiers.get(region, {})
        price_modifier = region_modifiers.get(item_type, 1.0)

        # Рассчитываем итоговую цену
        final_price = int(base_price * price_modifier)

        # Проверяем, может ли покупатель позволить себе товар
        if hasattr(customer, 'gold') and customer.gold >= final_price:
            customer.gold -= final_price
            if hasattr(trader, 'gold'):
                trader.gold += final_price

            # Добавляем товар покупателю
            if not hasattr(customer, 'inventory'):
                customer.inventory = []
            customer.inventory.append(item)

            return f"{customer.name} купил {item.name} за {final_price} золота (модификатор: {price_modifier:.2f})"
        else:
            return f"{customer.name} не может позволить себе {item.name} за {final_price} золота"


class AdaptiveQuestStrategy(QuestStrategy):
    """
    Адаптивная стратегия квестов - сложность зависит от уровня игрока
    """
    def assign_quest(self, player, quest):
        # Адаптируем квест к уровню игрока
        level_difference = player.level - quest.base_level
        if level_difference > 2:
            # Если игрок намного выше уровня квеста, увеличиваем награду
            quest.xp_reward = int(quest.xp_reward * (1 + level_difference * 0.2))
            quest.gold_reward = int(quest.gold_reward * (1 + level_difference * 0.15))
        elif level_difference < -2:
            # Если игрок намного ниже уровня квеста, снижаем сложность
            quest.goal = max(1, int(quest.goal * (1 - abs(level_difference) * 0.1)))

        return f"Квест '{quest.title}' назначен {player.name} (адаптирован к уровню {player.level})"

    def evaluate_quest_completion(self, player, quest, environment=None):
        # Проверяем выполнение квеста с учетом прогресса игрока
        if hasattr(player, 'quest_progress') and quest.title in player.quest_progress:
            progress = player.quest_progress[quest.title]
            if progress >= quest.goal:
                # Выдать награду
                if hasattr(player, 'gain_experience'):
                    player.gain_experience(quest.xp_reward)
                if hasattr(player, 'gold'):
                    player.gold += quest.gold_reward

                return f"Квест '{quest.title}' завершен! Награда: {quest.xp_reward} XP, {quest.gold_reward} золота"
            else:
                return f"Квест '{quest.title}' в процессе: {progress}/{quest.goal}"
        else:
            return f"Прогресс по квесту '{quest.title}' не найден"


# Пример использования комплексной системы
print("\n=== Демонстрация комплексной системы стратегий ===\n")

# Создаем игровую систему
game_system = GameSystem("Основная игровая система")

# Создаем стратегии
skill_dev_strategy = SkillPointDevelopmentStrategy()
economic_trading = EconomicTradingStrategy()
adaptive_quests = AdaptiveQuestStrategy()

# Устанавливаем стратегии в систему
game_system.set_development_strategy(skill_dev_strategy)
game_system.set_trading_strategy(economic_trading)
game_system.set_quest_strategy(adaptive_quests)

# Создаем игрока и другие объекты
player = Character("Артур", health=100, attack_power=20, defense=5, character_class="warrior")
player.level = 3  # Устанавливаем уровень вручную для демонстрации

# Квест для демонстрации
class Quest:
    def __init__(self, title, base_level, xp_reward, gold_reward, goal=10):
        self.title = title
        self.base_level = base_level
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.goal = goal

quest = Quest("Убить гоблинов", base_level=2, xp_reward=150, gold_reward=100, goal=5)

# Торговый товар
class Item:
    def __init__(self, name, item_type, base_value):
        self.name = name
        self.item_type = item_type
        self.base_value = base_value

sword = Item("Меч героя", "weapon", 200)

# Демонстрация стратегии развития
print("1. Развитие персонажа:")
result = game_system.develop_character(player, 350)  # 350 опыта
print(f"   {result}")
print(f"   Статистика после развития: Уровень {player.level}, Очки навыков: {getattr(player, 'skill_points', 0)}")

# Демонстрация торговли
player.gold = 500  # Даем игроку золото для покупки
print(f"\n2. Торговля:")
result = game_system.execute_trade(Character("Торговец", health=50), player, sword, 200)
print(f"   {result}")
print(f"   Золото игрока после покупки: {player.gold}")

# Демонстрация квестов
if not hasattr(player, 'quest_progress'):
    player.quest_progress = {}
player.quest_progress[quest.title] = 3  # Устанавливаем прогресс квеста

print(f"\n3. Назначение квеста:")
result = game_system.assign_quest(player, quest)
print(f"   {result}")

print(f"\n4. Оценка выполнения квеста:")
result = game_system.evaluate_quest_completion(player, quest)
print(f"   {result}")

# Обновляем прогресс и снова проверяем
player.quest_progress[quest.title] = 5  # Завершаем квест
result = game_system.evaluate_quest_completion(player, quest)
print(f"   {result} (после завершения)")
print(f"   Золото игрока после награды: {player.gold}")
```

## Методические указания
1. Используйте абстрактные классы для определения интерфейсов стратегий
2. Обеспечьте гибкость системы через параметры стратегий и возможность динамической замены
3. Обрабатывайте ошибки при выполнении стратегий, чтобы одна неудачная стратегия не повлияла на всю систему
4. Рассмотрите асинхронные подходы для сложных или длительных операций
5. Используйте enum для типов стратегий, чтобы избежать опечаток в строках

## Требования к отчету
- Исходный код всех реализаций Strategy с игровой тематикой
- Примеры использования каждой стратегии в игровом контексте
- Сравнение синхронных и асинхронных реализаций и их применимость в игровых приложениях

## Критерии оценки
- Корректная реализация паттерна Strategy в игровом контексте: 50%
- Понимание различных вариантов применения в игровой разработке: 30%
- Качество кода и документация в игровом контексте: 20%

## Практические задания

### Задание 1: Система боевых тактик

Создайте систему боевых тактик, где каждый персонаж может использовать разные тактики в зависимости от ситуации: `AmbushTactic`, `SiegeTactic`, `GuerrillaTactic`, `FormationTactic`. Каждая тактика должна по-разному влиять на боевые действия персонажа.

```python
class CombatTactic(ABC):
    """
    Абстрактная боевая тактика
    """
    @abstractmethod
    def apply_tactic(self, character, allies, enemies, environment=None):
        """
        Применить тактику в бою
        """
        pass

    @abstractmethod
    def calculate_damage_modifier(self, attacker, target, environment=None):
        """
        Рассчитать модификатор урона для этой тактики
        """
        pass

class AmbushTactic(CombatTactic):
    """
    Тактика засады - увеличивает урон при нападении с выгодной позиции
    """
    def apply_tactic(self, character, allies, enemies, environment=None):
        advantage = environment.get("ambush_advantage", 0) if environment else 0
        if advantage > 0:
            # Увеличиваем урон при наличии преимущества
            bonus_damage = character.attack_power * 0.5 * advantage  # 50% бонуса за каждое преимущество
            return f"{character.name} использует тактику засады и получает {bonus_damage} бонусного урона"
        else:
            return f"{character.name} не может эффективно использовать тактику засады в этой местности"

    def calculate_damage_modifier(self, attacker, target, environment=None):
        advantage = environment.get("ambush_advantage", 0) if environment else 0
        return 1.0 + (0.5 * advantage)  # 50% бонуса за каждое преимущество


class SiegeTactic(CombatTactic):
    """
    Тактика осады - эффективна против укрепленных позиций
    """
    def apply_tactic(self, character, allies, enemies, environment=None):
        siege_equipment = environment.get("siege_equipment", 0) if environment else 0
        if siege_equipment > 0:
            # Увеличиваем эффективность против укреплений
            return f"{character.name} использует осадное оборудование для эффективной атаки"
        else:
            return f"{character.name} ограничен в применении осадной тактики без оборудования"

    def calculate_damage_modifier(self, attacker, target, environment=None):
        # Повышает эффективность против целей с высокой защитой
        target_defense = getattr(target, 'defense', 0)
        if target_defense > 10:  # Если у цели высокая защита
            return 1.0 + (target_defense * 0.05)  # 5% бонуса за каждую единицу защиты цели
        return 1.0


class GuerrillaTactic(CombatTactic):
    """
    Тактика партизанской войны - фокус на мобильность и внезапность
    """
    def apply_tactic(self, character, allies, enemies, environment=None):
        mobility_advantage = environment.get("mobility_advantage", 0) if environment else 0
        if mobility_advantage > 0:
            # Повышает шанс уклонения и критического удара
            return f"{character.name} использует мобильность для уклонения и контратак"
        else:
            return f"{character.name} не может эффективно использовать мобильность в этой местности"

    def calculate_damage_modifier(self, attacker, target, environment=None):
        # Увеличивает урон при высокой мобильности
        return 1.0 + (0.3 if hasattr(attacker, 'speed') and attacker.speed > 5 else 0.0)


class FormationTactic(CombatTactic):
    """
    Тактика построения - усиливает командную эффективность
    """
    def apply_tactic(self, character, allies, enemies, environment=None):
        ally_count = len([a for a in allies if a.is_alive]) if allies else 1
        if ally_count > 1:
            # Усиление от соседей по построению
            formation_bonus = min(0.5, (ally_count - 1) * 0.1)  # Максимум 50% бонуса
            return f"{character.name} получает бонус {formation_bonus*100:.1f}% от построения с {ally_count} союзниками"
        else:
            return f"{character.name} не может получить выгоду от построения в одиночку"

    def calculate_damage_modifier(self, attacker, target, environment=None):
        ally_count = len([a for a in [attacker] + getattr(attacker, 'allies', []) if a.is_alive]) - 1
        formation_bonus = min(0.5, ally_count * 0.1)  # Максимум 50% бонуса
        return 1.0 + formation_bonus


class TacticCharacter(Character):
    """
    Персонаж, способный использовать боевые тактики
    """
    def __init__(self, name: str, health: int = 100, attack_power: int = 20, defense: int = 5, character_class: str = "warrior"):
        super().__init__(name, health, attack_power, defense, character_class)
        self._combat_tactic: CombatTactic = None

    def set_combat_tactic(self, tactic: CombatTactic):
        """Установить боевую тактику"""
        self._combat_tactic = tactic

    def perform_attack_with_tactic(self, target, environment=None, allies=None):
        """Выполнить атаку с учетом тактики"""
        if self._combat_tactic and self.is_alive and target.is_alive:
            # Применяем тактику
            tactic_result = self._combat_tactic.apply_tactic(self, allies or [], [target], environment)
            print(f"   {tactic_result}")

            # Рассчитываем модифицированный урон
            damage_modifier = self._combat_tactic.calculate_damage_modifier(self, target, environment)
            modified_damage = int(self.attack_power * damage_modifier)
            actual_damage = target.take_damage(modified_damage)

            return f"{self.name} атакует {target.name} с модифицированным уроном {actual_damage} (модификатор: {damage_modifier:.2f})"
        else:
            return f"{self.name} не может атаковать с тактикой"


# Пример использования системы боевых тактик
print("\n=== Система боевых тактик ===\n")

# Создаем персонажей
warrior = TacticCharacter("Рыцарь", health=120, attack_power=25, defense=8, character_class="warrior")
archer = TacticCharacter("Лучник", health=80, attack_power=30, defense=3, character_class="archer")
enemy = Character("Враг", health=100, attack_power=20, defense=5, character_class="warrior")

# Устанавливаем разные тактики
warrior.set_combat_tactic(FormationTactic())
archer.set_combat_tactic(AmbushTactic())

print(f"Персонажи: {warrior.name} и {archer.name} против {enemy.name}\n")

# Боевая симуляция с разными условиями
environments = [
    {"name": "Открытое поле", "ambush_advantage": 0, "mobility_advantage": 1},
    {"name": "Лесная засада", "ambush_advantage": 2, "mobility_advantage": 0},
    {"name": "Укрепленная позиция", "ambush_advantage": 0, "mobility_advantage": 0}
]

for env in environments:
    print(f"Бой в '{env['name']}':")
    print(f"  {warrior.perform_attack_with_tactic(enemy, environment=env, allies=[archer])}")
    print(f"  {archer.perform_attack_with_tactic(enemy, environment=env, allies=[warrior])}")
    print(f"  Состояние: {enemy.get_info()}\n")
    # Восстанавливаем здоровье врага для следующего раунда
    enemy.health = 100
```

### Задание 2: Система искусственного интеллекта

Создайте систему ИИ, где разные стратегии управления ИИ применяются к различным типам врагов: `PatrolAI`, `HuntAI`, `FleeAI`, `SupportAI`.

```python
class AIBehavior(ABC):
    """
    Абстрактное поведение ИИ
    """
    @abstractmethod
    def act(self, entity, environment=None, targets=None):
        """
        Выполнить действие ИИ
        """
        pass

    @abstractmethod
    def should_change_behavior(self, entity, environment=None, targets=None):
        """
        Проверить, нужно ли изменить поведение
        """
        pass

class PatrolAI(AIBehavior):
    """
    ИИ патрулирования - движение между точками
    """
    def __init__(self, patrol_points=None):
        self.patrol_points = patrol_points or [(0, 0), (5, 5), (10, 0), (5, -5)]
        self.current_patrol_index = 0

    def act(self, entity, environment=None, targets=None):
        # Перемещаемся к следующей точке патрулирования
        target_point = self.patrol_points[self.current_patrol_index]
        entity.position = target_point  # В реальной игре здесь была бы постепенная анимация движения

        # Переходим к следующей точке
        self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)

        return f"{entity.name} патрулирует точку {target_point}"

    def should_change_behavior(self, entity, environment=None, targets=None):
        # Меняем поведение, если видим врага
        visible_targets = targets or []
        return len(visible_targets) > 0  # Если есть цели, переходим к атаке


class HuntAI(AIBehavior):
    """
    ИИ охоты - активный поиск и преследование цели
    """
    def __init__(self, aggression_level=0.8):
        self.aggression_level = aggression_level
        self.current_target = None

    def act(self, entity, environment=None, targets=None):
        if targets:
            # Выбираем ближайшую цель
            self.current_target = min(targets, key=lambda t: ((entity.position[0] - t.position[0])**2 + (entity.position[1] - t.position[1])**2)**0.5)
            # Имитация преследования
            entity.position = self.current_target.position  # В реальной игре было бы постепенное приближение

            return f"{entity.name} преследует {self.current_target.name}"
        else:
            return f"{entity.name} ищет цели для охоты"

    def should_change_behavior(self, entity, environment=None, targets=None):
        # Меняем поведение, если здоровье низкое
        if hasattr(entity, 'health') and hasattr(entity, 'max_health'):
            return entity.health < entity.max_health * (1 - self.aggression_level)
        return False  # Не меняем, если нет информации о здоровье


class FleeAI(AIBehavior):
    """
    ИИ бегства - избегание конфликта при низком здоровье
    """
    def act(self, entity, environment=None, targets=None):
        # Находим безопасное место (противоположное от врагов)
        if targets:
            avg_target_x = sum(getattr(t, 'position', (0, 0))[0] for t in targets) / len(targets)
            avg_target_y = sum(getattr(t, 'position', (0, 0))[1] for t in targets) / len(targets)

            # Двигаемся в противоположном направлении
            flee_x = entity.position[0] - (avg_target_x - entity.position[0])
            flee_y = entity.position[1] - (avg_target_y - entity.position[1])

            entity.position = (flee_x, flee_y)
            return f"{entity.name} бежит в безопасное место ({flee_x:.1f}, {flee_y:.1f})"
        else:
            return f"{entity.name} ищет безопасное место"

    def should_change_behavior(self, entity, environment=None, targets=None):
        # Меняем поведение, если здоровье восстановилось
        if hasattr(entity, 'health') and hasattr(entity, 'max_health'):
            return entity.health > entity.max_health * 0.7
        return False


class SupportAI(AIBehavior):
    """
    ИИ поддержки - помощь союзникам
    """
    def act(self, entity, environment=None, targets=None):
        allies = environment.get("allies", []) if environment else []
        injured_allies = [ally for ally in allies if hasattr(ally, 'health') and ally.health < ally.max_health * 0.8]

        if injured_allies:
            # Выбираем самого тяжело раненого союзника
            target_ally = min(injured_allies, key=lambda a: a.health / a.max_health)
            # Имитация лечения или поддержки
            heal_amount = 10
            old_health = target_ally.health
            target_ally.health = min(target_ally.max_health, target_ally.health + heal_amount)
            actual_heal = target_ally.health - old_health

            return f"{entity.name} лечит {target_ally.name} на {actual_heal} здоровья"
        else:
            return f"{entity.name} охраняет союзников"


    def should_change_behavior(self, entity, environment=None, targets=None):
        # Меняем поведение, если нужно сбежать
        if hasattr(entity, 'health') and hasattr(entity, 'max_health'):
            return entity.health < entity.max_health * 0.3
        return False


class AIEntity(GameEntity):
    """
    Сущность с ИИ
    """
    def __init__(self, name: str, position=(0, 0), resources: dict = None):
        super().__init__(name, position, resources)
        self._ai_behavior: AIBehavior = None

    def set_ai_behavior(self, behavior: AIBehavior):
        """Установить поведение ИИ"""
        self._ai_behavior = behavior

    def act(self, environment=None, targets=None):
        """Выполнить действие ИИ"""
        if self._ai_behavior:
            # Проверяем, нужно ли изменить поведение
            if self._ai_behavior.should_change_behavior(self, environment, targets):
                # В реальной игре здесь могла бы быть логика смены поведения
                # Для примера просто сообщим об этом
                print(f"  {self.name} меняет поведение из-за изменений условий")
                # Здесь можно установить новое поведение в зависимости от условий

            return self._ai_behavior.act(self, environment, targets)
        else:
            return f"{self.name} не имеет установленного поведения ИИ"


# Пример использования системы ИИ
print("\n=== Система искусственного интеллекта ===\n")

# Создаем сущности
guard = AIEntity("Стражник", position=(0, 0), resources={"health": 100})
hunter = AIEntity("Охотник", position=(10, 10), resources={"health": 80})
healer = AIEntity("Лекарь", position=(5, 5), resources={"health": 60})

# Создаем цели (враги)
enemies = [GameEntity("Гоблин", position=(12, 12)), GameEntity("Тролль", position=(8, 8))]

# Устанавливаем поведения
guard.set_ai_behavior(PatrolAI(patrol_points=[(0, 0), (5, 0), (5, 5), (0, 5)]))
hunter.set_ai_behavior(HuntAI(aggression_level=0.9))
healer.set_ai_behavior(SupportAI())

entities = [guard, hunter, healer]

print("Исходные позиции:")
for entity in entities:
    print(f"  {entity.name} в {entity.position}")

print(f"\nСимуляция действий ИИ:")
for entity in entities:
    environment = {"allies": [e for e in entities if e != entity]}
    action_result = entity.act(environment=environment, targets=enemies)
    print(f"  {action_result}")

print(f"\nНовые позиции:")
for entity in entities:
    print(f"  {entity.name} в {entity.position}")
```

### Задача 3: Сравнение различных реализаций Strategy

Создайте таблицу сравнения различных типов стратегий (обычная, параметризованная, асинхронная) по критериям: сложность реализации, производительность, гибкость, применимость в игровой разработке. Приведите примеры, когда каждый тип стратегии наиболее эффективен в игровом контексте.

```python
def compare_strategies():
    """
    Сравнение различных типов стратегий
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

## Дополнительные задания

### Задание 4: Интеграция с другими паттернами

Создайте пример интеграции паттерна Strategy с другими паттернами (например, Observer, Factory), чтобы создать более сложную и гибкую игровую систему.

### Задание 5: Система модификаций

Реализуйте систему модификаций предметов, где разные стратегии модификаций применяются к различным типам предметов (оружие, броня, зелья и т.д.).

## Контрольные вопросы:
1. В чем разница между паттернами Strategy и State в игровом контексте?
2. Как обеспечить потокобезопасность стратегий в многопоточной игровой среде?
3. Какие преимущества дает использование Strategy в системах боевой тактики?
4. Как обрабатывать ошибки в стратегиях, чтобы не прерывать выполнение других компонентов?
5. Как использовать Strategy для создания адаптивного ИИ в играх?