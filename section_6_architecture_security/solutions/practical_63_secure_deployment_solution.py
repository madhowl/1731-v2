#!/usr/bin/env python3
"""
Практическое занятие 63: Безопасное развёртывание
Решение упражнений
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Environment Configuration
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Environment Configuration")
print("=" * 60)


class EnvironmentConfig:
    """Управление конфигурацией окружения"""
    
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    
    def __init__(self, env: str = None):
        self.env = env or os.environ.get('APP_ENV', self.DEVELOPMENT)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        configs = {
            self.DEVELOPMENT: {
                'debug': True,
                'log_level': 'DEBUG',
                'database_url': 'sqlite:///dev.db',
                'secret_key': 'dev-secret-key-not-for-production',
                'allowed_hosts': ['localhost', '127.0.0.1'],
                'cors_enabled': True
            },
            self.STAGING: {
                'debug': False,
                'log_level': 'INFO',
                'database_url': 'postgresql://staging-db',
                'secret_key': os.environ.get('SECRET_KEY', 'staging-key'),
                'allowed_hosts': ['staging.example.com'],
                'cors_enabled': True
            },
            self.PRODUCTION: {
                'debug': False,
                'log_level': 'WARNING',
                'database_url': 'postgresql://prod-db',
                'secret_key': os.environ.get('SECRET_KEY', ''),
                'allowed_hosts': ['example.com', 'www.example.com'],
                'cors_enabled': False
            }
        }
        
        return configs.get(self.env, configs[self.DEVELOPMENT])
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)
    
    def is_production(self) -> bool:
        return self.env == self.PRODUCTION
    
    def is_development(self) -> bool:
        return self.env == self.DEVELOPMENT


dev_config = EnvironmentConfig(EnvironmentConfig.DEVELOPMENT)
prod_config = EnvironmentConfig(EnvironmentConfig.PRODUCTION)

print(f"Development - Debug: {dev_config.get('debug')}")
print(f"Production - Debug: {prod_config.get('debug')}")
print(f"Is Production: {prod_config.is_production()}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Security Headers Middleware
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Security Headers Middleware")
print("=" * 60)


class SecurityHeadersMiddleware:
    """Middleware для добавления заголовков безопасности"""
    
    def __init__(self, app):
        self.app = app
    
    def process_response(self, response) -> Dict[str, str]:
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
        
        return security_headers


class MockResponse:
    def __init__(self):
        self.headers = {}


middleware = SecurityHeadersMiddleware(app=None)
response = MockResponse()
headers = middleware.process_response(response)

print("Security Headers:")
for header, value in headers.items():
    print(f"  {header}: {value}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Deployment Checklist
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Deployment Checklist")
print("=" * 60)


@dataclass
class ChecklistItem:
    name: str
    category: str
    passed: bool = False
    notes: str = ""


class DeploymentChecklist:
    """Чеклист для безопасного развёртывания"""
    
    def __init__(self):
        self.items: List[ChecklistItem] = self._create_checklist()
    
    def _create_checklist(self) -> List[ChecklistItem]:
        return [
            ChecklistItem("Enable HTTPS/TLS", "Network Security"),
            ChecklistItem("Configure security headers", "Application Security"),
            ChecklistItem("Set secure session cookies", "Application Security"),
            ChecklistItem("Disable debug mode", "Configuration"),
            ChecklistItem("Use strong authentication", "Access Control"),
            ChecklistItem("Implement rate limiting", "Network Security"),
            ChecklistItem("Configure logging and monitoring", "Operations"),
            ChecklistItem("Backup database", "Data Protection"),
            ChecklistItem("Set proper file permissions", "System Security"),
            ChecklistItem("Update all dependencies", "Software Updates")
        ]
    
    def mark_complete(self, item_name: str, notes: str = "") -> bool:
        for item in self.items:
            if item.name == item_name:
                item.passed = True
                item.notes = notes
                return True
        return False
    
    def get_summary(self) -> Dict[str, Any]:
        total = len(self.items)
        passed = sum(1 for item in self.items if item.passed)
        
        by_category = {}
        for item in self.items:
            if item.category not in by_category:
                by_category[item.category] = {'total': 0, 'passed': 0}
            by_category[item.category]['total'] += 1
            if item.passed:
                by_category[item.category]['passed'] += 1
        
        return {
            'total': total,
            'passed': passed,
            'remaining': total - passed,
            'by_category': by_category
        }


checklist = DeploymentChecklist()
checklist.mark_complete("Enable HTTPS/TLS", "SSL certificates installed")
checklist.mark_complete("Disable debug mode", "Set DEBUG=False")

summary = checklist.get_summary()
print(f"Checklist: {summary['passed']}/{summary['total']} completed")
print("By category:")
for category, stats in summary['by_category'].items():
    print(f"  {category}: {stats['passed']}/{stats['total']}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Server Hardening
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Server Hardening")
print("=" * 60)


class ServerHardening:
    """Рекомендации по защите сервера"""
    
    @staticmethod
    def get_firewall_rules() -> List[Dict[str, str]]:
        return [
            {'port': '22', 'protocol': 'tcp', 'source': '10.0.0.0/8', 'action': 'allow', 'comment': 'SSH from internal network'},
            {'port': '80', 'protocol': 'tcp', 'source': '0.0.0.0/0', 'action': 'allow', 'comment': 'HTTP'},
            {'port': '443', 'protocol': 'tcp', 'source': '0.0.0.0/0', 'action': 'allow', 'comment': 'HTTPS'},
            {'port': '5432', 'protocol': 'tcp', 'source': '10.0.0.0/8', 'action': 'allow', 'comment': 'PostgreSQL from internal'},
            {'port': 'all', 'protocol': 'all', 'source': '0.0.0.0/0', 'action': 'deny', 'comment': 'Default deny'}
        ]
    
    @staticmethod
    def get_system_configs() -> Dict[str, Any]:
        return {
            'ssh': {
                'permit_root_login': 'no',
                'password_authentication': 'no',
                'pubkey_authentication': 'yes',
                'max_auth_tries': 3
            },
            'firewall': {
                'enabled': True,
                'default_policy': 'deny',
                'allowed_services': ['ssh', 'http', 'https']
            },
            'updates': {
                'automatic_updates': True,
                'update_frequency': 'daily'
            }
        }


hardening = ServerHardening()

print("Firewall Rules:")
for rule in ServerHardening.get_firewall_rules():
    print(f"  {rule['port']}/{rule['protocol']}: {rule['action']} from {rule['source']}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Deployment Script
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Deployment Script")
print("=" * 60)


class DeploymentScript:
    """Скрипт развёртывания"""
    
    def __init__(self, app_name: str, version: str):
        self.app_name = app_name
        self.version = version
        self.steps: List[Dict[str, Any]] = []
    
    def add_step(self, name: str, command: str, rollback: str = None):
        self.steps.append({
            'name': name,
            'command': command,
            'rollback': rollback,
            'status': 'pending'
        })
    
    def run(self) -> bool:
        for step in self.steps:
            step['status'] = 'running'
            print(f"Running: {step['name']}")
            
            step['status'] = 'completed'
            print(f"  Command: {step['command']}")
        
        return True
    
    def rollback(self):
        for step in reversed(self.steps):
            if step['status'] == 'completed' and step.get('rollback'):
                print(f"Rolling back: {step['name']}")
                print(f"  Rollback: {step['rollback']}")


script = DeploymentScript("myapp", "1.0.0")
script.add_step("Backup database", "pg_dump myapp > backup.sql", "rm backup.sql")
script.add_step("Pull latest code", "git pull origin main")
script.add_step("Run migrations", "python manage.py migrate")
script.add_step("Restart service", "systemctl restart myapp", "systemctl restart myapp")

script.run()


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
