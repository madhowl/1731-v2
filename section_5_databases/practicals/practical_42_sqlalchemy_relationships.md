# Практическое занятие 40: Связи в SQLAlchemy

## Отношения между таблицами: один-ко-многим, один-к-одному, многие-ко-многим

### Цель занятия:
Освоить создание и использование различных типов связей между моделями в SQLAlchemy ORM.

### Задачи:
1. Научиться создавать отношение "один-ко-многим" (One-to-Many)
2. Освоить отношение "один-к-одному" (One-to-One)
3. Изучить отношение "многие-ко-многим" (Many-to-Many)
4. Научиться работать со связанными объектами
5. Выполнять запросы с JOIN через отношения

### План работы:
1. Настройка окружения и импорты
2. Отношение один-ко-многим
3. Отношение один-к-одному
4. Отношение многие-ко-многим
5. Работа со связанными объектами
6. Практические задания

---

## 1. Настройка окружения и импорты

### Пример 1: Базовая настройка

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Создание движка и сессии
engine = create_engine('sqlite:///company.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
```

---

## 2. Отношение один-ко-многим (One-to-Many)

Отношение "один-ко-многим" означает, что одна запись в одной таблице может быть связана с несколькими записями в другой таблице.

### Пример 2: Определение отношения один-ко-многим

```python
class Department(Base):
    """Отдел - одна сторона"""
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    
    # Связь с Employee (один отдел - много сотрудников)
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self):
        return f"<Department({self.name})>"


class Employee(Base):
    """Сотрудник - много сторона"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    position = Column(String(100))
    salary = Column(Integer)
    
    # Внешний ключ на Department
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    # Обратная связь
    department = relationship("Department", back_populates="employees")
    
    def __repr__(self):
        return f"<Employee({self.first_name} {self.last_name}, {self.position})>"
```

### Пример 3: Создание таблиц и добавление данных

```python
# Создание таблиц
Base.metadata.create_all(engine)

# Создание отделов
it_dept = Department(name="IT", location="Корпус А")
hr_dept = Department(name="HR", location="Корпус Б")
sales_dept = Department(name="Продажи", location="Корпус В")

session.add_all([it_dept, hr_dept, sales_dept])
session.commit()

# Создание сотрудников
emp1 = Employee(
    first_name='Иван',
    last_name='Петров',
    email='ivan.petrov@company.ru',
    position='Разработчик',
    salary=120000,
    department=it_dept  # Связь через объект
)

emp2 = Employee(
    first_name='Анна',
    last_name='Смирнова',
    email='anna.smirnova@company.ru',
    position='Тестировщик',
    salary=100000,
    department=it_dept
)

emp3 = Employee(
    first_name='Алексей',
    last_name='Кузнецов',
    email='alexey.kuznetsov@company.ru',
    position='HR менеджер',
    salary=80000,
    department=hr_dept
)

emp4 = Employee(
    first_name='Елена',
    last_name='Волкова',
    email='elena.volkova@company.ru',
    position='Менеджер по продажам',
    salary=90000,
    department=sales_dept
)

session.add_all([emp1, emp2, emp3, emp4])
session.commit()

print("Данные успешно добавлены")
```

### Пример 4: Доступ к связанным объектам

```python
# Получение всех сотрудников отдела
it_dept = session.query(Department).filter(
    Department.name == 'IT'
).first()

print(f"Отдел: {it_dept.name}")
print("Сотрудники отдела:")
for employee in it_dept.employees:
    print(f"  - {employee.first_name} {employee.last_name}, {employee.position}")

# Получение отдела сотрудника
employee = session.query(Employee).filter(
    Employee.last_name == 'Петров'
).first()

print(f"\nСотрудник: {employee.first_name} {employee.last_name}")
print(f"Отдел: {employee.department.name}")
print(f"Расположение: {employee.department.location}")
```

### Пример 5: Фильтрация через связанные объекты

```python
# Найти всех сотрудников IT отдела
it_employees = session.query(Employee).join(Employee.department).filter(
    Department.name == 'IT'
).all()

print("Сотрудники IT отдела (через JOIN):")
for emp in it_employees:
    print(f"  - {emp.first_name} {emp.last_name}")

# Найти отделы с сотрудниками с зарплатой > 100000
high_salary_depts = session.query(Department).join(Department.employees).filter(
    Employee.salary > 100000
).distinct().all()

print("\nОтделы с высокооплачиваемыми сотрудниками:")
for dept in high_salary_depts:
    print(f"  - {dept.name}")
```

---

## 3. Отношение один-к-одному (One-to-One)

Отношение "один-к-одному" означает, что каждая запись в одной таблице связана ровно с одной записью в другой таблице.

### Пример 6: Определение отношения один-к-одному

```python
class User(Base):
    """Пользователь"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    
    # Связь один-к-одному с UserProfile (один пользователь - один профиль)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User({self.username})>"


