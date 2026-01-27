# Практическое занятие 15: ООП - паттерн Observer в игровом контексте

## Цель занятия
Изучить паттерн проектирования Observer (Наблюдатель) и научиться реализовывать его в Python для создания системы подписки на события и уведомления об изменениях в игровой среде, а также понять, когда и зачем использовать этот паттерн в игровой разработке.

## Задачи

### Задача 1: Базовая реализация Observer для игровых событий (20 баллов)
Создайте систему наблюдения за игровыми событиями:
- Интерфейс `Observer` с методом `update()`
- Интерфейс `Subject` с методами для управления подписчиками
- Конкретные классы: `Player`, `Enemy`, `GameEventPublisher`

```python
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """
    Интерфейс наблюдателя для получения уведомлений об игровых событиях
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


class Enemy(Subject):
    """
    Класс врага, за которым могут наблюдать другие объекты
    """
    def __init__(self, name: str, health: int, attack_power: int):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self.attack_power = attack_power
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


class GameEventPublisher(Subject):
    """
    Публикатор игровых событий
    """
    def publish_event(self, event_type: str, data: dict = None):
        """Опубликовать событие"""
        self.notify(event_type, data)


# Пример использования
player = Player("Артур", health=100)
enemy = Enemy("Гоблин", health=50, attack_power=10)

print(f"Игрок: {player.get_info()}")
print(f"Враг: {enemy.name}, здоровье: {enemy.health}")

# Наносим урон игроку
player.take_damage(30)

# Наносим урон врагу
enemy.take_damage(25)

# Игрок получает опыт
player.gain_experience(150)

print(f"\nПосле изменений:")
print(f"Игрок: {player.get_info()}")
print(f"Враг: {enemy.name}, здоровье: {enemy.health}, жив: {enemy.is_alive}")
```

### Задача 2: Использование встроенных средств для системы уведомлений (20 баллов)
Реализуйте систему уведомлений с использованием:
- Событийной модели Python
- Callback-функций
- Класса `EventManager` для управления событиями

```python
from typing import Callable, Dict, List
import time

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
        if data['player'].health < data['player'].max_health * 0.3:
            print(f"⚠️ {data['player'].name} находится в опасности!")

def enemy_defeated_handler(event_type: str, data: dict):
    """Обработчик события уничтожения врага"""
    if data and "enemy" in data:
        print(f"💀 Враг {data['enemy'].name} повержен!")

def level_up_handler(event_type: str, data: dict):
    """Обработчик события повышения уровня"""
    if data and "player" in data and "new_level" in data:
        print(f"🎉 {data['player'].name} достиг {data['new_level']} уровня!")

def experience_gained_handler(event_type: str, data: dict):
    """Обработчик события получения опыта"""
    if data and "player" in data and "exp_gained" in data:
        print(f"⭐ {data['player'].name} получил {data['exp_gained']} опыта!")

def health_changed_handler(event_type: str, data: dict):
    """Обработчик события изменения здоровья"""
    if data and "old_health" in data and "new_health" in data:
        entity = data.get("player") or data.get("enemy")
        if entity:
            change = data["new_health"] - data["old_health"]
            action = "восстановил" if change > 0 else "потерял"
            print(f"❤️ {entity.name} {action} {abs(change)} здоровья. Теперь: {data['new_health']}")


# Пример использования EventManager
event_manager = EventManager()

# Подписываем обработчики на события
event_manager.subscribe("player_damaged", player_damaged_handler)
event_manager.subscribe("enemy_died", enemy_defeated_handler)
event_manager.subscribe("player_leveled_up", level_up_handler)
event_manager.subscribe("player_gained_experience", experience_gained_handler)
event_manager.subscribe("player_health_changed", health_changed_handler)
event_manager.subscribe("enemy_health_changed", health_changed_handler)

# Создаем игрока и врага
player = Player("Артур", health=100)
enemy = Enemy("Гоблин", health=50, attack_power=10)

print(f"Игрок: {player.get_info()}")
print(f"Враг: {enemy.name}, здоровье: {enemy.health}")

# Вызываем события через EventManager
print("\n--- События ---")
event_manager.trigger_event("player_gained_experience", {"player": player, "exp_gained": 50})
player.take_damage(30)  # Это вызовет событие через сеттер здоровья
enemy.take_damage(50)   # Это вызовет событие через сеттер здоровья

print(f"\nПосле событий:")
print(f"Игрок: {player.get_info()}")
print(f"Враг жив: {enemy.is_alive}")

# Проверяем количество подписчиков
print(f"\nКоличество подписчиков на 'player_damaged': {event_manager.get_subscribers_count('player_damaged')}")
```

