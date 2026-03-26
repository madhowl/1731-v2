# Лекция 22: SQLAlchemy ORM

## Основы ORM, модели данных, отношения между таблицами, запросы

### Цель лекции:
- Познакомиться с ORM (Object-Relational Mapping)
- Изучить основы SQLAlchemy и его архитектуру
- Освоить создание моделей данных и отношений
- Научиться выполнять запросы через ORM
- Понять жизненный цикл Session и лучшие практики

### План лекции:
1. Что такое ORM
2. Основы SQLAlchemy и архитектура
3. Создание моделей
4. Отношения между таблицами
5. Запросы через ORM
6. Жизненный цикл Session
7. Лучшие практики

---

## 1. Что такое ORM

ORM (Object-Relational Mapping) — технология программирования, которая позволяет преобразовывать объекты в структуры, используемые в реляционных базах данных, и наоборот.

### ORM как мост между ООП и БД:

```mermaid
graph TB
    subgraph "Python-приложение (ООП)"
        A["Объекты Python<br/>User(name='Иван', age=30)"]
    end
    
    subgraph "ORM слой"
        B[SQLAlchemy ORM<br/>Маппинг объектов]
    end
    
    subgraph "SQL слой"
        C[SQL запросы<br/>INSERT INTO users VALUES...]
    end
    
    subgraph "База данных"
        D[Таблицы БД<br/>users, posts]
    end
    
    A <-->|преобразование| B
    B <-->|генерация SQL| C
    C <-->|выполнение| D
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
```

### Сравнение подходов:

| Подход | Код | Преимущества |
|--------|-----|--------------|
| **Raw SQL (sqlite3)** | `cursor.execute("SELECT * FROM users WHERE age > ?", (25,))` | Полный контроль, производительность |
| **ORM (SQLAlchemy)** | `session.query(User).filter(User.age > 25).all()` | Абстракция, безопасность, переносимость |

### Преимущества ORM:
- **Абстрагирование от SQL** — работа с объектами вместо таблиц
- **Безопасность** — предотвращение SQL-инъекций
- **Переносимость** — возможность работы с разными СУБД без изменения кода
- **Удобство** — более понятный объектно-ориентированный синтаксис
- **Поддержка** — встроенные механизмы валидации, кэширования, миграций
- **Рефакторинг** — легче изменять структуру кода

### Недостатки ORM:
- **Производительность** — возможная задержка по сравнению с чистым SQL
- **Сложность** — дополнительный уровень абстракции
- **Ограничения** — не все SQL-конструкции могут быть представлены
- **N+1 проблема** — риск неэффективных запросов

### Когда использовать ORM:

```mermaid
flowchart TD
    Start([Выбор подхода]) --> Complex{Сложная<br/>логика?}
    Complex -->|Да| ORM[Использовать ORM]
    Complex -->|Нет| Perf{Критична<br/>производительность?}
    
    Perf -->|Да| RawSQL[Raw SQL / Core]
    Perf -->|Нет| Simple{Простые<br/>запросы?}
    
    Simple -->|Да| ORM
    Simple -->|Нет| RawSQL
    
    ORM --> End1([✅ SQLAlchemy ORM])
    RawSQL --> End2([✅ sqlite3 / Core])
    
    style End1 fill:#a5d6a7
    style End2 fill:#fff9c4
```

---

## 2. Основы SQLAlchemy и архитектура

SQLAlchemy — наиболее популярный ORM для Python, предоставляющий гибкие и мощные средства работы с базами данных.

### Архитектура SQLAlchemy:

```mermaid
graph TD
    A[Python-код] --> B[Engine<br/>create_engine<br/>Пул соединений]
    B --> C[Connection<br/>Выполнение запросов]
    C --> D[Session<br/>Unit of Work]
    D --> E[ORM Models<br/>User, Post]
    E --> F[Query Interface<br/>Генерация SQL]
    F --> G[SQLAlchemy Core<br/>Table, MetaData]
    G --> H[DBAPI Driver<br/>sqlite3/psycopg2]
    H --> I[СУБД<br/>SQLite/PostgreSQL]
    
    style B fill:#e1f5fe
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style G fill:#e8f5e9
```

### Два уровня API:

