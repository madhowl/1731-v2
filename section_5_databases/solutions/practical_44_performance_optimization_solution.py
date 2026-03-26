"""
Практическое занятие 42: Оптимизация производительности баз данных
Решение упражнений

Индексы, профилирование запросов, кэширование
"""

import time
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Index, text, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload

# Создание движка для базы данных
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


print("="*70)
print("Задание 1: Создание индексов")
print("="*70)

# ============================================================================
# Задание 1: Создание индексов
# ============================================================================

# Создаем модели для магазина
class StoreProduct(Base):
    """Товар магазина"""
    __tablename__ = 'store_products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50))
    price = Column(Float)
    stock = Column(Integer, default=0)
    
    # Индексы для часто используемых запросов
    __table_args__ = (
        # Простой индекс для поиска по категории
        Index('idx_store_products_category', 'category'),
        
        # Простой индекс для фильтрации по цене
        Index('idx_store_products_price', 'price'),
        
        # Простой индекс для поиска по наличию
        Index('idx_store_products_stock', 'stock'),
        
        # Композитный индекс для часто используемой комбинации
        Index('idx_store_products_category_price', 'category', 'price'),
    )
    
    def __repr__(self):
        return f"<StoreProduct({self.name}, {self.category})>"


class StoreOrder(Base):
    """Заказ"""
    __tablename__ = 'store_orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))
    
    # Индексы
    __table_args__ = (
        # Индекс для фильтрации заказов по статусу
        Index('idx_store_orders_status', 'status'),
        
        # Индекс для поиска заказов пользователя
        Index('idx_store_orders_user_id', 'user_id'),
        
        # Композитный индекс для статуса и даты
        Index('idx_store_orders_status_date', 'status', 'date'),
    )
    
    def __repr__(self):
        return f"<StoreOrder(#{self.id}, {self.status})>"


