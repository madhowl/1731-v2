"""
Пример: Паттерн Observer в игровых персонажах
"""

from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Абстрактный класс наблюдателя"""
    @abstractmethod
    def update(self, subject, event_type: str, data: dict = None):
        """Метод обновления при уведомлении от субъекта"""
        pass

class Subject(ABC):
    """Абстрактный класс субъекта (объекта наблюдения)"""
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Добавить наблюдателя"""
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """Удалить наблюдателя"""
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict = None):
        """Уведомить всех наблюдателей о событии"""
        for observer in self._observers:
            observer.update(self, event_type, data)

class GameCharacter(Subject):
    """Игровой персонаж, за которым могут наблюдать другие объекты"""
    def __init__(self, name: str, health: int = 100, level: int = 1):
        super().__init__()
        self.name = name
        self._health = health
        self._max_health = health
        self._level = level
        self._experience = 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        old_health = self._health
        self._health = max(0, min(self._max_health, value))
        # Уведомляем наблюдателей об изменении здоровья
        self.notify("health_changed", {
            "old_value": old_health, 
            "new_value": self._health,
            "max_value": self._max_health
        })
        # Проверяем, не умер ли персонаж
        if self._health <= 0:
            self.notify("character_died", {"character": self})

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        old_level = self._level
        self._level = value
        # Уведомляем наблюдателей о повышении уровня
        if self._level > old_level:
            self.notify("level_up", {
                "old_level": old_level,
                "new_level": self._level
            })

    def take_damage(self, damage: int):
        """Получить урон"""
        actual_damage = max(0, damage)
        self.health -= actual_damage
        self.notify("took_damage", {
            "damage_amount": actual_damage,
            "remaining_health": self._health
        })

    def gain_experience(self, exp: int):
        """Получить опыт"""
        self._experience += exp
        self.notify("gained_experience", {
            "exp_gained": exp,
            "total_exp": self._experience
        })
        # Проверяем, не пора ли повысить уровень
        required_exp = self._level * 100  # Упрощенная формула
        if self._experience >= required_exp:
            self.level_up()

    def level_up(self):
        """Повысить уровень персонажа"""
        self._experience = 0  # Сбрасываем опыт при повышении уровня
        self._level += 1
        self._max_health += 20  # Увеличиваем максимальное здоровье
        self.health = self._max_health  # Полностью восстанавливаем здоровье
        self.level = self._level  # Вызываем сеттер для уведомления

class HealthBarUI(Observer):
    """UI-компонент, отображающий здоровье персонажа"""
    def __init__(self, character_name: str):
        self.character_name = character_name

    def update(self, subject, event_type: str, data: dict = None):
        if isinstance(subject, GameCharacter) and event_type == "health_changed":
            print(f"[UI] Здоровье {subject.name}: {data['new_value']}/{data['max_value']}")

class DeathAnnouncer(Observer):
    """Компонент, объявляющий о смерти персонажа"""
    def update(self, subject, event_type: str, data: dict = None):
        if event_type == "character_died":
            character = data["character"]
            print(f"[АННОУНСЕР] {character.name} погибает!")

class ExperienceTracker(Observer):
    """Компонент, отслеживающий получение опыта"""
    def __init__(self):
        self.total_experience = 0

    def update(self, subject, event_type: str, data: dict = None):
        if event_type == "gained_experience":
            exp_gained = data["exp_gained"]
            self.total_experience += exp_gained
            print(f"[ОПЫТ] Получено {exp_gained} опыта. Всего: {self.total_experience}")

class LevelUpNotifier(Observer):
    """Компонент, уведомляющий о повышении уровня"""
    def update(self, subject, event_type: str, data: dict = None):
        if event_type == "level_up":
            if isinstance(subject, GameCharacter):
                print(f"[УРОВЕНЬ] {subject.name} достиг {data['new_level']} уровня!")

class AchievementSystem(Observer):
    """Система достижений, реагирующая на события"""
    def __init__(self):
        self.achievements_unlocked = []
        self.health_low_notified = False

    def update(self, subject, event_type: str, data: dict = None):
        if isinstance(subject, GameCharacter):
            # Проверяем достижение "Выживший" - пережить момент, когда здоровье <= 10%
            if event_type == "health_changed":
                health_percentage = (data['new_value'] / data['max_value']) * 10
                if health_percentage <= 10 and not self.health_low_notified:
                    self.health_low_notified = True
                    print(f"[ДОСТИЖЕНИЕ] '{subject.name}' получил достижение: 'Выживший'!")
                    self.achievements_unlocked.append("Выживший")
            elif event_type == "level_up":
                # Проверяем достижение "Быстрорастущий" - достичь 5 уровня
                if data['new_level'] >= 5:
                    print(f"[ДОСТИЖЕНИЕ] '{subject.name}' получил достижение: 'Быстрорастущий'!")
                    self.achievements_unlocked.append("Быстрорастущий")

def demonstrate_observer_pattern():
    """Демонстрация паттерна Observer в игровом контексте"""
    print("=== Демонстрация паттерна Observer в игровом контексте ===\n")

    # Создаем персонажа
    hero = GameCharacter("Артур", health=100, level=1)

    # Создаем наблюдателей
    health_bar = HealthBarUI("Артур")
    death_announcer = DeathAnnouncer()
    exp_tracker = ExperienceTracker()
    level_notifier = LevelUpNotifier()
    achievement_system = AchievementSystem()

    # Подписываем наблюдателей на персонажа
    hero.attach(health_bar)
    hero.attach(death_announcer)
    hero.attach(exp_tracker)
    hero.attach(level_notifier)
    hero.attach(achievement_system)

    print(f"Создан персонаж: {hero.name}, Здоровье: {hero.health}, Уровень: {hero.level}\n")

    # Симуляция игровых событий
    print("1. Персонаж получает урон:")
    hero.take_damage(30)

    print("\n2. Персонаж получает опыт:")
    hero.gain_experience(50)

    print("\n3. Персонаж получает больше опыта (для повышения уровня):")
    hero.gain_experience(70)

    print("\n4. Персонаж снова получает урон:")
    hero.take_damage(80)

    print("\n5. Персонаж получает малое количество здоровья (для проверки достижения):")
    hero.take_damage(85)  # Здоровье станет 5, что <= 10% от 100
    hero.health = 15  # Восстанавливаем немного здоровья

    print("\n6. Персонаж получает много опыта для достижения 5 уровня:")
    for i in range(4):  # Повышаем уровень до 5
        hero.gain_experience(100)

    print(f"\nИтоговое состояние персонажа: {hero.name}, Здоровье: {hero.health}, Уровень: {hero.level}")
    print(f"Разблокированные достижения: {achievement_system.achievements_unlocked}")


if __name__ == "__main__":
    demonstrate_observer_pattern()