# Практическое занятие 15: ООП - паттерн Observer в игровом контексте

## Создание системы наблюдения за игровыми событиями, наблюдатели и субъекты

### Цель занятия:
Научиться создавать систему наблюдения в Python, определять субъектов и наблюдателей, использовать паттерн Observer для реализации системы подписки на события и уведомления об изменениях в игровой среде.

### Задачи:
1. Создать интерфейсы наблюдателя и субъекта
2. Использовать паттерн Observer для уведомления о событиях
3. Реализовать различные типы наблюдателей: простые, параметризованные, асинхронные
4. Применить принципы ООП и паттерн Observer на практике в игровом контексте

### План работы:
1. Создание простой системы наблюдения за игровыми событиями
2. Определение интерфейсов наблюдателя и субъекта
3. Использование различных типов наблюдателей для отслеживания изменений
4. Применение принципов инкапсуляции и наследования в наблюдателях
5. Создание экземпляров классов наблюдателей и субъектов
6. Практические задания в игровом контексте

---
# Практическое занятие 15: ООП - паттерн Observer в игровом контексте

## Создание системы наблюдения за игровыми событиями, наблюдатели и субъекты

### Цель занятия:
Научиться создавать систему наблюдения в Python, определять субъектов и наблюдателей, использовать паттерн Observer для реализации системы подписки на события и уведомления об изменениях в игровой среде.

### Задачи:
1. Создать интерфейсы наблюдателя и субъекта
2. Использовать паттерн Observer для уведомления о событиях
3. Реализовать различные типы наблюдателей: простые, параметризованные, асинхронные
4. Применить принципы ООП и паттерн Observer на практике в игровом контексте

---

## 1. Теоретическая часть

### Основные понятия паттерна Observer

**Паттерн Observer (Наблюдатель)** — это поведенческий паттерн проектирования, который определяет зависимость "один ко многим" между объектами, так что при изменении состояния одного объекта (субъекта) происходит автоматическое уведомление и обновление всех зависимых объектов (наблюдателей).

**Субъект (Subject)** — это объект, который содержит информацию, на которую подписаны наблюдатели. Он управляет списком своих наблюдателей и уведомляет их о изменениях.

**Наблюдатель (Observer)** — это объект, который получает уведомления от субъекта об изменениях в состоянии.

### Пример простого наблюдателя (уровень 1 - начальный)

```python
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """
    Интерфейс наблюдателя для получения уведомлений об изменениях
    """
    @abstractmethod
    def update(self, event_type: str, data: dict = None):
        """
        Метод для получения уведомления об изменении
        """
        pass

class Subject(ABC):
    """
    Интерфейс субъекта, за которым могут наблюдать наблюдатели
    """
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Подписаться на уведомления"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Отписаться от уведомлений"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: dict = None):
        """Уведомить всех наблюдателей об изменении"""
        for observer in self._observers:
            observer.update(event_type, data)


class Player(Subject):
    """
    Класс игрока, за которым могут наблюдать другие объекты
    """
    def __init__(self, name: str, health: int = 100):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self._level = 1
        self._experience = 0
        self.is_alive = True

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        old_health = self._health
        self._health = max(0, min(self._max_health, value))
        if self._health <= 0:
            self._health = 0
            self.is_alive = False
            # Уведомляем наблюдателей о смерти игрока
            self.notify("player_died", {"player": self, "old_health": old_health, "new_health": self._health})
        elif old_health != self._health:
            # Уведомляем наблюдателей об изменении здоровья
            self.notify("player_health_changed", {"player": self, "old_health": old_health, "new_health": self._health})

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        old_level = self._level
        self._level = value
        if self._level > old_level:
            # Уведомляем наблюдателей о повышении уровня
            self.notify("player_leveled_up", {"player": self, "old_level": old_level, "new_level": self._level})

    def take_damage(self, damage: int):
        """Получить урон"""
        self.health -= damage
        self.notify("player_damaged", {"player": self, "damage_amount": damage})

    def gain_experience(self, exp: int):
        """Получить опыт"""
        self._experience += exp
        self.notify("player_gained_experience", {"player": self, "exp_gained": exp, "total_exp": self._experience})
        # Проверяем, не пора ли повысить уровень
        required_exp = self._level * 100  # Упрощенная формула
        if self._experience >= required_exp:
            self.level_up()

    def level_up(self):
        """Повысить уровень игрока"""
        self._experience = 0  # Сбрасываем опыт при повышении уровня
        self._level += 1
        self._max_health += 20  # Увеличиваем максимальное здоровье
        self.health = self._max_health  # Полностью восстанавливаем здоровье
        self.level = self._level  # Вызываем сеттер для уведомления

    def get_info(self):
        return f"{self.name}: Lvl.{self._level}, HP {self._health}/{self._max_health}, EXP {self._experience}"


class HealthBarObserver(Observer):
    """
    Наблюдатель за изменением здоровья игрока
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "player_health_changed":
            player = data.get("player")
            if player:
                print(f"📊 Полоска здоровья {player.name}: {player.health}/{player._max_health}")


class LevelUpObserver(Observer):
    """
    Наблюдатель за повышением уровня игрока
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "player_leveled_up":
            player = data.get("player")
            if player:
                new_level = data.get("new_level", "N/A")
                print(f"📈 {player.name} достиг {new_level} уровня!")


# Пример использования
player = Player("Артур", health=100)

# Создаем и подписываем наблюдателей
health_observer = HealthBarObserver()
level_observer = LevelUpObserver()

player.attach(health_observer)
player.attach(level_observer)

print(f"Игрок: {player.get_info()}")

# Наносим урон игроку
player.take_damage(30)

# Игрок получает опыт, который приводит к повышению уровня
player.gain_experience(150)

print(f"\nПосле изменений:")
print(f"Игрок: {player.get_info()}")
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Создание наблюдателя за смертью игрока

Создайте класс `DeathObserver`, который будет уведомлен, когда игрок умрет. Реализуйте метод `update`, который выводит сообщение о смерти игрока и причину смерти.

**Шаги выполнения:**
1. Создайте класс `DeathObserver`, наследующийся от `Observer`
2. Реализуйте метод `update` для обработки события "player_died"
3. Выведите сообщение о смерти игрока с деталями
4. Протестируйте работу наблюдателя

```python
class DeathObserver(Observer):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