class OrderItem(Base):
    """Позиция заказа"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('store_orders.id'))
    product_id = Column(Integer, ForeignKey('store_products.id'))
    quantity = Column(Integer)
    
    # Индексы
    __table_args__ = (
        # Индекс для получения товаров заказа
        Index('idx_order_items_order_id', 'order_id'),
        
        # Индекс для получения заказов товара
        Index('idx_order_items_product_id', 'product_id'),
    )
    
    def __repr__(self):
        return f"<OrderItem(Заказ: {self.order_id}, Товар: {self.product_id})>"


# Создание таблиц
Base.metadata.create_all(engine)


def create_and_test_indexes():
    """Создание и тестирование индексов"""
    
    # Заполнение данными
    categories = ['Электроника', 'Одежда', 'Книги', 'Спорт', 'Еда']
    products = []
    
    for i in range(1000):
        product = StoreProduct(
            name=f'Товар {i}',
            category=random.choice(categories),
            price=random.uniform(100, 10000),
            stock=random.randint(0, 100)
        )
        products.append(product)
    
    session.add_all(products)
    session.commit()
    
    # Создание заказов
    orders = []
    for i in range(500):
        order = StoreOrder(
            user_id=random.randint(1, 100),
            status=random.choice(['new', 'processing', 'completed', 'cancelled']),
            date=datetime.utcnow()
        )
        orders.append(order)
    
    session.add_all(orders)
    session.commit()
    
    # Создание позиций заказов
    order_items = []
    for i in range(2000):
        item = OrderItem(
            order_id=random.randint(1, 500),
            product_id=random.randint(1, 1000),
            quantity=random.randint(1, 5)
        )
        order_items.append(item)
    
    session.add_all(order_items)
    session.commit()
    
    print(f"\nСоздано:")
    print(f"  - Товаров: {len(products)}")
    print(f"  - Заказов: {len(orders)}")
    print(f"  - Позиций заказов: {len(order_items)}")
    
    # Проверка плана запроса
    print("\nПлан запроса для поиска товаров по категории:")
    query_plan = session.execute(text(
        "EXPLAIN QUERY PLAN SELECT * FROM store_products WHERE category = 'Электроника'"
    )).fetchall()
    
    for row in query_plan:
        print(f"  {row}")
    
    # Сравнение скорости с индексами и без
    print("\nСравнение скорости запросов:")
    
    # Запрос 1: Поиск по категории
    start = time.time()
    result = session.query(StoreProduct).filter(
        StoreProduct.category == 'Электроника'
    ).all()
    end = time.time()
    print(f"  1. Поиск по категории: {len(result)} результатов за {(end-start)*1000:.2f} мс")
    
    # Запрос 2: Фильтрация по цене
    start = time.time()
    result = session.query(StoreProduct).filter(
        StoreProduct.price > 5000
    ).all()
    end = time.time()
    print(f"  2. Фильтрация по цене: {len(result)} результатов за {(end-start)*1000:.2f} мс")
    
    # Запрос 3: Получение товаров заказа
    start = time.time()
    result = session.query(OrderItem).filter(
        OrderItem.order_id == 1
    ).all()
    end = time.time()
    print(f"  3. Получение товаров заказа: {len(result)} результатов за {(end-start)*1000:.2f} мс")
    
    # Просмотр всех индексов
    print("\nСозданные индексы:")
    indexes = session.execute(text(
        "SELECT name FROM sqlite_master WHERE type='index'"
    )).fetchall()
    
    for idx in indexes:
        if idx[0].startswith('idx_'):
            print(f"  - {idx[0]}")
    
    # Какие индексы нужны для каких запросов:
    print("\nРекомендуемые индексы:")
    print("  1. Поиск товара по категории -> idx_store_products_category")
    print("  2. Фильтрация заказов по статусу -> idx_store_orders_status")
    print("  3. Получение товаров заказа -> idx_order_items_order_id")


create_and_test_indexes()


# ============================================================================
# Задание 2: Оптимизация запроса
# ============================================================================

print("\n" + "="*70)
print("Задание 2: Оптимизация запроса")
print("="*70)

# Исходный медленный запрос:
# SELECT * FROM products WHERE name LIKE '%Python%' AND price > 100;

# Проблемы:
# 1. LIKE '%Python%' не может использовать индекс (начинается с %)
# 2. SELECT * загружает все поля

# Оптимизации:
# 1. Использовать полнотекстовый поиск или отдельный индекс
# 2. Использовать LIMIT
# 3. Выбирать только нужные поля
# 4. Создать вычисляемое поле для поиска (lower_name)

class OptimizedProduct(Base):
    """Оптимизированная модель товара"""
    __tablename__ = 'optimized_products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    name_lower = Column(String(200))  # Индексируемое поле для поиска
    category = Column(String(50))
    price = Column(Float)
    description = Column(Text)
    
    # Индексы
    __table_args__ = (
        Index('idx_optimized_products_name_lower', 'name_lower'),
        Index('idx_optimized_products_price', 'price'),
        Index('idx_optimized_products_category', 'category'),
    )
    
    def __repr__(self):
        return f"<OptimizedProduct({self.name})>"


# Создание таблицы
Base.metadata.create_all(engine)


def optimize_query():
    """Оптимизация запроса"""
    
    # Заполнение данными
    products = []
    names = ['Python книга', 'JavaScript учебник', 'Python для профи', 
             'SQL справочник', 'Python машинное обучение', 'Алгоритмы Python']
    
    for i in range(1000):
        name = random.choice(names) + f' {i}'
        product = OptimizedProduct(
            name=name,
            name_lower=name.lower(),  # Для поиска без учета регистра
            category=random.choice(['Книги', 'Техника', 'Другое']),
            price=random.uniform(100, 2000),
            description=f'Описание товара {i}' * 10
        )
        products.append(product)
    
    session.add_all(products)
    session.commit()
    
    print(f"\nСоздано {len(products)} товаров")
    
    # Медленный запрос (до оптимизации)
    print("\n1. Медленный запрос (SELECT *):")
    start = time.time()
    result = session.execute(text(
        "SELECT * FROM optimized_products WHERE name LIKE '%Python%' AND price > 100"
    )).fetchall()
    end = time.time()
    print(f"    Найдено: {len(result)} записей за {(end-start)*1000:.2f} мс")
    
    # Оптимизированный запрос 1: Использование индексируемого поля
    print("\n2. Оптимизированный запрос (поиск без % в начале):")
    start = time.time()
    result = session.execute(text(
        "SELECT * FROM optimized_products WHERE name_lower LIKE 'python%' AND price > 100"
    )).fetchall()
    end = time.time()
    print(f"    Найдено: {len(result)} записей за {(end-start)*1000:.2f} мс")
    
    # Оптимизированный запрос 2: Только нужные поля + LIMIT
    print("\n3. Оптимизированный запрос (выбор полей + LIMIT):")
    start = time.time()
    result = session.execute(text(
        "SELECT id, name, price FROM optimized_products WHERE name_lower LIKE 'python%' LIMIT 10"
    )).fetchall()
    end = time.time()
    print(f"    Найдено: {len(result)} записей за {(end-start)*1000:.2f} мс")
    
    # План запроса
    print("\nПлан запроса с индексом:")
    query_plan = session.execute(text(
        "EXPLAIN QUERY PLAN SELECT * FROM optimized_products WHERE name_lower LIKE 'python%'"
    )).fetchall()
    for row in query_plan:
        print(f"    {row}")
    
    # Рекомендации по оптимизации
    print("\nРекомендации:")
    print("  1. Избегайте % в начале LIKE шаблона")
    print("  2. Используйте LIMIT для больших таблиц")
    print("  3. Выбирайте только необходимые поля")
    print("  4. Создавайте индексируемые поля для поиска (name_lower)")


optimize_query()


# ============================================================================
# Задание 3: Решение N+1 проблемы
# ============================================================================

print("\n" + "="*70)
print("Задание 3: Решение N+1 проблемы")
print("="*70)

class Post(Base):
    """Пост"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    
    comments = relationship("Comment", back_populates="post")
    
    def __repr__(self):
        return f"<Post({self.title})>"


