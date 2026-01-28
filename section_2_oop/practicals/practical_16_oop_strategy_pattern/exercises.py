"""
Практическое задание 16: Паттерн Strategy в игровом контексте

Цель: Реализовать паттерн Strategy для выбора алгоритмов во время выполнения программы в игровом контексте.
"""

from abc import ABC, abstractmethod

# Уровень 1 - Начальный
# Задание 1.1: Создать базовую реализацию Strategy для боевых действий

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
        self._battle_strategy = None  # Текущая боевая стратегия

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = max(0, min(self.max_health, value))
        if self._health <= 0:
            self._health = 0
            self.is_alive = False

    def set_battle_strategy(self, strategy):
        """Установить боевую стратегию"""
        # TODO: Реализуйте установку боевой стратегии
        pass

    def perform_attack(self, target, environment=None):
        """Выполнить атаку с использованием текущей стратегии"""
        # TODO: Реализуйте выполнение атаки с использованием текущей стратегии
        pass

    def perform_defense(self, incoming_damage, environment=None):
        """Выполнить защиту с использованием текущей стратегии"""
        # TODO: Реализуйте выполнение защиты с использованием текущей стратегии
        pass

    def get_info(self):
        """Получить информацию о персонаже"""
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({self.character_class}, {status}): Lvl.{self.level}, HP {self.health}/{self.max_health}, ATK {self.attack_power}, DEF {self.defense}"

    def take_damage(self, damage: int):
        """Получить урон"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage


class AggressiveStrategy:
    """
    Агрессивная боевая стратегия - наносит максимальный урон, но плохо защищается
    """
    # TODO: Реализуйте класс с методами execute_attack и execute_defense
    pass


class DefensiveStrategy:
    """
    Защитная боевая стратегия - фокусируется на защите, наносит меньше урона
    """
    # TODO: Реализуйте класс с методами execute_attack и execute_defense
    pass


class BalancedStrategy:
    """
    Сбалансированная боевая стратегия - средний урон и средняя защита
    """
    # TODO: Реализуйте класс с методами execute_attack и execute_defense
    pass


# Уровень 2 - Средний
# Задание 2.1: Реализовать систему поведения врагов с использованием различных стратегий

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
        self._ai_strategy = None

    def set_ai_strategy(self, strategy):
        """Установить стратегию ИИ"""
        # TODO: Реализуйте установку стратегии ИИ
        pass

    def take_turn(self, player, environment=None):
        """Сделать ход в бою"""
        # TODO: Реализуйте выполнение хода в бою с использованием стратегии ИИ
        pass

    def evaluate_player_threat(self, player, environment=None):
        """Оценить угрозу от игрока с помощью стратегии ИИ"""
        # TODO: Реализуйте оценку угрозы от игрока
        pass

class AggressiveAI:
    """
    Агрессивный ИИ - всегда атакует, если может
    """
    # TODO: Реализуйте класс с методами decide_action и evaluate_threat
    pass

class DefensiveAI:
    """
    Защитный ИИ - фокусируется на выживании
    """
    # TODO: Реализуйте класс с методами decide_action и evaluate_threat
    pass

class RandomAI:
    """
    Случайный ИИ - выбирает случайное действие
    """
    # TODO: Реализуйте класс с методами decide_action и evaluate_threat
    pass

class TacticalAI:
    """
    Тактический ИИ - анализирует ситуацию и принимает обдуманные решения
    """
    # TODO: Реализуйте класс с методами decide_action и evaluate_threat
    pass


# Уровень 3 - Повышенный
# Задание 3.1: Реализовать систему с параметризованными стратегиями

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
        self._movement_strategy = None
        self._resource_strategy = None
        self._combat_strategy = None

    def set_movement_strategy(self, strategy):
        # TODO: Реализуйте установку стратегии перемещения
        pass

    def set_resource_strategy(self, strategy):
        # TODO: Реализуйте установку стратегии управления ресурсами
        pass

    def set_combat_strategy(self, strategy):
        # TODO: Реализуйте установку боевой тактики
        pass

    def move_to(self, target_position, environment=None):
        # TODO: Реализуйте перемещение с использованием стратегии
        pass

    def manage_resources(self, environment=None):
        # TODO: Реализуйте управление ресурсами с использованием стратегии
        pass

    def select_combat_target(self, possible_targets, environment=None):
        # TODO: Реализуйте выбор цели с использованием боевой тактики
        pass

    def choose_attack(self, target, environment=None):
        # TODO: Реализуйте выбор типа атаки с использованием боевой тактики
        pass


class DirectMovementStrategy:
    """
    Прямолинейное перемещение - движение по прямой к цели
    """
    # TODO: Реализуйте класс с методом move
    pass

class AvoidanceMovementStrategy:
    """
    Стратегия перемещения с избеганием препятствий
    """
    # TODO: Реализуйте класс с методом move
    pass

class ConservativeResourceStrategy:
    """
    Консервативная стратегия управления ресурсами - экономит ресурсы
    """
    # TODO: Реализуйте класс с методом manage_resources
    pass

class AggressiveResourceStrategy:
    """
    Агрессивная стратегия управления ресурсами - активно использует ресурсы
    """
    # TODO: Реализуйте класс с методом manage_resources
    pass

class PriorityTargetCombatStrategy:
    """
    Стратегия боевой тактики с приоритетами целей
    """
    # TODO: Реализуйте класс с методами select_target и choose_attack_type
    pass

class DefensiveCombatStrategy:
    """
    Защитная боевая стратегия - фокусируется на выживании
    """
    # TODO: Реализуйте класс с методами select_target и choose_attack_type
    pass


# Задание 3.2: Практическое применение Strategy в игровой системе

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
        self._dev_strategy = None
        self._trading_strategy = None
        self._quest_strategy = None

    def set_development_strategy(self, strategy):
        # TODO: Реализуйте установку стратегии развития
        pass

    def set_trading_strategy(self, strategy):
        # TODO: Реализуйте установку торговой стратегии
        pass

    def set_quest_strategy(self, strategy):
        # TODO: Реализуйте установку квестовой стратегии
        pass

    def develop_character(self, character, experience_points: int):
        # TODO: Реализуйте развитие персонажа с использованием стратегии
        pass

    def execute_trade(self, trader, customer, item, price):
        # TODO: Реализуйте выполнение торговли с использованием стратегии
        pass

    def assign_quest(self, player, quest):
        # TODO: Реализуйте назначение квеста с использованием стратегии
        pass

    def evaluate_quest_completion(self, player, quest, environment=None):
        # TODO: Реализуйте оценку выполнения квеста с использованием стратегии
        pass


class SkillPointDevelopmentStrategy:
    """
    Стратегия развития через распределение очков навыков
    """
    # TODO: Реализуйте класс с методом develop_character
    pass

class EconomicTradingStrategy:
    """
    Экономическая стратегия торговли - цены зависят от спроса и предложения
    """
    # TODO: Реализуйте класс с методом execute_trade
    pass

class AdaptiveQuestStrategy:
    """
    Адаптивная стратегия квестов - сложность зависит от уровня игрока
    """
    # TODO: Реализуйте класс с методами assign_quest и evaluate_quest_completion
    pass


# Тестирование реализации (раскомментируйте после реализации)
"""
# Тестирование уровня 1
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


# Тестирование уровня 2
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


# Тестирование уровня 3
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


# Тестирование уровня 3.2 - практическое применение
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
player.gold = 50  # Даем игроку золото для покупки
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
"""