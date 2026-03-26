# Практическое занятие 39: Основы SQLAlchemy ORM

## Создание моделей, базовые операции CRUD, запросы

### Цель занятия:
Научиться использовать SQLAlchemy ORM для работы с базами данных, создавать модели данных и выполнять базовые операции CRUD.

### Задачи:
1. Настроить подключение к базе данных SQLite с помощью SQLAlchemy
2. Создать модели данных с использованием декларативного стиля
3. Выполнить операции создания, чтения, обновления и удаления данных
4. Научиться фильтровать и сортировать данные с помощью ORM
5. Освоить базовые агрегатные функции

### План работы:
1. Установка и настройка SQLAlchemy
2. Создание моделей данных
3. Операции CRUD
4. Фильтрация и сортировка
5. Агрегатные функции
6. Практические задания

---

## 1. Установка и настройка SQLAlchemy

### Пример 1: Установка SQLAlchemy

```bash
pip install sqlalchemy
```

### Пример 2: Базовая настройка движка и сессии

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание движка (подключение к базе данных)
engine = create_engine('sqlite:///university.db', echo=True)

# Создание базового класса для моделей
Base = declarative_base()

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

# Создание сессии для работы с данными
session = Session()

print("Подключение к базе данных успешно установлено")
print(f"URL подключения: {engine.url}")
```

### Пример 3: Использование SQLite в памяти (для тестирования)

```python
# База данных в памяти - удобно для тестов
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
```

---

## 2. Создание моделей данных

### Пример 4: Определение простой модели

```python
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from datetime import datetime

class Student(Base):
    """Модель студента"""
    __tablename__ = 'students'
    
    # Определение колонок
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    gpa = Column(Float, default=0.0)  # Средний балл
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Student({self.first_name} {self.last_name}, {self.email})>"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}, {self.email}"
```

### Пример 5: Создание нескольких связанных моделей

```python
class Teacher(Base):
    """Модель преподавателя"""
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    department = Column(String(100))
    hire_date = Column(DateTime, default=datetime.utcnow)
    salary = Column(Float)
    
    def __repr__(self):
        return f"<Teacher({self.first_name} {self.last_name}, {self.department})>"


class Course(Base):
    """Модель курса"""
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    credits = Column(Integer, default=3)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    
    def __repr__(self):
        return f"<Course({self.title}, {self.credits} кредитов)>"
```

### Пример 6: Создание всех таблиц в базе данных

```python
# Создание всех таблиц, определенных в Base
Base.metadata.create_all(engine)

print("Все таблицы успешно созданы")

# Проверка списка таблиц
print(f"Таблицы в базе: {Base.metadata.tables.keys()}")
```

---

## 3. Операции CRUD

### Создание данных (Create)

### Пример 7: Создание одной записи

```python
# Создание нового студента
new_student = Student(
    first_name='Иван',
    last_name='Петров',
    email='ivan.petrov@university.ru',
    age=20,
    gpa=4.5,
    is_active=True
)

# Добавление в сессию
session.add(new_student)

# Сохранение в базе данных
session.commit()

print(f"Студент добавлен с ID: {new_student.id}")
```

### Пример 8: Создание нескольких записей

```python
# Создание списка студентов
students_data = [
    Student(
        first_name='Анна',
        last_name='Смирнова',
        email='anna.smirnova@university.ru',
        age=19,
        gpa=4.8,
        is_active=True
    ),
    Student(
        first_name='Алексей',
        last_name='Кузнецов',
        email='alexey.kuznetsov@university.ru',
        age=21,
        gpa=3.9,
        is_active=True
    ),
    Student(
        first_name='Елена',
        last_name='Волкова',
        email='elena.volkova@university.ru',
        age=20,
        gpa=4.2,
        is_active=True
    )
]

# Добавление всех студентов
session.add_all(students_data)
session.commit()

print(f"Добавлено {len(students_data)} студентов")
```

### Чтение данных (Read)

### Пример 9: Получение всех записей

```python
# Получение всех студентов
all_students = session.query(Student).all()

print(f"Всего студентов: {len(all_students)}")
for student in all_students:
    print(f"  {student.id}: {student.first_name} {student.last_name}")
```

### Пример 10: Получение одной записи

```python
# Получение первого студента
first_student = session.query(Student).first()
print(f"Первый студент: {first_student}")

# Получение студента по ID
student_by_id = session.query(Student).get(2)
print(f"Студент с ID 2: {student_by_id}")

# Получение одной записи с фильтром
student_filter = session.query(Student).filter(
    Student.email == 'ivan.petrov@university.ru'
).first()
print(f"Найденный студент: {student_filter}")
```

### Пример 11: Фильтрация данных

```python
# Фильтр по условию равенства
active_students = session.query(Student).filter(
    Student.is_active == True
).all()

# Фильтр по условию больше/меньше
high_gpa_students = session.query(Student).filter(
    Student.gpa >= 4.0
).all()

# Фильтр по диапазону
students_age_range = session.query(Student).filter(
    Student.age.between(19, 21)
).all()

# Фильтр с использованием IN
specific_students = session.query(Student).filter(
    Student.last_name.in_(['Петров', 'Смирнова', 'Кузнецов'])
).all()

# Комбинирование условий (AND)
from sqlalchemy import and_
filtered_students = session.query(Student).filter(
    and_(
        Student.gpa >= 4.0,
        Student.is_active == True
    )
).all()

# Использование OR
from sqlalchemy import or_
any_condition = session.query(Student).filter(
    or_(
        Student.age < 19,
        Student.gpa < 3.5
    )
).all()

# Фильтр с LIKE
name_search = session.query(Student).filter(
    Student.first_name.like('%а%')  # Все имена, содержащие 'а'
).all()

