# Практическое занятие 38: Работа с SQLite

## Создание таблиц, выполнение запросов

### Цель занятия:
Научиться работать с базой данных SQLite с использованием Python, создавать таблицы, выполнять основные операции CRUD.

### Задачи:
1. Создать базу данных SQLite
2. Создать таблицы с различными типами данных
3. Выполнить операции вставки, чтения, обновления и удаления данных
4. Выполнить простые SQL-запросы

### План работы:
1. Подключение к базе данных
2. Создание таблиц
3. Вставка данных
4. Выборка данных
5. Обновление и удаление данных
6. Практические задания

---

## 1. Подключение к базе данных

### Пример 1: Подключение к SQLite

```python
import sqlite3

# Подключение к базе данных (создаст файл, если не существует)
conn = sqlite3.connect('university.db')

# Создание курсора
cursor = conn.cursor()

print("Подключение к базе данных успешно установлено")

# Закрытие соединения
conn.close()
```

### Пример 2: Использование контекстного менеджера

```python
import sqlite3

# Использование контекстного менеджера для автоматического закрытия соединения
with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Выполнение операций с базой данных
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()
    print(f"Версия SQLite: {version[0]}")
```

---

## 2. Создание таблиц

### Пример 3: Создание таблицы студентов

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Создание таблицы студентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date DATE,
            email TEXT UNIQUE,
            group_number TEXT,
            enrollment_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    print("Таблица students создана успешно")
```

### Пример 4: Создание связанных таблиц

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Создание таблицы преподавателей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT,
            hire_date DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Создание таблицы курсов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            credits INTEGER DEFAULT 3,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    
    # Создание таблицы оценок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            grade REAL,
            date_received DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    
    print("Связанные таблицы созданы успешно")
```

---

## 3. Вставка данных

### Пример 5: Вставка одиночной записи

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Вставка одного студента
    cursor.execute('''
        INSERT INTO students (first_name, last_name, birth_date, email, group_number)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Иван', 'Петров', '2000-05-15', 'ivan.petrov@email.com', 'CS-101'))
    
    student_id = cursor.lastrowid
    print(f"Студент добавлен с ID: {student_id}")
```

### Пример 6: Вставка нескольких записей

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Подготовка данных для вставки
    students_data = [
        ('Мария', 'Сидорова', '1999-11-22', 'maria.sidorova@email.com', 'CS-101'),
        ('Алексей', 'Кузнецов', '2001-03-10', 'alexey.kuznetsov@email.com', 'CS-102'),
        ('Елена', 'Волкова', '2000-08-30', 'elena.volkova@email.com', 'IT-101')
    ]
    
    # Вставка нескольких студентов
    cursor.executemany('''
        INSERT INTO students (first_name, last_name, birth_date, email, group_number)
        VALUES (?, ?, ?, ?, ?)
    ''', students_data)
    
    print(f"Добавлено {len(students_data)} студентов")
```

---

## 4. Выборка данных

### Пример 7: Простая выборка

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Выборка всех студентов
    cursor.execute("SELECT * FROM students")
    all_students = cursor.fetchall()
    
    print("Все студенты:")
    for student in all_students:
        print(student)
    
    # Выборка с условием
    cursor.execute("SELECT * FROM students WHERE group_number = ?", ('CS-101',))
    cs_students = cursor.fetchall()
    
    print("\nСтуденты группы CS-101:")
    for student in cs_students:
        print(f"{student[1]} {student[2]}, email: {student[4]}")
```

### Пример 8: Выборка с сортировкой и ограничением

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Выборка с сортировкой
    cursor.execute("SELECT first_name, last_name FROM students ORDER BY last_name ASC")
    sorted_students = cursor.fetchall()
    
    print("Студенты по алфавиту:")
    for student in sorted_students:
        print(f"{student[0]} {student[1]}")
    
    # Выборка с ограничением количества
    cursor.execute("SELECT * FROM students LIMIT 2 OFFSET 1")
    limited_students = cursor.fetchall()
    
    print(f"\nОграниченная выборка (пропустить 1, взять 2):")
    for student in limited_students:
        print(f"{student[1]} {student[2]}")
```

---

## 5. Обновление и удаление данных

### Пример 9: Обновление данных

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Обновление email студента
    cursor.execute('''
        UPDATE students 
        SET group_number = ? 
        WHERE email = ?
    ''', ('CS-102', 'ivan.petrov@email.com'))
    
    print(f"Обновлено {cursor.rowcount} записей")
    
    # Проверка обновления
    cursor.execute("SELECT * FROM students WHERE email = ?", ('ivan.petrov@email.com',))
    updated_student = cursor.fetchone()
    print(f"Обновленный студент: {updated_student}")
```

### Пример 10: Удаление данных

```python
import sqlite3

with sqlite3.connect('university.db') as conn:
    cursor = conn.cursor()
    
    # Удаление студента по email
    cursor.execute("DELETE FROM students WHERE email = ?", ('elena.volkova@email.com',))
    
    print(f"Удалено {cursor.rowcount} записей")
    
    # Проверка удаления
    cursor.execute("SELECT COUNT(*) FROM students WHERE email = ?", ('elena.volkova@email.com',))
    count = cursor.fetchone()[0]
    print(f"Количество оставшихся студентов с этим email: {count}")
```

---

## 6. Практические задания

### Задание 1: Создание базы данных библиотеки
Создайте базу данных для библиотеки с таблицами:
- `books` (id, title, author, isbn, publication_year, genre)
- `readers` (id, first_name, last_name, email, registration_date)
- `loans` (id, book_id, reader_id, loan_date, return_date)

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 2: Заполнение базы данных
Добавьте несколько записей в каждую таблицу.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 3: Выборка с JOIN
Напишите запрос, который выводит список книг с именами читателей, которые их взяли.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 4: Агрегация данных
Напишите запрос, который показывает, сколько книг взял каждый читатель.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 5: Поиск и фильтрация
Найдите все книги определенного автора, опубликованные после 200 года.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## 7. Дополнительные задания

### Задание 6: Создание индексов
Создайте индексы для ускорения поиска по автору книги и фамилии читателя.

### Задание 7: Транзакции
Реализуйте транзакцию для выдачи книги читателю с проверкой наличия книги.

---

## Контрольные вопросы:
1. Какие преимущества предоставляет SQLite?
2. Какие типы данных поддерживаются в SQLite?
3. Как работает AUTOINCREMENT в SQLite?
4. Какие ограничения целостности можно применить?
5. В чем разница между fetchone(), fetchall() и fetchmany()?