# Примеры базового синтаксиса Python

"""
Этот файл содержит примеры базового синтаксиса Python, 
которые помогут новичкам понять основные концепции языка.
"""

# 1. Переменные и типы данных
def variables_and_types():
    """
    Примеры переменных и типов данных
    """
    print("=== Переменные и типы данных ===")
    
    # Числа
    integer_num = 42
    float_num = 3.14159
    complex_num = 2 + 3j
    
    print(f"Целое число: {integer_num} (тип: {type(integer_num).__name__})")
    print(f"Число с плавающей точкой: {float_num} (тип: {type(float_num).__name__})")
    print(f"Комплексное число: {complex_num} (тип: {type(complex_num).__name__})")
    
    # Строки
    single_quote_string = 'Привет'
    double_quote_string = "Мир"
    multiline_string = """
    Это многострочная
    строка в Python
    """
    
    print(f"Строка 1: {single_quote_string}")
    print(f"Строка 2: {double_quote_string}")
    print(f"Многострочная строка: {multiline_string.strip()}")
    
    # Булевые значения
    is_true = True
    is_false = False
    
    print(f"Логическое значение True: {is_true}")
    print(f"Логическое значение False: {is_false}")
    
    # Списки
    fruits = ["яблоко", "банан", "апельсин"]
    numbers = [1, 2, 3, 4, 5]
    
    print(f"Список фруктов: {fruits}")
    print(f"Список чисел: {numbers}")
    
    # Словари
    person = {
        "имя": "Иван",
        "возраст": 30,
        "город": "Москва"
    }
    
    print(f"Словарь: {person}")

# 2. Условные операторы
def conditional_statements():
    """
    Примеры условных операторов
    """
    print("\n=== Условные операторы ===")
    
    age = 25
    
    if age < 18:
        print("Вы несовершеннолетний")
    elif age < 65:
        print("Вы взрослый")
    else:
        print("Вы пенсионер")
    
    # Тернарный оператор
    status = "взрослый" if age >= 18 else "несовершеннолетний"
    print(f"Статус: {status}")
    
    # Логические операторы
    temperature = 25
    is_summer = True
    
    if temperature > 20 and is_summer:
        print("Тепло и лето - отличная погода для прогулки!")
    
    if temperature < 0 or not is_summer:
        print("Возможно, стоит остаться дома")

# 3. Циклы
def loops_examples():
    """
    Примеры циклов
    """
    print("\n=== Циклы ===")
    
    # Цикл for
    print("Цикл for:")
    for i in range(5):
        print(f"  Итерация {i+1}")
    
    # Цикл for с перебором списка
    colors = ["красный", "зеленый", "синий"]
    for color in colors:
        print(f"  Цвет: {color}")
    
    # Цикл while
    print("\nЦикл while:")
    count = 0
    while count < 3:
        print(f"  Счетчик: {count}")
        count += 1
    
    # Использование break и continue
    print("\nИспользование break и continue:")
    for i in range(10):
        if i == 2:
            continue  # Пропускаем итерацию
        if i == 5:
            break     # Выходим из цикла
        print(f"  Значение: {i}")

# 4. Функции
def function_examples():
    """
    Примеры функций
    """
    print("\n=== Функции ===")
    
    # Простая функция
    def greet(name):
        return f"Привет, {name}!"
    
    print(greet("Алексей"))
    
    # Функция с аргументами по умолчанию
    def introduce(name, age=25, city="Москва"):
        return f"Меня зовут {name}, мне {age} лет, я из {city}."
    
    print(introduce("Мария"))
    print(introduce("Петр", 30, "СПб"))
    
    # Функция с произвольным количеством аргументов
    def sum_all(*args):
        return sum(args)
    
    print(f"Сумма чисел: {sum_all(1, 2, 3, 4, 5)}")
    
    # Функция с произвольными именованными аргументами
    def print_info(**kwargs):
        for key, value in kwargs.items():
            print(f"  {key}: {value}")
    
    print_info(имя="Ольга", профессия="программист", опыт=5)

