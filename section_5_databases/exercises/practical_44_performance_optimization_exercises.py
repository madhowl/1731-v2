"""
Упражнения к практической работе 44: Оптимизация производительности

Выполните упражнения по оптимизации производительности БД.
"""

# Упражнение 1: Оптимизация запросов
def exercise_query_optimization():
    """
    Оптимизируйте SQL-запросы.
    """
    # Плохо: N+1 проблема
    # for user in session.query(User):
    #     print(user.orders)  # Отдельный запрос для каждого пользователя
    
    # Хорошо: Использование joinload
    from sqlalchemy.orm import joinedload
    # users = session.query(User).options(joinedload(User.orders)).all()
    
    # Плохо: Сложный подзапрос
    # SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 1000)
    
    # Хорошо: JOIN
    # SELECT u.* FROM users u JOIN orders o ON u.id = o.user_id WHERE o.total > 1000


# Упражнение 2: Индексы
def exercise_indexing():
    """
    Создайте правильные индексы.
    """
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Index
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class Transaction(Base):
        __tablename__ = 'transactions'
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer)
        amount = Column(Integer)
        date = Column(DateTime)
        status = Column(String(20))
        
        # Составной индекс для частых запросов
        __table_args__ = (
            Index('idx_user_date', 'user_id', 'date'),
            Index('idx_status_amount', 'status', 'amount'),
        )


# Упражнение 3: Кэширование
def exercise_caching():
    """
    Реализуйте кэширование запросов.
    """
    # Пример с использованием Redis
    import redis
    import pickle
    import hashlib
    
    cache = redis.Redis(host='localhost', port=6379, db=0)
    
    def get_user_with_cache(user_id):
        cache_key = f"user:{user_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return pickle.loads(cached_data)
        
        # Загрузка из БД
        user = session.query(User).filter_by(id=user_id).first()
        
        # Сохранение в кэш на 10 минут
        cache.setex(cache_key, 600, pickle.dumps(user))
        return user


# Упражнение 4: Пул соединений
def exercise_connection_pool():
    """
    Настройте пул соединений.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.pool import QueuePool
    
    # Настройка пула соединений
    engine = create_engine(
        'postgresql://user:password@localhost/dbname',
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True
    )


if __name__ == "__main__":
    print("Упражнения по оптимизации БД")
