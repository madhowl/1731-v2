# Лекция 21: Работа с базами данных

## Введение в SQL, модуль sqlite3, основные команды SQL

### Цель лекции:
- Познакомиться с основами работы с базами данных
- Изучить модуль sqlite3 в Python
- Освоить основные команды SQL

### План лекции:
1. Введение в базы данных
2. Модуль sqlite3
3. Основные команды SQL
4. Работа с базой данных в Python

---

## 1. Введение в базы данных

База данных — организованная коллекция структурированных записей или данных, обычно хранимая в компьютерной системе.

### Типы баз данных:
- **Реляционные** (SQL) - данные хранятся в таблицах
- **Нереляционные** (NoSQL) - гибкая структура данных

### Реляционные базы данных:
- MySQL, PostgreSQL, SQLite, Oracle, MS SQL Server
- Используют язык SQL (Structured Query Language)
- Данные организованы в таблицы, строки и столбцы

### Основные понятия:
- **Таблица** - коллекция связанных данных
- **Строка** - запись в таблице
- **Столбец** - атрибут данных
- **Ключ** - уникальный идентификатор записи

---

## 2. Модуль sqlite3

SQLite — встроенная в Python реляционная база данных без необходимости в отдельном сервере.

### Подключение к базе данных:
```python
import sqlite3

# Подключение к базе данных (создаст файл, если не существует)
conn = sqlite3.connect('example.db')

# Создание курсора
cursor = conn.cursor()
```

### Создание таблицы:
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER
    )
''')
```

### Закрытие соединения:
```python
conn.commit()  # Сохранение изменений
conn.close()   # Закрытие соединения
```

### Контекстный менеджер:
```python
with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()
    # Работа с базой данных
    # conn.commit() и conn.close() вызываются автоматически
```

---

## 3. Основные команды SQL

### CREATE TABLE - создание таблицы:
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT,
    salary REAL
);
```

### INSERT - добавление данных:
```sql
INSERT INTO employees (name, position, salary) 
VALUES ('Иван Иванов', 'Программист', 75000);
```

### SELECT - выборка данных:
```sql
SELECT * FROM employees;
SELECT name, salary FROM employees WHERE salary > 50000;
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;
```

### UPDATE - обновление данных:
```sql
UPDATE employees SET salary = 80000 WHERE name = 'Иван Иванов';
```

### DELETE - удаление данных:
```sql
DELETE FROM employees WHERE id = 1;
```

### WHERE - условия:
```sql
SELECT * FROM employees WHERE position = 'Программист' AND salary > 60000;
```

---

## 4. Работа с базой данных в Python

### Вставка данных:
```python
import sqlite3

with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()
    
    # Безопасная вставка данных (предотвращение SQL-инъекций)
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        ("Иван Петров", "ivan@example.com", 30)
    )
```

### Выборка данных:
```python
with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()
    
    # Выборка всех записей
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
        
    # Выборка одной записи
    cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
    row = cursor.fetchone()
    print(row)
```

### Использование именованных параметров:
```python
cursor.execute("""
    SELECT * FROM users 
    WHERE age > :min_age AND email LIKE :email_pattern
""", {"min_age": 25, "email_pattern": "%@gmail.com"})
```

### Работа с несколькими строками:
```python
users_data = [
    ("Анна Смирнова", "anna@example.com", 28),
    ("Петр Сидоров", "petr@example.com", 35),
    ("Мария Козлова", "maria@example.com", 22)
]

cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users_data
)