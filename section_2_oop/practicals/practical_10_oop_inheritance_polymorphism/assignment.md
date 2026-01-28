# Практическое занятие 10: ООП - наследование и полиморфизм

## Наследование, переопределение методов, полиморфизм, абстрактные классы

### Цель занятия:
Научиться использовать наследование и полиморфизм в Python для создания иерархий игровых классов и расширения функциональности игровых сущностей.

### Задачи:
1. Создать классы игровых сущностей с наследованием
2. Переопределять методы родительского класса для игровых сценариев
3. Применять полиморфизм в игровых системах
4. Использовать абстрактные классы для игровых сущностей
5. Реализовать иерархии классов для игровых персонажей и объектов

### План работы:
1. Создание иерархии классов с наследованием
2. Переопределение методов в дочерних классах
3. Применение полиморфизма в игровых системах
4. Использование абстрактных классов
5. Практические задания в игровом контексте

---
# Практическое занятие 10: ООП - наследование и полиморфизм

## Наследование, переопределение методов, полиморфизм, абстрактные классы

### Цель занятия:
Научиться использовать наследование и полиморфизм в Python для создания иерархий игровых классов и расширения функциональности игровых сущностей.

### Задачи:
1. Создать классы игровых сущностей с наследованием
2. Переопределять методы родительского класса для игровых сценариев
3. Применять полиморфизм в игровых системах
4. Использовать абстрактные классы для игровых сущностей
5. Реализовать иерархии классов для игровых персонажей и объектов

---

## 1. Теоретическая часть

### Основные понятия наследования и полиморфизма

**Наследование** — это механизм, позволяющий одному классу наследовать атрибуты и методы другого класса. Это позволяет создавать иерархии классов и повторно использовать код.

**Полиморфизм** — это способность объекта использовать методы производного класса, который ему неизвестен. То есть одинаковые интерфейсы могут использоваться для различных типов данных.

**Переопределение методов** — это процесс создания в дочернем классе метода с тем же именем, что и в родительском классе, но с отличающейся реализацией.

### Пример базового наследования (уровень 1 - начальный)

```python
class GameCharacter:
    """
    Базовый класс для игрового персонажа
    """
    def __init__(self, name, health, attack_power, character_class="warrior"):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.character_class = character_class
        self.level = 1
        self.is_alive = True
    
    def take_damage(self, damage):
        """
        Получение урона персонажем
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} погибает!")
        return damage
    
    def attack(self, target):
        """
        Атака цели
        """
        if self.is_alive and target.is_alive:
            print(f"{self.name} атакует {target.name} на {self.attack_power} урона")
            target.take_damage(self.attack_power)
        else:
            print(f"{self.name} не может атаковать, так как {'мертв' if not self.is_alive else 'цель мертва'}")
    
    def get_info(self):
        """
        Получение информации о персонаже
        """
        return f"{self.name} ({self.character_class}) - Уровень {self.level}, Здоровье: {self.health}/{self.max_health}"

class PlayerCharacter(GameCharacter):
    """
    Класс игрока - наследуется от GameCharacter
    """
    def __init__(self, name, health, attack_power, character_class="warrior", player_id=1):
        super().__init__(name, health, attack_power, character_class)  # Вызов конструктора родительского класса
        self.player_id = player_id
        self.experience = 0
        self.inventory = []
        self.guild = None
    
    def level_up(self):
        """
        Повышение уровня игрока
        """
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 5
        print(f"{self.name} достиг {self.level} уровня!")
    
    def gain_experience(self, exp):
        """
        Получение опыта
        """
        self.experience += exp
        print(f"{self.name} получил {exp} опыта. Всего: {self.experience}")
        # Проверяем, нужно ли повысить уровень
        if self.experience >= self.level * 100:
            self.level_up()
            self.experience = 0  # Сбрасываем опыт после повышения уровня

# Пример использования
player = PlayerCharacter("Артур", 100, 20, "warrior", 1)
print(player.get_info())  # Артур (warrior) - Уровень 1, Здоровье: 100/100
player.gain_experience(150)
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание базового класса и наследника

Создайте базовый класс `Animal` и класс-наследник `Pet`. Реализуйте атрибуты и методы для обоих классов.

**Шаги выполнения:**
1. Создайте класс `Animal` с конструктором `__init__`
2. Добавьте атрибуты: `name`, `species`, `age`, `health`
3. Добавьте методы: `make_sound()`, `eat()`, `sleep()`
4. Создайте класс `Pet` наследующийся от `Animal`
5. Добавьте специфичные атрибуты для питомца: `owner`, `happiness`
6. Переопределите метод `make_sound()` для класса `Pet`
7. Создайте экземпляр класса `Pet` и протестируйте его методы

```python
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

# Пример использования (после реализации)
# my_pet = Pet("Барсик", "кот", 3, "Иван")
# print(my_pet.make_sound())  # Должно вывести звук питомца
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Animal:
    def __init__(self, name, species, age, health=100):
        self.name = name
        self.species = species
        self.age = age
        self.health = health

    def make_sound(self):
        return f"{self.name} издает звук"

    def eat(self):
        print(f"{self.name} ест и восстанавливает здоровье")
        self.health = min(100, self.health + 10)

    def sleep(self):
        print(f"{self.name} спит и отдыхает")
        self.health = min(100, self.health + 5)

