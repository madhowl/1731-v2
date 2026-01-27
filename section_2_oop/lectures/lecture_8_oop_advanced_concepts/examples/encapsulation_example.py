"""
Пример: Инкапсуляция и уровни доступа в игровых объектах
"""

class PlayerCharacter:
    """Класс игрока с различными уровнями доступа к данным"""
    def __init__(self, name, level=1, gold=0):
        # Публичный атрибут - доступен извне напрямую
        self.name = name
        self.level = level

        # Защищенный атрибут (начинается с одного подчеркивания)
        # По соглашению не должен использоваться за пределами класса и его потомков
        self._experience = 0
        self._inventory = []  # Инвентарь игрока

        # Приватный атрибут (начинается с двух подчеркиваний)
        # Использует механизм name mangling для "сокрытия" атрибута
        self.__account_balance = gold  # Баланс аккаунта игрока (в игровой валюте)
        self.__password_hash = self.__hash_password("default_password")  # Хеш пароля

    def get_public_info(self):
        """Публичный метод - возвращает общедоступную информацию"""
        return f"Игрок: {self.name}, Уровень: {self.level}, Опыт: {self._experience}"

    def _get_protected_info(self):
        """Защищенный метод - используется внутри класса и его потомков"""
        return f"Инвентарь: {self._inventory}, Опыт: {self._experience}"

    def __hash_password(self, password):
        """Приватный метод - внутреннее использование, не должен вызываться извне"""
        # В реальном приложении использовался бы надежный алгоритм хеширования
        return sum(ord(c) for c in password) % 10000

    def get_account_balance(self):
        """Публичный метод для безопасного доступа к приватному атрибуту"""
        return self.__account_balance

    def set_password(self, new_password):
        """Публичный метод для изменения пароля"""
        self.__password_hash = self.__hash_password(new_password)
        print("Пароль успешно изменен")

    def add_gold(self, amount):
        """Публичный метод для добавления золота с проверкой"""
        if amount > 0:
            self.__account_balance += amount
            print(f"Добавлено {amount} золота. Всего: {self.__account_balance}")
        else:
            print("Невозможно добавить отрицательное количество золота")

    def withdraw_gold(self, amount):
        """Публичный метод для снятия золота с проверкой"""
        if 0 < amount <= self.__account_balance:
            self.__account_balance -= amount
            print(f"Снято {amount} золота. Осталось: {self.__account_balance}")
            return True
        else:
            print("Недостаточно средств или неверная сумма")
            return False

    def get_inventory_size(self):
        """Публичный метод для получения размера инвентаря"""
        return len(self._inventory)

    def _add_item_to_inventory(self, item):
        """Защищенный метод для добавления предмета в инвентарь"""
        if len(self._inventory) < 20:  # Максимальный размер инвентаря
            self._inventory.append(item)
            print(f"Предмет '{item}' добавлен в инвентарь")
            return True
        else:
            print("Инвентарь полон")
            return False

    def __str__(self):
        return f"Игрок {self.name}: уровень {self.level}, {self.__account_balance} золота"


class GameStats:
    """Класс игровой статистики с контролем значений"""
    def __init__(self, name, health=100, mana=50, stamina=100):
        self.name = name
        # Используем приватные атрибуты для хранения значений
        self.__health = self.__validate_stat_value(health, 1, 999, "здоровье")
        self.__max_health = self.__health
        self.__mana = self.__validate_stat_value(mana, 0, 999, "мана")
        self.__max_mana = self.__mana
        self.__stamina = self.__validate_stat_value(stamina, 0, 999, "выносливость")
        self.__max_stamina = self.__stamina

    def __validate_stat_value(self, value, min_val, max_val, stat_name):
        """Валидация значений статистики"""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{stat_name} должно быть числом")
        if value < min_val or value > max_val:
            print(f"Предупреждение: {stat_name} выходит за допустимые пределы [{min_val}, {max_val}], установлено в ближайшее значение")
            return max(min_val, min(max_val, value))
        return value

    @property
    def health(self):
        """Свойство для получения здоровья"""
        return self.__health

    @health.setter
    def health(self, value):
        """Свойство для установки здоровья с проверкой"""
        validated_value = self.__validate_stat_value(value, 0, self.__max_health, "здоровье")
        self.__health = validated_value
        if self.__health == 0:
            print(f"{self.name} погибает!")

    @property
    def mana(self):
        """Свойство для получения маны"""
        return self.__mana

    @mana.setter
    def mana(self, value):
        """Свойство для установки маны с проверкой"""
        self.__mana = self.__validate_stat_value(value, 0, self.__max_mana, "мана")

    @property
    def stamina(self):
        """Свойство для получения выносливости"""
        return self.__stamina

    @stamina.setter
    def stamina(self, value):
        """Свойство для установки выносливости с проверкой"""
        self.__stamina = self.__validate_stat_value(value, 0, self.__max_stamina, "выносливость")

    @property
    def health_percentage(self):
        """Свойство только для чтения - процент здоровья"""
        return (self.__health / self.__max_health) * 100 if self.__max_health > 0 else 0

    @property
    def mana_percentage(self):
        """Свойство только для чтения - процент маны"""
        return (self.__mana / self.__max_mana) * 100 if self.__max_mana > 0 else 0

    @property
    def stamina_percentage(self):
        """Свойство только для чтения - процент выносливости"""
        return (self.__stamina / self.__max_stamina) * 100 if self.__max_stamina > 0 else 0

    def rest(self):
        """Метод для отдыха и восстановления ресурсов"""
        self.__health = self.__max_health
        self.__mana = self.__max_mana
        self.__stamina = self.__max_stamina
        print(f"{self.name} полностью восстановил все ресурсы")


