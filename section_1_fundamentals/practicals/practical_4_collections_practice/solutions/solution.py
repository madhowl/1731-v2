# Решения для практического задания 4: Использование модуля collections в игровом контексте

# Ниже приведены полные реализации игровых структур данных согласно заданию


from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import datetime


# Задание 1.1: Создание namedtuple для различных игровых сущностей
Monster = namedtuple('Monster', ['name', 'level', 'health', 'attack_power', 'monster_type'])
Spell = namedtuple('Spell', ['name', 'mana_cost', 'damage', 'spell_type'])
Location = namedtuple('Location', ['name', 'description', 'danger_level', 'required_level'])

# Пример использования
goblin = Monster("Гоблин", 1, 20, 5, "common")
fireball = Spell("Огненный шар", 10, 15, "fire")
forest = Location("Темный лес", "Густой лес, полный опасностей", 3, 5)


# Задание 1.2: Использование deque для очереди игровых действий
def create_action_queue(max_actions=10):
    """
    Создает очередь для хранения последних действий игрока
    
    Args:
        max_actions (int): Максимальное количество действий в очереди
    
    Returns:
        deque: Очередь действий
    """
    return deque(maxlen=max_actions)

def add_action(action_queue, action):
    """
    Добавляет действие в очередь
    
    Args:
        action_queue (deque): Очередь действий
        action (str): Действие для добавления
    """
    action_queue.append(action)

def get_last_actions(action_queue, count=5):
    """
    Возвращает последние совершенные действия
    
    Args:
        action_queue (deque): Очередь действий
        count (int): Количество действий для возврата
    
    Returns:
        list: Список последних действий
    """
    return list(action_queue)[-count:]

# Пример использования
actions = create_action_queue(5)
add_action(actions, "атаковал гоблина")
add_action(actions, "использовал зелье")
recent_actions = get_last_actions(actions)


