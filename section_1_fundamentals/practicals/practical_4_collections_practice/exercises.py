# Упражнения для практического занятия 4: Использование модуля collections

from collections import namedtuple, deque, Counter, OrderedDict, defaultdict
import random
import string

# Задание 1: namedtuple
def create_student_namedtuple():
    """Создает namedtuple для студента"""
    Student = namedtuple('Student', ['name', 'age', 'grade', 'subjects'])
    return Student

def create_students_list(Student):
    """Создает список студентов"""
    students = [
        Student('Иванов Иван', 20, 'A', ['Математика', 'Физика']),
        Student('Петров Петр', 19, 'B', ['История', 'Литература']),
        Student('Сидорова Мария', 21, 'A', ['Химия', 'Биология']),
        Student('Козлов Алексей', 20, 'C', ['Информатика', 'Математика'])
    ]
    return students

# Задание 2: deque
def demonstrate_stack():
    """Демонстрирует работу стека с использованием deque"""
    stack = deque()
    
    # Операция push
    for i in range(1, 6):
        stack.append(i)
        print(f"Добавлен элемент: {i}, стек: {list(stack)}")
    
    # Операция pop
    while stack:
        element = stack.pop()
        print(f"Извлечен элемент: {element}, стек: {list(stack)}")

def demonstrate_queue():
    """Демонстрирует работу очереди с использованием deque"""
    queue = deque()
    
    # Операция enqueue
    for i in range(1, 6):
        queue.append(i)
        print(f"Добавлен элемент: {i}, очередь: {list(queue)}")
    
    # Операция dequeue
    while queue:
        element = queue.popleft()
        print(f"Извлечен элемент: {element}, очередь: {list(queue)}")

# Задание 3: Counter
def analyze_text(text):
    """Анализирует текст с использованием Counter"""
    # Разбиваем текст на слова и приводим к нижнему регистру
    words = text.lower().split()
    # Убираем знаки препинания
    cleaned_words = []
    for word in words:
        cleaned_word = ''.join(char for char in word if char.isalnum())
        if cleaned_word:
            cleaned_words.append(cleaned_word)
    
    word_counts = Counter(cleaned_words)
    return word_counts

def compare_texts(text1, text2):
    """Сравнивает два текста по частоте слов"""
    counter1 = analyze_text(text1)
    counter2 = analyze_text(text2)
    
    # Находим общие слова
    common_words = set(counter1.keys()) & set(counter2.keys())
    
    comparison = {}
    for word in common_words:
        comparison[word] = (counter1[word], counter2[word])
    
    return comparison

# Задание 4: defaultdict
def group_words_by_first_letter(words):
    """Группирует слова по первой букве"""
    grouped = defaultdict(list)
    for word in words:
        first_letter = word[0].lower()
        grouped[first_letter].append(word)
    return grouped

def group_grades_by_subject(grades_data):
    """Группирует оценки студентов по предметам"""
    subject_grades = defaultdict(list)
    for student_grades in grades_data:
        for subject, grade in student_grades.items():
            subject_grades[subject].append(grade)
    return subject_grades

# Задание 5: OrderedDict (LRU Cache)
class LRUCache:
    """LRU (Least Recently Used) кэш на основе OrderedDict"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """Получает значение по ключу, обновляя его позицию"""
        if key in self.cache:
            # Перемещаем элемент в конец (как недавно использованный)
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1 # Ключ не найден

    def put(self, key, value):
        """Добавляет или обновляет значение по ключу"""
        if key in self.cache:
            # Если ключ уже существует, обновляем его позицию
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Если кэш полон, удаляем первый элемент (наименее используемый)
            self.cache.popitem(last=False)
        
        self.cache[key] = value

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: namedtuple ===")
    Student = create_student_namedtuple()
    students = create_students_list(Student)
    for student in students:
        print(f"Студент: {student.name}, Возраст: {student.age}, Оценка: {student.grade}, Предметы: {student.subjects}")

    print("\n=== Задание 2: deque (стек) ===")
    demonstrate_stack()
    
    print("\n=== Задание 2: deque (очередь) ===")
    demonstrate_queue()
    
    print("\n=== Задание 3: Counter ===")
    sample_text = "Python это отличный язык программирования. Python популярен и прост в изучении."
    word_freq = analyze_text(sample_text)
    print(f"Частота слов: {dict(word_freq)}")
    print(f"3 самых частых слова: {word_freq.most_common(3)}")
    
    text1 = "Python это язык программирования"
    text2 = "Java это тоже язык программирования"
    comparison = compare_texts(text1, text2)
    print(f"Сравнение текстов: {comparison}")
    
    print("\n=== Задание 4: defaultdict ===")
    words = ["apple", "banana", "cherry", "avocado", "blueberry", "apricot"]
    grouped_words = group_words_by_first_letter(words)
    print(f"Слова по первой букве: {dict(grouped_words)}")
    
    grades_data = [
        {'math': 5, 'physics': 4, 'chemistry': 5},
        {'math': 4, 'physics': 5, 'chemistry': 4},
        {'math': 5, 'physics': 5, 'chemistry': 5}
    ]
    subject_grades = group_grades_by_subject(grades_data)
    print(f"Оценки по предметам: {dict(subject_grades)}")
    
    print("\n=== Задание 5: OrderedDict (LRU Cache) ===")
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"Кэш после добавления a, b, c: {list(cache.cache.items())}")
    
    cache.get("a")  # Обновляем позицию 'a'
    print(f"Кэш после доступа к 'a': {list(cache.cache.items())}")
    
    cache.put("d", 4)  # Добавляем новый элемент, 'b' должен быть удален
    print(f"Кэш после добавления 'd': {list(cache.cache.items())}")