# Пример использования (после реализации)
# death_observer = DeathObserver()
# player = Player("Борис", health=50)
# player.attach(death_observer)
# 
# print(f"Игрок: {player.get_info()}")
# player.take_damage(60)  # Это должно вызвать смерть игрока
# print(f"Игрок жив: {player.is_alive}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class DeathObserver(Observer):
    """
    Наблюдатель за смертью игрока
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "player_died":
            player = data.get("player")
            old_health = data.get("old_health", 0)
            new_health = data.get("new_health", 0)
            
            if player:
                print(f"💀 {player.name} погибает! Было HP: {old_health}, стало HP: {new_health}")
```

</details>

#### Задание 1.2: Наблюдатель за получением опыта

Создайте класс `ExperienceObserver`, который отслеживает получение опыта игроком и выводит сообщение о количестве полученного опыта.

```python
class ExperienceObserver(Observer):
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


# Пример использования (после реализации)
# exp_observer = ExperienceObserver()
# player = Player("Елена", health=100)
# player.attach(exp_observer)
# 
# print(f"Игрок: {player.get_info()}")
# player.gain_experience(75)
# print(f"После получения опыта: {player.get_info()}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class ExperienceObserver(Observer):
    """
    Наблюдатель за получением опыта
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "player_gained_experience":
            player = data.get("player")
            exp_gained = data.get("exp_gained", 0)
            total_exp = data.get("total_exp", 0)
            
            if player:
                print(f"⭐ {player.name} получил {exp_gained} опыта! Всего: {total_exp}")
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Система уведомлений с использованием callback-функций

Реализуйте систему уведомлений с использованием callback-функций вместо интерфейсов. Создайте класс `EventManager`, который позволяет подписываться на события с помощью функций.

**Шаги выполнения:**
1. Создайте класс `EventManager` с методами `subscribe`, `unsubscribe`, `trigger_event`
2. Реализуйте возможность подписки на события по типу
3. Добавьте вызов всех подписанных обработчиков при наступлении события
4. Протестируйте систему с различными обработчиками

