#!/usr/bin/env python3
"""
Практическое занятие 64: Стратегии резервного копирования и восстановления
Решение упражнений
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# ==============================================================================
# УПРАЖНЕНИЕ 1: Backup Types
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Backup Types")
print("=" * 60)


class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    MIRROR = "mirror"


@dataclass
class Backup:
    id: str
    backup_type: BackupType
    created_at: datetime
    size_bytes: int
    path: str
    status: str = "completed"
    files_count: int = 0


class BackupManager:
    """Менеджер резервного копирования"""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.backups: List[Backup] = []
        self._backup_counter = 1
    
    def create_full_backup(self, source_path: str) -> Backup:
        """Создание полной резервной копии"""
        backup_id = f"backup_{self._backup_counter:04d}"
        self._backup_counter += 1
        
        backup = Backup(
            id=backup_id,
            backup_type=BackupType.FULL,
            created_at=datetime.now(),
            size_bytes=1024 * 1024 * 100,
            path=f"{self.storage_path}/{backup_id}.tar.gz",
            status="completed",
            files_count=1500
        )
        
        self.backups.append(backup)
        return backup
    
    def create_incremental_backup(self, source_path: str, base_backup: Backup) -> Backup:
        """Создание инкрементной резервной копии"""
        backup_id = f"backup_{self._backup_counter:04d}"
        self._backup_counter += 1
        
        backup = Backup(
            id=backup_id,
            backup_type=BackupType.INCREMENTAL,
            created_at=datetime.now(),
            size_bytes=1024 * 1024 * 10,
            path=f"{self.storage_path}/{backup_id}.tar.gz",
            status="completed",
            files_count=50
        )
        
        self.backups.append(backup)
        return backup
    
    def get_backup_info(self, backup_id: str) -> Optional[Backup]:
        """Получение информации о резервной копии"""
        for backup in self.backups:
            if backup.id == backup_id:
                return backup
        return None


manager = BackupManager("/backups")

full_backup = manager.create_full_backup("/data")
print(f"Created full backup: {full_backup.id}")
print(f"  Type: {full_backup.backup_type.value}")
print(f"  Size: {full_backup.size_bytes / (1024*1024):.1f} MB")

incremental = manager.create_incremental_backup("/data", full_backup)
print(f"Created incremental backup: {incremental.id}")
print(f"  Type: {incremental.backup_type.value}")
print(f"  Size: {incremental.size_bytes / (1024*1024):.1f} MB")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Backup Schedule
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Backup Schedule")
print("=" * 60)


class BackupSchedule:
    """Расписание резервного копирования"""
    
    def __init__(self):
        self.schedules: List[Dict[str, Any]] = []
    
    def add_schedule(self, name: str, backup_type: str, frequency: str, time: str, retention_days: int):
        self.schedules.append({
            'name': name,
            'backup_type': backup_type,
            'frequency': frequency,
            'time': time,
            'retention_days': retention_days,
            'enabled': True
        })
    
    def get_next_run(self, schedule_name: str) -> Optional[datetime]:
        for schedule in self.schedules:
            if schedule['name'] == schedule_name:
                now = datetime.now()
                hour, minute = map(int, schedule['time'].split(':'))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if now.time().hour > hour or (now.time().hour == hour and now.time().minute > minute):
                    next_run += timedelta(days=1)
                
                return next_run
        return None
    
    def get_schedules_summary(self) -> Dict[str, Any]:
        return {
            'total': len(self.schedules),
            'enabled': sum(1 for s in self.schedules if s['enabled']),
            'schedules': self.schedules
        }


schedule = BackupSchedule()
schedule.add_schedule("Daily Full Backup", "full", "daily", "02:00", 30)
schedule.add_schedule("Hourly Incremental", "incremental", "hourly", "00:00", 7)
schedule.add_schedule("Weekly Archive", "full", "weekly", "03:00", 90)

summary = schedule.get_schedules_summary()
print(f"Total schedules: {summary['enabled']}/{summary['total']} enabled")

next_run = schedule.get_next_run("Daily Full Backup")
print(f"Next full backup: {next_run}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Restore Process
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Restore Process")
print("=" * 60)


class RestoreProcess:
    """Процесс восстановления"""
    
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager
        self.restore_steps: List[Dict[str, Any]] = []
    
    def prepare_restore(self, backup_id: str, target_path: str) -> Dict[str, Any]:
        backup = self.backup_manager.get_backup_info(backup_id)
        
        if not backup:
            return {'success': False, 'error': 'Backup not found'}
        
        return {
            'success': True,
            'backup_id': backup_id,
            'backup_type': backup.backup_type.value,
            'target_path': target_path,
            'estimated_time': '5 minutes',
            'steps': [
                '1. Verify backup integrity',
                '2. Stop application services',
                '3. Restore files to target location',
                '4. Verify restored data',
                '5. Start application services'
            ]
        }
    
    def execute_restore(self, backup_id: str, target_path: str) -> bool:
        prep_result = self.prepare_restore(backup_id, target_path)
        
        if not prep_result['success']:
            return False
        
        print(f"Restoring from backup {backup_id} to {target_path}")
        
        for step in prep_result['steps']:
            print(f"  {step}")
        
        return True


restore = RestoreProcess(manager)
result = restore.prepare_restore("backup_0001", "/data/restore")

print(f"Restore preparation: {result['success']}")
if result['success']:
    print(f"  Steps: {len(result['steps'])}")
    print(f"  Estimated time: {result['estimated_time']}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Disaster Recovery Plan
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Disaster Recovery Plan")
print("=" * 60)


@dataclass
class RecoveryPoint:
    rto_minutes: int
    rpo_minutes: int
    description: str


class DisasterRecoveryPlan:
    """План аварийного восстановления"""
    
    def __init__(self):
        self.recovery_points: List[RecoveryPoint] = []
        self.contact_list: List[Dict[str, str]] = []
        self.checklist: List[Dict[str, Any]] = []
    
    def add_recovery_point(self, name: str, rto_minutes: int, rpo_minutes: int):
        self.recovery_points.append(RecoveryPoint(rto_minutes, rpo_minutes, name))
    
    def add_contact(self, name: str, role: str, phone: str, email: str):
        self.contact_list.append({
            'name': name,
            'role': role,
            'phone': phone,
            'email': email
        })
    
    def add_checklist_item(self, item: str):
        self.checklist.append({
            'item': item,
            'completed': False,
            'completed_at': None
        })
    
    def get_recovery_summary(self) -> Dict[str, Any]:
        if not self.recovery_points:
            return {'error': 'No recovery points defined'}
        
        best_rto = min(rp.rto_minutes for rp in self.recovery_points)
        best_rpo = min(rp.rpo_minutes for rp in self.recovery_points)
        
        return {
            'best_rto_minutes': best_rto,
            'best_rpo_minutes': best_rpo,
            'contacts': len(self.contact_list),
            'checklist_items': len(self.checklist)
        }


plan = DisasterRecoveryPlan()
plan.add_recovery_point("Critical", 15, 5)
plan.add_recovery_point("Standard", 60, 30)
plan.add_recovery_point("Basic", 240, 60)

plan.add_contact("John Doe", "IT Director", "+1234567890", "john@example.com")
plan.add_contact("Jane Smith", "Security Lead", "+0987654321", "jane@example.com")

plan.add_checklist_item("Verify backup availability")
plan.add_checklist_item("Notify stakeholders")
plan.add_checklist_item("Initiate restore procedure")

summary = plan.get_recovery_summary()
print(f"RTO: {summary['best_rto_minutes']} minutes")
print(f"RPO: {summary['best_rpo_minutes']} minutes")
print(f"Contacts: {summary['contacts']}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Backup Verification
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Backup Verification")
print("=" * 60)


class BackupVerification:
    """Проверка резервных копий"""
    
    def __init__(self):
        self.verification_results: List[Dict[str, Any]] = []
    
    def verify_backup(self, backup: Backup) -> Dict[str, Any]:
        result = {
            'backup_id': backup.id,
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'file_exists': True,
                'readable': True,
                'checksum_valid': True,
                'size_reasonable': backup.size_bytes > 0
            },
            'status': 'passed'
        }
        
        if not all(result['checks'].values()):
            result['status'] = 'failed'
        
        self.verification_results.append(result)
        return result
    
    def get_verification_summary(self) -> Dict[str, Any]:
        total = len(self.verification_results)
        passed = sum(1 for r in self.verification_results if r['status'] == 'passed')
        
        return {
            'total': total,
            'passed': passed,
            'failed': total - passed
        }


verification = BackupVerification()

for backup in manager.backups:
    result = verification.verify_backup(backup)
    print(f"Backup {backup.id}: {result['status']}")

summary = verification.get_verification_summary()
print(f"Verification summary: {summary['passed']}/{summary['total']} passed")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