### Задача 3: Параметризованные уведомления в игровой системе (20 баллов)
Создайте систему уведомлений с фильтрацией:
- Возможность подписки на определенные типы событий
- Передача данных о событии подписчикам
- Классы `EventPublisher` и `EventSubscriber`

```python
from enum import Enum
from typing import Any, Optional

class GameEventType(Enum):
    """Типы игровых событий"""
    PLAYER_DAMAGE_TAKEN = "player_damage_taken"
    ENEMY_DEFEATED = "enemy_defeated"
    LEVEL_UP = "level_up"
    TREASURE_FOUND = "treasure_found"
    QUEST_COMPLETED = "quest_completed"
    HEALTH_CHANGED = "health_changed"
    MANA_CHANGED = "mana_changed"
    ITEM_ACQUIRED = "item_acquired"
    SKILL_UNLOCKED = "skill_unlocked"


class Event:
    """Класс события"""
    def __init__(self, event_type: GameEventType, source: Any = None, data: dict = None, timestamp: float = None):
        self.type = event_type
        self.source = source  # Источник события
        self.data = data or {}
        self.timestamp = timestamp or time.time()

    def __str__(self):
        return f"Event(type={self.type.value}, source={type(self.source).__name__ if self.source else 'None'}, data={self.data})"


class EventSubscriber(ABC):
    """Абстрактный класс подписчика на события"""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def handle_event(self, event: Event):
        """Обработать событие"""
        pass

    def can_handle_event(self, event_type: GameEventType) -> bool:
        """Проверить, может ли подписчик обрабатывать событие данного типа"""
        return True  # По умолчанию может обрабатывать любые события


class HealthBarObserver(EventSubscriber):
    """Наблюдатель за изменением здоровья"""
    def handle_event(self, event: Event):
        if event.type in [GameEventType.HEALTH_CHANGED, GameEventType.PLAYER_DAMAGE_TAKEN]:
            entity = event.data.get("entity") or event.source
            if entity:
                health = event.data.get("current_health", getattr(entity, 'health', 'N/A'))
                max_health = event.data.get("max_health", getattr(entity, 'max_health', 'N/A'))
                print(f"[HEALTH_BAR] {entity.name if hasattr(entity, 'name') else 'Entity'}: {health}/{max_health} HP")


class AchievementObserver(EventSubscriber):
    """Наблюдатель за достижениями"""
    def __init__(self, name: str):
        super().__init__(name)
        self.damage_dealt = 0
        self.enemies_defeated = 0
        self.treasures_found = 0

    def handle_event(self, event: Event):
        if event.type == GameEventType.PLAYER_DAMAGE_TAKEN:
            damage = event.data.get("damage_amount", 0)
            self.damage_dealt += damage
            if self.damage_dealt >= 1000:
                print(f"[ACHIEVEMENT] '{self.name}' получил достижение: 'Разрушитель'!")
        elif event.type == GameEventType.ENEMY_DEFEATED:
            self.enemies_defeated += 1
            if self.enemies_defeated >= 10:
                print(f"[ACHIEVEMENT] '{self.name}' получил достижение: 'Охотник за монстрами'!")
        elif event.type == GameEventType.TREASURE_FOUND:
            self.treasures_found += 1
            if self.treasures_found >= 5:
                print(f"[ACHIEVEMENT] '{self.name}' получил достижение: 'Искатель сокровищ'!")


class NotificationObserver(EventSubscriber):
    """Наблюдатель для отправки уведомлений"""
    def handle_event(self, event: Event):
        notifications = {
            GameEventType.LEVEL_UP: f"🎉 Поздравляем! {event.source.name if hasattr(event.source, 'name') else 'Игрок'} достиг нового уровня!",
            GameEventType.TREASURE_FOUND: f"💎 Найдено сокровище: {event.data.get('item_name', 'неизвестный предмет')}!",
            GameEventType.QUEST_COMPLETED: f"✅ Квест '{event.data.get('quest_name', 'неизвестный')}' завершен!",
            GameEventType.SKILL_UNLOCKED: f"🔮 Новый навык разблокирован: {event.data.get('skill_name', 'неизвестный навык')}!"
        }

        if event.type in notifications:
            print(f"[NOTIFICATION] {notifications[event.type]}")


class EventPublisher:
    """Публикатор событий с фильтрацией"""
    def __init__(self):
        self._subscribers: Dict[GameEventType, List[EventSubscriber]] = {}
        self._global_subscribers: List[EventSubscriber] = []  # Подписчики на все события

    def subscribe(self, subscriber: EventSubscriber, event_types: List[GameEventType] = None):
        """Подписаться на определенные типы событий"""
        if event_types is None:
            # Подписываемся на все события
            self._global_subscribers.append(subscriber)
        else:
            # Подписываемся на определенные типы событий
            for event_type in event_types:
                if event_type not in self._subscribers:
                    self._subscribers[event_type] = []
                if subscriber not in self._subscribers[event_type]:
                    self._subscribers[event_type].append(subscriber)

    def unsubscribe(self, subscriber: EventSubscriber, event_type: GameEventType = None):
        """Отписаться от событий"""
        if event_type is None:
            # Отписываемся от всех событий
            if subscriber in self._global_subscribers:
                self._global_subscribers.remove(subscriber)
            for subscribers_list in self._subscribers.values():
                if subscriber in subscribers_list:
                    subscribers_list.remove(subscriber)
        else:
            # Отписываемся от определенного типа событий
            if event_type in self._subscribers and subscriber in self._subscribers[event_type]:
                self._subscribers[event_type].remove(subscriber)

    def publish(self, event: Event):
        """Опубликовать событие"""
        # Уведомляем глобальных подписчиков
        for subscriber in self._global_subscribers:
            if subscriber.can_handle_event(event.type):
                subscriber.handle_event(event)

        # Уведомляем подписчиков на конкретный тип события
        if event.type in self._subscribers:
            for subscriber in self._subscribers[event.type]:
                if subscriber.can_handle_event(event.type):
                    subscriber.handle_event(event)


# Пример использования системы с фильтрацией
publisher = EventPublisher()

# Создаем подписчиков
health_bar = HealthBarObserver("HealthBar")
achievements = AchievementObserver("Player")
notifications = NotificationObserver("SystemNotifier")

# Подписываем на определенные события
publisher.subscribe(health_bar, [GameEventType.HEALTH_CHANGED, GameEventType.PLAYER_DAMAGE_TAKEN])
publisher.subscribe(achievements, [GameEventType.PLAYER_DAMAGE_TAKEN, GameEventType.ENEMY_DEFEATED, GameEventType.TREASURE_FOUND])
publisher.subscribe(notifications, [GameEventType.LEVEL_UP, GameEventType.TREASURE_FOUND, GameEventType.QUEST_COMPLETED, GameEventType.SKILL_UNLOCKED])

# Создаем игрока
player = Player("Артур", health=100)

# Публикуем различные события
print("=== Публикация событий ===")

# Событие получения урона
damage_event = Event(GameEventType.PLAYER_DAMAGE_TAKEN, player, {"damage_amount": 25, "current_health": 75})
publisher.publish(damage_event)

# Событие повышения уровня
level_up_event = Event(GameEventType.LEVEL_UP, player, {"new_level": 2})
publisher.publish(level_up_event)

# Событие нахождения сокровища
treasure_event = Event(GameEventType.TREASURE_FOUND, player, {"item_name": "Меч короля"})
publisher.publish(treasure_event)

# Событие уничтожения врага
enemy = Enemy("Гоблин", health=50, attack_power=10)
enemy_defeated_event = Event(GameEventType.ENEMY_DEFEATED, enemy)
publisher.publish(enemy_defeated_event)

# Событие изменения здоровья
health_change_event = Event(GameEventType.HEALTH_CHANGED, player, {"current_health": 80, "max_health": 100})
publisher.publish(health_change_event)

print("\n=== Статистика достижений ===")
print(f"Нанесено урона: {achievements.damage_dealt}")
print(f"Повержено врагов: {achievements.enemies_defeated}")
print(f"Найдено сокровищ: {achievements.treasures_found}")
```

