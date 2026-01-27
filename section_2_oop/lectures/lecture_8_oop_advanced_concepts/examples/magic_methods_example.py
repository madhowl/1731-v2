"""
Пример: Магические методы (dunder-методы) в контексте игровых объектов
"""

class Item:
    """Класс игрового предмета"""
    def __init__(self, name, value=0, weight=1.0, item_type="обычный"):
        self.name = name
        self.value = value  # Стоимость предмета
        self.weight = weight  # Вес предмета
        self.item_type = item_type  # Тип предмета
        self.durability = 100  # Прочность предмета

    def __repr__(self):
        """Строковое представление объекта для отладки"""
        return f"Item('{self.name}', {self.value}, {self.weight}, '{self.item_type}')"

    def __str__(self):
        """Строковое представление объекта для пользователя"""
        return f"{self.name} ({self.item_type}) - стоимость: {self.value}, вес: {self.weight}, прочность: {self.durability}"

    def __eq__(self, other):
        """Определение равенства двух предметов"""
        if not isinstance(other, Item):
            return NotImplemented
        return (self.name == other.name and 
                self.value == other.value and 
                self.weight == other.weight)

    def __lt__(self, other):
        """Определение операции 'меньше чем' для сортировки по стоимости"""
        if not isinstance(other, Item):
            return NotImplemented
        return self.value < other.value

    def __add__(self, other):
        """Сложение предметов (например, объединение стопок)"""
        if isinstance(other, Item) and self.name == other.name:
            # Объединяем стопки одинаковых предметов
            combined_weight = self.weight + other.weight
            combined_value = self.value + other.value
            return Item(f"{self.name} (стопка)", combined_value, combined_weight, self.item_type)
        return NotImplemented

    def __bool__(self):
        """Определение истинности объекта (предмет действителен, если его прочность > 0)"""
        return self.durability > 0

    def __hash__(self):
        """Определение хеша для использования в множествах и словарях"""
        return hash((self.name, self.value, self.weight))


class Inventory:
    """Класс инвентаря игрока"""
    def __init__(self, max_weight=100.0):
        self.items = []  # Список предметов
        self.max_weight = max_weight  # Максимальный вес, который можно нести

    def __len__(self):
        """Возвращает количество предметов в инвентаре"""
        return len(self.items)

    def __getitem__(self, index):
        """Позволяет получать доступ к предмету по индексу"""
        return self.items[index]

    def __setitem__(self, index, item):
        """Позволяет устанавливать предмет по индексу"""
        if self.get_total_weight() - self.items[index].weight + item.weight <= self.max_weight:
            self.items[index] = item
        else:
            raise ValueError("Превышен максимальный вес инвентаря")

    def __delitem__(self, index):
        """Позволяет удалять предмет по индексу"""
        del self.items[index]

    def __iter__(self):
        """Позволяет итерироваться по инвентарю"""
        return iter(self.items)

    def __contains__(self, item):
        """Проверяет, содержится ли предмет в инвентаре"""
        return item in self.items

    def __iadd__(self, item):
        """Реализация операции += для добавления предмета"""
        self.add_item(item)
        return self

    def __isub__(self, item):
        """Реализация операции -= для удаления предмета"""
        self.remove_item(item)
        return self

    def add_item(self, item):
        """Добавить предмет в инвентарь"""
        if self.get_total_weight() + item.weight <= self.max_weight:
            self.items.append(item)
            print(f"Предмет '{item.name}' добавлен в инвентарь")
        else:
            print(f"Невозможно добавить '{item.name}': превышен максимальный вес инвентаря")

    def remove_item(self, item):
        """Удалить предмет из инвентаря"""
        if item in self.items:
            self.items.remove(item)
            print(f"Предмет '{item.name}' удален из инвентаря")
        else:
            print(f"Предмет '{item.name}' не найден в инвентаре")

    def get_total_weight(self):
        """Получить общий вес всех предметов"""
        return sum(item.weight for item in self.items)

    def get_total_value(self):
        """Получить общую стоимость всех предметов"""
        return sum(item.value for item in self.items)

    def __str__(self):
        """Строковое представление инвентаря"""
        if not self.items:
            return "Инвентарь пуст"
        item_list = "\n  ".join(str(item) for item in self.items)
        return f"Инвентарь ({self.get_total_weight():.1f}/{self.max_weight} веса):\n  {item_list}"

    def __repr__(self):
        """Представление инвентаря для отладки"""
        return f"Inventory(items={self.items}, max_weight={self.max_weight})"


