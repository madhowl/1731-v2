# Практическое занятие 11: ООП - абстрактные классы и интерфейсы в игровом контексте

## Создание абстрактных классов и интерфейсов для игровых сущностей

### Цель занятия:
Научиться создавать абстрактные классы и интерфейсы в Python, определять абстрактные методы, использовать модуль abc для создания четкой архитектуры игровых систем и обеспечения обязательной реализации методов в дочерних классах игровых сущностей.

### Задачи:
1. Создать абстрактные классы игровых сущностей с абстрактными методами
2. Реализовать интерфейсы для боевых действий
3. Применить принципы ООП на практике в игровом контексте
4. Обеспечить обязательную реализацию методов в дочерних классах

### План работы:
1. Создание абстрактного класса игровой сущности
2. Определение абстрактных и конкретных методов
3. Создание интерфейсов для боевых действий
4. Реализация наследников абстрактных классов
5. Практические задания в игровом контексте

---
# Практическое занятие 11: ООП - абстрактные классы и интерфейсы в игровом контексте

## Создание абстрактных классов и интерфейсов для игровых сущностей

### Цель занятия:
Научиться создавать абстрактные классы и интерфейсы в Python, определять абстрактные методы, использовать модуль abc для создания четкой архитектуры игровых систем и обеспечения обязательной реализации методов в дочерних классах игровых сущностей.

### Задачи:
1. Создать абстрактные классы игровых сущностей с абстрактными методами
2. Реализовать интерфейсы для боевых действий
3. Применить принципы ООП на практике в игровом контексте
4. Обеспечить обязательную реализацию методов в дочерних классах

---

## 1. Теоретическая часть

### Основные понятия абстрактных классов

**Абстрактный класс** — это класс, который не может быть инстанцирован напрямую и содержит один или несколько абстрактных методов. Он служит шаблоном для других классов, которые должны реализовать абстрактные методы. В Python абстрактные классы создаются с помощью модуля `abc` (Abstract Base Classes).

**Абстрактный метод** — это метод, который объявлен в абстрактном классе, но не содержит реализации. Все классы, наследующиеся от абстрактного класса, обязаны реализовать этот метод, иначе они также будут считаться абстрактными и не смогут быть инстанцированы.

**Интерфейс** — это абстрактный класс, содержащий только абстрактные методы. В Python интерфейсы реализуются через абстрактные классы, в которых все методы являются абстрактными.

### Пример простого абстрактного класса (уровень 1 - начальный)

```python
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
        Абстрактный метод взаимодействия с другой игровой сущностью
        """
        pass

    @abstractmethod
    def update(self, delta_time):
        """
        Абстрактный метод обновления состояния сущности
        """
        pass

    def get_info(self):
        """
        Конкретный метод получения информации о сущности
        """
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({status}): здоровье {self.health}/{self.max_health}, позиция {self.position}"

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

# Создание экземпляра класса
player = PlayerCharacter("Артур", 100, (0, 0), 5)
npc = NonPlayerCharacter("Старик Мерлин", 50, (10, 10), "Я чувствую магическую силу в тебе...")

print(player.get_info())  # Артур (жив): здоровье 100/100, позиция (0, 0)
print(npc.get_info())     # Старик Мерлин (жив): здоровье 50/50, позиция (10, 10)

player.interact(npc)      # Артур взаимодействует с Старик Мерлин: Я чувствую магическую силу в тебе...
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание интерфейса для боевых действий

Создайте интерфейс `Attackable` с методами: `take_damage(damage)` и `deal_damage(target)`. Реализуйте этот интерфейс в классе `Warrior` с атрибутами: имя, здоровье, сила атаки, защита. Реализуйте метод `get_combat_info()`, который выводит боевую информацию о персонаже.

**Шаги выполнения:**
1. Создайте абстрактный класс `Attackable` с конструктором `ABC`
2. Добавьте абстрактные методы: `take_damage(damage)`, `deal_damage(target)`
3. Создайте класс `Warrior`, реализующий интерфейс `Attackable`
4. Добавьте атрибуты: `name`, `health`, `attack_power`, `defense`, `is_alive`
5. Реализуйте абстрактные методы по-своему
6. Создайте метод `get_combat_info()` для получения боевой информации
7. Создайте экземпляр класса и протестируйте его методы

```python
from abc import ABC, abstractmethod

