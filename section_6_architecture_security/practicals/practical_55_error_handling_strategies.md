# Практическое занятие 55: Стратегии обработки ошибок

## Обработка исключений, retry логика, circuit breaker, fallback стратегии

### Цель занятия:
Изучить основные стратегии обработки ошибок в приложениях, освоить паттерны обработки исключений, научиться создавать устойчивые к ошибкам системы.

### Задачи:
1. Понять принципы обработки ошибок
2. Освоить паттерны retry и circuit breaker
3. Научиться создавать fallback стратегии
4. Реализовать централизованную обработку ошибок

### План работы:
1. Основы обработки ошибок
2. Иерархия исключений
3. Retry логика
4. Circuit Breaker паттерн
5. Fallback стратегии
6. Централизованная обработка ошибок
7. Практические задания

---

## 1. Основы обработки ошибок

Обработка ошибок - это критически важная часть любого приложения. Правильная обработка ошибок обеспечивает надёжность и удобство использования.

### Принципы обработки ошибок:

1. **Предсказуемость** - ошибки должны быть предсказуемыми и понятными
2. **Информативность** - сообщения об ошибках должны быть информативными
3. **Изоляция** - ошибки в одном компоненте не должны влиять на другие
4. **Логирование** - все ошибки должны логироваться
5. **Восстановление** - система должна иметь возможность восстановиться после ошибок

### Пример 1: Базовая структура исключений

```python
from typing import Optional, Any, Dict
from dataclasses import dataclass
from datetime import datetime
import traceback
import uuid

# Базовый класс для всех исключений приложения
class AppException(Exception):
    """Базовый класс исключений приложения"""
    
    def __init__(self, message: str, code: str = None, details: Dict = None):
        super().__init__(message)
        self.message = message
        self.code = code or 'INTERNAL_ERROR'
        self.details = details or {}
        self.timestamp = datetime.utcnow()
        self.exception_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': {
                'message': self.message,
                'code': self.code,
                'details': self.details,
                'timestamp': self.timestamp.isoformat(),
                'exception_id': self.exception_id
            }
        }

# Исключения для бизнес-логики
class ValidationError(AppException):
    def __init__(self, message: str, field: str = None, details: Dict = None):
        super().__init__(message, 'VALIDATION_ERROR', details)
        self.field = field

class NotFoundError(AppException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f'{resource} with id {resource_id} not found',
            code='NOT_FOUND',
            details={'resource': resource, 'resource_id': resource_id}
        )

class ConflictError(AppException):
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, 'CONFLICT', details)

class UnauthorizedError(AppException):
    def __init__(self, message: str = 'Authentication required'):
        super().__init__(message, 'UNAUTHORIZED')

class ForbiddenError(AppException):
    def __init__(self, message: str = 'Access denied'):
        super().__init__(message, 'FORBIDDEN')

# Исключения для внешних сервисов
class ExternalServiceError(AppException):
    def __init__(self, service: str, original_error: Exception):
        super().__init__(
            message=f'External service {service} is unavailable',
            code='EXTERNAL_SERVICE_ERROR',
            details={'service': service, 'original_error': str(original_error)}
        )

class DatabaseError(AppException):
    def __init__(self, message: str, operation: str = None):
        super().__init__(
            message=f'Database error: {message}',
            code='DATABASE_ERROR',
            details={'operation': operation}
        )
```

---

## 2. Retry логика

### Пример 2: Универсальный декоратор для повторных попыток

```python
import time
import random
import functools
from typing import Callable, Type, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True
):
    """
    Декоратор для повторного выполнения функции при ошибке
    
    Args:
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками (сек)
        backoff: Множитель для увеличения задержки
        exceptions: Кортеж исключений для перехвата
        jitter: Добавить случайный джиттер к задержке
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    
                    # Добавить jitter если включено
                    actual_delay = current_delay
                    if jitter:
                        actual_delay = current_delay * (0.5 + random.random() * 0.5)
                    
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {actual_delay:.2f}s..."
                    )
                    
                    time.sleep(actual_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator

# Пример использования
class ExternalAPI:
    @retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
    def fetch_data(self, endpoint: str) -> dict:
        """Вызов внешнего API с retry логикой"""
        # Симуляция нестабильного API
        if random.random() < 0.7:
            raise ConnectionError("Connection failed")
        return {"data": "success"}

# Использование
api = ExternalAPI()
try:
    result = api.fetch_data("/api/data")
    print(f"Result: {result}")
except ConnectionError as e:
    print(f"Failed after retries: {e}")
```

### Пример 3: Продвинутая retry логика с условиями

