#!/usr/bin/env python3
"""
Практическое занятие 67: Оптимизация производительности
Решение упражнений
"""

import time
import functools
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Caching
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Caching")
print("=" * 60)


class Cache:
    """Простой кэш"""
    
    def __init__(self, ttl_seconds: int = 60):
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}
        self.ttl_seconds = ttl_seconds
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            if time.time() - self.timestamps[key] < self.ttl_seconds:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        self.cache.clear()
        self.timestamps.clear()
    
    def size(self) -> int:
        return len(self.cache)


cache = Cache(ttl_seconds=60)

cache.set("user:1", {"name": "John", "email": "john@example.com"})
cache.set("user:2", {"name": "Jane", "email": "jane@example.com"})

print(f"Cache size: {cache.size()}")
print(f"Get user:1: {cache.get('user:1')}")
print(f"Get user:999 (not exists): {cache.get('user:999')}")


def memoize(func: Callable) -> Callable:
    """Декоратор для мемоизации"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    wrapper.cache = cache
    return wrapper


@memoize
def expensive_function(n: int) -> int:
    time.sleep(0.1)
    return n * n


print("\nMemoization example:")
start = time.time()
result1 = expensive_function(5)
print(f"First call (5): {result1} - {time.time() - start:.3f}s")

start = time.time()
result2 = expensive_function(5)
print(f"Second call (5): {result2} - {time.time() - start:.3f}s")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Profiling
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Profiling")
print("=" * 60)


class Profiler:
    """Простой профилировщик"""
    
    def __init__(self):
        self.timings: Dict[str, List[float]] = {}
        self.call_counts: Dict[str, int] = {}
    
    def record(self, name: str, duration: float):
        if name not in self.timings:
            self.timings[name] = []
            self.call_counts[name] = 0
        
        self.timings[name].append(duration)
        self.call_counts[name] += 1
    
    def get_stats(self, name: str) -> Dict[str, float]:
        if name not in self.timings:
            return {}
        
        timings = self.timings[name]
        return {
            'calls': self.call_counts[name],
            'total': sum(timings),
            'average': sum(timings) / len(timings),
            'min': min(timings),
            'max': max(timings)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        return {name: self.get_stats(name) for name in self.timings}


def profile(profiler: Profiler, name: str):
    """Декоратор для профилирования"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            profiler.record(name, duration)
            return result
        return wrapper
    return decorator


profiler = Profiler()


@profile(profiler, "database_query")
def fetch_users():
    time.sleep(0.05)
    return [{"id": 1, "name": "John"}]


@profile(profiler, "api_call")
def fetch_data():
    time.sleep(0.1)
    return {"data": "test"}


fetch_users()
fetch_users()
fetch_data()

stats = profiler.get_all_stats()

print("Profiling results:")
for name, stat in stats.items():
    print(f"\n{name}:")
    print(f"  Calls: {stat['calls']}")
    print(f"  Total: {stat['total']:.3f}s")
    print(f"  Average: {stat['average']:.3f}s")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Database Query Optimization
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Database Query Optimization")
print("=" * 60)


