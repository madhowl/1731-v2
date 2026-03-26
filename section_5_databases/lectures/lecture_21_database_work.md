# Лекция 21: Работа с базами данных

## Введение в SQL, модуль sqlite3, основные команды SQL

### Цель лекции:
- Познакомиться с основами работы с базами данных
- Изучить модуль sqlite3 в Python
- Освоить основные команды SQL
- Понять архитектуру работы с БД в Python

### План лекции:
1. Введение в базы данных
2. Модуль sqlite3 и архитектура работы
3. Основные команды SQL
4. Работа с базой данных в Python
5. Архитектура работы с БД в Python
6. Лучшие практики

---

## 1. Введение в базы данных

База данных — организованная коллекция структурированных записей или данных, обычно хранимая в компьютерной системе.

### Типы баз данных:

```mermaid
graph TD
    A[Базы данных] --> B[Реляционные SQL]
    A --> C[Нереляционные NoSQL]
    
    B --> B1[SQLite]
    B --> B2[MySQL]
    B --> B3[PostgreSQL]
    B --> B4[Oracle]
    B --> B5[MS SQL Server]
    
    C --> C1[Документные MongoDB]
    C --> C2[Ключ-значение Redis]
    C --> C3[Колоночные Cassandra]
    C --> C4[Графовые Neo4j]
```

### Реляционные базы данных:
- Данные организованы в **таблицы** со строками и столбцами
- Используют язык **SQL** (Structured Query Language)
- Связи между таблицами через ключи
- Гарантируют **ACID**-транзакции:
  - **A**tomicity (Атомарность)
  - **C**onsistency (Согласованность)
  - **I**solation (Изоляция)
  - **D**urability (Долговечность)

### Архитектура клиент-сервер:

```mermaid
graph LR
    A[Клиент<br/>Python-приложение] -->|SQL-запросы| B[Сервер БД]
    B -->|Результаты| A
    B --> C[Файлы данных]
    
    subgraph "Ваш компьютер"
        A
    end
    
    subgraph "Сервер БД"
        B
        C
    end
```

> **Примечание:** SQLite работает **без сервера** — это встроенная библиотека, которая читает/пишет напрямую в файл.

### Основные понятия:
| Термин | Описание |
|--------|----------|
| **Таблица** | Коллекция связанных данных (как лист Excel) |
| **Строка (запись)** | Одна запись в таблице |
| **Столбец (поле)** | Атрибут данных (например, `name`, `age`) |
| **Первичный ключ** | Уникальный идентификатор строки (`PRIMARY KEY`) |
| **Внешний ключ** | Ссылка на первичный ключ другой таблицы (`FOREIGN KEY`) |
| **Индекс** | Структура для ускорения поиска данных |

---

## 2. Модуль sqlite3 и архитектура работы

SQLite — встроенная в Python реляционная база данных, не требующая отдельного сервера.

### Архитектура sqlite3:

```mermaid
graph TD
    A[Ваш Python-код] --> B[sqlite3.connect]
    B --> C[Connection<br/>Объект соединения]
    C --> D[conn.cursor]
    D --> E[Cursor<br/>Объект курсора]
    E --> F[SQLite Engine<br/>Движок БД]
    F --> G[Файл .db<br/>Хранилище данных]
    
    style C fill:#e1f5fe
    style E fill:#fff3e0
    style G fill:#f3e5f5
```

### Что такое `cursor = conn.cursor()`?

**`Connection` (соединение)** — это канал связи с базой данных:
- Управляет подключением к БД
- Контролирует транзакции (`commit()`, `rollback()`)
- Может создавать несколько курсоров

**`Cursor` (курсор)** — это объект для выполнения SQL-команд:
- Выполняет SQL-запросы через `execute()`
- Хранит состояние текущего запроса
- Содержит результаты выполнения
- Позволяет итерироваться по результатам

### Почему нужны оба объекта?

```mermaid
classDiagram
    class Connection {
        +connect(database: str)
        +cursor() Cursor
        +commit()
        +rollback()
        +close()
        +total_changes: int
    }
    
    class Cursor {
        +execute(sql: str, params: tuple)
        +executemany(sql: str, params: list)
        +fetchone() tuple
        +fetchall() list
        +fetchmany(size: int) list
        +description: tuple
        +rowcount: int
        +lastrowid: int
        +close()
    }
    
    class ResultSet {
        <<результат запроса>>
        +строки данных
    }
    
    Connection --> Cursor : создаёт курсор
    Cursor --> ResultSet : хранит результат
```

### Жизненный цикл соединения:

```mermaid
flowchart TD
    Start([Начало]) --> Connect[sqlite3.connect<br/>Создание Connection]
    Connect --> CreateCursor[conn.cursor<br/>Создание Cursor]
    CreateCursor --> Execute[cursor.execute<br/>Выполнение SQL]
    
    Execute --> IsSelect{SELECT запрос?}
    IsSelect -->|Да| Fetch[Получение данных<br/>fetchone/fetchall]
    IsSelect -->|Нет| SkipFetch[Пропуск выборки]
    
    Fetch --> Commit[conn.commit<br/>Сохранение изменений]
    SkipFetch --> Commit
    
    Commit --> CloseCursor[Закрытие курсора]
    CloseCursor --> CloseConn[Закрытие соединения]
    CloseConn --> End([Конец])
    
    style Start fill:#a5d6a7
    style End fill:#ef9a9a
    style Commit fill:#fff9c4
```

### Подключение к базе данных:

```python
import sqlite3

# Подключение к базе данных (создаст файл, если не существует)
conn = sqlite3.connect('example.db')

# Создание курсора для выполнения запросов
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
conn.commit()  # Сохранение изменений (транзакция)
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

### Типы данных в SQLite:

| Тип | Описание |
|-----|----------|
| `INTEGER` | Целые числа |
| `REAL` | Числа с плавающей точкой |
| `TEXT` | Строковый текст |
| `BLOB` | Бинарные данные |
| `NULL` | Отсутствие значения |

### INSERT - добавление данных:

```sql
INSERT INTO employees (name, position, salary)
VALUES ('Иван Иванов', 'Программист', 75000);
```

### SELECT - выборка данных:

```sql
-- Все записи
SELECT * FROM employees;

-- Выборка с условием
SELECT name, salary FROM employees WHERE salary > 50000;

-- Сортировка и ограничение
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
-- Одиночное условие
SELECT * FROM employees WHERE position = 'Программист';

-- Несколько условий (AND)
SELECT * FROM employees WHERE position = 'Программист' AND salary > 60000;

-- Несколько условий (OR)
SELECT * FROM employees WHERE position = 'Программист' OR position = 'Тестировщик';

-- LIKE - поиск по шаблону
SELECT * FROM employees WHERE name LIKE 'Иван%';
```

---

## 4. Работа с базой данных в Python

### Схема потока данных при выполнении запроса:

```mermaid
sequenceDiagram
    participant Dev as Разработчик
    participant Code as Python-код
    participant Conn as Connection
    participant Cursor as Cursor
    participant DB as SQLite DB
    participant File as Файл .db

    Dev->>Code: Пишет запрос
    Code->>Conn: connect('example.db')
    activate Conn
    Conn->>File: Открытие/создание
    File-->>Conn: Подключение готово
    
    Code->>Cursor: cursor()
    activate Cursor
    Cursor-->>Code: Курсор готов
    
    Code->>Cursor: execute(sql, params)
    Cursor->>DB: Парсинг SQL
    DB->>File: Чтение/запись
    File-->>DB: Данные
    DB-->>Cursor: Результат
    
    Code->>Cursor: fetchall() / fetchone()
    Cursor-->>Code: Данные Python
    
    Code->>Conn: commit()
    Conn->>File: Сохранение транзакции
    
    Code->>Cursor: close()
    deactivate Cursor
    Code->>Conn: close()
    deactivate Conn
```

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
    conn.commit()  # Обязательно сохраняем изменения!
```

### Выборка данных:

```python
with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()

    # Выборка всех записей
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()  # Возвращает список кортежей

    for row in rows:
        print(row)  # (id, name, email, age)

    # Выборка одной записи
    cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
    row = cursor.fetchone()  # Возвращает один кортеж или None
    print(row)
    
    # Выборка нескольких записей
    cursor.execute("SELECT * FROM users")
    five_rows = cursor.fetchmany(5)  # Возвращает N записей
```

### Методы получения данных из курсора:

| Метод | Описание | Возвращает |
|-------|----------|------------|
| `fetchone()` | Получить одну строку | `tuple` или `None` |
| `fetchall()` | Получить все строки | `list[tuple]` |
| `fetchmany(n)` | Получить N строк | `list[tuple]` |
| Итерация | `for row in cursor:` | Итератор по строкам |

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
conn.commit()
```

### Обработка ошибок:

```python
import sqlite3

try:
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                      ("Тест", "test@example.com"))
        conn.commit()
        
except sqlite3.IntegrityError as e:
    print(f"Ошибка целостности: {e}")  # Нарушение UNIQUE, NOT NULL
except sqlite3.OperationalError as e:
    print(f"Ошибка операции: {e}")  # Таблица не существует и т.д.
except sqlite3.DatabaseError as e:
    print(f"Ошибка БД: {e}")  # Общая ошибка базы данных
