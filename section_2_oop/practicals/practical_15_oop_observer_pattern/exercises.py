"""
Практическое задание 15: Паттерн Observer в игровом контексте

Цель: Реализовать паттерн Observer для создания системы подписки на события и уведомления об изменениях в игровой среде.
"""

from abc import ABC, abstractmethod
from typing import List

# Уровень 1 - Начальный
# Задание 1.1: Создать базовую реализацию Observer для игровых событий

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
        # TODO: Реализуйте добавление наблюдателя
        pass

    def detach(self, observer: Observer):
        """Отписаться от уведомлений"""
        # TODO: Реализуйте удаление наблюдателя
        pass

    def notify(self, event_type: str, data: dict = None):
        """Уведомить всех наблюдателей об изменении"""
        # TODO: Реализуйте уведомление всех наблюдателей
        pass


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
        # TODO: Реализуйте сеттер здоровья с уведомлением наблюдателей
        # когда здоровье изменяется, особенно при смерти
        pass

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        # TODO: Реализуйте сеттер уровня с уведомлением наблюдателей
        # при повышении уровня
        pass

    def take_damage(self, damage: int):
        """Получить урон"""
        # TODO: Реализуйте получение урона и уведомление
        pass

    def gain_experience(self, exp: int):
        """Получить опыт"""
        # TODO: Реализуйте получение опыта и уведомление
        # проверьте, не пора ли повысить уровень
        pass

    def level_up(self):
        """Повысить уровень игрока"""
        # TODO: Реализуйте повышение уровня
        pass

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
        # TODO: Реализуйте сеттер здоровья с уведомлением наблюдателей
        pass

    def take_damage(self, damage: int):
        """Получить урон"""
        # TODO: Реализуйте получение урона и уведомление
        pass


# Уровень 2 - Средний
# Задание 2.1: Реализовать систему уведомлений с использованием callback-функций

class EventManager:
    """
    Менеджер событий для управления игровыми событиями
    """
    def __init__(self):
        # TODO: Реализуйте инициализацию хранилища обработчиков
        pass

    def subscribe(self, event_type: str, handler):
        """Подписаться на событие определенного типа"""
        # TODO: Реализуйте добавление обработчика события
        pass

    def unsubscribe(self, event_type: str, handler):
        """Отписаться от события определенного типа"""
        # TODO: Реализуйте удаление обработчика события
        pass

    def trigger_event(self, event_type: str, data: dict = None):
        """Вызвать событие и уведомить всех подписчиков"""
        # TODO: Реализуйте вызов всех обработчиков для события
        pass

    def get_subscribers_count(self, event_type: str) -> int:
        """Получить количество подписчиков на событие"""
        # TODO: Реализуйте подсчет подписчиков
        pass


# Примеры обработчиков событий (заполните реализации)
def player_damaged_handler(event_type: str, data: dict):
    """Обработчик события получения урона игроком"""
    # TODO: Реализуйте обработчик
    pass

def enemy_defeated_handler(event_type: str, data: dict):
    """Обработчик события уничтожения врага"""
    # TODO: Реализуйте обработчик
    pass

def level_up_handler(event_type: str, data: dict):
    """Обработчик события повышения уровня"""
    # TODO: Реализуйте обработчик
    pass

def experience_gained_handler(event_type: str, data: dict):
    """Обработчик события получения опыта"""
    # TODO: Реализуйте обработчик
    pass

def health_changed_handler(event_type: str, data: dict):
    """Обработчик события изменения здоровья"""
    # TODO: Реализуйте обработчик
    pass


# Уровень 3 - Повышенный
# Задание 3.1: Реализовать систему уведомлений с фильтрацией

from enum import Enum

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
    def __init__(self, event_type, source=None, data: dict = None):
        # TODO: Реализуйте инициализацию события
        pass


class EventSubscriber(ABC):
    """Абстрактный класс подписчика на события"""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def handle_event(self, event):
        """Обработать событие"""
        pass

    def can_handle_event(self, event_type) -> bool:
        """Проверить, может ли подписчик обрабатывать событие данного типа"""
        # TODO: Реализуйте проверку возможности обработки события
        return True


class HealthBarObserver(EventSubscriber):
    """Наблюдатель за изменением здоровья"""
    def handle_event(self, event):
        # TODO: Реализуйте обработку событий изменения здоровья
        pass