```python
from typing import Callable, Dict

class EventManager:
    # ВАШ КОД ЗДЕСЬ - реализуйте класс
    pass


# Примеры обработчиков событий
def player_damaged_handler(event_type: str, data: dict):
    # ВАШ КОД ЗДЕСЬ - реализуйте обработчик
    pass

def enemy_defeated_handler(event_type: str, data: dict):
    # ВАШ КОД ЗДЕСЬ - реализуйте обработчик
    pass

def level_up_handler(event_type: str, data: dict):
    # ВАШ КОД ЗДЕСЬ - реализуйте обработчик
    pass


# Пример использования (после реализации)
# event_manager = EventManager()
# 
# # Подписываем обработчики на события
# event_manager.subscribe("player_damaged", player_damaged_handler)
# event_manager.subscribe("enemy_died", enemy_defeated_handler)
# event_manager.subscribe("player_leveled_up", level_up_handler)
# 
# # Вызываем события
# event_manager.trigger_event("player_damaged", {"player": Player("Артур"), "damage_amount": 25})
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
from typing import Callable, Dict, List

class EventManager:
    """
    Менеджер событий для управления игровыми событиями
    """
    def __init__(self):
        self._event_handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        """Подписаться на событие определенного типа"""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        if handler not in self._event_handlers[event_type]:
            self._event_handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable):
        """Отписаться от события определенного типа"""
        if event_type in self._event_handlers:
            if handler in self._event_handlers[event_type]:
                self._event_handlers[event_type].remove(handler)
                # Удаляем тип события, если больше нет обработчиков
                if not self._event_handlers[event_type]:
                    del self._event_handlers[event_type]

    def trigger_event(self, event_type: str, data: dict = None):
        """Вызвать событие и уведомить всех подписчиков"""
        if event_type in self._event_handlers:
            # Создаем копию списка обработчиков на случай, если он изменится во время вызова
            handlers_copy = self._event_handlers[event_type].copy()
            for handler in handlers_copy:
                try:
                    handler(event_type, data)
                except Exception as e:
                    print(f"Ошибка при обработке события {event_type}: {e}")

    def get_subscribers_count(self, event_type: str) -> int:
        """Получить количество подписчиков на событие"""
        return len(self._event_handlers.get(event_type, []))


# Примеры обработчиков событий
def player_damaged_handler(event_type: str, data: dict):
    """Обработчик события получения урона игроком"""
    if data and "player" in data and "damage_amount" in data:
        print(f"🛡️ Игрок {data['player'].name} получил {data['damage_amount']} урона!")
        if hasattr(data['player'], 'health') and data['player'].health < data['player']._max_health * 0.3:
            print(f"⚠️ {data['player'].name} находится в опасности!")

def enemy_defeated_handler(event_type: str, data: dict):
    """Обработчик события уничтожения врага"""
    if data and "enemy" in data:
        print(f"💀 Враг {data['enemy'].name} повержен!")

def level_up_handler(event_type: str, data: dict):
    """Обработчик события повышения уровня"""
    if data and "player" in data and "new_level" in data:
        print(f"🎉 {data['player'].name} достиг {data['new_level']} уровня!")
```

</details>

#### Задание 2.2: Параметризованный наблюдатель

Улучшите класс `Player` из примера выше, добавив возможность отслеживания различных параметров (например, брони, маны, выносливости) и уведомления наблюдателей об их изменениях.

