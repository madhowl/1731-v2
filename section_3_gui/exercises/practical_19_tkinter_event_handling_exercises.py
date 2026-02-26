# Упражнения для практического занятия 19: Tkinter - обработка событий

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from typing import Dict, Any, List, Callable
import threading


# =============================================================================
# Задание 1: Обработка кликов мыши
# =============================================================================

class MouseEventApp:
    """Приложение для обработки кликов мыши"""
    def __init__(self):
        """
        ЗАДАНИЕ 1.1: Создайте основное окно приложения
        - Создайте окно Tkinter
        - Установите заголовок "Обработка кликов мыши"
        - Установите размер 700x500
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна
        
        # ЗАДАНИЕ 1.2: Создайте Canvas для рисования
        # TODO: Создайте Canvas 680x400 с белым фоном и разместите его
        self.canvas = None
        
        # ЗАДАНИЕ 1.3: Создайте информационную панель
        # TODO: Создайте фрейм для информации
        
        # ЗАДАНИЕ 1.4: Создайте метку для отображения координат
        # TODO: Создайте Label для отображения координат
        self.coord_label = None
        
        # ЗАДАНИЕ 1.5: Создайте кнопку для очистки холста
        # TODO: Создайте кнопку "Очистить" с командой clear_canvas
        
        # ЗАДАНИЕ 1.6: Привяжите события мыши к Canvas
        # TODO: Привяжите <Button-1> (левый клик) к методу left_click
        # TODO: Привяжите <Button-3> (правый клик) к методу right_click
        # TODO: Привяжите <Motion> (движение мыши) к методу mouse_move
        # TODO: Привяжите <Double-Button-1> (двойной клик) к методу double_click
    
    def left_click(self, event):
        """
        ЗАДАНИЕ 1.7: Обработайте левый клик мыши
        - Обновите метку координат
        - Нарисуйте синий круг по клику
        """
        # TODO: Получите координаты x, y из event
        # TODO: Обновите coord_label с координатами
        # TODO: Нарисуйте овал (create_oval) синего цвета радиусом 20
        pass
    
    def right_click(self, event):
        """
        ЗАДАНИЕ 1.8: Обработайте правый клик мыши
        - Обновите метку координат
        - Нарисуйте красный квадрат по клику
        """
        # TODO: Получите координаты x, y из event
        # TODO: Обновите coord_label с координатами
        # TODO: Нарисуйте прямоугольник (create_rectangle) красного цвета размера 25
        pass
    
    def mouse_move(self, event):
        """
        ЗАДАНИЕ 1.9: Обработайте движение мыши
        """
        # TODO: Обновите coord_label с текущими координатами
        pass
    
    def double_click(self, event):
        """
        ЗАДАНИЕ 1.10: Обработайте двойной клик
        """
        # TODO: Вызовите clear_canvas()
        pass
    
    def clear_canvas(self):
        """
        ЗАДАНИЕ 1.11: Очистите холст
        """
        # TODO: Удалите все элементы с canvas (delete("all"))
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 1.12: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# =============================================================================
# Задание 2: Обработка клавиатуры
# =============================================================================

class KeyboardEventApp:
    """Приложение для обработки клавиатуры"""
    def __init__(self):
        """
        ЗАДАНИЕ 2.1: Создайте приложение для обработки клавиатуры
        - Создайте окно с заголовком "Обработка клавиатуры"
        - Установите размер 700x600
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна (700x600)
        
        # ЗАДАНИЕ 2.2: Создайте Canvas для перемещения объекта
        # TODO: Создайте Canvas 680x500 со светло-серым фоном
        self.canvas = None
        
        # ЗАДАНИЕ 2.3: Создайте объект для перемещения
        # TODO: Определите начальные координаты (obj_x=340, obj_y=250)
        # TODO: Определите размер объекта (30)
        # TODO: Создайте прямоугольник на canvas
        self.object = None
        self.obj_x = None
        self.obj_y = None
        self.obj_size = None
        
        # ЗАДАНИЕ 2.4: Создайте информационную панель
        # TODO: Создайте фрейм для информации
        # TODO: Создайте Label для отображения последней нажатой клавиши
        self.key_label = None
        
        # ЗАДАНИЕ 2.5: Создайте инструкции
        # TODO: Создайте Label с инструкциями по управлению
        
        # ЗАДАНИЕ 2.6: Привяжите события клавиатуры
        # TODO: Привяжите <KeyPress> к key_pressed
        # TODO: Привяжите <Control-c> к ctrl_c_pressed
        # TODO: Привяжите <Control-v> к ctrl_v_pressed
        
        # ЗАДАНИЕ 2.7: Установите фокус на окно
        # TODO: Вызовите focus_set() на root
        pass
    
    def key_pressed(self, event):
        """
        ЗАДАНИЕ 2.8: Обработайте нажатие клавиши
        - Обновите метку с названием клавиши
        - Перемещайте объект по стрелкам
        - Изменяйте цвет по R/G/B
        """
        # TODO: Получите keysym из event
        # TODO: Обновите key_label
        # TODO: По стрелкам Left/Right/Upмещайте объ/Down переект (шаг=10)
        # TODO: По R/G/B изменяйте цвет объекта (red/green/blue)
        # TODO: Обновите позицию объекта на canvas
        pass
    
    def ctrl_c_pressed(self, event):
        """
        ЗАДАНИЕ 2.9: Обработайте Ctrl+C
        """
        # TODO: Обновите key_label на "Нажата комбинация: Ctrl+C"
        # TODO: Покажите информационное сообщение о копировании
        # TODO: Верните "break"
        pass
    
    def ctrl_v_pressed(self, event):
        """
        ЗАДАНИЕ 2.10: Обработайте Ctrl+V
        """
        # TODO: Обновите key_label на "Нажата комбинация: Ctrl+V"
        # TODO: Покажите информационное сообщение о вставке
        # TODO: Верните "break"
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 2.11: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# =============================================================================
# Задание 3: Передача данных через события
# =============================================================================

