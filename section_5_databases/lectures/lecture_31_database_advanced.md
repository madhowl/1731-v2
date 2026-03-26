# Лекция 31: Работа с базами данных - продвинутый уровень

## Оптимизация запросов, транзакции, индексы

### Цель лекции:
- Изучить продвинутые техники работы с базами данных
- Освоить оптимизацию SQL-запросов
- Понять работу транзакций и уровней изоляции
- Научиться использовать индексы эффективно
- Освоить пулы соединений и обработку больших данных

### План лекции:
1. Оптимизация запросов
2. Транзакции
3. Индексы
4. Пул соединений
5. Обработка больших объемов данных
6. Мониторинг и отладка
7. Чек-лист оптимизации

---

## 1. Оптимизация запросов

Оптимизация запросов — процесс улучшения производительности SQL-запросов путем изменения их структуры или настройки базы данных.

### Жизненный цикл SQL-запроса:

```mermaid
flowchart TD
    A[SQL запрос] --> B[Parser<br/>Синтаксический анализ]
    B --> C[Rewriter<br/>Оптимизация правил]
    C --> D[Query Planner<br/>Генерация планов]
    D --> E{Cost-Based<br/>Optimizer}
    E -->|Выбор лучшего| F[План выполнения]
    F --> G[Executor<br/>Выполнение плана]
    G --> H{Тип доступа}
    H -->|Индекс| I[Index Scan<br/>Быстро]
    H -->|Без индекса| J[Full Table Scan<br/>Медленно]
    I --> K[Результат]
    J --> K
    
    style D fill:#fff9c4
    style E fill:#e1f5fe
    style I fill:#a5d6a7
    style J fill:#ef9a9a
```

### Основные проблемы производительности:

| Проблема | Описание | Решение |
|----------|----------|---------|
| **Неэффективные JOIN'ы** | Слишком много соединений таблиц | Оптимизировать структуру запроса |
| **Отсутствие индексов** | Медленные операции поиска | Создать индексы на ключевых полях |
| **Неправильная фильтрация** | Фильтрация после загрузки | Фильтровать до JOIN |
| **Сложные подзапросы** | Выполнение для каждой строки | Заменить на JOIN |
| **SELECT *** | Загрузка лишних данных | Выбирать конкретные поля |
| **Функции в WHERE** | Блокируют использование индексов | Переписать условие |

### Примеры плохих и хороших запросов:

```sql
-- ❌ ПЛОХО: Функция в WHERE мешает индексу
SELECT * FROM users WHERE YEAR(birth_date) = 1990;

-- ✅ ХОРОШО: Диапазон дат позволяет использовать индекс
SELECT * FROM users
WHERE birth_date >= '1990-01-01' 
  AND birth_date < '1991-01-01';
```

```sql
-- ❌ ПЛОХО: Подзапрос выполняется для каждой строки (N+1)
SELECT u.name,
       (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count
FROM users u;

-- ✅ ХОРОШО: JOIN более эффективен
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

```sql
-- ❌ ПЛОХО: Загрузка всех данных
SELECT * FROM orders;

-- ✅ ХОРОШО: Ограничение и конкретные поля
SELECT id, user_id, total, created_at
FROM orders
WHERE created_at >= '2024-01-01'
LIMIT 100;
```

```sql
-- ❌ ПЛОХО: Фильтрация после JOIN
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.age > 25;

-- ✅ ХОРОШО: Фильтрация до JOIN
SELECT * FROM (
    SELECT * FROM users WHERE age > 25
) u
JOIN orders o ON u.id = o.user_id;
```

### Анализ выполнения запросов:

```sql
-- PostgreSQL: Подробный анализ с фактическим выполнением
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE age > 25;

-- MySQL: Форматированный вывод
EXPLAIN FORMAT=JSON 
SELECT * FROM users WHERE age > 25;