```python
class Player(Subject):
    """
    Улучшенный класс игрока с дополнительными параметрами
    """
    def __init__(self, name: str, health: int = 100, mana: int = 50, stamina: int = 100):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self._mana = mana
        self._max_mana = mana
        self._stamina = stamina
        self._max_stamina = stamina
        self._level = 1
        self._experience = 0
        self._armor = 5
        self.is_alive = True

    # ВАШ КОД ЗДЕСЬ - добавьте свойства и сеттеры для mana и stamina
    # с уведомлением наблюдателей об изменениях
    
    def use_mana(self, amount: int):
        # ВАШ КОД ЗДЕСЬ - реализуйте использование маны с уведомлением
        pass

    def use_stamina(self, amount: int):
        # ВАШ КОД ЗДЕСЬ - реализуйте использование выносливости с уведомлением
        pass


# Пример использования (после реализации)
# player = Player("Маг", health=80, mana=100, stamina=80)
# 
# # Создаем наблюдателей
# class ManaObserver(Observer):
#     def update(self, event_type: str, data: dict = None):
#         if event_type == "player_mana_changed":
#             player = data.get("player")
#             old_mana = data.get("old_mana", 0)
#             new_mana = data.get("new_mana", 0)
#             if player:
#                 print(f"🔵 {player.name} изменила мана: {old_mana} -> {new_mana}")
# 
# mana_observer = ManaObserver()
# player.attach(mana_observer)
# 
# print(f"Игрок: {player.get_info()}")
# player.use_mana(30)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class Player(Subject):
    """
    Улучшенный класс игрока с дополнительными параметрами
    """
    def __init__(self, name: str, health: int = 100, mana: int = 50, stamina: int = 100):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self._mana = mana
        self._max_mana = mana
        self._stamina = stamina
        self._max_stamina = stamina
        self._level = 1
        self._experience = 0
        self._armor = 5
        self.is_alive = True

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        old_health = self._health
        self._health = max(0, min(self._max_health, value))
        if self._health <= 0:
            self._health = 0
            self.is_alive = False
            # Уведомляем наблюдателей о смерти игрока
            self.notify("player_died", {"player": self, "old_health": old_health, "new_health": self._health})
        elif old_health != self._health:
            # Уведомляем наблюдателей об изменении здоровья
            self.notify("player_health_changed", {"player": self, "old_health": old_health, "new_health": self._health})

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value: int):
        old_mana = self._mana
        self._mana = max(0, min(self._max_mana, value))
        if old_mana != self._mana:
            # Уведомляем наблюдателей об изменении маны
            self.notify("player_mana_changed", {"player": self, "old_mana": old_mana, "new_mana": self._mana})

    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, value: int):
        old_stamina = self._stamina
        self._stamina = max(0, min(self._max_stamina, value))
        if old_stamina != self._stamina:
            # Уведомляем наблюдателей об изменении выносливости
            self.notify("player_stamina_changed", {"player": self, "old_stamina": old_stamina, "new_stamina": self._stamina})

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        old_level = self._level
        self._level = value
        if self._level > old_level:
            # Уведомляем наблюдателей о повышении уровня
            self.notify("player_leveled_up", {"player": self, "old_level": old_level, "new_level": self._level})

    def take_damage(self, damage: int):
        """Получить урон"""
        # Учитываем броню при расчете урона
        actual_damage = max(1, damage - self._armor)
        self.health -= actual_damage
        self.notify("player_damaged", {"player": self, "damage_amount": actual_damage, "armor_reduced": self._armor})

    def gain_experience(self, exp: int):
        """Получить опыт"""
        self._experience += exp
        self.notify("player_gained_experience", {"player": self, "exp_gained": exp, "total_exp": self._experience})
        # Проверяем, не пора ли повысить уровень
        required_exp = self._level * 100  # Упрощенная формула
        if self._experience >= required_exp:
            self.level_up()

    def level_up(self):
        """Повысить уровень игрока"""
        self._experience = 0  # Сбрасываем опыт при повышении уровня
        self._level += 1
        self._max_health += 20  # Увеличиваем максимальное здоровье
        self._max_mana += 15   # Увеличиваем максимальную ману
        self._max_stamina += 10 # Увеличиваем максимальную выносливость
        self.health = self._max_health  # Полностью восстанавливаем здоровье
        self.mana = self._max_mana      # Восстанавливаем ману
        self.stamina = self._max_stamina # Восстанавливаем выносливость
        self._armor += 2  # Увеличиваем броню
        self.level = self._level  # Вызываем сеттер для уведомления

    def use_mana(self, amount: int):
        """Использовать ману"""
        if self._mana >= amount:
            old_mana = self._mana
            self._mana -= amount
            self.notify("player_mana_used", {"player": self, "mana_used": amount, "old_mana": old_mana, "new_mana": self._mana})
            return True
        else:
            self.notify("player_not_enough_mana", {"player": self, "required_mana": amount, "available_mana": self._mana})
            return False

    def use_stamina(self, amount: int):
        """Использовать выносливость"""
        if self._stamina >= amount:
            old_stamina = self._stamina
            self._stamina -= amount
            self.notify("player_stamina_used", {"player": self, "stamina_used": amount, "old_stamina": old_stamina, "new_stamina": self._stamina})
            return True
        else:
            self.notify("player_not_enough_stamina", {"player": self, "required_stamina": amount, "available_stamina": self._stamina})
            return False

    def get_info(self):
        return f"{self.name}: Lvl.{self._level}, HP {self._health}/{self._max_health}, MP {self._mana}/{self._max_mana}, STA {self._stamina}/{self._max_stamina}, EXP {self._experience}, ARMOR {self._armor}"
```

</details>

### Уровень 3 - Повышенный

#### Задание 3.1: Асинхронный Observer

Создайте асинхронную систему наблюдения, которая может обрабатывать события в асинхронном режиме. Реализуйте классы `AsyncObserver` и `AsyncSubject`.

**Шаги выполнения:**
1. Создайте абстрактный класс `AsyncObserver` с асинхронным методом `update_async`
2. Создайте класс `AsyncSubject` с асинхронным методом `notify_async`
3. Обработайте ошибки в асинхронных наблюдателях
4. Протестируйте систему с несколькими асинхронными наблюдателями

