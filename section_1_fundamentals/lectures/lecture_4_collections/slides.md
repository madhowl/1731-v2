# Лекция 4: Модуль collections

## namedtuple, deque, Counter, OrderedDict, defaultdict, ChainMap

### План лекции:
1. Введение в модуль collections
2. namedtuple
3. deque
4. Counter
5. OrderedDict
6. defaultdict
7. ChainMap
8. Практические примеры использования

---

## 1. Введение в модуль collections

Модуль `collections` предоставляет специализированные типы данных, которые дополняют стандартные типы данных, такие как `dict`, `list`, `set` и `tuple`. Эти типы данных реализуют альтернативные структуры данных, которые могут быть более эффективными в определенных ситуациях.

```python
from collections import namedtuple, deque, Counter, OrderedDict, defaultdict, ChainMap
```

---

## 2. namedtuple

`namedtuple` создает подкласс кортежа с именованными полями. Это позволяет обращаться к элементам кортежа по имени, а не только по индексу.

### Пример использования:

```python
from collections import namedtuple

# Создаем тип Point с полями x и y
Point = namedtuple('Point', ['x', 'y'])

# Создаем экземпляр
p = Point(11, y=22)

# Доступ к полям
print(p.x, p.y)  # 11 22
print(p[0], p[1])  # 11 22

# Распаковка
x, y = p
print(x, y)  # 11 22

# Методы namedtuple
print(p._fields)  # ('x', 'y')
print(p._asdict())  # OrderedDict([('x', 11), ('y', 22)])

# Замена значения поля
p2 = p._replace(x=10)
print(p2)  # Point(x=100, y=22)
```

### Практическое применение:

```python
# Определение структуры для хранения информации о сотруднике
Employee = namedtuple('Employee', ['name', 'id', 'department', 'salary'])

# Создание списка сотрудников
employees = [
    Employee('Иван Иванов', 1, 'IT', 75000),
    Employee('Мария Петрова', 2, 'HR', 65000),
    Employee('Алексей Сидоров', 3, 'IT', 80000)
]

# Легкий доступ к информации
for emp in employees:
    print(f"{emp.name} работает в отделе {emp.department} с зарплатой {emp.salary}")
```

---

## 3. deque

`deque` (double-ended queue) - это обобщение стека и очереди. Элементы можно добавлять и удалять с обоих концов. `deque` оптимизирован для быстрых операций добавления и удаления с любого конца.

```python
from collections import deque

# Создание deque
d = deque([1, 2, 3])

# Добавление элементов
d.append(4)        # Добавить в конец
d.appendleft(0)    # Добавить в начало
print(d)           # deque([0, 1, 2, 3, 4])

# Удаление элементов
right = d.pop()       # Удалить с конца
left = d.popleft()    # Удалить с начала
print(right, left)    # 4 0
print(d)              # deque([1, 2, 3])

# Ограничение размера
fixed_d = deque(maxlen=3)
fixed_d.extend([1, 2, 3, 4, 5])
print(fixed_d)        # deque([3, 4, 5], maxlen=3)
```

### Практическое применение:

```python
# Реализация скользящего окна
def sliding_window_average(iterable, window_size):
    window = deque(maxlen=window_size)
    for value in iterable:
        window.append(value)
        if len(window) == window_size:
            avg = sum(window) / len(window)
            yield avg

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
averages = list(sliding_window_average(data, 3))
print(averages)  # [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
```

---

## 4. Counter

`Counter` - это подкласс словаря, который помогает подсчитывать хешируемые объекты. Он принимает итерируемый объект и возвращает словарь, где ключами являются элементы, а значениями - их количество.

```python
from collections import Counter

# Подсчет элементов в строке
text = "hello world"
counter = Counter(text)
print(counter)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

# Подсчет элементов в списке
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
word_count = Counter(words)
print(word_count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Наиболее частые элементы
print(word_count.most_common(2))  # [('apple', 3), ('banana', 2)]

# Математические операции
c1 = Counter(['a', 'b', 'c', 'a'])
c2 = Counter(['a', 'b', 'b', 'd'])
print(c1 + c2)  # Counter({'a': 3, 'b': 3, 'c': 1, 'd': 1})
print(c1 - c2)  # Counter({'c': 1, 'a': 1})
print(c1 & c2)  # Counter({'a': 1, 'b': 1}) (минимум)
print(c1 | c2)  # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1}) (максимум)
```

---

## 5. OrderedDict

`OrderedDict` - это словарь, который помнит порядок добавления элементов. В Python 3.7+ обычный `dict` также сохраняет порядок, но `OrderedDict` предоставляет дополнительные методы для работы с порядком.

