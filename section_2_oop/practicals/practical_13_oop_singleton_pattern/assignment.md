# Практическое занятие 13: ООП - паттерн Singleton в игровом контексте

## Создание классов с паттерном Singleton для управления игровыми системами

### Цель занятия:
Изучить паттерн проектирования Singleton и научиться реализовывать его в Python различными способами в контексте игровых приложений, а также понять, когда и зачем его использовать в игровой разработке.

### Задачи:
1. Создать классы с паттерном Singleton для управления игровыми системами
2. Реализовать различные способы реализации Singleton (через `__new__`, метаклассы, декораторы)
3. Применить принципы ООП и паттерны проектирования в игровом контексте
4. Обеспечить потокобезопасность при необходимости в многопоточных играх

### План работы:
1. Создание базового Singleton класса
2. Реализация потокобезопасного Singleton
3. Использование метаклассов для создания Singleton
4. Применение декораторов для реализации Singleton
5. Практические задания в игровом контексте

---
# Практическое занятие 13: ООП - паттерн Singleton в игровом контексте

## Создание классов с паттерном Singleton для управления игровыми системами

### Цель занятия:
Изучить паттерн проектирования Singleton и научиться реализовывать его в Python различными способами в контексте игровых приложений, а также понять, когда и зачем его использовать в игровой разработке.

### Задачи:
1. Создать классы с паттерном Singleton для управления игровыми системами
2. Реализовать различные способы реализации Singleton (через `__new__`, метаклассы, декораторы)
3. Применить принципы ООП и паттерны проектирования в игровом контексте
4. Обеспечить потокобезопасность при необходимости в многопоточных играх

---

## 1. Теоретическая часть

### Основные понятия паттерна Singleton

**Паттерн Singleton** — это порождающий паттерн проектирования, который гарантирует, что у класса есть только один экземпляр, и предоставляет глобальную точку доступа к этому экземпляру. В игровой разработке Singleton часто используется для классов, которые должны быть уникальными в игре: менеджеры ресурсов, менеджеры сохранений, менеджеры аудио, логгеры и т.д.

**Преимущества Singleton:**
- Гарантированно один экземпляр класса
- Глобальная точка доступа
- Контролируемое владение объектом

**Недостатки Singleton:**
- Нарушение принципа единственной ответственности
- Сложности с тестированием
- Возможные проблемы с многопоточностью
- Скрывает зависимости

### Пример базовой реализации Singleton (уровень 1 - начальный)

```python
class GameManager:
    """
    Менеджер игры - Singleton для управления игровой сессией
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.game_state = "stopped"  # Начальное состояние
            cls._instance.current_level = 1
            cls._instance.score = 0
            cls._instance.players = []
        return cls._instance

    def start_game(self, level=1):
        """Инициализация игровой сессии"""
        self.game_state = "running"
        self.current_level = level
        self.score = 0
        print(f"Игра запущена. Уровень: {self.current_level}")

    def end_game(self):
        """Завершение игровой сессии"""
        self.game_state = "stopped"
        print(f"Игра завершена. Финальный счет: {self.score}")

    def add_score(self, points):
        """Добавить очки к общему счету"""
        self.score += points
        print(f"Получено {points} очков. Общий счет: {self.score}")

    def get_instance_info(self):
        """Получить информацию о текущем экземпляре"""
        return f"GameManager (ID: {id(self)}, State: {self.game_state}, Level: {self.current_level}, Score: {self.score})"


# Пример использования
game1 = GameManager()
game2 = GameManager()

print(f"Одинаковые экземпляры: {game1 is game2}")  # Должно быть True

game1.start_game(3)
game2.add_score(100)  # Обратите внимание, что используем game2, но изменяется состояние game1
print(game1.get_instance_info())
```

---

## 2. Практические задания

### Уровень 1 - Начальный

#### Задание 1.1: Базовая реализация менеджера ресурсов

Создайте класс `ResourceManager` как Singleton для управления игровыми ресурсами (текстуры, модели, звуки). Реализуйте методы для загрузки, получения и выгрузки ресурсов. Используйте `__new__` для обеспечения единственности экземпляра.