```python
import asyncio
from typing import List

class AsyncObserver(ABC):
    """
    Асинхронный наблюдатель
    """
    @abstractmethod
    async def update_async(self, event_type: str, data: dict = None):
        """
        Асинхронное обновление при получении уведомления
        """
        pass


class AsyncSubject:
    """
    Асинхронный субъект, за которым могут наблюдать
    """
    def __init__(self):
        self._async_observers: List[AsyncObserver] = []

    def attach_async(self, observer: AsyncObserver):
        """Подписаться на асинхронные уведомления"""
        if observer not in self._async_observers:
            self._async_observers.append(observer)

    def detach_async(self, observer: AsyncObserver):
        """Отписаться от асинхронных уведомлений"""
        if observer in self._async_observers:
            self._async_observers.remove(observer)

    async def notify_async(self, event_type: str, data: dict = None):
        """
        Асинхронно уведомить всех наблюдателей
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте асинхронное уведомление
        pass


class AsyncBattleLogger(AsyncObserver):
    """
    Асинхронный логгер боевых действий
    """
    def __init__(self, filename: str = "battle_log.txt"):
        self.filename = filename
        self.log_entries = []

    async def update_async(self, event_type: str, data: dict = None):
        """
        Обработать событие асинхронно и записать в лог
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте асинхронную обработку
        pass


# Пример использования (после реализации)
# async def test_async_observer():
#     subject = AsyncSubject()
#     
#     logger = AsyncBattleLogger()
#     subject.attach_async(logger)
#     
#     await subject.notify_async("player_damaged", {"player": "Артур", "damage": 25})
#     await asyncio.sleep(0.1)  # Небольшая задержка для завершения асинхронных операций
# 
# # Для запуска используйте: asyncio.run(test_async_observer())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import asyncio
from typing import List

class AsyncObserver(ABC):
    """
    Асинхронный наблюдатель
    """
    @abstractmethod
    async def update_async(self, event_type: str, data: dict = None):
        """
        Асинхронное обновление при получении уведомления
        """
        pass


class AsyncSubject:
    """
    Асинхронный субъект, за которым могут наблюдать
    """
    def __init__(self):
        self._async_observers: List[AsyncObserver] = []

    def attach_async(self, observer: AsyncObserver):
        """Подписаться на асинхронные уведомления"""
        if observer not in self._async_observers:
            self._async_observers.append(observer)

    def detach_async(self, observer: AsyncObserver):
        """Отписаться от асинхронных уведомлений"""
        if observer in self._async_observers:
            self._async_observers.remove(observer)

    async def notify_async(self, event_type: str, data: dict = None):
        """
        Асинхронно уведомить всех наблюдателей
        """
        tasks = []
        for observer in self._async_observers:
            task = asyncio.create_task(observer.update_async(event_type, data))
            tasks.append(task)
        
        # Ждем завершения всех задач уведомления
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            # Обрабатываем возможные исключения
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Ошибка в наблюдателе {i}: {result}")


class AsyncBattleLogger(AsyncObserver):
    """
    Асинхронный логгер боевых действий
    """
    def __init__(self, filename: str = "battle_log.txt"):
        self.filename = filename
        self.log_entries = []

    async def update_async(self, event_type: str, data: dict = None):
        """
        Обработать событие асинхронно и записать в лог
        """
        import time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_type}: {data}"
        self.log_entries.append(log_entry)
        print(f"[ASYNC_LOGGER] Записано: {log_entry}")
        
        # Имитация асинхронной операции записи в файл
        await asyncio.sleep(0.05)  # Задержка для имитации I/O операции


class AsyncAchievementNotifier(AsyncObserver):
    """
    Асинхронный обработчик достижений
    """
    def __init__(self):
        self.unlocked_achievements = []

    async def update_async(self, event_type: str, data: dict = None):
        """
        Обработать событие и проверить достижения
        """
        # Имитация асинхронной проверки достижений (например, запрос к серверу)
        await asyncio.sleep(0.1)  # Небольшая задержка для имитации работы
        
        if event_type == "player_damaged" and data and data.get("damage_amount", 0) >= 50:
            achievement = "Выносливость: Выдержал сильный удар"
            self.unlocked_achievements.append(achievement)
            print(f"[ASYNC_ACHIEVEMENT] Разблокировано достижение: {achievement}")
        elif event_type == "player_leveled_up" and data and data.get("new_level", 0) >= 10:
            achievement = "Опытный воин: Достиг 10 уровня"
            self.unlocked_achievements.append(achievement)
            print(f"[ASYNC_ACHIEVEMENT] Разблокировано достижение: {achievement}")


# Пример использования
async def test_async_observer():
    subject = AsyncSubject()
    
    logger = AsyncBattleLogger()
    achievements = AsyncAchievementNotifier()
    
    subject.attach_async(logger)
    subject.attach_async(achievements)
    
    print("=== Асинхронная симуляция событий ===")
    
    # Отправляем несколько событий
    await subject.notify_async("player_damaged", {"player": "Артур", "damage_amount": 25})
    await subject.notify_async("player_leveled_up", {"player": "Артур", "new_level": 10})
    await subject.notify_async("player_gained_experience", {"player": "Артур", "exp_gained": 150})
    
    print(f"\nЗаписи в логе: {len(logger.log_entries)}")
    print(f"Разблокированные достижения: {len(achievements.unlocked_achievements)}")
    for achievement in achievements.unlocked_achievements:
        print(f"  - {achievement}")
```