### Задача 4: Асинхронный Observer для игровых событий (20 баллов)
Реализуйте асинхронную систему наблюдения:
- Использование asyncio для асинхронных уведомлений
- Классы `AsyncSubject` и `AsyncObserver`
- Обработка уведомлений в отдельных задачах

```python
import asyncio
from typing import List, Awaitable, Callable

class AsyncObserver(ABC):
    """Асинхронный наблюдатель"""
    @abstractmethod
    async def update_async(self, event_type: str, data: dict = None):
        """Асинхронное обновление при получении уведомления"""
        pass

class AsyncSubject:
    """Асинхронный субъект, за которым могут наблюдать"""
    def __init__(self):
        self._async_observers: List[AsyncObserver] = []
        self._notification_tasks: List[asyncio.Task] = []

    def attach_async(self, observer: AsyncObserver):
        """Подписаться на асинхронные уведомления"""
        if observer not in self._async_observers:
            self._async_observers.append(observer)

    def detach_async(self, observer: AsyncObserver):
        """Отписаться от асинхронных уведомлений"""
        if observer in self._async_observers:
            self._async_observers.remove(observer)

    async def notify_async(self, event_type: str, data: dict = None):
        """Асинхронно уведомить всех наблюдателей"""
        tasks = []
        for observer in self._async_observers:
            task = asyncio.create_task(observer.update_async(event_type, data))
            tasks.append(task)
            self._notification_tasks.append(task)

        # Ждем завершения всех задач уведомления
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def cleanup_tasks(self):
        """Очистить завершенные задачи"""
        self._notification_tasks = [task for task in self._notification_tasks if not task.done()]


class AsyncPlayerStatsObserver(AsyncObserver):
    """Асинхронный наблюдатель за статистикой игрока"""
    def __init__(self, name: str):
        self.name = name
        self.stats = {"damage_taken": 0, "healing_received": 0, "levelups": 0}

    async def update_async(self, event_type: str, data: dict = None):
        """Обработать событие асинхронно"""
        # Имитация асинхронной обработки (например, запись в базу данных)
        await asyncio.sleep(0.1)  # Небольшая задержка для имитации работы
        
        if event_type == "player_damaged":
            damage = data.get("damage_amount", 0) if data else 0
            self.stats["damage_taken"] += damage
            print(f"[ASYNC_STATS] {self.name}: Игрок получил {damage} урона. Всего: {self.stats['damage_taken']}")
        elif event_type == "player_healed":
            healing = data.get("healing_amount", 0) if data else 0
            self.stats["healing_received"] += healing
            print(f"[ASYNC_STATS] {self.name}: Игрок получил {healing} лечения. Всего: {self.stats['healing_received']}")
        elif event_type == "player_leveled_up":
            self.stats["levelups"] += 1
            print(f"[ASYNC_STATS] {self.name}: Игрок повысил уровень! Всего повышений: {self.stats['levelups']}")


class AsyncBattleLogger(AsyncObserver):
    """Асинхронный логгер боевых действий"""
    def __init__(self, filename: str = "battle_log.txt"):
        self.filename = filename
        self.log_entries = []

    async def update_async(self, event_type: str, data: dict = None):
        """Обработать событие асинхронно и записать в лог"""
        # Имитация асинхронной записи в файл
        await asyncio.sleep(0.05)  # Небольшая задержка для имитации записи в файл
        
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {event_type}: {data}"
        self.log_entries.append(entry)
        print(f"[ASYNC_LOGGER] Записано в лог: {entry}")

    def get_log_entries(self):
        """Получить все записи лога"""
        return self.log_entries.copy()


class AsyncAchievementNotifier(AsyncObserver):
    """Асинхронный обработчик достижений"""
    def __init__(self):
        self.unlocked_achievements = []

    async def update_async(self, event_type: str, data: dict = None):
        """Обработать событие и проверить достижения"""
        # Имитация асинхронной проверки достижений (например, запрос к серверу)
        await asyncio.sleep(0.15)
        
        if event_type == "player_damaged" and data and data.get("damage_amount", 0) >= 50:
            achievement = "Выносливость: Выдержал сильный удар"
            self.unlocked_achievements.append(achievement)
            print(f"[ASYNC_ACHIEVEMENT] Разблокировано достижение: {achievement}")
        elif event_type == "player_leveled_up" and data and data.get("new_level", 0) >= 10:
            achievement = "Опытный воин: Достиг 10 уровня"
            self.unlocked_achievements.append(achievement)
            print(f"[ASYNC_ACHIEVEMENT] Разблокировано достижение: {achievement}")


# Пример использования асинхронной системы
async def async_game_simulation():
    """Асинхронная симуляция игровых событий"""
    # Создаем субъект (игрока)
    player = Player("Артур", health=100)
    subject = AsyncSubject()  # Используем асинхронный субъект для уведомлений

    # Создаем асинхронных наблюдателей
    stats_observer = AsyncPlayerStatsObserver("Статистик")
    logger = AsyncBattleLogger("battle_log.txt")
    achievements = AsyncAchievementNotifier()

    # Подписываем наблюдателей
    subject.attach_async(stats_observer)
    subject.attach_async(logger)
    subject.attach_async(achievements)

    print("=== Асинхронная симуляция игровых событий ===")

    # Симулируем серию игровых событий
    events = [
        ("player_damaged", {"player": player, "damage_amount": 25}),
        ("player_healed", {"player": player, "healing_amount": 30}),
        ("player_damaged", {"player": player, "damage_amount": 55}),  # Большой урон для достижения
        ("player_leveled_up", {"player": player, "new_level": 10}),  # Уровень для достижения
        ("player_damaged", {"player": player, "damage_amount": 15}),
    ]

    for event_type, event_data in events:
        print(f"\nГенерация события: {event_type}")
        await subject.notify_async(event_type, event_data)
        await asyncio.sleep(0.1)  # Небольшая пауза между событиями

    # Ожидаем завершения всех задач уведомления
    await subject.cleanup_tasks()

    print(f"\n=== Результаты асинхронной обработки ===")
    print(f"Статистика игрока: {stats_observer.stats}")
    print(f"Количество записей в логе: {len(logger.get_log_entries())}")
    print(f"Разблокированные достижения: {len(achievements.unlocked_achievements)}")
    for achievement in achievements.unlocked_achievements:
        print(f"  - {achievement}")


# Запуск асинхронной симуляции
# asyncio.run(async_game_simulation())
```

