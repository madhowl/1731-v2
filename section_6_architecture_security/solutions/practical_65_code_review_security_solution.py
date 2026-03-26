#!/usr/bin/env python3
"""
Практическое занятие 65: Безопасность при code review
Решение упражнений
"""

import re
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Security Checklist
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Security Checklist")
print("=" * 60)


SECURITY_CHECKLIST = {
    "authentication": [
        "Используются безопасные методы аутентификации",
        "Пароли хешируются с использованием соли",
        "Реализована защита от brute force",
        "Используются JWT с коротким временем жизни",
    ],
    "authorization": [
        "Проверка прав доступа на каждом endpoint",
        "Используется принцип минимальных привилегий",
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


class ChecklistManager:
    """Менеджер чеклиста безопасности"""
    
    def __init__(self):
        self.checklist = SECURITY_CHECKLIST.copy()
        self.completed_items: List[str] = []
    
    def get_items_by_category(self, category: str) -> List[str]:
        return self.checklist.get(category, [])
    
    def mark_completed(self, item: str):
        if item not in self.completed_items:
            self.completed_items.append(item)
    
    def get_progress(self) -> Dict[str, Any]:
        total = sum(len(items) for items in self.checklist.values())
        completed = len(self.completed_items)
        
        return {
            'total': total,
            'completed': completed,
            'percentage': (completed / total * 100) if total > 0 else 0
        }


manager = ChecklistManager()

print("Security Checklist Categories:")
for category, items in SECURITY_CHECKLIST.items():
    print(f"\n{category.upper()}:")
    for item in items:
        print(f"  - {item}")

manager.mark_completed("Используются безопасные методы аутентификации")
manager.mark_completed("Пароли хешируются с использованием соли")

progress = manager.get_progress()
print(f"\nProgress: {progress['completed']}/{progress['total']} ({progress['percentage']:.1f}%)")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Code Review Checker
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Code Review Checker")
print("=" * 60)


@dataclass
class SecurityFinding:
    type: str
    severity: str
    line: int
    description: str
    recommendation: str


class CodeReviewChecker:
    """Проверка кода на безопасность"""
    
    def __init__(self):
        self.findings: List[SecurityFinding] = []
    
    def check_code(self, code: str, filename: str = "unknown") -> List[Dict[str, Any]]:
        """Проверка кода"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            if re.search(r'password\s*=\s*["\']', line_lower) or \
               re.search(r'pwd\s*=\s*["\']', line_lower) or \
               re.search(r'passwd\s*=\s*["\']', line_lower):
                issues.append({
                    'type': 'hardcoded_password',
                    'severity': 'high',
                    'line': i,
                    'description': 'Найден hardcoded пароль',
                    'recommendation': 'Используйте переменные окружения'
                })
            
            if 'execute(' in line and ('+' in line or "'" in line):
                issues.append({
                    'type': 'sql_injection',
                    'severity': 'critical',
                    'line': i,
                    'description': 'Возможная SQL инъекция',
                    'recommendation': 'Используйте parameterized queries'
                })
            
            if 'eval(' in line:
                issues.append({
                    'type': 'dangerous_function',
                    'severity': 'high',
                    'line': i,
                    'description': 'Использование eval()',
                    'recommendation': 'Избегайте eval(), используйте ast.literal_eval'
                })
            
            if re.search(r'secret\s*=\s*["\']', line_lower) or \
               re.search(r'api[_-]?key\s*=\s*["\']', line_lower):
                issues.append({
                    'type': 'hardcoded_secret',
                    'severity': 'critical',
                    'line': i,
                    'description': 'Найден hardcoded secret/API key',
                    'recommendation': 'Храните secrets в переменных окружения'
                })
            
            if 'pickle.load' in line or 'pickle.loads' in line:
                issues.append({
                    'type': 'unsafe_deserialization',
                    'severity': 'critical',
                    'line': i,
                    'description': 'Использование pickle для десериализации',
                    'recommendation': 'Используйте JSON или безопасные форматы'
                })
            
            if re.search(r'system\(', line) or re.search(r'subprocess\([^)]*shell\s*=\s*True', line):
                issues.append({
                    'type': 'command_injection',
                    'severity': 'critical',
                    'line': i,
                    'description': 'Возможная command injection',
                    'recommendation': 'Избегайте shell=True, валидируйте ввод'
                })
            
            if 'random.' in line and ('password' in line_lower or 'token' in line_lower):
                issues.append({
                    'type': 'weak_random',
                    'severity': 'medium',
                    'line': i,
                    'description': 'Использование random для криптографии',
                    'recommendation': 'Используйте secrets или os.urandom'
                })
        
        return issues


checker = CodeReviewChecker()

sample_code = """
def get_user(user_id):
    password = "admin123"
    query = "SELECT * FROM users WHERE id = " + user_id
    db.execute(query)
    
    secret_key = "my-secret-key"
    eval(user_input)
"""

issues = checker.check_code(sample_code)

print("Security Issues Found:")
for issue in issues:
    print(f"  [{issue['severity'].upper()}] Line {issue['line']}: {issue['type']}")
    print(f"    {issue['description']}")
    print(f"    Recommendation: {issue['recommendation']}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: CI/CD Integration
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: CI/CD Integration")
print("=" * 60)


class CICDSecurityCheck:
    """Интеграция безопасности в CI/CD"""
    
    def __init__(self):
        self.checks: List[Dict[str, Any]] = []
    
    def add_check(self, name: str, command: str, severity: str = "medium"):
        self.checks.append({
            'name': name,
            'command': command,
            'severity': severity,
            'enabled': True
        })
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        return {
            'name': 'Security Pipeline',
            'stages': [
                {
                    'name': 'Static Analysis',
                    'checks': [c for c in self.checks if c['enabled']]
                },
                {
                    'name': 'Dependency Scanning',
                    'checks': [
                        {'name': 'Check vulnerabilities', 'command': 'safety check', 'severity': 'high'}
                    ]
                },
                {
                    'name': 'Secret Detection',
                    'checks': [
                        {'name': 'Scan for secrets', 'command': 'trufflehog', 'severity': 'critical'}
                    ]
                }
            ]
        }


cicd = CICDSecurityCheck()
cicd.add_check('Bandit', 'bandit -r .', 'medium')
cicd.add_check('Pylint', 'pylint .', 'low')
cicd.add_check('Safety', 'safety check', 'high')

config = cicd.get_pipeline_config()

print("CI/CD Security Pipeline:")
for stage in config['stages']:
    print(f"\n{stage['name']}:")
    for check in stage['checks']:
        print(f"  - {check['name']}: {check['command']}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Code Review Report
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Code Review Report")
print("=" * 60)


class CodeReviewReport:
    """Генератор отчёта о code review"""
    
    def __init__(self, repository: str, branch: str):
        self.repository = repository
        self.branch = branch
        self.findings: List[Dict[str, Any]] = []
        self.review_date = datetime.now()
    
    def add_finding(self, finding_type: str, severity: str, description: str, 
                   file: str = None, line: int = None):
        self.findings.append({
            'type': finding_type,
            'severity': severity,
            'description': description,
            'file': file,
            'line': line,
            'status': 'open'
        })
    
    def generate_summary(self) -> Dict[str, Any]:
        by_severity = {}
        for finding in self.findings:
            sev = finding['severity']
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        return {
            'repository': self.repository,
            'branch': self.branch,
            'date': self.review_date.isoformat(),
            'total_findings': len(self.findings),
            'by_severity': by_severity
        }


report = CodeReviewReport('myapp', 'feature/login')

report.add_finding('hardcoded_password', 'high', 'Hardcoded password found', 'auth.py', 42)
report.add_finding('sql_injection', 'critical', 'SQL injection vulnerability', 'users.py', 15)
report.add_finding('eval_usage', 'medium', 'Using eval() function', 'utils.py', 8)

summary = report.generate_summary()

print(f"Repository: {summary['repository']}")
print(f"Branch: {summary['branch']}")
print(f"Date: {summary['date']}")
print(f"Total findings: {summary['total_findings']}")
print("\nBy severity:")
for severity, count in summary['by_severity'].items():
    print(f"  {severity}: {count}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