</details>

---

## 1. Создание простой системы наблюдения для игровых сущностей

### Пример 1: Класс PlayerObserver

```python
class PlayerObserver(Observer):
    """
    Наблюдатель за действиями игрока
    """
    def __init__(self, name: str):
        self.name = name
        self.observed_events = []

    def update(self, event_type: str, data: dict = None):
        """
        Обработать событие и сохранить в истории
        """
        event_record = {
            "event_type": event_type,
            "data": data,
            "timestamp": __import__('time').time()
        }
        self.observed_events.append(event_record)
        
        # Выводим информацию о событии
        if event_type == "player_damaged":
            player = data.get("player") if data else None
            damage = data.get("damage_amount", 0) if data else 0
            print(f"[{self.name}] Игрок {player.name if player else 'неизвестный'} получил {damage} урона")
        elif event_type == "player_leveled_up":
            player = data.get("player") if data else None
            new_level = data.get("new_level", "N/A") if data else "N/A"
            print(f"[{self.name}] Игрок {player.name if player else 'неизвестный'} достиг {new_level} уровня!")
        elif event_type == "player_gained_experience":
            player = data.get("player") if data else None
            exp_gained = data.get("exp_gained", 0) if data else 0
            print(f"[{self.name}] Игрок {player.name if player else 'неизвестный'} получил {exp_gained} опыта")

    def get_observation_summary(self):
        """
        Получить краткую статистику наблюдений
        """
        event_counts = {}
        for event in self.observed_events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return event_counts


# Пример использования
player = Player("Герой", health=100, mana=50, stamina=100)

# Создаем наблюдателя
player_observer = PlayerObserver("Аналитик")
player.attach(player_observer)

print(f"Игрок: {player.get_info()}")

# Выполняем действия, вызывающие события
player.take_damage(20)
player.gain_experience(100)
player.use_mana(15)
player.use_stamina(25)

print(f"\nКраткая статистика наблюдений:")
summary = player_observer.get_observation_summary()
for event_type, count in summary.items():
    print(f"  {event_type}: {count} раз(а)")

print(f"\nВсего событий зафиксировано: {len(player_observer.observed_events)}")
```

### Пример 2: Класс GameEventPublisher

```python
class GameEventPublisher(Subject):
    """
    Публикатор игровых событий
    """
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def publish_event(self, event_type: str, data: dict = None):
        """
        Опубликовать событие и уведомить всех подписчиков
        """
        print(f"[{self.name}] Публикуется событие: {event_type}")
        self.notify(event_type, data)


# Пример использования
event_publisher = GameEventPublisher("Центральный уведомлятор")

# Подключаем к нему тех же наблюдателей
death_observer = DeathObserver()
exp_observer = ExperienceObserver()

event_publisher.attach(death_observer)
event_publisher.attach(exp_observer)

print(f"\n--- Использование GameEventPublisher ---")
event_publisher.publish_event("player_died", {"player": player, "reason": "смерть от старости"})
event_publisher.publish_event("player_gained_experience", {"player": player, "exp_gained": 50})
```

---

## 2. Наблюдатели и субъекты в игровом контексте

### Наблюдатели для различных игровых систем

