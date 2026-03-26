"""
Практическое занятие 41: Принципы проектирования баз данных
Решение упражнений

Нормализация, ER-диаграммы, лучшие практики
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Table, MetaData, UniqueConstraint, CheckConstraint, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Создание движка для базы данных в памяти
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


print("="*70)
print("Задание 1: Проектирование системы онлайн-обучения")
print("="*70)

# ============================================================================
# Задание 1: Система онлайн-обучения
# ============================================================================

# Анализ требований:
# - Студенты (имя, email, дата регистрации)
# - Курсы (название, описание, автор, цена)
# - Уроки (название, содержание, номер в курсе)
# - Записи на курсы (стudent, курс, дата записи, прогресс)
# - Оценки (student, урок, оценка, дата)

# ER-диаграмма:
# Student 1 --< Enrollment --< Course
# Course 1 --< Lesson
# Student 1 --< Grade --< Lesson

# Нормализация:
# 1НФ: Все атомарные значения
# 2НФ: Course -> Author (отдельная таблица авторов)
# 3НФ: Course -> Category (отдельная таблица категорий, если есть)

# Создание моделей
class Student(Base):
    """Студент"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    
    # Связь с записями на курсы
    enrollments = relationship("Enrollment", back_populates="student")
    # Связь с оценками
    grades = relationship("Grade", back_populates="student")
    
    def __repr__(self):
        return f"<Student({self.name})>"


class Author1(Base):
    """Автор курса"""
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text)
    email = Column(String(100))
    
    # Связь с курсами
    courses = relationship("Course", back_populates="author")
    
    def __repr__(self):
        return f"<Author({self.name})>"


class Course(Base):
    """Курс"""
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey('authors.id'))
    price = Column(Float, nullable=False)
    
    # Связи
    author = relationship("Author1", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    
    def __repr__(self):
        return f"<Course({self.title})>"


class Lesson(Base):
    """Урок"""
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    lesson_number = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    # Связи
    course = relationship("Course", back_populates="lessons")
    grades = relationship("Grade", back_populates="lesson")
    
    def __repr__(self):
        return f"<Lesson({self.title})>"


class Enrollment(Base):
    """Запись на курс"""
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)  # Процент прогресса
    
    # Связи
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment(Студент: {self.student_id}, Курс: {self.course_id})>"


class Grade(Base):
    """Оценка"""
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    grade = Column(Integer)  # Оценка (0-100)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    student = relationship("Student", back_populates="grades")
    lesson = relationship("Lesson", back_populates="grades")
    
    # Ограничения
    __table_args__ = (
        CheckConstraint('grade >= 0 AND grade <= 100', name='check_grade_range'),
    )
    
    def __repr__(self):
        return f"<Grade(Студент: {self.student_id}, Урок: {self.lesson_id}, Оценка: {self.grade})>"


# Создание таблиц
Base.metadata.create_all(engine)


