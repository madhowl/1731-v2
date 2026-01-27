# singleton_example.py

import json
import os
import threading
from datetime import datetime

class ResourceManager:
    """Менеджер ресурсов - Singleton для загрузки и управления игровыми ресурсами"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.resources = {}
            self.resource_paths = {}
            self.loaded_resources = {}
            self.initialized = True
            print("Менеджер ресурсов инициализирован")

    def register_resource_path(self, resource_type, path):
        """Зарегистрировать путь к ресурсам определенного типа"""
        self.resource_paths[resource_type] = path

    def load_resource(self, resource_name, resource_type):
        """Загрузить ресурс, если он еще не загружен"""
        resource_key = f"{resource_type}:{resource_name}"
        
        if resource_key in self.loaded_resources:
            print(f"Ресурс {resource_key} уже загружен, возвращаем из кэша")
            return self.loaded_resources[resource_key]
        
        # В реальной игре здесь была бы фактическая загрузка файла
        # Для примера создадим фиктивный ресурс
        resource_path = self.resource_paths.get(resource_type, "")
        full_path = os.path.join(resource_path, resource_name)
        
        # Имитация загрузки ресурса
        resource_data = {
            "name": resource_name,
            "type": resource_type,
            "path": full_path,
            "loaded_at": str(datetime.now()),
            "size": 1024 # условный размер
        }
        
        self.loaded_resources[resource_key] = resource_data
        print(f"Загружен ресурс: {resource_key}")
        return resource_data

    def get_loaded_resources_count(self):
        """Получить количество загруженных ресурсов"""
        return len(self.loaded_resources)

    def clear_cache(self):
        """Очистить кэш загруженных ресурсов"""
        self.loaded_resources.clear()
        print("Кэш ресурсов очищен")


class AudioManager:
    """Менеджер аудио - Singleton для управления звуком в игре"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.music_volume = 0.8
            self.sfx_volume = 1.0
            self.current_music = None
            self.playing_sounds = []
            self.audio_enabled = True
            self.initialized = True
            print("Менеджер аудио инициализирован")

    def play_sound(self, sound_name):
        """Воспроизвести звуковой эффект"""
        if not self.audio_enabled:
            print("Аудио отключено, звук не воспроизводится")
            return False
            
        if self.sfx_volume > 0:
            print(f"Воспроизводится звук: {sound_name} (громкость: {self.sfx_volume})")
            self.playing_sounds.append(sound_name)
            return True
        else:
            print(f"Звук {sound_name} не воспроизводится - SFX выключен")
            return False

    def play_music(self, music_name):
        """Воспроизвести музыку"""
        if not self.audio_enabled:
            print("Аудио отключено, музыка не воспроизводится")
            return False
            
        if self.music_volume > 0:
            if self.current_music:
                print(f"Останавливается музыка: {self.current_music}")
            self.current_music = music_name
            print(f"Воспроизводится музыка: {music_name} (громкость: {self.music_volume})")
            return True
        else:
            print(f"Музыка {music_name} не воспроизводится - музыка выключена")
            return False

    def stop_music(self):
        """Остановить текущую музыку"""
        if self.current_music:
            print(f"Музыка остановлена: {self.current_music}")
            self.current_music = None

    def set_music_volume(self, volume):
        """Установить громкость музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
        print(f"Громкость музыки установлена: {self.music_volume}")

    def set_sfx_volume(self, volume):
        """Установить громкость звуковых эффектов"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        print(f"Громкость SFX установлена: {self.sfx_volume}")

    def toggle_audio(self):
        """Включить/выключить аудио"""
        self.audio_enabled = not self.audio_enabled
        status = "включено" if self.audio_enabled else "отключено"
        print(f"Аудио {status}")


