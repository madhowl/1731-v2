"""
Практическое занятие 40: Связи в SQLAlchemy
Решение упражнений

Отношения между таблицами: один-ко-многим, один-к-одному, многие-ко-многим
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Создание движка для базы данных в памяти
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# ============================================================================
# Задание 1: Система блога
# ============================================================================

# Ассоциативная таблица для связи многие-ко-многим (посты и теги)
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Author(Base):
    """Модель автора блога"""
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    bio = Column(Text)
    
    # Связь один-ко-многим: автор -> посты
    posts = relationship("Post", back_populates="author")
    
    def __repr__(self):
        return f"<Author({self.name})>"


class Post(Base):
    """Модель поста блога"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    published_date = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('authors.id'))
    
    # Связь многие-ко-многим с тегами
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    
    # Связь с автором (многие-к-одному)
    author = relationship("Author", back_populates="posts")
    
    def __repr__(self):
        return f"<Post({self.title})>"


class Tag(Base):
    """Модель тега"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Связь многие-ко-многим с постами
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag({self.name})>"


# Создание всех таблиц
Base.metadata.create_all(engine)


def create_blog_system():
    """Создание системы блога"""
    
    print("="*70)
    print("Задание 1-3: Система блога")
    print("="*70)
    
    # Создание авторов
    author1 = Author(
        name='Иван Петров',
        email='ivan.petrov@blog.ru',
        bio='Python разработчик, любитель хороших статей'
    )
    
    author2 = Author(
        name='Анна Смирнова',
        email='anna.smirnova@blog.ru',
        bio='Data Science энтузиаст'
    )
    
    session.add_all([author1, author2])
    session.commit()
    
    # Создание тегов
    tags = [
        Tag(name='Python'),
        Tag(name='SQL'),
        Tag(name='Базы данных'),
        Tag(name='Веб-разработка'),
        Tag(name='Машинное обучение')
    ]
    
    session.add_all(tags)
    session.commit()
    
    # Создание постов
    post1 = Post(
        title='Введение в SQLAlchemy',
        content='SQLAlchemy - это библиотека Python для работы с базами данных...',
        author=author1
    )
    
    post2 = Post(
        title='Основы ORM',
        content='ORM (Object-Relational Mapping) - это техника...',
        author=author1
    )
    
    post3 = Post(
        title='Python для анализа данных',
        content='Python стал одним из самых популярных языков...',
        author=author2
    )
    
    post4 = Post(
        title='Создание веб-приложений с Flask',
        content='Flask - это легковесный веб-фреймворк...',
        author=author2
    )
    
    session.add_all([post1, post2, post3, post4])
    session.commit()
    
    # Связывание постов с тегами
    post1.tags = [tags[0], tags[1], tags[2]]  # SQLAlchemy, SQL, Базы данных
    post2.tags = [tags[0], tags[3]]  # Python, Веб-разработка
    post3.tags = [tags[0], tags[4]]  # Python, Машинное обучение
    post4.tags = [tags[0], tags[3]]  # Python, Веб-разработка
    
    session.commit()
    
    print(f"\nСоздано:")
    print(f"  - Авторов: 2")
    print(f"  - Постов: 4")
    print(f"  - Тегов: 5")
    
    return author1, author2, post1, post2, post3, post4, tags


authors, posts, tags = create_blog_system()


# ============================================================================
# Задание 3: Запросы к связанным данным
# ============================================================================

def query_related_data():
    """Запросы к связанным данным"""
    
    print("\nЗадание 3: Запросы к связанным данным")
    
    # 1. Получение всех постов автора
    print("\n1. Все посты автора Иван Петров:")
    author = session.query(Author).filter(Author.name == 'Иван Петров').first()
    if author:
        for post in author.posts:
            print(f"   - {post.title}")
            print(f"     Дата: {post.published_date.strftime('%d.%m.%Y')}")
    
    # 2. Получение всех тегов поста
    print("\n2. Теги поста 'Введение в SQLAlchemy':")
    post = session.query(Post).filter(
        Post.title == 'Введение в SQLAlchemy'
    ).first()
    if post:
        for tag in post.tags:
            print(f"   - {tag.name}")
    
    # 3. Поиск постов по тегу
    print("\n3. Посты с тегом 'Python':")
    python_tag = session.query(Tag).filter(Tag.name == 'Python').first()
    if python_tag:
        for post in python_tag.posts:
            print(f"   - {post.title} (автор: {post.author.name})")
    
    # Дополнительно: JOIN запрос
    print("\n4. Все посты с авторами (через JOIN):")
    results = session.query(Post.title, Author.name).join(
        Author, Post.author_id == Author.id
    ).all()
    
    for title, author_name in results:
        print(f"   - {title} | Автор: {author_name}")


query_related_data()


# ============================================================================
# Задание 4: Интернет-магазин
# ============================================================================

# Создаем новые таблицы для магазина
class Category(Base):
    """Модель категории товаров"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    
    # Self-referential отношение для иерархии категорий
    parent = relationship("Category", remote_side=[id], backref="children")
    
    # Связь один-ко-многим с товарами
    products = relationship("StoreProduct", back_populates="category")
    
    def __repr__(self):
        return f"<Category({self.name})>"


