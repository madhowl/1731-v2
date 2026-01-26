# Примеры работы с коллекциями в Python

"""
Этот файл содержит примеры использования различных типов коллекций в Python:
списки, кортежи, словари, множества, а также специализированные коллекции из модуля collections.
"""

from collections import namedtuple, deque, Counter, OrderedDict, defaultdict, ChainMap
import array
import heapq
from typing import List, Dict, Set, Tuple

# 1. Списки (Lists)
def list_examples():
    """
    Примеры работы со списками
    """
    print("=== Списки (Lists) ===")
    
    # Создание списков
    numbers = [1, 2, 3, 4, 5]
    strings = ["яблоко", "банан", "апельсин"]
    mixed = [1, "текст", 3.14, True, [1, 2, 3]]
    
    print(f"Числовой список: {numbers}")
    print(f"Список строк: {strings}")
    print(f"Смешанный список: {mixed}")
    
    # Основные операции со списками
    # Добавление элементов
    numbers.append(6)
    print(f"После добавления 6: {numbers}")
    
    numbers.insert(2, 99)  # Вставляем 99 на позицию 2
    print(f"После вставки 99 на позицию 2: {numbers}")
    
    # Удаление элементов
    removed = numbers.pop()  # Удаляем последний элемент
    print(f"Удален последний элемент {removed}, список: {numbers}")
    
    numbers.remove(99)  # Удаляем первое вхождение 99
    print(f"После удаления 99: {numbers}")
    
    # Срезы
    print(f"Срез [1:4]: {numbers[1:4]}")
    print(f"Срез [:3]: {numbers[:3]}")
    print(f"Срез [3:]: {numbers[3:]}")
    print(f"Разворот списка: {numbers[::-1]}")
    
    # Сортировка
    unsorted = [5, 2, 8, 1, 9, 3]
    print(f"Неотсортированный: {unsorted}")
    print(f"Отсортированный (временно): {sorted(unsorted)}")
    unsorted.sort()  # Сортировка на месте
    print(f"Отсортированный (на месте): {unsorted}")
    
    # Списковые включения
    squares = [x**2 for x in range(1, 6)]
    print(f"Квадраты чисел 1-5: {squares}")
    
    evens = [x for x in range(1, 11) if x % 2 == 0]
    print(f"Четные числа 1-10: {evens}")
    print()

list_examples()

# 2. Кортежи (Tuples)
def tuple_examples():
    """
    Примеры работы с кортежами
    """
    print("=== Кортежи (Tuples) ===")
    
    # Создание кортежей
    coordinates = (10, 20)
    colors = ("красный", "зеленый", "синий")
    single_element = (42,)  # Обратите внимание на запятую
    empty_tuple = ()
    
    print(f"Координаты: {coordinates}")
    print(f"Цвета: {colors}")
    print(f"Одиночный элемент: {single_element}")
    print(f"Пустой кортеж: {empty_tuple}")
    
    # Распаковка кортежей
    x, y = coordinates
    print(f"Распаковка координат: x={x}, y={y}")
    
    red, green, blue = colors
    print(f"Распаковка цветов: red={red}, green={green}, blue={blue}")
    
    # Использование * для распаковки
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"Распаковка с *: first={first}, middle={middle}, last={last}")
    
    # namedtuples для структурированных данных
    Point = namedtuple('Point', ['x', 'y'])
    p1 = Point(10, 20)
    p2 = Point(x=15, y=25)
    
    print(f"Namedtuple Point: {p1}")
    print(f"Координаты точки p1: x={p1.x}, y={p1.y}")
    print(f"Namedtuple доступ по индексу: {p1[0]}, {p1[1]}")
    
    # Кортежи как ключи словаря
    locations = {
        (0, 0): "начало координат",
        (1, 1): "диагональ",
        (5, 7): "произвольная точка"
    }
    
    for coord, name in locations.items():
        print(f"Координаты {coord}: {name}")
    print()

tuple_examples()