class SaveManager:
    """Менеджер сохранений - Singleton для управления сохранением и загрузкой игры"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.save_directory = "saves"
            self.save_slots = 3
            self.autosave_enabled = True
            self.last_save_time = None
            self.initialized = True
            print("Менеджер сохранений инициализирован")

    def save_game(self, slot, game_data):
        """Сохранить игру в указанный слот"""
        if 0 <= slot < self.save_slots:
            # Создаем директорию для сохранений, если её нет
            os.makedirs(self.save_directory, exist_ok=True)
            
            save_filename = os.path.join(self.save_directory, f"save_{slot}.json")
            
            save_data = {
                "timestamp": str(datetime.now()),
                "slot": slot,
                "game_data": game_data
            }
            
            with open(save_filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.last_save_time = datetime.now()
            print(f"Игра сохранена в слот {slot}")
            return True
        else:
            print(f"Неверный номер слота: {slot}. Допустимые значения: 0-{self.save_slots-1}")
            return False

    def load_game(self, slot):
        """Загрузить игру из указанного слота"""
        if 0 <= slot < self.save_slots:
            save_filename = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_filename):
                with open(save_filename, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                
                print(f"Игра загружена из слота {slot}")
                return save_data["game_data"]
            else:
                print(f"Слот {slot} пустой или файл не существует")
                return None
        else:
            print(f"Неверный номер слота: {slot}. Допустимые значения: 0-{self.save_slots-1}")
            return None

    def delete_save(self, slot):
        """Удалить сохранение из указанного слота"""
        if 0 <= slot < self.save_slots:
            save_filename = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_filename):
                os.remove(save_filename)
                print(f"Сохранение в слоте {slot} удалено")
                return True
            else:
                print(f"Слот {slot} пустой или файл не существует")
                return False
        else:
            print(f"Неверный номер слота: {slot}. Допустимые значения: 0-{self.save_slots-1}")
            return False

    def get_save_info(self, slot):
        """Получить информацию о сохранении"""
        if 0 <= slot < self.save_slots:
            save_filename = os.path.join(self.save_directory, f"save_{slot}.json")
            
            if os.path.exists(save_filename):
                with open(save_filename, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                
                return {
                    "exists": True,
                    "timestamp": save_data["timestamp"],
                    "slot": slot
                }
            else:
                return {
                    "exists": False,
                    "timestamp": None,
                    "slot": slot
                }
        else:
            print(f"Неверный номер слота: {slot}. Допустимые значения: 0-{self.save_slots-1}")
            return None


class GameManager:
    """Главный менеджер игры - использует другие singleton-менеджеры"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.game_state = "menu"  # menu, playing, paused, game_over
            self.current_level = 1
            self.player_score = 0
            self.paused = False
            self.initialized = True
            
            # Используем другие singleton-менеджеры
            self.resource_manager = ResourceManager()
            self.audio_manager = AudioManager()
            self.save_manager = SaveManager()
            
            print("Менеджер игры инициализирован")

    def start_new_game(self):
        """Начать новую игру"""
        self.game_state = "playing"
        self.current_level = 1
        self.player_score = 0
        self.audio_manager.play_music("main_theme")
        print("Новая игра началась")

    def pause_game(self):
        """Приостановить игру"""
        self.paused = True
        self.game_state = "paused"
        self.audio_manager.play_sound("pause_sound")
        print("Игра приостановлена")

    def resume_game(self):
        """Возобновить игру"""
        self.paused = False
        self.game_state = "playing"
        print("Игра возобновлена")

    def end_game(self):
        """Завершить игру"""
        self.game_state = "game_over"
        self.audio_manager.stop_music()
        print("Игра завершена")

    def get_game_status(self):
        """Получить статус игры"""
        return {
            "state": self.game_state,
            "level": self.current_level,
            "score": self.player_score,
            "paused": self.paused
        }


# Пример использования Singleton-менеджеров
print("=== Демонстрация Singleton в игровых менеджерах ===")

# Создание экземпляров менеджеров
game_manager1 = GameManager()
game_manager2 = GameManager()

# Проверка, что это один и тот же объект
print(f"GameManager - одинаковые экземпляры: {game_manager1 is game_manager2}")

# Создание экземпляров других менеджеров
resource_manager1 = ResourceManager()
resource_manager2 = ResourceManager()
audio_manager1 = AudioManager()
audio_manager2 = AudioManager()
save_manager1 = SaveManager()
save_manager2 = SaveManager()

print(f"ResourceManager - одинаковые экземпляры: {resource_manager1 is resource_manager2}")
print(f"AudioManager - одинаковые экземпляры: {audio_manager1 is audio_manager2}")
print(f"SaveManager - одинаковые экземпляры: {save_manager1 is save_manager2}")

# Работа с игровыми менеджерами
print(f"\n--- Работа с менеджерами ---")

# Регистрация путей к ресурсам
resource_manager1.register_resource_path("textures", "./assets/textures")
resource_manager1.register_resource_path("sounds", "./assets/sounds")
resource_manager1.register_resource_path("models", "./assets/models")

# Загрузка ресурсов
texture1 = resource_manager1.load_resource("player.png", "textures")
sound1 = resource_manager1.load_resource("jump.wav", "sounds")

print(f"Загружено ресурсов: {resource_manager1.get_loaded_resources_count()}")

# Работа с аудио
audio_manager1.play_sound("jump.wav")
audio_manager1.play_music("battle_theme.mp3")
audio_manager1.set_music_volume(0.5)

# Работа с сохранениями
game_data = {
    "level": 3,
    "score": 1500,
    "player_position": {"x": 100, "y": 200},
    "inventory": ["key", "potion", "sword"]
}

save_manager1.save_game(0, game_data)
loaded_data = save_manager1.load_game(0)
if loaded_data:
    print(f"Загружены данные уровня: {loaded_data['level']}")

# Работа с главным менеджером игры
game_manager1.start_new_game()
print(f"Статус игры: {game_manager1.get_game_status()}")

game_manager1.pause_game()
print(f"Статус игры после паузы: {game_manager1.get_game_status()}")

game_manager1.resume_game()
game_manager1.current_level = 2
game_manager1.player_score = 500
print(f"Статус игры после прогресса: {game_manager1.get_game_status()}")