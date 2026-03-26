# Практическое занятие 54: Мониторинг и логирование

## Системы мониторинга, сбор логов, метрики, алерты

### Цель занятия:
Изучить основы мониторинга и логирования, освоить инструменты для сбора метрик и логов, научиться настраивать алерты.

### Задачи:
1. Понять основные концепции мониторинга
2. Освоить инструменты сбора логов
3. Научиться собирать метрики
4. Настроить систему алертинга

### План работы:
1. Введение в мониторинг
2. Логирование
3. Сбор метрик
4. Системы мониторинга
5. Алертинг
6. Практические задания

---

## 1. Введение в мониторинг

Мониторинг - это процесс сбора, анализа и отображения информации о состоянии системы.

### Типы мониторинга:

1. **Инфраструктурный мониторинг** - состояние серверов, сетей, дисков
2. **Прикладной мониторинг** - производительность приложений
3. **Бизнес-метрики** - KPI,转化率, доход
4. **Безопасность** - обнаружение вторжений, аномалии

### Модель USE (Utilization, Saturation, Errors):

- **Utilization (использование)** - процент использования ресурса
- **Saturation (насыщенность)** - степень перегрузки
- **Errors (ошибки)** - количество ошибок

### Модель RED (Rate, Errors, Duration):

- **Rate** - количество запросов в секунду
- **Errors** - количество ошибок
- **Duration** - время обработки запросов

---

## 2. Логирование

### Пример 1: Структурированное логирование

```python
import logging
import json
from datetime import datetime
from typing import Any, Dict
import sys

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
        
        # Добавление исключения, если есть
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Добавление дополнительных полей
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)

def setup_logging(log_level: str = 'INFO'):
    """Настройка логирования"""
    
    # Настройка корневого логгера
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очистка существующих обработчиков
    logger.handlers.clear()
    
    # Консольный обработчик с JSON форматом
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    return logger

# Настройка логирования
logger = setup_logging('INFO')

# Примеры логирования
logger.info('Application started', extra={'extra': {'version': '1.0.0'}})
logger.info('User logged in', extra={'extra': {'user_id': '123', 'ip': '192.168.1.1'}})
logger.error('Request failed', extra={'extra': {'request_id': 'abc123', 'error': 'Timeout'}})
```

### Пример 2: Логирование с контекстом

```python
import logging
from contextvars import ContextVar
from typing import Optional
import uuid

# Контекстные переменные для трейсинга
request_id: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id: ContextVar[Optional[str]] = ContextVar('user_id', default=None)

class ContextFilter(logging.Filterer):
    """Фильтр для добавления контекста в логи"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        # Добавление контекстных переменных
        record.request_id = request_id.get()
        record.user_id = user_id.get()
        return True

def setup_request_logging(request_id_value: str, user_id_value: str = None):
    """Настройка контекста для логирования запроса"""
    request_id.set(request_id_value)
    if user_id_value:
        user_id.set(user_id_value)

# Настройка логирования с контекстным фильтром
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
)

logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

# Использование
def handle_request(request):
    req_id = str(uuid.uuid4())
    setup_request_logging(req_id, request.user_id)
    
    logger.info('Processing request')
    logger.info(f'User action: {request.action}')
    
    try:
        result = process_request(request)
        logger.info('Request completed successfully')
        return result
    except Exception as e:
        logger.error(f'Request failed: {str(e)}')
        raise

def process_request(request):
    # Логика обработки
    pass
```

### Пример 3: Интеграция с Python logging

```python
import logging
import logging.handlers
import sys

class LogAggregator:
    """Агрегатор логов с отправкой в централизованную систему"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.service_name)
        logger.setLevel(logging.INFO)
        
        # Обработчик для stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)
        
        # Формат
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        stdout_handler.setFormatter(formatter)
        
        logger.addHandler(stdout_handler)
        
        return logger
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra=kwargs)

# Использование
logger = LogAggregator('myapp')
logger.info('User action', user_id='123', action='login')
logger.error('Payment failed', order_id='456', error='Insufficient funds')
```

---

## 3. Сбор метрик

### Пример 4: Сбор метрик с Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response, request
import time
import random

app = Flask(__name__)

# Создание регистратора метрик
registry = CollectorRegistry()

# Счётчик запросов
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

# Гистограмма времени ответа
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=registry
)

#Gauge для активных соединений
active_connections = Gauge(
    'active_connections',
    'Number of active connections',
    registry=registry
)

#Gauge для использования памяти
memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes',
    ['type'],
    registry=registry
)

# Счётчик ошибок
error_counter = Counter(
    'application_errors_total',
    'Total number of errors',
    ['type', 'endpoint'],
    registry=registry
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Подсчёт запросов
    http_requests_total.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    # Время выполнения
    duration = time.time() - request.start_time
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown'
    ).observe(duration)
    
    return response

@app.route('/metrics')
def metrics():
    """Эндпоинт для сбора метрик Prometheus"""
    # Обновление метрик памяти
    import psutil
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_usage_bytes.labels(type='rss').set(memory_info.rss)
    memory_usage_bytes.labels(type='vms').set(memory_info.vms)
    
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/users')
def get_users():
    active_connections.inc()
    try:
        # Симуляция обработки
        time.sleep(random.uniform(0.01, 0.1))
        
        if random.random() < 0.05:
            error_counter.labels(type='database', endpoint='get_users').inc()
            raise Exception("Random error")
        
        return {'users': []}
    finally:
        active_connections.dec()