# 5. Работа со строками
def string_operations():
    """
    Примеры работы со строками
    """
    print("\n=== Работа со строками ===")
    
    text = "  Python - это мощный язык программирования  "
    
    # Основные операции
    print(f"Исходный текст: '{text}'")
    print(f"Длина строки: {len(text)}")
    print(f"В нижнем регистре: {text.lower()}")
    print(f"В верхнем регистре: {text.upper()}")
    print(f"Удаление пробелов: '{text.strip()}'")
    print(f"Замена: '{text.replace('Python', 'Java')}'")
    
    # Форматирование строк
    name = "Анна"
    age = 28
    formatted_text = f"Меня зовут {name}, мне {age} лет."
    print(f"Форматирование f-строкой: {formatted_text}")
    
    # Разделение и объединение строк
    words = text.split()
    print(f"Разделенные слова: {words}")
    
    joined_text = "-".join(words)
    print(f"Объединенные слова: {joined_text}")

# 6. Работа со списками
def list_operations():
    """
    Примеры работы со списками
    """
    print("\n=== Работа со списками ===")
    
    numbers = [1, 2, 3, 4, 5]
    
    # Основные операции
    print(f"Список: {numbers}")
    print(f"Длина списка: {len(numbers)}")
    print(f"Первый элемент: {numbers[0]}")
    print(f"Последний элемент: {numbers[-1]}")
    
    # Добавление элементов
    numbers.append(6)
    print(f"После добавления 6: {numbers}")
    
    numbers.insert(2, 99)
    print(f"После вставки 99 на позицию 2: {numbers}")
    
    # Удаление элементов
    removed = numbers.pop()
    print(f"Удален последний элемент {removed}, список: {numbers}")
    
    # Срезы
    slice_example = numbers[1:4]
    print(f"Срез [1:4]: {slice_example}")
    
    # Списковые включения
    squares = [x**2 for x in range(1, 6)]
    print(f"Квадраты чисел: {squares}")
    
    # Фильтрация в списковом включении
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"Квадраты четных чисел: {even_squares}")

# 7. Работа со словарями
def dictionary_operations():
    """
    Примеры работы со словарями
    """
    print("\n=== Работа со словарями ===")
    
    student = {
        "имя": "Иван",
        "фамилия": "Петров",
        "возраст": 20,
        "курс": "Программирование",
        "оценки": [5, 4, 5, 3, 5]
    }
    
    # Основные операции
    print(f"Студент: {student}")
    print(f"Имя студента: {student['имя']}")
    print(f"Ключи словаря: {list(student.keys())}")
    print(f"Значения словаря: {list(student.values())}")
    
    # Добавление и изменение элементов
    student["группа"] = "ИВТ-101"
    print(f"После добавления группы: {student}")
    
    # Итерация по словарю
    print("Итерация по словарю:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    # Словарные включения
    grades = [5, 4, 5, 3, 5, 4, 4, 5]
    grade_count = {grade: grades.count(grade) for grade in set(grades)}
    print(f"Подсчет оценок: {grade_count}")

# 8. Обработка исключений
def exception_handling():
    """
    Примеры обработки исключений
    """
    print("\n=== Обработка исключений ===")
    
    # Пример 1: деление на ноль
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    else:
        print(f"Результат: {result}")
    finally:
        print("Этот блок выполнится всегда")
    
    # Пример 2: работа с файлами
    try:
        with open("nonexistent_file.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        print("Файл не найден")
    except PermissionError:
        print("Нет доступа к файлу")
    
    # Пример 3: преобразование типов
    try:
        number = int("abc")
    except ValueError:
        print("Невозможно преобразовать строку в число")

# 9. Модули и импорт
def modules_example():
    """
    Примеры работы с модулями
    """
    print("\n=== Модули и импорт ===")
    
    import math
    import random
    
    # Использование встроенных модулей
    print(f"Квадратный корень из 16: {math.sqrt(16)}")
    print(f"Случайное число от 1 до 10: {random.randint(1, 10)}")
    
    # Импорт конкретных функций
    from datetime import datetime, timedelta
    
    now = datetime.now()
    print(f"Текущее время: {now}")
    
    tomorrow = now + timedelta(days=1)
    print(f"Завтра: {tomorrow.strftime('%Y-%m-%d')}")

def main():
    """
    Основная функция для демонстрации всех примеров
    """
    variables_and_types()
    conditional_statements()
    loops_examples()
    function_examples()
    string_operations()
    list_operations()
    dictionary_operations()
    exception_handling()
    modules_example()
    
    print("\n=== Все примеры выполнены ===")

if __name__ == "__main__":
    main()