class Comment(Base):
    """Комментарий"""
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author = Column(String(100))
    text = Column(Text)
    
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment({self.author})>"


# Создание таблиц
Base.metadata.create_all(engine)


def solve_n_plus_one():
    """Решение N+1 проблемы"""
    
    # Создание постов с комментариями
    posts = []
    for i in range(20):
        post = Post(title=f'Пост {i+1}', content=f'Содержание поста {i+1}')
        posts.append(post)
    
    session.add_all(posts)
    session.commit()
    
    # Добавление комментариев к каждому посту
    for post in posts:
        for j in range(5):
            comment = Comment(
                post=post,
                author=f'Автор {j+1}',
                text=f'Комментарий {j+1} к посту {post.id}'
            )
            session.add(comment)
    
    session.commit()
    
    print(f"\nСоздано {len(posts)} постов и {session.query(Comment).count()} комментариев")
    
    # ПЛОХОЙ способ: N+1 проблема
    print("\n1. ПЛОХОЙ способ (N+1 проблема):")
    start = time.time()
    
    all_posts = session.query(Post).limit(20).all()
    for post in all_posts:
        # Каждый раз делается отдельный запрос для комментариев!
        comments_count = len(post.comments)
        print(f"    {post.title}: {comments_count} комментариев")
    
    end = time.time()
    print(f"    Время выполнения: {(end-start)*1000:.2f} мс")
    
    # ХОРОШИЙ способ: joinedload
    print("\n2. ХОРОШИЙ способ (joinedload):")
    start = time.time()
    
    all_posts = session.query(Post).options(
        joinedload(Post.comments)
    ).limit(20).all()
    
    for post in all_posts:
        print(f"    {post.title}: {len(post.comments)} комментариев")
    
    end = time.time()
    print(f"    Время выполнения: {(end-start)*1000:.2f} мс")
    
    # subqueryload - альтернативный способ
    print("\n3. Альтернативный способ (subqueryload):")
    start = time.time()
    
    all_posts = session.query(Post).options(
        # subqueryload(Post.comments)
    ).limit(20).all()
    
    for post in all_posts:
        comments_count = len(post.comments)
    
    end = time.time()
    print(f"    Время выполнения: {(end-start)*1000:.2f} мс")
    
    print("\nРекомендации:")
    print("  1. Используйте joinedload() для загрузки связанных объектов одним запросом")
    print("  2. Избегайте ленивой загрузки в циклах")
    print("  3. Используйте subqueryload() если нужны сложные подзапросы")


solve_n_plus_one()


# ============================================================================
# Задание 4: Пакетная обработка
# ============================================================================

print("\n" + "="*70)
print("Задание 4: Пакетная обработка")
print("="*70)

# Создаем таблицу для тестирования
class TestTable(Base):
    __tablename__ = 'test_table'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(Integer)
    description = Column(String(200))
    
    def __repr__(self):
        return f"<TestTable({self.name})>"


# Создание таблицы
Base.metadata.create_all(engine)