class TemporaryBuff:
    """Контекстный менеджер для временного усиления персонажа"""
    def __init__(self, character, attribute, boost_value, duration=10):
        self.character = character
        self.attribute = attribute
        self.boost_value = boost_value
        self.duration = duration
        self.original_value = getattr(character, attribute, 0)

    def __enter__(self):
        """Вызывается при входе в блок with"""
        # Увеличиваем характеристику на время действия баффа
        setattr(self.character, self.attribute, self.original_value + self.boost_value)
        print(f"{self.character.name} получает бафф: +{self.boost_value} к {self.attribute} на {self.duration} секунд")
        return self.character

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Вызывается при выходе из блока with"""
        # Восстанавливаем оригинальное значение характеристики
        setattr(self.character, self.attribute, self.original_value)
        print(f"{self.character.name} теряет бафф: восстановлено {self.attribute} = {self.original_value}")


class Character:
    """Класс игрового персонажа"""
    def __init__(self, name, strength=10, agility=10, intelligence=10):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def __str__(self):
        return f"{self.name}: Сила={self.strength}, Ловкость={self.agility}, Интеллект={self.intelligence}"


class SpellBook:
    """Класс книги заклинаний с дополнительными магическими методами"""
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.spells = {}  # Словарь заклинаний: имя -> уровень
        self.read_only = False  # Режим только для чтения

    def __call__(self, spell_name, target=None):
        """Позволяет 'вызывать' книгу заклинаний как функцию для применения заклинания"""
        if self.read_only:
            print(f"Книга заклинаний {self.owner_name} находится в режиме 'только для чтения'")
            return False

        if spell_name in self.spells:
            level = self.spells[spell_name]
            print(f"{self.owner_name} произносит заклинание '{spell_name}' (уровень {level})")
            if target:
                print(f"Цель: {target}")
            return True
        else:
            print(f"Заклинание '{spell_name}' не найдено в книге")
            return False

    def __getattr__(self, attr_name):
        """Вызывается при обращении к несуществующему атрибуту"""
        if attr_name.startswith("can_cast_"):
            spell_name = attr_name.replace("can_cast_", "")
            return spell_name in self.spells
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr_name}'")

    def __len__(self):
        """Возвращает количество заклинаний в книге"""
        return len(self.spells)

    def __getitem__(self, key):
        """Позволяет получать уровень заклинания по имени"""
        return self.spells[key]

    def __setitem__(self, key, value):
        """Позволяет устанавливать уровень заклинания по имени"""
        if self.read_only:
            raise AttributeError("Невозможно изменить заклинание в режиме 'только для чтения'")
        self.spells[key] = value

    def __delitem__(self, key):
        """Позволяет удалять заклинание по имени"""
        if self.read_only:
            raise AttributeError("Невозможно удалить заклинание в режиме 'только для чтения'")
        del self.spells[key]

    def __iter__(self):
        """Позволяет итерироваться по заклинаниям"""
        return iter(self.spells.items())

    def __contains__(self, item):
        """Проверяет, содержится ли заклинание в книге"""
        return item in self.spells

    def __str__(self):
        """Строковое представление книги заклинаний"""
        if not self.spells:
            return f"Книга заклинаний {self.owner_name} пуста"
        spells_list = ", ".join([f"{name}(уровень {level})" for name, level in self.spells.items()])
        return f"Книга заклинаний {self.owner_name}: {spells_list}"

    def add_spell(self, name, level):
        """Добавить заклинание в книгу"""
        self.spells[name] = level
        print(f"Заклинание '{name}' (уровень {level}) добавлено в книгу {self.owner_name}")


def demonstrate_basic_magic_methods():
    """Демонстрация основных магических методов"""
    print("=== Демонстрация магических методов для игровых предметов ===\n")

    # Создание предметов
    sword = Item("Меч героя", value=150, weight=5.0, item_type="оружие")
    shield = Item("Деревянный щит", value=50, weight=3.0, item_type="защита")
    potion = Item("Зелье здоровья", value=25, weight=0.5, item_type="расходуемый")
    another_sword = Item("Меч героя", value=150, weight=5.0, item_type="оружие")

    print("Предметы созданы:")
    print(sword)  # Использует __str__
    print(repr(shield))  # Использует __repr__
    print(f"Равны ли sword и another_sword? {sword == another_sword}")  # Использует __eq__
    print(f"Предмет sword истинен? {bool(sword)}")  # Использует __bool__

    # Создание инвентаря и добавление предметов
    inventory = Inventory(max_weight=20.0)

    # Использование операций += и =
    inventory += sword
    inventory += shield
    inventory += potion

    print(f"\n{inventory}")

    print(f"\nКоличество предметов в инвентаре: {len(inventory)}")  # Использует __len__

    print("\nИтерация по инвентарю:")
    for i, item in enumerate(inventory):  # Использует __iter__
        print(f"{i}: {item.name}")

    print(f"\nСодержится ли sword в инвентаре? {sword in inventory}")  # Использует __contains__

    # Доступ к предмету по индексу
    first_item = inventory[0]  # Использует __getitem__
    print(f"\nПервый предмет: {first_item}")

    # Объединение одинаковых предметов
    potion_stack = Item("Зелье здоровья", value=25, weight=0.5, item_type="расходуемый")
    combined_potions = potion + potion_stack  # Использует __add__
    print(f"\nОбъединенные зелья: {combined_potions}")

    # Сортировка предметов по стоимости (__lt__)
    items_list = [sword, shield, potion]
    sorted_items = sorted(items_list)  # Использует __lt__
    print(f"\nПредметы, отсортированные по стоимости: {[item.name for item in sorted_items]}")


def demonstrate_context_managers():
    """Демонстрация контекстных менеджеров"""
    print("\n\n=== Демонстрация контекстных менеджеров ===\n")

    hero = Character("Артур", strength=15, agility=12, intelligence=8)
    print(f"До баффа: {hero}")

    # Использование контекстного менеджера для временного усиления
    with TemporaryBuff(hero, 'strength', 5, 10) as buffed_hero:
        print(f"Во время баффа: {buffed_hero}")
        print("Герой совершает подвиг силы...")

    print(f"После баффа: {hero}")


def demonstrate_spellbook_magic_methods():
    """Демонстрация дополнительных магических методов в книге заклинаний"""
    print("\n\n=== Демонстрация дополнительных магических методов ===\n")

    # Создание книги заклинаний
    spellbook = SpellBook("Мерлина")
    spellbook.add_spell("Огненный шар", 3)
    spellbook.add_spell("Ледяная стрела", 2)
    spellbook.add_spell("Целительное прикосновение", 4)

    print(spellbook)
    print(f"Количество заклинаний: {len(spellbook)}")

    # Проверка наличия заклинания
    print(f"Содержится ли 'Огненный шар'? {'Огненный шар' in spellbook}")

    # Применение заклинания через __call__
    spellbook("Огненный шар", "дракон")

    # Использование методов, созданных через __getattr__
    print(f"Можно ли колдовать 'Огненный шар'? {spellbook.can_cast_огненный_шар}")

    # Итерация по заклинаниям
    print("\nВсе заклинания в книге:")
    for name, level in spellbook:
        print(f"  {name}: уровень {level}")


def main():
    """Основная функция для демонстрации всех примеров"""
    demonstrate_basic_magic_methods()
    demonstrate_context_managers()
    demonstrate_spellbook_magic_methods()


if __name__ == "__main__":
    main()