# Задание 2.1: Использование Counter для анализа игровой статистики
class GameStatistics:
    """
    Класс для анализа игровой статистики
    """
    def __init__(self):
        self.spell_usage = Counter()  # Счетчик использования заклинаний
        self.item_usage = Counter()  # Счетчик использования предметов
        self.monster_encounters = Counter()  # Счетчик встреч с монстрами
    
    def record_spell_cast(self, spell_name):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
        """
        self.spell_usage[spell_name] += 1
    
    def record_item_use(self, item_name):
        """
        Записывает использование предмета
        
        Args:
            item_name (str): Название предмета
        """
        self.item_usage[item_name] += 1
    
    def record_monster_encounter(self, monster_name):
        """
        Записывает встречу с монстром
        
        Args:
            monster_name (str): Название монстра
        """
        self.monster_encounters[monster_name] += 1
    
    def get_top_spells(self, n=5):
        """
        Возвращает топ-N самых используемых заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N заклинаний
        """
        return self.spell_usage.most_common(n)
    
    def get_most_used_items(self, n=5):
        """
        Возвращает топ-N самых используемых предметов
        
        Args:
            n (int): Количество предметов для возврата
        
        Returns:
            list: Список топ-N предметов
        """
        return self.item_usage.most_common(n)

# Пример использования
stats = GameStatistics()
stats.record_spell_cast("Огненный шар")
stats.record_spell_cast("Огненный шар")
stats.record_spell_cast("Лечение")
top_spells = stats.get_top_spells(3)


# Задание 2.2: Использование defaultdict для группировки игровых данных
class GameDataOrganizer:
    """
    Класс для организации игровых данных
    """
    def __init__(self):
        # Группировка предметов по типам
        self.items_by_type = defaultdict(list)
        # Группировка монстров по уровням
        self.monsters_by_level = defaultdict(list)
        # Группировка заклинаний по школам
        self.spells_by_school = defaultdict(list)
    
    def add_item(self, item_name, item_type):
        """
        Добавляет предмет в группировку по типу
        
        Args:
            item_name (str): Название предмета
            item_type (str): Тип предмета
        """
        self.items_by_type[item_type].append(item_name)
    
    def add_monster(self, monster_name, level):
        """
        Добавляет монстра в группировку по уровню
        
        Args:
            monster_name (str): Название монстра
            level (int): Уровень монстра
        """
        self.monsters_by_level[level].append(monster_name)
    
    def add_spell(self, spell_name, school):
        """
        Добавляет заклинание в группировку по школе
        
        Args:
            spell_name (str): Название заклинания
            school (str): Школа магии
        """
        self.spells_by_school[school].append(spell_name)
    
    def get_items_of_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        return self.items_by_type[item_type]
    
    def get_monsters_of_level(self, level):
        """
        Возвращает всех монстров заданного уровня
        
        Args:
            level (int): Уровень монстров для поиска
        
        Returns:
            list: Список монстров заданного уровня
        """
        return self.monsters_by_level[level]

# Пример использования
organizer = GameDataOrganizer()
organizer.add_item("Меч", "weapon")
organizer.add_item("Щит", "armor")
weapons = organizer.get_items_of_type("weapon")


# Задание 3.1: Использование OrderedDict для системы достижений
class AchievementSystem:
    """
    Система достижений с сохранением порядка получения
    """
    def __init__(self):
        self.achievements = OrderedDict()  # Словарь достижений с порядком получения
        self.next_id = 1  # Следующий ID для достижения
    
    def add_achievement(self, name, description, points=10):
        """
        Добавляет новое достижение (если его еще нет)
        
        Args:
            name (str): Название достижения
            description (str): Описание достижения
            points (int): Количество очков за достижение
        """
        if name not in self.achievements:
            achievement_id = self.next_id
            self.next_id += 1
            self.achievements[name] = {
                'id': achievement_id,
                'name': name,
                'description': description,
                'points': points,
                'unlocked': False,
                'timestamp': None
            }
    
    def unlock_achievement(self, name, timestamp=None):
        """
        Разблокирует достижение
        
        Args:
            name (str): Название достижения для разблокировки
            timestamp (datetime): Время разблокировки (опционально)
        """
        if name in self.achievements and not self.achievements[name]['unlocked']:
            self.achievements[name]['unlocked'] = True
            self.achievements[name]['timestamp'] = timestamp or datetime.datetime.now()
    
    def get_unlocked_achievements(self):
        """
        Возвращает список разблокированных достижений в порядке получения
        
        Returns:
            list: Список разблокированных достижений
        """
        return [ach for ach in self.achievements.values() if ach['unlocked']]
    
    def get_achievement_progress(self):
        """
        Возвращает прогресс по достижениям (сколько получено, сколько всего)
        
        Returns:
            tuple: (количество разблокированных, общее количество)
        """
        unlocked_count = sum(1 for ach in self.achievements.values() if ach['unlocked'])
        total_count = len(self.achievements)
        return (unlocked_count, total_count)

# Пример использования
achievements = AchievementSystem()
achievements.add_achievement("Первый шаг", "Сделайте первый шаг в мир игры", 5)
achievements.unlock_achievement("Первый шаг")
unlocked = achievements.get_unlocked_achievements()


# Задание 3.2: Комплексное использование структур данных
# Определите namedtuple для предмета инвентаря
InventoryItem = namedtuple('InventoryItem', ['name', 'item_type', 'quantity', 'added_date'])

class AdvancedInventory:
    """
    Улучшенная система инвентаря с использованием различных структур данных
    """
    def __init__(self, max_size=20):
        self.max_size = max_size
        # Используем OrderedDict для хранения предметов сохранением порядка добавления
        self.items = OrderedDict()
        # Используем Counter для подсчета общего количества каждого типа предметов
        self.item_type_counts = Counter()
        # Используем defaultdict для группировки предметов по типам
        self.items_by_type = defaultdict(list)
        # Используем deque для хранения истории действий с инвентарем
        self.action_history = deque(maxlen=10)
    
    def add_item(self, name, item_type, quantity=1):
        """
        Добавляет предмет в инвентарь
        
        Args:
            name (str): Название предмета
            item_type (str): Тип предмета
            quantity (int): Количество предметов
        """
        if name in self.items:
            # Предмет уже есть в инвентаре, увеличиваем количество
            current_item = self.items[name]
            new_quantity = current_item.quantity + quantity
            self.items[name] = InventoryItem(name, item_type, new_quantity, current_item.added_date)
        else:
            # Новый предмет
            if len(self.items) >= self.max_size:
                # Удаляем самый старый предмет, если инвентарь полон
                oldest_key = next(iter(self.items))
                del self.items[oldest_key]
            
            new_item = InventoryItem(name, item_type, quantity, datetime.datetime.now())
            self.items[name] = new_item
        
        # Обновляем счетчики
        self.item_type_counts[item_type] += quantity
        if name not in self.items_by_type[item_type]:
            self.items_by_type[item_type].append(name)
        
        # Добавляем действие в историю
        self.action_history.append(f"Добавлено {quantity}x {name}")
    
    def remove_item(self, name, quantity=1):
        """
        Удаляет предмет из инвентаря
        
        Args:
            name (str): Название предмета
            quantity (int): Количество предметов для удаления
        """
        if name not in self.items:
            return False
        
        current_item = self.items[name]
        new_quantity = current_item.quantity - quantity
        
        if new_quantity <= 0:
            # Удаляем предмет полностью
            item_type = current_item.item_type
            del self.items[name]
            self.item_type_counts[item_type] -= current_item.quantity
            if self.item_type_counts[item_type] <= 0:
                del self.item_type_counts[item_type]
            if name in self.items_by_type[item_type]:
                self.items_by_type[item_type].remove(name)
        else:
            # Обновляем количество
            self.items[name] = InventoryItem(name, current_item.item_type, new_quantity, current_item.added_date)
            self.item_type_counts[current_item.item_type] -= quantity
        
        # Добавляем действие в историю
        self.action_history.append(f"Удалено {quantity}x {name}")
        return True
    
    def get_items_by_type(self, item_type):
        """
        Возвращает все предметы заданного типа
        
        Args:
            item_type (str): Тип предметов для поиска
        
        Returns:
            list: Список предметов заданного типа
        """
        result = []
        for item_name in self.items_by_type[item_type]:
            if item_name in self.items:
                result.append(self.items[item_name])
        return result
    
    def get_most_common_types(self, n=3):
        """
        Возвращает n самых распространенных типов предметов
        
        Args:
            n (int): Количество типов для возврата
        
        Returns:
            list: Список самых распространенных типов
        """
        return [item_type for item_type, count in self.item_type_counts.most_common(n)]
    
    def get_inventory_size(self):
        """
        Возвращает текущий размер инвентаря
        
        Returns:
            int: Количество уникальных предметов в инвентаре
        """
        return len(self.items)

# Пример использования
inventory = AdvancedInventory()
inventory.add_item("Зелье здоровья", "consumable", 5)
inventory.add_item("Меч", "weapon", 1)
consumables = inventory.get_items_by_type("consumable")


# Задание 1.3: Использование Counter для анализа битв
def create_battle_analyzer():
    """
    Создает анализатор битв
    
    Returns:
        Counter: Счетчик побед над монстрами
    """
    return Counter()

def record_victory(analyzer, monster_type):
    """
    Записывает победу над монстром
    
    Args:
        analyzer (Counter): Анализатор битв
        monster_type (str): Тип побежденного монстра
    """
    analyzer[monster_type] += 1

def get_victory_statistics(analyzer):
    """
    Возвращает статистику побед
    
    Args:
        analyzer (Counter): Анализатор битв
    
    Returns:
        dict: Статистика побед
    """
    total_victories = sum(analyzer.values())
    return {
        'total_victories': total_victories,
        'victories_by_type': dict(analyzer),
        'most_defeated': analyzer.most_common(1)[0] if analyzer else None
    }

# Пример использования
battle_stats = create_battle_analyzer()
record_victory(battle_stats, "гоблин")
record_victory(battle_stats, "орк")
record_victory(battle_stats, "гоблин")
stats = get_victory_statistics(battle_stats)


# Задание 1.4: Использование deque для системы чата
def create_chat_system(max_messages=50):
    """
    Создает систему чата
    
    Args:
        max_messages (int): Максимальное количество сообщений в истории
    
    Returns:
        deque: Очередь сообщений чата
    """
    return deque(maxlen=max_messages)

def send_message(chat, player_name, message):
    """
    Отправляет сообщение в чат
    
    Args:
        chat (deque): Система чата
        player_name (str): Имя игрока
        message (str): Сообщение
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    chat.append(f"[{timestamp}] {player_name}: {message}")

