# Практическое занятие 13: ООП - паттерн Singleton в игровом контексте

## Цель занятия
Изучить паттерн проектирования Singleton и научиться реализовывать его в Python различными способами в контексте игровых приложений, а также понять, когда и зачем его использовать в игровой разработке.

## Задачи

### Задача 1: Базовая реализация Singleton для игрового менеджера (20 баллов)
Создайте класс `GameManager` с использованием паттерна Singleton:
- Реализуйте метод `__new__` для обеспечения единственности экземпляра
- Добавьте метод `start_game()` для инициализации игровой сессии
- Добавьте метод `end_game()` для завершения игровой сессии

```python
class GameManager:
    """
    Менеджер игры -.Singleton для управления игровой сессией
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

### Задача 2: Потокобезопасная реализация игрового менеджера (20 баллов)
Реализуйте потокобезопасный Singleton `ResourceManager` с использованием:
- Блокировок (Lock) для предотвращения создания нескольких экземпляров в многопоточной среде
- Метода `get_instance()` для получения экземпляра класса

```python
import threading

class ResourceManager:
    """
    Менеджер ресурсов - потокобезопасный Singleton для управления игровыми ресурсами
    """
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
        """Загрузка ресурса в кэш"""
        with self._lock:
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
        with self._lock:
            if resource_name in self.resources:
                del self.resources[resource_name]
                print(f"Ресурс {resource_name} выгружен")
            else:
                print(f"Ресурс {resource_name} не найден в кэше")

    def get_loaded_resources_count(self):
        """Получить количество загруженных ресурсов"""
        return len(self.resources)
```

### Задача 3: Реализация через метакласс для игрового логгера (20 баллов)
Создайте метакласс `SingletonMeta`, который:
- Обеспечивает паттерн Singleton для любого класса
- Примените его к классу `GameLogger` для ведения логов в игре

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


class GameLogger(metaclass=SingletonMeta):
    """
    Логгер игры - Singleton для ведения игровых логов
    """
    def __init__(self):
        if not hasattr(self, 'logs'):
            self.logs = []
            self.log_file = "game.log"

    def log(self, message, level="INFO"):
        """Запись лога с уровнем"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # Выводим в консоль
        # Здесь могла бы быть запись в файл
        # with open(self.log_file, "a", encoding="utf-8") as f:
        #     f.write(log_entry + "\n")

    def get_logs(self, level_filter=None):
        """Получить логи с фильтрацией по уровню"""
        if level_filter:
            return [log for log in self.logs if level_filter in log]
        return self.logs.copy()

    def clear_logs(self):
        """Очистить все логи"""
        self.logs.clear()
        print("Логи очищены")
```

### Задача 4: Декоратор Singleton для игровой настройки (20 баллов)
Создайте декоратор `singleton`, который:
- Преобразует любой класс в Singleton
- Примените его к классу `GameSettings` для управления настройками игры

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
class GameSettings:
    """
    Настройки игры - Singleton для управления настройками приложения
    """
    def __init__(self):
        self.volume = 80
        self.resolution = (1920, 1080)
        self.fullscreen = False
        self.graphics_quality = "high"
        self.controls = {"move_forward": "W", "move_backward": "S", "jump": "SPACE"}

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
```

### Задача 5: Применение Singleton в реальном игровом сценарии (20 баллов)
Реализуйте систему уведомлений:
- Класс `NotificationManager` как Singleton
- Методы для отправки различных типов уведомлений
- Очередь уведомлений и возможность их просмотра

```python
import threading
from datetime import datetime

class NotificationManager(metaclass=SingletonMeta):
    """
    Менеджер уведомлений - Singleton для управления игровыми уведомлениями
    """
    def __init__(self):
        if not hasattr(self, 'notifications'):
            self.notifications = []
            self.subscribers = []  # Список подписчиков на уведомления

    def subscribe(self, subscriber):
        """Подписаться на уведомления"""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            print(f"{subscriber.__class__.__name__} подписался на уведомления")

    def unsubscribe(self, subscriber):
        """Отписаться от уведомлений"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            print(f"{subscriber.__class__.__name__} отписался от уведомлений")

    def send_notification(self, message, notification_type="info", priority="normal"):
        """Отправить уведомление"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        notification = {
            "timestamp": timestamp,
            "type": notification_type,
            "priority": priority,
            "message": message
        }
        self.notifications.append(notification)
        print(f"[{notification_type.upper()}] {message}")

        # Уведомить всех подписчиков
        for subscriber in self.subscribers:
            if hasattr(subscriber, 'receive_notification'):
                subscriber.receive_notification(notification)

    def get_notifications(self, notification_type=None, limit=None):
        """Получить уведомления с возможностью фильтрации"""
        filtered_notifications = self.notifications
        if notification_type:
            filtered_notifications = [n for n in filtered_notifications if n["type"] == notification_type]
        if limit:
            filtered_notifications = filtered_notifications[-limit:]
        return filtered_notifications

    def clear_notifications(self):
        """Очистить все уведомления"""
        count = len(self.notifications)
        self.notifications.clear()
        print(f"Очищено {count} уведомлений")

    def get_unread_count(self):
        """Получить количество непрочитанных уведомлений"""
        # В этой реализации все уведомления считаются непрочитанными
        return len(self.notifications)