### Задача 5: Практическое применение Observer в игровой системе (20 баллов)
Создайте систему уведомлений для социальной сети:
- Класс `PlayerProfile` как наблюдаемый объект
- Наблюдатели: `FriendNotifier`, `FeedUpdater`, `NotificationService`
- Уведомления о действиях игрока

```python
class PlayerProfile(Subject):
    """
    Профиль игрока как наблюдаемый объект
    """
    def __init__(self, username: str, level: int = 1):
        super().__init__()
        self.username = username
        self._level = level
        self._health = 100
        self._max_health = 100
        self._experience = 0
        self._gold = 0
        self._achievements = []
        self._online_status = "offline"
        self._last_action = None

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        old_level = self._level
        self._level = value
        if self._level > old_level:
            self._last_action = f"Достиг уровня {self._level}"
            self.notify("player_level_up", {"profile": self, "old_level": old_level, "new_level": self._level})

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        old_health = self._health
        self._health = max(0, min(self._max_health, value))
        if old_health != self._health:
            action = "восстановил" if self._health > old_health else "потерял"
            change = abs(self._health - old_health)
            self._last_action = f"{action} {change} здоровья"
            self.notify("player_health_change", {
                "profile": self, 
                "old_health": old_health, 
                "new_health": self._health,
                "change": change,
                "action": action
            })

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value: int):
        old_gold = self._gold
        self._gold = max(0, value)
        if old_gold != self._gold:
            action = "получил" if self._gold > old_gold else "потратил"
            change = abs(self._gold - old_gold)
            self._last_action = f"{action} {change} золота"
            self.notify("player_gold_change", {
                "profile": self, 
                "old_gold": old_gold, 
                "new_gold": self._gold,
                "change": change,
                "action": action
            })

    @property
    def online_status(self):
        return self._online_status

    @online_status.setter
    def online_status(self, status: str):
        old_status = self._online_status
        self._online_status = status
        if old_status != self._online_status:
            self._last_action = f"изменил статус на {status}"
            self.notify("player_status_change", {
                "profile": self, 
                "old_status": old_status, 
                "new_status": status
            })

    def add_experience(self, exp: int):
        """Добавить опыт и возможно повысить уровень"""
        self._experience += exp
        self._last_action = f"получил {exp} опыта"
        self.notify("player_experience_gain", {"profile": self, "exp_gained": exp, "total_exp": self._experience})
        # Проверяем, не пора ли повысить уровень
        required_exp = self._level * 100
        if self._experience >= required_exp:
            self.level_up()

    def level_up(self):
        """Повысить уровень"""
        self._experience = 0
        self._level += 1
        self._max_health += 20
        self.health = self._max_health  # Полное восстановление при уровне
        self.level = self._level

    def unlock_achievement(self, achievement_name: str):
        """Разблокировать достижение"""
        if achievement_name not in self._achievements:
            self._achievements.append(achievement_name)
            self._last_action = f"разблокировал достижение '{achievement_name}'"
            self.notify("achievement_unlocked", {"profile": self, "achievement": achievement_name})


class FriendNotifier(Observer):
    """
    Наблюдатель для уведомления друзей о действиях игрока
    """
    def __init__(self, friend_list: List[str]):
        self.friend_list = friend_list

    def update(self, event_type: str, data: dict = None):
        if event_type in ["player_level_up", "achievement_unlocked", "player_status_change"]:
            profile = data.get("profile") if data else None
            if profile:
                if event_type == "player_level_up":
                    new_level = data.get("new_level", "N/A")
                    print(f"[FRIEND_NOTIFIER] Друзьям {profile.username} отправлено уведомление: 'Ура! {profile.username} достиг {new_level} уровня!'")
                elif event_type == "achievement_unlocked":
                    achievement = data.get("achievement", "N/A")
                    print(f"[FRIEND_NOTIFIER] Друзьям {profile.username} отправлено уведомление: '{profile.username} разблокировал достижение {achievement}!'")
                elif event_type == "player_status_change":
                    new_status = data.get("new_status", "N/A")
                    print(f"[FRIEND_NOTIFIER] Друзьям {profile.username} отправлено уведомление: '{profile.username} теперь {new_status}'")


class FeedUpdater(Observer):
    """
    Наблюдатель для обновления ленты новостей
    """
    def __init__(self):
        self.feed = []

    def update(self, event_type: str, data: dict = None):
        profile = data.get("profile") if data else None
        if profile:
            if event_type == "player_level_up":
                new_level = data.get("new_level", "N/A")
                feed_entry = f"{profile.username} достиг {new_level} уровня! 🎉"
            elif event_type == "achievement_unlocked":
                achievement = data.get("achievement", "N/A")
                feed_entry = f"{profile.username} разблокировал достижение: {achievement}! 🏆"
            elif event_type == "player_status_change":
                new_status = data.get("new_status", "N/A")
                feed_entry = f"{profile.username} теперь {new_status} 💬"
            elif event_type == "player_experience_gain":
                exp_gained = data.get("exp_gained", "N/A")
                feed_entry = f"{profile.username} получил {exp_gained} опыта! ⭐"
            elif event_type == "player_gold_change":
                action = data.get("action", "")
                change = data.get("change", "")
                feed_entry = f"{profile.username} {action} {change} золота! 💰"
            else:
                return  # Для других событий не добавляем в ленту

            self.feed.append(feed_entry)
            print(f"[FEED_UPDATER] Новая запись в ленте: {feed_entry}")

    def get_recent_posts(self, count: int = 5) -> List[str]:
        """Получить последние записи из ленты"""
        return self.feed[-count:]


class NotificationService(Observer):
    """
    Сервис уведомлений для игрока
    """
    def __init__(self, player_username: str):
        self.player_username = player_username
        self.notifications = []

    def update(self, event_type: str, data: dict = None):
        profile = data.get("profile") if data else None
        if profile and profile.username != self.player_username:
            # Этот сервис уведомлений только для других игроков
            return

        if event_type in ["player_level_up", "achievement_unlocked", "player_experience_gain", "player_gold_change"]:
            if event_type == "player_level_up":
                new_level = data.get("new_level", "N/A")
                notification = f"Поздравляем! Вы достигли {new_level} уровня!"
            elif event_type == "achievement_unlocked":
                achievement = data.get("achievement", "N/A")
                notification = f"Вы разблокировали достижение: {achievement}!"
            elif event_type == "player_experience_gain":
                exp_gained = data.get("exp_gained", "N/A")
                notification = f"Вы получили {exp_gained} опыта!"
            elif event_type == "player_gold_change":
                action = data.get("action", "")
                change = data.get("change", "")
                notification = f"Вы {action} {change} золота!"
            else:
                return

            self.notifications.append(notification)
            print(f"[NOTIFICATION_SERVICE] Уведомление для {self.player_username}: {notification}")

    def get_unread_notifications(self) -> List[str]:
        """Получить непрочитанные уведомления"""
        return self.notifications.copy()


# Пример использования системы уведомлений для социальной сети
def social_network_demo():
    print("=== Демонстрация системы уведомлений для социальной сети ===\n")

    # Создаем профиль игрока
    player = PlayerProfile("Артур", level=1)

    # Создаем наблюдателей
    friends_notifier = FriendNotifier(["Борис", "Виктория", "Елена"])
    feed_updater = FeedUpdater()
    notification_service = NotificationService("Артур")

    # Подписываем наблюдателей на профиль игрока
    player.attach(friends_notifier)
    player.attach(feed_updater)
    player.attach(notification_service)

    print(f"Игрок: {player.username}, уровень: {player.level}, золото: {player.gold}\n")

    # Симулируем действия игрока
    print("1. Игрок получает опыт:")
    player.add_experience(150)

    print("\n2. Игрок получает золото:")
    player.gold = 100

    print("\n3. Игрок тратит золото:")
    player.gold = 75

    print("\n4. Игрок разблокирует достижение:")
    player.unlock_achievement("Первые шаги")

    print("\n5. Изменение статуса игрока:")
    player.online_status = "в сети"

    print("\n6. Игрок получает дополнительный опыт:")
    player.add_experience(200)

    print("\n=== Результаты ===")
    print(f"Итоговый уровень: {player.level}")
    print(f"Итоговое золото: {player.gold}")

    print(f"\nПоследние записи в ленте ({len(feed_updater.get_recent_posts())}):")
    for post in feed_updater.get_recent_posts():
        print(f"  - {post}")

    print(f"\nУведомления для игрока ({len(notification_service.get_unread_notifications())}):")
    for notification in notification_service.get_unread_notifications():
        print(f"  - {notification}")


social_network_demo()
```

