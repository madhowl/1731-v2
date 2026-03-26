#!/usr/bin/env python3
"""
Практическое занятие 54: Мониторинг и логирование
Решение упражнений
"""

import logging
import json
import time
from datetime import datetime
from typing import Any, Dict, Optional
import sys


# ==============================================================================
# УПРАЖНЕНИЕ 1: Структурированное логирование
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Структурированное логирование")
print("=" * 60)


class JSONFormatter(logging.Formatter):
    """Форматтер для вывода логов в формате JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """Настройка логирования"""
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    return logger


# Тестирование
logger = setup_logging('INFO')

logger.info('Application started')
logger.info('User logged in', extra={'extra': {'user_id': '123', 'ip': '192.168.1.1'}})
logger.error('Request failed', extra={'extra': {'request_id': 'abc123', 'error': 'Timeout'}})


# ==============================================================================
# УПРАЖНЕНИЕ 2: Логирование с контекстом
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Логирование с контекстом")
print("=" * 60)


from contextvars import ContextVar


# Контекстные переменные для трейсинга
request_id: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


class ContextFilter(logging.Filterer):
    """Фильтр для добавления контекста в логи"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        record.user_id = user_id.get()
        return True


def setup_request_logging(request_id_value: str, user_id_value: Optional[str] = None):
    """Настройка контекста для логирования запроса"""
    request_id.set(request_id_value)
    if user_id_value:
        user_id.set(user_id_value)


# Тестирование контекстного логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
)

context_logger = logging.getLogger(__name__)
context_logger.addFilter(ContextFilter())

# Симуляция запроса
setup_request_logging('req-123', 'user-456')
context_logger.info('Processing user request')
context_logger.info('User action: login')


# ==============================================================================
# УПРАЖНЕНИЕ 3: Сбор метрик
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Сбор метрик")
print("=" * 60)


