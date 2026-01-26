# Практическое занятие 41: SQLAlchemy - модели

## Создание моделей с использованием SQLAlchemy ORM

### Цель занятия:
Научиться создавать модели данных с использованием SQLAlchemy ORM, определять связи между моделями, использовать различные типы полей и атрибутов.

### Задачи:
1. Создать базовые модели с различными типами полей
2. Реализовать отношения между моделями (один-к-одному, один-ко-многим, многие-ко-многим)
3. Настроить связи с использованием ForeignKeys
4. Использовать различные атрибуты и ограничения полей

### План работы:
1. Основы SQLAlchemy ORM
2. Создание моделей
3. Типы полей
4. Отношения между моделями
5. Практические задания

---

## 1. Основы SQLAlchemy ORM

SQLAlchemy ORM (Object Relational Mapper) - это слой абстракции, который позволяет работать с базой данных как с объектами Python.

### Пример 1: Базовая настройка

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Создание базового класса для моделей
Base = declarative_base()

# Создание движка базы данных
engine = create_engine('sqlite:///example.db', echo=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Пример 2: Простая модель

```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
```

### Пример 3: Создание таблиц

```python
# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Создание таблицы для конкретной модели
User.__table__.create(bind=engine, checkfirst=True)
```

---

## 2. Создание моделей

### Пример 4: Модель с различными типами полей

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Date, Time
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(Base):
    __tablename__ = 'products'
    
    # Целочисленные поля
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    
    # Текстовые поля
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Числовые поля
    price = Column(Float, nullable=False)
    weight = Column(Float)
    
    # Логические поля
    is_available = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Временные поля
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    manufactured_date = Column(Date)
    
    # UUID поле (требует специального типа для PostgreSQL)
    internal_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"
```

### Пример 5: Модель с ограничениями

```python
from sqlalchemy import CheckConstraint, UniqueConstraint

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, CheckConstraint('age >= 18 AND age <= 70'))
    salary = Column(Float, CheckConstraint('salary > 0'))
    department = Column(String(50))
    hire_date = Column(Date, nullable=False)
    
    # Уникальное ограничение на сочетание полей
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', name='unique_name_combo'),
    )
    
    def __repr__(self):
        return f"<Employee(name='{self.first_name} {self.last_name}', department='{self.department}')>"
```

---

## 3. Типы полей

### Пример 6: Все основные типы полей SQLAlchemy

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Date, Time, LargeBinary
from sqlalchemy.dialects.postgresql import ARRAY, JSON, JSONB
from sqlalchemy.types import Enum
import enum

# Перечисление для использования в Enum поле
class StatusEnum(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Article(Base):
    __tablename__ = 'articles'
    
    # Целочисленные
    id = Column(Integer, primary_key=True, index=True)
    views_count = Column(Integer, default=0)
    
    # Строковые
    title = Column(String(200), nullable=False)
    slug = Column(String(220), unique=True, index=True)
    
    # Текстовые
    content = Column(Text)
    summary = Column(Text)
    
    # Числовые с плавающей точкой
    rating = Column(Float, default=0.0)
    
    # Логические
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Временные
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)
    scheduled_for = Column(Time)
    event_date = Column(Date)
    
    # Бинарные данные (например, для хранения файлов)
    thumbnail = Column(LargeBinary)
    
    # JSON поля (для PostgreSQL)
    metadata = Column(JSON)
    settings = Column(JSONB)
    
    # Массивы (для PostgreSQL)
    tags = Column(ARRAY(String))
    
    # Enum поля
    status = Column(Enum(StatusEnum), default=StatusEnum.DRAFT)
    
    def __repr__(self):
        return f"<Article(title='{self.title}', status='{self.status.value}')>"
```

---

## 4. Отношения между моделями

### Пример 7: Отношение один-ко-многим

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    
    # Обратная связь с продуктами
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    
    # Внешний ключ к категории
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    # Прямая связь с категорией
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', category_id={self.category_id})>"
```

### Пример 8: Отношение один-к-одному

```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    
    # Один-к-одному с профилем
    profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(Text)
    birth_date = Column(Date)
    avatar_url = Column(String(255))
    
    # Уникальный внешний ключ к пользователю
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    # Обратная связь с пользователем
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id})>"
```

### Пример 9: Отношение многие-ко-многим

```python
from sqlalchemy import Table

# Ассоциативная таблица для связи многие-ко-многим
user_roles_association = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Многие-ко-многим с пользователями
    users = relationship("User", secondary=user_roles_association, back_populates="roles")
    
    def __repr__(self):
        return f"<Role(name='{self.name}')>"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    
    # Многие-ко-многим с ролями
    roles = relationship("Role", secondary=user_roles_association, back_populates="users")
    
    def __repr__(self):
        return f"<User(username='{self.username}')>"
```

### Пример 10: Отношения с дополнительной информацией (Association Object)

```python
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    
    # Связь с OrderItem
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, total={self.total_amount})>"

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    
    # Связь с OrderItem
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float)
    
    # Связи с Order и Product
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id})>"
```

---

## 5. Практические задания

### Задание 1: Создание модели пользователя
Создайте модель User с полями:
- id (Integer, primary key)
- username (String, unique, not null)
- email (String, unique, not null)
- first_name (String)
- last_name (String)
- is_active (Boolean, default True)
- created_at (DateTime, default now)

### Задание 2: Модель блога
Создайте модели для блога:
- Post (id, title, content, created_at, author_id)
- Comment (id, content, created_at, post_id, author_id)
- Установите отношения между моделями

### Задание 3: Интернет-магазин
Создайте модели для интернет-магазина:
- Category (id, name, description)
- Product (id, name, description, price, category_id)
- Cart (id, user_id, created_at)
- CartItem (id, cart_id, product_id, quantity)
- Реализуйте все необходимые отношения

### Задание 4: Система управления задачами
Создайте модели для системы задач:
- Project (id, name, description, created_at)
- Task (id, title, description, status, priority, project_id, assignee_id)
- Tag (id, name)
- Реализуйте отношения многие-ко-многим между Task и Tag

### Задание 5: Библиотечная система
Создайте модели для библиотеки:
- Author (id, name, biography, birth_date)
- Book (id, title, isbn, publication_date, author_id)
- Reader (id, name, email, registration_date)
- BorrowRecord (id, book_id, reader_id, borrow_date, return_date)
- Реализуйте все необходимые отношения

---

## 6. Дополнительные задания

### Задание 6: Вложенные отношения
Создайте модель с вложенными отношениями (например, компания-отдел-сотрудник).

### Задание 7: Кастомные типы данных
Создайте пользовательский тип данных и используйте его в модели.

### Задание 8: Индексы и ограничения
Добавьте индексы и различные ограничения к созданным моделям.

---

## Контрольные вопросы:
1. Как создать базовую модель в SQLAlchemy?
2. Какие типы полей доступны в SQLAlchemy?
3. Как реализовать отношение один-ко-многим?
4. Как создать отношение многие-ко-многим?
5. Что такое каскадные операции и как их использовать?