# Практическое занятие 42: Оптимизация производительности баз данных

## Индексы, профилирование запросов, кэширование

### Цель занятия:
Научиться оптимизировать производительность баз данных, использовать индексы и профилировать запросы.

### Задачи:
1. Понять принципы работы индексов
2. Научиться создавать и использовать индексы
3. Освоить профилирование SQL-запросов
4. Изучить стратегии кэширования
5. Научиться оптимизировать慢 запросы

### План работы:
1. Введение в оптимизацию
2. Индексы и их типы
3. Профилирование запросов
4. Оптимизация запросов
5. Кэширование
6. Практические задания

---

## 1. Введение в оптимизацию производительности

Оптимизация производительности баз данных — это процесс улучшения скорости выполнения запросов и операций с данными.

### Пример 1: Замер времени выполнения

```python
import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test_performance.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Создание тестовой таблицы
session.execute(text('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''))

# Заполнение тестовыми данными (10000 записей)
start = time.time()
for i in range(10000):
    session.execute(text('''
        INSERT INTO products (name, category, price, description)
        VALUES (:name, :category, :price, :desc)
    '''), {
        'name': f'Товар {i}',
        'category': f'Категория {i % 10}',
        'price': 100 + (i % 100),
        'description': f'Описание товара {i}' * 10
    })
session.commit()

end = time.time()
print(f"Время вставки 10000 записей: {end - start:.2f} секунд")
```

---

## 2. Индексы

Индекс — это структура данных, которая позволяет быстро находить записи по значениям одного или нескольких полей.

### Пример 2: Создание индексов

```python
from sqlalchemy import Index, ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(Float)
    description = Column(Text)
    created_at = Column(String)
    
    # Создание индексов
    __table_args__ = (
        # Простой индекс на поле category
        Index('idx_products_category', 'category'),
        
        # Простой индекс на поле price
        Index('idx_products_price', 'price'),
        
        # Композитный индекс (для часто используемых комбинаций)
        Index('idx_products_category_price', 'category', 'price'),
        
        # Уникальный индекс
        Index('idx_products_name', 'name', unique=True),
    )

# Создание таблицы с индексами
Base.metadata.create_all(engine)

print("Индексы созданы")
```

### Пример 3: Проверка использования индексов в SQLite

```python
# Анализ плана запроса в SQLite
query_plan = session.execute(text(
    "EXPLAIN QUERY PLAN SELECT * FROM products WHERE category = 'Категория 1'"
)).fetchall()

print("План запроса:")
for row in query_plan:
    print(row)

# Сравнение скорости с индексами и без
def benchmark_query(condition, description):
    start = time.time()
    result = session.execute(text(f"SELECT * FROM products WHERE {condition}")).fetchall()
    end = time.time()
    print(f"{description}: {len(result)} результатов за {end-start:.4f} сек")

# Запрос без индекса по name
benchmark_query("name = 'Товар 5000'", "Поиск по name (с индексом)")

# Запрос с индексом по category
benchmark_query("category = 'Категория 1'", "Поиск по category (с индексом)")

# Запрос с композитным индексом
benchmark_query("category = 'Категория 1' AND price > 150", 
                 "Поиск по category + price (с композитным индексом)")
```

### Пример 4: Удаление неиспользуемых индексов

```python
# Удаление индекса
session.execute(text("DROP INDEX IF EXISTS idx_products_category"))
session.commit()

# Просмотр всех индексов
indexes = session.execute(text(
    "SELECT name FROM sqlite_master WHERE type='index'"
)).fetchall()

print("Существующие индексы:")
for idx in indexes:
    print(f"  - {idx[0]}")
```

---

## 3. Профилирование запросов

Профилирование помогает понять, какие запросы выполняются медленно и почему.

### Пример 5: Логирование SQL-запросов

```python
import logging
import sys

# Настройка логирования SQL-запросов
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Перенаправление логов в файл
handler = logging.FileHandler('sql_queries.log')
handler.setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').addHandler(handler)

# Теперь все SQL-запросы будут записываться в файл

# Пример запроса
products = session.query(Product).filter(Product.price > 500).limit(10).all()

print("Запросы записаны в файл sql_queries.log")
```

### Пример 6: Профилирование с использованием времени