## Методические указания
1. Используйте абстрактные классы для определения интерфейсов наблюдателя и субъекта
2. Обеспечьте гибкость системы через параметры уведомлений и фильтрацию событий
3. Обрабатывайте ошибки при уведомлении подписчиков, чтобы одно неудачное уведомление не повлияло на другие
4. Рассмотрите асинхронные подходы для масштабируемых игровых систем
5. Используйте enum для типов событий, чтобы избежать опечаток в строках

## Требования к отчету
- Исходный код всех реализаций Observer с игровой тематикой
- Примеры использования каждого подхода в игровом контексте
- Сравнение синхронных и асинхронных реализаций и их применимость в игровых приложениях

## Критерии оценки
- Корректная реализация паттерна Observer в игровом контексте: 50%
- Понимание различных вариантов применения в игровой разработке: 30%
- Качество кода и документация в игровом контексте: 20%

## Практические задания

### Задание 1: Система боевых уведомлений

Создайте систему уведомлений для боевой системы, где наблюдатели отслеживают:
- Нанесение урона
- Получение урона
- Использование способностей
- Смерть персонажа
- Изменение статуса (отравление, заморозка и т.д.)

```python
class BattleObserver(Observer):
    """
    Наблюдатель за боевыми действиями
    """
    def __init__(self, battle_log: List[str] = None):
        self.battle_log = battle_log or []
        self.damage_stats = {"dealt": 0, "received": 0}

    def update(self, event_type: str, data: dict = None):
        if event_type == "character_attacked":
            attacker = data.get("attacker")
            target = data.get("target")
            damage = data.get("damage", 0)
            self.damage_stats["dealt"] += damage
            log_entry = f"{attacker.name if attacker else 'Неизвестный'} атаковал {target.name if target else 'цель'} на {damage} урона"
            self.battle_log.append(log_entry)
            print(f"[BATTLE_LOG] {log_entry}")
        elif event_type == "character_damaged":
            target = data.get("target")
            damage = data.get("damage", 0)
            self.damage_stats["received"] += damage
            log_entry = f"{target.name if target else 'Неизвестный'} получил {damage} урона"
            self.battle_log.append(log_entry)
            print(f"[BATTLE_LOG] {log_entry}")
        elif event_type == "character_died":
            character = data.get("character")
            log_entry = f"{character.name if character else 'Неизвестный'} погибает!"
            self.battle_log.append(log_entry)
            print(f"[BATTLE_LOG] {log_entry}")
        elif event_type == "ability_used":
            user = data.get("user")
            ability = data.get("ability")
            target = data.get("target")
            log_entry = f"{user.name if user else 'Неизвестный'} использовал {ability} на {target.name if target else 'цель'}"
            self.battle_log.append(log_entry)
            print(f"[BATTLE_LOG] {log_entry}")


class BattleManager:
    """
    Менеджер боя, который управляет событиями
    """
    def __init__(self):
        self.subject = Subject()
        self.observer = BattleObserver()

    def add_observer(self, observer: Observer):
        self.subject.attach(observer)

    def character_attack(self, attacker, target, base_damage=10):
        """Симуляция атаки"""
        # Здесь могла бы быть боевая логика
        actual_damage = max(1, base_damage - (target.defense if hasattr(target, 'defense') else 0))
        target.take_damage(actual_damage)
        
        # Уведомляем о событиях
        self.subject.notify("character_attacked", {"attacker": attacker, "target": target, "damage": actual_damage})
        self.subject.notify("character_damaged", {"target": target, "damage": actual_damage})
        
        if not target.is_alive:
            self.subject.notify("character_died", {"character": target})

    def use_ability(self, user, ability, target=None):
        """Использование способности"""
        self.subject.notify("ability_used", {"user": user, "ability": ability, "target": target})


# Пример использования
battle_manager = BattleManager()
battle_observer = BattleObserver()
battle_manager.add_observer(battle_observer)

# Создаем персонажей для боя
player = Player("Герой", health=100)
enemy = Enemy("Враг", health=50, attack_power=15)

print("=== Боевая симуляция ===")
battle_manager.character_attack(player, enemy, 25)
battle_manager.use_ability(player, "Мощная атака", enemy)
battle_manager.character_attack(enemy, player, 15)

print(f"\nСтатистика урона: {battle_observer.damage_stats}")
print(f"Записи в боевом логе: {len(battle_observer.battle_log)}")
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


class QuestObserver(Observer):
    """
    Наблюдатель за квестами
    """
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.completed_quests = []
        self.ongoing_quests = []

    def update(self, event_type: str, data: dict = None):
        if event_type == "quest_accepted":
            quest = data.get("quest")
            if quest:
                self.ongoing_quests.append(quest)
                print(f"[QUEST_SYSTEM] {self.player_name} принял квест: {quest.title}")
        elif event_type == "quest_progress_updated":
            quest = data.get("quest")
            progress = data.get("progress", 0)
            goal = data.get("goal", 1)
            if quest:
                percentage = (progress / goal) * 100
                print(f"[QUEST_SYSTEM] Прогресс квеста '{quest.title}': {percentage:.1f}% ({progress}/{goal})")
        elif event_type == "quest_completed":
            quest = data.get("quest")
            if quest:
                self.ongoing_quests.remove(quest)
                self.completed_quests.append(quest)
                print(f"[QUEST_SYSTEM] {self.player_name} завершил квест: {quest.title}")
                print(f"[QUEST_SYSTEM] Награда: {quest.xp_reward} XP, {quest.gold_reward} золота")


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

    def accept_quest(self, quest_title: str, player):
        """Принять квест игроком"""
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_completed:
                self.notify("quest_accepted", {"quest": quest, "player": player})
                return quest
        return None

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

    def complete_quest(self, quest: Quest, player):
        """Завершить квест и дать награду"""
        if quest.is_completed:
            # Даем награду игроку
            player.gain_experience(quest.xp_reward)
            player.gold += quest.gold_reward
            self.notify("quest_reward_given", {
                "quest": quest,
                "player": player,
                "xp_reward": quest.xp_reward,
                "gold_reward": quest.gold_reward
            })


# Пример использования системы квестов
quest_manager = QuestManager()
quest_observer = QuestObserver("Артур")

# Подписываем наблюдателя
quest_manager.attach(quest_observer)

# Создаем квесты
kill_goblins_quest = Quest("Убить гоблинов", "Убейте 5 гоблинов в лесу", 100, 50)
find_treasure_quest = Quest("Найти сокровище", "Найдите спрятанное сокровище в пещере", 150, 100)

# Добавляем квесты в менеджер
quest_manager.add_quest(kill_goblins_quest)
quest_manager.add_quest(find_treasure_quest)

# Создаем игрока
player = Player("Артур", health=100)

print("=== Система квестов ===")
# Игрок принимает квест
accepted_quest = quest_manager.accept_quest("Убить гоблинов", player)

# Обновляем прогресс квеста
for i in range(5):
    quest_manager.update_quest_progress(accepted_quest)
    # Симулируем убийство гоблина
    enemy = Enemy(f"Гоблин_{i+1}", health=30, attack_power=5)
    print(f"  Убит {enemy.name}")

print(f"\nЗавершенные квесты: {len(quest_observer.completed_quests)}")
```

### Задача 3: Сравнение различных реализаций Observer

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

## Дополнительные задания

### Задание 4: Система ачивок и статистики

Создайте комплексную систему, которая отслеживает различные игровые достижения и собирает статистику игрока с использованием Observer паттерна.

### Задание 5: Система событий на основе Publisher-Subscriber

Реализуйте систему событий, вдохновленную паттерном Publisher-Subscriber, которая может использоваться в крупных игровых проектах с высокой масштабируемостью.

## Контрольные вопросы:
1. В чем разница между Observer и Publisher-Subscriber паттернами в игровом контексте?
2. Как обеспечить потокобезопасность системы наблюдателей в многопоточной игровой среде?
3. Какие преимущества дает использование Observer в системах уведомлений игроков?
4. Как обрабатывать ошибки в наблюдателях, чтобы не прерывать выполнение других наблюдателей?
5. Как использовать Observer для создания слабосвязанной архитектуры игровых систем?