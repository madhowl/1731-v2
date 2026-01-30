# Решения для практического задания 3: Работа с итераторами и генераторами в игровом контексте

# Ниже приведены полные реализации игровых итераторов и генераторов согласно заданию


class SpellBookIterator:
    """
    Итератор для перебора заклинаний в книге заклинаний
    """
    def __init__(self, spells):
        self.spells = spells
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.spells):
            raise StopIteration
        spell = self.spells[self.index]
        self.index += 1
        return spell


def level_generator(start_level=1, max_level=100):
    """
    Генератор для последовательности номеров уровней
    
    Args:
        start_level (int): Начальный уровень
        max_level (int): Максимальный уровень
    """
    current_level = start_level
    while current_level <= max_level:
        yield current_level
        current_level += 1


class SkillTreeIterator:
    """
    Итератор для обхода дерева скиллов (в глубину)
    """
    def __init__(self, skill_tree):
        self.skill_tree = skill_tree
        self.stack = [skill_tree]
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        
        current = self.stack.pop()
        
        # Проверяем, не посещали ли мы этот узел
        if id(current) in self.visited:
            return self.__next__()
        
        self.visited.add(id(current))
        
        # Добавляем детей в стек в обратном порядке, чтобы сохранить порядок
        if 'children' in current and current['children']:
            for child in reversed(current['children']):
                self.stack.append(child)
        
        return current['name']


import random

def loot_generator(loot_pool, drop_rate=0.5):
    """
    Генератор для случайной генерации лута
    
    Args:
        loot_pool (list): Список возможных предметов для лута
        drop_rate (float): Вероятность выпадения предмета (от 0 до 1)
    """
    while True:
        if random.random() < drop_rate:
            yield random.choice(loot_pool)


class BidirectionalIterator:
    """
    Двунаправленный итератор с возможностью перемещения вперед и назад
    """
    def __init__(self, items):
        self.items = items
        self.current_index = -1  # Начинаем перед первым элементом

    def __iter__(self):
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index >= len(self.items):
            raise StopIteration
        return self.items[self.current_index]

    def prev(self):
        self.current_index -= 1
        if self.current_index < 0:
            raise StopIteration
        return self.items[self.current_index]

    def has_next(self):
        return self.current_index + 1 < len(self.items)

    def has_prev(self):
        return self.current_index > 0


def battle_generator(player, enemies):
    """
    Генератор для пошаговой битвы
    
    Args:
        player (object): Объект игрока с атрибутами health, attack и т.д.
        enemies (list): Список вражеских персонажей
    """
    round_number = 1
    
    while player.health > 0 and any(enemy.health > 0 for enemy in enemies):
        yield f"Раунд {round_number}:"
        
        # Ход игрока
        if player.health > 0:
            active_enemy = next((enemy for enemy in enemies if enemy.health > 0), None)
            if active_enemy:
                damage = player.attack
                active_enemy.health -= damage
                yield f"Игрок атакует {active_enemy.name} на {damage} урона"
                if active_enemy.health <= 0:
                    yield f"{active_enemy.name} побежден!"
        
        # Ход врагов
        for enemy in enemies:
            if enemy.health > 0 and player.health > 0:
                damage = enemy.attack
                player.health -= damage
                yield f"{enemy.name} атакует игрока на {damage} урона"
        
        round_number += 1
    
    if player.health > 0:
        yield "Игрок победил!"
    else:
        yield "Игрок потерпел поражение!"


def player_turn_generator(actions):
    """
    Генератор для последовательности действий игрока
    
    Args:
        actions (list): Список возможных действий
    """
    while True:
        for action in actions:
            yield action


class DungeonRoomIterator:
    """
    Итератор для обхода комнат в подземелье
    """
    def __init__(self, dungeon_rooms):
        self.dungeon_rooms = dungeon_rooms
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.dungeon_rooms):
            raise StopIteration
        room = self.dungeon_rooms[self.index]
        self.index += 1
        return room


def world_generator(width, height, cell_types=["grass", "water", "forest", "mountain"]):
    """
    Генератор для процедурной генерации игрового мира
    
    Args:
        width (int): Ширина мира
        height (int): Высота мира
        cell_types (list): Типы клеток для генерации
    """
    for y in range(height):
        row = []
        for x in range(width):
            row.append(random.choice(cell_types))
        yield row


class TypedInventoryIterator:
    """
    Итератор для перебора предметов в инвентаре по типу
    """
    def __init__(self, inventory, item_type):
        self.inventory = inventory
        self.item_type = item_type
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.inventory):
            item = self.inventory[self.index]
            self.index += 1
            if item.type == self.item_type:
                return item
        raise StopIteration


def quest_chain_generator(available_quests, max_chain_length=5):
    """
    Генератор для создания цепочек квестов
    
    Args:
        available_quests (list): Список доступных квестов
        max_chain_length (int): Максимальная длина цепочки
    """
    import random
    while True:
        chain_length = random.randint(1, max_chain_length)
        selected_quests = random.sample(available_quests, min(chain_length, len(available_quests)))
        yield selected_quests


class FilteredTransformIterator:
    """
    Итератор с фильтрацией и преобразованием данных
    """
    def __init__(self, items, filter_func=None, transform_func=None):
        self.items = items
        self.filter_func = filter_func
        self.transform_func = transform_func
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            
            # Применяем фильтр, если он задан
            if self.filter_func is None or self.filter_func(item):
                # Применяем преобразование, если оно задано
                if self.transform_func is not None:
                    item = self.transform_func(item)
                return item
        
        raise StopIteration


# Примеры классов для тестирования

