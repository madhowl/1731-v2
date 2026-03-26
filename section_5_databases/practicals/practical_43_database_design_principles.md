# Практическое занятие 41: Принципы проектирования баз данных

## Нормализация, ER-диаграммы, лучшие практики

### Цель занятия:
Освоить принципы проектирования реляционных баз данных, изучить нормальные формы и научиться создавать эффективные схемы баз данных.

### Задачи:
1. Понять основы нормализации баз данных
2. Научиться создавать ER-диаграммы
3. Освоить принципы проектирования таблиц
4. Изучить ограничения целостности
5. Научиться применять нормальные формы на практике

### План работы:
1. Введение в проектирование БД
2. Нормализация баз данных
3. ER-моделирование
4. Ограничения целостности
5. Денормализация
6. Практические задания

---

## 1. Введение в проектирование баз данных

Проектирование базы данных — это процесс создания структуры данных, которая эффективно хранит необходимую информацию и обеспечивает быстрый доступ к ней.

### Пример 1: Анализ требований

```python
# Рассмотрим систему управления библиотекой
# Требования:
# 1. Хранение информации о книгах (название, автор, год издания, ISBN)
# 2. Хранение информации о читателях (ФИО, email, телефон, адрес)
# 3. Учет выдачи книг читателям
# 4. Хранение истории выдач

# Неправильный подход (одна таблица):
"""
library_bad (
    id,
    book_title,
    book_author,
    book_year,
    book_isbn,
    reader_name,
    reader_email,
    reader_phone,
    loan_date,
    return_date
)
"""

# Проблемы такого подхода:
# - Дублирование информации о книгах и читателях
# - Сложность обновления данных
# - Невозможность эффективного поиска
# - Избыточность данных

print("Анализ требований завершен")
```

### Пример 2: Разделение на сущности

```python
# Правильный подход - несколько связанных таблиц:

# Таблица книг
books = Table('books', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(200), nullable=False),
    Column('author', String(100)),
    Column('year', Integer),
    Column('isbn', String(20), unique=True),
    Column('total_copies', Integer, default=1),
    Column('available_copies', Integer, default=1)
)

# Таблица читателей
readers = Table('readers', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('email', String(100), unique=True),
    Column('phone', String(20)),
    Column('registration_date', DateTime, default=datetime.utcnow)
)

# Таблица выдач
loans = Table('loans', metadata,
    Column('id', Integer, primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('reader_id', Integer, ForeignKey('readers.id')),
    Column('loan_date', DateTime, default=datetime.utcnow),
    Column('return_date', DateTime, nullable=True),
    Column('due_date', DateTime, nullable=False)
)

print("Сущности определены")
```

---

## 2. Нормализация баз данных

Нормализация — это процесс организации данных в базе данных, направленный на устранение избыточности и обеспечение целостности данных.

### Нормальные формы:

| Форма | Описание | Основная цель |
|-------|----------|---------------|
| 1НФ | Первая нормальная форма | Атомарность данных |
| 2НФ | Вторая нормальная форма | Устранение частичных зависимостей |
| 3НФ | Третья нормальная форма | Устранение транзитивных зависимостей |
| БКНФ | Нормальная форма Бойса-Кодда | Устранение аномалий |
| 4НФ | Четвертая нормальная форма | Устранение многозначных зависимостей |
| 5НФ | Пятая нормальная форма | Устранение join-зависимостей |

### Пример 3: Приведение к 1НФ (Первая нормальная форма)

```python
# До нормализации (не 1НФ):
"""
students (
    id,
    name,
    courses -- содержит список курсов через запятую!
)
Пример данных: 1, Иван, "Математика, Физика, Химия"
"""

# Проблема: неатомарные данные, сложность поиска

# После приведения к 1НФ:
student_courses = Table('student_courses', metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
    PrimaryKeyConstraint('student_id', 'course_id')
)

# Теперь данные атомарны - каждый курс в отдельной строке

print("Таблица приведена к 1НФ")
```

