# Решения для практического задания 12: ООП - магические методы в игровом контексте

class GameCharacter:
    """
    Класс игрового персонажа
    """
    def __init__(self, name, health, attack, defense, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = 0
        self.is_alive = True

    def __add__(self, other):
        """Сложение характеристик двух персонажей"""
        if isinstance(other, GameCharacter):
            new_health = self.health + other.health
            new_attack = self.attack + other.attack
            new_defense = self.defense + other.defense
            return GameCharacter(f"{self.name}+{other.name}", new_health, new_attack, new_defense)
        else:
            raise TypeError("Можно складывать только с другим персонажем")

    def __sub__(self, other):
        """Вычитание характеристик (например, для вычисления урона)"""
        if isinstance(other, GameCharacter):
            # Для вычитания используем защиту для уменьшения урона
            damage = max(0, self.attack - other.defense)
            return damage
        else:
            raise TypeError("Можно вычитать только характеристики другого персонажа")

    def __mul__(self, factor):
        """Умножение характеристик на множитель (например, для усиления)"""
        if isinstance(factor, (int, float)):
            new_char = GameCharacter(
                f"{self.name}*{factor}", 
                int(self.health * factor), 
                int(self.attack * factor), 
                int(self.defense * factor), 
                self.level
            )
            return new_char
        else:
            raise TypeError("Можно умножать только на число")

    def __str__(self):
        """Строковое представление персонажа"""
        status = "жив" if self.is_alive else "мертв"
        return f"{self.name} (Lvl.{self.level}, {status}): HP {self.health}/{self.max_health}, ATK {self.attack}, DEF {self.defense}"

    def __repr__(self):
        """Подробное строковое представление для отладки"""
        return f"GameCharacter(name='{self.name}', health={self.health}, attack={self.attack}, defense={self.defense}, level={self.level})"

class Player:
    """
    Класс игрока для сравнения и сортировки
    """
    def __init__(self, name, level=1, experience=0, guild="None"):
        self.name = name
        self.level = level
        self.experience = experience
        self.guild = guild

    def __eq__(self, other):
        """Проверка равенства игроков по имени и уровню"""
        if isinstance(other, Player):
            return self.name == other.name and self.level == other.level
        return False

    def __lt__(self, other):
        """Сравнение по уровню, затем по опыту"""
        if isinstance(other, Player):
            if self.level != other.level:
                return self.level < other.level
            return self.experience < other.experience
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Player):
            return self < other or self == other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Player):
            if self.level != other.level:
                return self.level > other.level
            return self.experience > other.experience
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Player):
            return self > other or self == other
        return NotImplemented

    def __hash__(self):
        """Хеширование для использования в множествах и словарях"""
        return hash((self.name, self.level, self.experience))

    def __str__(self):
        return f"{self.name} (Lvl.{self.level}, EXP:{self.experience}, Guild:{self.guild})"

class Inventory:
    """
    Класс инвентаря игрока
    """
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size

    def __getitem__(self, index):
        """Получение предмета по индексу"""
        if 0 <= index < len(self.items):
            return self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __setitem__(self, index, item):
        """Установка предмета по индексу"""
        if 0 <= index < self.max_size:
            if index < len(self.items):
                self.items[index] = item
            else:
                # Если индекс за пределами текущего списка, расширяем его
                self.items.extend([None] * (index - len(self.items)))
                self.items.append(item)
        else:
            raise IndexError("Индекс вне допустимого размера инвентаря")

    def __delitem__(self, index):
        """Удаление предмета по индексу"""
        if 0 <= index < len(self.items):
            del self.items[index]
        else:
            raise IndexError("Индекс вне диапазона инвентаря")

    def __len__(self):
        """Количество предметов в инвентаре"""
        return len(self.items)

    def __contains__(self, item):
        """Проверка наличия предмета в инвентаре"""
        return item in self.items

    def __iter__(self):
        """Итерация по инвентарю"""
        return iter(self.items)

    def __bool__(self):
        """Проверка, пуст ли инвентарь"""
        return bool(self.items)

    def add_item(self, item):
        """Добавление предмета в инвентарь"""
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        else:
            print("Инвентарь полон!")
            return False

    def __str__(self):
        """Строковое представление инвентаря"""
        if not self.items:
            return "Инвентарь пуст"
        return f"Инвентарь ({len(self.items)}/{self.max_size}): {', '.join(map(str, self.items))}"