class StoreProduct(Base):
    """Модель товара магазина"""
    __tablename__ = 'store_products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    # Связь с категорией
    category = relationship("Category", back_populates="products")
    
    # Связь многие-ко-многим с заказами
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<StoreProduct({self.name}, {self.price} руб.)>"


class StoreOrder(Base):
    """Модель заказа"""
    __tablename__ = 'store_orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='new')
    
    # Связь один-ко-многим с позициями заказа
    items = relationship("OrderItem", back_populates="order")
    
    def __repr__(self):
        return f"<Order(#{self.id}, {self.status})>"


class OrderItem(Base):
    """Модель позиции заказа"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('store_orders.id'))
    product_id = Column(Integer, ForeignKey('store_products.id'))
    quantity = Column(Integer, default=1)
    price = Column(Integer)  # Цена на момент заказа
    
    # Связи
    order = relationship("StoreOrder", back_populates="items")
    product = relationship("StoreProduct", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(Товар: {self.product_id}, кол-во: {self.quantity})>"


# Создание таблиц магазина
Base.metadata.create_all(engine)


def create_online_store():
    """Создание интернет-магазина"""
    
    print("\n" + "="*70)
    print("Задание 4-6: Интернет-магазин")
    print("="*70)
    
    # Создание категорий (с иерархией)
    electronics = Category(name='Электроника')
    session.add(electronics)
    session.commit()
    
    smartphones = Category(name='Смартфоны', parent=electronics)
    laptops = Category(name='Ноутбуки', parent=electronics)
    
    session.add_all([smartphones, laptops])
    session.commit()
    
    # Создание товаров
    products = [
        StoreProduct(name='iPhone 15', price=99999, category=smartphones),
        StoreProduct(name='Samsung Galaxy S24', price=79999, category=smartphones),
        StoreProduct(name='ASUS VivoBook', price=45999, category=laptops),
        StoreProduct(name='MacBook Air', price=89999, category=laptops),
        StoreProduct(name='Sony WH-1000XM5', price=24999, category=electronics),
    ]
    
    session.add_all(products)
    session.commit()
    
    # Создание заказа
    order = StoreOrder(status='processing')
    session.add(order)
    session.commit()
    
    # Добавление позиций заказа
    order_items = [
        OrderItem(order=order, product=products[0], quantity=1, price=products[0].price),
        OrderItem(order=order, product=products[2], quantity=1, price=products[2].price),
    ]
    
    session.add_all(order_items)
    session.commit()
    
    print(f"\nСоздано:")
    print(f"  - Категорий: 3 (Электроника + 2 подкатегории)")
    print(f"  - Товаров: {len(products)}")
    print(f"  - Заказов: 1")
    print(f"  - Позиций в заказе: {len(order_items)}")
    
    return electronics, smartphones, products, order


electronics, smartphones, store_products, order = create_online_store()


# ============================================================================
# Задание 6: Подсчет статистики
# ============================================================================

def store_statistics():
    """Подсчет статистики магазина"""
    
    print("\nЗадание 6: Статистика магазина")
    
    from sqlalchemy import func
    
    # Количество товаров в каждой категории
    print("\n1. Количество товаров по категориям:")
    
    # Все категории с подкатегориями
    all_categories = session.query(Category).all()
    for cat in all_categories:
        # Подсчет товаров в категории и подкатегориях
        count = session.query(func.count(StoreProduct.id)).filter(
            StoreProduct.category_id == cat.id
        ).scalar()
        print(f"   - {cat.name}: {count} товаров")
    
    # Товары в категории Электроника (включая подкатегории)
    print("\n2. Все товары категории 'Электроника' (с подкатегориями):")
    
    # Получаем все id категорий (включая дочерние)
    cat_ids = [electronics.id, smartphones.id]
    electronics_products = session.query(StoreProduct).filter(
        StoreProduct.category_id.in_(cat_ids)
    ).all()
    
    for p in electronics_products:
        print(f"   - {p.name}: {p.price} руб. (категория: {p.category.name})")
    
    # Общая сумма заказа
    print("\n3. Детализация заказа:")
    total = 0
    for item in order.items:
        item_total = item.price * item.quantity
        total += item_total
        print(f"   - {item.product.name}: {item.price} x {item.quantity} = {item_total} руб.")
    print(f"   Итого: {total} руб.")


store_statistics()


# ============================================================================
# Задание 7: Социальная сеть
# ============================================================================

class User(Base):
    """Модель пользователя социальной сети"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    
    # Self-referential many-to-many для друзей
    friends = relationship(
        "User",
        secondary="friendships",
        primaryjoin="User.id==friendships.c.user_id",
        secondaryjoin="User.id==friendships.c.friend_id",
        backref="friends_of"
    )
    
    def __repr__(self):
        return f"<User({self.name})>"