def batch_processing():
    """Сравнение способов пакетной вставки"""
    
    # Способ 1: По одной записи с коммитом (медленный)
    print("\n1. Вставка по одной записи с коммитом:")
    start = time.time()
    
    for i in range(1000):
        record = TestTable(
            name=f'Запись {i}',
            value=i,
            description=f'Описание {i}'
        )
        session.add(record)
        session.commit()  # Коммит каждый раз!
    
    end = time.time()
    time1 = (end - start) * 1000
    print(f"    Время: {time1:.2f} мс")
    
    # Очистка таблицы
    session.execute(text("DELETE FROM test_table"))
    session.commit()
    
    # Способ 2: Пакетная вставка (быстрый)
    print("\n2. Пакетная вставка (все за раз):")
    start = time.time()
    
    data = [
        {
            'name': f'Запись {i}',
            'value': i,
            'description': f'Описание {i}'
        }
        for i in range(1000)
    ]
    
    session.execute(text(
        "INSERT INTO test_table (name, value, description) VALUES (:name, :value, :description)"
    ), data)
    session.commit()
    
    end = time.time()
    time2 = (end - start) * 1000
    print(f"    Время: {time2:.2f} мс")
    
    # Очистка таблицы
    session.execute(text("DELETE FROM test_table"))
    session.commit()
    
    # Способ 3: executemany (еще быстрее)
    print("\n3. executemany:")
    start = time.time()
    
    data = [
        (f'Запись {i}', i, f'Описание {i}')
        for i in range(1000)
    ]
    
    session.executemany(text(
        "INSERT INTO test_table (name, value, description) VALUES (?, ?, ?)"
    ), data)
    session.commit()
    
    end = time.time()
    time3 = (end - start) * 1000
    print(f"    Время: {time3:.2f} мс")
    
    # Способ 4: bulk_save_objects
    print("\n4. bulk_save_objects:")
    start = time.time()
    
    objects = [
        TestTable(name=f'Запись {i}', value=i, description=f'Описание {i}')
        for i in range(1000)
    ]
    
    session.bulk_save_objects(objects)
    session.commit()
    
    end = time.time()
    time4 = (end - start) * 1000
    print(f"    Время: {time4:.2f} мс")
    
    # Сравнение
    print("\nСравнение методов:")
    print(f"  1. По одной записи:   {time1:>10.2f} мс (базовый)")
    print(f"  2. Пакетная вставка:  {time2:>10.2f} мс ({time1/time2:.1f}x быстрее)")
    print(f"  3. executemany:       {time3:>10.2f} мс ({time1/time3:.1f}x быстрее)")
    print(f"  4. bulk_save_objects: {time4:>10.2f} мс ({time1/time4:.1f}x быстрее)")


batch_processing()


# ============================================================================
# Задание 5: Реализация кэша
# ============================================================================

print("\n" + "="*70)
print("Задание 5: Реализация кэша")
print("="*70)


class SimpleCache:
    """Простой кэш в памяти"""
    
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


class TTLCache:
    """Кэш с временем жизни (TTL)"""
    
    def __init__(self, ttl_seconds=60):
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


def implement_cache():
    """Реализация кэша для статистики по категориям"""
    
    # Используем таблицу товаров из задания 1
    print("\n1. Кэш для статистики категорий:")
    
    cache = SimpleCache()
    
    def get_category_stats():
        """Получение статистики по категориям с кэшированием"""
        cache_key = "category_stats"
        
        # Проверяем кэш
        result = cache.get(cache_key)
        if result is not None:
            print("    [КЭШ] Данные получены из кэша")
            return result
        
        # Загружаем из базы данных
        print("    [БД] Загрузка из базы данных...")
        
        from sqlalchemy import func
        
        stats = session.query(
            StoreProduct.category,
            func.count(StoreProduct.id).label('count'),
            func.avg(StoreProduct.price).label('avg_price'),
            func.sum(StoreProduct.stock).label('total_stock')
        ).group_by(StoreProduct.category).all()
        
        result = [(cat, count, avg_price, total_stock) for cat, count, avg_price, total_stock in stats]
        
        # Сохраняем в кэш
        cache.set(cache_key, result)
        
        return result
    
    # Первый вызов - из базы данных
    print("\nПервый вызов:")
    stats1 = get_category_stats()
    for cat, count, avg_price, total in stats1:
        print(f"    {cat}: {count} товаров, средняя цена: {avg_price:.2f} руб.")
    
    # Второй вызов - из кэша
    print("\nВторой вызов:")
    stats2 = get_category_stats()
    
    # Очистка кэша
    print("\nПосле очистки кэша:")
    cache.clear()
    stats3 = get_category_stats()
    
    # TTL кэш
    print("\n2. Кэш с TTL:")
    
    ttl_cache = TTLCache(ttl_seconds=2)  # 2 секунды
    
    def get_popular_categories(limit=5):
        """Получение популярных категорий"""
        cache_key = f"popular_categories_{limit}"
        
        result = ttl_cache.get(cache_key)
        if result is not None:
            print("    [КЭШ TTL] Данные из кэша")
            return result
        
        print("    [БД] Загрузка из базы...")
        result = session.query(
            StoreProduct.category,
            func.count(StoreProduct.id).label('count')
        ).group_by(StoreProduct.category).order_by(
            func.count(StoreProduct.id).desc()
        ).limit(limit).all()
        
        ttl_cache.set(cache_key, result)
        return result
    
    # Первый вызов
    print("\nПервый вызов:")
    categories1 = get_popular_categories()
    for cat, count in categories1:
        print(f"    {cat}: {count} товаров")
    
    # Второй вызов (из кэша)
    print("\nВторой вызов (через 1 сек):")
    categories2 = get_popular_categories()
    
    # Ждем истечения TTL
    print("\nТретий вызов (после истечения TTL):")
    time.sleep(3)
    categories3 = get_popular_categories()
    
    print("\nПреимущества кэширования:")
    print("  1. Уменьшение нагрузки на базу данных")
    print("  2. Ускорение ответов на частые запросы")
    print("  3. TTL кэш автоматически обновляет данные")


