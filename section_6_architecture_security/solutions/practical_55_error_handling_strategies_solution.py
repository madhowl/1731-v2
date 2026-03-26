#!/usr/bin/env python3
"""
Практическое занятие 55: Стратегии обработки ошибок
Решение упражнений
"""

import time
import random
import functools
from typing import Callable, Type, Tuple, Optional, Any, Dict
from dataclasses import dataclass
import logging
from enum import Enum


logger = logging.getLogger(__name__)


# ==============================================================================
# УПРАЖНЕНИЕ 1: Иерархия исключений
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Иерархия исключений")
print("=" * 60)


class AppException(Exception):
    """Базовый класс исключений приложения"""
    
    def __init__(self, message: str, code: str = None, details: Dict = None):
        super().__init__(message)
        self.message = message
        self.code = code or 'INTERNAL_ERROR'
        self.details = details or {}
        from datetime import datetime
        self.timestamp = datetime.now()
        import uuid
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


# Тестирование
print("Тестирование исключений:")
try:
    raise NotFoundError('User', '123')
except AppException as e:
    print(f"  {e.to_dict()}")

try:
    raise ValidationError('Email is required', 'email')
except AppException as e:
    print(f"  {e.to_dict()}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Retry логика
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Retry логика")
print("=" * 60)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True
):
    """Декоратор для повторного выполнения функции"""
    
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
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    
                    actual_delay = current_delay
                    if jitter:
                        actual_delay = current_delay * (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}. Retrying in {actual_delay:.2f}s...")
                    
                    time.sleep(actual_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


class ExternalAPI:
    @retry(max_attempts=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
    def fetch_data(self, endpoint: str) -> dict:
        """Вызов внешнего API с retry логикой"""
        if random.random() < 0.7:
            raise ConnectionError("Connection failed")
        return {"data": "success", "endpoint": endpoint}


api = ExternalAPI()
try:
    result = api.fetch_data("/api/data")
    print(f"  Result: {result}")
except ConnectionError as e:
    print(f"  Failed after retries: {e}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Circuit Breaker паттерн
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Circuit Breaker паттерн")
print("=" * 60)


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: float = 30.0
    excluded_exceptions: Tuple = ()


class CircuitBreakerOpenError(Exception):
    pass


class CircuitBreaker:
    """Реализация паттерна Circuit Breaker"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        import threading
        self._lock = threading.RLock()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                else:
                    raise CircuitBreakerOpenError(f"Circuit breaker {self.name} is OPEN")
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            
            except Exception as e:
                if isinstance(e, self.config.excluded_exceptions):
                    raise
                self._on_failure()
                raise
    
    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.config.timeout
    
    def _on_success(self):
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
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
            logger.warning(f"Circuit breaker {self.name} OPENED after HALF_OPEN failure")
        
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker {self.name} OPENED after {self.failure_count} failures")


def unstable_service_call(data: str) -> str:
    if random.random() < 0.6:
        raise ConnectionError("Service unavailable")
    return f"Success: {data}"


config = CircuitBreakerConfig(failure_threshold=3, success_threshold=2, timeout=5)
breaker = CircuitBreaker("user-service", config)

print("Тестирование Circuit Breaker:")
for i in range(10):
    try:
        result = breaker.call(unstable_service_call, f"request_{i}")
        print(f"  Request {i}: {result}")
    except CircuitBreakerOpenError:
        print(f"  Request {i}: Circuit breaker is OPEN, skipping...")
        time.sleep(0.5)
    except ConnectionError as e:
        print(f"  Request {i}: Failed - {e}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Fallback стратегии
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Fallback стратегии")
print("=" * 60)


class Cache:
    """Простой in-memory кэш с TTL"""
    
    def __init__(self, ttl: int = 300):
        self._cache: Dict = {}
        self._ttl = ttl
    
    def get(self, key: str):
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
    
    def with_fallback(self, fallback_func: Callable = None, cache_key: str = None):
        """Декоратор для добавления fallback логики"""
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Пробуем основную функцию
                try:
                    result = func(*args, **kwargs)
                    
                    if cache_key:
                        key = cache_key.format(*args, **kwargs)
                        self.cache.set(key, result)
                    
                    return result
                
                except Exception as e:
                    # Пробуем fallback
                    if fallback_func:
                        if cache_key:
                            cached = self.cache.get(cache_key.format(*args, **kwargs))
                            if cached:
                                logger.info(f"Using cached result for {func.__name__}")
                                return cached
                        
                        logger.warning(f"Falling back for {func.__name__}")
                        return fallback_func(*args, **kwargs)
                    
                    raise
        
        return decorator
    
    def with_default_value(self, default_value: Any):
        """Fallback с значением по умолчанию"""
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Error in {func.__name__}: {e}, returning default")
                    return default_value
        
        return decorator


fallback_handler = FallbackHandler()


@fallback_handler.with_fallback(fallback_func=lambda: {"data": "cached"}, cache_key="user_{}")
def fetch_user_data(user_id: str) -> dict:
    if random.random() < 0.3:
        raise ConnectionError("Service unavailable")
    return {"id": user_id, "name": f"User {user_id}"}


print("Тестирование Fallback:")
for i in range(5):
    try:
        result = fetch_user_data(str(i))
        print(f"  User {i}: {result}")
    except Exception as e:
        print(f"  User {i}: Error - {e}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Централизованная обработка ошибок
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Централизованная обработка ошибок")
print("=" * 60)


class ErrorHandler:
    """Централизованный обработчик ошибок"""
    
    def __init__(self):
        self.handlers: Dict[Type[Exception], Callable] = {}
    
    def register_handler(self, exception_type: Type[Exception], handler: Callable):
        self.handlers[exception_type] = handler
    
    def handle(self, error: Exception) -> Dict[str, Any]:
        error_type = type(error)
        
        for exc_type, handler in self.handlers.items():
            if isinstance(error, exc_type):
                return handler(error)
        
        # Default handler
        return {
            'status_code': 500,
            'error': {
                'message': str(error),
                'type': error_type.__name__
            }
        }


error_handler = ErrorHandler()

error_handler.register_handler(NotFoundError, lambda e: {
    'status_code': 404,
    'error': e.to_dict()['error']
})

error_handler.register_handler(ValidationError, lambda e: {
    'status_code': 422,
    'error': e.to_dict()['error']
})

error_handler.register_handler(ExternalServiceError, lambda e: {
    'status_code': 503,
    'error': e.to_dict()['error']
})

# Тестирование
errors = [
    NotFoundError('User', '123'),
    ValidationError('Invalid email', 'email'),
    ExternalServiceError('payment-gateway', Exception('timeout'))
]

print("Тестирование централизованной обработки:")
for error in errors:
    result = error_handler.handle(error)
    print(f"  {type(error).__name__}: {result['status_code']} - {result['error'].get('message', result['error'].get('code', ''))}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
