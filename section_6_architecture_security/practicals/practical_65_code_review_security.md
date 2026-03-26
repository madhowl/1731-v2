# Практическое занятие 65: Безопасность при code review

## Проверка кода на уязвимости, чеклист безопасности, автоматизация

### Цель занятия:
Изучить методы безопасного code review, освоить чеклист безопасности, научиться автоматизировать проверку кода.

### Задачи:
1. Понять основы безопасного code review
2. Освоить чеклист безопасности
3. Научиться автоматизировать проверку

### План работы:
1. Цель code review
2. Чеклист безопасности
3. Инструменты
4. Практические задания

---

## 1. Чеклист безопасности

### Пример 1: Чеклист для code review

```python
SECURITY_CHECKLIST = {
    "authentication": [
        "Используются безопасные методы аутентификации",
        "Пароли хешируются с использованием соли",
        "Реализована защита от brute force",
        "Используются JWT с коротким временем жизни",
    ],
    "authorization": [
        "Проверка прав доступа на каждом endpoint",
        "Используется принцип最小权限",
        "Нет hardcoded ролей",
    ],
    "input_validation": [
        "Все входные данные валидируются",
        "Используются parameterized queries",
        "Валидация на стороне сервера",
    ],
    "output_encoding": [
        "HTML экранируется перед выводом",
        "JSON данные правильно кодируются",
        "Нет sensitive данных в логах",
    ],
    "cryptography": [
        "Используются современные алгоритмы",
        "Ключи безопасно хранятся",
        "Нет hardcoded ключей в коде",
    ],
    "error_handling": [
        "Нет stack trace в production",
        "Ошибки логируются",
        "Пользователю показываются generic сообщения",
    ]
}

class CodeReviewChecker:
    """Проверка кода на безопасность"""
    
    def __init__(self):
        self.findings = []
    
    def check_code(self, code: str):
        """Проверка кода"""
        issues = []
        
        # Проверка на hardcoded пароли
        if 'password = ' in code.lower() or 'pwd = ' in code.lower():
            issues.append({
                'type': 'hardcoded_password',
                'severity': 'high',
                'description': 'Найден hardcoded пароль'
            })
        
        # Проверка на SQL инъекции
        if 'execute(' in code and '+ ' in code:
            issues.append({
                'type': 'sql_injection',
                'severity': 'critical',
                'description': 'Возможная SQL инъекция'
            })
        
        # Проверка на eval
        if 'eval(' in code:
            issues.append({
                'type': 'dangerous_function',
                'severity': 'high',
                'description': 'Использование eval()'
            })
        
        return issues

# Использование
checker = CodeReviewChecker()
sample_code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    db.execute(query)
"""
issues = checker.check_code(sample_code)
print(issues)
```

---

## 2. Практические задания

### Задание 1: Чеклист

Создайте чеклист безопасности для вашего проекта.

### Задание 2: Автоматизация

Настройте автоматическую проверку в CI/CD.

### Задание 3: Обучение

Проведите тренинг по безопасному code review для команды.
