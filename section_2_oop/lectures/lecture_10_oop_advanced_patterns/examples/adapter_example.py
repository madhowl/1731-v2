"""
Пример: Паттерн Adapter в игровых персонажах
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class GameInputInterface(ABC):
    """Целевой интерфейс для игрового ввода"""
    @abstractmethod
    def get_move_direction(self) -> tuple:
        """Получить направление движения (x, y)"""
        pass

    @abstractmethod
    def get_action_pressed(self) -> str:
        """Получить нажатое действие"""
        pass

    @abstractmethod
    def get_mouse_position(self) -> tuple:
        """Получить позицию мыши (x, y)"""
        pass

class LegacyInputSystem:
    """Старая система ввода с несовместимым интерфейсом"""
    def __init__(self):
        self.key_states = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'attack': False, 'jump': False, 'special': False
        }
        self.mouse_x = 0
        self.mouse_y = 0

    def update_keys(self, key_events: List[tuple]):
        """Обновить состояния клавиш"""
        for key, pressed in key_events:
            if key in self.key_states:
                self.key_states[key] = pressed

    def get_key_state(self, key: str) -> bool:
        """Получить состояние клавиши"""
        return self.key_states.get(key, False)

    def set_mouse_position(self, x: int, y: int):
        """Установить позицию мыши"""
        self.mouse_x = x
        self.mouse_y = y

    def get_mouse_coords(self) -> tuple:
        """Получить координаты мыши"""
        return (self.mouse_x, self.mouse_y)

class ModernControlSystem:
    """Современная система управления с несовместимым интерфейсом"""
    def __init__(self):
        self.input_data = {
            'movement_vector': (0, 0),
            'actions': [],
            'cursor_position': (0, 0)
        }

    def process_input(self, raw_input: Dict[str, Any]):
        """Обработать необработанный ввод"""
        movement = raw_input.get('movement', (0, 0))
        actions = raw_input.get('actions', [])
        cursor = raw_input.get('cursor', (0, 0))

        self.input_data['movement_vector'] = movement
        self.input_data['actions'] = actions
        self.input_data['cursor_position'] = cursor

    def get_movement_vector(self) -> tuple:
        """Получить вектор движения"""
        return self.input_data['movement_vector']

    def get_active_actions(self) -> List[str]:
        """Получить активные действия"""
        return self.input_data['actions'].copy()

    def get_cursor_position(self) -> tuple:
        """Получить позицию курсора"""
        return self.input_data['cursor_position']

class InputAdapter(GameInputInterface):
    """Адаптер для старой системы ввода к новому интерфейсу"""
    def __init__(self, legacy_input: LegacyInputSystem):
        self.legacy_input = legacy_input

    def get_move_direction(self) -> tuple:
        """Адаптируем старый интерфейс к новому"""
        x, y = 0, 0
        if self.legacy_input.get_key_state('up'):
            y -= 1
        if self.legacy_input.get_key_state('down'):
            y += 1
        if self.legacy_input.get_key_state('left'):
            x -= 1
        if self.legacy_input.get_key_state('right'):
            x += 1
        return (x, y)

    def get_action_pressed(self) -> str:
        """Адаптируем старый интерфейс к новому"""
        if self.legacy_input.get_key_state('attack'):
            return 'attack'
        elif self.legacy_input.get_key_state('jump'):
            return 'jump'
        elif self.legacy_input.get_key_state('special'):
            return 'special'
        return 'none'

    def get_mouse_position(self) -> tuple:
        """Адаптируем старый интерфейс к новому"""
        return self.legacy_input.get_mouse_coords()

class ModernInputAdapter(GameInputInterface):
    """Адаптер для современной системы ввода к стандартному интерфейсу"""
    def __init__(self, modern_input: ModernControlSystem):
        self.modern_input = modern_input

    def get_move_direction(self) -> tuple:
        """Адаптируем современный интерфейс к стандартному"""
        return self.modern_input.get_movement_vector()

    def get_action_pressed(self) -> str:
        """Адаптируем современный интерфейс к стандартному"""
        actions = self.modern_input.get_active_actions()
        return actions[0] if actions else 'none'

    def get_mouse_position(self) -> tuple:
        """Адаптируем современный интерфейс к стандартному"""
        return self.modern_input.get_cursor_position()

class GameCharacter:
    """Игровой персонаж, использующий стандартный интерфейс ввода"""
    def __init__(self, name: str, input_interface: GameInputInterface):
        self.name = name
        self.x, self.y = 0, 0  # Позиция персонажа
        self.input_interface = input_interface

    def update(self):
        """Обновить состояние персонажа на основе ввода"""
        # Получаем ввод через стандартный интерфейс
        move_dir = self.input_interface.get_move_direction()
        action = self.input_interface.get_action_pressed()
        mouse_pos = self.input_interface.get_mouse_position()

        # Обновляем позицию
        self.x += move_dir[0]
        self.y += move_dir[1]

        # Выполняем действия
        if action != 'none':
            print(f"{self.name} выполняет действие: {action}")

        # Печатаем текущее состояние
        print(f"{self.name} на позиции ({self.x}, {self.y}), мышь на ({mouse_pos[0]}, {mouse_pos[1]})")

def demonstrate_adapter_pattern():
    """Демонстрация паттерна Adapter в игровом контексте"""
    print("=== Демонстрация паттерна Adapter в игровом контексте ===\n")

    # Создаем персонажа с адаптером старой системы ввода
    legacy_input = LegacyInputSystem()
    legacy_adapter = InputAdapter(legacy_input)
    character_with_legacy = GameCharacter("Старый_герой", legacy_adapter)

    print("1. Использование старой системы ввода:")
    # Симулируем нажатия клавиш
    legacy_input.update_keys([('up', True), ('right', True)])
    legacy_input.set_mouse_position(100, 200)
    character_with_legacy.update()

    print()

    # Создаем персонажа с адаптером современной системы ввода
    modern_input = ModernControlSystem()
    modern_input.process_input({
        'movement': (1, -1),
        'actions': ['special'],
        'cursor': (150, 250)
    })
    modern_adapter = ModernInputAdapter(modern_input)
    character_with_modern = GameCharacter("Современный_герой", modern_adapter)

    print("2. Использование современной системы ввода:")
    character_with_modern.update()

    print()

    # Демонстрируем, что оба персонажа используют одинаковый интерфейс
    print("3. Оба персонажа используют одинаковый интерфейс ввода:")
    print(f"Старый герой использует: {type(legacy_adapter).__name__}")
    print(f"Современный герой использует: {type(modern_adapter).__name__}")

    # Симулируем обновление обоих персонажей
    legacy_input.update_keys([('attack', True)])
    legacy_input.set_mouse_position(120, 220)
    print("\nОбновление старого героя:")
    character_with_legacy.update()

    modern_input.process_input({
        'movement': (0, 1),
        'actions': ['jump'],
        'cursor': (180, 280)
    })
    print("\nОбновление современного героя:")
    character_with_modern.update()


if __name__ == "__main__":
    demonstrate_adapter_pattern()