class Attackable(ABC):
    @abstractmethod
    def take_damage(self, damage):
        # ВАШ КОД ЗДЕСЬ - реализуйте получение урона
        pass  # Замените на ваш код

    @abstractmethod
    def deal_damage(self, target):
        # ВАШ КОД ЗДЕСЬ - реализуйте нанесение урона цели
        pass  # Замените на ваш код

class Warrior(Attackable):
    def __init__(self, name, health, attack_power, defense=5):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    def take_damage(self, damage):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение урона с учетом защиты
        pass  # Замените на ваш код

    def deal_damage(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте нанесение урона цели
        pass  # Замените на ваш код

    def get_combat_info(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение боевой информации
        pass  # Замените на ваш код

# Пример использования (после реализации)
# warrior = Warrior("Конан", 120, 25, 8)
# print(warrior.get_combat_info())  # Должно вывести боевую информацию о воине
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

class Attackable(ABC):
    @abstractmethod
    def take_damage(self, damage):
        pass

    @abstractmethod
    def deal_damage(self, target):
        pass

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

    def get_combat_info(self):
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({status}): здоровье {self.health}/{self.max_health}, атака {self.attack_power}, защита {self.defense}"
```

</details>

#### Задание 1.2: Абстрактный класс игрового предмета

Создайте абстрактный класс `InventoryItem` с атрибутами: имя, тип предмета, вес, стоимость и методом `use(character)` который должен быть реализован в дочерних классах. Создайте класс `HealthPotion`, наследующийся от `InventoryItem`, с дополнительным атрибутом `healing_power` и реализуйте метод `use(character)` для восстановления здоровья персонажа.

```python
from abc import ABC, abstractmethod

class InventoryItem(ABC):
    def __init__(self, name, item_type, weight=1.0, value=0):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    @abstractmethod
    def use(self, character):
        # ВАШ КОД ЗДЕСЬ - абстрактный метод использования предмета
        pass  # Замените на ваш код

class HealthPotion(InventoryItem):
    def __init__(self, name="Зелье здоровья", healing_power=50, weight=0.5, value=25):
        # ВАШ КОД ЗДЕСЬ - вызов родительского конструктора
        pass  # Замените на ваш код

    def use(self, character):
        # ВАШ КОД ЗДЕСЬ - реализация использования зелья
        pass  # Замените на ваш код

# Пример использования (после реализации)
# health_potion = HealthPotion("Малое зелье здоровья", 30)
# warrior = Warrior("Артур", 100, 20, 5)
# print(f"Здоровье до: {warrior.health}")
# health_potion.use(warrior)
# print(f"Здоровье после: {warrior.health}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

class InventoryItem(ABC):
    def __init__(self, name, item_type, weight=1.0, value=0):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.value = value
        self.durability = 100  # Прочность предмета

    @abstractmethod
    def use(self, character):
        pass

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
```

</details>


### Уровень 2 - Средний

#### Задание 2.1: Абстрактный класс игрового персонажа

Создайте абстрактный класс `Character` с атрибутами: имя, здоровье, сила атаки, уровень, опыт и методами: `use_special_ability()` (абстрактный), `level_up()` (абстрактный), `rest()` (конкретный). Реализуйте наследников: `Knight`, `Wizard`, `Ranger` с уникальными характеристиками и реализациями абстрактных методов.

**Шаги выполнения:**
1. Создайте абстрактный класс `Character` с конструктором
2. Добавьте атрибуты: `name`, `health`, `max_health`, `attack_power`, `level`, `experience`, `is_alive`
3. Реализуйте абстрактные методы: `use_special_ability()`, `level_up()`
4. Реализуйте конкретный метод `rest()` для восстановления здоровья
5. Создайте классы-наследники с уникальной логикой
6. Протестируйте все классы

```python
from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, health, attack_power, level=1):
        # ВАШ КОД ЗДЕСЬ - инициализация атрибутов
        pass  # Замените на ваш код

    @abstractmethod
    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЬ - абстрактный метод специальной способности
        pass  # Замените на ваш код

    @abstractmethod
    def level_up(self):
        # ВАШ КОД ЗДЕСЬ - абстрактный метод повышения уровня
        pass  # Замените на ваш код

    def rest(self):
        # ВАШ КОД ЗДЕСЬ - конкретный метод отдыха
        pass  # Замените на ваш код

class Knight(Character):
    def __init__(self, name, health=150, attack_power=20, level=1, armor=10):
        # ВАШ КОД ЗДЕСЬ - инициализация рыцаря
        pass  # Замените на ваш код

    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЬ - реализация способности рыцаря
        pass  # Замените на ваш код

    def level_up(self):
        # ВАШ КОД ЗДЕСЬ - реализация повышения уровня рыцаря
        pass  # Замените на ваш код

class Wizard(Character):
    def __init__(self, name, health=90, attack_power=15, level=1, mana=100):
        # ВАШ КОД ЗДЕСЬ - инициализация волшебника
        pass  # Замените на ваш код

    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЯ - реализация способности волшебника
        pass  # Замените на ваш код

    def level_up(self):
        # ВАШ КОД ЗДЕСЯ - реализация повышения уровня волшебника
        pass  # Замените на ваш код

class Ranger(Character):
    def __init__(self, name, health=110, attack_power=18, level=1, arrows=30):
        # ВАШ КОД ЗДЕСЯ - инициализация рейнджера
        pass  # Замените на ваш код

    def use_special_ability(self):
        # ВАШ КОД ЗДЕСЯ - реализация способности рейнджера
        pass  # Замените на ваш код

    def level_up(self):
        # ВАШ КОД ЗДЕСЯ - реализация повышения уровня рейнджера
        pass  # Замените на ваш код

# Пример использования (после реализации)
# knight = Knight("Ланселот")
# wizard = Wizard("Гендальф")
# ranger = Ranger("Леголас")
#
# print(f"Здоровье Ланселота до отдыха: {knight.health}")
# knight.rest()
# print(f"Здоровье Ланселота после отдыха: {knight.health}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

class Character(ABC):
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
```

</details>

#### Задание 2.2: Интерфейс для взаимодействия с окружением

Расширьте абстрактный класс `GameEntity` из примера выше, добавив абстрактные методы для взаимодействия с окружением: `interact_with_environment(environment_object)` и `respond_to_event(event)`. Реализуйте эти методы в классах `PlayerCharacter` и `NonPlayerCharacter` с учетом их различий в поведении.

```python
# ВАШ КОД ЗДЕСЬ - обновите класс GameEntity с новыми абстрактными методами
# и реализуйте их в классах PlayerCharacter и NonPlayerCharacter
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
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
        Абстрактный метод взаимодействия с другой игровой сущностью
        """
        pass

    @abstractmethod
    def update(self, delta_time):
        """
        Абстрактный метод обновления состояния сущности
        """
        pass

    @abstractmethod
    def interact_with_environment(self, environment_object):
        """
        Абстрактный метод взаимодействия с объектом окружения
        """
        pass

    @abstractmethod
    def respond_to_event(self, event):
        """
        Абстрактный метод реакции на событие
        """
        pass

    def get_info(self):
        """
        Конкретный метод получения информации о сущности
        """
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({status}): здоровье {self.health}/{self.max_health}, позиция {self.position}"

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

    def interact_with_environment(self, environment_object):
        # Игрок может активно взаимодействовать с объектами окружения
        if environment_object == "door" and "ключ" in [item.name for item in self.inventory]:
            print(f"{self.name} открывает дверь ключом из инвентаря")
            return True
        elif environment_object == "chest":
            print(f"{self.name} пытается открыть сундук")
            # Здесь может быть логика проверки ловушек, навыков взлома и т.д.
            return True
        else:
            print(f"{self.name} не может взаимодействовать с {environment_object}")
            return False

    def respond_to_event(self, event):
        # Реакция игрока на событие
        if event == "trap_triggered":
            print(f"{self.name} получает урон от ловушки!")
            self.take_damage(10)
        elif event == "level_complete":
            print(f"{self.name} завершает уровень и получает опыт!")
            self.experience += 100
        elif event == "ally_in_danger":
            print(f"{self.name} спешит на помощь союзнику!")
            # Здесь может быть логика перемещения к союзнику
        else:
            print(f"{self.name} реагирует на событие: {event}")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

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

    def interact_with_environment(self, environment_object):
        # NPC обычно имеет ограниченное взаимодействие с окружением
        if environment_object in ["bench", "chair"]:
            print(f"{self.name} садится отдохнуть")
            return True
        elif environment_object == "shop_counter" and self.merchant:
            print(f"{self.name} обслуживает клиента")
            return True
        else:
            print(f"{self.name} не взаимодействует с {environment_object}")
            return False

    def respond_to_event(self, event):
        # Реакция NPC на событие
        if event == "player_approach":
            print(f"{self.name} замечает приближающегося игрока")
        elif event == "danger_nearby":
            print(f"{self.name} прячется от опасности")
            # Здесь может быть логика изменения поведения
        elif event == "working_hours_end":
            print(f"{self.name} заканчивает рабочий день")
            # Здесь может быть логика завершения торговли или услуг
        else:
            print(f"{self.name} замечает событие: {event}")

# Пример использования
player = PlayerCharacter("Артур", 100, (0, 0), 5)
npc = NonPlayerCharacter("Торговец", 50, (5, 5), "Добро пожаловать в мою лавку!")

print(player.get_info())
player.interact_with_environment("chest")
player.respond_to_event("trap_triggered")
```

</details>


### Уровень 3 - Повышенный

#### Задание 3.1: Комплексная система абстрактных классов

Создайте комплексную систему абстрактных классов для RPG-игры, включающую: `LivingEntity` (наследуется от `GameEntity`), `Mortal` (интерфейс), `MagicalBeing` (интерфейс). Реализуйте классы `Dragon`, `Elf`, `UndeadWarrior` с соответствующими особенностями и возможностями. Убедитесь, что все абстрактные методы реализованы и соблюдены контракты интерфейсов.

**Шаги выполнения:**
1. Создайте абстрактный класс `LivingEntity`, наследующийся от `GameEntity`, с дополнительными атрибутами (например, `mana`, `stamina`)
2. Создайте интерфейсы `Mortal` и `MagicalBeing` с соответствующими методами
3. Создайте классы `Dragon`, `Elf`, `UndeadWarrior`, реализующие нужные абстрактные классы и интерфейсы
4. Реализуйте уникальные способности для каждого класса
5. Продемонстрируйте взаимодействие между различными типами сущностей

```python
from abc import ABC, abstractmethod

class Mortal(ABC):
    @abstractmethod
    def die(self):
        # ВАШ КОД ЗДЕСЬ
        pass  # Замените на ваш код

class MagicalBeing(ABC):
    @abstractmethod
    def cast_spell(self, spell_name, target=None):
        # ВАШ КОД ЗДЕСЬ
        pass  # Замените на ваш код

class LivingEntity(GameEntity):
    def __init__(self, name, health, position=(0, 0), mana=50, stamina=100):
        # ВАШ КОД ЗДЕСЯ - расширьте конструктор
        pass  # Замените на ваш код

    # Добавьте дополнительные абстрактные методы для LivingEntity

class Dragon(LivingEntity, Mortal, MagicalBeing):
    # Реализуйте класс Dragon с уникальными свойствами
    pass  # Замените на ваш код

class Elf(LivingEntity, Mortal, MagicalBeing):
    # Реализуйте класс Elf с уникальными свойствами
    pass  # Замените на ваш код

class UndeadWarrior(LivingEntity, Mortal):
    # Реализуйте класс UndeadWarrior с уникальными свойствами
    pass  # Замените на ваш код

# Пример использования (после реализации)
# dragon = Dragon("Смауг", 500, (100, 100), 200, 150, 50)
# elf = Elf("Леголас", 120, (10, 10), 150, 80, 20)
# undead = UndeadWarrior("Рыцарь смерти", 200, (50, 50), 30, 100, 35)
#
# print(f"Дракон: {dragon.get_info()}")
# print(f"Эльф: {elf.get_info()}")
# print(f"Нежить: {undead.get_info()}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from abc import ABC, abstractmethod

class Mortal(ABC):
    @abstractmethod
    def die(self):
        """Метод смерти сущности"""
        pass

class MagicalBeing(ABC):
    @abstractmethod
    def cast_spell(self, spell_name, target=None):
        """Метод произнесения заклинания"""
        pass

class LivingEntity(GameEntity):
    def __init__(self, name, health, position=(0, 0), mana=50, stamina=100):
        super().__init__(name, health, position)
        self.mana = mana
        self.max_mana = mana
        self.stamina = stamina
        self.max_stamina = stamina

    @abstractmethod
    def regenerate(self, delta_time):
        """Абстрактный метод регенерации ресурсов"""
        pass

    def interact(self, other_entity):
        # Переопределяем метод для LivingEntity
        print(f"{self.name} встречает {other_entity.name}")

    def update(self, delta_time):
        # Переопределяем метод для LivingEntity
        # Регенерация маны и выносливости
        self.mana = min(self.max_mana, self.mana + delta_time * 2)
        self.stamina = min(self.max_stamina, self.stamina + delta_time * 3)
        print(f"Ресурсы {self.name} обновлены: Мана {self.mana:.1f}, Выносливость {self.stamina:.1f}")

class Dragon(LivingEntity, Mortal, MagicalBeing):
    def __init__(self, name, health, position=(0, 0), mana=200, stamina=150, fire_damage=30):
        super().__init__(name, health, position, mana, stamina)
        self.fire_damage = fire_damage
        self.wing_span = 20  # Размах крыльев в метрах
        self.treasure_guarded = True

    def interact_with_environment(self, environment_object):
        if environment_object == "treasure":
            print(f"{self.name} охраняет сокровище")
            return True
        elif environment_object == "cave":
            print(f"{self.name} возвращается в свое логово")
            return True
        else:
            print(f"{self.name} не интересуется {environment_object}")
            return False

    def respond_to_event(self, event):
        if event == "intruder_detected":
            print(f"{self.name} рычит и готовится к бою!")
        elif event == "sleep_time":
            print(f"{self.name} устраивается поудобнее и засыпает")
            self.health = self.max_health # Драконы быстро восстанавливаются во сне
        else:
            print(f"{self.name} реагирует на событие: {event}")

    def regenerate(self, delta_time):
        # Драконы быстро восстанавливают здоровье и ману
        self.health = min(self.max_health, self.health + delta_time * 5)
        self.mana = min(self.max_mana, self.mana + delta_time * 4)

    def die(self):
        self.is_alive = False
        self.health = 0
        print(f"Великий {self.name} пал в бою!")

    def cast_spell(self, spell_name, target=None):
        if self.mana >= 50:
            self.mana -= 50
            print(f"{self.name} испускает поток огня как заклинание '{spell_name}'")
            if target:
                target.take_damage(self.fire_damage * 2)
            return True
        else:
            print(f"{self.name} не хватает маны для заклинания '{spell_name}'")
            return False

    def fly_to(self, destination):
        print(f"{self.name} летит к {destination}")

class Elf(LivingEntity, Mortal, MagicalBeing):
    def __init__(self, name, health, position=(0, 0), mana=150, stamina=80, magic_power=20):
        super().__init__(name, health, position, mana, stamina)
        self.magic_power = magic_power
        self.graceful_movement = True
        self.connection_to_nature = True

    def interact_with_environment(self, environment_object):
        if environment_object == "forest":
            print(f"{self.name} чувствует связь с лесом, восстанавливая ману")
            self.mana = self.max_mana
            return True
        elif environment_object == "ancient_ruins":
            print(f"{self.name} изучает древние руины")
            return True
        else:
            print(f"{self.name} в гармонии с {environment_object}")
            return True

    def respond_to_event(self, event):
        if event == "nature_call":
            print(f"{self.name} откликается на зов природы")
        elif event == "dark_magic_nearby":
            print(f"{self.name} чувствует темную магию и настораживается")
        else:
            print(f"{self.name} элегантно реагирует на событие: {event}")

    def regenerate(self, delta_time):
        # Эльфы восстанавливают ману быстрее в природной среде
        self.mana = min(self.max_mana, self.mana + delta_time * 6)
        self.health = min(self.max_health, self.health + delta_time * 1.5)

    def die(self):
        self.is_alive = False
        self.health = 0
        print(f"{self.name} возвращается к природе...")

    def cast_spell(self, spell_name, target=None):
        if self.mana >= 25:
            self.mana -= 25
            damage = self.magic_power
            print(f"{self.name} произносит '{spell_name}', используя природную магию")
            if target:
                target.take_damage(damage)
            return True
        else:
            print(f"{self.name} не хватает маны для заклинания '{spell_name}'")
            return False

    def hide_in_nature(self):
        print(f"{self.name} маскируется в природе, становясь невидимым")

class UndeadWarrior(LivingEntity, Mortal):
    def __init__(self, name, health, position=(0, 0), mana=30, stamina=100, weapon_damage=25):
        super().__init__(name, health, position, mana, stamina)
        self.weapon_damage = weapon_damage
        self.resistances = ["poison", "fear", "cold"]
        self.vulnerabilities = ["holy_magic", "fire"]

    def interact_with_environment(self, environment_object):
        if environment_object == "graveyard":
            print(f"{self.name} чувствует себя сильнее на кладбище")
            self.health = min(self.max_health, self.health + 10)
            return True
        elif environment_object == "holy_ground":
            print(f"{self.name} страдает на святой земле")
            self.take_damage(5)
            return True
        else:
            print(f"{self.name} нечувствителен к {environment_object}")
            return True

    def respond_to_event(self, event):
        if event == "holy_light":
            print(f"{self.name} испытывает боль от святого света")
            self.take_damage(15)
        elif event == "life_drain":
            print(f"{self.name} получает силу от поглощения жизни")
            self.health = min(self.max_health, self.health + 10)
        else:
            print(f"{self.name} не реагирует на событие: {event}")

    def regenerate(self, delta_time):
        # Нежить медленно восстанавливается, потребляя жизненную силу
        if self.health < self.max_health:
            life_drain = delta_time * 0.5
            self.health = min(self.max_health, self.health + life_drain)

    def die(self):
        # Нежить может быть "уничтожена" или "рассеяна", но не "умереть" как живое существо
        self.is_alive = False
        self.health = 0
        print(f"{self.name} был рассеян, но не умер...")

    def attack_with_weapon(self, target):
        print(f"{self.name} атакует {target.name} своим оружием")
        if target:
            return target.take_damage(self.weapon_damage)

# Пример использования
dragon = Dragon("Смауг", 500, (100, 100), 200, 150, 50)
elf = Elf("Леголас", 120, (10, 10), 150, 80, 20)
undead = UndeadWarrior("Рыцарь смерти", 200, (50, 50), 30, 100, 35)

print(f"Дракон: {dragon.get_info()}")
print(f"Эльф: {elf.get_info()}")
print(f"Нежить: {undead.get_info()}")

# Демонстрация уникальных способностей
dragon.cast_spell("Огненный взрыв", elf)
elf.hide_in_nature()
undead.attack_with_weapon(elf)

# Обновление состояния сущностей
dragon.update(1.0)
elf.update(1.0)
undead.update(1.0)
```

</details>

---

## 1. Создание абстрактного класса игровой сущности

### Пример 1: Базовый абстрактный класс GameEntity

```python
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
        Абстрактный метод взаимодействия с другой игровой сущностью
        """
        pass

    @abstractmethod
    def update(self, delta_time):
        """
        Абстрактный метод обновления состояния сущности
        """
        pass

    def get_info(self):
        """
        Конкретный метод получения информации о сущности
        """
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} ({status}): здоровье {self.health}/{self.max_health}, позиция {self.position}"

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