class Pet(Animal):
    def __init__(self, name, species, age, owner, health=100):
        super().__init__(name, species, age, health)
        self.owner = owner
        self.happiness = 50  # Уровень счастья питомца

    def make_sound(self):
        return f"{self.name} радостно мяукает!"  # или лает, в зависимости от вида

    def play_with_owner(self):
        print(f"{self.name} играет с хозяином {self.owner}")
        self.happiness = min(100, self.happiness + 20)
        self.health = min(100, self.health + 5)
```

</details>

#### Задание 1.2: Наследование в игровом контексте

Создайте базовый класс `Vehicle` и два класса-наследника: `Car` и `Airplane`. Реализуйте методы движения для каждого транспортного средства.

```python
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

# Пример использования (после реализации)
# my_car = Car("Toyota", "Camry", 2020, 180, 60)
# my_airplane = Airplane("Boeing", "737", 2019, 850, 12000)
# print(my_car.move())  # Должно описать движение автомобиля
# print(my_airplane.move())  # Должно описать движение самолета
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Vehicle:
    def __init__(self, brand, model, year, max_speed):
        self.brand = brand
        self.model = model
        self.year = year
        self.max_speed = max_speed

    def move(self):
        return f"{self.brand} {self.model} движется"

    def get_info(self):
        return f"{self.year} {self.brand} {self.model}, макс. скорость: {self.max_speed} км/ч"

class Car(Vehicle):
    def __init__(self, brand, model, year, max_speed, fuel_capacity):
        super().__init__(brand, model, year, max_speed)
        self.fuel_capacity = fuel_capacity
        self.current_fuel = fuel_capacity  # Текущий уровень топлива

    def move(self):
        if self.current_fuel > 0:
            self.current_fuel -= 1  # Расход топлива
            return f"{self.brand} {self.model} едет по дороге со скоростью {self.max_speed} км/ч"
        else:
            return f"{self.brand} {self.model} не может двигаться - нет топлива"

class Airplane(Vehicle):
    def __init__(self, brand, model, year, max_speed, max_altitude):
        super().__init__(brand, model, year, max_speed)
        self.max_altitude = max_altitude
        self.altitude = 0  # Текущая высота

    def move(self):
        self.altitude = min(self.max_altitude, self.altitude + 1000)  # Подъем на высоту
        return f"{self.brand} {self.model} летит на высоте {self.altitude} м со скоростью {self.max_speed} км/ч"
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Множественное наследование в игровом контексте

Создайте систему классов с множественным наследованием, где персонаж может быть одновременно и магом, и воином. Используйте классы `Movable`, `Attackable`, `MagicUser`.

**Шаги выполнения:**
1. Создайте класс `Movable` с методом `move(dx, dy)`
2. Создайте класс `Attackable` с методом `attack(target)`
3. Создайте класс `MagicUser` с методом `cast_spell(spell_name)`
4. Создайте класс `HybridCharacter`, использующий множественное наследование
5. Реализуйте корректный вызов конструкторов родительских классов
6. Протестируйте функциональность

```python
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

# Пример использования (после реализации)
# hero = HybridCharacter("Герой", health=150, speed=2.0, attack_power=25, mana=100)
# hero.move(10, 5)
# enemy = type('Enemy', (), {'name': 'Монстр', 'health': 50})()  # Создаем временного врага
# hero.attack(enemy)
# hero.cast_spell("Огненный шар", enemy)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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

# Пример использования
hero = HybridCharacter("Герой", health=150, speed=2.0, attack_power=25, mana=100)
print(f"Герой создан: {hero.name}, позиция: {hero.position}, мана: {hero.mana}")

hero.move(10, 5)
enemy = type('Enemy', (), {'name': 'Монстр', 'health': 50})()  # Создаем временного врага
hero.attack(enemy)
hero.cast_spell("Огненный шар", enemy)
print(f"Здоровье врага после атак: {enemy.health}")
```

</details>

#### Задание 2.2: Полиморфизм в боевой системе

Создайте боевую систему, в которой разные типы персонажей могут по-разному атаковать, используя полиморфизм. Реализуйте общий интерфейс атаки, но с разными реализациями.

```python
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

# Пример использования (после реализации)
# warrior = Fighter("Конан", 120, 25)
# mage = Mage("Гендальф", 80, 15)
# archer = Archer("Робин", 90, 20)
# battle_round(warrior, mage)  # Воин атакует мага
# battle_round(mage, archer)   # Маг атакует лучника
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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
    print(f"\n{attacker.name} атакует {defender.name}!")
    damage = attacker.special_attack(defender)
    print(f"Здоровье {defender.name}: {defender.health}/{defender.max_health}")

# Пример использования
warrior = Fighter("Конан", 120, 25)
mage = Mage("Гендальф", 80, 15)
archer = Archer("Робин", 90, 20)

battle_round(warrior, mage)  # Воин атакует мага
battle_round(mage, archer)   # Маг атакует лучника
battle_round(archer, warrior) # Лучник атакует воина
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Абстрактные классы для игровых сущностей

Создайте систему абстрактных классов для игровых сущностей, используя модуль `abc`. Реализуйте иерархию классов, включающую абстрактные методы, которые должны быть реализованы в дочерних классах.

**Шаги выполнения:**
1. Создайте абстрактный класс `GameEntity` с абстрактными методами
2. Создайте классы-наследники, реализующие абстрактные методы
3. Реализуйте полиморфизм с использованием абстрактных классов
4. Создайте систему взаимодействия между сущностями

```python
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

