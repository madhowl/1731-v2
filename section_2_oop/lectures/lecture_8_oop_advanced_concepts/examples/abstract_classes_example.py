"""
Пример: Абстрактные классы для игровых сущностей
"""

from abc import ABC, abstractmethod

class GameEntity(ABC):
    """Абстрактный класс игровой сущности"""
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.max_health = health

    @abstractmethod
    def interact(self, other_entity):
        """Абстрактный метод взаимодействия с другой сущностью"""
        pass

    @abstractmethod
    def update(self, delta_time):
        """Абстрактный метод обновления состояния сущности"""
        pass

    def is_alive(self):
        """Метод проверки, жива ли сущность"""
        return self.health > 0

    def take_damage(self, amount):
        """Метод получения урона"""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Метод восстановления здоровья"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (Здоровье: {self.health}/{self.max_health})"


class LivingEntity(GameEntity):
    """Абстрактный класс живой сущности"""
    def __init__(self, name, health=100, armor=0):
        super().__init__(name, health)
        self.armor = armor

    @abstractmethod
    def move(self, direction):
        """Абстрактный метод движения"""
        pass

    def take_damage(self, amount):
        """Переопределение метода получения урона с учетом брони"""
        # Учет брони при получении урона
        reduced_damage = max(1, amount - self.armor)  # Минимум 1 урон
        print(f"{self.name} заблокировал {amount - reduced_damage} урона с помощью брони")
        super().take_damage(reduced_damage)


class Character(LivingEntity):
    """Абстрактный класс персонажа"""
    def __init__(self, name, health=100, armor=0, level=1):
        super().__init__(name, health, armor)
        self.level = level
        self.experience = 0

    @abstractmethod
    def level_up(self):
        """Абстрактный метод повышения уровня"""
        pass

    @abstractmethod
    def special_ability(self):
        """Абстрактный метод специальной способности"""
        pass

    def gain_experience(self, exp_amount):
        """Метод получения опыта"""
        self.experience += exp_amount
        print(f"{self.name} получил {exp_amount} опыта. Всего: {self.experience}")


class PlayerCharacter(Character):
    """Абстрактный класс игроком управляемого персонажа"""
    def __init__(self, name, health=100, armor=0, level=1, gold=0):
        super().__init__(name, health, armor, level)
        self.gold = gold  # Количество золота у игрока
        self.inventory = []  # Инвентарь игрока

    @abstractmethod
    def use_item(self, item_index):
        """Абстрактный метод использования предмета из инвентаря"""
        pass

    def add_item_to_inventory(self, item):
        """Метод добавления предмета в инвентарь"""
        if len(self.inventory) < 20:  # Ограничение размера инвентаря
            self.inventory.append(item)
            print(f"Предмет '{item}' добавлен в инвентарь {self.name}")
        else:
            print(f"Инвентарь {self.name} полон!")


class NPC(Character):
    """Абстрактный класс неигрового персонажа"""
    def __init__(self, name, health=100, armor=0, level=1, dialogue="Привет, путешественник!"):
        super().__init__(name, health, armor, level)
        self.dialogue = dialogue # Реплика НИПа

    @abstractmethod
    def ai_behavior(self):
        """Абстрактный метод поведения ИИ"""
        pass

    def speak(self):
        """Метод, с помощью которого НИП говорит"""
        print(f"{self.name}: {self.dialogue}")