# Создание экземпляра класса
player = PlayerCharacter("Артур", 100, (0, 0), 5)
print(player.get_info())  # Артур (жив): здоровье 100/100, позиция (0, 0)
player.interact(None)  # Артур исследует None
```

### Пример 2: Абстрактный класс для боевых действий

```python
from abc import ABC, abstractmethod

class Attackable(ABC):
    """
    Интерфейс для боевых действий
    """
    @abstractmethod
    def take_damage(self, damage):
        """
        Абстрактный метод получения урона
        """
        pass

    @abstractmethod
    def deal_damage(self, target):
        """
        Абстрактный метод нанесения урона цели
        """
        pass

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

# Пример использования
warrior1 = Warrior("Конан", 120, 25, 8)
warrior2 = Warrior("Ланселот", 100, 20, 5)

print(f"Здоровье Ланселота до атаки: {warrior2.health}")
warrior1.deal_damage(warrior2)
print(f"Здоровье Ланселота после атаки: {warrior2.health}")
```

---

## 2. Абстрактные классы и интерфейсы в игровом контексте

### Использование абстрактных классов для создания иерархии

```python
from abc import ABC, abstractmethod

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
        Абстрактный метод использования специальной способности
        """
        pass

    @abstractmethod
    def level_up(self):
        """
        Абстрактный метод повышения уровня
        """
        pass

    def rest(self):
        """
        Конкретный метод отдыха для восстановления здоровья
        """
        old_health = self.health
        self.health = self.max_health
        print(f"{self.name} отдохнул и восстановил здоровье с {old_health} до {self.health}")

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

# Пример использования
knight = Knight("Ланселот")
wizard = Wizard("Гендальф")

print(f"Рыцарь: {knight.name}, уровень {knight.level}, здоровье {knight.health}/{knight.max_health}")
print(f"Маг: {wizard.name}, уровень {wizard.level}, здоровье {wizard.health}/{wizard.max_health}, мана {wizard.mana}/{wizard.max_mana}")

knight.level_up()
wizard.level_up()
```

---

## 3. Интерфейсы в игровых системах

### Использование интерфейсов для унификации взаимодействия

```python
from abc import ABC, abstractmethod

class Interactable(ABC):
    """
    Интерфейс для взаимодействия с объектами
    """
    @abstractmethod
    def interact_with(self, entity):
        """
        Метод взаимодействия с сущностью
        """
        pass

class InventoryItem(Interactable):
    def __init__(self, name, item_type, weight=1.0, value=0):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.value = value
        self.durability = 100  # Прочность предмета

    def interact_with(self, entity):
        if hasattr(entity, 'inventory'):
            entity.inventory.append(self)
            print(f"{self.name} добавлен в инвентарь {entity.name}")
            return True
        else:
            print(f"{entity.name} не может взаимодействовать с предметами")
            return False

class Door(Interactable):
    def __init__(self, name, locked=True, key_required=None):
        self.name = name
        self.locked = locked
        self.key_required = key_required
        self.opened = False

    def interact_with(self, entity):
        if self.locked:
            if self.key_required and hasattr(entity, 'inventory'):
                # Проверяем, есть ли ключ в инвентаре
                has_key = any(item.name == self.key_required for item in entity.inventory)
                if has_key:
                    self.locked = False
                    print(f"{entity.name} открывает {self.name} ключом")
                    return True
                else:
                    print(f"{entity.name} не может открыть {self.name} - нужен ключ {self.key_required}")
                    return False
            else:
                print(f"{self.name} заперта и не может быть открыта")
                return False
        else:
            self.opened = True
            print(f"{self.name} открыта {entity.name}")
            return True

class Lever(Interactable):
    def __init__(self, name, connected_objects=None):
        self.name = name
        self.pulled = False
        self.connected_objects = connected_objects or []

    def interact_with(self, entity):
        self.pulled = True
        print(f"{entity.name} дергает {self.name}")
        # Активируем связанные объекты
        for obj in self.connected_objects:
            if hasattr(obj, 'activate'):
                obj.activate()
        return True

# Пример использования
player = PlayerCharacter("Артур", 100, (0, 0), 5)
key = InventoryItem("Золотой ключ", "key", 0.5, 50)
door = Door("Дверь в замок", locked=True, key_required="Золотой ключ")
lever = Lever("Рычаг", connected_objects=[door])

print(f"Инвентарь игрока до: {len(player.inventory)} предметов")
key.interact_with(player)
print(f"Инвентарь игрока после: {len(player.inventory)} предметов")

door.interact_with(player)  # Не откроется - нет ключа в инвентаре
lever.interact_with(player)  # Активирует рычаг, но дверь не откроется без ключа
```

---

## 4. Практические задания в игровом контексте

### Задание 1: Интерфейс для магических существ

Создайте интерфейс `MagicalCreature` с методами: `cast_spell(spell_name)`, `fly(height)`, `disappear()`. Реализуйте классы `Phoenix`, `Unicorn`, `Griffin` с уникальными характеристиками и реализациями интерфейса.

```python
from abc import ABC, abstractmethod

class MagicalCreature(ABC):
    """
    Интерфейс для магических существ
    """
    @abstractmethod
    def cast_spell(self, spell_name):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def fly(self, height):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def disappear(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте метод
        pass  # Замените на ваш код

class Phoenix(MagicalCreature):
    def __init__(self, name, health=200, regeneration_rate=5):
        # ВАШ КОД ЗДЕСЬ - инициализация
        pass  # Замените на ваш код

    def cast_spell(self, spell_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def fly(self, height):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def disappear(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def regenerate(self):
        # ВАШ КОД ЗДЕСЯ - уникальный метод восстановления
        pass  # Замените на ваш код

class Unicorn(MagicalCreature):
    def __init__(self, name, health=150, healing_power=10):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def cast_spell(self, spell_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def fly(self, height):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def disappear(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def heal(self, target):
        # ВАШ КОД ЗДЕСЯ - уникальный метод исцеления
        pass  # Замените на ваш код

class Griffin(MagicalCreature):
    def __init__(self, name, health=180, attack_power=25):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def cast_spell(self, spell_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def fly(self, height):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def disappear(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def attack(self, target):
        # ВАШ КОД ЗДЕСЯ - уникальный метод атаки
        pass  # Замените на ваш код

# Тестирование
phoenix = Phoenix("Огненная птица")
unicorn = Unicorn("Белый единорог")
griffin = Griffin("Крылатый лев")
```

### Задание 2: Абстрактный класс для игровых локаций

Создайте абстрактный класс `GameLocation` с атрибутами: название, тип локации, уровень опасности, список NPC, список монстров. Реализуйте методы: `enter_location(visitor)`, `spawn_monster()`, `get_safe()`, `get_age()`. Создайте классы-наследники `Forest`, `Dungeon`, `Castle` с уникальными особенностями.

```python
from abc import ABC, abstractmethod

class GameLocation(ABC):
    """
    Абстрактный класс игровой локации
    """
    location_types = ["forest", "dungeon", "castle", "village", "desert", "mountain"]

    def __init__(self, name, location_type, danger_level=1):
        if location_type not in GameLocation.location_types:
            raise ValueError(f"Тип локации должен быть одним из: {GameLocation.location_types}")
        if not 1 <= danger_level <= 10:
            raise ValueError("Уровень опасности должен быть от 1 до 10")

        self.name = name
        self.location_type = location_type
        self.danger_level = danger_level
        self.npcs = []
        self.monsters = []
        self.visitors = []
        self.created_at = __import__('datetime').datetime.now()

    @abstractmethod
    def enter_location(self, visitor):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def spawn_monster(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def get_safe(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def get_age(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class Forest(GameLocation):
    def __init__(self, name, danger_level=2, tree_density="high"):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def enter_location(self, visitor):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def spawn_monster(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_safe(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_age(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class Dungeon(GameLocation):
    def __init__(self, name, danger_level=7, trap_count=5):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def enter_location(self, visitor):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def spawn_monster(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_safe(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_age(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class Castle(GameLocation):
    def __init__(self, name, danger_level=4, guard_count=10):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def enter_location(self, visitor):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def spawn_monster(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_safe(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def get_age(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

# Тестирование
forest = Forest("Лес Эндор", danger_level=3)
dungeon = Dungeon("Подземелье Темного Лорда", danger_level=8)
castle = Castle("Крепость Света", danger_level=4)
```

### Задание 3: Интерфейс для боевых искусств

Создайте интерфейс `MartialArt` с методами: `perform_combat_move(target)`, `train()`, `improve_skill(skill_level)`. Реализуйте классы `Swordsman`, `ArcheryExpert`, `MartialArtist` с уникальными боевыми техниками и стилями боя.

```python
from abc import ABC, abstractmethod

class MartialArt(ABC):
    """
    Интерфейс для боевых искусств
    """
    @abstractmethod
    def perform_combat_move(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def train(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    @abstractmethod
    def improve_skill(self, skill_level):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class Swordsman(MartialArt):
    def __init__(self, name, sword_skill=1, health=120, attack_power=20):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def perform_combat_move(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def train(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def improve_skill(self, skill_level):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class ArcheryExpert(MartialArt):
    def __init__(self, name, archery_skill=1, health=100, arrows=30):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def perform_combat_move(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def train(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def improve_skill(self, skill_level):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

class MartialArtist(MartialArt):
    def __init__(self, name, martial_art_skill=1, health=90, chi_power=50):
        # ВАШ КОД ЗДЕСЯ - инициализация
        pass  # Замените на ваш код

    def perform_combat_move(self, target):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def train(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

    def improve_skill(self, skill_level):
        # ВАШ КОД ЗДЕСЯ - реализуйте метод
        pass  # Замените на ваш код

# Тестирование
fighter1 = Swordsman("Меченосец", sword_skill=3)
fighter2 = ArcheryExpert("Лучник", archery_skill=4)
fighter3 = MartialArtist("Мастер боевых искусств", martial_art_skill=5)
```

---

## 5. Дополнительные задания

### Задание 4: Система квестов с абстрактными классами

Создайте систему квестов, используя абстрактные классы. Реализуйте базовый класс `Quest` с абстрактными методами `check_completion_condition()` и `reward_player(player)`. Создайте несколько типов квестов: `KillQuest`, `CollectQuest`, `EscortQuest` с уникальными условиями выполнения.

### Задание 5: Иерархия магических школ

Разработайте иерархию классов для различных школ магии, используя абстрактные классы. Создайте базовую школу `MagicSchool` с абстрактными методами и несколько специализированных школ: `FireMagicSchool`, `WaterMagicSchool`, `EarthMagicSchool`, `AirMagicSchool`.

---

## Контрольные вопросы:
1. В чем разница между абстрактным классом и интерфейсом в Python?
2. Какие преимущества дают абстрактные классы в игровой разработке?
3. Что происходит при попытке создать экземпляр абстрактного класса?
4. Как использовать декоратор @abstractmethod для методов и свойств?
5. В чем заключается принцип "программировать на интерфейсе, а не на реализации"?
6. Как абстрактные классы помогают обеспечить целостность архитектуры игры?
7. Можно ли создавать конкретные методы внутри абстрактного класса?
8. Как правильно наследоваться от абстрактных классов и реализовывать их методы?
9. Какие ошибки могут возникнуть при неправильной реализации абстрактных методов?
10. Как абстрактные классы способствуют лучшему тестированию игровой логики?</details>
</summary>