| Уровень | Описание | Когда использовать |
|---------|----------|-------------------|
| **Core** | Низкоуровневый API, работа с таблицами и SQL-выражениями | Сложные запросы, максимальная производительность |
| **ORM** | Высокоуровневый API, работа с объектами-моделями | Бизнес-логика, CRUD-операции |

### Установка:

```bash
# Базовая установка
pip install sqlalchemy

# С дополнительными возможностями
pip install sqlalchemy[asyncio]

# Проверка версии
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

### Подключение к базе данных:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Создание engine - точки подключения к БД
engine = create_engine(
    'sqlite:///example.db',
    echo=True,           # Логирование SQL-запросов (для отладки)
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=10,        # Размер пула соединений
    max_overflow=20      # Максимум дополнительных соединений
)

# Создание базового класса для моделей
Base = declarative_base()

# Создание фабрики сессий
Session = sessionmaker(bind=engine)
session = Session()
```

### URL подключения к разным СУБД:

```mermaid
graph LR
    A[create_engine] --> B[SQLite]
    A --> C[PostgreSQL]
    A --> D[MySQL]
    A --> E[Oracle]
    A --> F[MS SQL Server]
    
    B --> B1["sqlite:///file.db"]
    B --> B2["sqlite:///:memory:"]
    
    C --> C1["postgresql://user:pass@localhost/dbname"]
    C --> C2["postgresql+psycopg2://user:pass@localhost/dbname"]
    
    D --> D1["mysql+pymysql://user:pass@localhost/dbname"]
    
    style B1 fill:#e8f5e9
    style C1 fill:#e3f2fd
    style D1 fill:#fff3e0
```

```python
# SQLite (файл)
engine = create_engine('sqlite:///database.db')

# SQLite (в памяти)
engine = create_engine('sqlite:///:memory:')

# PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5432/dbname')

# MySQL
engine = create_engine('mysql+pymysql://user:password@localhost:3306/dbname')

# С параметрами подключения
engine = create_engine(
    'postgresql://user:password@localhost/dbname',
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,  # Пересоздавать соединения через час
    pool_pre_ping=True  # Проверять перед использованием
)
```

---

## 3. Создание моделей

Модель в SQLAlchemy — это класс Python, который представляет таблицу в базе данных.

### Маппинг класс → таблица:

```mermaid
graph TB
    subgraph "Python класс"
        A["class User(Base)<br/>    id = Column(Integer, PK)<br/>    name = Column(String)"]
    end
    
    subgraph "База данных"
        B["Таблица 'users'<br/>    id INTEGER PRIMARY KEY<br/>    name VARCHAR"]
    end
    
    A <-->|__tablename__| B
    A <-->|"Column()"| B
    
    style A fill:#f3e5f5
    style B fill:#e8f5e9
```

### Пример базовой модели:

```python
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Базовый класс для всех моделей
Base = declarative_base()

class User(Base):
    # Имя таблицы в БД
    __tablename__ = 'users'

    # Столбцы таблицы
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Представление объекта для отладки
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    # Строковое представление
    def __str__(self):
        return f"{self.name} ({self.email})"
```

### Типы данных SQLAlchemy:

```python
from sqlalchemy import (
    String,      # Строка: VARCHAR(n)
    Integer,     # Целое число: INTEGER
    Float,       # Число с плавающей точкой: FLOAT
    Boolean,     # Логический тип: BOOLEAN
    Text,        # Текст переменной длины: TEXT
    DateTime,    # Дата и время: DATETIME
    Date,        # Только дата: DATE
    Time,        # Только время: TIME
    LargeBinary, # Бинарные данные: BLOB
    Numeric,     # Точные числа: DECIMAL
    JSON,        # JSON данные: JSON
    Enum         # Перечисление: ENUM
)

# Примеры использования
Column(String(50))              # Строка до 50 символов
Column(Text)                    # Неограниченный текст
Column(Integer)                 # Целое число
Column(Float(precision=10))     # Число с плавающей точкой
Column(Boolean, default=True)   # Булево значение
Column(DateTime, default=now)   # Дата и время
Column(Numeric(10, 2))          # Число 10 знаков, 2 после запятой
Column(JSON)                    # JSON объект
Column(Enum('admin', 'user'))   # Перечисление
```

### Ограничения и атрибуты столбцов:

```python
from sqlalchemy import Index, UniqueConstraint, CheckConstraint

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    
    # NOT NULL - не может быть пустым
    name = Column(String(100), nullable=False)
    
    # Значение по умолчанию
    price = Column(Float, nullable=False, default=0.0)
    
    # Уникальное значение
    sku = Column(String(50), unique=True)
    
    # Индекс для ускорения поиска
    category_id = Column(Integer, index=True)
    
    # Текст описания
    description = Column(Text)
    
    # В наличии
    in_stock = Column(Boolean, default=True)
    
    # Табличные ограничения
    __table_args__ = (
        # Уникальность по нескольким полям
        UniqueConstraint('name', 'category_id', name='uq_name_category'),
        # Проверочное ограничение
        CheckConstraint('price >= 0', name='chk_price_positive'),
        # Составной индекс
        Index('idx_category_price', 'category_id', 'price'),
    )
```

### Создание таблиц:

```python
# Создание всех таблиц, определённых в Base
Base.metadata.create_all(engine)

# Создание отдельной таблицы
User.__table__.create(engine)

# Проверка существования таблицы
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Таблицы в БД: {tables}")

# Удаление всех таблиц (ОСТОРОЖНО!)
Base.metadata.drop_all(engine)
```

### Метаданные и отражение:

```python
# Доступ к метаданным
print(Base.metadata.tables)  # Все таблицы
print(User.__table__)        # Конкретная таблица

# Автоматическое отражение существующей БД
from sqlalchemy import MetaData, Table

metadata = MetaData()
metadata.reflect(bind=engine)  # Загрузить структуру из БД

# Доступ к отражённой таблице
existing_table = metadata.tables['users']
```

---

## 4. Отношения между таблицами

SQLAlchemy поддерживает все основные типы отношений: один-к-одному, один-ко-многим и многие-ко-многим.

### Типы отношений:

```mermaid
graph LR
    A[Типы отношений] --> B["Один-ко-многим<br/>User → Posts"]
    A --> C["Один-к-одному<br/>User → Profile"]
    A --> D["Многие-ко-многим<br/>Users ↔ Roles"]
    
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

### Отношение один-ко-многим:

```mermaid
erDiagram
    USER ||--o{ POST : "пишет"
    USER {
        int id PK
        string name
        string email
    }
    POST {
        int id PK
        string title
        text content
        int user_id FK
        datetime created_at
    }
```

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

    # Один пользователь имеет много постов
    # back_populates создаёт двустороннюю связь
    posts = relationship(
        "Post",
        back_populates="author",
        lazy="select",      # Загружать при доступе (lazy loading)
        cascade="all, delete-orphan"  # Удалять посты при удалении пользователя
    )

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Внешний ключ
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    # Многие посты принадлежат одному автору
    author = relationship("User", back_populates="posts")
```

### Отношение один-к-одному:

```mermaid
erDiagram
    USER ||--|| PROFILE : "имеет"
    USER {
        int id PK
        string name
        string email
    }
    PROFILE {
        int id PK
        text bio
        string avatar
        int user_id FK
    }
```

```python
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

    # Один к одному: uselist=False
    profile = relationship(
        "UserProfile",
        uselist=False,      # Возвращать объект, а не список
        back_populates="user",
        cascade="all, delete-orphan"
    )

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    bio = Column(Text)
    avatar = Column(String(200))
    
    # Уникальный внешний ключ обеспечивает отношение 1:1
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )

    user = relationship("User", back_populates="profile")
```

### Отношение многие-ко-многим:

```mermaid
erDiagram
    USER ||--o{ USER_ROLE : "имеет"
    ROLE ||--o{ USER_ROLE : "назначен"
    
    USER {
        int id PK
        string name
    }
    ROLE {
        int id PK
        string name
    }
    USER_ROLE {
        int user_id FK
        int role_id FK
    }
```

```python
from sqlalchemy import Table

# Ассоциативная таблица (без модели)
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    Column('assigned_at', DateTime, default=datetime.utcnow),
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

    # Многие ко многим через ассоциативную таблицу
    roles = relationship(
        "Role",
        secondary=user_roles,  # Промежуточная таблица
        back_populates="users",
        lazy="dynamic"  # Возвращать Query для дополнительной фильтрации
    )

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text)

    users = relationship("User", secondary=user_roles, back_populates="roles")
```

### Варианты загрузки связанных данных:

```python
# lazy параметр в relationship():

lazy="select"      # Загружать при доступе (ленивая загрузка, по умолчанию)
lazy="joined"      # Загружать сразу через JOIN (жадная загрузка)
lazy="subquery"    # Загружать отдельным подзапросом
lazy="dynamic"     # Возвращать Query для фильтрации
lazy="selectin"    # Загружать через SELECT IN (эффективно для коллекций)

# Примеры использования:
class User(Base):
    # Ленивая загрузка - посты загружаются при первом обращении
    posts_lazy = relationship("Post", lazy="select")
    
    # Жадная загрузка - посты загружаются сразу с пользователем
    posts_eager = relationship("Post", lazy="joined")
    
    # Динамическая загрузка - можно фильтровать
    posts_dynamic = relationship("Post", lazy="dynamic")
```

### back_populates vs backref:

```python
# back_populates (явное объявление в обоих классах)
class User(Base):
    posts = relationship("Post", back_populates="author")

class Post(Base):
    author = relationship("User", back_populates="posts")

# backref (автоматическое создание обратного отношения)
class User(Base):
    posts = relationship("Post", backref="author")  # author создаётся автоматически

# backref с дополнительными параметрами
class User(Base):
    posts = relationship(
        "Post",
        backref=backref("author", lazy="joined")
    )
```

---

## 5. Запросы через ORM

SQLAlchemy предоставляет мощный интерфейс для выполнения запросов через ORM.

### Интерфейс запросов:

```mermaid
graph TD
    A[session.query] --> B[filter]
    B --> C[order_by]
    C --> D[limit/offset]
    D --> E[all/one/first]
    
    A --> F[join]
    F --> G[options]
    G --> H[eagerload]
    
    style A fill:#e1f5fe
    style E fill:#a5d6a7
    style H fill:#fff3e0
```

### Создание записей:

```python
# Создание нового пользователя
new_user = User(name="Иван Иванов", email="ivan@example.com", age=30)
session.add(new_user)
session.commit()  # Сохраняем изменения

# Получение ID после вставки
print(f"ID нового пользователя: {new_user.id}")

# Создание нескольких записей
users = [
    User(name="Анна Смирнова", email="anna@example.com", age=28),
    User(name="Петр Сидоров", email="petr@example.com", age=35)
]
session.add_all(users)
session.commit()

# Контекстный менеджер для автоматического commit/rollback
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = User(name="Тест", email="test@example.com")
    session.add(user)
    session.commit()  # Автоматический rollback при ошибке
```

### Выборка данных:

```python
# Выборка всех записей
all_users = session.query(User).all()

# Выборка одной записи по ID
user = session.get(User, 1)  # Современный синтаксис SQLAlchemy 2.0+
# или
user = session.query(User).filter(User.id == 1).first()

# Выборка по условию
active_users = session.query(User).filter(User.is_active == True).all()

# Выборка с сортировкой
sorted_users = session.query(User).order_by(User.name.asc()).all()
sorted_users_desc = session.query(User).order_by(User.name.desc()).all()

# Выборка с лимитом и смещением (пагинация)
page = 1
per_page = 10
users_page = session.query(User)\
    .order_by(User.id)\
    .limit(per_page)\
    .offset((page - 1) * per_page)\
    .all()

# Выборка конкретных столбцов
user_names = session.query(User.name, User.email).all()
for name, email in user_names:
    print(f"{name}: {email}")
```

### Фильтрация данных:

```python
from sqlalchemy import and_, or_, not_, func

# Одиночное условие
users = session.query(User).filter(User.age > 18).all()

# Несколько условий (AND)
users = session.query(User).filter(
    User.age > 20,
    User.is_active == True
).all()

# Явное использование and_
users = session.query(User).filter(
    and_(User.age > 20, User.name.like('%Иван%'))
).all()

# Использование or_
users = session.query(User).filter(
    or_(User.age < 18, User.age > 65)
).all()

# Отрицание
users = session.query(User).filter(
    not_(User.is_active)
).all()

# Различные операторы сравнения
users = session.query(User).filter(
    User.name.in_(['Иван', 'Мария']),      # IN
    User.age.between(20, 30),              # BETWEEN
    User.email.like('%@gmail.com'),        # LIKE
    User.name.startswith('А'),             # STARTS WITH
    User.name.endswith('ов'),              # ENDS WITH
    User.age.isnot(None)                   # IS NOT NULL
).all()
```

### Обновление данных:

```python
# Обновление одной записи
user = session.get(User, 1)
if user:
    user.age = 31
    user.email = "newemail@example.com"
    session.commit()

# Массовое обновление
session.query(User)\
    .filter(User.age < 18)\
    .update({User.is_active: False}, synchronize_session=False)
session.commit()

# Инкремент значения
session.query(User)\
    .filter(User.id == 1)\
    .update({User.age: User.age + 1}, synchronize_session=False)
session.commit()
```

### Удаление данных:

```python
# Удаление одной записи
user = session.get(User, 1)
if user:
    session.delete(user)
    session.commit()

# Массовое удаление
session.query(User)\
    .filter(User.is_active == False)\
    .delete(synchronize_session=False)
session.commit()
```

### Агрегатные функции:

```python
from sqlalchemy import func, distinct

# Подсчет записей
count = session.query(func.count(User.id)).scalar()
print(f"Всего пользователей: {count}")

# Подсчет с условием
active_count = session.query(func.count(User.id))\
    .filter(User.is_active == True)\
    .scalar()

# Среднее значение
avg_age = session.query(func.avg(User.age)).scalar()
print(f"Средний возраст: {avg_age:.1f}")

# Максимальное/минимальное значение
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()

# Сумма
total = session.query(func.sum(Product.price)).scalar()

# Группировка
result = session.query(
    User.age,
    func.count(User.id).label('count')
).group_by(User.age).having(func.count(User.id) > 1).all()

for age, count in result:
    print(f"Возраст {age}: {count} человек")

# Подсчет уникальных значений
unique_emails = session.query(func.count(distinct(User.email))).scalar()
```

### JOIN запросы:

```python
# INNER JOIN - только пользователи с постами
result = session.query(User, Post)\
    .join(Post)\
    .filter(Post.title.like('%Python%'))\
    .all()

for user, post in result:
    print(f"{user.name}: {post.title}")

# LEFT JOIN - все пользователи, даже без постов
result = session.query(User)\
    .outerjoin(Post)\
    .all()

# JOIN с условием
result = session.query(User)\
    .join(Post, User.id == Post.user_id)\
    .filter(Post.created_at > datetime(2024, 1, 1))\
    .all()

# Несколько JOIN
result = session.query(User)\
    .join(Post)\
    .join(Comment)\
    .filter(Comment.is_approved == True)\
    .all()
```

### Eager Loading (жадная загрузка):

```python
from sqlalchemy.orm import joinedload, subqueryload, selectinload

# Проблема N+1: 1 запрос на пользователей + N запросов на посты
users = session.query(User).all()
for user in users:
    print(user.posts)  # Выполняется запрос к БД для каждого пользователя

# Решение: joinedload - загрузка через JOIN
users = session.query(User)\
    .options(joinedload(User.posts))\
    .all()
for user in users:
    print(user.posts)  # Данные уже загружены

# subqueryload - загрузка подзапросом (эффективно для коллекций)
users = session.query(User)\
    .options(subqueryload(User.posts))\
    .all()

# selectinload - загрузка через SELECT IN (SQLAlchemy 1.4+)
users = session.query(User)\
    .options(selectinload(User.posts))\
    .all()

# Множественная жадная загрузка
users = session.query(User)\
    .options(
        joinedload(User.profile),
        selectinload(User.posts),
        selectinload(User.roles)
    )\
    .all()
```

### Сравнение стратегий загрузки:

```mermaid
graph TB
    subgraph "Lazy Loading (ленивая)"
        A1[Запрос пользователей] --> A2[Доступ к user.posts]
        A2 --> A3[N дополнительных запросов]
        A3 --> A4[❌ N+1 проблема]
    end
    
    subgraph "Eager Loading (жадная)"
        B1[Запрос с JOIN] --> B2[Все данные сразу]
        B2 --> B3[✅ 1 запрос]
    end
    
    style A4 fill:#ef9a9a
    style B3 fill:#a5d6a7
```

---

## 6. Жизненный цикл Session

Session в SQLAlchemy — это не просто соединение с БД, это паттерн **Unit of Work**, который отслеживает все изменения объектов.

### Состояния объекта в Session:

```mermaid
flowchart TD
    A[Transient<br/>Новый объект<br/>не в сессии] -->|session.add| B[Pending<br/>В сессии<br/>не в БД]
    B -->|session.flush/commit| C[Persistent<br/>В сессии<br/>в БД]
    C -->|session.close/expunge| D[Detached<br/>Не в сессии<br/>в БД]
    D -->|session.merge| C
    C -->|session.delete| E[Deleted<br/>Удалён]
    B -->|session.rollback| A
    C -->|session.rollback| C
    
    style A fill:#fff9c4
    style B fill:#e1f5fe
    style C fill:#a5d6a7
    style D fill:#ffcc80
    style E fill:#ef9a9a
```

### Описание состояний:

| Состояние | Описание | Как перейти |
|-----------|----------|-------------|
| **Transient** | Объект создан в Python, но не добавлен в сессию | `obj = User(...)` |
| **Pending** | Объект добавлен в сессию, но ещё не сохранён в БД | `session.add(obj)` |
| **Persistent** | Объект сохранён в БД и привязан к сессии | `session.commit()` |
| **Detached** | Объект в БД, но сессия закрыта | `session.close()` |
| **Deleted** | Объект помечен на удаление | `session.delete(obj)` |

### Примеры переходов между состояниями:

```python
# 1. Transient - новый объект
user = User(name="Иван", email="ivan@example.com")
print(inspect(user).transient)  # True

# 2. Pending - добавлен в сессию
session.add(user)
print(inspect(user).pending)  # True

# 3. Persistent - сохранён в БД
session.commit()
print(inspect(user).persistent)  # True
print(user.id)  # ID присвоен после commit

# 4. Detached - сессия закрыта
session.close()
print(inspect(user).detached)  # True
# print(user.name)  # Работает, но доступ к связям вызовет ошибку

# 5. Возврат в Persistent
session2 = Session()
session2.merge(user)  # Прикрепить объект к новой сессии
```

### Работа с Unit of Work:

```mermaid
sequenceDiagram
    participant Code as Python-код
    participant Session as Session
    participant IdentityMap as Identity Map
    participant DB as База данных

    Code->>Session: session.add(user)
    Session->>IdentityMap: Регистрация объекта
    Session->>Session: Отметка "new"
    
    Code->>Session: user.name = "Новое имя"
    Session->>IdentityMap: Отметка "dirty"
    
    Code->>Session: session.commit()
    Session->>Session: Анализ изменений
    Session->>DB: INSERT/UPDATE
    DB-->>Session: Результат
    Session->>IdentityMap: Обновление состояния
    Session->>Session: Очистка флагов
```

### Практическое использование:

```python
from sqlalchemy import inspect

# Проверка состояния объекта
inspector = inspect(user)
print(f"Transient: {inspector.transient}")
print(f"Pending: {inspector.pending}")
print(f"Persistent: {inspector.persistent}")
print(f"Detached: {inspector.detached}")

# Получение истории изменений
history = inspector.attrs.name.history
print(f"Было: {history.deleted}")
print(f"Стало: {history.added}")

# Откат изменений конкретного объекта
session.expunge(user)  # Открепить объект от сессии
session.refresh(user)  # Обновить из БД
```

### Управление сессией:

```python
# Явное создание и закрытие
session = Session()
try:
    # Работа с БД
    user = User(name="Тест")
    session.add(user)
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()

# Контекстный менеджер (рекомендуется)
with Session(engine) as session:
    user = User(name="Тест")
    session.add(user)
    session.commit()
    # session.close() вызывается автоматически

# Декоратор для сессии
from functools import wraps

def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return func(session, *args, **kwargs)
    return wrapper

@with_session
def create_user(session, name, email):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user.id
```

---

## 7. Лучшие практики

### 1. N+1 проблема и решение:

```mermaid
graph LR
    subgraph "N+1 Проблема"
        A1[1 запрос: SELECT * FROM users] --> A2[N запросов: SELECT * FROM posts WHERE user_id=?]
        A2 --> A3[❌ 101 запрос для 100 пользователей]
    end
    
    subgraph "Решение: Eager Loading"
        B1[1 запрос с JOIN] --> B2[Все данные сразу]
        B2 --> B3[✅ 1 запрос]
    end
    
    style A3 fill:#ef9a9a
    style B3 fill:#a5d6a7
```

```python
# ❌ ПЛОХО: N+1 проблема
users = session.query(User).all()
for user in users:
    print(user.posts)  # Выполняется запрос для каждого пользователя

# ✅ ХОРОШО: Eager loading с joinedload
users = session.query(User)\
    .options(joinedload(User.posts))\
    .all()
for user in users:
    print(user.posts)  # Данные уже загружены

# ✅ ХОРОШО: selectinload для коллекций
users = session.query(User)\
    .options(selectinload(User.posts))\
    .all()
```

### 2. Управление сессиями:

```python
# ✅ ХОРОШО: Контекстный менеджер
with Session(engine) as session:
    user = User(name="Тест")
    session.add(user)
    session.commit()

# ✅ ХОРОШО: Явный try/except/finally
session = Session()
try:
    session.add(user)
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()

# ❌ ПЛОХО: Без обработки ошибок
session = Session()
session.add(user)
session.commit()
session.close()  # Может не выполниться при ошибке
```

### 3. Безопасность (SQL-инъекции):

```python
# ✅ ХОРОШО: Параметризованные запросы
user = session.query(User)\
    .filter(User.name == user_input)\
    .first()

# ✅ ХОРОШО: text() с параметрами
from sqlalchemy import text
result = session.execute(
    text("SELECT * FROM users WHERE name = :name"),
    {"name": user_input}
)

# ❌ ПЛОХО: Конкатенация строк (уязвимость!)
query = f"SELECT * FROM users WHERE name = '{user_input}'"
result = session.execute(text(query))
```

### 4. Производительность:

```python
# ✅ Использовать пакетные операции
users = [User(name=f"user{i}", email=f"user{i}@example.com") for i in range(1000)]
session.add_all(users)
session.commit()  # Один commit вместо 1000

# ❌ Индивидуальные коммиты
for i in range(1000):
    user = User(name=f"user{i}", email=f"user{i}@example.com")
    session.add(user)
    session.commit()  # 1000 коммитов!

# ✅ Выбирать только нужные столбцы
user_names = session.query(User.name, User.email).all()

# ❌ Выбирать все столбцы
users = session.query(User).all()

# ✅ Использовать exists() для проверки существования
exists = session.query(User.id).filter(User.email == email).first() is not None

# ❌ Загружать весь объект для проверки
user = session.query(User).filter(User.email == email).first()
```

### 5. Миграции схемы БД:

```python
# Alembic - инструмент миграций для SQLAlchemy
# Установка
pip install alembic

# Инициализация
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Add users table"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

### 6. Чек-лист правильной работы с ORM:

```mermaid
flowchart TD
    Start([Начало работы]) --> Config{Настроен<br/>Engine?}
    Config -->|Да| Models{Модели<br/>созданы?}
    Config -->|Нет| ConfigEngine[Создать Engine]
    
    Models -->|Да| Tables{Таблицы<br/>созданы?}
    Models -->|Нет| CreateModels[Создать модели]
    
    Tables -->|Да| Session[Создать Session]
    Tables -->|Нет| CreateTables[Base.metadata.create_all]
    
    Session --> Operations[CRUD операции]
    Operations --> Commit{Есть<br/>изменения?}
    
    Commit -->|Да| DoCommit[session.commit]
    Commit -->|Нет| SkipCommit[Пропустить]
    
    DoCommit --> Close[session.close]
    SkipCommit --> Close
    
    Close --> End([Конец])
    
    style ConfigEngine fill:#e1f5fe
    style CreateModels fill:#fff3e0
    style CreateTables fill:#f3e5f5
    style DoCommit fill:#a5d6a7
    style End fill:#90caf9
```

### 7. Логирование SQL-запросов:

```python
# Включение логирования для отладки
engine = create_engine(
    'sqlite:///example.db',
    echo=True,      # Вывод SQL в консоль
    echo_pool=True  # Вывод событий пула
)

# Логирование через logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Вывод только медленных запросов
from sqlalchemy import event
import time

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > 1.0:  # Логируем запросы дольше 1 секунды
        print(f"Медленный запрос: {total:.3f}s")
        print(f"SQL: {statement}")
```

---

## Контрольные вопросы:

1. В чём разница между Core и ORM в SQLAlchemy?
2. Какие состояния объекта в Session вы знаете?
3. Что такое N+1 проблема и как её решить?
4. В чём разница между `lazy="select"` и `lazy="joined"`?
5. Зачем нужен `back_populates` и чем отличается от `backref`?
6. Что такое Unit of Work?
7. Когда использовать `session.commit()`?
8. Как правильно обрабатывать ошибки при работе с Session?

---


