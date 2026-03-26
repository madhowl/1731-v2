# Практическое занятие 63: Безопасное развёртывание

## Безопасная конфигурация, secrets management, безопасная инфраструктура

### Цель занятия:
Изучить методы безопасного развёртывания, освоить управление secrets, научиться создавать безопасную инфраструктуру.

### Задачи:
1. Понять основы безопасного развёртывания
2. Освоить управление secrets
3. Научиться настраивать безопасную инфраструктуру

### План работы:
1. Принципы безопасного развёртывания
2. Управление secrets
3. Безопасная инфраструктура
4. Практические задания

---

## 1. Управление secrets

### Пример 1: Безопасная конфигурация

```python
import os
import json
from dataclasses import dataclass

class SecureConfig:
    """Безопасная конфигурация"""
    
    def __init__(self):
        self.secrets = {}
        self._load_secrets()
    
    def _load_secrets(self):
        """Загрузка secrets из переменных окружения"""
        required = ['DATABASE_URL', 'SECRET_KEY', 'API_KEY']
        
        for key in required:
            value = os.environ.get(key)
            if not value:
                raise ValueError(f"Missing required secret: {key}")
            self.secrets[key] = value
    
    def get(self, key: str, default=None):
        """Получение secret"""
        return self.secrets.get(key, default)

# Конфигурация для разных окружений
class ConfigFactory:
    """Фабрика конфигураций"""
    
    @staticmethod
    def get_config(env: str = None):
        env = env or os.environ.get('APP_ENV', 'development')
        
        if env == 'production':
            return ProductionConfig()
        elif env == 'staging':
            return StagingConfig()
        else:
            return DevelopmentConfig()

class ProductionConfig(SecureConfig):
    """Production конфигурация"""
    pass
```

### Пример 2: Vault integration

```python
import hvac

class VaultClient:
    """Клиент для HashiCorp Vault"""
    
    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)
    
    def get_secret(self, path: str) -> dict:
        """Получение secret из Vault"""
        result = self.client.secrets.kv.v2.read_secret_version(path=path)
        return result['data']['data']
    
    def set_secret(self, path: str, data: dict):
        """Сохранение secret в Vault"""
        self.client.secrets.kv.v2.create_or_update_secret(path=path, secret=data)

# Использование
# vault = VaultClient('http://vault:8200', 'token')
# secrets = vault.get_secret('secret/data/myapp')
```

---

## 2. Практические задания

### Задание 1: Конфигурация

Создайте безопасную систему конфигурации для разных окружений.

### Задание 2: Secrets management

Интегрируйте Vault для управления secrets.

### Задание 3: Docker secrets

Настройте безопасное хранение secrets в Docker.

---

## Контрольные вопросы:

1. Как безопасно хранить пароли и ключи?
2. Что такое Vault?
3. Как настроить безопасное развёртывание?
