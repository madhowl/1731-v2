# Практическое занятие 68: Аудит безопасности и соответствие нормам

## Аудит безопасности, compliance, стандарты, отчётность

### Цель занятия:
Изучить методы проведения аудита безопасности, освоить compliance требования, научиться создавать отчёты.

### Задачи:
1. Понять основы аудита безопасности
2. Освоить compliance стандарты
3. Научиться создавать отчёты

### План работы:
1. Аудит безопасности
2. Compliance стандарты
3. Отчётность
4. Практические задания

---

## 1. Аудит безопасности

### Пример 1: Чеклист аудита

```python
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class AuditFinding:
    """Находка аудита"""
    category: str
    requirement: str
    status: str  # PASS, FAIL, N/A
    evidence: str
    recommendation: str

class SecurityAudit:
    """Аудит безопасности"""
    
    def __init__(self, audit_name: str):
        self.audit_name = audit_name
        self.findings: List[AuditFinding] = []
        self.audit_date = datetime.now()
    
    def add_finding(self, category: str, requirement: str, status: str, evidence: str, recommendation: str = ""):
        self.findings.append(AuditFinding(category, requirement, status, evidence, recommendation))
    
    def get_summary(self) -> dict:
        """Получение сводки"""
        passed = sum(1 for f in self.findings if f.status == "PASS")
        failed = sum(1 for f in self.findings if f.status == "FAIL")
        na = sum(1 for f in self.findings if f.status == "N/A")
        
        return {
            'audit_name': self.audit_name,
            'date': self.audit_date.isoformat(),
            'total': len(self.findings),
            'passed': passed,
            'failed': failed,
            'na': na,
            'compliance_rate': (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
        }

# Аудит
audit = SecurityAudit("Web Application Security Audit")

# Добавление находок
audit.add_finding(
    category="Authentication",
    requirement="Пароли хешируются с солью",
    status="PASS",
    evidence="Используется PBKDF2 с солью",
    recommendation=""
)

audit.add_finding(
    category="Authentication",
    requirement="Защита от brute force",
    status="FAIL",
    evidence="Нет защиты от brute force",
    recommendation="Добавить rate limiting"
)

# Сводка
summary = audit.get_summary()
print(f"Compliance Rate: {summary['compliance_rate']:.1f}%")
```

---

## 2. Compliance стандарты

### Пример 2: Проверка соответствия GDPR

```python
GDPR_REQUIREMENTS = {
    "data_encryption": "Данные должны быть зашифрованы",
    "access_control": "Контроль доступа к персональным данным",
    "consent": "Согласие на обработку персональных данных",
    "deletion_right": "Право на удаление персональных данных",
    "data_portability": "Переносимость персональных данных",
    "breach_notification": "Уведомление об утечке данных за 72 часа"
}

class GDPRCompliance:
    """Проверка соответствия GDPR"""
    
    def __init__(self):
        self.compliance = {}
    
    def check_requirement(self, requirement: str, compliant: bool, evidence: str):
        self.compliance[requirement] = {
            'compliant': compliant,
            'evidence': evidence
        }
    
    def generate_report(self) -> dict:
        compliant_count = sum(1 for v in self.compliance.values() if v['compliant'])
        total = len(self.compliance)
        
        return {
            'standard': 'GDPR',
            'compliant_count': compliant_count,
            'total_requirements': total,
            'compliance_percentage': (compliant_count / total * 100) if total > 0 else 0,
            'details': self.compliance
        }

# Использование
gdpr = GDPRCompliance()

gdpr.check_requirement(
    "data_encryption",
    True,
    "AES-256 используется для шифрования данных"
)

gdpr.check_requirement(
    "deletion_right",
    True,
    "Реализован endpoint для удаления данных"
)

report = gdpr.generate_report()
print(f"GDPR Compliance: {report['compliance_percentage']:.1f}%")
```

---

## 3. Отчётность

### Пример 3: Генерация отчёта

```python
import json
from datetime import datetime

class AuditReport:
    """Генератор отчётов об аудите"""
    
    def __init__(self, audit: SecurityAudit):
        self.audit = audit
    
    def generate_json(self) -> dict:
        """Генерация JSON отчёта"""
        summary = self.audit.get_summary()
        
        return {
            'report': {
                'title': self.audit.audit_name,
                'date': self.audit.audit_date.isoformat(),
                'summary': summary,
                'findings': [
                    {
                        'category': f.category,
                        'requirement': f.requirement,
                        'status': f.status,
                        'evidence': f.evidence,
                        'recommendation': f.recommendation
                    }
                    for f in self.audit.findings
                ]
            }
        }
    
    def generate_markdown(self) -> str:
        """Генерация Markdown отчёта"""
        summary = self.audit.get_summary()
        
        md = f"""# Отчёт об аудите безопасности

**Название аудита:** {self.audit.audit_name}
**Дата:** {self.audit.audit_date.strftime('%Y-%m-%d')}

## Сводка

- **Всего проверок:** {summary['total']}
- **Пройдено:** {summary['passed']}
- **Провалено:** {summary['failed']}
- **N/A:** {summary['na']}
- **Процент соответствия:** {summary['compliance_rate']:.1f}%

## Находки

"""
        
        for f in self.audit.findings:
            status_icon = "✅" if f.status == "PASS" else "❌" if f.status == "FAIL" else "➖"
            md += f"""### {status_icon} {f.category}: {f.requirement}

- **Статус:** {f.status}
- **Доказательство:** {f.evidence}
- **Рекомендация:** {f.recommendation}

"""
        
        return md

# Использование
report = AuditReport(audit)
json_report = report.generate_json()
md_report = report.generate_markdown()

print(md_report)
```

---

## 4. Практические задания

### Задание 1: Аудит

Проведите аудит безопасности для вашего проекта.

### Задание 2: Compliance

Проверьте соответствие GDPR.

### Задание 3: Отчёт

Создайте отчёт об аудите.

---

## Контрольные вопросы:

1. Что такое аудит безопасности?
2. Какие compliance стандарты вы знаете?
3. Как создать отчёт об аудите?