class DataTransferApp:
    """Приложение для передачи данных через события"""
    def __init__(self):
        """
        ЗАДАНИЕ 3.1: Создайте приложение для передачи данных
        - Создайте окно с заголовком "Передача данных через события"
        - Установите размер 700x600
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна (700x600)
        
        # ЗАДАНИЕ 3.2: Создайте основной фрейм
        # TODO: Создайте Frame и разместите его
        
        # ЗАДАНИЕ 3.3: Создайте кнопки с передачей данных
        # TODO: Создайте фрейм-контейнер (LabelFrame)
        # TODO: Создайте словарь button_data
        # TODO: Создайте 6 кнопок с разными цветами через lambda
        
        # ЗАДАНИЕ 3.4: Создайте кнопки с передачей через bind
        # TODO: Создайте фрейм для bind-кнопок
        # TODO: Создайте 3 кнопки и привяжите событие <Button-1>
        
        # ЗАДАНИЕ 3.5: Создайте список с событиями
        # TODO: Создайте фрейм для списка
        # TODO: Создайте Listbox
        # TODO: Добавьте 5 элементов в список
        # TODO: Привяжите событие <<ListboxSelect>>
        
        # ЗАДАНИЕ 3.6: Создайте метку для отображения информации
        # TODO: Создайте Label для отображения информации
        self.info_label = None
        self.listbox = None
    
    def button_clicked(self, color, number):
        """
        ЗАДАНИЕ 3.7: Обработайте нажатие кнопки
        """
        # TODO: Создайте информационное сообщение
        # TODO: Обновите info_label
        # TODO: Выведите в консоль
        pass
    
    def bind_button_clicked(self, event, number):
        """
        ЗАДАНИЕ 3.8: Обработайте нажатие bind-кнопки
        """
        # TODO: Получите виджет из event
        # TODO: Получите текст виджета
        # TODO: Обновите info_label
        pass
    
    def listbox_selected(self, event):
        """
        ЗАДАНИЕ 3.9: Обработайте выбор в списке
        """
        # TODO: Получите текущий выбор (curselection)
        # TODO: Получите значение по индексу
        # TODO: Обновите info_label
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 3.10: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# =============================================================================
# Задание 4: Кастомные события
# =============================================================================

class CustomEventApp:
    """Приложение для демонстрации кастомных событий"""
    def __init__(self):
        """
        ЗАДАНИЕ 4.1: Создайте приложение с кастомными событиями
        - Создайте окно с заголовком "Кастомные события"
        - Установите размер 700x600
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна (700x600)
        
        # ЗАДАНИЕ 4.2: Создайте основной фрейм и Canvas
        # TODO: Создайте Frame и разместите его
        # TODO: Создайте Canvas 680x400 с белым фоном
        self.canvas = None
        
        # ЗАДАНИЕ 4.3: Создайте кнопки для генерации событий
        # TODO: Создайте фрейм для кнопок
        # TODO: Создайте три кнопки для генерации CustomEvent1, CustomEvent2, CustomEvent3
        
        # ЗАДАНИЕ 4.4: Создайте кнопку подписки
        # TODO: Создайте BooleanVar для подписки
        # TODO: Создайте кнопку для переключения подписки
        self.subscription_button = None
        self.subscribed = None
        self._event_data = None
        
        # ЗАДАНИЕ 4.5: Создайте метки и лог
        # TODO: Создайте Label для отображения событий
        # TODO: Создайте Text для логирования
        self.event_label = None
        self.event_log = None
        
        # ЗАДАНИЕ 4.6: Привяжите кастомные события
        # TODO: Привяжите <<CustomEvent1>> к handle_custom_event1
        # TODO: Привяжите <<CustomEvent2>> к handle_custom_event2
        # TODO: Привяжите <<CustomEvent3>> к handle_custom_event3
        
        # ЗАДАНИЕ 4.7: Запланируйте периодическое событие
        # TODO: Вызовите schedule_periodic_event()
        pass
    
    def generate_custom_event(self, event_name, data):
        """
        ЗАДАНИЕ 4.8: Сгенерируйте кастомное событие
        """
        # TODO: Сохраните данные в _event_data
        # TODO: Вызовите event_generate с event_name
        pass
    
    def handle_custom_event1(self, event):
        """
        ЗАДАНИЕ 4.9: Обработайте CustomEvent1
        """
        # TODO: Получите данные из _event_data
        # TODO: Обновите event_label
        # TODO: Вызовите log_event
        pass
    
    def handle_custom_event2(self, event):
        """
        ЗАДАНИЕ 4.10: Обработайте CustomEvent2
        """
        # TODO: Получите данные из _event_data
        # TODO: Обновите event_label
        # TODO: Вызовите log_event
        pass
    
    def handle_custom_event3(self, event):
        """
        ЗАДАНИЕ 4.11: Обработайте CustomEvent3
        """
        # TODO: Получите данные из _event_data
        # TODO: Обновите event_label
        # TODO: Вызовите log_event
        pass
    
    def schedule_periodic_event(self):
        """
        ЗАДАНИЕ 4.12: Запланируйте периодическое событие
        """
        # TODO: Если subscribed, сгенерируйте <<PeriodicEvent>>
        # TODO: Запланируйте следующий вызов через 2000мс (after)
        pass
    
    def toggle_subscription(self):
        """
        ЗАДАНИЕ 4.13: Переключите подписку
        """
        # TODO: Инвертируйте subscribed
        # TODO: Обновите текст кнопки и label
        pass
    
    def log_event(self, event_info):
        """
        ЗАДАНИЕ 4.14: Логируйте событие
        """
        # TODO: Включите редактирование Text
        # TODO: Добавьте событие с временем
        # TODO: Прокрутите в конец
        # TODO: Отключите редактирование
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 4.15: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# =============================================================================
# Задание 5: Комплексное приложение "Рисовалка"
# =============================================================================