class Player:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def __str__(self):
        return f"Player(name='{self.name}', health={self.health}, attack={self.attack})"


class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def __str__(self):
        return f"Enemy(name='{self.name}', health={self.health}, attack={self.attack})"


class Item:
    def __init__(self, name, item_type):
        self.name = name
        self.type = item_type

    def __str__(self):
        return f"Item(name='{self.name}', type='{self.type}')"


class Quest:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Quest(name='{self.name}', description='{self.description}')"


# Примеры использования итераторов и генераторов
if __name__ == "__main__":
    print("=== Примеры использования игровых итераторов и генераторов ===\n")
    
    # Пример использования SpellBookIterator
    print("--- Итератор SpellBookIterator ---")
    spells = ["Огненный шар", "Ледяная стрела", "Целительное прикосновение", "Молния"]
    spell_iterator = SpellBookIterator(spells)
    for spell in spell_iterator:
        print(f"Заклинание: {spell}")
    print()
    
    # Пример использования level_generator
    print("--- Генератор level_generator ---")
    levels = level_generator(1, 5)
    for level in levels:
        print(f"Уровень: {level}")
        if level >= 5:  # Ограничиваем вывод
            break
    print()
    
    # Пример использования SkillTreeIterator
    print("--- Итератор SkillTreeIterator ---")
    skill_tree = {
        "name": "Воин",
        "children": [
            {"name": "Мечник", "children": [{"name": "Мастер меча", "children": []}]},
            {"name": "Щитоносец", "children": [{"name": "Танк", "children": []}]}
        ]
    }
    skill_iterator = SkillTreeIterator(skill_tree)
    for skill in skill_iterator:
        print(f"Скилл: {skill}")
    print()
    
    # Пример использования loot_generator
    print("--- Генератор loot_generator ---")
    common_loot = ["Зелье здоровья", "Зелье маны", "Монеты", "Меч"]
    loot_gen = loot_generator(common_loot, 0.7)
    count = 0
    for item in loot_gen:
        print(f"Выпал предмет: {item}")
        count += 1
        if count >= 5:  # Ограничиваем вывод
            break
    print()
    
    # Пример использования BidirectionalIterator
    print("--- Итератор BidirectionalIterator ---")
    locations = ["Город", "Лес", "Пещера", "Замок"]
    bi_iterator = BidirectionalIterator(locations)
    
    print(next(bi_iterator)) # Город
    print(next(bi_iterator))  # Лес
    print(bi_iterator.prev())  # Город
    print(f"Есть ли следующий элемент: {bi_iterator.has_next()}")
    print(f"Есть ли предыдущий элемент: {bi_iterator.has_prev()}")
    print()
    
    # Пример использования player_turn_generator
    print("--- Генератор player_turn_generator ---")
    actions = ["атаковать", "защититься", "использовать предмет", "побежать"]
    turn_gen = player_turn_generator(actions)
    for i, action in enumerate(turn_gen):
        print(f"Ход {i+1}: {action}")
        if i >= 7:  # Ограничим количество для тестирования
            break
    print()
    
    # Пример использования DungeonRoomIterator
    print("--- Итератор DungeonRoomIterator ---")
    rooms = ["Вход", "Зал с сокровищами", "Комната с ловушкой", "Финальная битва"]
    room_iterator = DungeonRoomIterator(rooms)
    for room in room_iterator:
        print(f"Комната: {room}")
    print()
    
    # Пример использования world_generator
    print("--- Генератор world_generator ---")
    world_gen = world_generator(3, 3)
    for i, row in enumerate(world_gen):
        print(f"Ряд {i}: {row}")
        if i >= 2:  # Ограничиваем вывод
            break
    print()
    
    # Пример использования TypedInventoryIterator
    print("--- Итератор TypedInventoryIterator ---")
    inventory = [
        Item("Меч", "weapon"),
        Item("Щит", "armor"),
        Item("Зелье", "consumable"),
        Item("Лук", "weapon")
    ]
    weapon_iterator = TypedInventoryIterator(inventory, "weapon")
    for item in weapon_iterator:
        print(f"Оружие: {item.name}")
    print()
    
    # Пример использования quest_chain_generator
    print("--- Генератор quest_chain_generator ---")
    quests = [Quest(f"Квест {i}", f"Описание квеста {i}") for i in range(1, 6)]
    quest_chain_gen = quest_chain_generator(quests)
    chains_generated = 0
    for chain in quest_chain_gen:
        print(f"Цепочка квестов: {[q.name for q in chain]}")
        chains_generated += 1
        if chains_generated >= 3:  # Ограничиваем вывод
            break
    print()
    
    # Пример использования FilteredTransformIterator
    print("--- Итератор FilteredTransformIterator ---")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Итератор, который возвращает квадраты четных чисел
    iterator = FilteredTransformIterator(
        numbers, 
        filter_func=lambda x: x % 2 == 0, 
        transform_func=lambda x: x ** 2
    )
    for item in iterator:
        print(item)  # 4, 16, 36, 64, 100
    print()
    
    # Пример использования battle_generator
    print("--- Генератор battle_generator ---")
    player = Player("Герой", 50, 15)
    enemies = [Enemy("Гоблин", 20, 5), Enemy("Орк", 30, 8)]
    battle_gen = battle_generator(player, enemies)
    rounds_simulated = 0
    for event in battle_gen:
        print(event)
        rounds_simulated += 1
        if "победил" in event or "потерпел поражение" in event or rounds_simulated > 10:
            break
    print()
    
    print("Все игровые итераторы и генераторы успешно реализованы и готовы к использованию!")