```

## Методические указания
1. Используйте разные подходы к реализации Singleton (через `__new__`, метаклассы, декораторы)
2. Обратите внимание на потокобезопасность при многопоточном использовании в игровых приложениях
3. Рассмотрите плюсы и минусы использования паттерна Singleton в игровой разработке
4. Следите за тем, чтобы Singleton действительно обеспечивал уникальность экземпляра в игровом контексте

## Требования к отчету
- Исходный код всех реализаций Singleton с игровой тематикой
- Примеры использования каждого подхода в игровом контексте
- Сравнение различных реализаций и их применимость в игровых приложениях

## Критерии оценки
- Корректная реализация паттерна Singleton в игровом контексте: 50%
- Понимание различных подходов к реализации в игровой разработке: 30%
- Качество кода и документация в игровом контексте: 20%

## Практические задания

### Задание 1: Менеджер аудио как Singleton

Реализуйте `AudioManager` как Singleton для управления звуком в игре. Добавьте методы для воспроизведения музыки и звуковых эффектов, регулировки громкости и управления аудио-ресурсами.

```python
class AudioManager(metaclass=SingletonMeta):
    """
    Менеджер аудио - Singleton для управления звуком в игре
    """
    def __init__(self):
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


# Демонстрация использования
audio_manager1 = AudioManager()
audio_manager2 = AudioManager()

print(f"Одинаковые экземпляры: {audio_manager1 is audio_manager2}")  # Должно быть True

audio_manager1.preload_audio("battle_theme", "/audio/battle.mp3")
audio_manager1.preload_audio("sword_swing", "/audio/sword.wav")

audio_manager1.play_music("battle_theme")
audio_manager2.play_sound_effect("sword_swing")  # Используем второй экземпляр, но это тот же объект

print(audio_manager1.get_instance_info())
```

### Задание 2: Менеджер сохранений как Singleton

Создайте `SaveManager` как Singleton для управления сохранением и загрузкой игровых данных. Реализуйте методы для сохранения прогресса, загрузки игры и управления слотами сохранения.

```python
import json
import os

@singleton
class SaveManager:
    """
    Менеджер сохранений - Singleton для управления сохранением и загрузкой игры
    """
    def __init__(self):
        self.save_directory = "saves"
        self.max_save_slots = 5
        self.auto_save_enabled = True

        # Создаем директорию для сохранений, если её нет
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def create_save_slot(self, slot_number, game_data):
        """Создать сохранение в определенном слоте"""
        if not 1 <= slot_number <= self.max_save_slots:
            print(f"Неверный номер слота. Допустимые значения: 1-{self.max_save_slots}")
            return False

        save_file = os.path.join(self.save_directory, f"save_{slot_number}.json")
        save_info = {
            "timestamp": datetime.now().isoformat(),
            "slot_number": slot_number,
            "game_data": game_data
        }

        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_info, f, ensure_ascii=False, indent=2)
            print(f"Игра сохранена в слот {slot_number}")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении в слот {slot_number}: {e}")
            return False

    def load_from_slot(self, slot_number):
        """Загрузить игру из определенного слота"""
        if not 1 <= slot_number <= self.max_save_slots:
            print(f"Неверный номер слота. Допустимые значения: 1-{self.max_save_slots}")
            return None

        save_file = os.path.join(self.save_directory, f"save_{slot_number}.json")

        if not os.path.exists(save_file):
            print(f"Слот {slot_number} пустой или файл не существует")
            return None

        try:
            with open(save_file, 'r', encoding='utf-8') as f:
                save_info = json.load(f)
            print(f"Игра загружена из слота {slot_number}")
            return save_info["game_data"]
        except Exception as e:
            print(f"Ошибка при загрузке из слота {slot_number}: {e}")
            return None

    def list_save_slots(self):
        """Получить список доступных слотов сохранения"""
        saves = []
        for i in range(1, self.max_save_slots + 1):
            save_file = os.path.join(self.save_directory, f"save_{i}.json")
            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r', encoding='utf-8') as f:
                        save_info = json.load(f)
                    saves.append({
                        "slot": i,
                        "timestamp": save_info["timestamp"],
                        "has_data": True
                    })
                except:
                    saves.append({
                        "slot": i,
                        "timestamp": "неизвестно",
                        "has_data": False
                    })
            else:
                saves.append({
                    "slot": i,
                    "timestamp": None,
                    "has_data": False
                })
        return saves

    def delete_save_slot(self, slot_number):
        """Удалить сохранение из слота"""
        if not 1 <= slot_number <= self.max_save_slots:
            print(f"Неверный номер слота. Допустимые значения: 1-{self.max_save_slots}")
            return False

        save_file = os.path.join(self.save_directory, f"save_{slot_number}.json")

        if os.path.exists(save_file):
            os.remove(save_file)
            print(f"Слот {slot_number} очищен")
            return True
        else:
            print(f"Слот {slot_number} и так пустой")
            return False

    def auto_save(self, game_data, slot_number=1):
        """Автоматическое сохранение"""
        if self.auto_save_enabled:
            return self.create_save_slot(slot_number, game_data)
        else:
            print("Автосохранение отключено")
            return False

    def get_save_info(self, slot_number):
        """Получить информацию о сохранении в слоте"""
        if not 1 <= slot_number <= self.max_save_slots:
            print(f"Неверный номер слота. Допустимые значения: 1-{self.max_save_slots}")
            return None

        save_file = os.path.join(self.save_directory, f"save_{slot_number}.json")

        if os.path.exists(save_file):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    save_info = json.load(f)
                return {
                    "slot": slot_number,
                    "timestamp": save_info["timestamp"],
                    "has_data": True,
                    "data_preview": dict(list(save_info["game_data"].items())[:3]) # Первые 3 поля данных
                }
            except Exception as e:
                print(f"Ошибка при чтении информации о слоте {slot_number}: {e}")
                return None
        else:
            return {
                "slot": slot_number,
                "timestamp": None,
                "has_data": False,
                "data_preview": None
            }


