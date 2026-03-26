# Практическое занятие 66: Управление зависимостями

## Безопасность зависимостей, обновления, аудит

### Цель занятия:
Изучить методы управления зависимостями, освоить безопасность зависимостей, научиться проводить аудит.

### Задачи:
1. Понять важность управления зависимостями
2. Освоить инструменты аудита
3. Научиться обновлять зависимости

### План работы:
1. Зависимости и безопасность
2. Инструменты аудита
3. Обновление зависимостей
4. Практические задания

---

## 1. Аудит зависимостей

### Пример 1: Проверка уязвимостей

```python
import subprocess
import json
from dataclasses import dataclass

@dataclass
class Vulnerability:
    """Уязвимость в зависимости"""
    package: str
    version: str
    vulnerability_id: str
    severity: str
    description: str

class DependencyAuditor:
    """Аудитор зависимостей"""
    
    def audit_requirements(self, requirements_file: str = 'requirements.txt') -> list:
        """Аудит зависимостей"""
        vulnerabilities = []
        
        try:
            # Запуск pip-audit
            result = subprocess.run(
                ['pip-audit', '-r', requirements_file, '--format=json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for vuln in data.get('dependencies', []):
                    vulnerabilities.append(Vulnerability(
                        package=vuln.get('name'),
                        version=vuln.get('version'),
                        vulnerability_id=vuln.get('vulns', [{}])[0].get('id', 'N/A'),
                        severity=vuln.get('vulns', [{}])[0].get('severity', 'UNKNOWN'),
                        description=vuln.get('vulns', [{}])[0].get('description', '')
                    ))
        
        except Exception as e:
            print(f"Error running audit: {e}")
        
        return vulnerabilities

# Использование
auditor = DependencyAuditor()
vulns = auditor.audit_requirements()

for v in vulns:
    print(f"[{v.severity}] {v.package} {v.version} - {v.vulnerability_id}")
```

### Пример 2: Проверка устаревших пакетов

```python
import subprocess
import json

def check_outdated():
    """Проверка устаревших пакетов"""
    result = subprocess.run(
        ['pip', 'list', '--outdated', '--format=json'],
        capture_output=True,
        text=True
    )
    
    return json.loads(result.stdout)

# Использование
outdated = check_outdated()
for pkg in outdated:
    print(f"{pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
```

---

## 2. Практические задания

### Задание 1: Аудит

Проведите аудит зависимостей вашего проекта.

### Задание 2: Обновление

Обновите устаревшие зависимости.

### Задание 3: Автоматизация

Настройте автоматическую проверку в CI/CD.

---

## Контрольные вопросы:

1. Как проверять зависимости на уязвимости?
2. Как часто нужно обновлять зависимости?
3. Что такое pip-audit?