class QueryOptimizer:
    """Оптимизатор запросов"""
    
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
    
    def add_query(self, query: str, duration: float, rows: int):
        self.queries.append({
            'query': query,
            'duration': duration,
            'rows': rows,
            'timestamp': datetime.now()
        })
    
    def analyze_slow_queries(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        return [
            q for q in self.queries 
            if q['duration'] > threshold
        ]
    
    def get_optimization_hints(self, query: str) -> List[str]:
        hints = []
        
        query_lower = query.lower()
        
        if 'select *' in query_lower:
            hints.append("Избегайте SELECT *, укажите конкретные поля")
        
        if 'where' not in query_lower and 'limit' not in query_lower:
            hints.append("Добавьте WHERE условие и LIMIT")
        
        if 'join' in query_lower and 'on' not in query_lower:
            hints.append("Проверьте условия JOIN")
        
        if 'order by' not in query_lower:
            hints.append("Рассмотрите использование ORDER BY для сортировки")
        
        return hints
    
    def get_summary(self) -> Dict[str, Any]:
        if not self.queries:
            return {'total_queries': 0}
        
        durations = [q['duration'] for q in self.queries]
        
        return {
            'total_queries': len(self.queries),
            'total_duration': sum(durations),
            'average_duration': sum(durations) / len(durations),
            'slow_queries': len(self.analyze_slow_queries())
        }


optimizer = QueryOptimizer()
optimizer.add_query("SELECT * FROM users", 0.5, 1000)
optimizer.add_query("SELECT id, name FROM users WHERE id = 1", 0.01, 1)
optimizer.add_query("SELECT * FROM orders JOIN users ON orders.user_id = users.id", 2.5, 5000)

slow = optimizer.analyze_slow_queries(threshold=1.0)
print(f"Slow queries found: {len(slow)}")

query = "SELECT * FROM users WHERE active = 1"
hints = optimizer.get_optimization_hints(query)
print(f"\nOptimization hints for: {query}")
for hint in hints:
    print(f"  - {hint}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Connection Pooling
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Connection Pooling")
print("=" * 60)


class ConnectionPool:
    """Пул подключений"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.available_connections: List[str] = []
        self.in_use_connections: List[str] = []
        
        for i in range(max_connections):
            self.available_connections.append(f"conn_{i}")
    
    def acquire(self) -> str:
        if self.available_connections:
            conn = self.available_connections.pop()
            self.in_use_connections.append(conn)
            return conn
        raise Exception("No available connections")
    
    def release(self, conn: str):
        if conn in self.in_use_connections:
            self.in_use_connections.remove(conn)
            self.available_connections.append(conn)
    
    def get_stats(self) -> Dict[str, int]:
        return {
            'total': self.max_connections,
            'available': len(self.available_connections),
            'in_use': len(self.in_use_connections)
        }


pool = ConnectionPool(max_connections=5)

conn1 = pool.acquire()
print(f"Acquired connection: {conn1}")

stats = pool.get_stats()
print(f"Pool stats: {stats}")

pool.release(conn1)
stats = pool.get_stats()
print(f"After release: {stats}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Async Optimization
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Async Optimization")
print("=" * 60)


class AsyncTask:
    """Асинхронная задача"""
    
    def __init__(self, name: str, duration: float):
        self.name = name
        self.duration = duration
        self.started_at = None
        self.completed_at = None
    
    def run(self):
        self.started_at = time.time()
        time.sleep(self.duration)
        self.completed_at = time.time()
    
    def get_duration(self) -> float:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return 0


class TaskScheduler:
    """Планировщик задач"""
    
    def __init__(self):
        self.tasks: List[AsyncTask] = []
    
    def add_task(self, task: AsyncTask):
        self.tasks.append(task)
    
    def run_sequential(self):
        start = time.time()
        for task in self.tasks:
            task.run()
        return time.time() - start
    
    def run_parallel(self):
        import concurrent.futures
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(task.run) for task in self.tasks]
            concurrent.futures.wait(futures)
        return time.time() - start


scheduler = TaskScheduler()
scheduler.add_task(AsyncTask("task1", 0.5))
scheduler.add_task(AsyncTask("task2", 0.5))
scheduler.add_task(AsyncTask("task3", 0.5))

seq_time = scheduler.run_sequential()
print(f"Sequential execution: {seq_time:.2f}s")

scheduler2 = TaskScheduler()
scheduler2.add_task(AsyncTask("task1", 0.5))
scheduler2.add_task(AsyncTask("task2", 0.5))
scheduler2.add_task(AsyncTask("task3", 0.5))

par_time = scheduler2.run_parallel()
print(f"Parallel execution: {par_time:.2f}s")
print(f"Speedup: {seq_time/par_time:.1f}x")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