-- SQLite: План запроса
EXPLAIN QUERY PLAN 
SELECT * FROM users WHERE age > 25;
```

### Пример вывода EXPLAIN (PostgreSQL):

```sql
EXPLAIN ANALYZE 
SELECT u.name, COUNT(o.id) 
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.age > 25
GROUP BY u.name;
```

```
QUERY PLAN
--------------------------------------------------------------------------------
HashAggregate  (cost=200.50..250.75 rows=1000 width=40) (actual time=15.2ms)
  Group Key: u.name
  ->  Hash Join  (cost=50.00..180.25 rows=5000 width=32) (actual time=2.1ms)
        Hash Cond: (o.user_id = u.id)
        ->  Seq Scan on orders o  (cost=0.00..120.00 rows=10000 width=16)
              (actual time=0.5ms)
        ->  Hash  (cost=40.00..40.00 rows=800 width=16) (actual time=1.2ms)
              ->  Index Scan using idx_users_age on users u  
                    (cost=0.25..40.00 rows=800 width=16) (actual time=0.8ms)
                    Index Cond: (age > 25)
Planning Time: 0.5ms
Execution Time: 16.8ms
```

### Ключевые метрики для анализа:

| Метрика | Описание | Хорошо |
|---------|----------|--------|
| **Seq Scan** | Полное сканирование таблицы | Избегать для больших таблиц |
| **Index Scan** | Сканирование по индексу | ✅ Предпочтительно |
| **Index Only Scan** | Только по индексу (без таблицы) | ✅✅ Оптимально |
| **Bitmap Heap Scan** | Сканирование по битовой карте | Хорошо для нескольких условий |
| **Nested Loop** | Вложенные циклы | Плохо для больших наборов |
| **Hash Join** | Хэш-соединение | Хорошо для средних таблиц |
| **Merge Join** | Слияние отсортированных | Хорошо для больших таблиц |

---

## 2. Транзакции

Транзакция — последовательность операций с базой данных, рассматриваемая как единое целое.

### ACID-свойства транзакций:

```mermaid
graph TB
    A[ACID] --> B[Atomicity<br/>Атомарность<br/>Все или ничего]
    A --> C[Consistency<br/>Согласованность<br/>Целостность данных]
    A --> D[Isolation<br/>Изоляция<br/>Независимость]
    A --> E[Durability<br/>Долговечность<br/>Сохранение]
    
    B --> B1[✅ COMMIT<br/>❌ ROLLBACK]
    C --> C1[✅ Ограничения БД<br/>✅ Триггеры]
    D --> D1[✅ Уровни изоляции]
    E --> E1[✅ Write-ahead log<br/>✅ Синхронизация]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#fff9c4
```

### Подробное описание ACID:

| Свойство | Описание | Реализация |
|----------|----------|------------|
| **Atomicity** | Транзакция выполняется полностью или не выполняется вообще | Журнал транзакций, rollback segments |
| **Consistency** | Транзакция переводит БД из одного согласованного состояния в другое | Ограничения, триггеры, каскады |
| **Isolation** | Параллельные транзакции не влияют друг на друга | Блокировки, MVCC |
| **Durability** | Результаты выполненной транзакции сохраняются навсегда | Write-ahead log, синхронизация на диск |

### Уровни изоляции транзакций:

```mermaid
graph TD
    subgraph "Матрица уровней изоляции"
        direction TB
        L1[READ UNCOMMITTED<br/>❌ Грязное чтение<br/>❌ Неповторяемое<br/>❌ Фантомы]
        L2[READ COMMITTED<br/>✅ Грязное чтение<br/>❌ Неповторяемое<br/>❌ Фантомы]
        L3[REPEATABLE READ<br/>✅ Грязное чтение<br/>✅ Неповторяемое<br/>❌ Фантомы]
        L4[SERIALIZABLE<br/>✅ Грязное чтение<br/>✅ Неповторяемое<br/>✅ Фантомы]
    end
    
    style L1 fill:#ffcc80
    style L2 fill:#fff9c4
    style L3 fill:#e1f5fe
    style L4 fill:#a5d6a7
