# Решения для практического задания 11: ООП - абстрактные классы и интерфейсы в игровом контексте

from abc import ABC, abstractmethod

class GameEntity(ABC):
    """
    Абстрактный класс игровой сущности
    """
    def __init__(self, name, health, position=(0, 0)):
        self.name = name
        self.health = health
        self.max_health = health
        self.position = position
        self.is_alive = True
    
    @abstractmethod
    def interact(self, other_entity):
        """
        Взаимодействие с другой игровой сущностью
        """
        pass
    
    @abstractmethod
    def update(self, delta_time):
        """
        Обновление состояния сущности
        """
        pass

    def get_info(self):
        """
        Получение информации о сущности
        """
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({status}): здоровье {self.health}/{self.max_health}, позиция {self.position}"

class Attackable(ABC):
    """
    Интерфейс для боевых действий
    """
    @abstractmethod
    def take_damage(self, damage):
        """
        Получить урон
        """
        pass

    @abstractmethod
    def deal_damage(self, target):
        """
        Нанести урон цели
        """
        pass

class Character(ABC):
    """
    Абстрактный класс игрового персонажа
    """
    def __init__(self, name, health, attack_power, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.level = level
        self.experience = 0
        self.is_alive = True

    @abstractmethod
    def use_special_ability(self):
        """
        Использовать специальную способность
        """
        pass

    @abstractmethod
    def level_up(self):
        """
        Повысить уровень персонажа
        """
        pass

    def rest(self):
        """
        Восстановить здоровье после отдыха
        """
        old_health = self.health
        self.health = self.max_health
        print(f"{self.name} отдохнул и восстановил здоровье с {old_health} до {self.health}")

class InventoryItem(ABC):
    """
    Абстрактный класс предмета инвентаря
    """
    def __init__(self, name, item_type, weight=1.0, value=0):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.value = value
        self.durability = 100  # Прочность предмета

    @abstractmethod
    def use(self, character):
        """
        Использовать предмет персонажем
        """
        pass

class PlayerCharacter(GameEntity):
    def __init__(self, name, health, position=(0, 0), level=1):
        super().__init__(name, health, position)
        self.level = level
        self.experience = 0
        self.inventory = []
        self.abilities = []

    def interact(self, other_entity):
        # Реализация взаимодействия игрока с другими сущностями
        if isinstance(other_entity, NonPlayerCharacter):
            print(f"{self.name} взаимодействует с {other_entity.name}: {other_entity.dialogue}")
        elif isinstance(other_entity, GameItem):
            print(f"{self.name} подбирает {other_entity.name}")
            self.inventory.append(other_entity)
        else:
            print(f"{self.name} исследует {other_entity.name}")

    def update(self, delta_time):
        # Обновление состояния игрока
        # Восстановление здоровья со временем при условии, что игрок не в бою
        if self.health < self.max_health and not hasattr(self, '_in_combat') or not self._in_combat:
            recovery_rate = 0.1 * delta_time  # 0.1 здоровья в секунду
            self.health = min(self.max_health, self.health + recovery_rate)
        print(f"Состояние {self.name} обновлено. Здоровье: {self.health:.1f}")

class NonPlayerCharacter(GameEntity):
    def __init__(self, name, health, position=(0, 0), dialogue="Привет, путник!"):
        super().__init__(name, health, position)
        self.dialogue = dialogue
        self.quest_available = False
        self.merchant = False

    def interact(self, other_entity):
        # Реализация взаимодействия NPC с другими сущностями
        if isinstance(other_entity, PlayerCharacter):
            print(f"{self.name} говорит: '{self.dialogue}'")
            if self.quest_available:
                print(f"{self.name} предлагает квест.")
        else:
            print(f"{self.name} не реагирует на {other_entity.name}")

    def update(self, delta_time):
        # Обновление состояния NPC
        # Например, периодическое изменение позиции или состояния
        print(f"{self.name} находится в ожидании...")

class GameItem(GameEntity):
    def __init__(self, name, health, position=(0, 0), item_type="misc"):
        super().__init__(name, health, position)
        self.item_type = item_type
        self.collected = False

    def interact(self, other_entity):
        # Реализация взаимодействия предмета с другими сущностями
        if isinstance(other_entity, PlayerCharacter):
            print(f"{other_entity.name} подбирает {self.name}")
            self.collected = True
            self.is_alive = False  # Предмет "исчезает" после подбора
        else:
            print(f"{other_entity.name} не может взаимодействовать с {self.name}")

    def update(self, delta_time):
        # Обновление состояния предмета
        # В большинстве случаев предметы не изменяются со временем
        if not self.collected:
            print(f"{self.name} ждет, чтобы быть найденным")

class Warrior(Attackable):
    def __init__(self, name, health, attack_power, defense=5):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.is_alive = True

    def take_damage(self, damage):
        # Учет защиты при получении урона
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} погибает!")
        else:
            print(f"{self.name} получает {actual_damage} урона, осталось здоровья: {self.health}")
        return actual_damage

    def deal_damage(self, target):
        # Нанесение урона цели
        if isinstance(target, Attackable):
            print(f"{self.name} атакует {target.name} с силой {self.attack_power}")
            return target.take_damage(self.attack_power)
        else:
            print(f"{self.name} не может атаковать {target.name}, цель неуязвима")
            return 0