class DrawingApp:
    """Комплексное приложение "Рисовалка" с обработкой событий"""
    def __init__(self):
        """
        ЗАДАНИЕ 5.1: Создайте приложение "Рисовалка"
        - Создайте окно с заголовком "Рисовалка"
        - Установите размер 900x700
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна (900x700)
        
        # ЗАДАНИЕ 5.2: Инициализируйте переменные состояния
        # TODO: self.drawing = False
        # TODO: self.current_color = "black"
        # TODO: self.current_tool = "pen"
        # TODO: self.start_x = None
        # TODO: self.start_y = None
        # TODO: self.current_item = None
        
        # ЗАДАНИЕ 5.3: Создайте меню
        # TODO: Вызовите create_menu()
        
        # ЗАДАНИЕ 5.4: Создайте тулбар
        # TODO: Вызовите create_toolbar()
        
        # ЗАДАНИЕ 5.5: Создайте Canvas для рисования
        # TODO: Создайте Canvas 880x600 с белым фоном и курсором cross
        self.canvas = None
        
        # ЗАДАНИЕ 5.6: Привяжите события мыши
        # TODO: Привяжите <ButtonPress-1> к start_draw
        # TODO: Привяжите <B1-Motion> к draw
        # TODO: Привяжите <ButtonRelease-1> к stop_draw
        
        # ЗАДАНИЕ 5.7: Привяжите события клавиатуры
        # TODO: Привяжите <KeyPress> к key_pressed
        
        # ЗАДАНИЕ 5.8: Установите фокус на окно
        # TODO: Вызовите focus_set()
        
        # ЗАДАНИЕ 5.9: Создайте статусную панель
        # TODO: Создайте Label для статуса с текстом о инструменте и цвете
        self.status_label = None
    
    def create_menu(self):
        """
        ЗАДАНИЕ 5.10: Создайте меню приложения
        """
        # TODO: Создайте Menu для root
        # TODO: Создайте меню "Файл" с командами: Сохранить, Загрузить, Очистить, Выход
        pass
    
    def create_toolbar(self):
        """
        ЗАДАНИЕ 5.11: Создайте панель инструментов
        """
        # TODO: Создайте Frame для тулбара
        
        # TODO: Создайте Radiobutton для инструментов: pen, rectangle, circle, eraser
        # TODO: Создайте StringVar для инструмента
        
        # TODO: Создайте кнопки выбора цвета (black, red, green, blue, yellow, purple, orange, pink)
        
        # TODO: Создайте Scale для размера кисти (1-20)
        self.tool_var = None
        self.color_var = None
        self.brush_size = None
    
    def select_tool(self, tool):
        """
        ЗАДАНИЕ 5.12: Выберите инструмент
        """
        # TODO: Установите current_tool
        # TODO: Вызовите update_status()
        pass
    
    def select_color(self, color):
        """
        ЗАДАНИЕ 5.13: Выберите цвет
        """
        # TODO: Установите current_color
        # TODO: Вызовите update_status()
        pass
    
    def change_brush_size(self, size):
        """
        ЗАДАНИЕ 5.14: Измените размер кисти
        """
        # TODO: Вызовите update_status()
        pass
    
    def update_status(self):
        """
        ЗАДАНИЕ 5.15: Обновите статусную информацию
        """
        # TODO: Обновите status_label с информацией об инструменте, цвете и размере
        pass
    
    def start_draw(self, event):
        """
        ЗАДАНИЕ 5.16: Начните рисование
        """
        # TODO: Установите drawing = True
        # TODO: Сохраните start_x и start_y
        # TODO: В зависимости от инструмента создайте соответствующий объект на canvas
        pass
    
    def draw(self, event):
        """
        ЗАДАНИЕ 5.17: Продолжайте рисование
        """
        # TODO: Если drawing и current_item:
        # TODO: Для pen/eraser - добавьте координаты к линии
        # TODO: Для rectangle/circle - обновите размеры фигуры
        pass
    
    def stop_draw(self, event):
        """
        ЗАДАНИЕ 5.18: Закончите рисование
        """
        # TODO: Установите drawing = False
        # TODO: Установите current_item = None
        pass
    
    def key_pressed(self, event):
        """
        ЗАДАНИЕ 5.19: Обработайте нажатие клавиши
        - P/R/C/E - выбор инструмента
        - D - очистка
        - S - сохранение
        - L - загрузка
        """
        # TODO: По key P/R/C/E установите соответствующий инструмент
        # TODO: По D вызовите clear_canvas()
        # TODO: По S вызовите save_image()
        # TODO: По L вызовите load_image()
        pass
    
    def clear_canvas(self):
        """
        ЗАДАНИЕ 5.20: Очистите холст
        """
        # TODO: Удалите все элементы с canvas
        pass
    
    def save_image(self):
        """
        ЗАДАНИЕ 5.21: Сохраните изображение
        """
        # TODO: Покажите информационное сообщение о сохранении
        pass
    
    def load_image(self):
        """
        ЗАДАНИЕ 5.22: Загрузите изображение
        """
        # TODO: Покажите информационное сообщение о загрузке
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 5.23: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# =============================================================================
# Задание 6: Дополнительные примеры событий
# =============================================================================

class AdvancedEventExamples:
    """Дополнительные примеры продвинутого использования событий"""
    def __init__(self):
        """
        ЗАДАНИЕ 6.1: Создайте приложение с дополнительными примерами
        - Создайте окно с заголовком "Дополнительные примеры событий"
        - Установите размер 800x700
        """
        # TODO: Создайте окно Tkinter
        self.root = None
        # TODO: Установите заголовок окна
        # TODO: Установите размер окна (800x700)
        
        # ЗАДАНИЕ 6.2: Создайте Notebook для примеров
        # TODO: Создайте Notebook и разместите его
        self.notebook = None
        
        # ЗАДАНИЕ 6.3: Создайте вкладку для Drag & Drop
        # TODO: Создайте фрейм для вкладки
        # TODO: Добавьте вкладку в Notebook
        # TODO: Вызовите create_drag_drop_example()
        self.drag_drop_frame = None
        
        # ЗАДАНИЕ 6.4: Создайте вкладку для Focus Events
        # TODO: Создайте фрейм для вкладки
        # TODO: Добавьте вкладку в Notebook
        # TODO: Вызовите create_focus_events_example()
        self.focus_frame = None
        
        # ЗАДАНИЕ 6.5: Создайте вкладку для Mouse Wheel
        # TODO: Создайте фрейм для вкладки
        # TODO: Добавьте вкладку в Notebook
        # TODO: Вызовите create_mousewheel_example()
        self.scroll_frame = None
    
    def create_drag_drop_example(self):
        """
        ЗАДАНИЕ 6.6: Создайте пример Drag & Drop
        """
        # TODO: Создайте фрейм-контейнер
        
        # TODO: Создайте Canvas для drag & drop
        
        # TODO: Создайте 6 перетаскиваемых объектов разных цветов
        
        # TODO: Привяжите события <ButtonPress-1>, <B1-Motion>, <ButtonRelease-1> к объектам
        
        # TODO: Создайте инструкции
        self.draggable_objects = None
        pass
    
    def start_drag(self, event, object_id):
        """
        ЗАДАНИЕ 6.7: Начните перетаскивание
        """
        # TODO: Сохраните начальные координаты и ID объекта
        pass
    
    def drag(self, event, object_id):
        """
        ЗАДАНИЕ 6.8: Перетаскивайте объект
        """
        # TODO: Вычислите смещение
        # TODO: Переместите объект на canvas
        # TODO: Обновите координаты
        pass
    
    def stop_drag(self, event, object_id):
        """
        ЗАДАНИЕ 6.9: Завершите перетаскивание
        """
        # TODO: Очистите данные перетаскивания
        pass
    
    def create_focus_events_example(self):
        """
        ЗАДАНИЕ 6.10: Создайте пример событий фокуса
        """
        # TODO: Создайте фрейм-контейнер
        
        # TODO: Создайте 5 полей ввода с привязкой <FocusIn> и <FocusOut>
        
        # TODO: Создайте Label для отображения фокуса
        self.focus_label = None
        pass
    
    def focus_in(self, event, field_num):
        """
        ЗАДАНИЕ 6.11: Обработайте получение фокуса
        """
        # TODO: Обновите focus_label
        # TODO: Измените стиль виджета
        pass
    
    def focus_out(self, event, field_num):
        """
        ЗАДАНИЕ 6.12: Обработайте потерю фокуса
        """
        # TODO: Обновите focus_label
        # TODO: Верните стандартный стиль
        pass
    
    def create_mousewheel_example(self):
        """
        ЗАДАНИЕ 6.13: Создайте пример событий колеса мыши
        """
        # TODO: Создайте фрейм-контейнер
        
        # TODO: Создайте Text с прокруткой
        
        # TODO: Заполните Text большим количеством текста
        
        # TODO: Привяжите <MouseWheel>, <Button-4>, <Button-5>
        
        self.text_widget = None
        pass
    
    def mouse_wheel(self, event):
        """
        ЗАДАНИЕ 6.14: Обработайте колесо мыши (Windows/macOS)
        """
        # TODO: Прокрутите текст в зависимости от event.delta
        # TODO: Верните "break"
        pass
    
    def mouse_wheel_linux_up(self, event):
        """
        ЗАДАНИЕ 6.15: Обработайте колесо мыши вверх (Linux)
        """
        # TODO: Прокрутите текст вверх
        # TODO: Верните "break"
        pass
    
    def mouse_wheel_linux_down(self, event):
        """
        ЗАДАНИЕ 6.16: Обработайте колесо мыши вниз (Linux)
        """
        # TODO: Прокрутите текст вниз
        # TODO: Верните "break"
        pass
    
    def run(self):
        """
        ЗАДАНИЕ 6.17: Запустите главный цикл приложения
        """
        # TODO: Запустите mainloop()
        pass


# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 19 ===")
    
    print("\n1. Задание 1: Обработка кликов мыши")
    # TODO: Раскомментируйте для запуска:
    # mouse_app = MouseEventApp()
    # mouse_app.run()
    
    print("\n2. Задание 2: Обработка клавиатуры")
    # TODO: Раскомментируйте для запуска:
    # keyboard_app = KeyboardEventApp()
    # keyboard_app.run()
    
    print("\n3. Задание 3: Передача данных через события")
    # TODO: Раскомментируйте для запуска:
    # data_app = DataTransferApp()
    # data_app.run()
    
    print("\n4. Задание 4: Кастомные события")
    # TODO: Раскомментируйте для запуска:
    # custom_app = CustomEventApp()
    # custom_app.run()
    
    print("\n5. Задание 5: Комплексное приложение (Рисовалка)")
    # TODO: Раскомментируйте для запуска:
    # drawing_app = DrawingApp()
    # drawing_app.run()
    
    print("\n6. Дополнительные примеры")
    # TODO: Раскомментируйте для запуска:
    # advanced_app = AdvancedEventExamples()
    # advanced_app.run()
    
    print("\nЗапустите одно из приложений для демонстрации")