# Пример использования (после реализации)
# warrior = Warrior("Артур", health=150, armor=15, level=5)
# dragon = Dragon("Смауг", health=500, armor=30, level=15)
# warrior.interact(dragon)
# dragon.interact(warrior)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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
        if isinstance(other_entity, Character):
            print(f"{self.name} приветствует {other_entity.name}")
        elif isinstance(other_entity, Monster) and other_entity.is_alive:
            print(f"{self.name} атакует {other_entity.name}!")
            self.attack(other_entity)
        else:
            print(f"{self.name} осматривается вокруг")
    
    def update(self, delta_time):
        # Восстанавливаем немного ярости со временем
        self.rage = min(100, self.rage + delta_time * 2)
        if self.health < self.max_health * 0.3 and self.rage > 50:
            # При низком здоровье используем ярость для лечения
            heal_amount = self.rage // 4
            self.heal(heal_amount)
            self.rage //= 2
            print(f"{self.name} использует ярость для лечения на {heal_amount} здоровья")
    
    def use_special_ability(self):
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
        if isinstance(other_entity, Character) and other_entity.is_alive:
            print(f"{self.name} рычит на {other_entity.name} и готовится к атаке!")
        else:
            print(f"{self.name} гордо парит в небе")
    
    def update(self, delta_time):
        # Дракон восстанавливает немного здоровья в броне
        if self.health < self.max_health:
            recovery = self.armor * 0.1 * delta_time
            self.heal(recovery)
            print(f"{self.name} восстанавливает {recovery:.1f} здоровья благодаря своей броне")
    
    def ai_behavior(self, targets):
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
    
    def fly_to_position(self, x, y):
        print(f"{self.name} летит к позиции ({x}, {y})")

# Пример использования
print("Создание игровых сущностей:")
warrior = Warrior("Артур", health=150, armor=15, level=5)
dragon = Dragon("Смауг", health=500, armor=30, level=15)

print(f"\n{warrior.name} ({type(warrior).__name__}): здоровье {warrior.health}/{warrior.max_health}, ярость {warrior.rage}%")
print(f"{dragon.name} ({type(dragon).__name__}): здоровье {dragon.health}/{dragon.max_health}, броня {dragon.armor}")

print(f"\nВзаимодействие:")
warrior.interact(dragon)
dragon.interact(warrior)

print(f"\nОбновление состояния:")
warrior.update(1.0)
dragon.update(1.0)

print(f"\nСпециальные способности:")
warrior.use_special_ability()
dragon.ai_behavior([warrior])
```

</details>

#### Задание 3.2: Комплексная система с использованием всех концепций

Создайте комплексную систему, объединяющую наследование, полиморфизм и абстрактные классы. Реализуйте систему боя между различными типами существ, где каждый тип имеет уникальные особенности, но все они соответствуют общему интерфейсу.

```python
from abc import ABC, abstractmethod

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

class Warrior(BattleParticipant):
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

class Mage(BattleParticipant):
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

class Healer(BattleParticipant):
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

# Пример использования (после реализации)
# team1 = [Warrior("Конан"), Mage("Мерлин")]
# team2 = [Warrior("Харальд"), Healer("Эльза")]
# all_participants = team1 + team2
# execute_battle_round(all_participants)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

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

class Warrior(BattleParticipant):
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
        return "Танк/Боец"

class Mage(BattleParticipant):
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
        return "Дамагер/Саппорт"

class Healer(BattleParticipant):
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
        if self.mana >= 15 and ally.is_alive and ally.health < ally.max_health:
            heal_amount = min(ally.max_health - ally.health, self.healing_power)
            ally.health += heal_amount
            self.mana -= 15
            return f"{self.name} лечит {ally.name} на {heal_amount} здоровья (мана: {self.mana}/{self.max_mana})"
        return f"{self.name} не может вылечить {ally.name}"
    
    def battle_action(self, opponents, allies):
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
        return "Саппорт/Целитель"

def execute_battle_round(participants):
    """
    Функция, демонстрирующая полиморфизм
    Принимает список участников боя и позволяет каждому выполнить действие
    """
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
team1 = [
    Warrior("Конан"),
    Mage("Мерлин")
]

team2 = [
    Warrior("Харальд"),
    Healer("Эльза")
]

all_participants = team1 + team2

print("Начальное состояние:")
for participant in all_participants:
    print(f"  {participant.name} ({participant.get_role()}): здоровье {participant.health}/{participant.max_health}")