def test_online_learning_system():
    """Тестирование системы онлайн-обучения"""
    
    # Создание авторов
    author1 = Author1(name='Профессор Иванов', bio='Специалист по Python')
    author2 = Author1(name='Доцент Петрова', bio='Эксперт по базам данных')
    
    session.add_all([author1, author2])
    session.commit()
    
    # Создание курсов
    course1 = Course(
        title='Python для начинающих',
        description='Изучите основы программирования на Python',
        author=author1,
        price=4999.00
    )
    
    course2 = Course(
        title='SQL с нуля до профи',
        description='Основы реляционных баз данных и SQL',
        author=author2,
        price=3999.00
    )
    
    session.add_all([course1, course2])
    session.commit()
    
    # Создание уроков
    lessons_course1 = [
        Lesson(title='Введение в Python', content='...', lesson_number=1, course=course1),
        Lesson(title='Переменные и типы данных', content='...', lesson_number=2, course=course1),
        Lesson(title='Условные операторы', content='...', lesson_number=3, course=course1),
    ]
    
    lessons_course2 = [
        Lesson(title='Что такое база данных', content='...', lesson_number=1, course=course2),
        Lesson(title='Основы SQL', content='...', lesson_number=2, course=course2),
    ]
    
    session.add_all(lessons_course1 + lessons_course2)
    session.commit()
    
    # Создание студентов
    students = [
        Student(name='Алексей Смирнов', email='alexey@email.ru'),
        Student(name='Мария Кузнецова', email='maria@email.ru'),
        Student(name='Петр Волков', email='petr@email.ru'),
    ]
    
    session.add_all(students)
    session.commit()
    
    # Запись на курсы
    enrollment1 = Enrollment(student=students[0], course=course1, progress=50)
    enrollment2 = Enrollment(student=students[0], course=course2, progress=100)
    enrollment3 = Enrollment(student=students[1], course=course1, progress=25)
    
    session.add_all([enrollment1, enrollment2, enrollment3])
    session.commit()
    
    # Выставление оценок
    grades = [
        Grade(student=students[0], lesson=lessons_course1[0], grade=85),
        Grade(student=students[0], lesson=lessons_course1[1], grade=90),
        Grade(student=students[1], lesson=lessons_course1[0], grade=75),
    ]
    
    session.add_all(grades)
    session.commit()
    
    print("\nСоздано:")
    print(f"  - Авторов: 2")
    print(f"  - Курсов: 2")
    print(f"  - Уроков: {len(lessons_course1) + len(lessons_course2)}")
    print(f"  - Студентов: {len(students)}")
    print(f"  - Записей на курсы: 3")
    print(f"  - Оценок: {len(grades)}")
    
    # Вывод информации
    print("\nКурсы:")
    for course in [course1, course2]:
        print(f"  - {course.title} ({course.author.name}) - {course.price} руб.")
        print(f"    Уроков: {len(course.lessons)}")
    
    print("\nЗаписи на курсы:")
    for enrollment in [enrollment1, enrollment2, enrollment3]:
        print(f"  - {enrollment.student.name} -> {enrollment.course.title}")
        print(f"    Прогресс: {enrollment.progress}%")


test_online_learning_system()


# ============================================================================
# Задание 2: Приведение к 3НФ (Таблица автобусных рейсов)
# ============================================================================

print("\n" + "="*70)
print("Задание 2: Приведение к 3НФ (Таблица автобусных рейсов)")
print("="*70)

# Анализ исходной таблицы:
# travels (id, route_name, driver_name, driver_phone, bus_number, 
#          bus_model, departure_time, arrival_time, price)

# Проблемы (аномалии):
# 1. Дублирование информации о водителях (имя, телефон)
# 2. Дублирование информации о автобусах (номер, модель)
# 3. При изменении данных водителя нужно обновить все записи
# 4. При удалении рейса удаляется информация о водителе/автобусе

# Нормализация:
# 1НФ: Все значения атомарны (уже выполнено)
# 2НФ: route_name зависит от id, но driver_name зависит от driver_phone
#      bus_model зависит от bus_number
#      -> Выносим водителей и автобусы в отдельные таблицы
# 3НФ: price зависит от route, но не напрямую от id
#      -> Выносим маршруты в отдельную таблицу

# Таблицы после нормализации:
# - routes (id, name, price, departure_time, arrival_time)
# - drivers (id, name, phone)
# - buses (id, number, model)
# - travels (id, route_id, driver_id, bus_id)

class Route(Base):
    """Маршрут"""
    __tablename__ = 'routes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    departure_time = Column(String(10))  # Время в формате HH:MM
    arrival_time = Column(String(10))
    
    def __repr__(self):
        return f"<Route({self.name})>"


class Driver(Base):
    """Водитель"""
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Driver({self.name})>"


class Bus(Base):
    """Автобус"""
    __tablename__ = 'buses'
    
    id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True, nullable=False)
    model = Column(String(100))
    
    def __repr__(self):
        return f"<Bus({self.number} - {self.model})>"


