#!/usr/bin/env python3
"""
Практическое занятие 66: Управление зависимостями
Решение упражнений
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Dependency Management
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Dependency Management")
print("=" * 60)


@dataclass
class Dependency:
    name: str
    version: str
    latest_version: str = None
    is_vulnerable: bool = False
    vulnerability_details: List[str] = None
    
    def __post_init__(self):
        self.vulnerability_details = self.vulnerability_details or []


class DependencyManager:
    """Менеджер зависимостей"""
    
    def __init__(self):
        self.dependencies: Dict[str, Dependency] = {}
    
    def add_dependency(self, name: str, version: str):
        self.dependencies[name] = Dependency(name, version)
    
    def update_dependency(self, name: str, new_version: str):
        if name in self.dependencies:
            self.dependencies[name].version = new_version
    
    def get_outdated(self) -> List[Dependency]:
        outdated = []
        for dep in self.dependencies.values():
            if dep.latest_version and dep.version != dep.latest_version:
                outdated.append(dep)
        return outdated
    
    def get_vulnerable(self) -> List[Dependency]:
        return [dep for dep in self.dependencies.values() if dep.is_vulnerable]
    
    def generate_requirements_txt(self) -> str:
        lines = []
        for dep in self.dependencies.values():
            lines.append(f"{dep.name}=={dep.version}")
        return "\n".join(lines)


manager = DependencyManager()
manager.add_dependency("flask", "2.0.0")
manager.add_dependency("requests", "2.25.0")
manager.add_dependency("django", "3.2.0")

print("Current dependencies:")
for name, dep in manager.dependencies.items():
    print(f"  {name}: {dep.version}")

requirements = manager.generate_requirements_txt()
print(f"\nGenerated requirements.txt:")
print(requirements)


# ==============================================================================
# УПРАЖНЕНИЕ 2: Vulnerability Scanner
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Vulnerability Scanner")
print("=" * 60)


class VulnerabilityScanner:
    """Сканер уязвимостей в зависимостях"""
    
    KNOWN_VULNERABILITIES = {
        'flask': {
            '2.0.0': ['CVE-2021-23336'],
            '1.0.0': ['CVE-2020-1962', 'CVE-2019-1010083']
        },
        'django': {
            '3.2.0': ['CVE-2021-44420'],
            '2.2.0': ['CVE-2021-3283']
        },
        'requests': {
            '2.25.0': [],
            '2.20.0': ['CVE-2020-26116']
        }
    }
    
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager = dependency_manager
    
    def scan(self) -> List[Dict[str, Any]]:
        results = []
        
        for name, dep in self.dependency_manager.dependencies.items():
            if name in self.KNOWN_VULNERABILITIES:
                vuln_versions = self.KNOWN_VULNERABILITIES[name]
                
                if dep.version in vuln_versions:
                    cves = vuln_versions[dep.version]
                    if cves:
                        dep.is_vulnerable = True
                        dep.vulnerability_details = cves
                        
                        results.append({
                            'package': name,
                            'version': dep.version,
                            'cves': cves,
                            'severity': 'high'
                        })
        
        return results
    
    def get_report(self) -> Dict[str, Any]:
        vulnerable = self.dependency_manager.get_vulnerable()
        
        return {
            'total_packages': len(self.dependency_manager.dependencies),
            'vulnerable_packages': len(vulnerable),
            'vulnerabilities': [
                {
                    'package': dep.name,
                    'version': dep.version,
                    'cves': dep.vulnerability_details
                }
                for dep in vulnerable
            ]
        }


scanner = VulnerabilityScanner(manager)
vulns = scanner.scan()

print(f"Found {len(vulns)} vulnerabilities:")
for vuln in vulns:
    print(f"  {vuln['package']} {vuln['version']}: {', '.join(vuln['cves'])}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Lock File Management
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Lock File Management")
print("=" * 60)


class LockFileManager:
    """Управление lock файлами"""
    
    def __init__(self):
        self.lock_data: Dict[str, Any] = {}
    
    def generate_lock_file(self, dependencies: Dict[str, Dependency]) -> Dict[str, Any]:
        lock_data = {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'packages': {}
        }
        
        for name, dep in dependencies.items():
            lock_data['packages'][name] = {
                'version': dep.version,
                'resolved': f'https://pypi.org/project/{name}/{dep.version}/',
                'dependencies': []
            }
        
        return lock_data
    
    def write_lock_file(self, filepath: str, lock_data: Dict[str, Any]):
        with open(filepath, 'w') as f:
            json.dump(lock_data, f, indent=2)
    
    def read_lock_file(self, filepath: str) -> Dict[str, Any]:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def verify_lock_file(self, current_deps: Dict[str, Dependency], 
                        lock_data: Dict[str, Any]) -> List[str]:
        mismatches = []
        
        for name, dep in current_deps.items():
            if name in lock_data.get('packages', {}):
                locked_version = lock_data['packages'][name]['version']
                if locked_version != dep.version:
                    mismatches.append(f"{name}: {dep.version} -> {locked_version}")
        
        return mismatches


lock_manager = LockFileManager()
lock_data = lock_manager.generate_lock_file(manager.dependencies)

print("Generated lock file:")
print(json.dumps(lock_data, indent=2)[:500])


# ==============================================================================
# УПРАЖНЕНИЕ 4: Dependency Update Strategy
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Dependency Update Strategy")
print("=" * 60)


class UpdateStrategy:
    """Стратегия обновления зависимостей"""
    
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    SECURITY = "security"
    
    def __init__(self, strategy: str = self.MINOR):
        self.strategy = strategy
    
    def get_allowed_updates(self, current_version: str, latest_version: str) -> bool:
        current_parts = [int(x) for x in current_version.split('.')]
        latest_parts = [int(x) for x in latest_version.split('.')]
        
        if len(current_parts) < 3:
            return False
        
        if self.strategy == self.PATCH:
            return current_parts[0] == latest_parts[0] and current_parts[1] == latest_parts[1]
        
        elif self.strategy == self.MINOR:
            return current_parts[0] == latest_parts[0]
        
        elif self.strategy == self.MAJOR:
            return True
        
        elif self.strategy == self.SECURITY:
            return True
        
        return False
    
    def plan_updates(self, dependencies: Dict[str, Dependency]) -> List[Dict[str, str]]:
        updates = []
        
        for name, dep in dependencies.items():
            if dep.latest_version:
                if self.get_allowed_updates(dep.version, dep.latest_version):
                    updates.append({
                        'package': name,
                        'current': dep.version,
                        'new': dep.latest_version,
                        'type': self.strategy
                    })
        
        return updates


manager.add_dependency("flask", "2.0.0")
manager.dependencies["flask"].latest_version = "2.3.0"

strategy = UpdateStrategy(UpdateStrategy.MINOR)
updates = strategy.plan_updates(manager.dependencies)

print("Planned updates:")
for update in updates:
    print(f"  {update['package']}: {update['current']} -> {update['new']}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Virtual Environment
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Virtual Environment")
print("=" * 60)


class VirtualEnvironmentManager:
    """Управление виртуальными окружениями"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.venv_path = f".venv/{project_name}"
    
    def create_venv(self) -> str:
        return f"python -m venv {self.venv_path}"
    
    def activate_venv(self) -> str:
        return f"source {self.venv_path}/bin/activate"
    
    def install_requirements(self, requirements_file: str = "requirements.txt") -> str:
        return f"pip install -r {requirements_file}"
    
    def export_requirements(self) -> str:
        return f"pip freeze > requirements.txt"
    
    def get_setup_instructions(self) -> List[str]:
        return [
            self.create_venv(),
            self.activate_venv(),
            self.install_requirements(),
            "pip install -e ."
        ]


venv_manager = VirtualEnvironmentManager("myproject")

print("Virtual environment setup:")
for instruction in venv_manager.get_setup_instructions():
    print(f"  {instruction}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