**Шаги выполнения:**
1. Создайте класс `ResourceManager` с атрибутом `_instance` для хранения единственного экземпляра
2. Реализуйте метод `__new__` для создания единственного экземпляра
3. Добавьте атрибут `resources` (словарь) для хранения загруженных ресурсов
4. Реализуйте метод `load_resource(name, path)` для загрузки ресурса
5. Реализуйте метод `get_resource(name)` для получения ресурса
6. Реализуйте метод `unload_resource(name)` для выгрузки ресурса
7. Создайте экземпляры класса и протестируйте его работу

```python
class ResourceManager:
    # ВАШ КОД ЗДЕСЬ - реализуйте Singleton через __new__
    pass  # Замените на ваш код

    def load_resource(self, resource_name, resource_path):
        # ВАШ КОД ЗДЕСЬ - реализуйте загрузку ресурса
        pass  # Замените на ваш код

    def get_resource(self, resource_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение ресурса
        pass  # Замените на ваш код

    def unload_resource(self, resource_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте выгрузку ресурса
        pass  # Замените на ваш код

# Пример использования (после реализации)
# rm1 = ResourceManager()
# rm2 = ResourceManager()
# print(f"Одинаковые экземпляры: {rm1 is rm2}")  # Должно быть True
# rm1.load_resource("background", "/assets/background.png")
# resource = rm2.get_resource("background")  # Обратите внимание, что используем rm2
# print(f"Ресурс получен: {resource is not None}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.resources = {}  # Хранилище ресурсов
            cls._instance.loading_queue = []  # Очередь загрузки
        return cls._instance

    def load_resource(self, resource_name, resource_path):
        """Загрузка ресурса в кэш"""
        if resource_name not in self.resources:
            print(f"Загружаем ресурс: {resource_name} из {resource_path}")
            # Здесь могла бы быть реальная логика загрузки файла
            self.resources[resource_name] = f"Данные ресурса {resource_name}"
            print(f"Ресурс {resource_name} успешно загружен")
        else:
            print(f"Ресурс {resource_name} уже загружен")

    def get_resource(self, resource_name):
        """Получение ресурса из кэша"""
        return self.resources.get(resource_name, None)

    def unload_resource(self, resource_name):
        """Выгрузка ресурса из кэша"""
        if resource_name in self.resources:
            del self.resources[resource_name]
            print(f"Ресурс {resource_name} выгружен")
        else:
            print(f"Ресурс {resource_name} не найден в кэше")

    def get_loaded_resources_count(self):
        """Получить количество загруженных ресурсов"""
        return len(self.resources)

# Пример использования
rm1 = ResourceManager()
rm2 = ResourceManager()

print(f"Одинаковые экземпляры: {rm1 is rm2}")  # Должно быть True

rm1.load_resource("background", "/assets/background.png")
resource = rm2.get_resource("background")  # Обратите внимание, что используем rm2
print(f"Ресурс получен: {resource is not None}")

print(f"Количество загруженных ресурсов: {rm1.get_loaded_resources_count()}")
```

</details>

#### Задание 1.2: Реализация логгера как Singleton

Создайте класс `GameLogger` как Singleton для ведения игровых логов. Реализуйте методы для записи сообщений разных уровней (INFO, WARNING, ERROR), получения истории логов и очистки логов. Используйте `__new__` для обеспечения единственности экземпляра.

```python
class GameLogger:
    # ВАШ КОД ЗДЕСЯ - реализуйте Singleton через __new__
    pass  # Замените на ваш код

    def log(self, message, level="INFO"):
        # ВАШ КОД ЗДЕСЯ - реализуйте запись лога
        pass  # Замените на ваш код

    def get_logs(self, level_filter=None):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение логов с фильтрацией
        pass  # Замените на ваш код

    def clear_logs(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте очистку логов
        pass  # Замените на ваш код

# Пример использования (после реализации)
# logger1 = GameLogger()
# logger2 = GameLogger()
# print(f"Одинаковые экземпляры: {logger1 is logger2}")  # Должно быть True
# logger1.log("Игра запущена", "INFO")
# logger2.log("Ошибка загрузки уровня", "ERROR")  # Используем logger2
# print(f"Все логи: {logger1.get_logs()}")
# print(f"Только ошибки: {logger1.get_logs(level_filter='ERROR')}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import datetime

class GameLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []  # История логов
            cls._instance.log_file = "game.log"  # Файл для сохранения логов
        return cls._instance

    def log(self, message, level="INFO"):
        """Запись лога с уровнем"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # Выводим в консоль
        # Здесь могла бы быть запись в файл
        # with open(self.log_file, "a", encoding="utf-8") as f:
        #     f.write(log_entry + "\n")

    def get_logs(self, level_filter=None):
        """Получение логов с фильтрацией по уровню"""
        if level_filter:
            return [log for log in self.logs if level_filter in log]
        return self.logs.copy()

    def clear_logs(self):
        """Очистка всех логов"""
        self.logs.clear()
        print("Логи очищены")

# Пример использования
logger1 = GameLogger()
logger2 = GameLogger()

print(f"Одинаковые экземпляры: {logger1 is logger2}")  # Должно быть True

logger1.log("Игра запущена", "INFO")
logger2.log("Ошибка загрузки уровня", "ERROR")  # Используем logger2
logger1.log("Игрок вошел в игру", "INFO")

print(f"Все логи: {logger1.get_logs()}")
print(f"Только ошибки: {logger1.get_logs(level_filter='ERROR')}")

logger1.clear_logs()
print(f"После очистки: {logger1.get_logs()}")
```