```

### Проблемы параллельного доступа:

```mermaid
sequenceDiagram
    participant T1 as Транзакция 1
    participant DB as База данных
    participant T2 as Транзакция 2
    
    Note over T1,T2: "Грязное" чтение (Dirty Read)
    T1->>DB: UPDATE accounts SET balance=100
    T2->>DB: SELECT balance → 100 ❌
    T1->>DB: ROLLBACK
    T2-->>T2: Читает отменённые данные
    
    Note over T1,T2: Неповторяемое чтение (Non-repeatable Read)
    T1->>DB: SELECT balance → 50
    T2->>DB: UPDATE accounts SET balance=100
    T2->>DB: COMMIT
    T1->>DB: SELECT balance → 100 ❌
    
    Note over T1,T2: Фантомное чтение (Phantom Read)
    T1->>DB: SELECT COUNT(*) → 10
    T2->>DB: INSERT INTO accounts VALUES(...)
    T2->>DB: COMMIT
    T1->>DB: SELECT COUNT(*) → 11 ❌
    
    Note over T1,T2: Потерянное обновление (Lost Update)
    T1->>DB: SELECT balance → 100
    T2->>DB: SELECT balance → 100
    T1->>DB: UPDATE balance=150
    T1->>DB: COMMIT
    T2->>DB: UPDATE balance=120
    T2->>DB: COMMIT
    T1-->>T2: balance=120 (изменение T1 потеряно) ❌
    
```

### Транзакции в sqlite3:

```python
import sqlite3

conn = sqlite3.connect('bank.db')

try:
    # Явное начало транзакции
    conn.execute('BEGIN')

    # Снятие денег со счета
    conn.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (100, 1)
    )

    # Зачисление денег на другой счет
    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (100, 2)
    )

    conn.commit()  # Подтверждение транзакции
    print("✅ Перевод успешно выполнен")
    
except Exception as e:
    conn.rollback()  # Откат транзакции
    print(f"❌ Ошибка транзакции: {e}")
    
finally:
    conn.close()
```

### Транзакции в SQLAlchemy:

```python
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bank.db')
Session = sessionmaker(bind=engine)

# Способ 1: Явное управление
session = Session()
try:
    session.begin()  # Начало транзакции

    # Выполнение операций
    user = User(name="Иван", email="ivan@example.com")
    session.add(user)
    session.flush()  # Получение ID без коммита

    profile = UserProfile(user_id=user.id, bio="Новый пользователь")
    session.add(profile)

    session.commit()  # Подтверждение транзакции
    print("✅ Транзакция успешна")
    
except IntegrityError:
    session.rollback()  # Откат транзакции
    print("❌ Ошибка целостности данных")
    
finally:
    session.close()

# Способ 2: Контекстный менеджер (рекомендуется)
with Session() as session:
    try:
        user = User(name="Петр", email="petr@example.com")
        session.add(user)
        session.commit()
    except Exception:
        session.rollback()
        raise
```

### Установка уровня изоляции:

```python
# SQLite
conn.isolation_level = 'DEFERRED'  # По умолчанию
conn.isolation_level = 'IMMEDIATE'
conn.isolation_level = 'EXCLUSIVE'

# PostgreSQL через SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    isolation_level='READ COMMITTED'  # или 'REPEATABLE READ', 'SERIALIZABLE'
)

# Выполнение с конкретным уровнем изоляции
with engine.connect() as conn:
    conn.execution_options(isolation_level='SERIALIZABLE')
    # ... работа с БД