class UserProfile(Base):
    """Профиль пользователя"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(Text)  # О себе
    avatar_url = Column(String(255))
    phone = Column(String(20))
    address = Column(String(255))
    
    # Внешний ключ на User (уникальный для обеспечения 1:1)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    
    # Обратная связь
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile({self.user.username})>"
```

### Пример 7: Создание и работа с данными

```python
# Создание таблиц
Base.metadata.create_all(engine)

# Создание пользователя с профилем
user1 = User(username='ivan_ivanov', email='ivan@email.ru')
user1.profile = UserProfile(
    bio='Разработчик Python',
    phone='+7 999 123-45-67',
    address='Москва, ул. Ленина 1'
)

user2 = User(username='anna_petrova', email='anna@email.ru')
user2.profile = UserProfile(
    bio='Дизайнер',
    phone='+7 999 987-65-43',
    address='СПб, Невский пр. 10'
)

session.add_all([user1, user2])
session.commit()

# Доступ к профилю пользователя
user = session.query(User).filter(User.username == 'ivan_ivanov').first()
print(f"Пользователь: {user.username}")
print(f"Email: {user.email}")
print(f"Профиль: {user.profile.bio}")
print(f"Телефон: {user.profile.phone}")

# Доступ к пользователю через профиль
profile = session.query(UserProfile).filter(UserProfile.phone.like('%123%')).first()
print(f"\nПрофиль принадлежит пользователю: {profile.user.username}")
```

---

## 4. Отношение многие-ко-многим (Many-to-Many)

Отношение "многие-ко-многим" означает, что несколько записей в одной таблице могут быть связаны с несколькими записями в другой таблице.

### Пример 8: Определение отношения многие-ко-многим

```python
# Ассоциативная таблица (таблица связи)
student_courses = Table(
    'student_courses',  # Название таблицы связи
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('enrollment(20), default=datetime.utcnow_date', String().strftime('%Y-%m-%d')),
    Column('grade', Integer)  # Оценка
)


class Student(Base):
    """Студент"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    group_number = Column(String(20))
    
    # Связь многие-ко-многим через ассоциативную таблицу
    courses = relationship("Course", secondary=student_courses, back_populates="students")
    
    def __repr__(self):
        return f"<Student({self.first_name} {self.last_name})>"


class Course(Base):
    """Курс"""
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    credits = Column(Integer, default=3)
    
    # Обратная связь
    students = relationship("Student", secondary=student_courses, back_populates="courses")
    
    def __repr__(self):
        return f"<Course({self.title})>"
```

### Пример 9: Работа с данными many-to-many

```python
# Создание таблиц
Base.metadata.create_all(engine)

# Создание курсов
python_course = Course(title="Python Basics", description="Основы Python", credits=5)
sql_course = Course(title="SQL Fundamentals", description="Основы SQL", credits=4)
web_course = Course(title="Web Development", description="Веб-разработка", credits=6)

session.add_all([python_course, sql_course, web_course])
session.commit()

# Создание студентов
student1 = Student(
    first_name='Мария',
    last_name='Сидорова',
    email='maria.sidorova@uni.ru',
    group_number='CS-101'
)

student2 = Student(
    first_name='Петр',
    last_name='Смирнов',
    email='petr.smirnov@uni.ru',
    group_number='CS-101'
)

student3 = Student(
    first_name='Анна',
    last_name='Кузнецова',
    email='anna.kuznetsova@uni.ru',
    group_number='CS-102'
)

