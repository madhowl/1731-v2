"""
Пример: Паттерн Decorator в игровых персонажах
"""

from abc import ABC, abstractmethod

class CharacterComponent(ABC):
    """Абстрактный компонент персонажа"""
    @abstractmethod
    def get_attack_power(self) -> int:
        pass

    @abstractmethod
    def get_speed(self) -> float:
        pass

    @abstractmethod
    def get_defense(self) -> int:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

class BaseCharacter(CharacterComponent):
    """Базовый персонаж"""
    def __init__(self, name: str, base_attack: int = 10, base_speed: float = 1.0, base_defense: int = 5):
        self.name = name
        self.base_attack = base_attack
        self.base_speed = base_speed
        self.base_defense = base_defense

    def get_attack_power(self) -> int:
        return self.base_attack

    def get_speed(self) -> float:
        return self.base_speed

    def get_defense(self) -> int:
        return self.base_defense

    def get_description(self) -> str:
        return f"{self.name} (базовый)"

class CharacterDecorator(CharacterComponent):
    """Базовый декоратор персонажа"""
    def __init__(self, character: CharacterComponent):
        self._character = character

    def get_attack_power(self) -> int:
        return self._character.get_attack_power()

    def get_speed(self) -> float:
        return self._character.get_speed()

    def get_defense(self) -> int:
        return self._character.get_defense()

    def get_description(self) -> str:
        return self._character.get_description()

class StrengthPotionDecorator(CharacterDecorator):
    """Декоратор зелья силы"""
    def __init__(self, character: CharacterComponent, strength_boost: int = 5):
        super().__init__(character)
        self.strength_boost = strength_boost

    def get_attack_power(self) -> int:
        return self._character.get_attack_power() + self.strength_boost

    def get_description(self) -> str:
        return f"{self._character.get_description()} + Зелье Силы (+{self.strength_boost} к атаке)"

class SpeedPotionDecorator(CharacterDecorator):
    """Декоратор зелья скорости"""
    def __init__(self, character: CharacterComponent, speed_boost: float = 0.5):
        super().__init__(character)
        self.speed_boost = speed_boost

    def get_speed(self) -> float:
        return self._character.get_speed() + self.speed_boost

    def get_description(self) -> str:
        return f"{self._character.get_description()} + Зелье Скорости (+{self.speed_boost} к скорости)"

class DefensePotionDecorator(CharacterDecorator):
    """Декоратор зелья защиты"""
    def __init__(self, character: CharacterComponent, defense_boost: int = 3):
        super().__init__(character)
        self.defense_boost = defense_boost

    def get_defense(self) -> int:
        return self._character.get_defense() + self.defense_boost

    def get_description(self) -> str:
        return f"{self._character.get_description()} + Зелье Защиты (+{self.defense_boost} к защите)"

class FireResistanceDecorator(CharacterDecorator):
    """Декоратор огненного иммунитета"""
    def __init__(self, character: CharacterComponent, fire_resistance: int = 50):
        super().__init__(character)
        self.fire_resistance = fire_resistance

    def get_description(self) -> str:
        return f"{self._character.get_description()} + Огненный иммунитет (-{self.fire_resistance}% к огненному урону)"

    def get_fire_resistance(self) -> int:
        # Дополнительный метод для иммунитета к огню
        if hasattr(self._character, 'get_fire_resistance'):
            return self._character.get_fire_resistance() + self.fire_resistance
        return self.fire_resistance

class WeaponDecorator(CharacterDecorator):
    """Декоратор оружия"""
    def __init__(self, character: CharacterComponent, weapon_name: str, attack_bonus: int = 0, special_effect: str = ""):
        super().__init__(character)
        self.weapon_name = weapon_name
        self.attack_bonus = attack_bonus
        self.special_effect = special_effect

    def get_attack_power(self) -> int:
        return self._character.get_attack_power() + self.attack_bonus

    def get_description(self) -> str:
        desc = f"{self._character.get_description()} + {self.weapon_name}"
        if self.attack_bonus > 0:
            desc += f" (+{self.attack_bonus} к атаке)"
        if self.special_effect:
            desc += f" ({self.special_effect})"
        return desc

class ArmorDecorator(CharacterDecorator):
    """Декоратор брони"""
    def __init__(self, character: CharacterComponent, armor_name: str, defense_bonus: int = 0, special_property: str = ""):
        super().__init__(character)
        self.armor_name = armor_name
        self.defense_bonus = defense_bonus
        self.special_property = special_property

    def get_defense(self) -> int:
        return self._character.get_defense() + self.defense_bonus

    def get_description(self) -> str:
        desc = f"{self._character.get_description()} + {self.armor_name}"
        if self.defense_bonus > 0:
            desc += f" (+{self.defense_bonus} к защите)"
        if self.special_property:
            desc += f" ({self.special_property})"
        return desc

from enum import Enum

class EquipmentSlot(Enum):
    """Слоты экипировки"""
    WEAPON = "weapon"
    HELMET = "helmet"
    CHEST = "chest"
    LEGS = "legs"
    BOOTS = "boots"
    RING = "ring"
    AMULET = "amulet"