# Ассоциативная таблица для друзей
friendships = Table(
    'friendships',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)


# Создание таблиц социальной сети
Base.metadata.create_all(engine)


def create_social_network():
    """Создание системы друзей"""
    
    print("\n" + "="*70)
    print("Задание 7: Социальная сеть")
    print("="*70)
    
    # Создание пользователей
    users = [
        User(name='Алексей', email='alexey@social.ru'),
        User(name='Мария', email='maria@social.ru'),
        User(name='Петр', email='petr@social.ru'),
        User(name='Елена', email='elena@social.ru'),
        User(name='Иван', email='ivan@social.ru'),
    ]
    
    session.add_all(users)
    session.commit()
    
    # Создание дружеских связей (взаимных)
    users[0].friends.append(users[1])  # Алексей -> Мария
    users[0].friends.append(users[2])  # Алексей -> Петр
    users[1].friends.append(users[0])  # Мария -> Алексей
    users[1].friends.append(users[3])  # Мария -> Елена
    users[2].friends.append(users[0])  # Петр -> Алексей
    users[2].friends.append(users[4])  # Петр -> Иван
    users[3].friends.append(users[1])  # Елена -> Мария
    
    session.commit()
    
    # Найти всех друзей пользователя
    print("\n1. Друзья пользователя Алексей:")
    alexey = session.query(User).filter(User.name == 'Алексей').first()
    for friend in alexey.friends:
        print(f"   - {friend.name}")
    
    # Друзья друзей (рекомендации)
    print("\n2. Друзья друзей (потенциальные знакомые):")
    friends_of_friends = set()
    for friend in alexey.friends:
        for friends_friend in friend.friends:
            if friends_friend != alexey and friends_friend not in alexey.friends:
                friends_of_friends.add(friends_friend.name)
    
    for name in friends_of_friends:
        print(f"   - {name}")
    
    # Количество друзей у каждого
    print("\n3. Количество друзей у каждого пользователя:")
    all_users = session.query(User).all()
    for user in all_users:
        print(f"   - {user.name}: {len(user.friends)} друзей")


create_social_network()


# ============================================================================
# Задание 8: Иерархия категорий
# ============================================================================

def hierarchy_example():
    """Пример работы с иерархией категорий"""
    
    print("\n" + "="*70)
    print("Задание 8: Иерархия категорий")
    print("="*70)
    
    # Дополнительные категории для демонстрации
    # Уже созданы: Электроника -> Смартфоны, Ноутбуки
    
    # Добавим еще одну ветку
    appliances = Category(name='Бытовая техника')
    session.add(appliances)
    session.commit()
    
    kitchen = Category(name='Кухонная техника', parent=appliances)
    cleaning = Category(name='Техника для уборки', parent=appliances)
    
    session.add_all([kitchen, cleaning])
    session.commit()
    
    # Найти все подкатегории
    print("\n1. Все подкатегории 'Электроника':")
    electronics = session.query(Category).filter(
        Category.name == 'Электроника'
    ).first()
    
    if electronics:
        for child in electronics.children:
            print(f"   - {child.name}")
    
    print("\n2. Все подкатегории 'Бытовая техника':")
    appliances = session.query(Category).filter(
        Category.name == 'Бытовая техника'
    ).first()
    
    if appliances:
        for child in appliances.children:
            print(f"   - {child.name}")
    
    # Вывод всей иерархии (рекурсивно)
    def print_hierarchy(category, indent=0):
        print(" " * indent + f"├── {category.name}")
        for child in category.children:
            print_hierarchy(child, indent + 2)
    
    print("\n3. Полная иерархия категорий:")
    root_categories = session.query(Category).filter(
        Category.parent_id == None
    ).all()
    
    for root in root_categories:
        print_hierarchy(root)


