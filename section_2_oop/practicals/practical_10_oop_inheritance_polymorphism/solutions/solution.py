# Решения для практической работы 10: ООП - наследование и полиморфизм

# Задание 1: Создание базового класса и наследника
class Animal:
    def __init__(self, name, species, age, health=100):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты
        self.name = name
        self.species = species
        self.age = age
        self.health = health

    def make_sound(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        return f"{self.name} издает звук"

    def eat(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        print(f"{self.name} ест и восстанавливает здоровье")
        self.health = min(100, self.health + 10)

    def sleep(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        print(f"{self.name} спит и отдыхает")
        self.health = min(100, self.health + 5)

class Pet(Animal):
    def __init__(self, name, species, age, owner, health=100):
        # ВАШ КОД ЗДЕСЬ - вызовите конструктор родительского класса
        super().__init__(name, species, age, health)
        self.owner = owner
        self.happiness = 50  # Уровень счастья питомца

    def make_sound(self):
        # ВАШ КОД ЗДЕСЬ - переопределите метод
        return f"{self.name} радостно мяукает!"  # или лает, в зависимости от вида

    def play_with_owner(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        print(f"{self.name} играет с хозяином {self.owner}")
        self.happiness = min(100, self.happiness + 20)
        self.health = min(100, self.health + 5)


# Задание 2: Наследование в игровом контексте
class Vehicle:
    def __init__(self, brand, model, year, max_speed):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты
        self.brand = brand
        self.model = model
        self.year = year
        self.max_speed = max_speed

    def move(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        return f"{self.brand} {self.model} движется"

    def get_info(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        return f"{self.year} {self.brand} {self.model}, макс. скорость: {self.max_speed} км/ч"

class Car(Vehicle):
    def __init__(self, brand, model, year, max_speed, fuel_capacity):
        # ВАШ КОД ЗДЕСЬ - вызовите конструктор родительского класса
        super().__init__(brand, model, year, max_speed)
        self.fuel_capacity = fuel_capacity
        self.current_fuel = fuel_capacity  # Текущий уровень топлива

    def move(self):
        # ВАШ КОД ЗДЕСЬ - переопределите метод
        if self.current_fuel > 0:
            self.current_fuel -= 1  # Расход топлива
            return f"{self.brand} {self.model} едет по дороге со скоростью {self.max_speed} км/ч"
        else:
            return f"{self.brand} {self.model} не может двигаться - нет топлива"

class Airplane(Vehicle):
    def __init__(self, brand, model, year, max_speed, max_altitude):
        # ВАШ КОД ЗДЕСЯ - вызовите конструктор родительского класса
        super().__init__(brand, model, year, max_speed)
        self.max_altitude = max_altitude
        self.altitude = 0  # Текущая высота

    def move(self):
        # ВАШ КОД ЗДЕСЯ - переопределите метод
        self.altitude = min(self.max_altitude, self.altitude + 1000)  # Подъем на высоту
        return f"{self.brand} {self.model} летит на высоте {self.altitude} м со скоростью {self.max_speed} км/ч"


# Задание 3: Множественное наследование в игровом контексте
class Movable:
    """
    Класс, предоставляющий возможность перемещения
    """
    def __init__(self, speed=1.0, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Вызов конструктора следующего класса в MRO
        self.speed = speed
        self.position = [0, 0]
    
    def move(self, dx, dy):
        """
        Перемещение по карте
        """
        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed
        print(f"Персонаж перемещается на позицию ({self.position[0]}, {self.position[1]})")

class Attackable:
    """
    Класс, предоставляющий возможность атаки
    """
    def __init__(self, attack_power=10, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Вызов конструктора следующего класса в MRO
        self.attack_power = attack_power
    
    def attack(self, target):
        """
        Атака цели
        """
        if hasattr(target, 'health'):
            target.health -= self.attack_power
            print(f"Атака на {target.name} нанесла {self.attack_power} урона")
        else:
            print("Цель не имеет здоровья")

class MagicUser:
    """
    Класс, предоставляющий возможность использования магии
    """
    def __init__(self, mana=50, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Вызов конструктора следующего класса в MRO
        self.mana = mana
        self.max_mana = mana
    
    def cast_spell(self, spell_name, target=None):
        """
        Произнесение заклинания
        """
        if self.mana >= 10:
            self.mana -= 10
            print(f"Произнесено заклинание '{spell_name}'")
            if target and hasattr(target, 'health'):
                target.health -= 15  # Урон от заклинания
        else:
            print("Недостаточно маны для заклинания")

class HybridCharacter(Movable, Attackable, MagicUser):
    """
    Гибридный персонаж - сочетает возможности перемещения, атаки и магии
    """
    def __init__(self, name, health=100, **kwargs):
        # Используем аргументы ключевых слов для корректного вызова super()
        super().__init__(**kwargs)
        self.name = name
        self.health = health
        self.max_health = health


# Задание 4: Полиморфизм в боевой системе
class Fighter:
    """
    Класс воина
    """
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.is_alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage

    def special_attack(self, target):
        # ВАШ КОД ЗДЕСЬ - реализуйте специальную атаку воина
        """Специальная атака - тяжелый удар"""
        damage = self.attack_power * 1.5  # На 50% сильнее обычной атаки
        print(f"{self.name} наносит тяжелый удар по {target.name} на {damage} урона")
        target.take_damage(damage)
        return damage

class Mage:
    """
    Класс мага
    """
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.mana = 100
        self.is_alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage

    def special_attack(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте специальную атаку мага
        """Специальная атака - магическое заклинание"""
        if self.mana >= 20:
            self.mana -= 20
            damage = self.attack_power * 2  # Вдвое сильнее обычной атаки
            print(f"{self.name} накладывает мощное заклинание на {target.name} на {damage} урона")
            target.take_damage(damage)
            return damage
        else:
            print(f"{self.name} недостаточно маны для заклинания")
            return 0

class Archer:
    """
    Класс лучника
    """
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.arrows = 30
        self.is_alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage

    def special_attack(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте специальную атаку лучника
        """Специальная атака - точный выстрел"""
        if self.arrows > 0:
            self.arrows -= 1
            damage = self.attack_power * 1.8  # На 80% сильнее обычной атаки
            print(f"{self.name} делает точный выстрел по {target.name} на {damage} урона")
            target.take_damage(damage)
            return damage
        else:
            print(f"{self.name} закончились стрелы")
            return 0

def battle_round(attacker, defender):
    """
    Функция, демонстрирующая полиморфизм
    """
    # ВАШ КОД ЗДЕСЯ - реализуйте вызов специальной атаки
    print(f"\n{attacker.name} атакует {defender.name}!")
    damage = attacker.special_attack(defender)
    print(f"Здоровье {defender.name}: {defender.health}/{defender.max_health}")


# Задание 5: Абстрактные классы для игровых сущностей
from abc import ABC, abstractmethod

class GameEntity(ABC):
    """
    Абстрактный класс игровой сущности
    """
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.max_health = health
        self.is_alive = True
    
    @abstractmethod
    def interact(self, other_entity):
        """
        Взаимодействие с другой сущностью (должен быть реализован в дочернем классе)
        """
        pass
    
    @abstractmethod
    def update(self, delta_time):
        """
        Обновление состояния сущности (должен быть реализован в дочернем классе)
        """
        pass
    
    def take_damage(self, damage):
        """
        Общая логика получения урона
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage
    
    def heal(self, amount):
        """
        Общая логика восстановления здоровья
        """
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health

class Character(GameEntity):
    """
    Абстрактный класс персонажа
    """
    def __init__(self, name, health, armor=0, level=1):
        super().__init__(name, health)
        self.armor = armor
        self.level = level
        self.experience = 0
    
    def take_damage(self, damage):
        """
        Переопределение получения урона с учетом брони
        """
        reduced_damage = max(1, damage - self.armor)  # Минимум 1 урон
        return super().take_damage(reduced_damage)
    
    @abstractmethod
    def use_special_ability(self):
        """
        Использование специальной способности (должно быть реализовано в дочернем классе)
        """
        pass

class Monster(GameEntity):
    """
    Абстрактный класс монстра
    """
    def __init__(self, name, health, monster_type="common"):
        super().__init__(name, health)
        self.monster_type = monster_type
        self.aggression_level = 50  # Уровень агрессии от 0 до 100
    
    @abstractmethod
    def ai_behavior(self, targets):
        """
        Поведение ИИ монстра (должно быть реализовано в дочернем классе)
        """
        pass

class Warrior(Character):
    """
    Класс воина - конкретная реализация
    """
    def __init__(self, name, health=120, armor=10, level=1):
        super().__init__(name, health, armor, level)
        self.rage = 0
        self.strength = 20
    
    def interact(self, other_entity):
        # ВАШ КОД ЗДЕСЯ - реализуйте взаимодействие
        if isinstance(other_entity, Character):
            print(f"{self.name} приветствует {other_entity.name}")
        elif isinstance(other_entity, Monster) and other_entity.is_alive:
            print(f"{self.name} атакует {other_entity.name}!")
            self.attack(other_entity)
        else:
            print(f"{self.name} осматривается вокруг")
    
    def update(self, delta_time):
        # ВАШ КОД ЗДЕСЯ - реализуйте обновление состояния
        # Восстанавливаем немного ярости со временем
        self.rage = min(100, self.rage + delta_time * 2)
        if self.health < self.max_health * 0.3 and self.rage > 50:
            # При низком здоровье используем ярость для лечения
            heal_amount = self.rage // 4
            self.heal(heal_amount)
            self.rage //= 2
            print(f"{self.name} использует ярость для лечения на {heal_amount} здоровья")
    
    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте специальную способность
        if self.rage >= 30:
            self.rage -= 30
            damage_boost = self.strength * 1.5
            print(f"{self.name} использует яростную атаку с силой {damage_boost}!")
            return damage_boost
        else:
            print(f"{self.name} недостаточно ярости для специальной способности")
            return 0

    def attack(self, target):
        if target.is_alive:
            damage = self.strength + (self.rage // 10)
            print(f"{self.name} атакует {target.name} на {damage} урона")
            target.take_damage(damage)

class Dragon(Monster):
    """
    Класс дракона - конкретная реализация
    """
    def __init__(self, name, health=300, armor=20, level=10):
        super().__init__(name, health, "boss")
        self.level = level
        self.fire_damage = 30
        self.wing_span = 20  # Размах крыльев в метрах
    
    def interact(self, other_entity):
        # ВАШ КОД ЗДЕСЯ - реализуйте взаимодействие
        if isinstance(other_entity, Character) and other_entity.is_alive:
            print(f"{self.name} рычит на {other_entity.name} и готовится к атаке!")
        else:
            print(f"{self.name} гордо парит в небе")
    
    def update(self, delta_time):
        # ВАШ КОД ЗДЕСЯ - реализуйте обновление состояния
        # Дракон восстанавливает немного здоровья в броне
        if self.health < self.max_health:
            recovery = self.armor * 0.1 * delta_time
            self.heal(recovery)
            print(f"{self.name} восстанавливает {recovery:.1f} здоровья благодаря своей броне")
    
    def ai_behavior(self, targets):
        # ВАШ КОД ЗДЕСЯ - реализуйте поведение ИИ
        if targets:
            # Выбираем ближайшую цель
            closest_target = targets[0]
            if self.aggression_level > 70:
                print(f"{self.name} атакует {closest_target.name} огненным дыханием!")
                closest_target.take_damage(self.fire_damage)
            else:
                print(f"{self.name} наблюдает за {closest_target.name}, оценивая угрозу")
        else:
            print(f"{self.name} патрулирует свою территорию")


# Задание 6: Комплексная система с использованием всех концепций
class BattleParticipant(ABC):
    """
    Абстрактный класс участника боя
    """
    @abstractmethod
    def battle_action(self, opponents, allies):
        """
        Выполнение боевого действия
        """
        pass
    
    @abstractmethod
    def get_role(self):
        """
        Получение роли в команде
        """
        pass

class WarriorBattle(BattleParticipant):
    """
    Класс воина для боевой системы
    """
    def __init__(self, name, health=120, attack_power=25):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.rage = 0
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage
    
    def battle_action(self, opponents, allies):
        # ВАШ КОД ЗДЕСЯ - реализуйте боевое действие
        if not self.is_alive:
            return f"{self.name} мертв и не может действовать"
        
        if opponents:
            # Атакуем самого слабого врага
            weakest_opponent = min(opponents, key=lambda x: x.health)
            damage = self.attack_power + (self.rage // 10)  # Дополнительный урон от ярости
            weakest_opponent.take_damage(damage)
            self.rage = min(100, self.rage + 15)  # Накапливаем ярость при атаке
            return f"{self.name} атакует {weakest_opponent.name} на {damage} урона (ярость: {self.rage}%)"
        else:
            return f"{self.name} оглядывается в поисках противников..."
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение роли
        return "Танк/Боец"

class MageBattle(BattleParticipant):
    """
    Класс мага для боевой системы
    """
    def __init__(self, name, health=80, attack_power=15):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.mana = 100
        self.max_mana = 100
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage
    
    def battle_action(self, opponents, allies):
        # ВАШ КОД ЗДЕСЯ - реализуйте боевое действие
        if not self.is_alive:
            return f"{self.name} мертв и не может действовать"
        
        if self.mana >= 20 and opponents:
            # Атакуем любого врага
            target = opponents[0]
            damage = self.attack_power * 1.8
            target.take_damage(damage)
            self.mana -= 20
            return f"{self.name} накладывает заклинание на {target.name} на {damage} урона (мана: {self.mana}/{self.max_mana})"
        elif self.mana < 20:
            # Если маны мало, восстанавливаем
            self.mana = min(self.max_mana, self.mana + 30)
            return f"{self.name} восстанавливает ману (мана: {self.mana}/{self.max_mana})"
        else:
            return f"{self.name} ожидает появление противников..."
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение роли
        return "Дамагер/Саппорт"

class HealerBattle(BattleParticipant):
    """
    Класс целителя для боевой системы
    """
    def __init__(self, name, health=90, healing_power=20):
        self.name = name
        self.health = health
        self.max_health = health
        self.healing_power = healing_power
        self.mana = 120
        self.max_mana = 120
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage
    
    def heal_ally(self, ally):
        """Метод для исцеления союзника"""
        # ВАШ КОД ЗДЕСЯ - реализуйте исцеление
        if self.mana >= 15 and ally.is_alive and ally.health < ally.max_health:
            heal_amount = min(ally.max_health - ally.health, self.healing_power)
            ally.health += heal_amount
            self.mana -= 15
            return f"{self.name} лечит {ally.name} на {heal_amount} здоровья (мана: {self.mana}/{self.max_mana})"
        return f"{self.name} не может вылечить {ally.name}"
    
    def battle_action(self, opponents, allies):
        # ВАШ КОД ЗДЕСЯ - реализуйте боевое действие
        if not self.is_alive:
            return f"{self.name} мертв и не может действовать"
        
        if self.mana >= 15:
            # Ищем союзника с наименьшим здоровьем
            injured_ally = None
            lowest_hp_ratio = 1.0
            for ally in allies:
                if ally.is_alive and ally.health < ally.max_health:
                    hp_ratio = ally.health / ally.max_health
                    if hp_ratio < lowest_hp_ratio:
                        lowest_hp_ratio = hp_ratio
                        injured_ally = ally
            
            if injured_ally:
                return self.heal_ally(injured_ally)
            elif opponents:
                # Если некого лечить, помогаем атаковать
                target = opponents[0]
                damage = self.healing_power // 2  # Небольшая атака
                target.take_damage(damage)
                return f"{self.name} слабо атакует {target.name} на {damage} урона (нет нуждающихся в лечении)"
            else:
                return f"{self.name} ожидает... (мана: {self.mana}/{self.max_mana})"
        else:
            # Если маны мало, восстанавливаем
            self.mana = min(self.max_mana, self.mana + 25)
            return f"{self.name} восстанавливает ману (мана: {self.mana}/{self.max_mana})"
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение роли
        return "Саппорт/Целитель"

def execute_battle_round(participants):
    """
    Функция, демонстрирующая полиморфизм
    Принимает список участников боя и позволяет каждому выполнить действие
    """
    # ВАШ КОД ЗДЕСЯ - реализуйте раунд боя
    # Разделяем участников на живых и мертвых
    alive_participants = [p for p in participants if p.is_alive]
    dead_participants = [p for p in participants if not p.is_alive]
    
    print("=== Начало раунда боя ===")
    for participant in alive_participants:
        # Определяем противников и союзников
        # Для простоты: все, кроме участника, считаются противниками
        opponents = [p for p in alive_participants if p != participant]
        allies = [participant]  # Сам участник как союзник
        
        action_result = participant.battle_action(opponents, allies)
        print(action_result)
    print("=== Конец раунда боя ===\n")


# Пример использования
if __name__ == "__main__":
    # Тестирование задания 1
    print("=== Задание 1: Создание базового класса и наследника ===")
    my_pet = Pet("Барсик", "кот", 3, "Иван")
    print(my_pet.make_sound())
    print()

    # Тестирование задания 2
    print("=== Задание 2: Наследование в игровом контексте ===")
    my_car = Car("Toyota", "Camry", 2020, 180, 60)
    my_airplane = Airplane("Boeing", "737", 2019, 850, 12000)
    print(my_car.move())
    print(my_airplane.move())
    print()

    # Тестирование задания 3
    print("=== Задание 3: Множественное наследование ===")
    hero = HybridCharacter("Герой", health=150, speed=2.0, attack_power=25, mana=100)
    print(f"Герой создан: {hero.name}, позиция: {hero.position}, мана: {hero.mana}")
    hero.move(10, 5)
    enemy = type('Enemy', (), {'name': 'Монстр', 'health': 50})()  # Создаем временного врага
    hero.attack(enemy)
    hero.cast_spell("Огненный шар", enemy)
    print(f"Здоровье врага после атак: {enemy.health}")
    print()

    # Тестирование задания 4
    print("=== Задание 4: Полиморфизм в боевой системе ===")
    warrior = Fighter("Конан", 120, 25)
    mage = Mage("Гендальф", 80, 15)
    archer = Archer("Робин", 90, 20)

    battle_round(warrior, mage)  # Воин атакует мага
    battle_round(mage, archer)   # Маг атакует лучника
    battle_round(archer, warrior) # Лучник атакует воина
    print()

    # Тестирование задания 5
    print("=== Задание 5: Абстрактные классы для игровых сущностей ===")
    warrior_char = Warrior("Артур", health=150, armor=15, level=5)
    dragon = Dragon("Смауг", health=500, armor=30, level=15)

    print(f"{warrior_char.name} ({type(warrior_char).__name__}): здоровье {warrior_char.health}/{warrior_char.max_health}, ярость {warrior_char.rage}%")
    print(f"{dragon.name} ({type(dragon).__name__}): здоровье {dragon.health}/{dragon.max_health}, броня {dragon.armor}")

    print(f"\nВзаимодействие:")
    warrior_char.interact(dragon)
    dragon.interact(warrior_char)

    print(f"\nОбновление состояния:")
    warrior_char.update(1.0)
    dragon.update(1.0)

    print(f"\nСпециальные способности:")
    warrior_char.use_special_ability()
    dragon.ai_behavior([warrior_char])
    print()

    # Тестирование задания 6
    print("=== Задание 6: Комплексная система с использованием всех концепций ===")
    team1 = [
        WarriorBattle("Конан"),
        MageBattle("Мерлин")
    ]

    team2 = [
        WarriorBattle("Харальд"),
        HealerBattle("Эльза")
    ]

    all_participants = team1 + team2

    print("Начальное состояние:")
    for participant in all_participants:
        print(f"  {participant.name} ({participant.get_role()}): здоровье {participant.health}/{participant.max_health}")

    # Выполняем несколько раундов боя
    for round_num in range(2):
        print(f"--- Раунд {round_num + 1} ---")
        execute_battle_round(all_participants)

        # Проверяем состояние
        alive = [p for p in all_participants if p.is_alive]
        print(f"Выживших: {len(alive)}")
        for p in alive:
            if hasattr(p, 'mana'):
                print(f"  {p.name}: здоровье {p.health}/{p.max_health}, мана {p.mana}/{p.max_mana}" if p.is_alive else f"  {p.name}: ПОГИБ")
            else:
                print(f"  {p.name}: здоровье {p.health}/{p.max_health}" if p.is_alive else f"  {p.name}: ПОГИБ")
        print()