class Player:
    """Класс игрока с использованием свойств для контроля статистики"""
    def __init__(self, name, character_class="Воин"):
        self.name = name
        self.character_class = character_class
        self.stats = GameStats(name, health=120, mana=80, stamina=100)

    def __str__(self):
        return (f"{self.name} ({self.character_class}): "
                f"Здоровье: {self.stats.health}/{self.stats.max_health} "
                f"({self.stats.health_percentage:.1f}%), "
                f"Мана: {self.stats.mana}/{self.stats.max_mana} "
                f"({self.stats.mana_percentage:.1f}%), "
                f"Выносливость: {self.stats.stamina}/{self.stats.max_stamina} "
                f"({self.stats.stamina_percentage:.1f}%)" )


def demonstrate_encapsulation():
    """Демонстрация инкапсуляции"""
    print("=== Демонстрация инкапсуляции ===\n")
    
    # Пример использования
    player = PlayerCharacter("Алекс", gold=100)

    # Публичные атрибуты и методы - можно использовать напрямую
    print(f"Имя игрока: {player.name}")  # Алекс
    print(f"Публичная информация: {player.get_public_info()}")  # Общедоступная информация

    # Защищенные атрибуты - технически доступны, но по соглашению не должны использоваться
    print(f"Защищенный атрибут _experience: {player._experience}")  # 0 - можно получить, но не рекомендуется
    print(f"Защищенная информация: {player._get_protected_info()}")  # Можно вызвать, но не рекомендуется

    # Приватные атрибуты - скрыты через name mangling
    try:
        print(player.__account_balance) # Ошибка AttributeError
    except AttributeError as e:
        print(f"Ошибка доступа к приватному атрибуту: {e}")

    # Но можно получить через name mangling (не рекомендуется делать так на практике)
    print(f"Баланс через name mangling: {player._PlayerCharacter__account_balance}")

    # Правильный способ работы с приватными данными - через публичные методы
    print(f"Баланс: {player.get_account_balance()}")
    player.add_gold(50)
    player.withdraw_gold(30)

    print(f"\nИнформация об игроке: {player}\n")


def demonstrate_properties():
    """Демонстрация использования свойств"""
    print("=== Демонстрация использования свойств ===\n")
    
    # Пример использования свойств
    player = Player("Артур", "Маг")

    print(f"Игрок: {player}")
    print(f"Процент здоровья: {player.stats.health_percentage:.1f}%")

    # Изменение здоровья через свойство с автоматической проверкой
    player.stats.health = 150  # Будет ограничено максимальным значением
    print(f"Здоровье после установки 150: {player.stats.health}")

    player.stats.health = -10  # Будет установлено в 0
    print(f"Здоровье после установки -10: {player.stats.health}")

    # Попытка изменить процент здоровья (только для чтения) - вызовет ошибку
    try:
        player.stats.health_percentage = 50  # Ошибка - свойство только для чтения
    except AttributeError as e:
        print(f"Ошибка при попытке изменить свойство только для чтения: {e}")

    # Восстановление ресурсов
    player.stats.rest()
    print(f"После отдыха: {player}")


if __name__ == "__main__":
    demonstrate_encapsulation()
    demonstrate_properties()