```

---

## 3. Индексы

Индекс — структура данных, позволяющая быстро находить записи в таблице.

### Структура B-tree индекса:

```mermaid
graph TD
    A[Root Node<br/>50] --> B[Internal<br/>25]
    A --> C[Internal<br/>75]
    
    B --> D[Leaf<br/>10]
    B --> E[Leaf<br/>35]
    
    C --> F[Leaf<br/>60]
    C --> G[Leaf<br/>90]
    
    D --> H[📄 Row 10]
    E --> I[📄 Row 35]
    F --> J[📄 Row 60]
    G --> K[📄 Row 90]
    
    style A fill:#e1f5fe,stroke:#0277bd
    style B fill:#fff3e0,stroke:#ef6c00
    style C fill:#fff3e0,stroke:#ef6c00
    style H fill:#a5d6a7,stroke:#2e7d32
    style I fill:#a5d6a7,stroke:#2e7d32
    style J fill:#a5d6a7,stroke:#2e7d32
    style K fill:#a5d6a7,stroke:#2e7d32
```

### Как работает поиск по B-tree:

```mermaid
flowchart LR
    Start([Поиск 35]) --> Root{Root: 50}
    Root -->|35 < 50| Left{Left: 25}
    Root -->|35 > 50| Right[Right: 75]
    
    Left -->|35 > 25| RightLeaf[Leaf: 35]
    Left -->|35 < 25| LeftLeaf[Leaf: 10]
    
    RightLeaf --> Found[✅ Найдено!]
    LeftLeaf --> NotFound[❌ Не найдено]
    
    style Start fill:#90caf9
    style Found fill:#a5d6a7
    style NotFound fill:#ef9a9a
```

### Типы индексов:

| Тип | Описание | Когда использовать |
|-----|----------|-------------------|
| **B-tree** | Сбалансированное дерево | По умолчанию, для =, <, >, BETWEEN, LIKE 'prefix%' |
| **Hash** | Хэш-таблица | Только для = (точное совпадение) |
| **GiST** | Обобщенное дерево поиска | Для геоданных, полнотекстового поиска |
| **GIN** | Обобщенный инвертированный индекс | Для массивов, JSON, полнотекстового поиска |
| **BRIN** | Блочный диапазон | Для больших отсортированных таблиц |
| **Bitmap** | Битовые карты | Для полей с низкой кардинальностью |

### Создание индексов:

```sql
-- Простой индекс на одном поле
CREATE INDEX idx_users_email ON users(email);

-- Композитный индекс (несколько полей)
-- Порядок полей важен!
CREATE INDEX idx_users_name_age ON users(name, age);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Частичный индекс (только для активных пользователей)
CREATE INDEX idx_active_users_email 
ON users(email) 
WHERE active = true;

-- Функциональный индекс
CREATE INDEX idx_users_lower_email 
ON users(LOWER(email));

-- Индекс для LIKE с wildcard в начале (PostgreSQL)
CREATE INDEX idx_users_name_trgm ON users USING gin (name gin_trgm_ops);
```

### Когда использовать индексы:

```mermaid
flowchart TD
    Start([Нужен ли индекс?]) --> Where{Используется<br/>в WHERE?}
    Where -->|Да| Create[✅ Создать индекс]
    Where -->|Нет| Join{Используется<br/>в JOIN?}
    
    Join -->|Да| Create
    Join -->|Нет| Order{Используется<br/>в ORDER BY?}
    
    Order -->|Да| Create
    Order -->|Нет| NoIndex[❌ Индекс не нужен]
    
    Create --> Selective{Высокая<br/>селективность?}
    Selective -->|Да| Final[✅ Создавать]
    Selective -->|Нет| CheckSize{Таблица<br/>большая?}
    
    CheckSize -->|Да| Final
    CheckSize -->|Нет| NoIndex
    
    style Final fill:#a5d6a7
    style NoIndex fill:#ef9a9a
```

### Когда НЕ использовать индексы:

```sql
-- ❌ Поля с низкой селективностью
CREATE INDEX idx_users_gender ON users(gender);  -- Только 2-3 значения

-- ❌ Часто изменяемые таблицы
-- Индексы замедляют INSERT, UPDATE, DELETE

-- ❌ Маленькие таблицы (< 1000 строк)
-- Полное сканирование может быть быстрее