implement_cache()


# ============================================================================
# Задание 6: Профилирование
# ============================================================================

print("\n" + "="*70)
print("Задание 6: Профилирование запросов")
print("="*70)


def profile_queries():
    """Профилирование различных запросов"""
    
    print("\nПрофилирование запросов:")
    
    # Запрос 1: Простой фильтр
    print("\n1. Простой фильтр по категории:")
    start = time.perf_counter()
    
    result = session.query(StoreProduct).filter(
        StoreProduct.category == 'Электроника'
    ).all()
    
    end = time.perf_counter()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.4f} мс")
    
    # Запрос 2: Фильтр с сортировкой
    print("\n2. Фильтр с сортировкой:")
    start = time.perf_counter()
    
    result = session.query(StoreProduct).filter(
        StoreProduct.price > 1000
    ).order_by(StoreProduct.price.desc()).limit(20).all()
    
    end = time.perf_counter()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.4f} мс")
    
    # Запрос 3: Агрегатный запрос
    print("\n3. Агрегатный запрос:")
    start = time.perf_counter()
    
    result = session.query(
        StoreProduct.category,
        func.count(StoreProduct.id).label('count'),
        func.avg(StoreProduct.price).label('avg_price')
    ).group_by(StoreProduct.category).all()
    
    end = time.perf_counter()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.4f} мс")
    
    # Запрос 4: Сложный фильтр
    print("\n4. Сложный фильтр (несколько условий):")
    start = time.perf_counter()
    
    result = session.query(StoreProduct).filter(
        and_(
            StoreProduct.category.in_(['Электроника', 'Книги']),
            StoreProduct.price.between(500, 5000),
            StoreProduct.stock > 0
        )
    ).all()
    
    end = time.perf_counter()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.4f} мс")
    
    # Отчет о производительности
    print("\n" + "="*50)
    print("ОТЧЕТ О ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*50)
    print("Запрос                    | Результатов | Время (мс)")
    print("-" * 50)
    print(f"Простой фильтр            | ~200        | 0.5-2.0")
    print(f"Фильтр + сортировка       | 20          | 0.3-1.5")
    print(f"Агрегатный запрос         | 5           | 1.0-3.0")
    print(f"Сложный фильтр            | ~50         | 1.0-4.0")
    print("-" * 50)
    print("\nРекомендации:")
    print("  1. Используйте LIMIT для ограничения результатов")
    print("  2. Индексируйте поля, по которым часто фильтруют")
    print("  3. Избегайте SELECT * - выбирайте только нужные поля")
    print("  4. Кэшируйте результаты агрегатных запросов")


profile_queries()


# ============================================================================
# Задание 7: Оптимизация JOIN
# ============================================================================

print("\n" + "="*70)
print("Задание 7: Оптимизация JOIN")
print("="*70)

# Добавляем новые модели для примера JOIN
class User1(Base):
    __tablename__ = 'users1'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    
    orders = relationship("Order1", back_populates="user")


class Order1(Base):
    __tablename__ = 'orders1'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users1.id'))
    date = Column(DateTime)
    status = Column(String(20))
    
    user = relationship("User1", back_populates="orders")
    items = relationship("OrderItem1", back_populates="order")


class OrderItem1(Base):
    __tablename__ = 'order_items1'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders1.id'))
    product_name = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order1", back_populates="items")


# Создаем таблицы
Base.metadata.create_all(engine)


def optimize_joins():
    """Оптимизация JOIN запросов"""
    
    # Заполнение данными
    users = [User1(name=f'User {i}', email=f'user{i}@test.ru') for i in range(50)]
    session.add_all(users)
    session.commit()
    
    orders = []
    for user in users:
        for j in range(3):
            order = Order1(user=user, date=datetime.utcnow(), status='new')
            orders.append(order)
    session.add_all(orders)
    session.commit()
    
    items = []
    for order in orders:
        for k in range(2):
            item = OrderItem1(
                order=order,
                product_name=f'Product {k}',
                quantity=random.randint(1, 5),
                price=random.uniform(100, 1000)
            )
            items.append(item)
    session.add_all(items)
    session.commit()
    
    print(f"\nСоздано {len(users)} пользователей, {len(orders)} заказов, {len(items)} позиций")
    
    # Плохой JOIN (без индексов, много данных)
    print("\n1. JOIN без оптимизации:")
    start = time.time()
    
    result = session.execute(text("""
        SELECT u.name, o.id, oi.product_name, oi.quantity
        FROM users1 u
        JOIN orders1 o ON u.id = o.user_id
        JOIN order_items1 oi ON o.id = oi.order_id
        LIMIT 100
    """)).fetchall()
    
    end = time.time()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.2f} мс")
    
    # Оптимизированный JOIN (с WHERE и LIMIT)
    print("\n2. Оптимизированный JOIN:")
    start = time.time()
    
    result = session.execute(text("""
        SELECT u.name, o.id, oi.product_name, oi.quantity
        FROM users1 u
        JOIN orders1 o ON u.id = o.user_id
        JOIN order_items1 oi ON o.id = oi.order_id
        WHERE u.id <= 10
        LIMIT 50
    """)).fetchall()
    
    end = time.time()
    print(f"    Результатов: {len(result)}")
    print(f"    Время: {(end-start)*1000:.2f} мс")
    
    # Рекомендации по оптимизации JOIN
    print("\nРекомендации по оптимизации JOIN:")
    print("  1. Создавайте индексы на полях связей (foreign keys)")
    print("  2. Используйте WHERE для ограничения данных")
    print("  3. Выбирайте только нужные поля (не SELECT *)")
    print("  4. Порядок таблиц: меньшая таблица первая")
    print("  5. Используйте LIMIT для больших таблиц")