```python
def profile_query(query_func, description):
    """Профилирование функции запроса"""
    import time
    
    start = time.perf_counter()
    result = query_func()
    end = time.perf_counter()
    
    print(f"{description}: {end - start:.6f} сек")
    return result

# Профилирование разных способов запроса

# Способ 1: Простой фильтр
profile_query(
    lambda: session.query(Product).filter(Product.category == 'Категория 1').all(),
    "Простой фильтр"
)

# Способ 2: Фильтр с подзапросом
profile_query(
    lambda: session.query(Product).filter(
        Product.id.in_([p.id for p in session.query(Product.id).limit(100)])
    ).all(),
    "Подзапрос"
)

# Способ 3: Прямой SQL
profile_query(
    lambda: session.execute(text(
        "SELECT * FROM products WHERE category = 'Категория 1'"
    )).fetchall(),
    "Прямой SQL"
)
```

---

## 4. Оптимизация запросов

### Пример 7: Выбор только необходимых полей

```python
# Плохо: загрузка всех полей
start = time.time()
all_products = session.query(Product).all()
end = time.time()
print(f"Загрузка всех полей: {end - start:.4f} сек")

# Хорошо: выбор только нужных полей
start = time.time()
product_names = session.query(Product.name, Product.price).all()
end = time.time()
print(f"Выбор только нужных полей: {end - start:.4f} сек")

# Результат для примера (нужно много записей для наглядности)
# Использование load_only() в SQLAlchemy
start = time.time()
products = session.query(Product).options(
    from sqlalchemy.orm import load_only
).limit(1000).all()
end = time.time()
print(f"load_only(): {end - start:.4f} сек")
```

### Пример 8: Использование LIMIT и OFFSET

```python
# Плохо: загрузка всех записей для пагинации
all_products = session.query(Product).all()
page_size = 10
page = all_products[50:60]  # Неэффективно!

# Хорошо: использование LIMIT и OFFSET
page_size = 10
page_number = 6

start = time.time()
products = session.query(Product).limit(page_size).offset(
    (page_number - 1) * page_size
).all()
end = time.time()
print(f"Пагинация с LIMIT/OFFSET: {end - start:.4f} сек")

for p in products:
    print(f"  {p.name}: {p.price}")
```

### Пример 9: Правильное использование JOIN

```python
# Плохо: N+1 проблема - отдельные запросы для связанных объектов
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

# N+1 запросов
start = time.time()
orders = session.query(Order).limit(100).all()
for order in orders:
    print(f"Заказ {order.id}: {order.user.name}")  # Каждый раз новый запрос!
end = time.time()
print(f"N+1 проблема: {end - start:.4f} сек")

# Решение: использование joinedload или subqueryload
from sqlalchemy.orm import joinedload

start = time.time()
orders = session.query(Order).options(
    joinedload(Order.user)
).limit(100).all()
for order in orders:
    print(f"Заказ {order.id}: {order.user.name}")  # Один запрос!
end = time.time()
print(f"С joinedload: {end - start:.4f} сек")
```

### Пример 10: Пакетная вставка данных

```python
# Медленный способ: вставка по одной записи
start = time.time()
for i in range(1000):
    session.execute(text('''
        INSERT INTO products (name, category, price, description)
        VALUES (:name, :category, :price, :desc)
    '''), {
        'name': f'Товар {i}',
        'category': f'Категория {i % 5}',
        'price': 100 + i,
        'description': f'Описание {i}'
    })
    session.commit()  # Коммит каждый раз!
end = time.time()
print(f"Вставка по одной записи: {end - start:.4f} сек")

# Быстрый способ: пакетная вставка
start = time.time()
data = [
    {'name': f'Товар {i}', 'category': f'Категория {i % 5}', 
     'price': 100 + i, 'description': f'Описание {i}'}
    for i in range(1000)
]
session.execute(text('''
    INSERT INTO products (name, category, price, description)
    VALUES (:name, :category, :price, :desc)
'''), data)
session.commit()  # Один коммит в конце
end = time.time()
print(f"Пакетная вставка: {end - start:.4f} сек")

# Ещё быстрее: executemany
start = time.time()
data = [
    (f'Товар {i}', f'Категория {i % 5}', 100 + i, f'Описание {i}')
    for i in range(1000)
]
session.executemany(text('''
    INSERT INTO products (name, category, price, description)
    VALUES (?, ?, ?, ?)
'''), data)
session.commit()
end = time.time()
print(f"executemany: {end - start:.4f} сек")
```

---

## 5. Кэширование

