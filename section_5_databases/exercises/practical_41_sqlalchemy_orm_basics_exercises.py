"""
Упражнения к практической работе 41: Основы SQLAlchemy ORM

Выполните упражнения по основам SQLAlchemy ORM.
"""

# Упражнение 1: Базовая модель
def exercise_basic_model():
    """
    Создайте базовую модель SQLAlchemy.
    """
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    Base = declarative_base()
    
    class User(Base):
        __tablename__ = 'users'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        email = Column(String(100))
    
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Создание нового пользователя
    user = User(name='Иван', email='ivan@example.com')
    session.add(user)
    session.commit()


# Упражнение 2: CRUD операции
def exercise_crud_operations():
    """
    Выполните CRUD операции.
    """
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    Base = declarative_base()
    
    class Product(Base):
        __tablename__ = 'products'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        price = Column(Integer)
    
    engine = create_engine('sqlite:///products.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create
    product = Product(name='Ноутбук', price=50000)
    session.add(product)
    session.commit()
    
    # Read
    products = session.query(Product).all()
    for p in products:
        print(f'{p.id}: {p.name} - {p.price}')
    
    # Update
    product = session.query(Product).filter_by(id=1).first()
    product.price = 45000
    session.commit()
    
    # Delete
    session.delete(product)
    session.commit()


# Упражнение 3: Запросы
def exercise_queries():
    """
    Выполните различные типы запросов.
    """
    from sqlalchemy import create_engine, Column, Integer, String, func
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    Base = declarative_base()
    
    class Employee(Base):
        __tablename__ = 'employees'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        department = Column(String(50))
        salary = Column(Integer)
    
    engine = create_engine('sqlite:///company.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Примеры запросов
    employees = session.query(Employee).filter(Employee.salary > 50000).all()
    avg_salary = session.query(func.avg(Employee.salary)).scalar()
    grouped = session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()


if __name__ == "__main__":
    print("Упражнения по SQLAlchemy ORM")