session.add_all([student1, student2, student3])
session.commit()

# Запись студентов на курсы
student1.courses.append(python_course)
student1.courses.append(sql_course)

student2.courses.append(python_course)
student2.courses.append(web_course)

student3.courses.append(python_course)
student3.courses.append(sql_course)
student3.courses.append(web_course)

session.commit()

print("Студенты записаны на курсы")
```

### Пример 10: Доступ к связанным данным many-to-many

```python
# Получить все курсы студента
student = session.query(Student).filter(
    Student.first_name == 'Мария'
).first()

print(f"Студент: {student.first_name} {student.last_name}")
print("Записанные курсы:")
for course in student.courses:
    print(f"  - {course.title} ({course.credits} кредитов)")

# Получить всех студентов курса
course = session.query(Course).filter(
    Course.title == 'Python Basics'
).first()

print(f"\nКурс: {course.title}")
print("Записавшиеся студенты:")
for student in course.students:
    print(f"  - {student.first_name} {student.last_name}")
```

### Пример 11: Работа с ассоциативной таблицей

```python
# Добавление оценок через ассоциативную таблицу
from sqlalchemy.orm import Mapper

# Прямая работа с таблицей связи
session.execute(
    student_courses.insert().values(
        student_id=student1.id,
        course_id=python_course.id,
        enrollment_date='2024-09-01',
        grade=5
    )
)
session.commit()

# Запрос к ассоциативной таблице
result = session.query(student_courses).filter(
    student_courses.c.student_id == student1.id
).all()

print("Записи в таблице связи:")
for row in result:
    print(f"  Студент ID: {row.student_id}, Курс ID: {row.course_id}, Оценка: {row.grade}")
```

---

## 5. Каскадные операции

### Пример 12: Настройка каскадного удаления

```python
class Parent(Base):
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    # cascade='all, delete-orphan' - удаление детей при удалении родителя
    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")


class Child(Base):
    __tablename__ = 'children'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey('parents.id'))
    
    parent = relationship("Parent", back_populates="children")

# Создание родителя с детьми
parent1 = Parent(name="Иван Иванович")
parent1.children = [
    Child(name="Алексей"),
    Child(name="Мария")
]

session.add(parent1)
session.commit()

# При удалении родителя автоматически удалятся и дети
session.delete(parent1)
session.commit()
print("Родитель и его дети удалены")
```

---

## 6. Практические задания

### Задание 1: Система блога
Создайте модели для блоговой системы:
- Author (id, name, email, bio)
- Post (id, title, content, published_date, author_id)
- Tag (id, name)
- PostTag (post_id, tag_id) - связь many-to-many

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 2: Добавление данных
Добавьте 2 авторов, 4 поста и 5 тегов. Свяжите посты с тегами.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 3: Запросы к связанным данным
Напишите запросы для:
1. Получения всех постов автора
2. Получения всех тегов поста
3. Поиска постов по тегу

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 4: Интернет-магазин
Создайте модели:
- Category (id, name, parent_id) - категория с родительской категорией
- Product (id, name, price, category_id)
- Order (id, order_date, status)
- OrderItem (order_id, product_id, quantity, price)

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 5: Заказы и товары
Добавьте категорию "Электроника" с подкатегорией "Смартфоны", несколько товаров и создайте заказ.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 6: Подсчет статистики
Напишите запрос для подсчета общего количества товаров в каждой категории.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## 7. Дополнительные задания

### Задание 7: Социальная сеть
Создайте систему друзей:
- User (id, name, email)
- Friendship (user_id, friend_id, created_at) - связь many-to-many

Найдите всех друзей пользователя.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 8: Иерархия категорий
Создайте дерево категорий с помощью self-referential отношения и найдите все подкатегории.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## Контрольные вопросы:
1. Какие типы отношений поддерживаются в SQLAlchemy?
2. Что такое ассоциативная таблица и для чего она используется?
3. Чем отличается `uselist=False` в отношении one-to-one?
4. Как работает параметр `back_populates`?
5. Что такое каскадные операции и как их настроить?
6. Как выполнить JOIN через отношение между моделями?
7. В чем преимущество использования отношений перед прямым написанием JOIN-запросов?