def get_recent_messages(chat, count=10):
    """
    Возвращает последние сообщения
    
    Args:
        chat (deque): Система чата
        count (int): Количество сообщений для возврата
    
    Returns:
        list: Список последних сообщений
    """
    return list(chat)[-count:]

# Пример использования
chat = create_chat_system(20)
send_message(chat, "Игрок1", "Привет всем!")
send_message(chat, "Игрок2", "Привет!")
recent_msgs = get_recent_messages(chat, 5)


# Задание 2.3: Использование defaultdict для системы крафта
class CraftingSystem:
    """
    Система крафта с группировкой рецептов
    """
    def __init__(self):
        # Группировка рецептов по категориям
        self.recipes_by_category = defaultdict(list)
        # Хранение всех рецептов
        self.all_recipes = {}
    
    def add_recipe(self, name, category, ingredients, result):
        """
        Добавляет рецепт в систему
        
        Args:
            name (str): Название рецепта
            category (str): Категория рецепта
            ingredients (dict): Ингредиенты {название: количество}
            result (str): Результат крафта
        """
        recipe = {
            'name': name,
            'category': category,
            'ingredients': ingredients,
            'result': result
        }
        self.recipes_by_category[category].append(recipe)
        self.all_recipes[name] = recipe
    
    def get_recipes_by_category(self, category):
        """
        Возвращает все рецепты в заданной категории
        
        Args:
            category (str): Категория рецептов
        
        Returns:
            list: Список рецептов в категории
        """
        return self.recipes_by_category[category]
    
    def can_craft(self, recipe_name, inventory):
        """
        Проверяет, можно ли создать предмет по рецепту
        
        Args:
            recipe_name (str): Название рецепта
            inventory (dict): Инвентарь игрока {предмет: количество}
        
        Returns:
            bool: Можно ли создать предмет
        """
        if recipe_name not in self.all_recipes:
            return False
        
        recipe = self.all_recipes[recipe_name]
        ingredients = recipe['ingredients']
        
        for ingredient, required_amount in ingredients.items():
            if inventory.get(ingredient, 0) < required_amount:
                return False
        
        return True

