#!/usr/bin/env python3
"""
Практическое занятие 43: Работа с SQLite
Решение упражнений

Этот файл содержит решения всех упражнений из практического занятия 43
по работе с базой данных SQLite.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Any


# Имя файла базы данных
DATABASE_NAME = 'library.db'


def delete_database():
    """Удаление существующей базы данных для чистого запуска."""
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"База данных {DATABASE_NAME} удалена")


def get_connection() -> sqlite3.Connection:
    """Создание подключения к базе данных."""
    return sqlite3.connect(DATABASE_NAME)


# ============================================================================
# Основные примеры из лекции (демонстрация работы)
# ============================================================================

def example_basic_connection():
    """Пример 1: Подключение к SQLite."""
    print("\n=== Пример 1: Подключение к базе данных ===")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Подключение к базе данных успешно установлено")
    
    conn.close()


def example_context_manager():
    """Пример 2: Использование контекстного менеджера."""
    print("\n=== Пример 2: Контекстный менеджер ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        print(f"Версия SQLite: {version[0]}")


def example_create_students_table():
    """Пример 3: Создание таблицы студентов."""
    print("\n=== Пример 3: Создание таблицы students ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date DATE,
                email TEXT UNIQUE,
                group_number TEXT,
                enrollment_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        print("Таблица students создана успешно")


def example_create_related_tables():
    """Пример 4: Создание связанных таблиц."""
    print("\n=== Пример 4: Создание связанных таблиц ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Таблица преподавателей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                department TEXT,
                hire_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Таблица курсов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                credits INTEGER DEFAULT 3,
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')
        
        # Таблица оценок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                grade REAL,
                date_received DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (course_id) REFERENCES courses (id)
            )
        ''')
        
        print("Связанные таблицы созданы успешно")


def example_insert_single_record():
    """Пример 5: Вставка одиночной записи."""
    print("\n=== Пример 5: Вставка одиночной записи ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (first_name, last_name, birth_date, email, group_number)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Иван', 'Петров', '2000-05-15', 'ivan.petrov@email.com', 'CS-101'))
        
        student_id = cursor.lastrowid
        print(f"Студент добавлен с ID: {student_id}")
        conn.commit()


def example_insert_multiple_records():
    """Пример 6: Вставка нескольких записей."""
    print("\n=== Пример 6: Вставка нескольких записей ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        students_data = [
            ('Мария', 'Сидорова', '1999-11-22', 'maria.sidorova@email.com', 'CS-101'),
            ('Алексей', 'Кузнецов', '2001-03-10', 'alexey.kuznetsov@email.com', 'CS-102'),
            ('Елена', 'Волкова', '2000-08-30', 'elena.volkova@email.com', 'IT-101')
        ]
        
        cursor.executemany('''
            INSERT INTO students (first_name, last_name, birth_date, email, group_number)
            VALUES (?, ?, ?, ?, ?)
        ''', students_data)
        
        print(f"Добавлено {len(students_data)} студентов")
        conn.commit()


def example_select_data():
    """Пример 7: Простая выборка данных."""
    print("\n=== Пример 7: Выборка данных ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Выборка всех студентов
        cursor.execute("SELECT * FROM students")
        all_students = cursor.fetchall()
        
        print("Все студенты:")
        for student in all_students:
            print(student)
        
        # Выборка с условием
        cursor.execute("SELECT * FROM students WHERE group_number = ?", ('CS-101',))
        cs_students = cursor.fetchall()
        
        print("\nСтуденты группы CS-101:")
        for student in cs_students:
            print(f"{student[1]} {student[2]}, email: {student[4]}")


def example_select_with_sort_limit():
    """Пример 8: Выборка с сортировкой и ограничением."""
    print("\n=== Пример 8: Выборка с сортировкой и ограничением ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Выборка с сортировкой
        cursor.execute("SELECT first_name, last_name FROM students ORDER BY last_name ASC")
        sorted_students = cursor.fetchall()
        
        print("Студенты по алфавиту:")
        for student in sorted_students:
            print(f"{student[0]} {student[1]}")
        
        # Выборка с ограничением
        cursor.execute("SELECT * FROM students LIMIT 2 OFFSET 1")
        limited_students = cursor.fetchall()
        
        print(f"\nОграниченная выборка (пропустить 1, взять 2):")
        for student in limited_students:
            print(f"{student[1]} {student[2]}")


def example_update_data():
    """Пример 9: Обновление данных."""
    print("\n=== Пример 9: Обновление данных ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Обновление группы студента
        cursor.execute('''
            UPDATE students 
            SET group_number = ? 
            WHERE email = ?
        ''', ('CS-102', 'ivan.petrov@email.com'))
        
        print(f"Обновлено {cursor.rowcount} записей")
        
        # Проверка обновления
        cursor.execute("SELECT * FROM students WHERE email = ?", ('ivan.petrov@email.com',))
        updated_student = cursor.fetchone()
        print(f"Обновленный студент: {updated_student}")
        
        conn.commit()


def example_delete_data():
    """Пример 10: Удаление данных."""
    print("\n=== Пример 10: Удаление данных ===")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Удаление студента
        cursor.execute("DELETE FROM students WHERE email = ?", ('elena.volkova@email.com',))
        
        print(f"Удалено {cursor.rowcount} записей")
        
        # Проверка удаления
        cursor.execute("SELECT COUNT(*) FROM students WHERE email = ?", ('elena.volkova@email.com',))
        count = cursor.fetchone()[0]
        print(f"Количество оставшихся студентов с этим email: {count}")
        
        conn.commit()


# ============================================================================
# Практические задания
# ============================================================================

def task1_create_library_database():
    """
    Задание 1: Создание базы данных библиотеки
    
    Создайте базу данных для библиотеки с таблицами:
    - books (id, title, author, isbn, publication_year, genre)
    - readers (id, first_name, last_name, email, registration_date)
    - loans (id, book_id, reader_id, loan_date, return_date)
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 1: Создание базы данных библиотеки")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Таблица книг
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                publication_year INTEGER,
                genre TEXT,
                available INTEGER DEFAULT 1
            )
        ''')
        print("Таблица books создана")
        
        # Таблица читателей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                registration_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        print("Таблица readers создана")
        
        # Таблица выдачи книг
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                reader_id INTEGER NOT NULL,
                loan_date DATE DEFAULT CURRENT_DATE,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (reader_id) REFERENCES readers (id)
            )
        ''')
        print("Таблица loans создана")
        
        conn.commit()
        print("\nБаза данных библиотеки успешно создана!")


