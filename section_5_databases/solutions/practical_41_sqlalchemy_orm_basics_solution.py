"""
Практическое занятие 39: Основы SQLAlchemy ORM
Решение упражнений

Модели, базовые операции CRUD, запросы
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Создание движка для базы данных в памяти
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# ============================================================================
# Задание 1: Создание модели товара
# ============================================================================

class Product(Base):
    """Модель товара для интернет-магазина"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_available = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Product({self.name}, {self.price} руб., на складе: {self.stock})>"
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."


# Создание таблицы
Base.metadata.create_all(engine)


# ============================================================================
# Задание 2: Заполнение базы данных
# ============================================================================

def add_products():
    """Добавление 5 товаров в таблицу"""
    products = [
        Product(
            name='Ноутбук ASUS VivoBook',
            description='15.6 дюймов, Intel Core i5, 8GB RAM',
            price=45999.00,
            stock=15,
            category='Электроника',
            is_available=True
        ),
        Product(
            name='Смартфон Samsung Galaxy',
            description='6.5 дюймов, 128GB, черный',
            price=32999.00,
            stock=25,
            category='Электроника',
            is_available=True
        ),
        Product(
            name='Наушники Sony WH-1000XM4',
            description='Беспроводные, шумоподавление',
            price=19999.00,
            stock=8,
            category='Электроника',
            is_available=True
        ),
        Product(
            name='Книга "Python для начинающих"',
            description='Учебное пособие по программированию',
            price=890.00,
            stock=50,
            category='Книги',
            is_available=True
        ),
        Product(
            name='Кофемашина DeLonghi',
            description='Автоматическая, 15 бар',
            price=15999.00,
            stock=5,
            category='Бытовая техника',
            is_available=True
        )
    ]
    
    session.add_all(products)
    session.commit()
    
    print("Задание 2: Добавлено 5 товаров")
    for p in products:
        print(f"  - {p}")
    
    return products


# Выполнение добавления товаров
products = add_products()


# ============================================================================
# Задание 3: Поиск товаров
# ============================================================================

def search_products():
    """Поиск товаров по различным критериям"""
    
    print("\nЗадание 3: Поиск товаров")
    
    # 1. Нахождение всех доступных товаров
    available = session.query(Product).filter(
        Product.is_available == True
    ).all()
    print(f"\n1. Доступные товары ({len(available)} шт.):")
    for p in available:
        print(f"   - {p.name}")
    
    # 2. Нахождение товаров с ценой в диапазоне 1000-5000
    price_range = session.query(Product).filter(
        Product.price.between(1000, 5000)
    ).all()
    print(f"\n2. Товары с ценой 1000-5000 руб. ({len(price_range)} шт.):")
    if price_range:
        for p in price_range:
            print(f"   - {p.name}: {p.price} руб.")
    else:
        print("   (нет товаров в этом диапазоне)")
    
    # 3. Нахождение товаров определенной категории
    electronics = session.query(Product).filter(
        Product.category == 'Электроника'
    ).all()
    print(f"\n3. Товары категории 'Электроника' ({len(electronics)} шт.):")
    for p in electronics:
        print(f"   - {p.name}: {p.price} руб.")


search_products()


# ============================================================================
# Задание 4: Обновление данных
# ============================================================================

def update_product_prices():
    """Обновление цен товаров категории 'Электроника'"""
    
    print("\nЗадание 4: Обновление цен")
    
    # Покажем цены до обновления
    electronics_before = session.query(Product).filter(
        Product.category == 'Электроника'
    ).all()
    
    print("Цены до обновления:")
    for p in electronics_before:
        print(f"   - {p.name}: {p.price} руб.")
    
    # Обновление: увеличение цены на 15%
    updated_count = session.query(Product).filter(
        Product.category == 'Электроника'
    ).update({
        Product.price: Product.price * 1.15
    })
    
    session.commit()
    
    # Покажем цены после обновления
    electronics_after = session.query(Product).filter(
        Product.category == 'Электроника'
    ).all()
    
    print(f"\nОбновлено {updated_count} товаров")
    print("Цены после обновления ( +15% ):")
    for p in electronics_after:
        print(f"   - {p.name}: {p.price:.2f} руб.")


update_product_prices()


# ============================================================================
# Задание 5: Статистика товаров
# ============================================================================

from sqlalchemy import func, count, avg, sum as sql_sum