# Пример использования
crafting = CraftingSystem()
crafting.add_recipe("Деревянный меч", "оружие", {"дерево": 3}, "меч")
weapons = crafting.get_recipes_by_category("оружие")


# Задание 2.4: Использование Counter для анализа эффективности заклинаний
class SpellEffectivenessAnalyzer:
    """
    Анализатор эффективности заклинаний
    """
    def __init__(self):
        # Счетчик успешных использований заклинаний
        self.successful_casts = Counter()
        # Счетчик неудачных использований заклинаний
        self.failed_casts = Counter()
        # Общее количество использований
        self.total_casts = Counter()
    
    def record_cast(self, spell_name, success=True):
        """
        Записывает использование заклинания
        
        Args:
            spell_name (str): Название заклинания
            success (bool): Успешно ли было использование
        """
        self.total_casts[spell_name] += 1
        if success:
            self.successful_casts[spell_name] += 1
        else:
            self.failed_casts[spell_name] += 1
    
    def get_effectiveness(self, spell_name):
        """
        Возвращает эффективность заклинания (в процентах)
        
        Args:
            spell_name (str): Название заклинания
        
        Returns:
            float: Эффективность в процентах
        """
        total = self.total_casts[spell_name]
        if total == 0:
            return 0.0
        successful = self.successful_casts[spell_name]
        return (successful / total) * 100
    
    def get_top_effective_spells(self, n=5):
        """
        Возвращает топ-N самых эффективных заклинаний
        
        Args:
            n (int): Количество заклинаний для возврата
        
        Returns:
            list: Список топ-N эффективных заклинаний
        """
        effectiveness_list = []
        for spell in self.total_casts:
            eff = self.get_effectiveness(spell)
            uses = self.total_casts[spell]
            # Учитываем только заклинания, которые использовались хотя бы 3 раза
            if uses >= 3:
                effectiveness_list.append((spell, eff, uses))
        
        # Сортируем по эффективности (в убывающем порядке)
        effectiveness_list.sort(key=lambda x: x[1], reverse=True)
        return effectiveness_list[:n]