```python
class InventoryObserver(Observer):
    """
    Наблюдатель за изменениями в инвентаре
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "item_added":
            item = data.get("item") if data else None
            player = data.get("player") if data else None
            if item and player:
                print(f"🎒 {player.name} получил предмет: {item}")
        elif event_type == "item_removed":
            item = data.get("item") if data else None
            player = data.get("player") if data else None
            if item and player:
                print(f"❌ {player.name} потерял предмет: {item}")


class QuestObserver(Observer):
    """
    Наблюдатель за прогрессом квестов
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "quest_started":
            quest = data.get("quest") if data else None
            player = data.get("player") if data else None
            if quest and player:
                print(f"📜 {player.name} начал квест: {quest}")
        elif event_type == "quest_completed":
            quest = data.get("quest") if data else None
            player = data.get("player") if data else None
            if quest and player:
                print(f"✅ {player.name} завершил квест: {quest}")


class SocialObserver(Observer):
    """
    Наблюдатель за социальными событиями
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "player_joined":
            player = data.get("player") if data else None
            if player:
                print(f"👥 {player.name} присоединился к игре")
        elif event_type == "player_left":
            player = data.get("player") if data else None
            if player:
                print(f"👋 {player.name} покинул игру")
        elif event_type == "friend_request_sent":
            sender = data.get("sender") if data else None
            receiver = data.get("receiver") if data else None
            if sender and receiver:
                print(f"💌 {sender.name} отправил запрос на дружбу {receiver.name}")
```

---

## 3. Практические задания в игровом контексте

### Задание 1: Система уведомлений о смерти врагов

Создайте систему, в которой наблюдатели отслеживают смерть врагов и реагируют на это событие (например, начисляют опыт игроку, добавляют монеты и т.д.).

```python
class Enemy(Subject):
    """
    Класс врага как наблюдаемый объект
    """
    def __init__(self, name: str, health: int, attack_power: int, enemy_type: str = "common"):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self.attack_power = attack_power
        self.enemy_type = enemy_type
        self.is_alive = True

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        old_health = self._health
        self._health = max(0, min(self._max_health, value))
        if self._health <= 0:
            self._health = 0
            self.is_alive = False
            # Уведомляем наблюдателей о смерти врага
            self.notify("enemy_died", {"enemy": self, "old_health": old_health, "new_health": self._health})
        elif old_health != self._health:
            # Уведомляем наблюдателей об изменении здоровья
            self.notify("enemy_health_changed", {"enemy": self, "old_health": old_health, "new_health": self._health})

    def take_damage(self, damage: int):
        """Получить урон"""
        self.health -= damage
        self.notify("enemy_damaged", {"enemy": self, "damage_amount": damage})


class EnemyDeathRewardObserver(Observer):
    """
    Наблюдатель, начисляющий награду за смерть врага
    """
    def __init__(self, player):
        self.player = player

    def update(self, event_type: str, data: dict = None):
        if event_type == "enemy_died":
            enemy = data.get("enemy") if data else None
            if enemy:
                # Начисляем опыт в зависимости от типа врага
                exp_reward = {"common": 10, "elite": 25, "boss": 50}.get(enemy.enemy_type, 10)
                self.player.gain_experience(exp_reward)
                
                # Начисляем золото
                gold_reward = {"common": 5, "elite": 15, "boss": 30}.get(enemy.enemy_type, 5)
                if hasattr(self.player, '_gold'):
                    self.player._gold += gold_reward
                
                print(f"🏆 За убийство {enemy.name} ({enemy.enemy_type}) получено: {exp_reward} XP, {gold_reward} золота")


# Тестирование системы
player = Player("Рыцарь", health=150)
enemy = Enemy("Гоблин", health=50, attack_power=10, enemy_type="common")

# Подписываем наблюдателя
reward_observer = EnemyDeathRewardObserver(player)
enemy.attach(reward_observer)

print(f"Игрок: {player.get_info()}")
print(f"Враг: {enemy.name}, здоровье: {enemy.health}")

# Убиваем врага
enemy.take_damage(60)

print(f"\nПосле убийства врага:")
print(f"Игрок: {player.get_info()}")
```

### Задание 2: Система уведомлений о квестах

Создайте систему, где наблюдатели отслеживают прогресс выполнения квестов, получение наград и открытие новых квестов.

