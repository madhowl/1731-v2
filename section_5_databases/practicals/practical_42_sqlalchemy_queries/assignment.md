# Практическое занятие 42: SQLAlchemy - запросы

## Выполнение запросов к базе данных с использованием SQLAlchemy ORM

### Цель занятия:
Научиться выполнять различные типы запросов к базе данных с использованием SQLAlchemy ORM, включая выборку, фильтрацию, сортировку, агрегацию и изменение данных.

### Задачи:
1. Выполнять простые и сложные запросы к базе данных
2. Использовать фильтрацию, сортировку и пагинацию
3. Применять агрегационные функции
4. Выполнять операции создания, обновления и удаления

### План работы:
1. Основы выполнения запросов
2. Фильтрация данных
3. Сортировка и пагинация
4. Агрегационные функции
5. CRUD операции
6. Практические задания

---

## 1. Основы выполнения запросов

### Пример 1: Базовые операции с сессией

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from datetime import datetime

# Настройка базы данных
engine = create_engine('sqlite:///example.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Пример модели
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Пример работы с сессией
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Использование сессии
db = SessionLocal()
try:
    # Пример запроса
    users = db.query(User).all()
finally:
    db.close()
```

### Пример 2: Простые запросы

```python
from sqlalchemy.orm import Session

def get_all_users(db: Session):
    """Получить всех пользователей"""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """Получить пользователя по ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Получить пользователя по имени пользователя"""
    return db.query(User).filter(User.username == username).first()

def get_active_users(db: Session):
    """Получить всех активных пользователей"""
    return db.query(User).filter(User.is_active == True).all()
```

### Пример 3: Основные методы запросов

```python
def demonstrate_basic_queries(db: Session):
    # query(Model) - создание запроса
    # all() - получить все результаты
    all_users = db.query(User).all()
    
    # first() - получить первый результат или None
    first_user = db.query(User).first()
    
    # one() - получить один результат (бросает исключение, если результатов нет или их несколько)
    try:
        user = db.query(User).filter(User.id == 1).one()
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # scalar() - получить скалярное значение (первое поле первой строки)
    count = db.query(User.id).filter(User.is_active == True).scalar()
    
    # get() - получить объект по первичному ключу
    user_by_pk = db.query(User).get(1)
    
    return all_users, first_user, count, user_by_pk
```

---

## 2. Фильтрация данных

### Пример 4: Базовая фильтрация

```python
def get_users_with_conditions(db: Session):
    # Одиночные условия
    active_users = db.query(User).filter(User.is_active == True).all()
    
    # Несколько условий (AND по умолчанию)
    active_users_with_email = db.query(User).filter(
        User.is_active == True,
        User.email.contains('@example.com')
    ).all()
    
    # OR условия
    from sqlalchemy import or_
    users_or_condition = db.query(User).filter(
        or_(User.is_active == True, User.username.like('%admin%'))
    ).all()
    
    # NOT условия
    from sqlalchemy import not_
    inactive_users = db.query(User).filter(not_(User.is_active)).all()
    
    return active_users, active_users_with_email, users_or_condition, inactive_users
```

### Пример 5: Операторы фильтрации

```python
def demonstrate_filter_operators(db: Session):
    # equals (==)
    user = db.query(User).filter(User.username == 'john_doe').first()
    
    # not equals (!=)
    users = db.query(User).filter(User.username != 'admin').all()
    
    # like и ilike (регистронезависимый like)
    users_like = db.query(User).filter(User.username.like('%doe%')).all()
    
    # in_
    usernames = ['user1', 'user2', 'admin']
    users_in = db.query(User).filter(User.username.in_(usernames)).all()
    
    # notin_
    users_not_in = db.query(User).filter(~User.username.in_(usernames)).all()
    
    # between
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = db.query(User).filter(User.created_at >= week_ago).all()
    
    # is_ и isnot_ (для NULL)
    users_with_full_name = db.query(User).filter(User.full_name.isnot(None)).all()
    
    # contains, startswith, endswith
    users_start_with_a = db.query(User).filter(User.username.startswith('a')).all()
    users_end_with_com = db.query(User).filter(User.email.endswith('.com')).all()
    
    return user, users_like, users_in, recent_users, users_with_full_name
```

---

## 3. Сортировка и пагинация

### Пример 6: Сортировка

```python
def get_sorted_users(db: Session):
    # Сортировка по одному полю (ASC по умолчанию)
    users_by_username = db.query(User).order_by(User.username).all()
    
    # Сортировка по убыванию
    users_by_id_desc = db.query(User).order_by(User.id.desc()).all()
    
    # Множественная сортировка
    users_multi_sort = db.query(User).order_by(
        User.is_active.desc(),
        User.created_at.desc(),
        User.username.asc()
    ).all()
    
    # Сортировка по вычисленным полям
    from sqlalchemy import func
    users_with_count = db.query(
        User,
        func.length(User.username).label('username_length')
    ).order_by(func.length(User.username).desc()).all()
    
    return users_by_username, users_by_id_desc, users_multi_sort
```

### Пример 7: Пагинация

```python
def get_users_paginated(db: Session, skip: int = 0, limit: int = 10):
    """Получить пользователей с пагинацией"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_users_with_pagination_and_count(db: Session, page: int = 1, per_page: int = 10):
    """Получить пользователей с пагинацией и общим количеством"""
    offset = (page - 1) * per_page
    
    # Получение данных
    users = db.query(User).offset(offset).limit(per_page).all()
    
    # Получение общего количества
    total_count = db.query(User).count()
    
    return {
        'users': users,
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'pages': (total_count + per_page - 1) // per_page
    }

def search_users_paginated(db: Session, search_term: str = None, page: int = 1, per_page: int = 10):
    """Поиск пользователей с пагинацией"""
    offset = (page - 1) * per_page
    
    query = db.query(User)
    
    if search_term:
        query = query.filter(
            User.username.contains(search_term) |
            User.email.contains(search_term) |
            User.full_name.contains(search_term)
        )
    
    users = query.offset(offset).limit(per_page).all()
    total_count = query.count()
    
    return {
        'users': users,
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'pages': (total_count + per_page - 1) // per_page
    }
```

---

## 4. Агрегационные функции

### Пример 8: Базовые агрегационные функции

```python
from sqlalchemy import func

def get_aggregated_data(db: Session):
    # Подсчет
    total_users = db.query(func.count(User.id)).scalar()
    active_users_count = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    # Сумма (для числовых полей)
    # total_score = db.query(func.sum(User.score)).scalar()
    
    # Среднее значение
    # avg_score = db.query(func.avg(User.score)).scalar()
    
    # Максимальное и минимальное значения
    # max_score = db.query(func.max(User.score)).scalar()
    # min_score = db.query(func.min(User.score)).scalar()
    
    # Группировка
    user_counts_by_status = db.query(
        User.is_active,
        func.count(User.id).label('count')
    ).group_by(User.is_active).all()
    
    # Группировка с фильтрацией
    user_counts_by_status_filtered = db.query(
        User.is_active,
        func.count(User.id).label('count')
    ).group_by(User.is_active).having(func.count(User.id) > 1).all()
    
    return {
        'total_users': total_users,
        'active_users_count': active_users_count,
        'user_counts_by_status': user_counts_by_status
    }
```

### Пример 9: Продвинутые агрегационные запросы

```python
def advanced_aggregation_examples(db: Session):
    # Подзапросы
    from sqlalchemy import exists
    
    # Проверка существования
    has_admin_user = db.query(exists().where(User.username.like('%admin%'))).scalar()
    
    # Сложные агрегации с условиями
    stats = db.query(
        func.count(User.id).label('total'),
        func.sum(case([(User.is_active, 1)], else_=0)).label('active_count'),
        func.avg(case([(User.is_active, 1)], else_=0)).label('active_ratio')
    ).first()
    
    # Использование case для условной агрегации
    from sqlalchemy import case
    user_categories = db.query(
        case(
            [(User.created_at > datetime.utcnow() - timedelta(days=7), 'new')],
            [(User.is_active, 'active')],
            else_='inactive'
        ).label('category'),
        func.count(User.id)
    ).group_by('category').all()
    
    return stats, user_categories
```

---

## 5. CRUD операции

### Пример 10: Создание данных

```python
def create_user(db: Session, username: str, email: str, full_name: str = None):
    """Создать нового пользователя"""
    db_user = User(
        username=username,
        email=email,
        full_name=full_name,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Обновить объект из базы данных
    return db_user

def create_multiple_users(db: Session, users_data: list):
    """Создать несколько пользователей за один раз"""
    db_users = [User(**user_data) for user_data in users_data]
    db.add_all(db_users)
    db.commit()
    
    # Обновить все объекты
    for user in db_users:
        db.refresh(user)
    
    return db_users
```

### Пример 11: Обновление данных

```python
def update_user(db: Session, user_id: int, **kwargs):
    """Обновить пользователя по ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    # Обновление полей
    for key, value in kwargs.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def bulk_update_users(db: Session, condition_field, condition_value, **updates):
    """Массовое обновление пользователей"""
    query = db.query(User).filter(getattr(User, condition_field) == condition_value)
    query.update(updates)
    db.commit()
    return query.rowcount  # Возвращает количество затронутых строк

def conditional_update(db: Session, user_id: int, new_email: str):
    """Условное обновление"""
    from sqlalchemy import and_
    
    result = db.query(User).filter(
        and_(
            User.id == user_id,
            User.is_active == True  # Только для активных пользователей
        )
    ).update({"email": new_email})
    
    db.commit()
    return result
```

### Пример 12: Удаление данных

```python
def delete_user(db: Session, user_id: int):
    """Удалить пользователя по ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def bulk_delete_users(db: Session, status: bool = None):
    """Массовое удаление пользователей"""
    query = db.query(User)
    if status is not None:
        query = query.filter(User.is_active == status)
    
    deleted_count = query.delete()
    db.commit()
    return deleted_count

def soft_delete_user(db: Session, user_id: int):
    """Мягкое удаление (деактивация) пользователя"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user
```

---

## 6. Сложные запросы и соединения

### Пример 13: JOIN операции

```python
# Определение дополнительных моделей для примера JOIN
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

def get_products_with_categories(db: Session):
    """Получить продукты с их категориями (INNER JOIN)"""
    products = db.query(Product, Category).join(Category).all()
    return products

def get_all_categories_with_products(db: Session):
    """Получить все категории, включая те, у которых нет продуктов (LEFT JOIN)"""
    from sqlalchemy.orm import joinedload
    
    categories = db.query(Category).options(joinedload(Category.products)).all()
    return categories

def get_product_details(db: Session):
    """Получить детали продукта с именем категории"""
    result = db.query(
        Product.name.label('product_name'),
        Product.price,
        Category.name.label('category_name')
    ).join(Category).all()
    
    return result
```

### Пример 14: Подзапросы

```python
def get_users_with_most_recent_posts(db: Session):
    """Получить пользователей с самым последним постом"""
    from sqlalchemy import desc
    
    # Подзапрос для получения последней даты поста для каждого пользователя
    latest_post_subquery = db.query(
        Post.user_id,
        func.max(Post.created_at).label('latest_post_date')
    ).group_by(Post.user_id).subquery()
    
    # Основной запрос
    result = db.query(User, latest_post_subquery.c.latest_post_date).join(
        latest_post_subquery,
        User.id == latest_post_subquery.c.user_id
    ).all()
    
    return result
```

---

## 7. Практические задания

### Задание 1: Базовые запросы
Создайте функции для:
- Получения всех пользователей
- Получения пользователя по ID
- Получения пользователей по статусу активности

### Задание 2: Фильтрация
Реализуйте фильтрацию пользователей по:
- Имени пользователя (с использованием like)
- Email домену
- Дате регистрации
- Комбинации условий с OR и AND

### Задание 3: Сортировка и пагинация
Создайте функцию для получения пользователей с:
- Сортировкой по нескольким полям
- Пагинацией
- Поиском и фильтрацией

### Задание 4: Агрегация
Реализуйте:
- Подсчет общего количества пользователей
- Подсчет по статусу активности
- Группировку пользователей по дате регистрации

### Задание 5: CRUD операции
Создайте полный набор функций CRUD для сущности:
- Создание
- Чтение (один и список)
- Обновление
- Удаление

---

## 8. Дополнительные задания

### Задание 6: Сложные JOIN запросы
Создайте запросы с соединением нескольких таблиц.

### Задание 7: Подзапросы
Реализуйте запросы с использованием подзапросов.

### Задание 8: Транзакции
Используйте транзакции для обеспечения целостности данных.

---

## Контрольные вопросы:
1. Как выполнить простой запрос на выборку?
2. Какие методы фильтрации данных доступны?
3. Как реализовать пагинацию в SQLAlchemy?
4. Какие агрегационные функции можно использовать?
5. Как выполнить операции CRUD в SQLAlchemy?