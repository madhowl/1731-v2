"""
Пример: Множественное наследование в игровых персонажах
"""

class GameEntity:
    """Абстрактная базовая сущность в игре"""
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.max_health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (Здоровье: {self.health}/{self.max_health})"


class Movable:
    """Класс, предоставляющий возможность перемещения"""
    def __init__(self, speed=1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = speed
        self.position = (0, 0)

    def move(self, x, y):
        """Переместить персонажа в новую позицию"""
        old_pos = self.position
        self.position = (x, y)
        print(f"{self.name} переместился из {old_pos} в {self.position} со скоростью {self.speed}")


class Attackable:
    """Класс, предоставляющий возможность атаки"""
    def __init__(self, attack_power=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack_power = attack_power

    def attack(self, target):
        """Атаковать цель"""
        if isinstance(target, GameEntity) and target.is_alive():
            print(f"{self.name} атакует {target.name} силой {self.attack_power}")
            target.take_damage(self.attack_power)
            return True
        else:
            print(f"{self.name} не может атаковать {target.name}, цель недействительна")
            return False


class LivingEntity(GameEntity):
    """Живая сущность с дополнительными характеристиками"""
    def __init__(self, name, health=100, armor=0):
        super().__init__(name, health)
        self.armor = armor

    def take_damage(self, amount):
        # Учет брони при получении урона
        reduced_damage = max(1, amount - self.armor)  # Минимум 1 урон
        print(f"{self.name} заблокировал {amount - reduced_damage} урона с помощью брони")
        super().take_damage(reduced_damage)


class MagicUser:
    """Класс, предоставляющий магические способности"""
    def __init__(self, magic_power=10, mana=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mana = mana
        self.max_mana = mana
        self.magic_power = magic_power

    def cast_spell(self, spell_name, target=None):
        """Произнести заклинание"""
        if self.mana >= 10:
            self.mana -= 10
            print(f"{self.name} произносит заклинание '{spell_name}'")
            if target:
                print(f"Цель: {target.name}")
            return True
        else:
            print(f"Недостаточно маны для заклинания '{spell_name}'. Требуется 10, доступно {self.mana}")
            return False

    def restore_mana(self, amount):
        """Восстановить ману"""
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        print(f"{self.name} восстановил {amount} маны")


class Paladin(LivingEntity, Movable, Attackable, MagicUser):
    """Паладин - воин со священными заклинаниями"""
    def __init__(self, name, weapon="Святой меч", *args, **kwargs):
        # Устанавливаем значения по умолчанию
        kwargs.setdefault('health', 180)
        kwargs.setdefault('armor', 15)
        kwargs.setdefault('attack_power', 20)
        kwargs.setdefault('magic_power', 15)
        kwargs.setdefault('mana', 80)
        kwargs.setdefault('speed', 1.5)
        super().__init__(name, *args, **kwargs)
        self.weapon = weapon

    def holy_smite(self, target):
        """Святое поражение - комбинация физической атаки и магии"""
        if isinstance(target, GameEntity) and target.is_alive():
            physical_damage = self.attack_power
            magical_damage = self.magic_power
            total_damage = physical_damage + magical_damage
            
            print(f"{self.name} применяет Святое Поражение по {target.name}!")
            print(f"Физический урон: {physical_damage}, Магический урон: {magical_damage}")
            
            # Сначала магическая атака
            self.cast_spell("Святое Поражение", target)
            # Затем физическая атака
            target.take_damage(total_damage)
            return True
        else:
            print(f"{self.name} не может применить Святое Поражение к {target.name}, цель недействительна")
            return False


if __name__ == "__main__":
    print("=== Демонстрация множественного наследования ===\n")
    
    # Проверка порядка разрешения методов
    print("Порядок разрешения методов для класса Paladin:")
    for cls in Paladin.__mro__:
        print(f"  - {cls.__name__}")

    paladin = Paladin("Сэр Ланселот")
    print(f"\n{paladin}")
    print(f"Мана: {paladin.mana}/{paladin.max_mana}")

    # Пример использования способностей паладина
    goblin = LivingEntity("Злобный гоблин", health=70, armor=3)
    print(f"\n{goblin}")

    paladin.holy_smite(goblin)
    print(f"\n{goblin} после атаки")
    print(f"Мана паладина: {paladin.mana}/{paladin.max_mana}")
    
    # Демонстрация других способностей
    paladin.move(10, 5)
    paladin.attack(goblin)