class Skill:
    """
    Класс навыка, который можно применить к цели
    """
    def __init__(self, name, power, skill_type="combat"):
        self.name = name
        self.power = power
        self.skill_type = skill_type  # combat, support, magic, etc.
        self.cooldown = 0
        self.max_cooldown = 3  # максимальный кулдаун

    def __call__(self, target, user=None):
        """Применение навыка к цели"""
        if self.cooldown > 0:
            print(f"Навык {self.name} на кулдауне. Осталось {self.cooldown} ходов.")
            return False

        if hasattr(target, 'health') and hasattr(target, 'is_alive') and target.is_alive:
            if self.skill_type == "combat":
                damage = self.power
                if user and hasattr(user, 'attack'):
                    damage += user.attack * 0.5  # Учитываем атаку пользователя
                target.health -= damage
                print(f"{user.name if user else 'Неизвестный'} использует {self.name} и наносит {damage} урона {target.name}")
                if target.health <= 0:
                    target.health = 0
                    target.is_alive = False
                    print(f"{target.name} погибает!")
            elif self.skill_type == "support":
                if hasattr(target, 'max_health'):
                    heal = min(self.power, target.max_health - target.health)
                    target.health += heal
                    print(f"{user.name if user else 'Неизвестный'} использует {self.name} и восстанавливает {heal} здоровья {target.name}")
            elif self.skill_type == "magic":
                # Магические эффекты могут иметь особую логику
                print(f"{user.name if user else 'Неизвестный'} использует магический навык {self.name} на {target.name}")

            # Устанавливаем кулдаун
            self.cooldown = self.max_cooldown
            return True
        else:
            print(f"Навык {self.name} не может быть применен к {target.name}, цель недоступна")
            return False

    def reduce_cooldown(self):
        """Уменьшение кулдауна"""
        if self.cooldown > 0:
            self.cooldown -= 1

    def __repr__(self):
        return f"Skill(name='{self.name}', power={self.power}, type='{self.skill_type}', cooldown={self.cooldown})"

    def __str__(self):
        status = f" (кулдаун: {self.cooldown})" if self.cooldown > 0 else ""
        return f"{self.name}{status} [{self.skill_type}] - сила {self.power}"