</details>


### Уровень 2 - Средний

#### Задание 2.1: Потокобезопасный Singleton

Реализуйте потокобезопасный `ResourceManager` с использованием блокировок (Lock) для предотвращения создания нескольких экземпляров в многопоточной среде. Используйте двойную проверку блокировки для эффективности. Добавьте метод `get_instance()` для получения экземпляра класса в многопоточной среде.

**Шаги выполнения:**
1. Создайте класс `ThreadSafeResourceManager` с атрибутом `_instance` и `_lock` для блокировки
2. Реализуйте метод `__new__` с двойной проверкой блокировки
3. Добавьте методы для работы с ресурсами (загрузка, получение, выгрузка)
4. Используйте блокировку при работе с ресурсами для предотвращения гонок
5. Протестируйте работу в многопоточной среде

```python
import threading

class ThreadSafeResourceManager:
    # ВАШ КОД ЗДЕСЯ - реализуйте потокобезопасный Singleton
    pass  # Замените на ваш код

    def load_resource(self, resource_name, resource_path):
        # ВАШ КОД ЗДЕСЯ - реализуйте потокобезопасную загрузку ресурса
        pass  # Замените на ваш код

    def get_resource(self, resource_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте потокобезопасное получение ресурса
        pass  # Замените на ваш код

    def get_loaded_resources_count(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение количества ресурсов
        pass  # Замените на ваш код

def create_resource_manager(results, idx):
    """Функция для создания экземпляра в отдельном потоке"""
    # ВАШ КОД ЗДЕСЯ - создайте экземпляр и сохраните в results
    pass  # Замените на ваш код

# Тестирование в многопоточной среде
# threads = []
# results = [None] * 5  # Создаем 5 потоков
# for i in range(5):
#     t = threading.Thread(target=create_resource_manager, args=(results, i))
#     threads.append(t)
#
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()
#
# # Проверяем результаты
# ids = [id(r) for r in results]
# print(f"ID экземпляров: {ids}")
# print(f"Все ID одинаковы: {len(set(ids)) == 1}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import threading

class ThreadSafeResourceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Двойная проверка блокировки для эффективности
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.resources = {}
                    cls._instance.loading_queue = []
        return cls._instance

    def load_resource(self, resource_name, resource_path):
        """Потокобезопасная загрузка ресурса в кэш"""
        with self._lock:
            if resource_name not in self.resources:
                print(f"Загружаем ресурс: {resource_name} из {resource_path}")
                # Здесь могла бы быть реальная логика загрузки файла
                self.resources[resource_name] = f"Данные ресурса {resource_name}"
                print(f"Ресурс {resource_name} успешно загружен")
            else:
                print(f"Ресурс {resource_name} уже загружен")

    def get_resource(self, resource_name):
        """Потокобезопасное получение ресурса из кэша"""
        with self._lock:
            return self.resources.get(resource_name, None)

    def unload_resource(self, resource_name):
        """Потокобезопасная выгрузка ресурса из кэша"""
        with self._lock:
            if resource_name in self.resources:
                del self.resources[resource_name]
                print(f"Ресурс {resource_name} выгружен")
            else:
                print(f"Ресурс {resource_name} не найден в кэше")

    def get_loaded_resources_count(self):
        """Потокобезопасное получение количества загруженных ресурсов"""
        with self._lock:
            return len(self.resources)

def create_resource_manager(results, idx):
    """Функция для создания экземпляра в отдельном потоке"""
    import time
    time.sleep(0.1)  # Небольшая задержка для симуляции конкурентности
    results[idx] = ThreadSafeResourceManager()

# Тестирование в многопоточной среде
print("=== Тестирование потокобезопасного Singleton ===")
threads = []
results = [None] * 5  # Создаем 5 потоков

for i in range(5):
    t = threading.Thread(target=create_resource_manager, args=(results, i))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# Проверяем результаты
ids = [id(r) for r in results]
print(f"ID экземпляров: {ids}")
print(f"Все ID одинаковы: {len(set(ids)) == 1}")

# Демонстрация работы с ресурсами из разных потоков
rm = results[0]  # Берем первый экземпляр
print(f"\nЗагрузка ресурсов в потокобезопасном режиме:")
rm.load_resource("texture1", "/assets/texture1.png")
rm.load_resource("model1", "/assets/model1.obj")
print(f"Количество загруженных ресурсов: {rm.get_loaded_resources_count()}")
```