# Пример использования
analyzer = SpellEffectivenessAnalyzer()
analyzer.record_cast("Огненный шар", True)
analyzer.record_cast("Огненный шар", False)
effectiveness = analyzer.get_effectiveness("Огненный шар")


# Задание 3.3: Система рангов игроков с использованием OrderedDict
class RankingSystem:
    """
    Система рангов игроков с сохранением порядка
    """
    def __init__(self):
        # Хранит игроков в порядке их достижения ранга
        self.player_rankings = OrderedDict()
        self.next_rank = 1
    
    def add_player(self, player_name, score):
        """
        Добавляет игрока в систему рангов
        
        Args:
            player_name (str): Имя игрока
            score (int): Очки игрока
        """
        self.player_rankings[player_name] = score
        # Пересчитываем рейтинги
        self._recalculate_rankings()
    
    def update_score(self, player_name, new_score):
        """
        Обновляет счет игрока и пересчитывает рейтинги
        
        Args:
            player_name (str): Имя игрока
            new_score (int): Новый счет
        """
        if player_name in self.player_rankings:
            self.player_rankings[player_name] = new_score
            # Пересчитываем рейтинги
            self._recalculate_rankings()
    
    def _recalculate_rankings(self):
        """
        Пересчитывает рейтинги на основе очков
        """
        # Сортируем игроков по очкам в убывающем порядке
        sorted_players = sorted(self.player_rankings.items(), key=lambda x: x[1], reverse=True)
        # Обновляем OrderedDict с правильным порядком
        self.player_rankings = OrderedDict(sorted_players)
    
    def get_leaderboard(self, top_n=10):
        """
        Возвращает таблицу лидеров
        
        Args:
            top_n (int): Количество игроков для возврата
        
        Returns:
            list: Таблица лидеров
        """
        leaderboard = []
        rank = 1
        for player_name, score in self.player_rankings.items():
            if rank > top_n:
                break
            leaderboard.append((rank, player_name, score))
            rank += 1
        return leaderboard
    
    def get_player_rank(self, player_name):
        """
        Возвращает ранг игрока
        
        Args:
            player_name (str): Имя игрока
        
        Returns:
            int: Ранг игрока (1 - лучший)
        """
        if player_name not in self.player_rankings:
            return -1  # Игрок не найден
        
        rank = 1
        for name in self.player_rankings.keys():
            if name == player_name:
                return rank
            rank += 1
        return -1  # Игрок не найден

# Пример использования
ranking = RankingSystem()
ranking.add_player("Игрок1", 1500)
ranking.add_player("Игрок2", 2000)
leaderboard = ranking.get_leaderboard(5)


# Задание 3.4: Комплексная игровая статистика
# Определите namedtuple для игрового события
GameEvent = namedtuple('GameEvent', ['timestamp', 'event_type', 'player', 'details'])