# Выполняем несколько раундов боя
for round_num in range(3):
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
```

</details>

---

## 1. Создание иерархии классов с наследованием

### Пример 1: Базовый класс игрового персонажа и наследование

```python
class GameCharacter:
    """
    Базовый класс для игрового персонажа
    """
    def __init__(self, name, health, attack_power, character_class="warrior"):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.character_class = character_class
        self.level = 1
        self.is_alive = True
    
    def take_damage(self, damage):
        """
        Получение урона персонажем
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} погибает!")
        return damage
    
    def attack(self, target):
        """
        Атака цели
        """
        if self.is_alive and target.is_alive:
            print(f"{self.name} атакует {target.name} на {self.attack_power} урона")
            target.take_damage(self.attack_power)
        else:
            print(f"{self.name} не может атаковать, так как {'мертв' if not self.is_alive else 'цель мертва'}")
    
    def get_info(self):
        """
        Получение информации о персонаже
        """
        return f"{self.name} ({self.character_class}) - Уровень {self.level}, Здоровье: {self.health}/{self.max_health}"

class PlayerCharacter(GameCharacter):
    """
    Класс игрока - наследуется от GameCharacter
    """
    def __init__(self, name, health, attack_power, character_class="warrior", player_id=1):
        super().__init__(name, health, attack_power, character_class)  # Вызов конструктора родительского класса
        self.player_id = player_id
        self.experience = 0
        self.inventory = []
        self.guild = None
    
    def level_up(self):
        """
        Повышение уровня игрока
        """
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 5
        print(f"{self.name} достиг {self.level} уровня!")
    
    def gain_experience(self, exp):
        """
        Получение опыта
        """
        self.experience += exp
        print(f"{self.name} получил {exp} опыта. Всего: {self.experience}")
        # Проверяем, нужно ли повысить уровень
        if self.experience >= self.level * 100:
            self.level_up()
            self.experience = 0  # Сбрасываем опыт после повышения уровня

class NonPlayerCharacter(GameCharacter):
    """
    Класс NPC - наследуется от GameCharacter
    """
    def __init__(self, name, health, attack_power, character_class="warrior", dialogue="Привет, путник!"):
        super().__init__(name, health, attack_power, character_class)
        self.dialogue = dialogue
        self.quest_available = False
        self.merchant = False
    
    def speak(self):
        """
        NPC говорит
        """
        print(f"{self.name} говорит: {self.dialogue}")
    
    def give_quest(self, player):
        """
        Дать квест игроку
        """
        if self.quest_available:
            print(f"{self.name} предлагает квест игроку {player.name}")
        else:
            print(f"{self.name} в данный момент не может предложить квест")

# Пример использования
player = PlayerCharacter("Артур", 100, 20, "warrior", 1)
npc = NonPlayerCharacter("Старик Мерлин", 50, 5, "mage", "Я чувствую магическую силу в тебе...")

print(player.get_info())  # Артур (warrior) - Уровень 1, Здоровье: 100/100
print(npc.get_info())  # Старик Мерлин (mage) - Уровень 1, Здоровье: 50/50

player.gain_experience(150)
npc.speak()
```

---

## 2. Переопределение методов в игровом контексте

### Пример 2: Переопределение методов для различных классов персонажей

```python
class Character:
    """
    Базовый класс для персонажа
    """
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.is_alive = True
    
    def take_damage(self, damage):
        """
        Базовая логика получения урона
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} погибает!")
        return damage
    
    def perform_action(self):
        """
        Выполнение действия (будет переопределен в дочерних классах)
        """
        return f"{self.name} выполняет базовое действие"
    
    def get_character_type(self):
        """
        Получение типа персонажа
        """
        return "Обычный персонаж"

class Warrior(Character):
    """
    Класс воина
    """
    def __init__(self, name, health=120, attack_power=25):
        super().__init__(name, health, attack_power)
        self.rage = 0  # Ярость воина
    
    def perform_action(self):
        # Переопределение метода
        self.rage = min(100, self.rage + 10)  # Накапливаем ярость
        return f"{self.name} атакует с яростью! Ярость: {self.rage}%"
    
    def heavy_strike(self, target):
        """
        Мощный удар с расходованием ярости
        """
        if self.rage >= 30:
            self.rage -= 30
            damage = self.attack_power * 2
            print(f"{self.name} наносит тяжелый удар по {target.name} на {damage} урона")
            target.take_damage(damage)
        else:
            print(f"{self.name} недостаточно ярости для тяжелого удара")
    
    def get_character_type(self):
        # Переопределение метода с расширением
        base_type = super().get_character_type()
        return f"{base_type}, воин"

class Mage(Character):
    """
    Класс мага
    """
    def __init__(self, name, health=80, attack_power=15):
        super().__init__(name, health, attack_power)
        self.mana = 100  # Мана мага
        self.max_mana = 100
    
    def perform_action(self):
        # Переопределение метода с дополнительной функциональностью
        if self.mana >= 20:
            self.mana -= 20
            return f"{self.name} произносит заклинание! Осталось маны: {self.mana}/{self.max_mana}"
        else:
            return f"{self.name} не хватает маны для заклинания"
    
    def cast_spell(self, target, spell_power=1.5):
        """
        Произнесение заклинания
        """
        if self.mana >= 15:
            self.mana -= 15
            damage = self.attack_power * spell_power
            print(f"{self.name} накладывает заклинание на {target.name} на {damage} урона")
            target.take_damage(damage)
        else:
            print(f"{self.name} не хватает маны для заклинания")
    
    def get_character_type(self):
        base_type = super().get_character_type()
        return f"{base_type}, маг"
    
    def restore_mana(self, amount):
        """
        Восстановление маны
        """
        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        restored = self.mana - old_mana
        print(f"{self.name} восстановил {restored} маны. Сейчас: {self.mana}/{self.max_mana}")

class Archer(Character):
    """
    Класс лучника
    """
    def __init__(self, name, health=90, attack_power=20):
        super().__init__(name, health, attack_power)
        self.arrows = 30  # Количество стрел
        self.critical_chance = 0.2  # Шанс критического удара
    
    def perform_action(self):
        # Переопределение метода
        if self.arrows > 0:
            self.arrows -= 1
            # Проверяем критический удар
            if __import__('random').random() < self.critical_chance:
                return f"{self.name} делает критический выстрел! Осталось стрел: {self.arrows}"
            else:
                return f"{self.name} делает выстрел. Осталось стрел: {self.arrows}"
        else:
            return f"{self.name} закончились стрелы!"
    
    def headshot(self, target):
        """
        Выстрел в голову с гарантированным критическим эффектом
        """
        if self.arrows > 0:
            self.arrows -= 1
            damage = self.attack_power * 2.5
            print(f"{self.name} делает выстрел в голову по {target.name} на {damage} урона")
            target.take_damage(damage)
        else:
            print(f"{self.name} закончились стрелы для выстрела в голову")
    
    def get_character_type(self):
        base_type = super().get_character_type()
        return f"{base_type}, лучник"
    
    def reload(self):
        """
        Перезарядка стрел
        """
        self.arrows = 30
        print(f"{self.name} перезаряжается. Стрел снова: {self.arrows}")