def task2_populate_database():
    """
    Задание 2: Заполнение базы данных
    
    Добавьте несколько записей в каждую таблицу.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 2: Заполнение базы данных")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Добавление книг
        books_data = [
            ('Война и мир', 'Лев Толстой', '978-5-17-089796-3', 1869, 'Роман'),
            ('Преступление и наказание', 'Федор Достоевский', '978-5-17-983132-5', 1866, 'Роман'),
            ('Мастер и Маргарита', 'Михаил Булгаков', '978-5-17-108727-1', 1967, 'Фэнтези'),
            ('1984', 'Джордж Оруэлл', '978-5-17-112751-9', 1949, 'Антиутопия'),
            ('Унесенные ветром', 'Маргарет Митчелл', '978-5-17-983132-6', 1936, 'Роман'),
            ('Анна Каренина', 'Лев Толстой', '978-5-17-089797-0', 1878, 'Роман'),
            ('Идиот', 'Федор Достоевский', '978-5-17-983132-7', 1869, 'Роман'),
            ('Мертвые души', 'Николай Гоголь', '978-5-17-983132-8', 1842, 'Сатира'),
            ('Евгений Онегин', 'Александр Пушкин', '978-5-17-983132-9', 1833, 'Роман в стихах'),
            ('Герой нашего времени', 'Михаил Лермонтов', '978-5-17-983133-0', 1840, 'Роман')
        ]
        
        cursor.executemany('''
            INSERT INTO books (title, author, isbn, publication_year, genre)
            VALUES (?, ?, ?, ?, ?)
        ''', books_data)
        
        print(f"Добавлено {len(books_data)} книг")
        
        # Добавление читателей
        readers_data = [
            ('Александр', 'Иванов', 'alexandr.ivanov@email.com'),
            ('Наталья', 'Петрова', 'natalia.petrova@email.com'),
            ('Дмитрий', 'Сидоров', 'dmitry.sidorov@email.com'),
            ('Екатерина', 'Смирнова', 'ekaterina.smirnova@email.com'),
            ('Михаил', 'Козлов', 'mikhail.kozlov@email.com')
        ]
        
        cursor.executemany('''
            INSERT INTO readers (first_name, last_name, email)
            VALUES (?, ?, ?)
        ''', readers_data)
        
        print(f"Добавлено {len(readers_data)} читателей")
        
        # Добавление записей о выдаче книг
        # Книги выданы читателям (некоторые уже возвращены)
        loans_data = [
            (1, 1, '2024-01-15', '2024-02-15'),  # Война и мир - возвращена
            (2, 2, '2024-02-01', '2024-03-01'),  # Преступление - возвращена
            (3, 1, '2024-03-10', None),           # Мастер и Маргарита - не возвращена
            (4, 3, '2024-03-15', None),           # 1984 - не возвращена
            (5, 4, '2024-03-20', '2024-04-20'),  # Унесенные ветром - возвращена
            (7, 5, '2024-04-01', None),           # Идиот - не возвращена
            (9, 2, '2024-04-10', None),           # Евгений Онегин - не возвращена
        ]
        
        cursor.executemany('''
            INSERT INTO loans (book_id, reader_id, loan_date, return_date)
            VALUES (?, ?, ?, ?)
        ''', loans_data)
        
        print(f"Добавлено {len(loans_data)} записей о выдаче книг")
        
        # Обновляем доступность книг
        cursor.execute('''
            UPDATE books 
            SET available = 0 
            WHERE id IN (SELECT book_id FROM loans WHERE return_date IS NULL)
        ''')
        
        conn.commit()
        print("\nБаза данных успешно заполнена!")


def task3_join_query():
    """
    Задание 3: Выборка с JOIN
    
    Напишите запрос, который выводит список книг с именами читателей, 
    которые их взяли.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 3: Выборка с JOIN")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Запрос: книги с именами читателей, которые их взяли (не возвращенные)
        cursor.execute('''
            SELECT 
                b.title AS Название_книги,
                b.author AS Автор,
                r.first_name || ' ' || r.last_name AS Читатель,
                l.loan_date AS Дата_выдачи
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN readers r ON l.reader_id = r.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date DESC
        ''')
        
        results = cursor.fetchall()
        
        print("\nНе возвращенные книги:")
        print("-" * 60)
        if results:
            for row in results:
                print(f"Книга: '{row[0]}'")
                print(f"  Автор: {row[1]}")
                print(f"  Читатель: {row[2]}")
                print(f"  Дата выдачи: {row[3]}")
                print()
        else:
            print("Нет не возвращенных книг")
        
        # Альтернативный запрос: все записи (включая возвращенные)
        cursor.execute('''
            SELECT 
                b.title AS Название_книги,
                b.author AS Автор,
                r.first_name || ' ' || r.last_name AS Читатель,
                l.loan_date AS Дата_выдачи,
                l.return_date AS Дата_возврата,
                CASE 
                    WHEN l.return_date IS NULL THEN 'Не возвращена'
                    ELSE 'Возвращена'
                END AS Статус
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN readers r ON l.reader_id = r.id
            ORDER BY l.loan_date DESC
        ''')
        
        all_loans = cursor.fetchall()
        
        print("\nВсе записи о выдаче книг:")
        print("-" * 60)
        for row in all_loans:
            print(f"Книга: '{row[0]}', Автор: {row[1]}")
            print(f"  Читатель: {row[2]}, Выдана: {row[3]}, Возвращена: {row[4] or 'еще не возвращена'}")
            print(f"  Статус: {row[5]}")
            print()


