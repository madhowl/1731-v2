# Практическое занятие 64: Стратегии резервного копирования и восстановления

## Резервное копирование, восстановление, DR план, тестирование восстановления

### Цель занятия:
Изучить стратегии резервного копирования и восстановления, освоить планирование катастрофоустойчивости, научиться тестировать восстановление.

### Задачи:
1. Понять основы резервного копирования
2. Освоить различные стратегии
3. Научиться создавать DR план

### План работы:
1. Типы резервного копирования
2. Стратегии
3. DR план
4. Тестирование
5. Практические задания

---

## 1. Типы резервного копирования

### Пример 1: Система резервного копирования

```python
import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path

class BackupManager:
    """Менеджер резервного копирования"""
    
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup_database(self, db_path: str, backup_name: str = None):
        """Резервное копирование базы данных"""
        backup_name = backup_name or f"db_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / f"{backup_name}.dump"
        
        # Создание дампа
        os.system(f"pg_dump {db_path} > {backup_path}")
        
        return str(backup_path)
    
    def backup_files(self, source_dir: str, backup_name: str = None):
        """Резервное копирование файлов"""
        backup_name = backup_name or f"files_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / f"{backup_name}.tar.gz"
        
        shutil.make_archive(
            str(self.backup_dir / backup_name),
            'gztar',
            source_dir
        )
        
        return str(backup_path)
    
    def restore_database(self, backup_path: str, db_name: str):
        """Восстановление базы данных"""
        os.system(f"psql {db_name} < {backup_path}")
    
    def list_backups(self) -> list:
        """Список резервных копий"""
        return sorted(self.backup_dir.glob('*'), key=os.path.getmtime, reverse=True)
    
    def cleanup_old_backups(self, days: int = 30):
        """Удаление старых резервных копий"""
        cutoff = datetime.now() - timedelta(days=days)
        
        for backup in self.backup_dir.glob('*'):
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            if mtime < cutoff:
                backup.unlink()
                print(f"Deleted: {backup}")

# Использование
manager = BackupManager('/backups')

# Создание backup
db_backup = manager.backup_database('mydb')
files_backup = manager.backup_files('/app/data')

# Восстановление
# manager.restore_database(db_backup, 'restored_db')

# Очистка
manager.cleanup_old_backups(30)
```

---

## 2. DR План

### Пример 2: DR план

```python
from dataclasses import dataclass
from typing import List
from enum import Enum

class DRStatus(Enum):
    OK = "ok"
    DEGRADED = "degraded"
    DOWN = "down"

@dataclass
class DRStep:
    """Шаг DR плана"""
    order: int
    description: str
    estimated_time: str
    responsible: str

class DRPlan:
    """План восстановления после катастроф"""
    
    def __init__(self, rto_minutes: int = 60, rpo_minutes: int = 15):
        self.rto = rto_minutes  # Recovery Time Objective
        self.rpo = rpo_minutes  # Recovery Point Objective
        self.steps: List[DRStep] = []
    
    def add_step(self, order: int, description: str, time: str, responsible: str):
        self.steps.append(DRStep(order, description, time, responsible))
    
    def execute(self):
        """Выполнение DR плана"""
        print("Starting DR procedure...")
        for step in sorted(self.steps, key=lambda s: s.order):
            print(f"[{step.order}] {step.description}")
        print("DR procedure completed")

# Использование
dr_plan = DRPlan(rto_minutes=60, rpo_minutes=15)

dr_plan.add_step(1, "Оповестить команду", "5 мин", "oncall")
dr_plan.add_step(2, "Проверить статус систем", "10 мин", "ops")
dr_plan.add_step(3, "Запустить backup", "15 мин", "dba")
dr_plan.add_step(4, "Восстановить БД", "20 мин", "dba")
dr_plan.add_step(5, "Проверить работу", "10 мин", "qa")

dr_plan.execute()
```

---

## 3. Практические задания

### Задание 1: Система backup

Создайте систему резервного копирования с ротацией.

### Задание 2: DR план

Разработайте DR план для веб-приложения.

### Задание 3: Тестирование восстановления

Проведите тестирование восстановления.

---

## Контрольные вопросы:

1. Что такое RTO и RPO?
2. Какие типы backup вы знаете?
3. Как часто делать backup?