def get_product_statistics():
    """Получение статистики по товарам"""
    
    print("\nЗадание 5: Статистика товаров")
    
    # 1. Общее количество товаров
    total_count = session.query(func.count(Product.id)).scalar()
    print(f"\n1. Общее количество товаров: {total_count}")
    
    # 2. Средняя цена товара
    average_price = session.query(func.avg(Product.price)).scalar()
    print(f"2. Средняя цена товара: {average_price:.2f} руб.")
    
    # 3. Общая стоимость всех товаров на складе
    # (цена * количество на складе для каждого товара)
    total_value = session.query(
        func.sum(Product.price * Product.stock)
    ).scalar()
    print(f"3. Общая стоимость товаров на складе: {total_value:,.2f} руб.")
    
    # Дополнительная статистика
    max_price = session.query(func.max(Product.price)).scalar()
    min_price = session.query(func.min(Product.price)).scalar()
    total_stock = session.query(func.sum(Product.stock)).scalar()
    
    print(f"\nДополнительная статистика:")
    print(f"   - Максимальная цена: {max_price:.2f} руб.")
    print(f"   - Минимальная цена: {min_price:.2f} руб.")
    print(f"   - Всего единиц на складе: {total_stock}")


get_product_statistics()


# ============================================================================
# Задание 6: Удаление данных
# ============================================================================

def delete_out_of_stock_products():
    """Удаление товаров с нулевым количеством на складе"""
    
    print("\nЗадание 6: Удаление данных")
    
    # Добавим товар с нулевым складом для демонстрации
    out_of_stock = Product(
        name='Товар для удаления',
        description='Товар с нулевым складом',
        price=999.00,
        stock=0,
        category='Тест',
        is_available=False
    )
    session.add(out_of_stock)
    session.commit()
    
    # Покажем товары с нулевым складом до удаления
    zero_stock = session.query(Product).filter(Product.stock == 0).all()
    print(f"Товары с нулевым складом до удаления ({len(zero_stock)} шт.):")
    for p in zero_stock:
        print(f"   - {p.name}")
    
    # Удаление товаров с нулевым количеством
    deleted_count = session.query(Product).filter(
        Product.stock == 0
    ).delete()
    
    session.commit()
    
    print(f"\nУдалено товаров: {deleted_count}")


delete_out_of_stock_products()


# ============================================================================
# Задание 7: Создание полной модели библиотеки
# ============================================================================

class Book(Base):
    """Модель книги для библиотечной системы"""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100))
    isbn = Column(String(20), unique=True)
    year = Column(Integer)
    genre = Column(String(50))
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    
    def __repr__(self):
        return f"<Book({self.title}, {self.author})>"


class Reader(Base):
    """Модель читателя библиотеки"""
    __tablename__ = 'readers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    registration_date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Reader({self.last_name} {self.first_name})>"


class Loan(Base):
    """Модель выдачи книги"""
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    reader_id = Column(Integer, ForeignKey('readers.id'))
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Loan(Книга ID: {self.book_id}, Читатель ID: {self.reader_id})>"


# Создание таблиц библиотеки
Base.metadata.create_all(engine)


def test_library_models():
    """Тестирование моделей библиотеки"""
    
    print("\nЗадание 7: Модели библиотеки")
    
    # Создание книг
    books = [
        Book(title='Война и мир', author='Л.Н. Толстой', isbn='978-5-17-089796-3',
             year=2015, genre='Роман', total_copies=5, available_copies=3),
        Book(title='Преступление и наказание', author='Ф.М. Достоевский', 
             isbn='978-5-17-983132-3', year=2014, genre='Роман', total_copies=3, available_copies=1),
        Book(title='Мастер и Маргарита', author='М.А. Булгаков', 
             isbn='978-5-17-108727-3', year=2016, genre='Мистика', total_copies=4, available_copies=4),
    ]
    
    # Создание читателей
    readers = [
        Reader(first_name='Иван', last_name='Петров', email='ivan.petrov@email.ru', 
               phone='+7 999 123-45-67'),
        Reader(first_name='Анна', last_name='Смирнова', email='anna.smirnova@email.ru',
               phone='+7 999 987-65-43'),
    ]
    
    session.add_all(books + readers)
    session.commit()
    
    # Создание выдач
    loan1 = Loan(book_id=books[0].id, reader_id=readers[0].id)
    loan2 = Loan(book_id=books[1].id, reader_id=readers[1].id)
    
    session.add_all([loan1, loan2])
    session.commit()
    
    print("Создано:")
    print(f"  - Книг: {len(books)}")
    print(f"  - Читателей: {len(readers)}")
    print(f"  - Выдач: 2")
    
    # Вывод всех книг
    all_books = session.query(Book).all()
    print("\nСписок книг в библиотеке:")
    for book in all_books:
        print(f"  - {book.title} ({book.author}) - доступно: {book.available_copies}/{book.total_copies}")