hierarchy_example()


# ============================================================================
# Дополнительные примеры
# ============================================================================

print("\n" + "="*70)
print("ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ")
print("="*70)


def one_to_one_example():
    """Пример отношения один-к-одному"""
    
    print("\n1. Отношение один-к-одному:")
    
    # Пример: User и UserProfile (уже определены выше в файле)
    # Пересоздадим для примера
    
    class User1(Base):
        __tablename__ = 'users_one_to_one'
        id = Column(Integer, primary_key=True)
        username = Column(String(50))
        email = Column(String(100))
        
        # uselist=False делает отношение один-к-одному
        profile = relationship("UserProfile1", back_populates="user", uselist=False)
    
    class UserProfile1(Base):
        __tablename__ = 'user_profiles_one_to_one'
        id = Column(Integer, primary_key=True)
        bio = Column(Text)
        avatar_url = Column(String(255))
        user_id = Column(Integer, ForeignKey('users_one_to_one.id'), unique=True)
        
        user = relationship("User1", back_populates="profile")
    
    Base.metadata.create_all(engine)
    
    # Создание пользователя с профилем
    user = User1(username='test_user', email='test@example.com')
    user.profile = UserProfile1(bio='Мой профиль', avatar_url='/avatars/user.png')
    
    session.add(user)
    session.commit()
    
    # Доступ к профилю
    print(f"   Пользователь: {user.username}")
    print(f"   Профиль: {user.profile.bio}")
    print(f"   Аватар: {user.profile.avatar_url}")


one_to_one_example()


def cascade_example():
    """Пример каскадных операций"""
    
    print("\n2. Каскадные операции:")
    
    class Parent(Base):
        __tablename__ = 'parents'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        
        children = relationship("Child1", back_populates="parent", 
                               cascade="all, delete-orphan")
    
    class Child1(Base):
        __tablename__ = 'children'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        parent_id = Column(Integer, ForeignKey('parents.id'))
        
        parent = relationship("Parent", back_populates="children")
    
    Base.metadata.create_all(engine)
    
    # Создание родителя с детьми
    parent = Parent(name="Иван Иванович")
    parent.children = [
        Child1(name="Алексей"),
        Child1(name="Мария"),
        Child1(name="Петр")
    ]
    
    session.add(parent)
    session.commit()
    
    print(f"   Создан родитель: {parent.name}")
    print(f"   У него {len(parent.children)} детей")
    
    # При удалении родителя автоматически удалятся и дети
    parent_id = parent.id
    session.delete(parent)
    session.commit()
    
    # Проверим, что дети удалены
    children_count = session.query(Child1).filter(
        Child1.parent_id == parent_id
    ).count()
    
    print(f"   После удаления родителя детей в базе: {children_count}")


cascade_example()


def join_examples():
    """Примеры JOIN запросов"""
    
    print("\n3. JOIN запросы:")
    
    # JOIN через relationship
    print("   Посты с информацией об авторе (через relationship):")
    posts_with_authors = session.query(Post, Author).join(
        Author, Post.author_id == Author.id
    ).all()
    
    for post, author in posts_with_authors[:3]:
        print(f"   - '{post.title}' | Автор: {author.name}")
    
    # Фильтрация через связанные объекты
    print("\n   Посты автора 'Анна Смирнова':")
    anna_posts = session.query(Post).join(
        Author, Post.author_id == Author.id
    ).filter(Author.name == 'Анна Смирнова').all()
    
    for post in anna_posts:
        print(f"   - {post.title}")


join_examples()


print("\n" + "="*70)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*70)