# Пример использования
characters = [
    Warrior("Конан"),
    Mage("Гендальф"),
    Archer("Леголас")
]

for character in characters:
    print(character.get_character_type())
    print(character.perform_action())
    print()
```

---

## 3. Применение полиморфизма в игровых системах

### Пример 3: Полиморфизм в действии в боевой системе

```python
from abc import ABC, abstractmethod

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

class Warrior(BattleParticipant):
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
        return "Танк/Боец"

class Mage(BattleParticipant):
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
        return "Дамагер/Саппорт"

class Healer(BattleParticipant):
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
        if self.mana >= 15 and ally.is_alive and ally.health < ally.max_health:
            heal_amount = min(ally.max_health - ally.health, self.healing_power)
            ally.health += heal_amount
            self.mana -= 15
            return f"{self.name} лечит {ally.name} на {heal_amount} здоровья (мана: {self.mana}/{self.max_mana})"
        return f"{self.name} не может вылечить {ally.name}"
    
    def battle_action(self, opponents, allies):
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
        return "Саппорт/Целитель"

def execute_battle_round(participants):
    """
    Функция, демонстрирующая полиморфизм
    Принимает список участников боя и позволяет каждому выполнить действие
    """
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
team1 = [
    Warrior("Конан"),
    Mage("Мерлин")
]

team2 = [
    Warrior("Харальд"),
    Healer("Эльза")
]

all_participants = team1 + team2

print("Начальное состояние:")
for participant in all_participants:
    print(f"  {participant.name} ({participant.get_role()}): здоровье {participant.health}/{participant.max_health}")

# Выполняем несколько раундов боя
for round_num in range(3):
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
```

---

## 4. Использование абстрактных классов

### Пример 4: Использование абстрактных классов для игровых сущностей

```python
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

class LivingEntity(GameEntity):
    """
    Абстрактный класс живой сущности
    """
    def __init__(self, name, health, armor=0):
        super().__init__(name, health)
        self.armor = armor
    
    def take_damage(self, damage):
        """
        Переопределение получения урона с учетом брони
        """
        reduced_damage = max(1, damage - self.armor)  # Минимум 1 урон
        return super().take_damage(reduced_damage)

class Character(LivingEntity):
    """
    Абстрактный класс персонажа
    """
    def __init__(self, name, health, armor=0, level=1):
        super().__init__(name, health, armor)
        self.level = level
        self.experience = 0
    
    @abstractmethod
    def use_special_ability(self):
        """
        Использование специальной способности (должно быть реализовано в дочернем классе)
        """
        pass

class Monster(LivingEntity):
    """
    Абстрактный класс монстра
    """
    def __init__(self, name, health, armor=0, monster_type="common"):
        super().__init__(name, health, armor)
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
        if isinstance(other_entity, Character):
            print(f"{self.name} приветствует {other_entity.name}")
        elif isinstance(other_entity, Monster) and other_entity.is_alive:
            print(f"{self.name} атакует {other_entity.name}!")
            self.attack(other_entity)
        else:
            print(f"{self.name} осматривается вокруг")
    
    def update(self, delta_time):
        # Восстанавливаем немного ярости со временем
        self.rage = min(100, self.rage + delta_time * 2)
        if self.health < self.max_health * 0.3 and self.rage > 50:
            # При низком здоровье используем ярость для лечения
            heal_amount = self.rage // 4
            self.heal(heal_amount)
            self.rage //= 2
            print(f"{self.name} использует ярость для лечения на {heal_amount} здоровья")
    
    def use_special_ability(self):
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
        super().__init__(name, health, armor, "boss")
        self.level = level
        self.fire_damage = 30
        self.wing_span = 20  # Размах крыльев в метрах
    
    def interact(self, other_entity):
        if isinstance(other_entity, Character) and other_entity.is_alive:
            print(f"{self.name} рычит на {other_entity.name} и готовится к атаке!")
        else:
            print(f"{self.name} гордо парит в небе")
    
    def update(self, delta_time):
        # Дракон восстанавливает немного здоровья в броне
        if self.health < self.max_health:
            recovery = self.armor * 0.1 * delta_time
            self.heal(recovery)
            print(f"{self.name} восстанавливает {recovery:.1f} здоровья благодаря своей броне")
    
    def ai_behavior(self, targets):
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
    
    def fly_to_position(self, x, y):
        print(f"{self.name} летит к позиции ({x}, {y})")

# Пример использования
print("Создание игровых сущностей:")

warrior = Warrior("Артур", health=150, armor=15, level=5)
dragon = Dragon("Смауг", health=500, armor=30, level=15)

print(f"\n{warrior.name} ({type(warrior).__name__}): здоровье {warrior.health}/{warrior.max_health}, ярость {warrior.rage}%")
print(f"{dragon.name} ({type(dragon).__name__}): здоровье {dragon.health}/{dragon.max_health}, броня {dragon.armor}")

print(f"\nВзаимодействие:")
warrior.interact(dragon)
dragon.interact(warrior)