class Orc(Attackable):
    def __init__(self, name, health, attack_power, rage_factor=1.0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.rage_factor = rage_factor  # Множитель силы в состоянии ярости
        self.is_alive = True
        self.rage = False  # Состояние ярости

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} погибает!")
        else:
            print(f"{self.name} получает {damage} урона, осталось здоровья: {self.health}")
            # Вход в состояние ярости при низком здоровье
            if self.health < self.max_health * 0.3 and not self.rage:
                self.rage = True
                self.attack_power *= 1.5
                print(f"{self.name} входит в ярость! Сила увеличена до {self.attack_power}")
        return damage

    def deal_damage(self, target):
        if isinstance(target, Attackable):
            # Увеличение урона при ярости
            damage = self.attack_power * (self.rage_factor if self.rage else 1.0)
            print(f"{self.name} яростно атакует {target.name} с силой {damage}")
            return target.take_damage(damage)
        else:
            print(f"{self.name} не может атаковать {target.name}, цель неуязвима")
            return 0

class Dragon(Attackable):
    def __init__(self, name, health, attack_power, fire_damage=20):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.fire_damage = fire_damage  # Дополнительный урон огнем
        self.is_alive = True
        self.flight_mode = True  # Режим полета

    def take_damage(self, damage):
        # Драконы могут быть менее уязвимы к некоторым видам урона
        reduced_damage = damage * 0.7  # 30% сопротивления урону
        self.health -= reduced_damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"Великий {self.name} падает!")
        else:
            print(f"{self.name} получает {reduced_damage} урона, осталось здоровья: {self.health}")
        return reduced_damage

    def deal_damage(self, target):
        if isinstance(target, Attackable):
            # Дракон наносит как физический, так и огненный урон
            print(f"{self.name} атакует {target.name} и наносит урон огнем!")
            physical_damage = target.take_damage(self.attack_power)
            fire_damage = target.take_damage(self.fire_damage)
            return physical_damage + fire_damage
        else:
            print(f"{self.name} не может атаковать {target.name}, цель неуязвима")
            return 0

class Knight(Character):
    def __init__(self, name, health=150, attack_power=20, level=1, armor=10):
        super().__init__(name, health, attack_power, level)
        self.armor = armor
        self.rage_points = 0  # Очки ярости для специальных способностей

    def use_special_ability(self):
        # Специальная способность: щит или яростная атака
        if self.rage_points >= 50:
            self.rage_points -= 50
            self.attack_power *= 1.5  # Увеличение силы атаки
            print(f"{self.name} использует яростную атаку! Сила атаки увеличена.")
            # Возвращаем нормальный уровень силы после боя
            import threading
            import time
            def reset_attack_power():
                time.sleep(5)  # Способность действует 5 секунд
                self.attack_power /= 1.5
                print(f"Эффект яростной атаки у {self.name} заканчивается.")
            threading.Thread(target=reset_attack_power, daemon=True).start()
        else:
            print(f"{self.name} недостаточно очков ярости для специальной способности.")

    def level_up(self):
        # Повышение уровня рыцаря
        self.level += 1
        self.max_health += 25
        self.health = self.max_health # Полное восстановление при повышении уровня
        self.attack_power += 7
        self.armor += 3
        print(f"{self.name} достиг {self.level} уровня! Здоровье: {self.max_health}, Броня: {self.armor}")

class Wizard(Character):
    def __init__(self, name, health=90, attack_power=15, level=1, mana=100):
        super().__init__(name, health, attack_power, level)
        self.mana = mana
        self.max_mana = mana
        self.spell_power = 1.2  # Множитель силы заклинаний

    def use_special_ability(self):
        # Специальная способность: мощное заклинание
        if self.mana >= 30:
            self.mana -= 30
            damage = self.attack_power * self.spell_power * 2  # Особо мощное заклинание
            print(f"{self.name} произносит мощное заклинание! Урон: {damage}, Осталось маны: {self.mana}")
            # Здесь могла бы быть логика нанесения урона цели
            return damage
        else:
            print(f"{self.name} недостаточно маны для специальной способности.")
            return 0

    def level_up(self):
        # Повышение уровня волшебника
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack_power += 5
        self.max_mana += 20
        self.mana = self.max_mana  # Восстанавливаем ману при повышении уровня
        self.spell_power += 0.1
        print(f"{self.name} достиг {self.level} уровня! Здоровье: {self.max_health}, Мана: {self.max_mana}, Сила заклинаний: {self.spell_power:.1f}")

