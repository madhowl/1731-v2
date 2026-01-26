# Лекция 22: SQLAlchemy ORM

## Основы ORM, модели данных, отношения между таблицами, запросы

### Цель лекции:
- Познакомиться с ORM (Object-Relational Mapping)
- Изучить основы SQLAlchemy
- Освоить создание моделей данных и отношений
- Научиться выполнять запросы через ORM

### План лекции:
1. Что такое ORM
2. Основы SQLAlchemy
3. Создание моделей
4. Отношения между таблицами
5. Запросы через ORM

---

## 1. Что такое ORM

ORM (Object-Relational Mapping) — технология программирования, которая позволяет преобразовывать объекты в структуры, используемые в реляционных базах данных, и наоборот.

### Преимущества ORM:
- **Абстрагирование от SQL** - работа с объектами вместо таблиц
- **Безопасность** - предотвращение SQL-инъекций
- **Переносимость** - возможность работы с разными СУБД
- **Удобство** - более понятный синтаксис
- **Поддержка** - встроенные механизмы валидации и кэширования

### Недостатки ORM:
- **Производительность** - возможная задержка по сравнению с чистым SQL
- **Сложность** - дополнительный уровень абстракции
- **Ограничения** - не все SQL-конструкции могут быть представлены

### Пример сравнения:
```sql
-- SQL запрос
SELECT * FROM users WHERE age > 25;
```

```python
# ORM запрос
users = session.query(User).filter(User.age > 25).all()
```

---

## 2. Основы SQLAlchemy

SQLAlchemy — наиболее популярный ORM для Python, предоставляющий гибкие и мощные средства работы с базами данных.

### Установка:
```bash
pip install sqlalchemy
```

### Основные компоненты SQLAlchemy:
- **Core** - низкоуровневый API для работы с базами данных
- **ORM** - объектно-реляционный mapper
- **Engine** - интерфейс взаимодействия с базой данных
- **Session** - интерфейс для выполнения запросов

### Подключение к базе данных:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание engine
engine = create_engine('sqlite:///example.db')

# Создание базового класса
Base = declarative_base()

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()
```

### Подключения к разным СУБД:
```python
# SQLite (файл)
engine = create_engine('sqlite:///database.db')

# PostgreSQL
engine = create_engine('postgresql://user:password@localhost/dbname')

# MySQL
engine = create_engine('mysql://user:password@localhost/dbname')

# SQLite (в памяти)
engine = create_engine('sqlite:///:memory:')
```

---

## 3. Создание моделей

Модель в SQLAlchemy — это класс Python, который представляет таблицу в базе данных.

### Пример базовой модели:
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
```

### Типы данных SQLAlchemy:
```python
from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, Date, Time, LargeBinary

# Примеры столбцов
Column(String(50))        # Строка фиксированной длины
Column(Text)              # Текст переменной длины
Column(Integer)           # Целое число
Column(Float)             # Число с плавающей точкой
Column(Boolean)           # Логический тип
Column(DateTime)          # Дата и время
Column(Date)              # Только дата
Column(Time)              # Только время
Column(LargeBinary)       # Бинарные данные
```

### Ограничения и атрибуты:
```python
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Не может быть пустым
    price = Column(Float, nullable=False)
    description = Column(Text)
    in_stock = Column(Boolean, default=True)    # Значение по умолчанию
    category_id = Column(Integer, index=True)   # Индекс для ускорения поиска
    sku = Column(String(50), unique=True)      # Уникальное значение
```

### Создание таблиц:
```python
# Создание всех таблиц
Base.metadata.create_all(engine)

# Или создание отдельной таблицы
User.__table__.create(engine)
```

---

## 4. Отношения между таблицами

SQLAlchemy поддерживает все основные типы отношений: один-к-одному, один-ко-многим и многие-ко-многим.

### Отношение один-ко-многим:
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # Отношение "один ко многим"
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Обратное отношение
    author = relationship("User", back_populates="posts")
```

### Отношение один-к-одному:
```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # Один к одному
    profile = relationship("UserProfile", uselist=False, back_populates="user")

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    bio = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    user = relationship("User", back_populates="profile")
```

### Отношение многие-ко-многим:
```python
from sqlalchemy import Table

# Ассоциативная таблица
association_table = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # Многие ко многим
    roles = relationship("Role", secondary=association_table, back_populates="users")

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    users = relationship("User", secondary=association_table, back_populates="roles")
```

---

## 5. Запросы через ORM

SQLAlchemy предоставляет мощный интерфейс для выполнения запросов через ORM.

### Создание записей:
```python
# Создание нового пользователя
new_user = User(name="Иван Иванов", email="ivan@example.com", age=30)
session.add(new_user)
session.commit()

# Создание нескольких записей
users = [
    User(name="Анна Смирнова", email="anna@example.com"),
    User(name="Петр Сидоров", email="petr@example.com")
]
session.add_all(users)
session.commit()
```

### Выборка данных:
```python
# Выборка всех записей
all_users = session.query(User).all()

# Выборка одной записи
user = session.query(User).filter(User.id == 1).first()

# Выборка по условию
active_users = session.query(User).filter(User.age > 18).all()

# Выборка с сортировкой
sorted_users = session.query(User).order_by(User.name).all()

# Выборка с лимитом
recent_users = session.query(User).order_by(User.id.desc()).limit(10).all()
```

### Фильтрация данных:
```python
from sqlalchemy import and_, or_

# Использование and_
users = session.query(User).filter(and_(User.age > 20, User.name.like('%Иван%'))).all()

# Использование or_
users = session.query(User).filter(or_(User.age < 18, User.age > 65)).all()

# Различные фильтры
users = session.query(User).filter(
    User.name.in_(['Иван', 'Мария']),
    User.age.between(20, 30),
    User.email.like('%@gmail.com')
).all()
```

### Обновление данных:
```python
# Обновление одной записи
user = session.query(User).filter(User.id == 1).first()
user.age = 31
session.commit()

# Обновление нескольких записей
session.query(User).filter(User.age < 18).update({User.active: False})
session.commit()
```

### Удаление данных:
```python
# Удаление одной записи
user = session.query(User).filter(User.id == 1).first()
session.delete(user)
session.commit()

# Удаление нескольких записей
session.query(User).filter(User.active == False).delete()
session.commit()
```

### Агрегатные функции:
```python
from sqlalchemy import func

# Подсчет
count = session.query(func.count(User.id)).scalar()

# Среднее значение
avg_age = session.query(func.avg(User.age)).scalar()

# Максимальное/минимальное значение
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()

# Группировка
result = session.query(User.age, func.count(User.id)).group_by(User.age).all()
```

### JOIN запросы:
```python
# INNER JOIN
result = session.query(User, Post).join(Post).filter(Post.title.like('%Python%')).all()

# LEFT JOIN
result = session.query(User).outerjoin(Post).all()

# Использование отношений
user_with_posts = session.query(User).options(subqueryload(User.posts)).all()