print(f"\nОбновление состояния:")
warrior.update(1.0)
dragon.update(1.0)

print(f"\nСпециальные способности:")
warrior.use_special_ability()
dragon.ai_behavior([warrior])
```

---

## 5. Практические задания в игровом контексте

### Задание 1: Иерархия классов для игровых существ

Создайте иерархию классов для существ в фэнтезийной игре:
- `Creature` (абстрактный класс)
- `Beast` (дикая природа)
- `Undead` (нежить)
- `Elemental` (стихийные существа)

Каждый класс должен реализовать методы:
- `hunt(prey)` - охота на жертву
- `defend()` - защита от атаки
- `move(location)` - перемещение между локациями

```python
from abc import ABC, abstractmethod

class Creature(ABC):
    """
    Абстрактный класс существа
    """
    def __init__(self, name, health, strength, creature_type="unknown"):
        # ВАШ КОД ЗДЕСЬ
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.creature_type = creature_type
        self.is_alive = True
    
    @abstractmethod
    def hunt(self, prey):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def defend(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def move(self, location):
        # ВАШ КОД ЗДЕСЯ
        pass

class Beast(Creature):
    """
    Класс дикого зверя
    """
    def __init__(self, name, health, strength, terrain_preference="forest"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, health, strength, "beast")
        self.terrain_preference = terrain_preference
        self.hunting_aggression = 70  # Уровень агрессии при охоте от 0 до 100
    
    def hunt(self, prey):
        # ВАШ КОД ЗДЕСЯ
        import random
        success_rate = self.hunting_aggression / 100.0
        if random.random() < success_rate:
            damage = self.strength * 0.8
            prey.take_damage(damage)
            print(f"{self.name} успешно охотится на {prey.name} и наносит {damage} урона")
            return True
        else:
            print(f"{self.name} неудачно охотится на {prey.name}")
            return False
    
    def defend(self):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} рычит и оскаливает зубы, пугая противника")
        return self.strength * 0.3  # Небольшой контроль урона
    
    def move(self, location):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} перемещается в {location} используя знание местности {self.terrain_preference}")
        return True

class Undead(Creature):
    """
    Класс нежити
    """
    def __init__(self, name, health, strength, undead_type="skeleton"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, health, strength, "undead")
        self.undead_type = undead_type
        self.resistance_to_holy = 0.5  # Сопротивление святому урону в процентах
    
    def hunt(self, prey):
        # ВАШ КОД ЗДЕСЯ
        damage = self.strength * 1.1  # Нежить наносит немного больше урона
        prey.take_damage(damage)
        print(f"{self.name} ({self.undead_type}) атакует {prey.name} и наносит {damage} урона")
        return True
    
    def defend(self):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} использует магическую ауру для защиты")
        return self.strength * 0.4  # Средняя защита за счет магии
    
    def move(self, location):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} перемещается в {location} в поисках теплой плоти")
        return True

class Elemental(Creature):
    """
    Класс стихийного существа
    """
    def __init__(self, name, health, strength, element_type="fire"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, health, strength, "elemental")
        self.element_type = element_type
        self.elemental_affinity = element_type  # Стихия, к которой существо наиболее близко
    
    def hunt(self, prey):
        # ВАШ КОД ЗДЕСЯ
        elemental_damage_multipliers = {
            "fire": 1.0,
            "water": 0.8,
            "earth": 1.2,
            "air": 0.9
        }
        multiplier = elemental_damage_multipliers.get(self.element_type, 1.0)
        damage = self.strength * multiplier
        prey.take_damage(damage)
        print(f"{self.name} ({self.element_type}) атакует {prey.name} стихийной атакой на {damage} урона")
        return True
    
    def defend(self):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} создает стихийный барьер из {self.element_type}")
        return self.strength * 0.5  # Высокая защита
    
    def move(self, location):
        # ВАШ КОД ЗДЕСЯ
        print(f"{self.name} перемещается в {location} в форме {self.element_type}")
        return True

# Тестирование
beast = Beast("Волк", 80, 15, "forest")
undead = Undead("Скелет-воин", 60, 12, "skeleton")
elemental = Elemental("Огненный элементаль", 100, 20, "fire")

creatures = [beast, undead, elemental]
for creature in creatures:
    print(f"{creature.name} ({creature.creature_type}): здоровье {creature.health}/{creature.max_health}")
    creature.move("пещера")
    print()
```

### Задание 2: Иерархия классов для оружия

Создайте иерархию классов для оружия:
- `Weapon` (абстрактный класс)
- `MeleeWeapon` (ручное оружие)
- `RangedWeapon` (дальнобойное оружие)
- `MagicWeapon` (магическое оружие)

Каждый класс должен реализовать свои методы и атрибуты.

```python
from abc import ABC, abstractmethod

class Weapon(ABC):
    """
    Абстрактный класс оружия
    """
    def __init__(self, name, damage, durability, weapon_type="generic"):
        # ВАШ КОД ЗДЕСЯ
        self.name = name
        self.damage = damage
        self.durability = durability
        self.max_durability = durability
        self.weapon_type = weapon_type
        self.enchanted = False
    
    @abstractmethod
    def attack(self, target):
        # ВАШ КОД ЗДЕСЯ
        pass
    
    @abstractmethod
    def equip(self, character):
        # ВАШ КОД ЗДЕСЯ
        pass
    
    def is_broken(self):
        # ВАШ КОД ЗДЕСЯ
        return self.durability <= 0