### Пример 4: Приведение к 2НФ (Вторая нормальная форма)

```python
# До нормализации (1НФ, но не 2НФ):
"""
enrollments (
    student_id,
    course_id,
    course_name,    -- зависит только от course_id
    course_credits, -- зависит только от course_id
    grade,
    PRIMARY KEY (student_id, course_id)
)

Проблема: course_name и course_credits зависят только от course_id,
но находятся в таблице с составным ключом
"""

# После приведения к 2НФ - вынесение курсов в отдельную таблицу:
courses = Table('courses', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('credits', Integer)
)

enrollments = Table('enrollments', metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('grade', Integer),
    PrimaryKeyConstraint('student_id', 'course_id')
)

print("Таблица приведена к 2НФ")
```

### Пример 5: Приведение к 3НФ (Третья нормальная форма)

```python
# До нормализации (2НФ, но не 3НФ):
"""
students (
    id,
    name,
    department_id,
    department_name,  -- транзитивная зависимость от id через department_id
    department_head
)
"""

# После приведения к 3НФ - вынесение отделов в отдельную таблицу:
departments = Table('departments', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('head', String(100))
)

students = Table('students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('department_id', Integer, ForeignKey('departments.id'))
)

print("Таблица приведена к 3НФ")
```

---

## 3. ER-моделирование (Entity-Relationship)

ER-диаграммы — это визуальное представление сущностей и их взаимосвязей.

### Обозначения:

```
Сущность (Entity)        - Прямоугольник
Атрибут (Attribute)     - Овал
Связь (Relationship)     - Ромб

Типы связей:
--1--   один-к-одному (1:1)
--<     один-ко-многим (1:N)
--<<    многие-ко-многим (M:N)
```

### Пример 6: Создание ER-диаграммы для интернет-магазина

```python
# Опишем структуру базы данных интернет-магазина:

"""
ER-диаграмма:

[Пользователи] 1 --< [Заказы]
     |
     |
     1 (one-to-one)
     |
[Профили]

[Заказы] 1 --< [Товары_заказа]
     |
     |
     M (many-to-many через таблицу связи)
     |
[Товары] --< [Категории]

[Категории] 1 --< [Категории] (иерархия)
"""

# Теперь реализуем это в SQLAlchemy:
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    
    # Один-к-одному с профилем
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    
    # Один-ко-многим с заказами
    orders = relationship("Order", back_populates="user")


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    bio = Column(Text)
    avatar = Column(String(255))


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    status = Column(String(20))
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey('categories.id'))
    
    products = relationship("Product", back_populates="category")
    children = relationship("Category", backref='parent', remote_side=[id])


class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

print("ER-модель создана")
```

---

## 4. Ограничения целостности

Ограничения целостности — это правила, которые обеспечивают корректность данных в базе.

### Пример 7: Определение ограничений

```python
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(
        String(100),
        nullable=False,  # NOT NULL - обязательное поле
        index=True       # Индекс для быстрого поиска
    )
    price = Column(
        Float,
        nullable=False,
        check_constraint('price >= 0')  # Проверка значения
    )
    stock = Column(
        Integer,
        default=0,
        check_constraint('stock >= 0')
    )
    sku = Column(
        String(50),
        unique=True  # UNIQUE - уникальное значение
    )
    created_at = Column(DateTime, default=datetime.utcnow)


# Ограничения на уровне таблицы
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default='pending'
    )
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Составной уникальный ключ
    __table_args__ = (
        UniqueConstraint('user_id', 'status', name='uix_user_status'),
    )

print("Ограничения определены")
```

### Пример 8: Проверка ограничений в SQLAlchemy