class Ranger(Character):
    def __init__(self, name, health=110, attack_power=18, level=1, arrows=30):
        super().__init__(name, health, attack_power, level)
        self.arrows = arrows
        self.max_arrows = 30
        self.critical_chance = 0.15  # Шанс критического удара

    def use_special_ability(self):
        # Специальная способность: меткий выстрел
        if self.arrows > 0:
            self.arrows -= 1
            import random
            critical = 2 if random.random() < self.critical_chance else 1
            damage = self.attack_power * 2.5 * critical  # Очень мощный выстрел
            print(f"{self.name} делает меткий выстрел! Урон: {damage}, Осталось стрел: {self.arrows}")
            if critical > 1:
                print("КРИТИЧЕСКИЙ УДАР!")
            # Здесь могла бы быть логика нанесения урона цели
            return damage
        else:
            print(f"{self.name} закончились стрелы для специальной способности.")
            return 0

    def level_up(self):
        # Повышение уровня рейнджера
        self.level += 1
        self.max_health += 15
        self.health = self.max_health
        self.attack_power += 6
        self.max_arrows += 10
        self.arrows = self.max_arrows  # Пополняем запас стрел при повышении уровня
        self.critical_chance += 0.03
        print(f"{self.name} достиг {self.level} уровня! Здоровье: {self.max_health}, Стрелы: {self.max_arrows}, Шанс крита: {self.critical_chance:.2f}")

class HealthPotion(InventoryItem):
    def __init__(self, name="Зелье здоровья", healing_power=50, weight=0.5, value=25):
        super().__init__(name, "consumable", weight, value)
        self.healing_power = healing_power  # Количество здоровья, которое восстанавливает зелье

    def use(self, character):
        # Использование зелья здоровья персонажем
        if not self.durability > 0:
            print(f"{self.name} разрушено и не может быть использовано.")
            return False

        if not hasattr(character, 'health'):
            print(f"{self.name} не может быть использовано {character.name}, потому что сущность не имеет здоровья.")
            return False

        old_health = character.health
        character.health = min(character.max_health, character.health + self.healing_power)
        healed = character.health - old_health
        self.durability -= 25  # Зелье уничтожается при использовании

        print(f"{character.name} использует {self.name} и восстанавливает {healed} здоровья.")
        if self.durability <= 0:
            print(f"{self.name} полностью израсходовано.")
        return True

class ManaPotion(InventoryItem):
    def __init__(self, name="Зелье маны", mana_restored=40, weight=0.5, value=20):
        super().__init__(name, "consumable", weight, value)
        self.mana_restored = mana_restored  # Количество маны, которую восстанавливает зелье

    def use(self, character):
        # Использование зелья маны персонажем
        if not self.durability > 0:
            print(f"{self.name} разрушено и не может быть использовано.")
            return False

        # Проверяем, имеет ли персонаж ману
        if not hasattr(character, 'mana'):
            print(f"{character.name} не может использовать {self.name}, потому что не обладает магическими способностями.")
            return False

        old_mana = character.mana
        character.mana = min(character.max_mana, character.mana + self.mana_restored)
        restored = character.mana - old_mana
        self.durability -= 25  # Зелье уничтожается при использовании

        print(f"{character.name} использует {self.name} и восстанавливает {restored} маны.")
        if self.durability <= 0:
            print(f"{self.name} полностью израсходовано.")
        return True

class Sword(InventoryItem):
    def __init__(self, name="Стальной меч", attack_bonus=10, weight=5.0, value=100, durability=100):
        super().__init__(name, "weapon", weight, value)
        self.attack_bonus = attack_bonus  # Бонус к атаке при экипировке
        self.durability = durability  # Прочность оружия
        self.equipped = False  # Состояние экипировки

    def use(self, character):
        # Экипировка меча персонажем
        if not self.durability > 0:
            print(f"{self.name} слишком поврежден для использования.")
            return False

        if self.equipped:
            print(f"{self.name} уже экипирован.")
            return True

        # Проверяем, есть ли у персонажа атрибут атаки
        if not hasattr(character, 'attack_power'):
            print(f"{self.name} не может быть экипирован {character.name}, потому что сущность не может атаковать.")
            return False

        # Экипируем меч
        character.attack_power += self.attack_bonus
        self.equipped = True
        self.durability -= 5  # Небольшой износ при экипировке

        print(f"{character.name} экипировал {self.name}, атака увеличена на {self.attack_bonus}.")
        return True

    def unequip(self, character):
        # Снятие меча с персонажа
        if not self.equipped:
            print(f"{self.name} не экипирован.")
            return False

        # Снимаем бонус
        character.attack_power -= self.attack_bonus
        self.equipped = False

        print(f"{character.name} снял {self.name}, атака уменьшена на {self.attack_bonus}.")
        return True