class MeleeWeapon(Weapon):
    """
    Ручное оружие
    """
    def __init__(self, name, damage, durability, weapon_class="sword"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, damage, durability, "melee")
        self.weapon_class = weapon_class  # Тип оружия: sword, axe, mace, etc.
        self.attack_range = 1  # Ближний бой
    
    def attack(self, target):
        # ВАШ КОД ЗДЕСЯ
        if self.is_broken():
            print(f"{self.name} сломано и не может атаковать")
            return 0
        
        actual_damage = self.damage
        if self.enchanted:
            actual_damage *= 1.5  # Зачарованное оружие наносит больше урона
            
        print(f"{self.name} наносит {actual_damage} урона по {target.name}")
        target.take_damage(actual_damage)
        self.durability -= 1  # Износ оружия при атаке
        return actual_damage
    
    def equip(self, character):
        # ВАШ КОД ЗДЕСЯ
        print(f"{character.name} экипировал {self.name}")
        character.attack_power += self.damage * 0.3  # Бонус к атаке
        return True

class RangedWeapon(Weapon):
    """
    Дальнобойное оружие
    """
    def __init__(self, name, damage, durability, ammo_type="arrows"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, damage, durability, "ranged")
        self.ammo_type = ammo_type
        self.ammo_count = 30  # Количество боеприпасов
        self.attack_range = 10  # Дальность атаки
    
    def attack(self, target):
        # ВАШ КОД ЗДЕСЯ
        if self.is_broken():
            print(f"{self.name} сломано и не может атаковать")
            return 0
        if self.ammo_count <= 0:
            print(f"Закончились боеприпасы для {self.name}")
            return 0
        
        self.ammo_count -= 1
        actual_damage = self.damage
        if self.enchanted:
            actual_damage *= 1.3  # Зачарованное дальнобойное оружие
            
        print(f"{self.name} стреляет в {target.name} и наносит {actual_damage} урона (боеприпасов осталось: {self.ammo_count})")
        target.take_damage(actual_damage)
        self.durability -= 0.5  # Меньше износа для дальнобойного оружия
        return actual_damage
    
    def equip(self, character):
        # ВАШ КОД ЗДЕСЯ
        print(f"{character.name} экипировал {self.name}")
        character.attack_power += self.damage * 0.2  # Бонус к атаке
        return True
    
    def reload(self):
        # ВАШ КОД ЗДЕСЯ
        self.ammo_count = 30
        print(f"{self.name} перезаряжено. Боеприпасов: {self.ammo_count}")

class MagicWeapon(Weapon):
    """
    Магическое оружие
    """
    def __init__(self, name, damage, durability, magic_type="fire"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, damage, durability, "magic")
        self.magic_type = magic_type
        self.mana_cost = 10  # Стоимость использования в мане
        self.attack_range = 5  # Средняя дальность
    
    def attack(self, target):
        # ВАШ КОД ЗДЕСЯ
        if self.is_broken():
            print(f"{self.name} сломано и не может атаковать")
            return 0
        # Предполагаем, что у цели есть атрибут mana или он равен 0
        if hasattr(target, 'mana') and target.mana < self.mana_cost:
            print(f"{target.name} недостаточно маны для сопротивления магии {self.name}")
        elif hasattr(target, 'mana'):
            target.mana -= self.mana_cost  # Поглощение маны цели
        
        actual_damage = self.damage
        if self.enchanted:
            actual_damage *= 1.7  # Зачарованное магическое оружие наносит больше урона
            
        print(f"{self.name} накладывает {self.magic_type} заклинание на {target.name} и наносит {actual_damage} урона")
        target.take_damage(actual_damage)
        self.durability -= 0.8  # Средний износ
        return actual_damage
    
    def equip(self, character):
        # ВАШ КОД ЗДЕСЯ
        print(f"{character.name} экипировал {self.name}")
        character.attack_power += self.damage * 0.4  # Высокий бонус к атаке
        if hasattr(character, 'mana'):
            character.mana += 20  # Бонус к мане при экипировке
        return True

# Тестирование
melee = MeleeWeapon("Меч Света", 25, 100, "sword")
ranged = RangedWeapon("Лук Эльфов", 20, 80, "arrows")
magic = MagicWeapon("Посох Огня", 30, 70, "fire")

weapons = [melee, ranged, magic]
character = Warrior("Артур", 100, 10)  # Используем класс Warrior из предыдущего примера

for weapon in weapons:
    print(f"Оружие: {weapon.name} ({weapon.weapon_type})")
    weapon.equip(character)
    print(f"Прочность: {weapon.durability}/{weapon.max_durability}")
    print()
```

### Задание 3: Иерархия классов для игровых локаций

Создайте иерархию классов для игровых локаций:
- `Location` (абстрактный класс)
- `Dungeon` (подземелье)
- `Town` (город)
- `Wilderness` (дикая местность)

Каждый класс должен реализовать методы:
- `enter(player)`
- `exit(player)`
- `get_danger_level()`

```python
from abc import ABC, abstractmethod

class Location(ABC):
    """
    Абстрактный класс локации
    """
    def __init__(self, name, size, climate="temperate"):
        # ВАШ КОД ЗДЕСЯ
        self.name = name
        self.size = size  # Размер локации (маленькая, средняя, большая)
        self.climate = climate
        self.visitors = []  # Список посетителей
    
    @abstractmethod
    def enter(self, player):
        # ВАШ КОД ЗДЕСЯ
        pass
    
    @abstractmethod
    def exit(self, player):
        # ВАШ КОД ЗДЕСЯ
        pass
    
    @abstractmethod
    def get_danger_level(self):
        # ВАШ КОД ЗДЕСЯ
        pass

