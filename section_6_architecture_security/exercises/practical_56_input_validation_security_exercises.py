"""
Упражнения к практической работе 56: Валидация ввода и безопасность

Выполните упражнения по валидации ввода и обеспечению безопасности.
"""

# Упражнение 1: Базовая валидация
def exercise_basic_validation():
    """
    Реализуйте базовую валидацию ввода.
    """
    # Валидация email адреса
    # Валидация пароля
    # Валидация номера телефона
    pass


# Упражнение 2: SQL Injection защита
def exercise_sql_injection_protection():
    """
    Защититесь от SQL инъекций.
    """
    # Используйте параметризованные запросы
    # Экранируйте пользовательский ввод
    # Примените ORM для запросов
    pass


# Упражнение 3: XSS защита
def exercise_xss_protection():
    """
    Защититесь от XSS атак.
    """
    # Экранируйте HTML теги
    # Используйте Content Security Policy
    # Валидируйте пользовательский ввод
    pass


# Упражнение 4: CSRF защита
def exercise_csrf_protection():
    """
    Защититесь от CSRF атак.
    """
    # Генерируйте CSRF токены
    # Проверяйте токены при POST запросах
    # Используйте SameSite cookies
    pass


# Упражнение 5: Rate limiting
def exercise_rate_limiting():
    """
    Реализуйте ограничение частоты запросов.
    """
    # Создайте RateLimiter класс
    # Ограничьте количество запросов в минуту
    # Блокируйте превысивших лимит
    pass


if __name__ == "__main__":
    print("Упражнения по валидации ввода и безопасности")
    exercise_basic_validation()
    exercise_sql_injection_protection()
    exercise_xss_protection()
    exercise_csrf_protection()
    exercise_rate_limiting()