print(f"Найдено студентов: {len(filtered_students)}")
```

### Пример 12: Сортировка результатов

```python
# Сортировка по возрастанию
students_asc = session.query(Student).order_by(Student.last_name).all()

# Сортировка по убыванию
students_desc = session.query(Student).order_by(Student.gpa.desc()).all()

# Сортировка по нескольким полям
students_multi = session.query(Student).order_by(
    Student.is_active.desc(),
    Student.gpa.desc()
).all()

# Ограничение количества результатов
top_students = session.query(Student).order_by(
    Student.gpa.desc()
).limit(3).all()

# Пропуск и ограничение (пагинация)
page_students = session.query(Student).order_by(
    Student.id
).offset(5).limit(5).all()
```

### Обновление данных (Update)

### Пример 13: Обновление одной записи

```python
# Получение студента для обновления
student = session.query(Student).filter(
    Student.email == 'ivan.petrov@university.ru'
).first()

# Изменение полей
if student:
    student.gpa = 4.7
    student.age = 21
    session.commit()
    print(f"Обновлен студент: {student}")
```

### Пример 14: Обновление нескольких записей

```python
# Обновление всех записей, удовлетворяющих условию
updated_count = session.query(Student).filter(
    Student.gpa < 3.5
).update({Student.is_active: False})

session.commit()
print(f"Обновлено {updated_count} записей")

# Массовое обновление с выражением
session.query(Student).filter(
    Student.is_active == True
).update({
    Student.gpa: Student.gpa * 1.1  # Увеличение на 10%
})
session.commit()
```

### Удаление данных (Delete)

### Пример 15: Удаление одной записи

```python
# Получение студента для удаления
student = session.query(Student).filter(
    Student.email == 'elena.volkova@university.ru'
).first()

if student:
    session.delete(student)
    session.commit()
    print(f"Удален студент: {student}")
```

### Пример 16: Удаление нескольких записей

```python
# Удаление всех неактивных студентов
deleted_count = session.query(Student).filter(
    Student.is_active == False
).delete()

session.commit()
print(f"Удалено {deleted_count} записей")
```

---

## 4. Агрегатные функции

### Пример 17: Использование агрегатных функций

```python
from sqlalchemy import func, count, avg, max, min, sum

# Подсчет количества записей
total_students = session.query(func.count(Student.id)).scalar()
print(f"Всего студентов: {total_students}")

# Среднее значение
average_gpa = session.query(func.avg(Student.gpa)).scalar()
print(f"Средний балл: {average_gpa:.2f}")

# Максимальное и минимальное значение
max_gpa = session.query(func.max(Student.gpa)).scalar()
min_gpa = session.query(func.min(Student.gpa)).scalar()
print(f"Диапазон GPA: {min_gpa} - {max_gpa}")

# Сумма
total_ages = session.query(func.sum(Student.age)).scalar()
print(f"Сумма возрастов: {total_ages}")
```

### Пример 18: Группировка данных

```python
# Группировка по полю
from sqlalchemy import case

# Количество студентов по возрасту
age_distribution = session.query(
    Student.age,
    func.count(Student.id).label('count')
).group_by(Student.age).all()

print("Распределение по возрасту:")
for age, count in age_distribution:
    print(f"  {age} лет: {count} студентов")

# Группировка с ус_count
active_stats = session.query(
    Student.is_active,
    func.count(Student.id).label('count'),
    func.avg(Student.gpa).label('avg_gpa')
).group_by(Student.is_active).all()

print("\nСтатистика по активности:")
for is_active, count, avg_gpa in active_stats:
    status = "Активные" if is_active else "Неактивные"
    print(f"  {status}: {count} студентов, средний балл {avg_gpa:.2f}")
```

---

## 5. Практические задания

### Задание 1: Создание модели товара
Создайте модель Product для интернет-магазина с полями:
- id (Integer, первичный ключ)
- name (String 100, обязательное)
- description (Text)
- price (Float, обязательное)
- stock (Integer, по умолчанию 0)
- category (String 50)
- created_at (DateTime)
- is_available (Boolean, по умолчанию True)

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 2: Заполнение базы данных
Добавьте 5 товаров в таблицу с различными значениями.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 3: Поиск товаров
Напишите запросы для:
1. Нахождения всех доступных товаров
2. Нахождения товаров с ценой в диапазоне 1000-5000
3. Нахождения товаров определенной категории

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 4: Обновление данных
Обновите цену всех товаров категории "Электроника", увеличив её на 15%.

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 5: Статистика товаров
Напишите запросы для получения:
1. Общего количества товаров
2. Средней цены товара
3. Общей стоимости всех товаров на складе

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 6: Удаление данных
Удалите все товары с нулевым количеством на складе.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## 6. Дополнительные задания

### Задание 7: Создание полной модели библиотеки
Создайте модель для библиотечной системы:
- Book (id, title, author, isbn, year, genre, total_copies, available_copies)
- Reader (id, first_name, last_name, email, phone, registration_date)
- Loan (id, book_id, reader_id, loan_date, return_date, is_returned)

```python
# ВАШ КОД ЗДЕСЬ
```

### Задание 8: Работа с датами
Выберите всех читателей, зарегистрированных в текущем году.

```python
# ВАШ КОД ЗДЕСЬ
```

---

## Контрольные вопросы:
1. Какие преимущества предоставляет ORM перед прямым использованием SQL?
2. В чем разница между методами `filter()` и `filter_by()`?
3. Как работает механизм автоматического commit в SQLAlchemy?
4. Что такое `sessionmaker` и для чего он используется?
5. Какой метод используется для получения только одного результата?
6. В чем разница между `scalar()`, `first()` и `all()`?
7. Как создать уникальный индекс на поле с помощью SQLAlchemy?