class Travel(Base):
    """Рейс"""
    __tablename__ = 'travels'
    
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    bus_id = Column(Integer, ForeignKey('buses.id'))
    
    route = relationship("Route")
    driver = relationship("Driver")
    bus = relationship("Bus")
    
    def __repr__(self):
        return f"<Travel({self.route.name}, {self.driver.name})>"


# Создание таблиц
Base.metadata.create_all(engine)


def test_normalized_bus_system():
    """Тестирование нормализованной системы рейсов"""
    
    # Создание маршрутов
    routes = [
        Route(name='Москва - Санкт-Петербург', price=1500.00, departure_time='08:00', arrival_time='12:00'),
        Route(name='Москва - Казань', price=2000.00, departure_time='09:00', arrival_time='16:00'),
        Route(name='Санкт-Петербург - Helsinki', price=2500.00, departure_time='10:00', arrival_time='14:00'),
    ]
    
    session.add_all(routes)
    session.commit()
    
    # Создание водителей
    drivers = [
        Driver(name='Иванов Иван Иванович', phone='+7 999 111-11-11'),
        Driver(name='Петров Петр Петрович', phone='+7 999 222-22-22'),
        Driver(name='Сидоров Сидор Сидорович', phone='+7 999 333-33-33'),
    ]
    
    session.add_all(drivers)
    session.commit()
    
    # Создание автобусов
    buses = [
        Bus(number='А123АА', model='Mercedes Sprinter'),
        Bus(number='В456ВВ', model='Volvo 9700'),
        Bus(number='С789СС', model='Neoplan Cityliner'),
    ]
    
    session.add_all(buses)
    session.commit()
    
    # Создание рейсов
    travels = [
        Travel(route=routes[0], driver=drivers[0], bus=buses[0]),
        Travel(route=routes[1], driver=drivers[1], bus=buses[1]),
        Travel(route=routes[0], driver=drivers[2], bus=buses[2]),
    ]
    
    session.add_all(travels)
    session.commit()
    
    print("\nПосле нормализации создано:")
    print(f"  - Маршрутов: {len(routes)}")
    print(f"  - Водителей: {len(drivers)}")
    print(f"  - Автобусов: {len(buses)}")
    print(f"  - Рейсов: {len(travels)}")
    
    # Вывод всех рейсов
    print("\nВсе рейсы:")
    for t in travels:
        print(f"  - {t.route.name}")
        print(f"    Водитель: {t.driver.name} ({t.driver.phone})")
        print(f"    Автобус: {t.bus.number} ({t.bus.model})")
        print(f"    Время: {t.route.departure_time} - {t.route.arrival_time}")
        print(f"    Цена: {t.route.price} руб.")
    
    # Преимущества нормализации:
    print("\nПреимущества нормализации:")
    print("  1. Нет дублирования информации о водителях и автобусах")
    print("  2. Легко обновить данные водителя/автобуса в одном месте")
    print("  3. Можно добавить водителя без привязки к рейсу")
    print("  4. Нет аномалий вставки, обновления, удаления")


test_normalized_bus_system()


# ============================================================================
# Задание 3: ER-диаграмма для CRM
# ============================================================================

print("\n" + "="*70)
print("Задание 3: ER-диаграмма для CRM")
print("="*70)

# ER-диаграмма:
# Company 1 --< Contact
# Company 1 --< Deal
# User 1 --< Deal
# Deal 1 --< Task

class Company(Base):
    """Компания"""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300))
    contact_name = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    
    # Связи
    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")
    
    def __repr__(self):
        return f"<Company({self.name})>"


class Contact(Base):
    """Контакт (человек в компании)"""
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    company_id = Column(Integer, ForeignKey('companies.id'))
    
    # Связь
    company = relationship("Company", back_populates="contacts")
    
    def __repr__(self):
        return f"<Contact({self.name})>"