```python
from collections import OrderedDict

# Создание Ordered Dict
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od['third'] = 3
print(od)  # OrderedDict([('first', 1), ('second', 2), ('third', 3)])

# Перемещение элемента в конец или начало
od.move_to_end('first')  # Переместить 'first' в конец
print(od)  # OrderedDict([('second', 2), ('third', 3), ('first', 1)])

od.move_to_end('third', last=False)  # Переместить 'third' в начало
print(od)  # OrderedDict([('third', 3), ('second', 2), ('first', 1)])

# Удаление последнего элемента
last_item = od.popitem(last=True)
print(last_item)  # ('first', 1)
print(od)  # OrderedDict([('third', 3), ('second', 2)])
```

---

## 6. defaultdict

`defaultdict` автоматически создает значение для несуществующего ключа, используя функцию-фабрику, предоставленную при создании.

```python
from collections import defaultdict

# Обычный словарь
regular_dict = {}
# regular_dict['missing_key']  # Вызовет KeyError

# defaultdict с int в качестве фабрики
dd = defaultdict(int)
print(dd['missing_key'])  # 0 (int() возвращает 0)
dd['a'] += 1
dd['b'] += 2
print(dd)  # defaultdict(<class 'int'>, {'a': 1, 'b': 2})

# defaultdict со списком в качестве фабрики
dd_list = defaultdict(list)
dd_list['fruits'].append('apple')
dd_list['fruits'].append('banana')
dd_list['vegetables'].append('carrot')
print(dd_list)  # defaultdict(<class 'list'>, {'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})

# defaultdict с set в качестве фабрики
dd_set = defaultdict(set)
dd_set['colors'].add('red')
dd_set['colors'].add('blue')
dd_set['shapes'].add('circle')
print(dd_set)  # defaultdict(<class 'set'>, {'colors': {'red', 'blue'}, 'shapes': {'circle'}})
```

---

## 7. ChainMap

`ChainMap` объединяет несколько словарей в одно отображение. Поиск производится последовательно во всех словарях до тех пор, пока ключ не будет найден.

```python
from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
dict3 = {'a': 5, 'e': 6}

chain = ChainMap(dict1, dict2, dict3)
print(chain['a'])  # 1 (берется из первого словаря)
print(chain['c'])  # 3 (берется из второго словаря)
print(chain['e'])  # 6 (берется из третьего словаря)

# Добавление нового словаря в начало цепочки
dict4 = {'f': 7, 'a': 8}
new_chain = chain.new_child(dict4)
print(new_chain['a'])  # 8 (берется из нового словаря)
print(len(new_chain.maps))  # 4 (4 словаря в цепочке)

# Доступ к родительскому ChainMap
parent_chain = new_chain.parents
print(parent_chain['a'])  # 1 (берется из исходного dict1)
```

---

## 8. Практические примеры использования

### Пример 1: Анализ текста

```python
from collections import Counter, defaultdict

def analyze_text(text):
    """Анализ текста с подсчетом слов и букв"""
    words = text.lower().split()
    word_count = Counter(words)
    
    letters = Counter(text.lower())
    del letters[' ']  # Удаляем пробелы
    
    return word_count, letters

text = "Python is great and Python is fun"
word_freq, letter_freq = analyze_text(text)

print("Частота слов:", word_freq)
print("Частота букв:", letter_freq)
```

### Пример 2: Группировка данных

```python
from collections import defaultdict

def group_students_by_grade(students):
    """Группировка студентов по оценкам"""
    grouped = defaultdict(list)
    
    for student in students:
        grade = student['grade']
        grouped[grade].append(student['name'])
    
    return grouped

students = [
    {'name': 'Иван', 'grade': 'A'},
    {'name': 'Мария', 'grade': 'B'},
    {'name': 'Петр', 'grade': 'A'},
    {'name': 'Анна', 'grade': 'C'},
    {'name': 'Сергей', 'grade': 'B'}
]

grouped = group_students_by_grade(students)
for grade, names in grouped.items():
    print(f"Оценка {grade}: {', '.join(names)}")
```

### Пример 3: Кэширование с ограниченным размером

```python
from collections import OrderedDict

class LRUCache:
    """LRU (Least Recently Used) кэш"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # Перемещаем элемент в конец (помечаем как недавно использованный)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            # Обновляем существующий ключ
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Удаляем самый старый элемент (первый в порядке добавления)
            self.cache.popitem(last=False)
        
        self.cache[key] = value

# Использование
lru = LRUCache(3)
lru.put('a', 1)
lru.put('b', 2)
lru.put('c', 3)
print(lru.get('a'))  # 1
lru.put('d', 4)  # Удаляет 'b'
print(lru.cache)  # OrderedDict([('c', 3), ('a', 1), ('d', 4)])
```

---

## Заключение

Модуль `collections` предоставляет мощные инструменты для работы с данными. Использование этих специализированных типов данных может сделать код более читаемым, эффективным и менее подверженным ошибкам.

## Контрольные вопросы:
1. В чем преимущество namedtuple перед обычным кортежем?
2. Когда лучше использовать deque вместо обычного списка?
3. Какие операции можно выполнять с Counter?
4. В чем разница между OrderedDict и обычным dict?
5. Для чего используется defaultdict?
6. Как работает ChainMap?