```

---

## 5. Архитектура работы с БД в Python

### Полная схема взаимодействия компонентов:

```mermaid
graph TB
    subgraph "Уровень приложения"
        A[Python-код]
    end
    
    subgraph "sqlite3 модуль"
        B[Connection<br/>Соединение]
        C[Cursor 1]
        D[Cursor 2]
        E[Cursor N]
    end
    
    subgraph "SQLite движок"
        F[SQL Parser]
        G[Query Executor]
        H[Transaction Manager]
    end
    
    subgraph "Хранилище"
        I[Файл .db]
        J[Страницы данных]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    
    C --> F
    D --> F
    E --> F
    
    F --> G
    G --> H
    H --> I
    I --> J
    
    style B fill:#e1f5fe
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#fff3e0
    style H fill:#f3e5f5
```

### Транзакции в SQLite:

```mermaid
flowchart LR
    Start([Начало<br/>транзакции]) --> Ops[SQL операции<br/>INSERT/UPDATE/DELETE]
    Ops --> Decision{Результат?}
    Decision -->|Успех| Commit[COMMIT<br/>Сохранить]
    Decision -->|Ошибка| Rollback[ROLLBACK<br/>Отменить]
    Commit --> End([Конец])
    Rollback --> End
    
    style Start fill:#a5d6a7
    style Commit fill:#a5d6a7
    style Rollback fill:#ef9a9a
    style End fill:#90caf9
```

### Пример работы с транзакциями:

```python
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

try:
    # Начало транзакции (автоматически при первой операции)
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    
    # Если всё успешно - сохраняем
    conn.commit()
    print("Перевод выполнен успешно")
    
except Exception as e:
    # При ошибке - откатываем все изменения
    conn.rollback()
    print(f"Ошибка перевода: {e}")
    
finally:
    conn.close()
```

---

## 6. Лучшие практики

### 1. Управление соединениями:

```python
# ✅ ХОРОШО: Использование контекстного менеджера
with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # conn.close() вызывается автоматически

# ❌ ПЛОХО: Ручное управление без finally
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
conn.close()  # Может не вызваться при ошибке
```

### 2. Безопасность (защита от SQL-инъекций):

```python
# ✅ ХОРОШО: Параметризованные запросы
cursor.execute(
    "SELECT * FROM users WHERE name = ?", 
    (user_input,)
)

# ❌ ПЛОХО: Конкатенация строк (уязвимость!)
cursor.execute(
    f"SELECT * FROM users WHERE name = '{user_input}'"
)
```

### Почему параметризованные запросы безопасны:

```mermaid
graph TD
    A[Параметризованный запрос] --> B[SQL и данные разделены]
    B --> C[SQLite обрабатывает данные как значения]
    C --> D[Невозможно внедрить SQL-код]
    
    E[Конкатенация строк] --> F[SQL и данные смешаны]
    F --> G[Злоумышленник может внедрить код]
    G --> H[SQL-инъекция успешна]
    
    style A fill:#a5d6a7
    style D fill:#a5d6a7
    style E fill:#ef9a9a
    style H fill:#ef9a9a
```

### 3. Производительность:

```python
# ✅ Использование индексов для частых запросов
cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

# ✅ Пакетная вставка данных
users_data = [(f"user{i}", f"user{i}@example.com") for i in range(1000)]
cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
conn.commit()

# ❌ Индивидуальная вставка (медленно)
for i in range(1000):
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                  (f"user{i}", f"user{i}@example.com"))
    conn.commit()  # commit после каждой записи!
```

### 4. Закрытие курсоров:

```python
# ✅ Явное закрытие при длительной работе
cursor = conn.cursor()
cursor.execute("SELECT * FROM large_table")
results = cursor.fetchall()
cursor.close()  # Освобождаем ресурсы

# Для коротких скриптов с контекстным менеджером
# курсор закроется автоматически с соединением
```

### 5. Чек-лист правильной работы с БД:

```mermaid
flowchart TD
    A[Начало работы с БД] --> B{Контекстный<br/>менеджер?}
    B -->|Да| C[with sqlite3.connect]
    B -->|Нет| D[try/finally блок]
    
    C --> E[Создать курсор]
    D --> E
    
    E --> F[Выполнить запросы]
    F --> G{Есть изменения?}
    
    G -->|Да| H[Вызвать commit]
    G -->|Нет| I[Пропустить commit]
    
    H --> J[Обработать ошибки]
    I --> J
    
    J --> K[Автоматическое<br/>закрытие]
    K --> L([Конец])
    
    style C fill:#a5d6a7
    style D fill:#a5d6a7
    style H fill:#fff9c4
    style L fill:#90caf9
```

---

## Контрольные вопросы:

1. В чём разница между `Connection` и `Cursor`?
2. Зачем нужен `commit()` и когда он не требуется?
3. Почему параметризованные запросы безопаснее конкатенации строк?
4. Что произойдёт, если не вызвать `commit()` после `INSERT`?
5. Как правильно обрабатывать ошибки при работе с БД?

---