class User(Base):
    """Пользователь (ответственный за сделку)"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(String(50))
    
    # Связь
    deals = relationship("Deal", back_populates="responsible")
    
    def __repr__(self):
        return f"<User({self.name})>"


class Deal(Base):
    """Сделка"""
    __tablename__ = 'deals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    responsible_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50), default='new')  # new, in_progress, won, lost
    date = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    company = relationship("Company", back_populates="deals")
    responsible = relationship("User", back_populates="deals")
    tasks = relationship("Task", back_populates="deal")
    
    def __repr__(self):
        return f"<Deal({self.name}, {self.amount} руб.)>"


class Task(Base):
    """Задача"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    deal_id = Column(Integer, ForeignKey('deals.id'))
    status = Column(String(50), default='pending')  # pending, in_progress, completed
    executor_id = Column(Integer, ForeignKey('users.id'))
    
    # Связь
    deal = relationship("Deal", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task({self.name})>"


# Создание таблиц
Base.metadata.create_all(engine)


def test_crm_system():
    """Тестирование CRM системы"""
    
    # Создание пользователей
    users = [
        User(name='Алексей Менеджер', email='alexey@crm.ru', role='manager'),
        User(name='Мария Продавец', email='maria@crm.ru', role='sales'),
    ]
    
    session.add_all(users)
    session.commit()
    
    # Создание компаний
    companies = [
        Company(name='ООО ТехноДом', address='Москва, ул. Ленина 1', 
                contact_name='Иван Директор', contact_email='dir@technodom.ru'),
        Company(name='ЗАО Инновации', address='СПб, Невский пр. 10',
                contact_name='Петр CEO', contact_email='ceo@inn.ru'),
    ]
    
    session.add_all(companies)
    session.commit()
    
    # Создание контактов
    contacts = [
        Contact(name='Иван Сергеев', email='ivan@technodom.ru', company=companies[0]),
        Contact(name='Анна Петрова', email='anna@inn.ru', company=companies[1]),
    ]
    
    session.add_all(contacts)
    session.commit()
    
    # Создание сделок
    deals = [
        Deal(name='Поставка оборудования', amount=500000, company=companies[0], 
             responsible=users[0], status='in_progress'),
        Deal(name='IT консалтинг', amount=250000, company=companies[1],
             responsible=users[1], status='new'),
    ]
    
    session.add_all(deals)
    session.commit()
    
    # Создание задач
    tasks = [
        Task(name='Подготовить коммерческое предложение', description='...',
             deal=deals[0], status='in_progress'),
        Task(name='Согласовать договор', description='...',
             deal=deals[0], status='pending'),
        Task(name='Провести презентацию', description='...',
             deal=deals[1], status='pending'),
    ]
    
    session.add_all(tasks)
    session.commit()
    
    print("\nCRM система создана:")
    print(f"  - Компаний: {len(companies)}")
    print(f"  - Контактов: {len(contacts)}")
    print(f"  - Сделок: {len(deals)}")
    print(f"  - Задач: {len(tasks)}")
    
    # Вывод сделок
    print("\nСделки:")
    for deal in deals:
        print(f"  - {deal.name}")
        print(f"    Компания: {deal.company.name}")
        print(f"    Ответственный: {deal.responsible.name}")
        print(f"    Сумма: {deal.amount} руб.")
        print(f"    Статус: {deal.status}")
        print(f"    Задач: {len(deal.tasks)}")


test_crm_system()


# ============================================================================
# Задание 4: Добавление ограничений
# ============================================================================

print("\n" + "="*70)
print("Задание 4: Ограничения для справочной системы")
print("="*70)

# Ограничения:
# - Код страны ровно 2-3 символа
# - Население > 0
# - Название страны уникально

class Country(Base):
    """Страна"""
    __tablename__ = 'countries'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    iso_code = Column(String(3), nullable=False)  # 2-3 символа
    population = Column(Integer)
    
    # Ограничения на уровне таблицы
    __table_args__ = (
        CheckConstraint('LENGTH(iso_code) >= 2 AND LENGTH(iso_code) <= 3', 
                        name='check_iso_code_length'),
        CheckConstraint('population > 0', name='check_population_positive'),
    )
    
    def __repr__(self):
        return f"<Country({self.name}, {self.iso_code})>"


class City(Base):
    """Город"""
    __tablename__ = 'cities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    population = Column(Integer)
    
    # Ограничения
    __table_args__ = (
        CheckConstraint('population > 0', name='check_city_population_positive'),
    )
    
    def __repr__(self):
        return f"<City({self.name})>"


# Создание таблиц
Base.metadata.create_all(engine)


def test_constraints():
    """Тестирование ограничений"""
    
    from sqlalchemy.exc import IntegrityError
    
    # Добавление стран
    countries = [
        Country(name='Россия', iso_code='RU', population=144000000),
        Country(name='Германия', iso_code='DE', population=83000000),
        Country(name='США', iso_code='US', population=331000000),
    ]
    
    session.add_all(countries)
    session.commit()
    
    print("\nСозданы страны:")
    for c in countries:
        print(f"  - {c.name} ({c.iso_code}), население: {c.population:,}")
    
    # Добавление городов
    cities = [
        City(name='Москва', country_id=countries[0].id, population=12500000),
        City(name='Санкт-Петербург', country_id=countries[0].id, population=5400000),
        City(name='Берлин', country_id=countries[1].id, population=3700000),
    ]
    
    session.add_all(cities)
    session.commit()
    
    print("\nСозданы города:")
    for city in cities:
        print(f"  - {city.name}, население: {city.population:,}")
    
    # Тестирование ограничений
    print("\nТестирование ограничений:")
    
    # Попытка добавить страну с неправильным кодом
    try:
        bad_country = Country(name='Тест', iso_code='RUSSIA', population=1000)
        session.add(bad_country)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print("  - Ошибка: код страны должен быть 2-3 символа")
    
    # Попытка добавить страну с отрицательным населением
    try:
        bad_country = Country(name='Тест2', iso_code='TS', population=-100)
        session.add(bad_country)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print("  - Ошибка: население должно быть > 0")
    
    # Попытка добавить дубликат названия
    try:
        dup_country = Country(name='Россия', iso_code='RS', population=1000)
        session.add(dup_country)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print("  - Ошибка: название страны должно быть уникальным")


test_constraints()


# ============================================================================
# Задание 5: Анализ нормализации
# ============================================================================

print("\n" + "="*70)
print("Задание 5: Анализ нормализации")
print("="*70)

# Исходная таблица:
# employees (
#     id,
#     name,
#     department_name,
#     department_location,
#     project_names,  -- через запятую!
#     project_start_dates,  -- через запятую!
#     skill_names  -- через запятую!
# )

# Проблемы:
# 1. Не 1НФ: project_names, project_start_dates, skill_names - неатомарные
# 2. Зависимости: department_name, department_location зависят от department_id
# 3. Избыточность: дублирование информации об отделах и проектах

# Нормализованная схема:
# - employees (id, name, department_id)
# - departments (id, name, location)
# - projects (id, name, start_date)
# - employee_projects (employee_id, project_id)
# - skills (id, name)
# - employee_skills (employee_id, skill_id)

class Employee(Base):
    """Сотрудник"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    def __repr__(self):
        return f"<Employee({self.name})>"


class Department(Base):
    """Отдел"""
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    
    def __repr__(self):
        return f"<Department({self.name})>"


class Project(Base):
    """Проект"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(String(10))  # YYYY-MM-DD
    
    def __repr__(self):
        return f"<Project({self.name})>"


class Skill(Base):
    """Навык"""
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Skill({self.name})>"


# Ассоциативные таблицы
employee_projects = Table(
    'employee_projects',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)

employee_skills = Table(
    'employee_skills',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)


# Создание таблиц
Base.metadata.create_all(engine)


def test_employee_normalization():
    """Тестирование нормализации таблицы сотрудников"""
    
    # Создание отделов
    depts = [
        Department(name='IT', location='Корпус А'),
        Department(name='HR', location='Корпус Б'),
        Department(name='Sales', location='Корпус В'),
    ]
    
    session.add_all(depts)
    session.commit()
    
    # Создание проектов
    projects = [
        Project(name='Разработка сайта', start_date='2024-01-15'),
        Project(name='Внедрение CRM', start_date='2024-03-01'),
        Project(name='Обучение персонала', start_date='2024-02-01'),
    ]
    
    session.add_all(projects)
    session.commit()
    
    # Создание навыков
    skills = [
        Skill(name='Python'),
        Skill(name='SQL'),
        Skill(name='JavaScript'),
        Skill(name='Коммуникации'),
    ]
    
    session.add_all(skills)
    session.commit()
    
    # Создание сотрудников
    emps = [
        Employee(name='Иванов И.И.', department_id=depts[0].id),
        Employee(name='Петрова А.С.', department_id=depts[0].id),
        Employee(name='Сидоров В.К.', department_id=depts[1].id),
    ]
    
    session.add_all(emps)
    session.commit()
    
    # Связывание сотрудников с проектами
    session.execute(employee_projects.insert().values([
        {'employee_id': emps[0].id, 'project_id': projects[0].id},
        {'employee_id': emps[0].id, 'project_id': projects[1].id},
        {'employee_id': emps[1].id, 'project_id': projects[0].id},
        {'employee_id': emps[2].id, 'project_id': projects[2].id},
    ]))
    
    # Связывание сотрудников с навыками
    session.execute(employee_skills.insert().values([
        {'employee_id': emps[0].id, 'skill_id': skills[0].id},
        {'employee_id': emps[0].id, 'skill_id': skills[1].id},
        {'employee_id': emps[1].id, 'skill_id': skills[0].id},
        {'employee_id': emps[1].id, 'skill_id': skills[2].id},
        {'employee_id': emps[2].id, 'skill_id': skills[3].id},
    ]))
    
    session.commit()
    
    print("\nНормализованная схема создана:")
    print(f"  - Отделов: {len(depts)}")
    print(f"  - Проектов: {len(projects)}")
    print(f"  - Навыков: {len(skills)}")
    print(f"  - Сотрудников: {len(emps)}")
    
    # Вывод информации о сотруднике
    print("\nИнформация о сотрудниках:")
    for emp in emps:
        print(f"\n  {emp.name}")
        
        # Отдел
        dept = session.query(Department).get(emp.department_id)
        print(f"    Отдел: {dept.name} ({dept.location})")
        
        # Проекты
        proj_ids = [r.project_id for r in session.execute(
            employee_projects.select().where(employee_projects.c.employee_id == emp.id)
        ).fetchall()]
        proj_names = [session.query(Project).get(p).name for p in proj_ids]
        print(f"    Проекты: {', '.join(proj_names)}")
        
        # Навыки
        skill_ids = [r.skill_id for r in session.execute(
            employee_skills.select().where(employee_skills.c.employee_id == emp.id)
        ).fetchall()]
        skill_names = [session.query(Skill).get(s).name for s in skill_ids]
        print(f"    Навыки: {', '.join(skill_names)}")


test_employee_normalization()


# ============================================================================
# Задание 6: Денормализация для отчетности
# ============================================================================

print("\n" + "="*70)
print("Задание 6: Денормализация для аналитики")
print("="*70)

# Денормализация - намеренное добавление избыточности для ускорения чтения

class SalesReport(Base):
    """Отчет о продажах по дням (денормализованная таблица)"""
    __tablename__ = 'sales_reports'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(10))  # YYYY-MM-DD
    product_name = Column(String(200))
    product_category = Column(String(100))  # Денормализовано
    quantity = Column(Integer)
    price = Column(Float)
    total = Column(Float)  # quantity * price (денормализовано)
    manager_name = Column(String(100))  # Денормализовано
    manager_region = Column(String(100))  # Денормализовано
    
    def __repr__(self):
        return f"<SalesReport({self.date}, {self.product_name})>"