class AchievementObserver(EventSubscriber):
    """Наблюдатель за достижениями"""
    def __init__(self, name: str):
        super().__init__(name)
        # TODO: Инициализируйте счетчики для отслеживания достижений
        pass

    def handle_event(self, event):
        # TODO: Реализуйте обработку событий для отслеживания достижений
        pass


class NotificationObserver(EventSubscriber):
    """Наблюдатель для отправки уведомлений"""
    def handle_event(self, event):
        # TODO: Реализуйте обработку событий для отправки уведомлений
        pass


class EventPublisher:
    """Публикатор событий с фильтрацией"""
    def __init__(self):
        # TODO: Инициализируйте хранилище подписчиков
        pass

    def subscribe(self, subscriber, event_types=None):
        """Подписаться на определенные типы событий"""
        # TODO: Реализуйте добавление подписчика
        pass

    def unsubscribe(self, subscriber, event_type=None):
        """Отписаться от событий"""
        # TODO: Реализуйте удаление подписчика
        pass

    def publish(self, event):
        """Опубликовать событие"""
        # TODO: Реализуйте публикацию события и уведомление подписчиков
        pass


# Задание 3.2: Практическое применение Observer в игровой системе

class PlayerProfile(Subject):
    """
    Профиль игрока как наблюдаемый объект
    """
    def __init__(self, username: str, level: int = 1):
        super().__init__()
        # TODO: Инициализируйте атрибуты профиля игрока
        pass

    @property
    def level(self):
        # TODO: Реализуйте геттер уровня
        pass

    @level.setter
    def level(self, value: int):
        # TODO: Реализуйте сеттер уровня с уведомлением
        pass

    @property
    def health(self):
        # TODO: Реализуйте геттер здоровья
        pass

    @health.setter
    def health(self, value: int):
        # TODO: Реализуйте сеттер здоровья с уведомлением
        pass

    @property
    def gold(self):
        # TODO: Реализуйте геттер золота
        pass

    @gold.setter
    def gold(self, value: int):
        # TODO: Реализуйте сеттер золота с уведомлением
        pass

    @property
    def online_status(self):
        # TODO: Реализуйте геттер статуса
        pass

    @online_status.setter
    def online_status(self, status: str):
        # TODO: Реализуйте сеттер статуса с уведомлением
        pass

    def add_experience(self, exp: int):
        """Добавить опыт и возможно повысить уровень"""
        # TODO: Реализуйте добавление опыта с уведомлением
        pass

    def level_up(self):
        """Повысить уровень"""
        # TODO: Реализуйте повышение уровня
        pass

    def unlock_achievement(self, achievement_name: str):
        """Разблокировать достижение"""
        # TODO: Реализуйте разблокировку достижения с уведомлением
        pass


class FriendNotifier(Observer):
    """
    Наблюдатель для уведомления друзей о действиях игрока
    """
    def __init__(self, friend_list: List[str]):
        # TODO: Инициализируйте список друзей
        pass

    def update(self, event_type: str, data: dict = None):
        # TODO: Реализуйте обработку событий для уведомления друзей
        pass


class FeedUpdater(Observer):
    """
    Наблюдатель для обновления ленты новостей
    """
    def __init__(self):
        # TODO: Инициализируйте ленту новостей
        pass

    def update(self, event_type: str, data: dict = None):
        # TODO: Реализуйте обновление ленты новостей
        pass

    def get_recent_posts(self, count: int = 5) -> List[str]:
        """Получить последние записи из ленты"""
        # TODO: Реализуйте получение последних записей
        pass


class NotificationService(Observer):
    """
    Сервис уведомлений для игрока
    """
    def __init__(self, player_username: str):
        # TODO: Инициализируйте сервис уведомлений
        pass

    def update(self, event_type: str, data: dict = None):
        # TODO: Реализуйте обработку событий для уведомлений
        pass

    def get_unread_notifications(self) -> List[str]:
        """Получить непрочитанные уведомления"""
        # TODO: Реализуйте получение непрочитанных уведомлений
        pass


# Тестирование реализации (раскомментируйте после реализации)
"""
# Тестирование уровня 1
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

# Тестирование уровня 2
event_manager = EventManager()

# Подписываем обработчики на события
event_manager.subscribe("player_damaged", player_damaged_handler)
event_manager.subscribe("enemy_died", enemy_defeated_handler)
event_manager.subscribe("player_leveled_up", level_up_handler)
event_manager.subscribe("player_gained_experience", experience_gained_handler)
event_manager.subscribe("player_health_changed", health_changed_handler)
event_manager.subscribe("enemy_health_changed", health_changed_handler)

# Тестирование уровня 3
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
"""