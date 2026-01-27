# aggregation_example.py

class Character:
    """Класс персонажа"""
    def __init__(self, name, char_class="Воин"):
        self.name = name
        self.char_class = char_class
        self.level = 1
        
        # Компоненты, которые существуют только с персонажем (композиция)
        self.stats = Stats()
        self.equipment = Equipment()

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


class Party:
    """Класс отряда - использует агрегацию для хранения персонажей"""
    def __init__(self, name="Отряд приключений"):
        self.name = name
        self.members = []  # Агрегация: персонажи могут существовать без отряда
        self.leader = None

    def add_member(self, character):
        """Добавить персонажа в отряд"""
        if character not in self.members:
            self.members.append(character)
            if len(self.members) == 1:
                self.leader = character
            return True
        return False

    def remove_member(self, character):
        """Удалить персонажа из отряда"""
        if character in self.members:
            self.members.remove(character)
            # Если удаляем лидера, выбираем нового
            if character == self.leader and self.members:
                self.leader = self.members[0]
            elif character == self.leader:
                self.leader = None
            return True
        return False

    def set_leader(self, character):
        """Установить лидера отряда"""
        if character in self.members:
            self.leader = character
            return True
        return False

    def get_total_level(self):
        """Получить суммарный уровень отряда"""
        return sum(member.level for member in self.members)

    def get_average_stats(self):
        """Получить среднюю статистику отряда"""
        if not self.members:
            return None
        total_strength = sum(member.stats.strength for member in self.members)
        total_agility = sum(member.stats.agility for member in self.members)
        total_intelligence = sum(member.stats.intelligence for member in self.members)
        
        count = len(self.members)
        return {
            'strength': total_strength // count,
            'agility': total_agility // count,
            'intelligence': total_intelligence // count
        }

    def battle_ready(self):
        """Проверить, готов ли отряд к битве"""
        return len(self.members) > 0 and all(member.stats.health > 0 for member in self.members)

    def __len__(self):
        """Количество членов отряда"""
        return len(self.members)

    def __iter__(self):
        """Итерация по членам отряда"""
        return iter(self.members)

    def __str__(self):
        members_str = ", ".join(member.name for member in self.members)
        return f"Отряд '{self.name}': [{members_str}] (Лидер: {self.leader.name if self.leader else 'нет'})"


class Guild:
    """Класс гильдии - еще один пример агрегации"""
    def __init__(self, name, guild_master):
        self.name = name
        self.guild_master = guild_master  # Гильдмастер может быть персонажем
        self.members = []  # Агрегация: персонажи могут покинуть гильдию
        self.funds = 0

    def recruit(self, character):
        """Нанять персонажа в гильдию"""
        if character not in self.members:
            self.members.append(character)
            return True
        return False

    def dismiss(self, character):
        """Уволить персонажа из гильдии"""
        if character in self.members:
            self.members.remove(character)
            return True
        return False

    def contribute_funds(self, character, amount):
        """Внести средства в казну гильдии"""
        # Предполагаем, что у персонажа есть деньги
        if hasattr(character, 'gold') and character.gold >= amount:
            character.gold -= amount
            self.funds += amount
            return True
        return False

    def __str__(self):
        return f"Гильдия '{self.name}' во главе с {self.guild_master.name}, членов: {len(self.members)}, казна: {self.funds}"


# Пример использования агрегации
print("=== Демонстрация агрегации в игровых системах ===")

# Создание персонажей
warrior = Character("Конан", "Воин")
mage = Character("Мерлин", "Маг")
archer = Character("Робин", "Лучник")

# У персонажей добавим немного денег для примера
warrior.gold = 100
mage.gold = 50

# Создание отряда (агрегация)
adventurers_party = Party("Храбрые искатели")
adventurers_party.add_member(warrior)
adventurers_party.add_member(mage)
adventurers_party.add_member(archer)

print(adventurers_party)
print(f"Суммарный уровень отряда: {adventurers_party.get_total_level()}")
print(f"Средняя статистика: {adventurers_party.get_average_stats()}")
print(f"Готовность к битве: {adventurers_party.battle_ready()}")

# Создание гильдии (агрегация)
guild = Guild("Бродячие псы", warrior)
guild.recruit(warrior)
guild.recruit(mage)

guild.contribute_funds(warrior, 30)
guild.contribute_funds(mage, 20)

print(f"\n{guild}")

# Демонстрация независимости персонажей
print(f"\nПерсонажи существуют независимо от групп:")
print(f"Воин: {warrior}")
print(f"Маг: {mage}")
print(f"Лучник: {archer}")

# Персонаж может покинуть отряд
adventurers_party.remove_member(archer)
print(f"\nПосле того как лучник покинул отряд: {adventurers_party}")
print(f"Лучник по-прежнему существует: {archer}")

# Демонстрация изменения характеристик персонажа вне группы
print(f"\nИзменение уровня у воина вне отряда:")
warrior.level_up()
print(f"Уровень воина после повышения: {warrior.level}")
print(f"Новый суммарный уровень отряда: {adventurers_party.get_total_level()}")