def task4_aggregation():
    """
    Задание 4: Агрегация данных
    
    Напишите запрос, который показывает, сколько книг взял каждый читатель.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 4: Агрегация данных")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Запрос: количество книг у каждого читателя
        cursor.execute('''
            SELECT 
                r.id,
                r.first_name || ' ' || r.last_name AS Читатель,
                r.email AS Email,
                COUNT(l.id) AS Всего_книг,
                SUM(CASE WHEN l.return_date IS NULL THEN 1 ELSE 0 END) AS Не_возвращено,
                SUM(CASE WHEN l.return_date IS NOT NULL THEN 1 ELSE 0 END) AS Возвращено
            FROM readers r
            LEFT JOIN loans l ON r.id = l.reader_id
            GROUP BY r.id, r.first_name, r.last_name, r.email
            ORDER BY Всего_книг DESC
        ''')
        
        results = cursor.fetchall()
        
        print("\nСтатистика по читателям:")
        print("-" * 70)
        print(f"{'ID':<4} {'Читатель':<25} {'Всего':<8} {'Не возвращено':<15} {'Возвращено':<10}")
        print("-" * 70)
        
        for row in results:
            print(f"{row[0]:<4} {row[1]:<25} {row[3]:<8} {row[4]:<15} {row[5]:<10}")
        
        # Общая статистика
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT l.id) AS Всего_выдач,
                COUNT(DISTINCT l.reader_id) AS Активных_читателей,
                SUM(CASE WHEN l.return_date IS NULL THEN 1 ELSE 0 END) AS Не_возвращено
            FROM loans l
        ''')
        
        total_stats = cursor.fetchone()
        
        print("\nОбщая статистика:")
        print(f"  Всего выдач книг: {total_stats[0]}")
        print(f"  Активных читателей: {total_stats[1]}")
        print(f"  Не возвращено книг: {total_stats[2]}")


def task5_search_and_filter():
    """
    Задание 5: Поиск и фильтрация
    
    Найдите все книги определенного автора, опубликованные после 2000 года.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 5: Поиск и фильтрация")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Поиск книг Льва Толстого после 2000 года
        author = 'Лев Толстой'
        year = 2000
        
        cursor.execute('''
            SELECT title, author, publication_year, genre
            FROM books
            WHERE author = ? AND publication_year > ?
            ORDER BY publication_year DESC
        ''', (author, year))
        
        results = cursor.fetchall()
        
        print(f"\nКниги автора '{author}', опубликованные после {year} года:")
        print("-" * 60)
        
        if results:
            for row in results:
                print(f"  Название: {row[0]}")
                print(f"  Год публикации: {row[2]}")
                print(f"  Жанр: {row[3]}")
                print()
        else:
            print(f"  Книг автора '{author}' после {year} года не найдено")
        
        # Дополнительный поиск: все книги по жанру
        print("\n" + "-" * 60)
        print("Все книги жанра 'Роман':")
        print("-" * 60)
        
        cursor.execute('''
            SELECT title, author, publication_year
            FROM books
            WHERE genre = ?
            ORDER BY author, publication_year
        ''', ('Роман',))
        
        roman_books = cursor.fetchall()
        
        for row in roman_books:
            print(f"  '{row[0]}' - {row[1]} ({row[2]} г.)")
        
        # Поиск по ISBN
        print("\n" + "-" * 60)
        print("Поиск книги по ISBN:")
        print("-" * 60)
        
        isbn = '978-5-17-089796-3'
        cursor.execute('SELECT * FROM books WHERE isbn = ?', (isbn,))
        book = cursor.fetchone()
        
        if book:
            print(f"  Найдена книга: {book[1]}")
            print(f"  Автор: {book[2]}")
            print(f"  ISBN: {book[3]}")
            print(f"  Год: {book[4]}")
            print(f"  Жанр: {book[5]}")


