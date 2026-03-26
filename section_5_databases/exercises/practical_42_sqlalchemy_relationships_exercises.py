"""
Упражнения к практической работе 42: Отношения в SQLAlchemy

Выполните упражнения по работе с отношениями в SQLAlchemy.
"""

# Упражнение 1: One-to-Many
def exercise_one_to_many():
    """
    Создайте отношение один ко многим.
    """
    from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker
    
    Base = declarative_base()
    
    class Author(Base):
        __tablename__ = 'authors'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        
        # Отношение один ко многим
        books = relationship("Book", back_populates="author")
    
    class Book(Base):
        __tablename__ = 'books'
        
        id = Column(Integer, primary_key=True)
        title = Column(String(200))
        author_id = Column(Integer, ForeignKey('authors.id'))
        
        # Обратное отношение
        author = relationship("Author", back_populates="books")
    
    engine = create_engine('sqlite:///library.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Создание автора и книг
    author = Author(name='Толстой')
    book1 = Book(title='Война и мир', author=author)
    book2 = Book(title='Анна Каренина', author=author)
    
    session.add(author)
    session.commit()


# Упражнение 2: Many-to-Many
def exercise_many_to_many():
    """
    Создайте отношение многие ко многим.
    """
    from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker
    
    Base = declarative_base()
    
    # Промежуточная таблица
    student_course = Table('student_courses', Base.metadata,
        Column('student_id', Integer, ForeignKey('students.id')),
        Column('course_id', Integer, ForeignKey('courses.id'))
    )
    
    class Student(Base):
        __tablename__ = 'students'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        
        courses = relationship("Course", secondary=student_course, back_populates="students")
    
    class Course(Base):
        __tablename__ = 'courses'
        
        id = Column(Integer, primary_key=True)
        title = Column(String(200))
        
        students = relationship("Student", secondary=student_course, back_populates="courses")
    
    engine = create_engine('sqlite:///university.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Создание студентов и курсов
    student1 = Student(name='Иванов')
    student2 = Student(name='Петров')
    course1 = Course(title='Математика')
    course2 = Course(title='Физика')
    
    student1.courses = [course1, course2]
    student2.courses = [course1]
    
    session.add_all([student1, student2, course1, course2])
    session.commit()


# Упражнение 3: One-to-One
def exercise_one_to_one():
    """
    Создайте отношение один к одному.
    """
    from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker
    
    Base = declarative_base()
    
    class Person(Base):
        __tablename__ = 'persons'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        
        passport = relationship("Passport", uselist=False, back_populates="person")
    
    class Passport(Base):
        __tablename__ = 'passports'
        
        id = Column(Integer, primary_key=True)
        number = Column(String(20))
        person_id = Column(Integer, ForeignKey('persons.id'))
        
        person = relationship("Person", back_populates="passport")
    
    engine = create_engine('sqlite:///citizenship.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    person = Person(name='Сидоров')
    passport = Passport(number='1234567890', person=person)
    
    session.add(passport)
    session.commit()


if __name__ == "__main__":
    print("Упражнения по отношениям SQLAlchemy")
