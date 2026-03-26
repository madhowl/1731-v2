"""
Упражнения к практической работе 43: Принципы проектирования баз данных

Выполните упражнения по проектированию баз данных.
"""

# Упражнение 1: Нормализация
def exercise_normalization():
    """
    Примените нормализацию к таблице.
    """
    # Пример до нормализации:
    # Orders(order_id, customer_name, customer_address, product_name, quantity, price)
    
    # После нормализации:
    # Customers(customer_id, name, address)
    # Products(product_id, name, price)
    # Orders(order_id, customer_id, order_date)
    # OrderDetails(order_detail_id, order_id, product_id, quantity)


# Упражнение 2: Индексы
def exercise_indexes():
    """
    Создайте индексы для оптимизации запросов.
    """
    from sqlalchemy import create_engine, Column, Integer, String, Index
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class User(Base):
        __tablename__ = 'users'
        
        id = Column(Integer, primary_key=True)
        email = Column(String(100), unique=True)
        name = Column(String(100))
        city = Column(String(50))
        
        # Создание индекса
        __table_args__ = (
            Index('idx_users_city', 'city'),
            Index('idx_users_name_email', 'name', 'email')
        )


# Упражнение 3: Constraints
def exercise_constraints():
    """
    Добавьте ограничения в таблицу.
    """
    from sqlalchemy import create_engine, Column, Integer, String, CheckConstraint
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class Employee(Base):
        __tablename__ = 'employees'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        age = Column(Integer)
        salary = Column(Integer)
        
        # Ограничения
        __table_args__ = (
            CheckConstraint('age >= 18', name='check_age'),
            CheckConstraint('salary > 0', name='check_salary'),
        )


# Упражнение 4: ERD диаграмма
def exercise_erd():
    """
    Спроектируйте ERD диаграмму для системы заказов.
    """
    # Сущности:
    # Customer: id, name, email, phone
    # Product: id, name, description, price
    # Order: id, customer_id, order_date, status
    # OrderItem: id, order_id, product_id, quantity, price
    
    # Связи:
    # Customer --< Order (один ко многим)
    # Order --< OrderItem (один ко многим)
    # Product --< OrderItem (один ко многим)


if __name__ == "__main__":
    print("Упражнения по проектированию баз данных")