-- ❌ Поля, используемые только с функциями
CREATE INDEX idx_users_year ON users(YEAR(birth_date));  -- Не будет использоваться
```

### Проверка использования индексов:

```sql
-- PostgreSQL: Статистика использования индексов
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- PostgreSQL: Размер индексов
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes
WHERE schemaname = 'public';

-- Удаление неиспользуемых индексов
DROP INDEX IF EXISTS idx_unused_column;

-- Переиндексация (для улучшения производительности)
REINDEX TABLE users;  -- PostgreSQL
OPTIMIZE TABLE users;  -- MySQL
```

### Композитные индексы:

```sql
-- Порядок полей в композитном индексе важен!
CREATE INDEX idx_users_name_age ON users(name, age);

-- ✅ Будет использоваться для:
SELECT * FROM users WHERE name = 'Иван';           -- Использует индекс
SELECT * FROM users WHERE name = 'Иван' AND age > 25;  -- Использует индекс
SELECT * FROM users ORDER BY name, age;            -- Использует индекс

-- ❌ НЕ будет использоваться для:
SELECT * FROM users WHERE age > 25;                -- Не использует индекс
SELECT * FROM users WHERE age > 25 AND name = 'Иван';  -- Может не использовать
```

---

## 4. Пул соединений

Пул соединений — кэш соединений с базой данных, которые могут повторно использоваться.

### Архитектура пула соединений:

```mermaid
graph TB
    subgraph "Приложение"
        T1[Thread 1]
        T2[Thread 2]
        T3[Thread 3]
        TN[Thread N]
    end
    
    subgraph "Connection Pool"
        direction TB
        Active[Active Connections<br/>В использовании: 1-5]
        Idle[Idle Connections<br/>Свободные: 6-10]
        Overflow[Overflow<br/>Переполнение: 11-15]
    end
    
    subgraph "База данных"
        DB[(PostgreSQL<br/>Max: 100)]
    end
    
    T1 --> Active
    T2 --> Idle
    T3 --> Active
    TN --> Overflow
    
    Active --> DB
    Idle --> DB
    Overflow --> DB
    
    style Active fill:#a5d6a7
    style Idle fill:#fff9c4
    style Overflow fill:#ffcc80
    style DB fill:#e1f5fe
```

### Жизненный цикл соединения в пуле:

```mermaid
flowchart TD
    Start([Запрос соединения]) --> Pool{Есть<br/>свободные?}
    Pool -->|Да| Idle[Взять из Idle]
    Pool -->|Нет| Max{Достигнут<br/>max_overflow?}
    
    Max -->|Нет| Create[Создать новое]
    Max -->|Да| Wait[Ждать в очереди]
    
    Wait --> Timeout{Timeout?<br/>30 сек}
    Timeout -->|Да| Error[❌ Ошибка]
    Timeout -->|Нет| Wait
    
    Idle --> Use[Использование]
    Create --> Use
    
    Use --> Return[Вернуть в пул]
    Return --> Check{Проверка<br/>соединения}
    Check -->|OK| Idle
    Check -->|Ошибка| Recreate[Пересоздать]
    Recreate --> Idle
    
    style Start fill:#90caf9
    style Error fill:#ef9a9a
    style Idle fill:#a5d6a7
```

### Настройка пула в SQLAlchemy:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

# Рекомендуемая конфигурация для продакшена
engine = create_engine(
    'postgresql://user:password@localhost:5432/dbname',
    
    # Класс пула
    poolclass=QueuePool,
    
    # Размер пула (постоянные соединения)
    pool_size=10,
    
    # Максимум дополнительных соединений
    max_overflow=20,
    
    # Время жизни соединения (секунды)
    pool_recycle=3600,
    
    # Проверка перед использованием
    pool_pre_ping=True,
    
    # Таймаут ожидания из пула
    pool_timeout=30,
    
    # Логирование
    echo=False,
)

# Типы пулов:
# QueuePool - пул с очередью (по умолчанию для PostgreSQL/MySQL)
# NullPool - без пула (каждый раз новое соединение)
# StaticPool - статический пул (для тестов)
# SingletonThreadPool - одно соединение на поток (для SQLite)
```