</details>

#### Задание 2.2: Реализация через метакласс

Создайте метакласс `SingletonMeta`, который обеспечивает паттерн Singleton для любого класса. Примените его к классу `GameSettings` для управления настройками игры. Реализуйте потокобезопасность с использованием метакласса. Добавьте методы для установки и получения настроек игры (громкость, разрешение, качество графики и т.д.).

```python
import threading

class SingletonMeta(type):
    # ВАШ КОД ЗДЕСЯ - реализуйте метакласс для Singleton
    pass  # Замените на ваш код

class GameSettings(metaclass=SingletonMeta):
    # ВАШ КОД ЗДЕСЯ - реализуйте класс настроек игры
    pass  # Замените на ваш код

    def set_volume(self, volume):
        # ВАШ КОД ЗДЕСЯ - реализуйте установку громкости
        pass  # Замените на ваш код

    def set_resolution(self, width, height):
        # ВАШ КОД ЗДЕСЯ - реализуйте установку разрешения
        pass  # Замените на ваш код

    def toggle_fullscreen(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте переключение полноэкранного режима
        pass  # Замените на ваш код

    def get_settings_summary(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте получение сводки настроек
        pass  # Замените на ваш код

# Пример использования (после реализации)
# settings1 = GameSettings()
# settings2 = GameSettings()
# print(f"Одинаковые экземпляры: {settings1 is settings2}")  # Должно быть True
# settings1.set_volume(80)
# settings2.set_resolution(1920, 1080)  # Используем settings2
# print(settings1.get_settings_summary())
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import threading

class SingletonMeta(type):
    """
    Метакласс для создания Singleton классов
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class GameSettings(metaclass=SingletonMeta):
    """
    Настройки игры - Singleton для управления настройками приложения
    """
    def __init__(self):
        # Защита от повторной инициализации атрибутов
        if not hasattr(self, 'initialized'):
            self.volume = 80
            self.resolution = (1920, 1080)
            self.fullscreen = False
            self.graphics_quality = "high"
            self.controls = {"move_forward": "W", "move_backward": "S", "jump": "SPACE"}
            self.initialized = True

    def set_volume(self, volume):
        """Установить громкость"""
        if 0 <= volume <= 100:
            old_volume = self.volume
            self.volume = volume
            print(f"Громкость изменена с {old_volume}% на {self.volume}%")
        else:
            print("Некорректное значение громкости. Должно быть от 0 до 100.")

    def set_resolution(self, width, height):
        """Установить разрешение экрана"""
        self.resolution = (width, height)
        print(f"Разрешение изменено на {width}x{height}")

    def toggle_fullscreen(self):
        """Переключить полноэкранный режим"""
        self.fullscreen = not self.fullscreen
        status = "включен" if self.fullscreen else "выключен"
        print(f"Полноэкранный режим {status}")

    def get_settings_summary(self):
        """Получить сводку настроек"""
        return f"""
        Настройки игры:
        - Громкость: {self.volume}%
        - Разрешение: {self.resolution[0]}x{self.resolution[1]}
        - Полноэкранный режим: {'Да' if self.fullscreen else 'Нет'}
        - Качество графики: {self.graphics_quality}
        """

# Пример использования
settings1 = GameSettings()
settings2 = GameSettings()

print(f"Одинаковые экземпляры: {settings1 is settings2}")  # Должно быть True

settings1.set_volume(80)
settings2.set_resolution(1920, 1080)  # Используем settings2
settings1.toggle_fullscreen()

print(settings1.get_settings_summary())

# Проверка, что изменения применяются к одному и тому же экземпляру
print(f"Громкость в settings2: {settings2.volume}%")  # Должно быть 80%
```