class Dungeon(Location):
    """
    Подземелье
    """
    def __init__(self, name, size, climate="underground", difficulty="normal"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, size, climate)
        self.difficulty = difficulty  # normal, hard, legendary
        self.traps = []
        self.treasures = []
        self.monsters = []
    
    def enter(self, player):
        # ВАШ КОД ЗДЕСЯ
        self.visitors.append(player)
        print(f"{player.name} входит в подземелье {self.name}. Уровень сложности: {self.difficulty}")
        if player.level < 3 and self.difficulty in ["hard", "legendary"]:
            print("Предупреждение: уровень сложности может быть слишком высок для вашего уровня!")
        return True
    
    def exit(self, player):
        # ВАШ КОД ЗДЕСЯ
        if player in self.visitors:
            self.visitors.remove(player)
            print(f"{player.name} покидает подземелье {self.name}")
            return True
        else:
            print(f"{player.name} не находится в подземелье {self.name}")
            return False
    
    def get_danger_level(self):
        # ВАШ КОД ЗДЕСЯ
        danger_multipliers = {"easy": 0.5, "normal": 1.0, "hard": 2.0, "legendary": 3.0}
        return danger_multipliers.get(self.difficulty, 1.0) * 2  # Подземелья обычно опаснее

class Town(Location):
    """
    Город
    """
    def __init__(self, name, size, climate="temperate", population=1000):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, size, climate)
        self.population = population
        self.shops = []
        self.inns = []
        self.guard_efficiency = 0.9  # Эффективность городской стражи (0-1)
    
    def enter(self, player):
        # ВАШ КОД ЗДЕСЯ
        self.visitors.append(player)
        print(f"{player.name} входит в город {self.name}. Население: {self.population} человек")
        if player.is_alive:  # Только живые игроки могут посещать город
            print("Добро пожаловать в безопасную зону!")
        return True
    
    def exit(self, player):
        # ВАШ КОД ЗДЕСЯ
        if player in self.visitors:
            self.visitors.remove(player)
            print(f"{player.name} покидает город {self.name}")
            return True
        else:
            print(f"{player.name} не находится в городе {self.name}")
            return False
    
    def get_danger_level(self):
        # ВАШ КОД ЗДЕСЯ
        # Города обычно безопасны, но зависит от эффективности стражи
        return (1 - self.guard_efficiency) * 0.5 # Чем ниже эффективность, тем выше опасность

class Wilderness(Location):
    """
    Дикая местность
    """
    def __init__(self, name, size, climate="varied", wildlife_density="moderate"):
        # ВАШ КОД ЗДЕСЯ
        super().__init__(name, size, climate)
        self.wildlife_density = wildlife_density  # low, moderate, high, extreme
        self.weather_conditions = "clear"  # Текущие погодные условия
        self.hidden_paths = []
    
    def enter(self, player):
        # ВАШ КОД ЗДЕСЯ
        self.visitors.append(player)
        print(f"{player.name} входит в дикую местность {self.name}. Плотность дикой природы: {self.wildlife_density}")
        if self.wildlife_density == "extreme":
            print("Будьте осторожны: здесь обитает много опасных существ!")
        return True
    
    def exit(self, player):
        # ВАШ КОД ЗДЕСЯ
        if player in self.visitors:
            self.visitors.remove(player)
            print(f"{player.name} покидает дикую местность {self.name}")
            return True
        else:
            print(f"{player.name} не находится в дикой местности {self.name}")
            return False
    
    def get_danger_level(self):
        # ВАШ КОД ЗДЕСЯ
        density_multipliers = {"low": 0.5, "moderate": 1.0, "high": 1.5, "extreme": 2.5}
        return density_multipliers.get(self.wildlife_density, 1.0)

# Тестирование
dungeon = Dungeon("Подземелье Темного Лорда", "large", "underground", "hard")
town = Town("Город Милтарион", "medium", "temperate", 5000)
wilderness = Wilderness("Лес Эндар", "huge", "temperate", "high")

locations = [dungeon, town, wilderness]
player = Warrior("Артур", 100, 10)  # Используем класс Warrior из предыдущего примера

for location in locations:
    print(f"Локация: {location.name} ({location.__class__.__name__})")
    location.enter(player)
    print(f"Уровень опасности: {location.get_danger_level():.2f}")
    location.exit(player)
    print()
```

---

## 6. Дополнительные задания

### Задание 4: Игровая система классов

Создайте полную иерархию классов для ролевой игры с классами:
- `Fighter`
- `Wizard` 
- `Rogue`
- `Cleric`

### Задание 5: Система крафта предметов

Расширьте пример с оружием, добавив систему крафта и улучшения предметов с использованием наследования и полиморфизма.

---

## Контрольные вопросы:
1. В чем разница между наследованием и композицией в игровом контексте?
2. Что такое полиморфизм и как он реализуется в боевых системах?
3. Как использовать ключевое слово super() в иерархиях игровых классов?
4. Что такое абстрактный класс и зачем он нужен в игровых сущностях?
5. Как реализовать множественное наследование в игровых персонажах?
6. В чем преимущества использования абстрактных классов в игровых системах?
7. Как обеспечить правильный порядок вызова методов при множественном наследовании?
8. Как использовать полиморфизм для упрощения боевой системы?
9. Какие проблемы могут возникнуть при использовании множественного наследования?
10. Какие преимущества дает разделение на абстрактные и конкретные классы?