```python
from sqlalchemy.exc import IntegrityError

# Попытка добавить товар с отрицательной ценой
try:
    product = Product(
        name="Тестовый товар",
        price=-100,  # Нарушение check constraint
        stock=10
    )
    session.add(product)
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"Ошибка целостности: {e}")

# Попытка добавить дубликат SKU
try:
    product1 = Product(name="Товар 1", price=100, sku="ABC123")
    product2 = Product(name="Товар 2", price=200, sku="ABC123")
    session.add_all([product1, product2])
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"Ошибка уникальности: {e}")
```

---

## 5. Денормализация

Денормализация — это намеренное добавление избыточности данных для повышения производительности.

### Пример 9: Когда нужна денормализация

```python
# Пример: система отчетов
# Нормализованная схема (для транзакций):
"""
orders (id, user_id, date)
order_items (id, order_id, product_id, quantity, price)
products (id, name, price)
users (id, name)
"""

# Для отчетов нужно часто вычислять:
# "Сумма продаж по пользователям за период"
# Это требует JOIN + GROUP BY

# Денормализованное решение - добавление вычисляемых полей:
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # Денормализованное поле - кэш суммы заказов
    total_orders_amount = Column(Float, default=0)
    orders_count = Column(Integer, default=0)


# Обновление при создании заказа
def create_order(user_id, items):
    order = Order(user_id=user_id, items=items)
    total = sum(item.price * item.quantity for item in items)
    
    session.add(order)
    
    # Обновление денормализованных полей
    session.query(User).filter(User.id == user_id).update({
        User.total_orders_amount: User.total_orders_amount + total,
        User.orders_count: User.orders_count + 1
    })
    
    session.commit()

print("Денормализация применена")
```

---

## 6. Практические задания

### Задание 1: Проектирование системы онлайн-обучения
Спроектируйте базу данных для системы онлайн-обучения:
- Студенты (имя, email, дата регистрации)
- Курсы (название, описание, автор, цена)
- Уроки (название, содержание, номер в курсе)
- Записи на курсы (студент, курс, дата записи, прогресс)
- Оценки (студент, урок, оценка, дата)

Определите связи между таблицами и нормализуйте схему.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 2: Приведение к 3НФ
Дана таблица "Автобусные рейсы". Приведите её к 3НФ:

```
travels (id, route_name, driver_name, driver_phone, bus_number, 
         bus_model, departure_time, arrival_time, price)

Определите:
- Какие аномалии здесь есть?
- Какие таблицы нужно создать?
- Какие внешние ключи нужны?
```

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 3: ER-диаграмма для CRM
Создайте ER-диаграмму и модели для CRM-системы:
- Компании (название, адрес, контакт)
- Контакты (имя, email, телефон, компания)
- Сделки (название, сумма, компания, ответственный, статус, дата)
- Задачи (название, описание, исполнитель, связанная сделка, статус)

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 4: Добавление ограничений
Добавьте ограничения для справочной системы:
- Таблица стран (название, код ISO, население)
- Таблица городов (название, страна, население)

Ограничения:
- Код страны ровно 2-3 символа
- Население > 0
- Название страны уникально

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 5: Анализ нормализации
Проанализируйте следующую таблицу и исправьте проблемы:

```
employees (
    id,
    name,
    department_name,
    department_location,
    project_names,  -- через запятую!
    project_start_dates,  -- через запятую!
    skill_names  -- через запятую!
)
```

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 6: Денормализация для отчетности
Спроектируйте схему для системы аналитики с денормализацией:
- Отчеты о продажах по дням
- Суммарные показатели по менеджерам
- Рейтинг товаров по продажам

```python
# ВАШ КОД ЗДЕСЬ
```

---

## Контрольные вопросы:
1. Что такое нормализация базы данных и для чего она нужна?
2. Какие проблемы решает каждая нормальная форма?
3. Чем отличаются 2НФ и 3НФ?
4. Что такое ER-диаграмма и какие элементы она содержит?
5. Какие типы связей бывают между сущностями?
6. Что такое денормализация и когда её следует применять?
7. Какие типы ограничений целостности вы знаете?
8. Какой нормальной форме соответствует ваша текущая база данных?
