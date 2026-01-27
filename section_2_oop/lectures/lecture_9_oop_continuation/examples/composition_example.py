# composition_example.py

class Stats:
    """Класс статистики персонажа - компонент, который существует только с персонажем"""
    def __init__(self, strength=10, agility=10, intelligence=10, vitality=10):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.vitality = vitality
        self.base_health = 100 + (self.vitality * 5)
        self.health = self.base_health

    def update_health(self):
        """Обновить здоровье на основе выносливости"""
        self.base_health = 100 + (self.vitality * 5)
        self.health = min(self.health, self.base_health)

    def level_up(self):
        """Повышение характеристик при уровне"""
        self.strength += 2
        self.agility += 2
        self.intelligence += 2
        self.vitality += 2
        self.update_health()

    def __str__(self):
        return f"Сила:{self.strength}, Ловкость:{self.agility}, Интеллект:{self.intelligence}, Живучесть:{self.vitality}"


class Equipment:
    """Класс снаряжения персонажа - компонент, который существует только с персонажем"""
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.accessories = []

    def equip_weapon(self, weapon):
        """Надеть оружие"""
        old_weapon = self.weapon
        self.weapon = weapon
        return old_weapon

    def equip_armor(self, armor):
        """Надеть броню"""
        old_armor = self.armor
        self.armor = armor
        return old_armor

    def add_accessory(self, accessory):
        """Добавить аксессуар (до 3 штук)"""
        if len(self.accessories) < 3:
            self.accessories.append(accessory)
            return True
        return False

    def unequip_weapon(self):
        """Снять оружие"""
        weapon = self.weapon
        self.weapon = None
        return weapon

    def unequip_armor(self):
        """Снять броню"""
        armor = self.armor
        self.armor = None
        return armor

    def get_total_damage_bonus(self):
        """Получить общий бонус к урону"""
        bonus = 0
        if self.weapon:
            bonus += self.weapon.damage_bonus
        for accessory in self.accessories:
            bonus += accessory.damage_bonus
        return bonus

    def get_total_protection_bonus(self):
        """Получить общий бонус к защите"""
        bonus = 0
        if self.armor:
            bonus += self.armor.protection_bonus
        for accessory in self.accessories:
            bonus += accessory.protection_bonus
        return bonus


class Inventory:
    """Класс инвентаря персонажа - компонент, который существует только с персонажем"""
    def __init__(self, max_capacity=20):
        self.items = []
        self.max_capacity = max_capacity

    def add_item(self, item):
        """Добавить предмет в инвентарь"""
        if len(self.items) < self.max_capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item):
        """Удалить предмет из инвентаря"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_item_by_name(self, name):
        """Получить предмет по имени"""
        for item in self.items:
            if item.name == name:
                return item
        return None

    def get_total_weight(self):
        """Получить общий вес предметов"""
        return sum(item.weight for item in self.items)

    def __len__(self):
        """Количество предметов в инвентаре"""
        return len(self.items)

    def __iter__(self):
        """Итерация по инвентарю"""
        return iter(self.items)


class Character:
    """Класс персонажа - использует композицию для статистики, снаряжения и инвентаря"""
    def __init__(self, name, char_class="Воин"):
        self.name = name
        self.char_class = char_class
        self.level = 1
        
        # Композиция: компоненты создаются и уничтожаются вместе с персонажем
        self.stats = Stats()
        self.equipment = Equipment()
        self.inventory = Inventory()

    def get_total_damage(self):
        """Получить общий урон персонажа"""
        base_damage = self.stats.strength * 2
        equipment_bonus = self.equipment.get_total_damage_bonus()
        return base_damage + equipment_bonus

    def get_total_protection(self):
        """Получить общую защиту персонажа"""
        base_protection = self.stats.vitality
        equipment_bonus = self.equipment.get_total_protection_bonus()
        return base_protection + equipment_bonus

    def take_damage(self, damage):
        """Получить урон"""
        protection = self.get_total_protection()
        actual_damage = max(1, damage - protection)
        self.stats.health -= actual_damage
        if self.stats.health < 0:
            self.stats.health = 0
        return actual_damage

    def level_up(self):
        """Повысить уровень персонажа"""
        self.level += 1
        self.stats.level_up()
        print(f"{self.name} достиг {self.level} уровня!")

    def __str__(self):
        return f"{self.name} ({self.char_class}): Уровень {self.level}, Здоровье: {self.stats.health}/{self.stats.base_health}"


# Пример использования композиции
print("=== Демонстрация композиции в игровых персонажах ===")

# Создание персонажа (компоненты создаются автоматически)
hero = Character("Артур", "Воин")
print(hero)

print(f"\nСтатистика: {hero.stats}")
print(f"Урон: {hero.get_total_damage()}, Защита: {hero.get_total_protection()}")

# Создание предметов
class WeaponItem:
    def __init__(self, name, damage_bonus):
        self.name = name
        self.damage_bonus = damage_bonus

class ArmorItem:
    def __init__(self, name, protection_bonus):
        self.name = name
        self.protection_bonus = protection_bonus

class AccessoryItem:
    def __init__(self, name, damage_bonus=0, protection_bonus=0):
        self.name = name
        self.damage_bonus = damage_bonus
        self.protection_bonus = protection_bonus

# Экипировка персонажа
sword = WeaponItem("Экскалибур", 15)
shield = ArmorItem("Щит короля Артура", 10)
ring = AccessoryItem("Кольцо силы", damage_bonus=5)

hero.equipment.equip_weapon(sword)
hero.equipment.equip_armor(shield)
hero.equipment.add_accessory(ring)

print(f"\nПосле экипировки:")
print(f"Урон: {hero.get_total_damage()}, Защита: {hero.get_total_protection()}")

# Добавление предметов в инвентарь
potion = {"name": "Зелье здоровья", "type": "consumable", "effect": "heal_50"}
hero.inventory.add_item(potion)

print(f"\nИнвентарь: {len(hero.inventory)} предметов")