```python
class Quest:
    """
    Класс квеста
    """
    def __init__(self, title: str, description: str, xp_reward: int, gold_reward: int):
        self.title = title
        self.description = description
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.is_completed = False
        self.progress = 0
        self.goal = 10  # Условное значение цели (например, убить 10 монстров)

    def update_progress(self, amount: int = 1):
        """Обновить прогресс квеста"""
        self.progress = min(self.goal, self.progress + amount)
        if self.progress >= self.goal:
            self.complete()

    def complete(self):
        """Завершить квест"""
        self.is_completed = True


class QuestProgressObserver(Observer):
    """
    Наблюдатель за прогрессом квеста
    """
    def update(self, event_type: str, data: dict = None):
        if event_type == "quest_progress_updated":
            quest = data.get("quest")
            progress = data.get("progress", 0)
            goal = data.get("goal", 1)
            if quest:
                percentage = (progress / goal) * 100
                print(f"🎯 Прогресс квеста '{quest.title}': {percentage:.1f}% ({progress}/{goal})")
        elif event_type == "quest_completed":
            quest = data.get("quest")
            player = data.get("player")
            if quest and player:
                print(f"🎊 Квест '{quest.title}' завершен игроком {player.name}!")
                print(f"  Награда: {quest.xp_reward} XP, {quest.gold_reward} золота")


class QuestManager(Subject):
    """
    Менеджер квестов
    """
    def __init__(self):
        super().__init__()
        self.quests = []

    def add_quest(self, quest: Quest):
        """Добавить квест"""
        self.quests.append(quest)
        self.notify("quest_added", {"quest": quest})

    def update_quest_progress(self, quest: Quest, amount: int = 1):
        """Обновить прогресс квеста"""
        old_progress = quest.progress
        quest.update_progress(amount)
        self.notify("quest_progress_updated", {
            "quest": quest,
            "old_progress": old_progress,
            "progress": quest.progress,
            "goal": quest.goal
        })
        if quest.is_completed:
            self.notify("quest_completed", {"quest": quest})


# Тестирование системы квестов
quest_manager = QuestManager()
quest_observer = QuestProgressObserver()

# Подписываем наблюдателя
quest_manager.attach(quest_observer)

# Создаем квест
kill_goblins_quest = Quest("Убить гоблинов", "Убейте 5 гоблинов в лесу", 100, 50)

# Добавляем квест в менеджер
quest_manager.add_quest(kill_goblins_quest)

print(f"\nКвест: {kill_goblins_quest.title}")
print(f"Описание: {kill_goblins_quest.description}")

# Обновляем прогресс квеста
for i in range(5):
    quest_manager.update_quest_progress(kill_goblins_quest)
    print(f"  Убит гоблин #{i+1}")

print(f"\nКвест завершен: {kill_goblins_quest.is_completed}")
```

### Задание 3: Сравнение различных реализаций Observer

Создайте таблицу сравнения различных типов Observer (обычный, с фильтрацией, асинхронный) по критериям: сложность реализации, производительность, гибкость, применимость в игровой разработке. Приведите примеры, когда каждый тип наблюдателя наиболее эффективен в игровом контексте.

```python
def compare_observers():
    """
    Сравнение различных типов Observer
    """
    comparison = {
        "Обычный Observer": {
            "Сложность реализации": "Низкая",
            "Производительность": "Высокая",
            "Гибкость": "Средняя",
            "Применимость в играх": "Простые уведомления, такие как изменение здоровья, уровня и т.п."
        },
        "Observer с фильтрацией": {
            "Сложность реализации": "Средняя",
            "Производительность": "Средняя",
            "Гибкость": "Высокая",
            "Применимость в играх": "Системы с множеством типов событий, где нужны только определенные"
        },
        "Асинхронный Observer": {
            "Сложность реализации": "Высокая",
            "Производительность": "Высокая (для I/O операций)",
            "Гибкость": "Высокая",
            "Применимость в играх": "Системы с тяжелыми операциями (запись в БД, сетевые вызовы)"
        }
    }

    print("Сравнение типов Observer в игровой разработке:")
    print("-" * 80)
    print(f"{'Тип Observer':<20} {'Сложность':<12} {'Произв.':<10} {'Гибкость':<10} {'Применимость':<30}")
    print("-" * 80)

    for observer_type, props in comparison.items():
        print(f"{observer_type:<20} {props['Сложность реализации']:<12} {props['Производительность']:<10} {props['Гибкость']:<10} {props['Применимость в играх']:<30}")

compare_observers()
```

---

## 4. Дополнительные задания

### Задание 4: Комплексная игровая система

Создайте комплексную систему, которая объединяет несколько наблюдателей для реализации сложной игровой механики (например, система комбо-атак, где за определенные действия начисляются бонусы).

### Задание 5: Система модификаций

Реализуйте систему, где наблюдатели могут динамически изменять характеристики объектов на основе игровых событий (например, бафы/дебафы, влияющие на параметры персонажа).

---

## Контрольные вопросы:
1. В чем разница между Observer и Publisher-Subscriber паттернами в игровом контексте?
2. Как обеспечить потокобезопасность системы наблюдателей в многопоточной игровой среде?
3. Какие преимущества дает использование Observer в системах уведомлений игроков?
4. Как обрабатывать ошибки в наблюдателях, чтобы не прерывать выполнение других наблюдателей?
5. Как использовать Observer для создания слабосвязанной архитектуры игровых систем?