class MetricsCollector:
    """Сборщик метрик"""
    
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, list] = {}
    
    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Увеличение счётчика"""
        key = self._make_key(name, labels)
        self._counters[key] = self._counters.get(key, 0) + 1
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Установка значения gauge"""
        key = self._make_key(name, labels)
        self._gauges[key] = value
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Добавление значения в гистограмму"""
        key = self._make_key(name, labels)
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)
    
    def _make_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        if labels:
            label_str = ','.join(f'{k}={v}' for k, v in sorted(labels.items()))
            return f'{name}{{{label_str}}}'
        return name
    
    def get_metrics(self) -> str:
        """Получение метрик в формате Prometheus"""
        lines = []
        
        for name, value in self._counters.items():
            lines.append(f'# TYPE {name} counter')
            lines.append(f'{name} {value}')
        
        for name, value in self._gauges.items():
            lines.append(f'# TYPE {name} gauge')
            lines.append(f'{name} {value}')
        
        for name, values in self._histograms.items():
            lines.append(f'# TYPE {name} histogram')
            avg = sum(values) / len(values) if values else 0
            lines.append(f'{name}_sum {sum(values)}')
            lines.append(f'{name}_count {len(values)}')
        
        return '\n'.join(lines)


# Тестирование
metrics = MetricsCollector()

# Симуляция HTTP запросов
for i in range(100):
    metrics.increment_counter('http_requests_total', {'method': 'GET', 'endpoint': '/api/users', 'status': '200'})

metrics.set_gauge('active_connections', 42)
metrics.set_gauge('memory_usage_bytes', 1024 * 1024 * 256)

for i in range(100):
    metrics.observe_histogram('http_request_duration_seconds', 0.05 + (i % 10) * 0.01)

print("Собранные метрики:")
print(metrics.get_metrics())


# ==============================================================================
# УПРАЖНЕНИЕ 4: Система мониторинга
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Система мониторинга")
print("=" * 60)


class HealthChecker:
    """Проверка здоровья сервисов"""
    
    def __init__(self):
        self.services: Dict[str, Dict[str, Any]] = {}
    
    def register_service(self, name: str, check_func):
        """Регистрация сервиса для проверки"""
        self.services[name] = {
            'check_func': check_func,
            'status': 'unknown',
            'last_check': None
        }
    
    def check_service(self, name: str) -> Dict[str, Any]:
        """Проверка конкретного сервиса"""
        if name not in self.services:
            return {'error': 'Service not found'}
        
        service = self.services[name]
        
        try:
            result = service['check_func']()
            service['status'] = 'healthy' if result else 'unhealthy'
            service['last_check'] = datetime.now().isoformat()
            return {'status': service['status'], 'last_check': service['last_check']}
        except Exception as e:
            service['status'] = 'unhealthy'
            service['last_check'] = datetime.now().isoformat()
            return {'status': 'unhealthy', 'error': str(e), 'last_check': service['last_check']}
    
    def check_all(self) -> Dict[str, Any]:
        """Проверка всех сервисов"""
        results = {}
        for name in self.services:
            results[name] = self.check_service(name)
        return results


# Пример использования
health_checker = HealthChecker()

health_checker.register_service('database', lambda: True)
health_checker.register_service('cache', lambda: True)
health_checker.register_service('api', lambda: True)

print("Проверка здоровья сервисов:")
results = health_checker.check_all()
for service, status in results.items():
    print(f"  {service}: {status['status']}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Alerting
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Система алертинга")
print("=" * 60)


class AlertManager:
    """Менеджер алертов"""
    
    def __init__(self):
        self.alerts: list = []
        self.rules: list = []
    
    def add_rule(self, name: str, condition_func, severity: str = 'warning'):
        """Добавление правила для алерта"""
        self.rules.append({
            'name': name,
            'condition': condition_func,
            'severity': severity
        })
    
    def check_and_alert(self, metrics: MetricsCollector):
        """Проверка условий и создание алертов"""
        new_alerts = []
        
        for rule in self.rules:
            try:
                if rule['condition'](metrics):
                    alert = {
                        'name': rule['name'],
                        'severity': rule['severity'],
                        'timestamp': datetime.now().isoformat(),
                        'message': f"Alert triggered: {rule['name']}"
                    }
                    new_alerts.append(alert)
                    print(f"ALERT [{rule['severity'].upper()}]: {rule['name']}")
            except Exception as e:
                print(f"Error checking rule {rule['name']}: {e}")
        
        self.alerts.extend(new_alerts)
        return new_alerts
    
    def get_active_alerts(self) -> list:
        """Получение активных алертов"""
        return [a for a in self.alerts if a.get('status') != 'resolved']
    
    def resolve_alert(self, alert_name: str):
        """Разрешение алерта"""
        for alert in self.alerts:
            if alert['name'] == alert_name and alert.get('status') != 'resolved':
                alert['status'] = 'resolved'
                alert['resolved_at'] = datetime.now().isoformat()


# Настройка алертов
alert_manager = AlertManager()

# Добавление правил
alert_manager.add_rule('high_error_rate', lambda m: m._counters.get('http_requests_total{status="500"}', 0) > 10, 'critical')
alert_manager.add_rule('high_latency', lambda m: sum(m._histograms.get('http_request_duration_seconds', [0])) / max(len(m._histograms.get('http_request_duration_seconds', [1])), 1) > 1.0, 'warning')
alert_manager.add_rule('high_memory', lambda m: m._gauges.get('memory_usage_bytes', 0) > 1024 * 1024 * 512, 'warning')

# Проверка
alert_manager.check_and_alert(metrics)


# ==============================================================================
# УПРАЖНЕНИЕ 6: Dashboard данные
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 6: Dashboard данные")
print("=" * 60)


class Dashboard:
    """Генератор данных для dashboard"""
    
    def __init__(self, metrics: MetricsCollector, health_checker: HealthChecker):
        self.metrics = metrics
        self.health_checker = health_checker
    
    def get_overview(self) -> Dict[str, Any]:
        """Получение обзорных данных"""
        return {
            'timestamp': datetime.now().isoformat(),
            'health': self.health_checker.check_all(),
            'metrics': {
                'requests_total': sum(v for k, v in self.metrics._counters.items() if 'http_requests' in k),
                'active_connections': self.metrics._gauges.get('active_connections', 0),
                'memory_usage_mb': self.metrics._gauges.get('memory_usage_bytes', 0) / (1024 * 1024)
            },
            'alerts': alert_manager.get_active_alerts()
        }


dashboard = Dashboard(metrics, health_checker)
overview = dashboard.get_overview()

print("Dashboard данные:")
print(f"  Запросов всего: {overview['metrics']['requests_total']}")
print(f"  Активных соединений: {overview['metrics']['active_connections']}")
print(f"  Использование памяти (MB): {overview['metrics']['memory_usage_mb']:.2f}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