```python
import asyncio
from typing import Callable, Any, Optional
from dataclasses import dataclass

@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0
    jitter: bool = True
    
    def get_delay(self, attempt: int) -> float:
        delay = min(self.initial_delay * (self.backoff_factor ** (attempt - 1)), self.max_delay)
        if self.jitter:
            import random
            delay = delay * (0.5 + random.random() * 0.5)
        return delay

class RetryHandler:
    """Обработчик retry логики с гибкой конфигурацией"""
    
    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        should_retry: Optional[Callable[[Exception], bool]] = None,
        **kwargs
    ) -> Any:
        """Выполнение функции с retry логикой"""
        
        last_exception = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            
            except Exception as e:
                last_exception = e
                
                # Проверка условия retry
                if should_retry and not should_retry(e):
                    raise
                
                # Определение является ли ошибка временной
                if self._is_retryable_error(e):
                    if attempt < self.config.max_attempts:
                        delay = self.config.get_delay(attempt)
                        print(f"Attempt {attempt} failed, retrying in {delay:.2f}s...")
                        await asyncio.sleep(delay)
                    else:
                        print(f"All {self.config.max_attempts} attempts failed")
                        raise
                else:
                    # Нере retryable ошибка - сразу поднимаем
                    raise
        
        raise last_exception
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """Определение типа ошибки"""
        retryable_errors = (
            ConnectionError,
            TimeoutError,
            asyncio.TimeoutError,
        )
        
        # Добавить специфичные для приложения ошибки
        return isinstance(error, retryable_errors)

# Пример использования с asyncio
async def fetch_user_data(user_id: int) -> dict:
    """Асинхронная функция получения данных пользователя"""
    import random
    if random.random() < 0.5:
        raise ConnectionError("Connection timeout")
    return {"id": user_id, "name": "John"}

async def main():
    handler = RetryHandler(RetryConfig(max_attempts=3, initial_delay=0.5))
    
    # Вызов с условием retry
    should_retry = lambda e: isinstance(e, ConnectionError)
    result = await handler.execute_with_retry(
        fetch_user_data, 
        123,
        should_retry=should_retry
    )
    print(f"Result: {result}")

asyncio.run(main())
```

---

## 3. Circuit Breaker паттерн

### Пример 4: Реализация Circuit Breaker

```python
import time
import threading
from enum import Enum
from typing import Callable, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Нормальная работа
    OPEN = "open"          # Сервис недоступен
    HALF_OPEN = "half_open"  # Проверка восстановления

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # Количество ошибок для открытия
    success_threshold: int = 2       # Успешных запросов для закрытия
    timeout: float = 30.0            # Время ожидания перед переходом в HALF_OPEN
    excluded_exceptions: tuple = ()   # Исключения не влияющие на счётчик

class CircuitBreaker:
    """Реализация паттерна Circuit Breaker"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self._lock = threading.RLock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Вызов функции с защитой circuit breaker"""
        
        with self._lock:
            # Проверка состояния
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker {self.name} is OPEN"
                    )
            
            # Выполнение функции
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            
            except Exception as e:
                # Проверка исключения
                if isinstance(e, self.config.excluded_exceptions):
                    raise
                
                self._on_failure()
                raise
    
    def _should_attempt_reset(self) -> bool:
        """Проверка времени для перехода в HALF_OPEN"""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.config.timeout
    
    def _on_success(self):
        """Обработка успешного вызова"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                logger.info(f"Circuit breaker {self.name} CLOSED")
        
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
    
    def _on_failure(self):
        """Обработка неудачного вызова"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
            logger.warning(f"Circuit breaker {self.name} OPENED after HALF_OPEN failure")
        
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker {self.name} OPENED after {self.failure_count} failures"
            )

class CircuitBreakerOpenError(Exception):
    """Исключение при открытом circuit breaker"""
    pass

# Пример использования
def unstable_service_call(data: str) -> str:
    """Симуляция нестабильного сервиса"""
    import random
    if random.random() < 0.6:
        raise ConnectionError("Service unavailable")
    return f"Success: {data}"

# Создание circuit breaker
config = CircuitBreakerConfig(
    failure_threshold=3,
    success_threshold=2,
    timeout=10
)
breaker = CircuitBreaker("user-service", config)

# Вызов функции
for i in range(10):
    try:
        result = breaker.call(unstable_service_call, f"request_{i}")
        print(f"Request {i}: {result}")
    except CircuitBreakerOpenError:
        print(f"Request {i}: Circuit breaker is OPEN, skipping...")
        time.sleep(1)
    except ConnectionError as e:
        print(f"Request {i}: Failed - {e}")
```

---

## 4. Fallback стратегии

### Пример 5: Fallback с кэшированием