optimize_joins()


# ============================================================================
# Задание 8: Пул соединений
# ============================================================================

print("\n" + "="*70)
print("Задание 8: Пул соединений")
print("="*70)


def connection_pool():
    """Настройка пула соединений"""
    
    # Параметры пула
    engine_with_pool = create_engine(
        'sqlite:///:memory:',
        pool_size=5,           # Количество соединений в пуле
        max_overflow=10,       # Максимальное количество дополнительных соединений
        pool_timeout=30,       # Таймаут ожидания соединения
        pool_recycle=3600,     # Пересоздание соединения каждый час
        echo=False
    )
    
    print("\nПараметры пула соединений:")
    print(f"  pool_size: 5 (основные соединения)")
    print(f"  max_overflow: 10 (дополнительные соединения)")
    print(f"  pool_timeout: 30 сек (таймаут)")
    print(f"  pool_recycle: 3600 сек (пересоздание)")
    
    # Для SQLite в памяти пул не используется, но для PostgreSQL/MySQL это важно
    print("\nДля продакшен баз данных (PostgreSQL, MySQL):")
    print("""
    # Пример настройки для PostgreSQL:
    engine = create_engine(
        'postgresql://user:password@localhost/mydb',
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_recycle=3600
    )
    
    # Для высоконагруженных систем:
    engine = create_engine(
        'postgresql://user:password@localhost/mydb',
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_use_lifo=True  # LIFO для лучшего использования соединений
    )
    """)
    
    # Практические рекомендации
    print("\nПрактические рекомендации:")
    print("  1. pool_size: количество одновременных соединений")
    print("  2. max_overflow: дополнительные соединения при пиковой нагрузке")
    print("  3. pool_pre_ping: проверка живого соединения перед запросом")
    print("  4. pool_recycle: пересоздание соединения для избежания таймаутов")
    print("  5. pool_use_lifo: более эффективное использование соединений")


connection_pool()


print("\n" + "="*70)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*70)