class EquipmentItem:
    """Предмет экипировки"""
    def __init__(self, name: str, slot: EquipmentSlot, attack_bonus: int = 0, defense_bonus: int = 0, speed_bonus: float = 0, special_effect: str = ""):
        self.name = name
        self.slot = slot
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.speed_bonus = speed_bonus
        self.special_effect = special_effect

class EquipmentDecorator(CharacterDecorator):
    """Декоратор экипировки"""
    def __init__(self, character: CharacterComponent, equipment: list):
        super().__init__(character)
        self.equipment = equipment

    def get_attack_power(self) -> int:
        base_attack = self._character.get_attack_power()
        equipment_bonus = sum(item.attack_bonus for item in self.equipment)
        return base_attack + equipment_bonus

    def get_speed(self) -> float:
        base_speed = self._character.get_speed()
        equipment_bonus = sum(item.speed_bonus for item in self.equipment)
        return base_speed + equipment_bonus

    def get_defense(self) -> int:
        base_defense = self._character.get_defense()
        equipment_bonus = sum(item.defense_bonus for item in self.equipment)
        return base_defense + equipment_bonus

    def get_description(self) -> str:
        equipment_names = [item.name for item in self.equipment]
        equipment_str = ", ".join(equipment_names) if equipment_names else "без экипировки"
        return f"{self._character.get_description()} с экипировкой: [{equipment_str}]"

def demonstrate_decorator_pattern():
    """Демонстрация паттерна Decorator в игровом контексте"""
    print("=== Демонстрация паттерна Decorator в игровом контексте ===\n")

    # Создаем базового персонажа
    hero = BaseCharacter("Артур", base_attack=15, base_speed=1.2, base_defense=8)
    print(f"Базовый персонаж: {hero.get_description()}")
    print(f"  Атака: {hero.get_attack_power()}, Скорость: {hero.get_speed()}, Защита: {hero.get_defense()}\n")

    # Применяем различные декораторы
    # Сначала добавляем оружие
    enhanced_hero = WeaponDecorator(hero, "Меч Правосудия", attack_bonus=10, special_effect="может оглушить врага")

    print(f"С оружием: {enhanced_hero.get_description()}")
    print(f"  Атака: {enhanced_hero.get_attack_power()}, Скорость: {enhanced_hero.get_speed()}, Защита: {enhanced_hero.get_defense()}\n")

    # Добавляем броню
    enhanced_hero = ArmorDecorator(enhanced_hero, "Кольчуга Дракона", defense_bonus=12, special_property="огнестойкость")

    print(f"С оружием и броней: {enhanced_hero.get_description()}")
    print(f"  Атака: {enhanced_hero.get_attack_power()}, Скорость: {enhanced_hero.get_speed()}, Защита: {enhanced_hero.get_defense()}\n")

    # Добавляем зелье силы
    enhanced_hero = StrengthPotionDecorator(enhanced_hero, strength_boost=7)

    print(f"С оружием, броней и зельем силы: {enhanced_hero.get_description()}")
    print(f"  Атака: {enhanced_hero.get_attack_power()}, Скорость: {enhanced_hero.get_speed()}, Защита: {enhanced_hero.get_defense()}\n")

    # Добавляем зелье скорости
    enhanced_hero = SpeedPotionDecorator(enhanced_hero, speed_boost=0.8)

    print(f"Полностью улучшенный персонаж: {enhanced_hero.get_description()}")
    print(f"  Атака: {enhanced_hero.get_attack_power()}, Скорость: {enhanced_hero.get_speed()}, Защита: {enhanced_hero.get_defense()}\n")

    # Пример с огненным иммунитетом
    fire_resistant_hero = FireResistanceDecorator(enhanced_hero, fire_resistance=75)

    print(f"С огненным иммунитетом: {fire_resistant_hero.get_description()}")
    print(f"  Атака: {fire_resistant_hero.get_attack_power()}, Скорость: {fire_resistant_hero.get_speed()}, Защита: {fire_resistant_hero.get_defense()}")
    if hasattr(fire_resistant_hero, 'get_fire_resistance'):
        print(f"  Огнестойкость: {fire_resistant_hero.get_fire_resistance()}%\n")

    # Пример создания другого персонажа с другой комбинацией
    print("--- Другой пример ---")
    rogue = BaseCharacter("Эльдар", base_attack=12, base_speed=1.8, base_defense=5)
    enhanced_rogue = SpeedPotionDecorator(
        StrengthPotionDecorator(
            WeaponDecorator(rogue, "Отравленные кинжалы", attack_bonus=8, special_effect="отравляет цель"),
            strength_boost=3
        ),
        speed_boost=1.0
    )

    print(f"Разбойник: {enhanced_rogue.get_description()}")
    print(f"  Атака: {enhanced_rogue.get_attack_power()}, Скорость: {enhanced_rogue.get_speed()}, Защита: {enhanced_rogue.get_defense()}")


if __name__ == "__main__":
    demonstrate_decorator_pattern()