# Демонстрация использования
save_manager1 = SaveManager()
save_manager2 = SaveManager()

print(f"Одинаковые экземпляры: {save_manager1 is save_manager2}")  # Должно быть True

# Сохраняем игру
game_data = {
    "player_name": "Артур",
    "level": 5,
    "score": 15000,
    "position": {"x": 100, "y": 200},
    "inventory": ["меч", "щит", "зелье"]
}

save_manager1.create_save_slot(1, game_data)

# Загружаем игру
loaded_data = save_manager2.load_from_slot(1)
if loaded_data:
    print(f"Загруженные данные: {loaded_data['player_name']}, уровень {loaded_data['level']}")

# Проверяем список слотов
saves = save_manager1.list_save_slots()
for save in saves:
    status = "занят" if save["has_data"] else "пустой"
    print(f"Слот {save['slot']}: {status} {save['timestamp'] or ''}")
```

### Задача 3: Сравнение различных реализаций Singleton

Создайте три разных класса Singleton (с использованием `__new__`, метакласса и декоратора) и сравните их поведение в многопоточной среде. Напишите тест, который создает экземпляры в разных потоках и проверяет, что всегда создается только один экземпляр.

```python
import threading
import time

# Singleton реализованный через __new__
class NewStyleSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.creation_time = time.time()
        return cls._instance

# Singleton реализованный через метакласс
class MetaSingleton(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'creation_time'):
            self.creation_time = time.time()

# Singleton реализованный через декоратор
@singleton
class DecoratorSingleton:
    def __init__(self):
        self.creation_time = time.time()

def create_instance(cls, results, idx):
    """Функция для создания экземпляра в отдельном потоке"""
    time.sleep(0.1)  # Небольшая задержка для симуляции конкурентности
    instance = cls()
    results[idx] = (instance, id(instance), instance.creation_time)

def test_multithreaded_singleton(cls, cls_name):
    """Тест многопоточного создания экземпляров Singleton"""
    print(f"\nТестирование {cls_name}:")
    threads = []
    results = [None] * 5  # Создаем 5 потоков

    # Создаем потоки
    for i in range(5):
        t = threading.Thread(target=create_instance, args=(cls, results, i))
        threads.append(t)

    # Запускаем потоки
    for t in threads:
        t.start()

    # Ждем завершения всех потоков
    for t in threads:
        t.join()

    # Проверяем результаты
    ids = [result[1] for result in results]
    times = [result[2] for result in results]

    print(f"  ID экземпляров: {ids}")
    print(f"  Все ID одинаковы: {len(set(ids)) == 1}")
    print(f"  Времена создания: {times}")

# Запускаем тесты
test_multithreaded_singleton(NewStyleSingleton, "NewStyleSingleton")
test_multithreaded_singleton(MetaSingleton, "MetaSingleton")
test_multithreaded_singleton(DecoratorSingleton, "DecoratorSingleton")
```

## Дополнительные задания

### Задание 4: Игровой менеджер событий

Создайте `EventManager` как Singleton для управления игровыми событиями. Реализуйте систему подписки на события, публикации событий и обработки событий различными компонентами игры.

### Задание 5: Менеджер шаблонов

Реализуйте `TemplateManager` как Singleton для управления шаблонами игровых объектов (например, шаблоны монстров, предметов, уровней).

## Контрольные вопросы:
1. В чем разница между различными способами реализации Singleton (через `__new__`, метакласс, декоратор)?
2. Как обеспечить потокобезопасность Singleton в многопоточной игровой среде?
3. В каких случаях в игровой разработке целесообразно использовать паттерн Singleton?
4. Какие проблемы могут возникнуть при использовании Singleton в тестировании игровой логики?
5. Какие альтернативы Singleton существуют для управления глобальным состоянием в игре?