# 3. Словари (Dictionaries)
def dictionary_examples():
    """
    Примеры работы со словарями
    """
    print("=== Словари (Dictionaries) ===")
    
    # Создание словарей
    person = {
        "имя": "Иван",
        "возраст": 30,
        "город": "Москва"
    }
    
    # Создание с помощью dict()
    contact = dict(имя="Мария", телефон="+7-XXX-XXX-XX-XX", email="maria@example.com")
    
    # Создание с помощью генератора словаря
    squares_dict = {x: x**2 for x in range(1, 6)}
    
    print(f"Словарь person: {person}")
    print(f"Словарь contact: {contact}")
    print(f"Словарь квадратов: {squares_dict}")
    
    # Основные операции со словарями
    # Доступ к значениям
    print(f"Имя: {person['имя']}")
    print(f"Возраст: {person.get('возраст', 'неизвестно')}")
    
    # Добавление и изменение значений
    person["профессия"] = "программист"
    person["возраст"] = 31  # Изменение существующего значения
    print(f"Обновленный словарь: {person}")
    
    # Итерация по словарю
    print("Итерация по словарю:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    # Итерация только по ключам
    print("Ключи:", list(person.keys()))
    
    # Итерация только по значениям
    print("Значения:", list(person.values()))
    
    # Объединение словарей (Python 3.9+)
    merged = person | contact
    print(f"Объединенный словарь: {merged}")
    
    # Использование defaultdict
    dd = defaultdict(list)
    dd["фрукты"].append("яблоко")
    dd["фрукты"].append("банан")
    dd["овощи"].append("морковь")
    print(f"defaultdict: {dict(dd)}")
    
    # Использование OrderedDict для сохранения порядка вставки
    ordered = OrderedDict()
    ordered["первый"] = 1
    ordered["второй"] = 2
    ordered["третий"] = 3
    print(f"OrderedDict: {ordered}")
    print()

dictionary_examples()

# 4. Множества (Sets)
def set_examples():
    """
    Примеры работы с множествами
    """
    print("=== Множества (Sets) ===")
    
    # Создание множеств
    fruits = {"яблоко", "банан", "апельсин"}
    numbers = {1, 2, 3, 4, 5}
    mixed = {1, "текст", 3.14, True}  # Заметьте, True становится 1
    
    print(f"Множество фруктов: {fruits}")
    print(f"Множество чисел: {numbers}")
    print(f"Смешанное множество: {mixed}")
    
    # Создание множества с помощью set()
    from_list = set([1, 2, 2, 3, 3, 4, 5])  # Убирает дубликаты
    print(f"Множество из списка (без дубликатов): {from_list}")
    
    # Основные операции с множествами
    # Добавление элементов
    fruits.add("груша")
    print(f"После добавления груши: {fruits}")
    
    # Удаление элементов
    fruits.discard("банан")  # Не вызывает ошибку, если элемент не существует
    print(f"После удаления банана: {fruits}")
    
    # Операции над множествами
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    
    print(f"set1: {set1}, set2: {set2}")
    print(f"Объединение: {set1 | set2}")
    print(f"Пересечение: {set1 & set2}")
    print(f"Разность: {set1 - set2}")
    print(f"Симметричная разность: {set1 ^ set2}")
    
    # Проверка принадлежности
    print(f"'яблоко' в множестве fruits: {'яблоко' in fruits}")
    print(f"'банан' в множестве fruits: {'банан' in fruits}")
    
    # Подмножества и надмножества
    subset = {1, 2}
    superset = {1, 2, 3, 4, 5}
    print(f"{subset} является подмножеством {superset}: {subset.issubset(superset)}")
    print(f"{superset} является надмножеством {subset}: {superset.issuperset(subset)}")
    
    # Множества frozenset (неизменяемые)
    frozen = frozenset([1, 2, 3, 4, 5])
    print(f"frozenset: {frozen}")
    # frozen.add(6)  # Это вызовет ошибку, так как frozenset неизменяем
    print()

set_examples()

# 5. deque (двусторонняя очередь)
def deque_examples():
    """
    Примеры работы с deque (двусторонняя очередь)
    """
    print("=== deque (двусторонняя очередь) ===")
    
    # Создание deque
    dq = deque([1, 2, 3, 4, 5])
    print(f"Исходный deque: {dq}")
    
    # Добавление элементов
    dq.append(6)  # Добавить в конец
    dq.appendleft(0)  # Добавить в начало
    print(f"После добавления в конец и начало: {dq}")
    
    # Удаление элементов
    right = dq.pop()  # Удалить с конца
    left = dq.popleft()  # Удалить с начала
    print(f"Удаленные элементы: {right}, {left}")
    print(f"Текущий deque: {dq}")
    
    # Другие полезные методы
    dq.extend([6, 7, 8])  # Расширить в конец
    print(f"После расширения в конец: {dq}")
    
    dq.extendleft([0, -1, -2])  # Расширить в начало (в обратном порядке)
    print(f"После расширения в начало: {dq}")
    
    # Вращение (циклический сдвиг)
    dq.rotate(2)  # Сдвиг вправо на 2
    print(f"После вращения вправо на 2: {dq}")
    
    dq.rotate(-3)  # Сдвиг влево на 3
    print(f"После вращения влево на 3: {dq}")
    
    # Ограничение размера
    fixed_dq = deque(maxlen=3)
    for i in range(6):
        fixed_dq.append(i)
        print(f"Добавлен {i}, deque: {fixed_dq}")
    print()

deque_examples()

# 6. Counter (счетчик элементов)
def counter_examples():
    """
    Примеры работы с Counter
    """
    print("=== Counter (счетчик элементов) ===")
    
    # Создание Counter из строки
    text = "hello world"
    char_count = Counter(text)
    print(f"Подсчет символов в '{text}': {char_count}")
    
    # Создание Counter из списка
    words = ["яблоко", "банан", "яблоко", "апельсин", "банан", "яблоко"]
    word_count = Counter(words)
    print(f"Подсчет слов: {word_count}")
    
    # Наиболее частые элементы
    print(f"Наиболее частые слова: {word_count.most_common(2)}")
    
    # Добавление элементов
    word_count.update(["банан", "груша", "яблоко"])
    print(f"После обновления: {word_count}")
    
    # Математические операции с Counter
    c1 = Counter(["a", "b", "c", "a", "b", "b"])
    c2 = Counter(["a", "b", "b", "d"])
    
    print(f"c1: {c1}")
    print(f"c2: {c2}")
    print(f"Сложение: {c1 + c2}")
    print(f"Вычитание: {c1 - c2}")
    print(f"Пересечение (минимум): {c1 & c2}")
    print(f"Объединение (максимум): {c1 | c2}")
    
    # Удаление нулевых и отрицательных значений
    c1.subtract(c2)  # Не удаляет элементы, может давать отрицательные значения
    print(f"После вычитания (subtract): {c1}")
    print()

counter_examples()

# 7. Примеры продвинутых коллекций
def advanced_collection_examples():
    """
    Примеры продвинутых коллекций и их использования
    """
    print("=== Продвинутые коллекции ===")
    
    # ChainMap для объединения нескольких словарей
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    dict3 = {"a": 5, "e": 6}  # 'a' уже есть в dict1
    
    chain = ChainMap(dict1, dict2, dict3)
    print(f"ChainMap: {chain}")
    print(f"Значение 'a': {chain['a']}")  # Берется из первого словаря с этим ключом
    print(f"Значение 'c': {chain['c']}")  # Берется из dict2
    print(f"Значение 'e': {chain['e']}")  # Берется из dict3
    
    # Добавление нового словаря в начало цепочки
    dict4 = {"f": 7, "a": 8}
    new_chain = chain.new_child(dict4)
    print(f"ChainMap с новым словарем: {new_chain}")
    print(f"Новое значение 'a': {new_chain['a']}")  # Теперь из dict4
    
    # Использование array для эффективного хранения чисел
    import array
    arr = array.array('i', [1, 2, 3, 4, 5])  # 'i' означает целые числа
    print(f"Array: {arr.tolist()}")
    arr.append(6)
    print(f"После добавления 6: {arr.tolist()}")
    
    # Использование heapq для работы с кучей
    heap = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Исходный список: {heap}")
    
    # Преобразование в кучу
    heapq.heapify(heap)
    print(f"Куча: {heap}")
    
    # Добавление элемента в кучу
    heapq.heappush(heap, 0)
    print(f"После добавления 0: {heap}")
    
    # Извлечение минимального элемента
    min_elem = heapq.heappop(heap)
    print(f"Извлечен минимальный элемент: {min_elem}, куча: {heap}")
    
    # Получение n наибольших/наименьших элементов
    largest = heapq.nlargest(3, [3, 1, 4, 1, 5, 9, 2, 6])
    smallest = heapq.nsmallest(3, [3, 1, 4, 1, 5, 9, 2, 6])
    print(f"3 наибольших: {largest}")
    print(f"3 наименьших: {smallest}")
    print()

advanced_collection_examples()

# 8. Использование коллекций для решения задач
def collection_problem_solving():
    """
    Примеры использования коллекций для решения задач
    """
    print("=== Решение задач с использованием коллекций ===")
    
    # Задача 1: Найти наиболее часто встречающиеся слова в тексте
    def find_most_common_words(text, n=3):
        """
        Найти n наиболее часто встречающихся слов в тексте
        """
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = Counter(words)
        return word_count.most_common(n)
    
    sample_text = "Python - это мощный язык программирования. Python позволяет создавать эффективные приложения. Язык Python прост в изучении."
    common_words = find_most_common_words(sample_text)
    print(f"Наиболее частые слова в тексте: {common_words}")
    
    # Задача 2: Реализация LIFO и FIFO очередей
    class Stack:
        """LIFO (Last In, First Out) стек"""
        def __init__(self):
            self.items = []
        
        def push(self, item):
            self.items.append(item)
        
        def pop(self):
            if not self.is_empty():
                return self.items.pop()
            return None
        
        def peek(self):
            if not self.is_empty():
                return self.items[-1]
            return None
        
        def is_empty(self):
            return len(self.items) == 0
        
        def size(self):
            return len(self.items)
    
    class Queue:
        """FIFO (First In, First Out) очередь"""
        def __init__(self):
            self.items = deque()
        
        def enqueue(self, item):
            self.items.append(item)
        
        def dequeue(self):
            if not self.is_empty():
                return self.items.popleft()
            return None
        
        def front(self):
            if not self.is_empty():
                return self.items[0]
            return None
        
        def is_empty(self):
            return len(self.items) == 0
        
        def size(self):
            return len(self.items)
    
    # Демонстрация стека
    stack = Stack()
    for item in [1, 2, 3, 4, 5]:
        stack.push(item)
    
    print(f"Стек: {stack.items}")
    print(f"Извлечение из стека: {[stack.pop() for _ in range(3)]}")
    
    # Демонстрация очереди
    queue = Queue()
    for item in [1, 2, 3, 4, 5]:
        queue.enqueue(item)
    
    print(f"Очередь: {list(queue.items)}")
    print(f"Извлечение из очереди: {[queue.dequeue() for _ in range(3)]}")
    
    # Задача 3: Группировка данных
    def group_by_category(items):
        """
        Группировка элементов по категории
        """
        groups = defaultdict(list)
        for item in items:
            category = item.get('category', 'без_категории')
            groups[category].append(item)
        return groups
    
    products = [
        {"name": "Ноутбук", "category": "электроника", "price": 50000},
        {"name": "Книга", "category": "литература", "price": 500},
        {"name": "Телефон", "category": "электроника", "price": 30000},
        {"name": "Мышь", "category": "электроника", "price": 1000},
        {"name": "Журнал", "category": "литература", "price": 200}
    ]
    
    grouped_products = group_by_category(products)
    print(f"Группировка товаров по категориям:")
    for category, items in grouped_products.items():
        print(f"  {category}: {[item['name'] for item in items]}")
    
    print()

collection_problem_solving()

# 9. Практические примеры использования коллекций
def practical_collection_examples():
    """
    Практические примеры использования коллекций
    """
    print("=== Практические примеры использования коллекций ===")
    
    # Пример 1: Система учета задач
    class TaskManager:
        def __init__(self):
            self.tasks = defaultdict(list)
            self.completed_tasks = set()
            self.all_categories = set()
        
        def add_task(self, task, category="общее"):
            self.tasks[category].append(task)
            self.all_categories.add(category)
        
        def complete_task(self, task):
            for category, task_list in self.tasks.items():
                if task in task_list:
                    task_list.remove(task)
                    self.completed_tasks.add(task)
                    break
        
        def get_tasks_by_category(self, category):
            return self.tasks[category]
        
        def get_all_tasks(self):
            all_tasks = []
            for category, task_list in self.tasks.items():
                all_tasks.extend([(task, category) for task in task_list])
            return all_tasks
    
    tm = TaskManager()
    tm.add_task("Изучить Python", "обучение")
    tm.add_task("Написать программу", "работа")
    tm.add_task("Прочитать статью", "обучение")
    tm.add_task("Купить продукты", "личное")
    
    print(f"Все задачи: {tm.get_all_tasks()}")
    print(f"Задачи по категории 'обучение': {tm.get_tasks_by_category('обучение')}")
    
    tm.complete_task("Изучить Python")
    print(f"Выполненные задачи: {tm.completed_tasks}")
    print(f"Все задачи после выполнения: {tm.get_all_tasks()}")
    
    # Пример 2: Словарь для быстрого поиска
    class DictionaryLookup:
        def __init__(self):
            self.words = {}  # Словарь слов
            self.word_lengths = defaultdict(list)  # Слова по длине
        
        def add_word(self, word, definition):
            self.words[word.lower()] = definition
            self.word_lengths[len(word)].append(word.lower())
        
        def lookup(self, word):
            return self.words.get(word.lower(), "Слово не найдено")
        
        def words_by_length(self, length):
            return self.word_lengths[length]
        
        def search_by_prefix(self, prefix):
            prefix = prefix.lower()
            matches = [word for word in self.words.keys() if word.startswith(prefix)]
            return matches[:10]  # Ограничиваем результат
    
    dictionary = DictionaryLookup()
    dictionary.add_word("Python", "Язык программирования")
    dictionary.add_word("Tkinter", "Библиотека для GUI")
    dictionary.add_word("Collection", "Группа элементов")
    dictionary.add_word("Decorator", "Функция, изменяющая поведение другой функции")
    
    print(f"Поиск 'python': {dictionary.lookup('python')}")
    print(f"Слова длиной 6: {dictionary.words_by_length(6)}")
    print(f"Слова с префиксом 'col': {dictionary.search_by_prefix('col')}")
    
    print()

practical_collection_examples()

# 10. Заключение: выбор подходящей коллекции
def choosing_the_right_collection():
    """
    Рекомендации по выбору подходящей коллекции
    """
    print("=== Выбор подходящей коллекции ===")
    
    recommendations = {
        "Список (list)": [
            "Когда нужен упорядоченный изменяемый набор элементов",
            "Когда нужен доступ по индексу",
            "Когда часто добавляются/удаляются элементы в конец"
        ],
        "Кортеж (tuple)": [
            "Когда нужен упорядоченный неизменяемый набор элементов",
            "Когда кортеж используется как ключ словаря",
            "Когда важна неизменяемость данных"
        ],
        "Словарь (dict)": [
            "Когда нужна ассоциация ключ-значение",
            "Когда нужен быстрый доступ к данным по ключу",
            "Когда данные структурированы в пары"
        ],
        "Множество (set)": [
            "Когда нужна уникальность элементов",
            "Когда важны операции над множествами (объединение, пересечение)",
            "Когда нужна проверка принадлежности элемента"
        ],
        "Deque": [
            "Когда часто добавляются/удаляются элементы с обоих концов",
            "Когда нужна эффективная реализация очереди",
            "Когда нужен циклический буфер"
        ],
        "Counter": [
            "Когда нужно подсчитать вхождения элементов",
            "Когда нужно сравнивать количества элементов",
            "Когда нужно статистика по данным"
        ],
        "defaultdict": [
            "Когда нужно автоматически создавать значения для новых ключей",
            "Когда часто работаем с вложенными структурами",
            "Когда не хотим проверять существование ключей"
        ]
    }
    
    for collection, reasons in recommendations.items():
        print(f"{collection}:")
        for reason in reasons:
            print(f"  - {reason}")
        print()

choosing_the_right_collection()