class GameSession:
    """
    Класс игровой сессии как контекстный менеджер
    """
    def __init__(self, player_name, game_map="Tutorial"):
        self.player_name = player_name
        self.game_map = game_map
        self.session_active = False
        self.turn_count = 0
        self.events = []

    def __enter__(self):
        """Начало игровой сессии"""
        print(f"=== Начало игровой сессии для {self.player_name} ===")
        print(f"Карта: {self.game_map}")
        self.session_active = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Завершение игровой сессии"""
        self.session_active = False
        print(f"=== Завершение игровой сессии для {self.player_name} ===")
        print(f"Всего ходов: {self.turn_count}")
        print(f"Событий зарегистрировано: {len(self.events)}")
        if exc_type:
            print(f"Сессия завершена с ошибкой: {exc_type.__name__}: {exc_value}")
        else:
            print("Сессия завершена успешно.")
        return False # Не подавлять исключения, если они были

class Item:
    """Простой класс предмета для демонстрации"""
    def __init__(self, name, item_type="usual"):
        self.name = name
        self.item_type = item_type

    def __str__(self):
        return f"{self.name}({self.item_type})"

    def __repr__(self):
        return f"Item('{self.name}', '{self.item_type}')"

# Создаем персонажей для демонстрации
warrior = GameCharacter("Конан", 100, 20, 10, 5)
mage = GameCharacter("Мерлин", 70, 15, 5, 4)

print("Исходные персонажи:")
print(warrior)
print(mage)

# Сложение персонажей
combined = warrior + mage
print(f"\nСложенные характеристики: {combined}")

# Умножение характеристик (усиление)
boosted_warrior = warrior * 1.5
print(f"Усиленный воин: {boosted_warrior}")

# Вычитание (урон)
damage = warrior - mage
print(f"Урон от воина по магу: {damage}")

# Демонстрация repr
print(f"\nПодробное представление воина: {repr(warrior)}")

# Создаем игроков
players = [
    Player("Артур", 10, 15000, "Рыцари Света"),
    Player("Ланселот", 12, 23000, "Рыцари Света"),
    Player("Мерлин", 8, 18000, "Хранители Тайн"),
    Player("Робин", 10, 12000, "Лесные Бродяги")
]

print("\nИсходный список игроков:")
for p in players:
    print(f"  {p}")

# Сортировка игроков
sorted_players = sorted(players)
print("\nОтсортированные игроки по уровню/опыту:")
for p in sorted_players:
    print(f"  {p}")

# Использование в множестве (благодаря __hash__)
player_set = set(players)
print(f"\nКоличество уникальных игроков в множестве: {len(player_set)}")

# Сравнение
print(f"\nАртур < Ланселот: {players[0] < players[1]}")
print(f"Артур == Робин (одинаковый уровень): {players[0] == players[3]}")

# Создаем инвентарь
inventory = Inventory(5)

# Добавляем предметы
items = [Item("Меч"), Item("Щит"), Item("Зелье"), Item("Шлем")]
for item in items:
    inventory.add_item(item)

print(f"\nИнвентарь: {inventory}")

# Доступ к элементам через индекс (__getitem__)
print(f"Первый предмет: {inventory[0]}")
print(f"Третий предмет: {inventory[2]}")

# Изменение элемента (__setitem__)
inventory[1] = Item("Броня")
print(f"После замены второго предмета: {inventory}")

# Проверка на вхождение (__contains__)
print(f"Меч в инвентаре: {items[0] in inventory}")

# Длина (__len__)
print(f"Количество предметов: {len(inventory)}")

# Итерация (__iter__)
print("Все предметы в инвентаре:")
for item in inventory:
    print(f"  {item}")

# Проверка, пуст ли инвентарь (__bool__)
print(f"Инвентарь пуст? {not inventory}")

# Удаление (__delitem__)
del inventory[2]  # Удаляем зелье
print(f"После удаления зелья: {inventory}")

# Создаем персонажей для демонстрации
target = GameCharacter("Гоблин", 50, 5, 2)

# Создаем навыки
slash = Skill("Рубящий удар", 15, "combat")
heal = Skill("Лечебное прикосновение", 20, "support")
fireball = Skill("Огненный шар", 25, "magic")

print(f"\nЦель до применения навыков: {target}")

# Применяем навыки (__call__)
slash(target, GameCharacter("Игрок", 100, 10, 5))
print(f"После рубящего удара: {target}")

heal(target, None)  # Лечение без пользователя
print(f"После лечения: {target}")

# Показываем строковые представления
print(f"\nНавыки:")
print(f"  {slash}")
print(f"  {heal}")
print(f"  {repr(fireball)}")

# Демонстрируем кулдауны
print(f"\nПробуем использовать рубящий удар снова:")
slash(target, GameCharacter("Игрок", 100, 10, 5))
print(f"Цель: {target}")

# Уменьшаем кулдаун и пробуем снова
slash.reduce_cooldown()
print(f"После уменьшения кулдауна:")
slash(target, GameCharacter("Игрок", 100, 10, 5))

# Использование контекстного менеджера для нормальной сессии
print("\n=== Демонстрация нормальной сессии ===")
with GameSession("Артур", "Лес Чудес") as session:
    session.turn_count = 5
    session.events = ["Найден меч", "Побежден гоблин", "Открыт сундук", "Получен опыт", "Уровень повышен"]

print()

# Использование контекстного менеджера с исключением
print("=== Демонстрация сессии с исключением ===")
try:
    with GameSession("Ланселот", "Подземелье Теней") as session:
        session.turn_count = 3
        session.events = ["Встречен дракон", "Получен урон", "Использовано зелье"]
        raise ValueError("Игрок покинул игру")
except ValueError as e:
    print(f"Перехвачено исключение: {e}")