### Параметры пула:

| Параметр | Описание | Рекомендуемое значение |
|----------|----------|----------------------|
| `pool_size` | Количество постоянных соединений | 10-20 |
| `max_overflow` | Дополнительные соединения | 10-20 |
| `pool_recycle` | Пересоздание через N секунд | 3600 (1 час) |
| `pool_pre_ping` | Проверка перед использованием | True |
| `pool_timeout` | Таймаут ожидания | 30 секунд |

### Пример использования:

```python
from sqlalchemy.orm import sessionmaker, scoped_session

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

# Потокобезопасная сессия
SessionScoped = scoped_session(Session)

# Правильное использование сессии
def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()  # Возврат соединения в пул

# Использование scoped_session
def get_user_scoped(user_id):
    try:
        user = SessionScoped.query(User).filter(User.id == user_id).first()
        return user
    finally:
        SessionScoped.remove()  # Возврат соединения в пул
```

### Мониторинг пула:

```python
from sqlalchemy import event

# Логирование событий пула
@event.listens_for(engine, 'connect')
def on_connect(dbapi_conn, connection_record):
    print("✅ Новое соединение создано")

@event.listens_for(engine, 'checkout')
def on_checkout(dbapi_conn, connection_record, connection_proxy):
    print("🔌 Соединение взято из пула")

@event.listens_for(engine, 'checkin')
def on_checkin(dbapi_conn, connection_record):
    print("🔌 Соединение возвращено в пул")

# Статистика пула
pool = engine.pool
print(f"Размер пула: {pool.size()}")
print(f"Проверено: {pool.checkedout()}")
print(f"Свободно: {pool.checkedin()}")
print(f"Переполнение: {pool.overflow()}")
```

---

## 5. Обработка больших объемов данных

### Пакетная обработка:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///large_db.db')
Session = sessionmaker(bind=engine)

def batch_process_users(batch_size=1000):
    """Обработка пользователей пакетами"""
    session = Session()
    try:
        offset = 0
        processed = 0
        
        while True:
            # Загрузка пакета
            users = session.query(User)\
                .filter(User.processed == False)\
                .offset(offset)\
                .limit(batch_size)\
                .all()
            
            if not users:
                break
            
            # Обработка пакета
            for user in users:
                user.processed = True
                user.processed_at = datetime.utcnow()
            
            # Сохранение изменений
            session.commit()
            
            processed += len(users)
            offset += batch_size
            print(f"Обработано: {processed}")
            
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
```

### Использование курсоров (server-side cursors):

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Для PostgreSQL: name required for server-side cursor
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    execution_options={'stream_results': True}
)

# Обработка миллионов строк без загрузки в память
def process_large_table():
    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(
            text("SELECT * FROM large_table")
        )
        
        for row in result:
            # Обработка одной строки
            process_row(row)
```

### Yield для ленивой загрузки:

```python
def fetch_users_batched(session, batch_size=1000):
    """Генератор для ленивой загрузки"""
    offset = 0
    while True:
        users = session.query(User)\
            .offset(offset)\
            .limit(batch_size)\
            .yield_per(batch_size)\
            .all()
        
        if not users:
            break
            
        for user in users:
            yield user
            
        offset += batch_size

# Использование
for user in fetch_users_batched(session):
    process_user(user)
```

### Оптимизация для больших таблиц:

```sql
-- Партицирование таблиц (PostgreSQL 10+)
CREATE TABLE measurements (
    city_id int,
    logdate date,
    peaktemp int,
    unitsales int
) PARTITION BY RANGE (logdate);

CREATE TABLE measurements_2024_q1 
    PARTITION OF measurements
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Материализованные представления
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    user_id,
    COUNT(*) as order_count,
    SUM(total) as total_spent
FROM orders
GROUP BY user_id;

-- Обновление материализованного представления
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

---

## 6. Мониторинг и отладка

### Логирование медленных запросов:

```python
from sqlalchemy import event
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sql_performance')