@app.route('/api/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Пример 5: Кастомные метрики для бизнеса

```python
from prometheus_client import Counter, Histogram, Gauge

# Метрики для e-commerce приложения
orders_placed = Counter(
    'orders_placed_total',
    'Total number of orders placed',
    ['currency', 'payment_method']
)

order_value = Histogram(
    'order_value_usd',
    'Value of orders in USD',
    ['currency'],
    buckets=[10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
)

users_registered = Counter(
    'users_registered_total',
    'Total number of registered users',
    ['source']
)

active_users = Gauge(
    'active_users',
    'Number of active users',
    ['timeframe']
)

cart_abandonment_rate = Gauge(
    'cart_abandonment_rate',
    'Percentage of abandoned carts',
    []
)

payment_failures = Counter(
    'payment_failures_total',
    'Total number of payment failures',
    ['payment_method', 'failure_reason']
)

# Пример использования метрик
def track_order(order):
    orders_placed.labels(
        currency=order.currency,
        payment_method=order.payment_method
    ).inc()
    
    order_value.labels(currency=order.currency).observe(order.total)

def track_user_registration(user):
    users_registered.labels(source=user.source).inc()

def track_cart_abandonment(abandoned_carts, total_carts):
    rate = (abandoned_carts / total_carts) * 100 if total_carts > 0 else 0
    cart_abandonment_rate.set(rate)
```

---

## 4. Системы мониторинга

### Пример 6: Настройка Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - "/etc/prometheus/rules/*.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'myapp'
    scrape_interval: 10s
    static_configs:
      - targets: ['app:5000']
    metrics_path: '/metrics'

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Пример 7: Настройка Grafana

```python
# grafana_dashboard.py - Пример создания дашборда через API
import requests
import json

GRAFANA_URL = "http://localhost:3000"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

dashboard = {
    "dashboard": {
        "title": "Application Overview",
        "tags": ["application", "overview"],
        "timezone": "browser",
        "panels": [
            {
                "id": 1,
                "title": "Requests per second",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(http_requests_total[5m])",
                        "legendFormat": "{{method}} - {{endpoint}}"
                    }
                ],
                "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
            },
            {
                "id": 2,
                "title": "Error rate",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(http_requests_total{status=~'5..'}[5m])",
                        "legendFormat": "5xx errors"
                    }
                ],
                "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
            },
            {
                "id": 3,
                "title": "Response time",
                "type": "graph",
                "targets": [
                    {
                        "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "p95"
                    },
                    {
                        "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "p99"
                    }
                ],
                "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8}
            },
            {
                "id": 4,
                "title": "Active connections",
                "type": "graph",
                "targets": [
                    {
                        "expr": "active_connections",
                        "legendFormat": "Active"
                    }
                ],
                "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8}
            }
        ],
        "refresh": "10s",
        "time": {
            "from": "now-1h",
            "to": "now"
        }
    },
    "overwrite": True
}

response = requests.post(
    f"{GRAFANA_URL}/api/dashboards/db",
    headers=headers,
    json=dashboard
)

print(f"Dashboard created: {response.json()}")
```

---

## 5. Алертинг

### Пример 8: Правила алертинга Prometheus

```yaml
# alerts.yml
groups:
  - name: application
    rules:
      # Высокий уровень ошибок
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.endpoint }}"

      # Высокое время отклика
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time"
          description: "p95 response time is {{ $value }}s for {{ $labels.endpoint }}"

      # Недоступность сервиса
      - alert: ServiceDown
        expr: up{job="myapp"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.job }} has been down for more than 1 minute"

      # Высокое использование памяти
      - alert: HighMemoryUsage
        expr: memory_usage_bytes / 1024 / 1024 / 1024 > 4
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is above 4GB"

      # Аномальное количество ошибок
      - alert: ErrorSpike
        expr: rate(application_errors_total[5m]) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Error spike detected"
          description: "Error rate is {{ $value }} per second"
```

---

## 6. Практические задания

### Задание 1: Настройка логирования

Создайте систему логирования для Flask приложения:
- Структурированный вывод в JSON формате
- Логирование контекста запроса (request_id, user_id)
- Ротация логов
- Отправка логов в централизованную систему

### Задание 2: Метрики Prometheus

Добавьте метрики в ваше приложение:
- Счётчик HTTP запросов
- Гистограмма времени отклика
- Кастомные бизнес-метрики
- Метрики использования ресурсов

### Задание 3: Grafana дашборд

Создайте дашборд в Grafana:
- Графики запросов и ошибок
- Время отклика (p50, p95, p99)
- Использование ресурсов
- Бизнес-метрики

### Задание 4: Настройка алертинга

Настройте систему алертинга:
- Оповещения о недоступности сервиса
- Оповещения о высоком уровне ошибок
- Оповещения о высоком времени отклика
- Интеграция с Telegram/Slack

### Задание 5: Distributed Tracing

Реализуйте распределённый трейсинг:
- Генерация trace_id для каждого запроса
- Отправка трейсов в Jaeger/Zipkin
- Анализ распределения времени по сервисам

---

## Контрольные вопросы:

1. Какие типы мониторинга вы знаете?
2. Что такое модель USE и RED?
3. Зачем нужно структурированное логирование?
4. Какие инструменты для сбора метрик вы знаете?
5. Как настроить эффективную систему алертинга?

---

## Дополнительные материалы:

- Prometheus Documentation: https://prometheus.io/docs/
- Grafana Documentation: https://grafana.com/docs/
- The Zen of Monitoring: https://landing.google.com/sre/sre-book/chapters/monitoring-distributed-systems/