# Реализация конкретных классов
class Warrior(PlayerCharacter):
    """Класс воина - конкретная реализация"""
    def __init__(self, name, weapon="Меч"):
        super().__init__(name, health=150, armor=15, level=1)
        self.weapon = weapon
        self.rage = 0  # Ярость воина

    def interact(self, other_entity):
        """Реализация взаимодействия"""
        if isinstance(other_entity, NPC):
            print(f"{self.name} говорит: 'Привет, {other_entity.name}!'")
            other_entity.speak()
        elif isinstance(other_entity, GameEntity) and other_entity.is_alive():
            print(f"{self.name} атакует {other_entity.name} с {self.weapon}!")
            other_entity.take_damage(25)
        else:
            print(f"{self.name} осматривается вокруг.")

    def update(self, delta_time):
        """Обновление состояния воина"""
        # Постепенное восстановление ярости
        self.rage = min(100, self.rage + delta_time * 2)
        if self.rage > 95:
            print(f"Ярость {self.name} почти максимальна: {self.rage:.1f}%")

    def move(self, direction):
        """Реализация движения"""
        print(f"{self.name} движется в направлении {direction}")

    def level_up(self):
        """Реализация повышения уровня"""
        self.level += 1
        self.max_health += 20
        self.health = self.max_health  # Полное восстановление при повышении уровня
        print(f"{self.name} достиг {self.level} уровня! Здоровье увеличено до {self.max_health}")

    def special_ability(self):
        """Реализация специальной способности"""
        if self.rage >= 30:
            self.rage -= 30
            damage = 40
            print(f"{self.name} использует 'Яростную атаку' и наносит {damage} урона!")
            return damage
        else:
            print(f"Недостаточно ярости для 'Яростной атаки'. Требуется 30, доступно {self.rage:.1f}")
            return 0

    def use_item(self, item_index):
        """Реализация использования предмета"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            print(f"{self.name} использует предмет: {item}")
            # Удаляем использованный предмет
            del self.inventory[item_index]
        else:
            print(f"Неверный индекс предмета: {item_index}")

    def berserker_rage(self):
        """Специальная способность воина - берсерк"""
        if self.rage >= 50:
            self.rage -= 50
            self.health = min(self.max_health, self.health + 30)  # Лечение
            print(f"{self.name} впадает в ярость берсерка! Восстанавливает 30 здоровья.")
        else:
            print(f"Недостаточно ярости для 'Берсерка'. Требуется 50, доступно {self.rage:.1f}")


class Mage(NPC):
    """Класс мага - конкретная реализация НИПа"""
    def __init__(self, name, spell="Огненный шар"):
        super().__init__(name, health=80, armor=5, level=2, dialogue="Я чувствую магическую энергию воздухе...")
        self.spell = spell
        self.mana = 100
        self.max_mana = 100

    def interact(self, other_entity):
        """Реализация взаимодействия"""
        if isinstance(other_entity, PlayerCharacter):
            print(f"{self.name} замечает {other_entity.name} и говорит: 'О, путник! Ищу помощника в исследовании древних рун.'")
            self.speak()
        elif isinstance(other_entity, GameEntity) and other_entity.is_alive():
            print(f"{self.name} атакует {other_entity.name} магией!")
            self.cast_spell(other_entity)
        else:
            print(f"{self.name} читает древние тексты.")

    def update(self, delta_time):
        """Обновление состояния мага"""
        # Постепенное восстановление маны
        self.mana = min(self.max_mana, self.mana + delta_time * 5)
        if self.mana == self.max_mana:
            print(f"Мана {self.name} полностью восстановлена.")

    def move(self, direction):
        """Реализация движения"""
        print(f"{self.name} телепортируется в направлении {direction}")

    def level_up(self):
        """Реализация повышения уровня"""
        self.level += 1
        self.max_health += 10
        self.max_mana += 15
        self.health = self.max_health
        self.mana = self.max_mana
        print(f"{self.name} достиг {self.level} уровня! Здоровье: {self.max_health}, Мана: {self.max_mana}")

    def special_ability(self):
        """Реализация специальной способности"""
        return self.cast_spell(None)

    def ai_behavior(self):
        """Реализация поведения ИИ"""
        print(f"{self.name} изучает магические руны или готовит зелья.")

    def cast_spell(self, target=None):
        """Метод произнесения заклинания"""
        if self.mana >= 20:
            self.mana -= 20
            if target:
                target.take_damage(25)
                print(f"{self.name} произносит '{self.spell}' и наносит 25 урона {target.name}!")
            else:
                print(f"{self.name} практикует '{self.spell}', расходуя ману.")
            return True
        else:
            print(f"{self.name} не хватает маны для заклинания.")
            return False


def demonstrate_abstract_classes():
    """Демонстрация абстрактных классов"""
    print("=== Демонстрация абстрактных классов ===\n")
    
    # Попытка создания экземпляра абстрактного класса приведет к ошибке
    try:
        entity = GameEntity("Тестовая сущность")  # Ошибка: нельзя создать экземпляр абстрактного класса
    except TypeError as e:
        print(f"Ошибка при создании GameEntity: {e}\n")

    # Создание персонажей
    warrior = Warrior("Артур", weapon="Экскалибур")
    mage = Mage("Мерлин")

    print(f"Созданы персонажи:")
    print(f"{warrior}")
    print(f"{mage}\n")

    print(f"Ярость воина: {warrior.rage}")
    warrior.special_ability()  # Не хватит ярости

    # Повышение ярости искусственно для демонстрации
    warrior.rage = 40
    print(f"Ярость воина после восстановления: {warrior.rage}")
    warrior.special_ability()  # Теперь способность сработает

    print(f"\nМана мага: {mage.mana}/{mage.max_mana}")
    mage.cast_spell(warrior)

    print(f"\nЗдоровье воина после атаки: {warrior.health}/{warrior.max_health}")

    # Взаимодействие между персонажами
    print("\n--- Взаимодействие ---")
    warrior.interact(mage)
    print()
    mage.interact(warrior)

    # Использование инвентаря
    print("\n--- Использование инвентаря ---")
    warrior.add_item_to_inventory("Зелье здоровья")
    warrior.add_item_to_inventory("Магический кристалл")
    warrior.use_item(0)  # Используем первое зелье
    print(f"Инвентарь воина: {warrior.inventory}")


if __name__ == "__main__":
    demonstrate_abstract_classes()