```python
from typing import Callable, Any, Optional
from functools import wraps
import time
import json
import logging

logger = logging.getLogger(__name__)

class Cache:
    """Простой in-memory кэш с TTL"""
    
    def __init__(self, ttl: int = 300):
        self._cache = {}
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        self._cache[key] = (value, time.time())
    
    def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]

class FallbackHandler:
    """Обработчик fallback стратегий"""
    
    def __init__(self):
        self.cache = Cache(ttl=300)
    
    def with_fallback(
        self,
        fallback_func: Callable = None,
        cache_key: str = None,
        cache_ttl: int = 300
    ):
        """Декоратор для добавления fallback логики"""
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Пробуем основную функцию
                try:
                    result = func(*args, **kwargs)
                    
                    # Кэшируем результат
                    if cache_key:
                        key = cache_key.format(*args, **kwargs)
                        self.cache.set(key, result)
                    
                    return result
                
                except Exception as e:
                    logger.warning(f"Primary function failed: {e}")
                    
                    # Пробуем получить из кэша
                    if cache_key:
                        key = cache_key.format(*args, **kwargs)
                        cached = self.cache.get(key)
                        if cached is not None:
                            logger.info(f"Returning cached result for {key}")
                            return {
                                'data': cached,
                                'from_cache': True,
                                'original_error': str(e)
                            }
                    
                    # Пробуем fallback функцию
                    if fallback_func:
                        logger.info("Attempting fallback function")
                        return fallback_func(*args, **kwargs)
                    
                    raise
            
            return wrapper
        return decorator

# Пример использования
fallback_handler = FallbackHandler()

@fallback_handler.with_fallback(
    fallback_func=lambda user_id: {
        'id': user_id,
        'name': 'Unknown User',
        'source': 'fallback'
    },
    cache_key='user_{}',
    cache_ttl=600
)
def fetch_user_from_api(user_id: int) -> dict:
    """Основная функция получения пользователя"""
    import random
    if random.random() < 0.5:
        raise ConnectionError("API unavailable")
    return {
        'id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com'
    }

# Тестирование
for i in range(5):
    result = fetch_user_from_api(i)
    print(f"User {i}: {result}")
```

---

## 5. Централизованная обработка ошибок

### Пример 6: Обработчик ошибок для Flask

```python
from flask import Flask, jsonify, request
from functools import wraps
import logging
import traceback

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Реестр исключений
exception_handlers = {}

def register_exception_handler(exception_class, handler):
    """Регистрация обработчика для конкретного исключения"""
    exception_handlers[exception_class] = handler

# Обработчики для различных исключений
def handle_validation_error(error):
    return jsonify({
        'error': {
            'message': error.message,
            'code': error.code,
            'field': error.field,
            'details': error.details
        }
    }), 400

def handle_not_found_error(error):
    return jsonify({
        'error': {
            'message': error.message,
            'code': error.code,
            'details': error.details
        }
    }), 404

def handle_app_exception(error):
    return jsonify({
        'error': {
            'message': error.message,
            'code': error.code,
            'exception_id': error.exception_id,
            'details': error.details
        }
    }), 500

def handle_generic_exception(error):
    """Обработчик для необработанных исключений"""
    exception_id = str(uuid.uuid4())
    
    logger.error(
        f"Unhandled exception {exception_id}: {traceback.format_exc()}"
    )
    
    return jsonify({
        'error': {
            'message': "Internal server error",
            'code': 'INTERNAL_ERROR',
            'exception_id': exception_id
        }
    }), 500

# Регистрация обработчиков
register_exception_handler(ValidationError, handle_validation_error)
register_exception_handler(NotFoundError, handle_not_found_error)
register_exception_handler(AppException, handle_app_exception)

@app.errorhandler(Exception)
def handle_exception(error):
    """Централизованный обработчик ошибок"""
    
    # Поиск наиболее специфичного обработчика
    for exc_type in type(error).__mro__:
        if exc_type in exception_handlers:
            return exception_handlers[exc_type](error)
    
    # Использование generic обработчика
    return handle_generic_exception(error)

# Примеры использования
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    if user_id < 0:
        raise ValidationError("User ID must be positive", field="user_id")
    
    if user_id > 1000:
        raise NotFoundError("User", str(user_id))
    
    return jsonify({'id': user_id, 'name': 'John'})

@app.route('/api/error')
def trigger_error():
    raise AppException("Something went wrong")
```

---

## 6. Практические задания

### Задание 1: Иерархия исключений

Создайте иерархию исключений для приложения электронной коммерции:
- Базовые исключения
- Исключения для заказов, платежей, пользователей
- Обработчики для каждого типа

### Задание 2: Retry логика

Реализуйте retry логику для вызова внешнего API:
- Настраиваемое количество попыток
- Экспоненциальный backoff
- Jitter для предотвращения thundering herd
- Логирование попыток

### Задание 3: Circuit Breaker

Создайте реализацию Circuit Breaker:
- Состояния: Closed, Open, Half-Open
- Настраиваемые пороги
- Мониторинг состояния
- Thread-safe реализация

### Задание 4: Fallback стратегии

Реализуйте систему fallback для внешних сервисов:
- Кэширование последних успешных ответов
- Fallback на резервный сервис
- Fallback на статические данные

### Задание 5: Централизованная обработка

Создайте систему централизованной обработки ошибок:
- Единый формат ошибок
- Логирование с контекстом
- Graceful degradation
- Мониторинг ошибок

---

## Контрольные вопросы:

1. В чём преимущества использования иерархии исключений?
2. Что такое circuit breaker и зачем он нужен?
3. Как правильно настроить retry логику?
4. Какие стратегии fallback вы знаете?
5. Почему важна централизованная обработка ошибок?

---

## Дополнительные материалы:

- "Release It!" - Michael Nygard
- "The Art of Error Handling" - https://blog.pragmaticengineer.com/
- Resilience Patterns: https://resilience4j.readme.io/