@event.listens_for(engine, 'before_cursor_execute')
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    
    # Логирование запросов дольше 1 секунды
    if total > 1.0:
        logger.warning(f"Медленный запрос: {total:.3f}s")
        logger.warning(f"SQL: {statement}")
        logger.warning(f"Parameters: {parameters}")
```

### Профилирование запросов:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

class QueryProfiler:
    def __init__(self, engine):
        self.engine = engine
        self.queries = []
        
    @contextmanager
    def profile(self, name="Query"):
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            self.queries.append({
                'name': name,
                'time': elapsed
            })
            print(f"{name}: {elapsed:.3f}s")
    
    def report(self):
        print("\n=== Отчёт профилирования ===")
        for q in sorted(self.queries, key=lambda x: x['time'], reverse=True):
            print(f"{q['name']}: {q['time']:.3f}s")

# Использование
profiler = QueryProfiler(engine)

with profiler.profile("Загрузка пользователей"):
    users = session.query(User).all()

with profiler.profile("Загрузка заказов"):
    orders = session.query(Order).all()

profiler.report()
```

---

## 7. Чек-лист оптимизации

### Контрольный список оптимизации БД:

```mermaid
flowchart TD
    Start([Оптимизация БД]) --> Indexes{Индексы<br/>созданы?}
    Indexes -->|Нет| CreateIdx[Создать индексы]
    Indexes -->|Да| Queries{Запросы<br/>оптимизированы?}
    
    Queries -->|Нет| OptQueries[Оптимизировать запросы]
    Queries -->|Да| Connections{Пул<br/>настроен?}
    
    Connections -->|Нет| ConfigPool[Настроить пул]
    Connections -->|Да| Analyze{EXPLAIN<br/>проверен?}
    
    Analyze -->|Нет| RunExplain[Запустить EXPLAIN]
    Analyze -->|Да| Monitor{Мониторинг<br/>настроен?}
    
    Monitor -->|Нет| SetupMon[Настроить мониторинг]
    Monitor -->|Да| Done[✅ Оптимизация завершена]
    
    style CreateIdx fill:#e1f5fe
    style OptQueries fill:#fff3e0
    style ConfigPool fill:#f3e5f5
    style RunExplain fill:#e8f5e9
    style SetupMon fill:#fff9c4
    style Done fill:#a5d6a7
```

### Чек-лист для проверки:

- [ ] **Индексы**: Созданы на полях WHERE, JOIN, ORDER BY
- [ ] **Запросы**: Используются конкретные поля вместо SELECT *
- [ ] **Функции в WHERE**: Убраны функции из условий WHERE
- [ ] **Подзапросы**: Заменены на JOIN где возможно
- [ ] **Пул соединений**: Настроен pool_size и max_overflow
- [ ] **Транзакции**: Короткие транзакции, правильный уровень изоляции
- [ ] **EXPLAIN**: Проверены планы выполнения критичных запросов
- [ ] **Мониторинг**: Настроено логирование медленных запросов
- [ ] **Бэкапы**: Настроено регулярное резервное копирование
- [ ] **VACUUM/ANALYZE**: Выполняется регулярно (PostgreSQL)

---

## Контрольные вопросы:

1. Что такое EXPLAIN и как его использовать для оптимизации?
2. Какие проблемы параллельного доступа вы знаете?
3. Чем отличаются уровни изоляции транзакций?
4. Как работает B-tree индекс и когда его использовать?
5. Что такое композитный индекс и важен ли порядок полей?
6. Зачем нужен пул соединений и как его настроить?
7. Какие существуют типы индексов в PostgreSQL?
8. Как обрабатывать большие объемы данных эффективно?

---