test_library_models()


# ============================================================================
# Задание 8: Работа с датами
# ============================================================================

def filter_by_date():
    """Выбор читателей, зарегистрированных в текущем году"""
    
    print("\nЗадание 8: Работа с датами")
    
    # Создадим читателей с разными датами регистрации
    now = datetime.utcnow()
    
    # Читатель в текущем году
    reader_current_year = Reader(
        first_name='Текущий',
        last_name='Год',
        email='current.year@email.ru'
    )
    
    # Читатель в прошлом году
    reader_last_year = Reader(
        first_name='Прошлый',
        last_name='Год',
        email='last.year@email.ru'
    )
    reader_last_year.registration_date = now.replace(year=now.year - 1)
    
    session.add_all([reader_current_year, reader_last_year])
    session.commit()
    
    # Выбор читателей, зарегистрированных в текущем году
    current_year = datetime.utcnow().year
    readers_this_year = session.query(Reader).filter(
        func.strftime('%Y', Reader.registration_date) == str(current_year)
    ).all()
    
    print(f"Читатели, зарегистрированные в {current_year} году:")
    for r in readers_this_year:
        print(f"  - {r.last_name} {r.first_name}, email: {r.email}")
        print(f"    Дата регистрации: {r.registration_date.strftime('%d.%m.%Y')}")


filter_by_date()


# ============================================================================
# Дополнительные примеры для практики
# ============================================================================

print("\n" + "="*70)
print("ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ")
print("="*70)

# Примеры агрегатных функций
def aggregate_examples():
    """Примеры использования агрегатных функций"""
    
    print("\n1. Агрегатные функции:")
    
    # Группировка по категориям
    category_stats = session.query(
        Product.category,
        func.count(Product.id).label('count'),
        func.avg(Product.price).label('avg_price'),
        func.sum(Product.stock).label('total_stock')
    ).group_by(Product.category).all()
    
    print("\nСтатистика по категориям:")
    for cat, count, avg_price, total_stock in category_stats:
        print(f"  {cat}: {count} товаров, средняя цена: {avg_price:.2f} руб., всего на складе: {total_stock}")
    
    # Группировка с условием HAVING
    categories_with_high_avg = session.query(
        Product.category,
        func.avg(Product.price).label('avg_price')
    ).group_by(Product.category).having(
        func.avg(Product.price) > 5000
    ).all()
    
    print("\nКатегории со средней ценой > 5000 руб.:")
    for cat, avg_price in categories_with_high_avg:
        print(f"  - {cat}: {avg_price:.2f} руб.")


aggregate_examples()


def advanced_queries():
    """Продвинутые запросы"""
    
    print("\n2. Продвинутые запросы:")
    
    # Сортировка по убыванию цены
    sorted_by_price = session.query(Product).order_by(Product.price.desc()).all()
    print("\nТовары по убыванию цены:")
    for p in sorted_by_price[:3]:
        print(f"  - {p.name}: {p.price:.2f} руб.")
    
    # Ограничение результатов (TOP 3)
    top_expensive = session.query(Product).order_by(
        Product.price.desc()
    ).limit(3).all()
    print("\nТоп-3 самых дорогих товаров:")
    for p in top_expensive:
        print(f"  - {p.name}: {p.price:.2f} руб.")
    
    # Пагинация
    page_size = 2
    page_number = 1
    page = session.query(Product).order_by(Product.id).offset(
        (page_number - 1) * page_size
    ).limit(page_size).all()
    
    print(f"\nСтраница {page_number} (по {page_size} товаров):")
    for p in page:
        print(f"  - {p.name}")
    
    # Использование LIKE
    products_with_letter = session.query(Product).filter(
        Product.name.like('%о%')
    ).all()
    print(f"\nТовары, содержащие букву 'о': {len(products_with_letter)} шт.")
    
    # Использование IN
    categories = ['Электроника', 'Книги']
    in_category = session.query(Product).filter(
        Product.category.in_(categories)
    ).all()
    print(f"\nТовары категорий {categories}:")
    for p in in_category:
        print(f"  - {p.name} ({p.category})")


advanced_queries()


print("\n" + "="*70)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*70)
