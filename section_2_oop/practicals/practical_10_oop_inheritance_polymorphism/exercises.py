# Упражнения для практической работы 10: ООП - наследование и полиморфизм

# Задание 1: Создание базового класса и наследника
class Animal:
    def __init__(self, name, species, age, health=100):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты
        pass  # Замените на ваш код

    def make_sound(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

    def eat(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

    def sleep(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

class Pet(Animal):
    def __init__(self, name, species, age, owner, health=100):
        # ВАШ КОД ЗДЕСЬ - вызовите конструктор родительского класса
        pass  # Замените на ваш код

    def make_sound(self):
        # ВАШ КОД ЗДЕСЬ - переопределите метод
        pass  # Замените на ваш код

    def play_with_owner(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код


# Задание 2: Наследование в игровом контексте
class Vehicle:
    def __init__(self, brand, model, year, max_speed):
        # ВАШ КОД ЗДЕСЬ - добавьте атрибуты
        pass  # Замените на ваш код

    def move(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

    def get_info(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

class Car(Vehicle):
    def __init__(self, brand, model, year, max_speed, fuel_capacity):
        # ВАШ КОД ЗДЕСЬ - вызовите конструктор родительского класса
        pass  # Замените на ваш код

    def move(self):
        # ВАШ КОД ЗДЕСЬ - переопределите метод
        pass  # Замените на ваш код

class Airplane(Vehicle):
    def __init__(self, brand, model, year, max_speed, max_altitude):
        # ВАШ КОД ЗДЕСЬ - вызовите конструктор родительского класса
        pass  # Замените на ваш код

    def move(self):
        # ВАШ КОД ЗДЕСЬ - переопределите метод
        pass  # Замените на ваш код


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
            if target:
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
        pass  # Замените на ваш код

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
        # ВАШ КОД ЗДЕСЬ - реализуйте специальную атаку мага
        pass  # Замените на ваш код

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
        # ВАШ КОД ЗДЕСЬ - реализуйте специальную атаку лучника
        pass  # Замените на ваш код

def battle_round(attacker, defender):
    """
    Функция, демонстрирующая полиморфизм
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте вызов специальной атаки
    pass  # Замените на ваш код


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
        # ВАШ КОД ЗДЕСЬ - реализуйте взаимодействие
        pass  # Замените на ваш код
    
    def update(self, delta_time):
        # ВАШ КОД ЗДЕСЬ - реализуйте обновление состояния
        pass  # Замените на ваш код
    
    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте специальную способность
        pass # Замените на ваш код

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
        # ВАШ КОД ЗДЕСЬ - реализуйте взаимодействие
        pass  # Замените на ваш код
    
    def update(self, delta_time):
        # ВАШ КОД ЗДЕСЬ - реализуйте обновление состояния
        pass  # Замените на ваш код
    
    def ai_behavior(self, targets):
        # ВАШ КОД ЗДЕСЬ - реализуйте поведение ИИ
        pass  # Замените на ваш код


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
        # ВАШ КОД ЗДЕСЬ - реализуйте боевое действие
        pass  # Замените на ваш код
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение роли
        pass  # Замените на ваш код

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
        # ВАШ КОД ЗДЕСЬ - реализуйте боевое действие
        pass  # Замените на ваш код
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение роли
        pass  # Замените на ваш код

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
        # ВАШ КОД ЗДЕСЬ - реализуйте исцеление
        pass  # Замените на ваш код
    
    def battle_action(self, opponents, allies):
        # ВАШ КОД ЗДЕСЬ - реализуйте боевое действие
        pass  # Замените на ваш код
    
    def get_role(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение роли
        pass  # Замените на ваш код

def execute_battle_round(participants):
    """
    Функция, демонстрирующая полиморфизм
    Принимает список участников боя и позволяет каждому выполнить действие
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте раунд боя
    pass  # Замените на ваш код