def task6_create_indexes():
    """
    Задание 6: Создание индексов
    
    Создайте индексы для ускорения поиска по автору книги 
    и фамилии читателя.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 6: Создание индексов")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Создание индекса для поиска по автору
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_books_author 
            ON books (author)
        ''')
        print("Индекс idx_books_author создан (поиск по автору)")
        
        # Создание индекса для поиска по фамилии читателя
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_readers_last_name 
            ON readers (last_name)
        ''')
        print("Индекс idx_readers_last_name создан (поиск по фамилии)")
        
        # Создание индекса для поиска по email читателя
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_readers_email 
            ON readers (email)
        ''')
        print("Индекс idx_readers_email создан (поиск по email)")
        
        # Создание индекса для поиска по дате выдачи
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_loans_loan_date 
            ON loans (loan_date)
        ''')
        print("Индекс idx_loans_loan_date создан (поиск по дате выдачи)")
        
        conn.commit()
        
        # Показываем все созданные индексы
        cursor.execute('''
            SELECT name, tbl_name 
            FROM sqlite_master 
            WHERE type = 'index' AND name LIKE 'idx_%'
        ''')
        
        indexes = cursor.fetchall()
        
        print("\nСозданные индексы:")
        for idx in indexes:
            print(f"  {idx[0]} (таблица: {idx[1]})")


def task7_transactions():
    """
    Задание 7: Транзакции
    
    Реализуйте транзакцию для выдачи книги читателю с проверкой 
    наличия книги.
    """
    print("\n" + "="*60)
    print("ЗАДАНИЕ 7: Транзакции")
    print("="*60)
    
    def issue_book(book_id: int, reader_id: int) -> bool:
        """
        Выдача книги читателю с использованием транзакции.
        
        Returns:
            True если книга успешно выдана, False в противном случае
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Начало транзакции
            conn.execute("BEGIN TRANSACTION")
            
            # Проверка наличия книги
            cursor.execute(
                "SELECT id, title, available FROM books WHERE id = ?",
                (book_id,)
            )
            book = cursor.fetchone()
            
            if not book:
                print(f"Ошибка: Книга с ID {book_id} не найдена")
                conn.execute("ROLLBACK")
                return False
            
            if not book[2]:  # available
                print(f"Ошибка: Книга '{book[1]}' уже выдана")
                conn.execute("ROLLBACK")
                return False
            
            # Проверка существования читателя
            cursor.execute(
                "SELECT id, first_name, last_name FROM readers WHERE id = ?",
                (reader_id,)
            )
            reader = cursor.fetchone()
            
            if not reader:
                print(f"Ошибка: Читатель с ID {reader_id} не найден")
                conn.execute("ROLLBACK")
                return False
            
            # Проверка лимита книг (не более 3 книг на читателя)
            cursor.execute(
                "SELECT COUNT(*) FROM loans WHERE reader_id = ? AND return_date IS NULL",
                (reader_id,)
            )
            current_loans = cursor.fetchone()[0]
            
            if current_loans >= 3:
                print(f"Ошибка: Читатель '{reader[1]} {reader[2]}' уже имеет 3 книги")
                conn.execute("ROLLBACK")
                return False
            
            # Выдача книги
            loan_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "INSERT INTO loans (book_id, reader_id, loan_date) VALUES (?, ?, ?)",
                (book_id, reader_id, loan_date)
            )
            
            # Обновление статуса доступности книги
            cursor.execute(
                "UPDATE books SET available = 0 WHERE id = ?",
                (book_id,)
            )
            
            # Фиксация транзакции
            conn.execute("COMMIT")
            
            print(f"Успех: Книга '{book[1]}' выдана читателю '{reader[1]} {reader[2]}'")
            print(f"  Дата выдачи: {loan_date}")
            return True
            
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            conn.execute("ROLLBACK")
            return False
        finally:
            conn.close()
    
    def return_book(loan_id: int) -> bool:
        """
        Возврат книги с использованием транзакции.
        
        Returns:
            True если книга успешно возвращена, False в противном случае
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            conn.execute("BEGIN TRANSACTION")
            
            # Проверка существования записи о выдаче
            cursor.execute(
                "SELECT id, book_id, return_date FROM loans WHERE id = ?",
                (loan_id,)
            )
            loan = cursor.fetchone()
            
            if not loan:
                print(f"Ошибка: Запись о выдаче с ID {loan_id} не найдена")
                conn.execute("ROLLBACK")
                return False
            
            if loan[2]:  # return_date already set
                print(f"Ошибка: Книга уже была возвращена")
                conn.execute("ROLLBACK")
                return False
            
            # Установка даты возврата
            return_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "UPDATE loans SET return_date = ? WHERE id = ?",
                (return_date, loan_id)
            )
            
            # Обновление статуса доступности книги
            cursor.execute(
                "UPDATE books SET available = 1 WHERE id = ?",
                (loan[1],)
            )
            
            conn.execute("COMMIT")
            
            print(f"Успех: Книга возвращена {return_date}")
            return True
            
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            conn.execute("ROLLBACK")
            return False
        finally:
            conn.close()
    
    # Демонстрация работы транзакций
    
    print("\n--- Попытка выдать книгу, которая уже выдана ---")
    issue_book(3, 1)  # Мастер и Маргарита уже выдана
    
    print("\n--- Выдача доступной книги ---")
    # id=6 - Анна Каренина (доступна)
    issue_book(6, 1)
    
    print("\n--- Попытка превысить лимит книг ---")
    # Попробуем выдать еще книги читателю 1
    issue_book(8, 1)  # Мертвые души
    issue_book(10, 1) # Герой нашего времени
    
    print("\n--- Возврат книги ---")
    # Находим ID записи о выдаче
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM loans 
            WHERE book_id = 6 AND return_date IS NULL
        ''')
        loan = cursor.fetchone()
        if loan:
            return_book(loan[0])
    
    print("\n--- Повторная выдача книги после возврата ---")
    issue_book(6, 1)


# ============================================================================
# Дополнительные функции для работы с базой данных
# ============================================================================

def demonstrate_crud_operations():
    """Демонстрация полных CRUD операций."""
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНО: CRUD операции")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # CREATE - Создание
        print("\n[CREATE] Добавление новой книги:")
        cursor.execute('''
            INSERT INTO books (title, author, isbn, publication_year, genre)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Скотный двор', 'Джордж Оруэлл', '978-5-17-999999-9', 1945, 'Аллегория'))
        conn.commit()
        new_book_id = cursor.lastrowid
        print(f"  Добавлена книга с ID: {new_book_id}")
        
        # READ - Чтение
        print("\n[READ] Чтение добавленной книги:")
        cursor.execute("SELECT * FROM books WHERE id = ?", (new_book_id,))
        book = cursor.fetchone()
        print(f"  {book}")
        
        # UPDATE - Обновление
        print("\n[UPDATE] Обновление книги:")
        cursor.execute(
            "UPDATE books SET genre = ? WHERE id = ?",
            ("Притча", new_book_id)
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (new_book_id,))
        book = cursor.fetchone()
        print(f"  Обновленная запись: {book}")
        
        # DELETE - Удаление
        print("\n[DELETE] Удаление книги:")
        cursor.execute("DELETE FROM books WHERE id = ?", (new_book_id,))
        conn.commit()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (new_book_id,))
        book = cursor.fetchone()
        print(f"  Книга после удаления: {book}")


def demonstrate_aggregation_functions():
    """Демонстрация агрегатных функций."""
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНО: Агрегатные функции")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # COUNT
        print("\n[COUNT] Количество книг в библиотеке:")
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()[0]
        print(f"  Всего книг: {count}")
        
        # COUNT с условием
        cursor.execute("SELECT COUNT(*) FROM books WHERE available = 1")
        available = cursor.fetchone()[0]
        print(f"  Доступных книг: {available}")
        
        # AVG - среднее значение
        print("\n[AVG] Средний год публикации книг:")
        cursor.execute("SELECT AVG(publication_year) FROM books")
        avg_year = cursor.fetchone()[0]
        print(f"  Средний год: {avg_year:.1f}")
        
        # MIN/MAX
        print("\n[MIN/MAX] Самая старая и новая книги:")
        cursor.execute("SELECT MIN(publication_year), MAX(publication_year) FROM books")
        years = cursor.fetchone()
        print(f"  Годы: {years[0]} - {years[1]}")
        
        # SUM
        print("\n[SUM] Сумма кредитов (для примера с курсами):")
        # Используем другую таблицу для демонстрации
        cursor.execute("SELECT SUM(credits) FROM courses")
        sum_credits = cursor.fetchone()[0]
        print(f"  Сумма кредитов: {sum_credits}")
        
        # GROUP BY
        print("\n[GROUP BY] Количество книг по жанрам:")
        cursor.execute('''
            SELECT genre, COUNT(*) as count 
            FROM books 
            GROUP BY genre 
            ORDER BY count DESC
        ''')
        genres = cursor.fetchall()
        for genre in genres:
            print(f"  {genre[0]}: {genre[1]}")
        
        # HAVING
        print("\n[HAVING] Жанры с более чем 1 книгой:")
        cursor.execute('''
            SELECT genre, COUNT(*) as count 
            FROM books 
            GROUP BY genre 
            HAVING count > 1
        ''')
        genres = cursor.fetchall()
        for genre in genres:
            print(f"  {genre[0]}: {genre[1]}")


def demonstrate_subqueries():
    """Демонстрация подзапросов."""
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНО: Подзапросы")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Подзапрос в WHERE
        print("\n[Подзапрос] Книги, которые никогда не выдавались:")
        cursor.execute('''
            SELECT title, author 
            FROM books 
            WHERE id NOT IN (SELECT DISTINCT book_id FROM loans)
        ''')
        never_loaned = cursor.fetchall()
        for book in never_loaned:
            print(f"  '{book[0]}' - {book[1]}")
        
        # Подзапрос в FROM (derived table)
        print("\n[Подзапрос] Читатели с количеством книг выше среднего:")
        cursor.execute('''
            SELECT r.first_name, r.last_name, loan_count
            FROM readers r
            JOIN (
                SELECT reader_id, COUNT(*) as loan_count
                FROM loans
                GROUP BY reader_id
            ) l ON r.id = l.reader_id
            WHERE loan_count > (
                SELECT AVG(cnt) 
                FROM (SELECT COUNT(*) as cnt FROM loans GROUP BY reader_id)
            )
        ''')
        active_readers = cursor.fetchall()
        for reader in active_readers:
            print(f"  {reader[0]} {reader[1]}: {reader[2]} книг")
        
        # Подзапрос с EXISTS
        print("\n[Подзапрос EXISTS] Читатели, которые брали книги:")
        cursor.execute('''
            SELECT first_name, last_name 
            FROM readers r
            WHERE EXISTS (
                SELECT 1 FROM loans l WHERE l.reader_id = r.id
            )
        ''')
        borrowers = cursor.fetchall()
        for reader in borrowers:
            print(f"  {reader[0]} {reader[1]}")


def cleanup_database():
    """Очистка базы данных (удаление всех таблиц)."""
    print("\n" + "="*60)
    print("ОЧИСТКА БАЗЫ ДАННЫХ")
    print("="*60)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Удаление таблиц
        cursor.execute("DROP TABLE IF EXISTS loans")
        cursor.execute("DROP TABLE IF EXISTS readers")
        cursor.execute("DROP TABLE IF EXISTS books")
        cursor.execute("DROP TABLE IF EXISTS grades")
        cursor.execute("DROP TABLE IF EXISTS courses")
        cursor.execute("DROP TABLE IF EXISTS teachers")
        cursor.execute("DROP TABLE IF EXISTS students")
        
        conn.commit()
        print("Все таблицы удалены")


# ============================================================================
# Основная функция
# ============================================================================

def main():
    """Основная функция для запуска всех примеров и заданий."""
    print("="*60)
    print("ПРАКТИЧЕСКОЕ ЗАНЯТИЕ 43: РАБОТА С SQLITE")
    print("="*60)
    
    # Удаление старой базы данных для чистого запуска
    delete_database()
    
    # Демонстрация основных примеров из лекции
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ ОСНОВНЫХ ПРИМЕРОВ")
    print("="*60)
    
    example_basic_connection()
    example_context_manager()
    example_create_students_table()
    example_create_related_tables()
    example_insert_single_record()
    example_insert_multiple_records()
    example_select_data()
    example_select_with_sort_limit()
    example_update_data()
    example_delete_data()
    
    # Выполнение практических заданий
    task1_create_library_database()
    task2_populate_database()
    task3_join_query()
    task4_aggregation()
    task5_search_and_filter()
    task6_create_indexes()
    task7_transactions()
    
    # Дополнительные демонстрации
    demonstrate_crud_operations()
    demonstrate_aggregation_functions()
    demonstrate_subqueries()
    
    print("\n" + "="*60)
    print("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
    print("="*60)
    print(f"\nБаза данных создана: {DATABASE_NAME}")
    print("Вы можете открыть её в sqlite3 для просмотра данных:")
    print(f"  sqlite3 {DATABASE_NAME}")


if __name__ == '__main__':
    main()