### Пример 11: Кэширование на уровне приложения

```python
from functools import lru_cache

# Простой кэш в памяти
class SimpleCache:
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        return self._cache.get(key)
    
    def set(self, key, value):
        self._cache[key] = value
    
    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        self._cache = {}

cache = SimpleCache()

# Кэширование результатов запроса
def get_popular_products(limit=10):
    cache_key = f"popular_products_{limit}"
    
    # Проверяем кэш
    result = cache.get(cache_key)
    if result is not None:
        print("Данные из кэша")
        return result
    
    # Загружаем из базы
    print("Загрузка из базы данных")
    result = session.query(Product).order_by(Product.price.desc()).limit(limit).all()
    
    # Сохраняем в кэш
    cache.set(cache_key, result)
    return result

# Первый вызов - из базы
products = get_popular_products(10)

# Второй вызов - из кэша
products = get_popular_products(10)
```

### Пример 12: Кэширование с TTL (время жизни)

```python
import time

class TTLCache:
    def __init__(self, ttl_seconds=300):
        self._cache = {}
        self._ttl = ttl_seconds
    
    def get(self, key):
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key, value):
        self._cache[key] = (value, time.time())

ttl_cache = TTLCache(ttl_seconds=60)

def get_categories():
    cache_key = "all_categories"
    result = ttl_cache.get(cache_key)
    
    if result is None:
        result = session.query(Product.category).distinct().all()
        ttl_cache.set(cache_key, result)
        print("Категории загружены из БД")
    else:
        print("Категории из кэша")
    
    return result
```

### Пример 13: Использование Redis для кэширования

```python
# Пример (требует установки Redis)
"""
pip install redis
"""

# import redis
# from json import dumps, loads

# Подключение к Redis
# r = redis.Redis(host='localhost', port=6379, db=0)

# def get_user_cached(user_id):
#     cache_key = f"user:{user_id}"
#     
#     # Попытка получить из кэша
#     cached = r.get(cache_key)
#     if cached:
#         return loads(cached)
#     
#     # Загрузка из БД
#     user = session.query(User).get(user_id)
#     if user:
#         user_data = {'id': user.id, 'name': user.name, 'email': user.email}
#         r.setex(cache_key, 3600, dumps(user_data))  # Кэш на 1 час
#     return user_data
```

---

## 6. Практические задания

### Задание 1: Создание индексов
Создайте базу данных для магазина с таблицами:
- products (id, name, category, price, stock)
- orders (id, user_id, date, status)
- order_items (id, order_id, product_id, quantity)

Определите, какие индексы нужны для следующих запросов:
1. Поиск товара по категории
2. Фильтрация заказов по статусу
3. Получение товаров заказа

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 2: Оптимизация запроса
У вас есть медленный запрос:
```sql
SELECT * FROM products WHERE name LIKE '%Python%' AND price > 100;
```

Как его оптимизировать? Создайте тестовые данные и проверьте скорость до и после оптимизации.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 3: Решение N+1 проблемы
Создайте модели для системы комментариев и решите N+1 проблему:
- Post (id, title, content)
- Comment (id, post_id, author, text)

Выведите все посты с их комментариями, используя joinedload.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 4: Пакетная обработка
Загрузите 10000 записей в базу данных разными способами и сравните скорость:
1. По одной записи с коммитом
2. Пакетная вставка
3. executemany

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 5: Реализация кэша
Реализуйте кэш для функции, которая получает статистику по категориям товаров:
- Количество товаров в каждой категории
- Средняя цена по категориям

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 6: Профилирование
Проведите профилирование трёх разных запросов к вашей базе данных и составьте отчёт о производительности.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## 7. Дополнительные задания

### Задание 7: Оптимизация JOIN
Создайте запрос, который объединяет 4 таблицы, и оптимизируйте его с помощью правильных индексов.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 8: Пул соединений
Настройте пул соединений в SQLAlchemy для повышения производительности.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## Контрольные вопросы:
1. Что такое индексы и как они ускоряют поиск?
2. Какие типы индексов существуют в SQLite?
3. Что такое N+1 проблема и как её решить?
4. Почему важно использовать LIMIT в запросах?
5. Чем отличаются виды кэширования (память, Redis, Memcached)?
6. Как профилировать SQL-запросы в Python?
7. Какие методы пакетной вставки данных самые быстрые?
8. Когда следует использовать композитные индексы?