</details>


### Уровень 3 - Повышенный

#### Задание 3.1: Декоратор Singleton

Создайте декоратор `singleton`, который превращает любой класс в Singleton. Примените его к классу `AudioManager` для управления аудио в игре. Реализуйте потокобезопасность с использованием декоратора. Добавьте методы для воспроизведения музыки и звуковых эффектов, регулировки громкости и управления аудио-ресурсами. Убедитесь, что все методы работают корректно в многопоточной среде.

**Шаги выполнения:**
1. Создайте декоратор `singleton` с использованием потокобезопасной логики
2. Примените декоратор к классу `AudioManager`
3. Реализуйте методы для управления аудио (воспроизведение, громкость, загрузка ресурсов)
4. Протестируйте работу в многопоточной среде
5. Убедитесь, что все методы обеспечивают потокобезопасность

```python
import threading

def singleton(cls):
    # ВАШ КОД ЗДЕСЯ - реализуйте декоратор Singleton
    pass  # Замените на ваш код

@singleton
class AudioManager:
    # ВАШ КОД ЗДЕСЯ - реализуйте класс аудио менеджера
    pass  # Замените на ваш код

    def play_music(self, music_track, loop=True):
        # ВАШ КОД ЗДЕСЯ - реализуйте воспроизведение музыки
        pass  # Замените на ваш код

    def play_sound_effect(self, sfx_name):
        # ВАШ КОД ЗДЕСЯ - реализуйте воспроизведение звукового эффекта
        pass  # Замените на ваш код

    def set_music_volume(self, volume):
        # ВАШ КОД ЗДЕСЯ - реализуйте установку громкости музыки
        pass  # Замените на ваш код

    def set_sfx_volume(self, volume):
        # ВАШ КОД ЗДЕСЯ - реализуйте установку громкости звуковых эффектов
        pass  # Замените на ваш код

    def toggle_mute(self):
        # ВАШ КОД ЗДЕСЯ - реализуйте вкл/выкл звук
        pass  # Замените на ваш код

    def preload_audio(self, audio_name, audio_path):
        # ВАШ КОД ЗДЕСЯ - реализуйте предзагрузку аудио
        pass  # Замените на ваш код

def create_audio_manager(results, idx):
    """Функция для создания экземпляра в отдельном потоке"""
    # ВАШ КОД ЗДЕСЯ - создайте экземпляр и сохраните в results
    pass  # Замените на ваш код

# Тестирование в многопоточной среде
# threads = []
# results = [None] * 3  # Создаем 3 потока
# for i in range(3):
#     t = threading.Thread(target=create_audio_manager, args=(results, i))
#     threads.append(t)
#
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()
#
# # Проверяем результаты
# ids = [id(r) for r in results]
# print(f"ID экземпляров: {ids}")
# print(f"Все ID одинаковы: {len(set(ids)) == 1}")
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import threading

def singleton(cls):
    """
    Декоратор для превращения класса в Singleton
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class AudioManager:
    """
    Менеджер аудио - Singleton для управления звуком в игре
    """
    def __init__(self):
        # Защита от повторной инициализации атрибутов
        if not hasattr(self, 'initialized'):
            self.music_volume = 80
            self.sfx_volume = 100
            self.current_music = None
            self.is_muted = False
            self.audio_library = {}  # Библиотека аудиофайлов
            self.playing_sounds = set()  # Воспроизводимые звуки
            self.initialized = True
            print("AudioManager инициализирован")

    def play_music(self, music_track, loop=True):
        """Воспроизведение фоновой музыки"""
        if self.is_muted:
            print("Звук выключен, музыка не воспроизводится")
            return False

        if music_track in self.audio_library:
            self.current_music = music_track
            volume = self.music_volume if not self.is_muted else 0
            print(f"Воспроизводим музыку '{music_track}' (громкость: {volume}%, loop: {loop})")
            return True
        else:
            print(f"Музыкальный трек '{music_track}' не найден в библиотеке")
            return False

    def play_sound_effect(self, sfx_name):
        """Воспроизведение звукового эффекта"""
        if self.is_muted:
            print("Звук выключен, звуковые эффекты не воспроизводятся")
            return False

        if sfx_name in self.audio_library:
            volume = self.sfx_volume if not self.is_muted else 0
            self.playing_sounds.add(sfx_name)
            print(f"Воспроизводим звуковой эффект '{sfx_name}' (громкость: {volume}%)")
            # Здесь могла бы быть логика остановки звука через некоторое время
            self.playing_sounds.discard(sfx_name)  # В реальности это произошло бы позже
            return True
        else:
            print(f"Звуковой эффект '{sfx_name}' не найден в библиотеке")
            return False

    def set_music_volume(self, volume):
        """Установить громкость музыки"""
        if 0 <= volume <= 100:
            old_volume = self.music_volume
            self.music_volume = volume
            print(f"Громкость музыки изменена с {old_volume}% на {self.music_volume}%")
            if self.current_music:
                print(f"Применяем новую громкость к текущей музыке '{self.current_music}'")
        else:
            print("Некорректное значение громкости музыки. Должно быть от 0 до 100.")

    def set_sfx_volume(self, volume):
        """Установить громкость звуковых эффектов"""
        if 0 <= volume <= 100:
            old_volume = self.sfx_volume
            self.sfx_volume = volume
            print(f"Громкость звуковых эффектов изменена с {old_volume}% на {self.sfx_volume}%")
        else:
            print("Некорректное значение громкости звуковых эффектов. Должно быть от 0 до 100.")

    def toggle_mute(self):
        """Вкл/выкл звук"""
        self.is_muted = not self.is_muted
        status = "включен" if not self.is_muted else "выключен"
        print(f"Звук {status}")

    def preload_audio(self, audio_name, audio_path):
        """Предзагрузка аудиофайла"""
        self.audio_library[audio_name] = audio_path
        print(f"Аудиофайл '{audio_name}' предзагружен из '{audio_path}'")

    def get_instance_info(self):
        """Получить информацию о текущем экземпляре"""
        return f"AudioManager (ID: {id(self)}, Music Vol: {self.music_volume}%, SFX Vol: {self.sfx_volume}%, Muted: {self.is_muted})"


def create_audio_manager(results, idx):
    """Функция для создания экземпляра в отдельном потоке"""
    import time
    time.sleep(0.1)  # Небольшая задержка для симуляции конкурентности
    results[idx] = AudioManager()


# Тестирование в многопоточной среде
print("=== Тестирование Singleton через декоратор ===")
threads = []
results = [None] * 3  # Создаем 3 потока

for i in range(3):
    t = threading.Thread(target=create_audio_manager, args=(results, i))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# Проверяем результаты
ids = [id(r) for r in results]
print(f"ID экземпляров: {ids}")
print(f"Все ID одинаковы: {len(set(ids)) == 1}")

# Демонстрация использования
audio_manager1 = results[0]  # Берем первый экземпляр
audio_manager2 = AudioManager()  # Создаем еще один (должен быть тем же)

print(f"Одинаковые экземпляры: {audio_manager1 is audio_manager2}")  # Должно быть True

audio_manager1.preload_audio("battle_theme", "/audio/battle.mp3")
audio_manager1.preload_audio("sword_swing", "/audio/sword.wav")

audio_manager1.play_music("battle_theme")
audio_manager2.play_sound_effect("sword_swing")  # Используем второй экземпляр, но это тот же объект

print(audio_manager1.get_instance_info())
```

</details>

#### Задание 3.2: Комплексная игровая система с несколькими Singleton

Создайте комплексную игровую систему, объединяющую несколько Singleton классов: `GameManager`, `ResourceManager`, `GameLogger`, `GameSettings`, `AudioManager`. Реализуйте взаимодействие между этими системами. Создайте класс `GameEngine`, который будет использовать все эти менеджеры для управления игрой. Убедитесь, что все менеджеры работают как настоящие Singleton и правильно взаимодействуют друг с другом в многопоточной среде.

```python