class ManagerStats(Base):
    """Суммарные показатели по менеджерам (денормализованная таблица)"""
    __tablename__ = 'manager_stats'
    
    id = Column(Integer, primary_key=True)
    manager_name = Column(String(100))
    region = Column(String(100))
    total_sales = Column(Float)  # Сумма всех продаж
    transaction_count = Column(Integer)  # Количество транзакций
    avg_check = Column(Float)  # Средний чек
    period_start = Column(String(10))
    period_end = Column(String(10))
    
    def __repr__(self):
        return f"<ManagerStats({self.manager_name})>"


class ProductRating(Base):
    """Рейтинг товаров по продажам (денормализованная таблица)"""
    __tablename__ = 'product_ratings'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String(200))
    category = Column(String(100))
    total_quantity = Column(Integer)
    total_revenue = Column(Float)
    avg_price = Column(Float)
    rank = Column(Integer)  # Рейтинг
    
    def __repr__(self):
        return f"<ProductRating({self.product_name}, ранг: {self.rank})>"


# Создание таблиц
Base.metadata.create_all(engine)


def test_denormalization():
    """Тестирование денормализации"""
    
    # Заполнение отчета о продажах
    sales_data = [
        SalesReport(date='2024-01-15', product_name='Ноутбук', product_category='Электроника',
                   quantity=2, price=50000, total=100000, manager_name='Иванов', manager_region='Центр'),
        SalesReport(date='2024-01-15', product_name='Книга', product_category='Книги',
                   quantity=10, price=500, total=5000, manager_name='Петрова', manager_region='Север'),
        SalesReport(date='2024-01-16', product_name='Смартфон', product_category='Электроника',
                   quantity=5, price=30000, total=150000, manager_name='Иванов', manager_region='Центр'),
        SalesReport(date='2024-01-16', product_name='Наушники', product_category='Электроника',
                   quantity=8, price=5000, total=40000, manager_name='Сидоров', manager_region='Юг'),
    ]
    
    session.add_all(sales_data)
    session.commit()
    
    # Заполнение статистики по менеджерам
    manager_data = [
        ManagerStats(manager_name='Иванов', region='Центр', total_sales=250000, 
                    transaction_count=2, avg_check=125000, period_start='2024-01-01', period_end='2024-01-31'),
        ManagerStats(manager_name='Петрова', region='Север', total_sales=5000,
                    transaction_count=1, avg_check=5000, period_start='2024-01-01', period_end='2024-01-31'),
        ManagerStats(manager_name='Сидоров', region='Юг', total_sales=40000,
                    transaction_count=1, avg_check=40000, period_start='2024-01-01', period_end='2024-01-31'),
    ]
    
    session.add_all(manager_data)
    session.commit()
    
    # Заполнение рейтинга товаров
    product_ratings = [
        ProductRating(product_name='Смартфон', category='Электроника', total_quantity=5,
                    total_revenue=150000, avg_price=30000, rank=1),
        ProductRating(product_name='Ноутбук', category='Электроника', total_quantity=2,
                    total_revenue=100000, avg_price=50000, rank=2),
        ProductRating(product_name='Наушники', category='Электроника', total_quantity=8,
                    total_revenue=40000, avg_price=5000, rank=3),
        ProductRating(product_name='Книга', category='Книги', total_quantity=10,
                    total_revenue=5000, avg_price=500, rank=4),
    ]
    
    session.add_all(product_ratings)
    session.commit()
    
    print("\nДенормализованные таблицы созданы:")
    print(f"  - Продажи: {len(sales_data)} записей")
    print(f"  - Статистика менеджеров: {len(manager_data)} записей")
    print(f"  - Рейтинг товаров: {len(product_ratings)} записей")
    
    # Вывод рейтинга товаров
    print("\nРейтинг товаров по продажам:")
    for rating in product_ratings:
        print(f"  {rating.rank}. {rating.product_name} ({rating.category})")
        print(f"     Продано: {rating.total_quantity}, Выручка: {rating.total_revenue} руб.")
    
    print("\nКогда использовать денормализацию:")
    print("  1. Частые аналитические запросы (отчеты, дашборды)")
    print("  2. Сложные агрегации, требующие JOIN многих таблиц")
    print("  3. Нужно снизить нагрузку на основные таблицы")
    print("  4. Данные редко изменяются, но часто читаются")


test_denormalization()


print("\n" + "="*70)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*70)
