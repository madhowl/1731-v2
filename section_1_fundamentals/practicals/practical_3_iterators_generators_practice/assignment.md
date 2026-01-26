# Практическое занятие 3: Обработка ошибок

## Цель занятия
Научиться использовать механизмы обработки ошибок в Python для создания надежных приложений.

## Задачи
1. Изучить основные конструкции try-except-finally
2. Научиться обрабатывать различные типы исключений
3. Понять разницу между исключениями и ошибками
4. Научиться создавать собственные исключения
5. Применить обработку ошибок в реальных сценариях

## Ход работы

### 1. Основы обработки исключений

Создайте файл `exception_handling_basics.py` и реализуйте следующие примеры:

#### Простая обработка исключения

```python
def divide_numbers(a, b):
    """
    Функция деления двух чисел с обработкой исключения
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль невозможно")
        return None

# Пример использования
print(divide_numbers(10, 2))  # 5.0
print(divide_numbers(10, 0))  # Ошибка: Деление на ноль невозможно, None
```

#### Обработка нескольких типов исключений

```python
def safe_convert_to_int(value):
    """
    Безопасное преобразование значения в целое число
    """
    try:
        result = int(value)
        return result
    except ValueError:
        print(f"Ошибка: '{value}' невозможно преобразовать в число")
        return None
    except TypeError:
        print(f"Ошибка: '{value}' имеет неподдерживаемый тип для преобразования")
        return None

# Примеры использования
print(safe_convert_to_int("123"))  # 123
print(safe_convert_to_int("abc"))  # Ошибка: 'abc' невозможно преобразовать в число
print(safe_convert_to_int(None))   # Ошибка: 'None' имеет неподдерживаемый тип для преобразования
```

### 2. Конструкция try-except-else-finally

```python
def process_file(filename):
    """
    Обработка файла с полной конструкцией try-except-else-finally
    """
    file_handle = None
    try:
        file_handle = open(filename, 'r', encoding='utf-8')
        content = file_handle.read()
        data = content.split('\n')
        print(f"Файл успешно прочитан, строк: {len(data)}")
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
    except PermissionError:
        print(f"Ошибка: Нет доступа к файлу {filename}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    else:
        # Выполняется только если не было исключений
        print("Дополнительная обработка данных...")
        return data
    finally:
        # Выполняется всегда
        if file_handle:
            file_handle.close()
            print("Файл закрыт")

# Пример использования
process_file("nonexistent.txt")  # Ошибка: файл не найден
# process_file("existing_file.txt")  # Для тестирования с существующим файлом
```

---

## 3. Создание пользовательских исключений

```python
class ValidationError(Exception):
    """Исключение для ошибок валидации данных"""
    pass

class InsufficientFundsError(Exception):
    """Исключение для ошибок недостатка средств"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Недостаточно средств: баланс {balance}, запрошено {amount}")

class BankAccount:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValidationError("Начальный баланс не может быть отрицательным")
        self.balance = initial_balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValidationError("Сумма снятия должна быть положительной")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

# Пример использования
try:
    account = BankAccount(-100)  # Вызовет ValidationError
except ValidationError as e:
    print(f"Ошибка создания счета: {e}")

try:
    account = BankAccount(100)
    account.withdraw(150)  # Вызовет InsufficientFundsError
except InsufficientFundsError as e:
    print(f"Ошибка снятия: {e}")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

### 4. Контекстные менеджеры и обработка ошибок

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False
    
    def __enter__(self):
        print(f"Подключение к базе данных: {self.connection_string}")
        # Здесь обычно происходит реальное подключение
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Закрытие соединения с базой данных")
        self.connected = False
        
        if exc_type:
            print(f"Произошло исключение: {exc_type.__name__}: {exc_value}")
        
        # Возвращаем False, чтобы исключение продолжило распространение
        return False
    
    def execute_query(self, query):
        if not self.connected:
            raise ConnectionError("Соединение с базой данных не установлено")
        print(f"Выполнение запроса: {query}")
        # Здесь обычно выполняется реальный запрос

# Пример использования
try:
    with DatabaseConnection("sqlite:///example.db") as db:
        db.execute_query("SELECT * FROM users")
        # Искусственно создаем ошибку для демонстрации
        raise ValueError("Искусственная ошибка для тестирования")
except ValueError as e:
    print(f"Обработано исключение: {e}")
```

---

## 5. Практические задания

### Задание 1: Калькулятор с обработкой ошибок

Создайте калькулятор, который обрабатывает все возможные ошибки:

```python
def safe_calculator(operation, a, b):
    """
    Безопасный калькулятор с обработкой ошибок
    
    Args:
        operation (str): Операция ('+', '-', '*', '/', '**', '%')
        a (float): Первое число
        b (float): Второе число
    
    Returns:
        float or None: Результат операции или None в случае ошибки
    """
    # Ваш код здесь
    pass

# Тестирование
operations = [
    ('+', 10, 5),
    ('-', 10, 5),
    ('*', 10, 5),
    ('/', 10, 5),
    ('/', 10, 0),  # Деление на ноль
    ('**', 2, 3),
    ('%', 10, 3),
    ('invalid', 10, 5)  # Неверная операция
]

for op, x, y in operations:
    result = safe_calculator(op, x, y)
    print(f"{x} {op} {y} = {result}")
```

### Задание 2: Валидация данных пользователя

Создайте функцию для валидации данных пользователя:

```python
class UserDataValidator:
    @staticmethod
    def validate_email(email):
        """Проверка формата email"""
        # Реализуйте проверку формата email
        pass
    
    @staticmethod
    def validate_phone(phone):
        """Проверка формата телефона"""
        # Реализуйте проверку формата телефона
        pass
    
    @staticmethod
    def validate_age(age):
        """Проверка возраста"""
        # Проверьте, что возраст в допустимом диапазоне
        pass
    
    @classmethod
    def validate_user_data(cls, user_data):
        """
        Валидация всех данных пользователя
        
        Args:
            user_data (dict): Данные пользователя с ключами: name, email, phone, age
        
        Raises:
            ValidationError: Если данные невалидны
        """
        # Ваш код здесь
        pass

# Пример использования
user_data = {
    "name": "Иван Иванов",
    "email": "ivan@example.com",
    "phone": "+79123456789",
    "age": 25
}

try:
    UserDataValidator.validate_user_data(user_data)
    print("Данные пользователя валидны")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

### Задание 3: Обработка ошибок ввода-вывода

Создайте функцию для безопасного чтения и записи файлов:

```python
def safe_file_operations():
    """Демонстрация обработки ошибок при работе с файлами"""
    # Ваш код здесь
    pass

# Реализуйте функцию, которая:
# 1. Читает данные из файла
# 2. Обрабатывает возможные ошибки (файл не найден, нет доступа и т.д.)
# 3. Записывает обработанные данные в новый файл
# 4. Использует контекстные менеджеры
```

---

## Контрольные вопросы

1. В чем разница между исключениями и ошибками?
2. Какие типы исключений вы знаете?
3. Когда использовать конструкцию try-except-else-finally?
4. Как создать собственное исключение?
5. Что такое контекстный менеджер и как его использовать?
6. Как обрабатываются исключения в Python?
7. В чем преимущества обработки исключений?

## Дополнительное задание

Реализуйте систему логирования ошибок, которая сохраняет информацию об исключениях в файл с временной меткой.