class ComprehensiveGameStats:
    """
    Комплексная система игровой статистики
    """
    def __init__(self):
        # Хранение всех событий с сохранением порядка
        self.events = deque(maxlen=1000)
        # Счетчик типов событий
        self.event_counts = Counter()
        # Группировка событий по игрокам
        self.events_by_player = defaultdict(list)
        # Статистика по типам событий
        self.stats_by_event_type = defaultdict(Counter)
        # Хронология событий конкретного игрока
        self.player_timeline = OrderedDict()
    
    def log_event(self, event_type, player, details=""):
        """
        Логирует игровое событие
        
        Args:
            event_type (str): Тип события
            player (str): Имя игрока
            details (str): Детали события
        """
        event = GameEvent(datetime.datetime.now(), event_type, player, details)
        self.events.append(event)
        self.event_counts[event_type] += 1
        self.events_by_player[player].append(event)
        
        # Обновляем статистику по типам событий для игрока
        self.stats_by_event_type[event_type][player] += 1
        
        # Обновляем временную шкалу игрока
        if player not in self.player_timeline:
            self.player_timeline[player] = OrderedDict()
        self.player_timeline[player][event.timestamp] = event
    
    def get_player_stats(self, player):
        """
        Возвращает статистику по игроку
        
        Args:
            player (str): Имя игрока
        
        Returns:
            dict: Статистика игрока
        """
        if player not in self.events_by_player:
            return {}
        
        player_events = self.events_by_player[player]
        event_types = Counter([event.event_type for event in player_events])
        
        return {
            'total_events': len(player_events),
            'event_types': dict(event_types),
            'first_event': min(player_events, key=lambda x: x.timestamp).timestamp if player_events else None,
            'last_event': max(player_events, key=lambda x: x.timestamp).timestamp if player_events else None
        }
    
    def get_top_players_by_activity(self, n=5):
        """
        Возвращает топ-N самых активных игроков
        
        Args:
            n (int): Количество игроков для возврата
        
        Returns:
            list: Список самых активных игроков
        """
        player_activity = Counter({player: len(events) for player, events in self.events_by_player.items()})
        return player_activity.most_common(n)
    
    def get_recent_events(self, n=10):
        """
        Возвращает последние n событий
        
        Args:
            n (int): Количество событий для возврата
        
        Returns:
            list: Список последних событий
        """
        return list(self.events)[-n:]

# Пример использования
stats = ComprehensiveGameStats()
stats.log_event("battle_won", "Игрок1", "Победа над драконом")
stats.log_event("item_found", "Игрок1", "Меч легенд")
player_stats = stats.get_player_stats("Игрок1")


# Примеры использования всех структур данных
if __name__ == "__main__":
    print("=== Примеры использования структур данных из модуля collections ===\n")
    
    # Пример использования namedtuple
    print("--- NamedTuple ---")
    print(f"Монстр: {goblin.name}, уровень: {goblin.level}, здоровье: {goblin.health}")
    print(f"Заклинание: {fireball.name}, стоимость маны: {fireball.mana_cost}")
    print(f"Локация: {forest.name}, уровень опасности: {forest.danger_level}")
    print()
    
    # Пример использования deque
    print("--- Deque ---")
    print(f"Последние действия: {recent_actions}")
    print()
    
    # Пример использования Counter
    print("--- Counter ---")
    print(f"Топ заклинаний: {top_spells}")
    print(f"Статистика битв: {stats.get_most_used_items(3)}")
    print()
    
    # Пример использования defaultdict
    print("--- DefaultDict ---")
    print(f"Оружие в инвентаре: {weapons}")
    print()
    
    # Пример использования OrderedDict
    print("--- OrderedDict ---")
    print(f"Разблокированные достижения: {[a['name'] for a in unlocked]}")
    print(f"Прогресс достижений: {achievements.get_achievement_progress()}")
    print()
    
    # Пример использования всех структур в комплексном классе
    print("--- AdvancedInventory ---")
    print(f"Размер инвентаря: {inventory.get_inventory_size()}")
    print(f"Типы предметов: {inventory.get_most_common_types(3)}")
    print(f"Предметы типа 'consumable': {[(item.name, item.quantity) for item in consumables]}")
    print()
    
    # Пример статистики битв
    print("--- Battle Statistics ---")
    print(f"Статистика побед: {stats}")
    print()
    
    # Пример чата
    print("--- Chat System ---")
    print(f"Последние сообщения: {recent_msgs}")
    print()
    
    # Пример системы крафта
    print("--- Crafting System ---")
    print(f"Рецепты оружия: {[r['name'] for r in weapons]}")
    print()
    
    # Пример анализа эффективности заклинаний
    print("--- Spell Effectiveness ---")
    print(f"Эффективность 'Огненный шар': {effectiveness}%")
    print()
    
    # Пример системы рангов
    print("--- Ranking System ---")
    print(f"Таблица лидеров: {leaderboard}")
    print()
    
    # Пример комплексной статистики
    print("--- Comprehensive Game Stats ---")
    print(f"Статистика игрока: {player_stats}")
    print(f"Топ активных игроков: {stats.get_top_players_by_activity(3)}")
    print(f"Последние события: {stats.get_recent_events(5)}")
    print()
    
    print("Все структуры данных из модуля collections успешно реализованы и готовы к использованию!")