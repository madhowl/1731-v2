"""
Пример: Паттерн Strategy в игровых персонажах
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class CharacterClass(Enum):
    """Классы персонажей"""
    WARRIOR = "Воин"
    MAGE = "Маг"
    ARCHER = "Лучник"
    HEALER = "Целитель"
    ROGUE = "Разбойник"

class BattleStrategy(ABC):
    """Абстрактная стратегия боя"""
    @abstractmethod
    def execute_turn(self, character, enemies: List, allies: List) -> str:
        """Выполнить ход персонажа"""
        pass

class AggressiveBattleStrategy(BattleStrategy):
    """Агрессивная стратегия боя - всегда атакует"""
    def execute_turn(self, character, enemies: List, allies: List) -> str:
        if enemies:
            target = enemies[0]  # Атакуем первого врага
            damage = character.attack_power + character.strength
            target.take_damage(damage)
            return f"{character.name} атакует {target.name} на {damage} урона (агрессивно)"
        return f"{character.name} оглядывается в поисках врагов..."

class DefensiveBattleStrategy(BattleStrategy):
    """Защитная стратегия боя - сосредоточена на выживании"""
    def execute_turn(self, character, enemies: List, allies: List) -> str:
        if character.health < character.max_health * 0.5:
            # Если здоровье меньше половины, лечимся
            heal_amount = min(character.max_health - character.health, 20)
            character.health += heal_amount
            return f"{character.name} восстанавливает {heal_amount} здоровья (оборонительно)"
        elif enemies:
            # Иначе атакуем, но с осторожностью
            target = min(enemies, key=lambda e: e.health)  # Атакуем самого слабого врага
            damage = character.attack_power
            target.take_damage(damage)
            return f"{character.name} атакует {target.name} на {damage} урона (осторожно)"
        return f"{character.name} защищается..."

class SupportBattleStrategy(BattleStrategy):
    """Поддерживающая стратегия боя - помогает союзникам"""
    def execute_turn(self, character, enemies: List, allies: List) -> str:
        # Ищем союзника с минимальным здоровьем
        injured_ally = None
        for ally in allies:
            if ally != character and ally.health < ally.max_health * 0.7:
                if injured_ally is None or ally.health < injured_ally.health:
                    injured_ally = ally

        if injured_ally:
            # Лечим союзника
            heal_amount = min(injured_ally.max_health - injured_ally.health, 25)
            injured_ally.health += heal_amount
            return f"{character.name} лечит {injured_ally.name} на {heal_amount} здоровья (поддержка)"
        elif enemies:
            # Если некого лечить, атакуем
            target = enemies[0]
            damage = character.attack_power // 2 # Половина обычного урона
            target.take_damage(damage)
            return f"{character.name} слабо атакует {target.name} на {damage} урона (фокус на поддержку)"
        return f"{character.name} оценивает ситуацию..."

class Character:
    """Игровой персонаж с возможностью изменения стратегии боя"""
    def __init__(self, name: str, char_class: CharacterClass, health: int = 100):
        self.name = name
        self.char_class = char_class
        self.max_health = health
        self.health = health
        self.attack_power = 10
        self.defense = 5
        self.strength = 15
        self.intelligence = 10
        self.dexterity = 12
        self.level = 1
        self.experience = 0

        # Начальная стратегия боя зависит от класса
        self.battle_strategy = self._get_default_strategy()

    def _get_default_strategy(self) -> BattleStrategy:
        """Получить стратегию по умолчанию для класса персонажа"""
        if self.char_class == CharacterClass.WARRIOR:
            return AggressiveBattleStrategy()
        elif self.char_class == CharacterClass.MAGE:
            return AggressiveBattleStrategy()  # Маги тоже агрессивны в бою
        elif self.char_class == CharacterClass.HEALER:
            return SupportBattleStrategy()
        else:
            return AggressiveBattleStrategy()

    def set_battle_strategy(self, strategy: BattleStrategy):
        """Установить стратегию боя"""
        self.battle_strategy = strategy

    def perform_battle_action(self, enemies: List, allies: List) -> str:
        """Выполнить боевое действие в соответствии со стратегией"""
        return self.battle_strategy.execute_turn(self, enemies, allies)

    def take_damage(self, damage: int):
        """Получить урон с учетом защиты"""
        actual_damage = max(1, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage

    def is_alive(self) -> bool:
        """Проверить, жив ли персонаж"""
        return self.health > 0

    def gain_experience(self, exp: int):
        """Получить опыт и возможно повысить уровень"""
        self.experience += exp
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level_up()

    def level_up(self):
        """Повысить уровень персонажа"""
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 3
        self.defense += 2
        self.strength += 2
        self.experience = 0
        print(f"{self.name} достиг {self.level} уровня!")

    def __str__(self):
        return f"{self.name} ({self.char_class.value}): Уровень {self.level}, Здоровье {self.health}/{self.max_health}"

class Enemy:
    """Класс врага для демонстрации"""
    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power

    def take_damage(self, damage: int):
        """Получить урон"""
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        """Проверить, жив ли враг"""
        return self.health > 0

class BattleSystem:
    """Система боя для демонстрации стратегий"""
    def __init__(self):
        self.turn = 0

    def battle_round(self, party: List[Character], enemies: List[Enemy]):
        """Выполнить раунд боя"""
        print(f"\n--- Раунд {self.turn + 1} ---")
        self.turn += 1

        # Ход союзников
        for character in party:
            if character.is_alive() and any(e.is_alive() for e in enemies):
                action_result = character.perform_battle_action(
                    [e for e in enemies if e.is_alive()],  # Живые враги
                    [c for c in party if c.is_alive()]    # Живые союзники
                )
                print(action_result)

        # Ход врагов (упрощенно)
        for enemy in enemies:
            if enemy.is_alive() and any(c.is_alive() for c in party):
                # Враг атакует случайного живого персонажа
                alive_characters = [c for c in party if c.is_alive()]
                if alive_characters:
                    target = alive_characters[0]  # Упрощенно - атакуем первого
                    damage = enemy.attack_power
                    actual_damage = target.take_damage(damage)
                    print(f"{enemy.name} атакует {target.name} на {actual_damage} урона")

        # Выводим текущее состояние
        print("\nСостояние после раунда:")
        for character in party:
            if character.is_alive():
                print(f"  {character}")
        for enemy in enemies:
            if enemy.is_alive():
                print(f"  {enemy.name}: {enemy.health}/{enemy.max_health} здоровья")

    def is_battle_over(self, party: List[Character], enemies: List[Enemy]) -> bool:
        """Проверить, закончилась ли битва"""
        party_alive = any(c.is_alive() for c in party)
        enemies_alive = any(e.is_alive() for e in enemies)
        return not party_alive or not enemies_alive

    def get_battle_result(self, party: List[Character], enemies: List[Enemy]) -> str:
        """Получить результат битвы"""
        party_alive = any(c.is_alive() for c in party)
        enemies_alive = any(e.is_alive() for e in enemies)
        if party_alive and not enemies_alive:
            return "Победа!"
        elif not party_alive and enemies_alive:
            return "Поражение!"
        else:
            return "Ничья!"

def demonstrate_strategy_pattern():
    """Демонстрация паттерна Strategy в игровом контексте"""
    print("=== Демонстрация паттерна Strategy в игровом контексте ===\n")

    # Создаем персонажей
    warrior = Character("Конан", CharacterClass.WARRIOR, health=150)
    mage = Character("Мерлин", CharacterClass.MAGE, health=80)
    healer = Character("Эльза", CharacterClass.HEALER, health=90)

    party = [warrior, mage, healer]

    # Создаем врагов
    goblins = [Enemy("Гоблин 1", 40, 8), Enemy("Гоблин 2", 40, 8)]

    # Создаем боевую систему
    battle_system = BattleSystem()

    print("Начальное состояние:")
    for character in party:
        print(f"  {character}")

    print(f"\nВраги: {len(goblins)} гоблинов по 40 здоровья")

    # Проводим несколько раундов боя с разными стратегиями
    print("\n1. Бой с начальными стратегиями:")

    # Покажем текущие стратегии
    print(f" {warrior.name} использует агрессивную стратегию (по умолчанию для воина)")
    print(f"  {mage.name} использует агрессивную стратегию (по умолчанию для мага)")
    print(f"  {healer.name} использует поддерживающую стратегию (по умолчанию для целителя)")

    for round_num in range(3):
        battle_system.battle_round(party, goblins)
        if battle_system.is_battle_over(party, goblins):
            break

    # Меняем стратегии для следующей фазы боя
    print(f"\n2. Меняем стратегии и продолжаем бой:")
    warrior.set_battle_strategy(DefensiveBattleStrategy())  # Воин становится осторожным
    mage.set_battle_strategy(AggressiveBattleStrategy())   # Маг остается агрессивным
    healer.set_battle_strategy(SupportBattleStrategy())    # Целитель продолжает поддерживать

    print(f"  {warrior.name} теперь использует защитную стратегию")
    print(f"  {mage.name} продолжает использовать агрессивную стратегию")
    print(f"  {healer.name} продолжает использовать поддерживающую стратегию")

    # Продолжаем бой
    while not battle_system.is_battle_over(party, goblins) and battle_system.turn < 6:
        battle_system.battle_round(party, goblins)

    # Выводим результат
    print(f"\nРезультат битвы: {battle_system.get_battle_result(party, goblins)}")
    print("\nФинальное состояние персонажей:")
    for character in party:
        if character.is_alive():
            print(f"  {character}")

    # Раздаем опыт выжившим персонажам
    if battle_system.get_battle_result(party, goblins) == "Победа!":
        for character in party:
            if character.is_alive():
                character.gain_experience(50)
                print(f"  {character.name} получает 50 опыта")


if __name__ == "__main__":
    demonstrate_strategy_pattern()