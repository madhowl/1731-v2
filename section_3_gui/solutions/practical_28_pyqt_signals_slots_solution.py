#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 28: PyQt6 - сигналы и слоты
Решение задач по механизму сигналов и слотов в PyQt6

Автор: AI Assistant
"""

# Используем PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit,
    QCheckBox, QRadioButton, QComboBox, QSlider, QSpinBox,
    QFrame, QDialog, QDialogButtonBox, QProgressBar
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer, QPoint, PYQT_VERSION, QThread
from PyQt6.QtGui import QFont, QColor, QPainter, QPen


# ==============================================================================
# ЗАДАЧА 1: Основы сигналов и слотов
# ==============================================================================

class SignalSlotBasicsDemo(QMainWindow):
    """Демонстрация основ сигналов и слотов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 1: Основы сигналов и слотов")
        self.setGeometry(100, 100, 500, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Основы сигналов и слотов")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Простое соединение
        layout.addWidget(QLabel("1. Простое соединение:"))
        
        self.btn_simple = QPushButton("Нажми меня")
        self.btn_simple.clicked.connect(self.on_simple_click)
        layout.addWidget(self.btn_simple)
        
        self.simple_label = QLabel("-")
        layout.addWidget(self.simple_label)
        
        # Лямбда-функции
        layout.addWidget(QLabel("\n2. Лямбда-функции:"))
        
        lambda_btn = QPushButton("Умножить на 2")
        lambda_btn.clicked.connect(lambda checked, x=5: self.on_lambda_click(x))
        layout.addWidget(lambda_btn)
        
        # Отключение сигнала
        layout.addWidget(QLabel("\n3. Блокировка сигнала:"))
        
        self.toggle_btn = QPushButton("Переключатель (активен)")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.toggled.connect(self.on_toggle)
        layout.addWidget(self.toggle_btn)
        
        self.toggle_label = QLabel("Включено")
        layout.addWidget(self.toggle_label)
        
        # Несколько слотов
        layout.addWidget(QLabel("\n4. Несколько слотов:"))
        
        multi_btn = QPushButton("Несколько действий")
        multi_btn.clicked.connect(self.on_multi_1)
        multi_btn.clicked.connect(self.on_multi_2)
        multi_btn.clicked.connect(self.on_multi_3)
        layout.addWidget(multi_btn)
        
        self.multi_output = QTextEdit()
        self.multi_output.setMaximumHeight(80)
        self.multi_output.setReadOnly(True)
        layout.addWidget(self.multi_output)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def on_simple_click(self):
        """Простой обработчик"""
        self.simple_label.setText("Кнопка нажата!")
    
    def on_lambda_click(self, value):
        """Лямбда-функция"""
        result = value * 2
        self.simple_label.setText(f"5 x 2 = {result}")
    
    def on_toggle(self, checked):
        """Обработчик переключателя"""
        if checked:
            self.toggle_label.setText("Включено")
        else:
            self.toggle_label.setText("Выключено")
    
    def on_multi_1(self):
        """Первый слот"""
        self.multi_output.append("Действие 1 выполнено")
    
    def on_multi_2(self):
        """Второй слот"""
        self.multi_output.append("Действие 2 выполнено")
    
    def on_multi_3(self):
        """Третий слот"""
        self.multi_output.append("Действие 3 выполнено")


# ==============================================================================
# ЗАДАЧА 2: Собственные сигналы
# ==============================================================================

class DataProcessor(QObject):
    """Класс с пользовательскими сигналами"""
    
    # Сигналы
    started = pyqtSignal()
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str, int)
    data_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.data = {}
    
    def process(self, data):
        """Обработка данных"""
        self.started.emit()
        
        total = len(data)
        
        for i, (key, value) in enumerate(data.items()):
            # Имитация обработки
            import time
            time.sleep(0.2)
            
            self.data[key] = value.upper()  # Преобразование
            progress = int((i + 1) / total * 100)
            self.progress.emit(progress)
            
            # Эмитим сигнал с данными
            self.data_changed.emit(self.data)
        
        self.finished.emit("Обработка завершена!")
    
    def trigger_error(self, message, code):
        """Генерация ошибки"""
        self.error.emit(message, code)


class WorkerThread(QThread):
    """Рабочий поток для безопасной обработки данных с сигналами"""
    
    started = pyqtSignal()
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str, int)
    data_changed = pyqtSignal(dict)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.result = {}
    
    def run(self):
        """Выполнение в отдельном потоке"""
        self.started.emit()
        
        total = len(self.data)
        
        for i, (key, value) in enumerate(self.data.items()):
            # Имитация обработки
            import time
            time.sleep(0.2)
            
            self.result[key] = value.upper()  # Преобразование
            progress = int((i + 1) / total * 100)
            self.progress.emit(progress)
            
            # Эмитим сигнал с данными
            self.data_changed.emit(self.result)
        
        self.finished.emit("Обработка завершена!")


class CustomSignalsDemo(QMainWindow):
    """Демонстрация пользовательских сигналов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 2: Собственные сигналы")
        self.setGeometry(100, 100, 500, 450)
        
        self.processor = DataProcessor()
        
        # Подключение сигналов
        self.processor.started.connect(self.on_started)
        self.processor.progress.connect(self.on_progress)
        self.processor.finished.connect(self.on_finished)
        self.processor.error.connect(self.on_error)
        self.processor.data_changed.connect(self.on_data_changed)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Пользовательские сигналы")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Прогресс
        layout.addWidget(QLabel("Прогресс:"))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel("Готов")
        layout.addWidget(self.status_label)
        
        # Обработанные данные
        layout.addWidget(QLabel("Обработанные данные:"))
        
        self.data_output = QTextEdit()
        self.data_output.setReadOnly(True)
        layout.addWidget(self.data_output)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        start_btn = QPushButton("Начать обработку")
        start_btn.clicked.connect(self.start_processing)
        btn_layout.addWidget(start_btn)
        
        error_btn = QPushButton("Симулировать ошибку")
        error_btn.clicked.connect(self.trigger_error)
        btn_layout.addWidget(error_btn)
        
        layout.addLayout(btn_layout)
        
        central.setLayout(layout)
    
    def start_processing(self):
        """Запуск обработки данных в отдельном потоке"""
        data = {
            "item1": "первый",
            "item2": "второй",
            "item3": "третий",
            "item4": "четвертый",
            "item5": "пятый"
        }
        
        # Используем QThread для безопасной работы с сигналами
        self.worker = WorkerThread(data)
        self.worker.started.connect(self.on_started)
        self.worker.progress.connect(self.on_progress)
        self.worker.data_changed.connect(self.on_data_changed)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
    
    def trigger_error(self):
        """Генерация ошибки"""
        self.processor.trigger_error("Тестовая ошибка", 404)
    
    def on_started(self):
        """Обработчик начала"""
        self.status_label.setText("Начало обработки...")
        self.data_output.clear()
    
    def on_progress(self, value):
        """Обработчик прогресса"""
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Прогресс: {value}%")
    
    def on_finished(self, message):
        """Обработчик завершения"""
        self.status_label.setText(message)
        self.progress_bar.setValue(100)
    
    def on_error(self, message, code):
        """Обработчик ошибки"""
        self.status_label.setText(f"Ошибка: {message} (код {code})")
    
    def on_data_changed(self, data):
        """Обработчик изменения данных"""
        self.data_output.clear()
        for key, value in data.items():
            self.data_output.append(f"{key}: {value}")


# ==============================================================================
# ЗАДАЧА 3: Сложные соединения
# ==============================================================================

class ComplexConnectionsDemo(QMainWindow):
    """Демонстрация сложных соединений"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 3: Сложные соединения")
        self.setGeometry(100, 100, 500, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Сложные соединения")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Несколько слотов
        layout.addWidget(QLabel("1. Несколько слотов к одному сигналу:"))
        
        multi_btn = QPushButton("Три обработчика")
        multi_btn.clicked.connect(self.handler_a)
        multi_btn.clicked.connect(self.handler_b)
        multi_btn.clicked.connect(self.handler_c)
        layout.addWidget(multi_btn)
        
        self.multi_log = QTextEdit()
        self.multi_log.setMaximumHeight(60)
        self.multi_log.setReadOnly(True)
        layout.addWidget(self.multi_log)
        
        # Отключение сигнала
        layout.addWidget(QLabel("\n2. Отключение сигнала:"))
        
        self.connect_btn = QPushButton("Переключить сигнал")
        self.connect_btn.setCheckable(True)
        self.connect_btn.setChecked(True)
        self.connect_btn.toggled.connect(self.on_toggle_signal)
        layout.addWidget(self.connect_btn)
        
        self.signal_label = QLabel("Сигнал подключен")
        layout.addWidget(self.signal_label)
        
        # Блокировка
        layout.addWidget(QLabel("\n3. Блокировка виджета:"))
        
        blocked_btn = QPushButton("Заблокировать")
        blocked_btn.clicked.connect(self.toggle_block)
        layout.addWidget(blocked_btn)
        
        self.blocked_btn2 = QPushButton("Кнопка для блокировки")
        self.blocked_btn2.clicked.connect(lambda: self.signal_label.setText("Нажата!"))
        layout.addWidget(self.blocked_btn2)
        
        self.block_label = QLabel("Разблокирована")
        layout.addWidget(self.block_label)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def handler_a(self):
        """Обработчик A"""
        self.multi_log.append("A: Обработчик A выполнен")
    
    def handler_b(self):
        """Обработчик B"""
        self.multi_log.append("B: Обработчик B выполнен")
    
    def handler_c(self):
        """Обработчик C"""
        self.multi_log.append("C: Обработчик C выполнен")
    
    def on_toggle_signal(self, checked):
        """Переключение сигнала"""
        if checked:
            self.connect_btn.clicked.connect(self.on_click)
            self.signal_label.setText("Сигнал подключен")
        else:
            try:
                self.connect_btn.clicked.disconnect(self.on_click)
            except TypeError:
                pass
            self.signal_label.setText("Сигнал отключен")
    
    def on_click(self):
        """Обработчик клика"""
        self.signal_label.setText("Клик!")
    
    def toggle_block(self):
        """Переключение блокировки"""
        is_blocked = self.blocked_btn2.isEnabled()
        
        if is_blocked:
            self.blocked_btn2.setEnabled(False)
            self.block_label.setText("Заблокирована")
        else:
            self.blocked_btn2.setEnabled(True)
            self.block_label.setText("Разблокирована")


# ==============================================================================
# ЗАДАЧА 4: События мыши и клавиатуры
# ==============================================================================

class EventDemoWidget(QWidget):
    """Виджет для обработки событий"""
    
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.click_count = 0
        self.last_click_pos = QPoint()
    
    def mousePressEvent(self, event):
        """Обработка нажатия кнопки мыши"""
        self.click_count += 1
        self.last_click_pos = event.pos()
        
        buttons = []
        if event.button() == Qt.MouseButton.LeftButton:
            buttons.append("Левая")
        if event.button() == Qt.MouseButton.RightButton:
            buttons.append("Правая")
        if event.button() == Qt.MouseButton.MiddleButton:
            buttons.append("Средняя")
        
        print(f"MousePress: {', '.join(buttons)} кнопка, позиция ({event.position().x()}, {event.position().y()})")
        self.update()
    
    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши"""
        print(f"MouseRelease: позиция ({event.position().x()}, {event.position().y()})")
        self.update()
    
    def mouseMoveEvent(self, event):
        """Обработка движения мыши"""
        #print(f"MouseMove: ({event.position().x()}, {event.position().y()})")
        self.update()
    
    def keyPressEvent(self, event):
        """Обработка нажатия клавиши"""
        key_text = event.text()
        key_code = event.key()
        
        modifiers = []
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            modifiers.append("Ctrl")
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            modifiers.append("Shift")
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            modifiers.append("Alt")
        
        mod_str = "+".join(modifiers) if modifiers else ""
        
        print(f"KeyPress: key={key_text}, code={key_code}, modifiers={mod_str}")
        self.update()
    
    def keyReleaseEvent(self, event):
        """Обработка отпускания клавиши"""
        print(f"KeyRelease: {event.text()}")
        self.update()
    
    def paintEvent(self, event):
        """Перерисовка виджета"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(240, 240, 240))
        
        # Отображение кликов
        if self.click_count > 0:
            painter.setPen(QPen(QColor(0, 0, 255), 2))
            painter.drawText(10, 20, f"Кликов: {self.click_count}")
            painter.drawText(10, 40, f"Последний клик: ({self.last_click_pos.x()}, {self.last_click_pos.y()})")
        
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawText(10, self.height() - 20, "Кликните мышью или нажмите клавишу")


class EventDemo(QMainWindow):
    """Демонстрация событий"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 4: События мыши и клавиатуры")
        self.setGeometry(100, 100, 600, 500)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Обработка событий мыши и клавиатуры")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Кликните в области ниже и нажмите клавиши:"))
        
        # Кастомный виджет для событий
        self.event_widget = EventDemoWidget()
        self.event_widget.setMinimumHeight(200)
        layout.addWidget(self.event_widget)
        
        # Лог событий
        layout.addWidget(QLabel("Лог (смотрите консоль):"))
        
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(100)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        central.setLayout(layout)


# ==============================================================================
# ЗАДАЧА 5: События окна
# ==============================================================================

class WindowEventDemo(QMainWindow):
    """Демонстрация событий окна"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 5: События окна")
        self.setGeometry(100, 100, 500, 400)
        
        self.create_ui()
        
        # Таймер для обновления позиции
        self.pos_timer = QTimer()
        self.pos_timer.timeout.connect(self.update_position)
        self.pos_timer.start(100)
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("События окна")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Информация о событиях
        layout.addWidget(QLabel("События:"))
        
        self.events_log = QTextEdit()
        self.events_log.setReadOnly(True)
        layout.addWidget(self.events_log)
        
        # Текущее состояние
        self.state_label = QLabel("Готов")
        layout.addWidget(self.state_label)
        
        # Размер и позиция
        self.pos_label = QLabel("Позиция: -")
        layout.addWidget(self.pos_label)
        
        self.size_label = QLabel("Размер: -")
        layout.addWidget(self.size_label)
        
        central.setLayout(layout)
        
        self.log_event("Окно создано")
    
    def log_event(self, event):
        """Логирование события"""
        self.events_log.append(event)
        self.state_label.setText(event)
    
    def update_position(self):
        """Обновление позиции"""
        pos = self.pos()
        size = self.size()
        self.pos_label.setText(f"Позиция: ({pos.x()}, {pos.y()})")
        self.size_label.setText(f"Размер: {size.width()} x {size.height()}")
    
    def showEvent(self, event):
        """Событие показа окна"""
        self.log_event("Окно показано (showEvent)")
        super().showEvent(event)
    
    def closeEvent(self, event):
        """Событие закрытия окна"""
        self.log_event("Закрытие окна (closeEvent)")
        
        # Запрос подтверждения
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 'Подтверждение',
            "Вы уверены, что хотите закрыть?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
    
    def resizeEvent(self, event):
        """Событие изменения размера"""
        size = event.size()
        self.log_event(f"Изменен размер: {size.width()} x {size.height()}")
        super().resizeEvent(event)
    
    def moveEvent(self, event):
        """Событие перемещения"""
        pos = event.pos()
        self.log_event(f"Перемещено: ({pos.x()}, {pos.y()})")
        super().moveEvent(event)
    
    def focusInEvent(self, event):
        """Событие получения фокуса"""
        self.log_event("Получен фокус")
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        """Событие потери фокуса"""
        self.log_event("Потерян фокус")
        super().focusOutEvent(event)


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self):
        self.app = QApplication([])
        
        # Список для хранения ссылок на открытые окна
        self.windows = []
        
        self.tasks = [
            ("Задача 1: Основы сигналов и слотов", self.open_task1),
            ("Задача 2: Собственные сигналы", self.open_task2),
            ("Задача 3: Сложные соединения", self.open_task3),
            ("Задача 4: События мыши и клавиатуры", self.open_task4),
            ("Задача 5: События окна", self.open_task5),
        ]
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = SignalSlotBasicsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task2(self):
        """Открыть задачу 2"""
        window = CustomSignalsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task3(self):
        """Открыть задачу 3"""
        window = ComplexConnectionsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = EventDemo()
        self.windows.append(window)
        window.show()
    
    def open_task5(self):
        """Открыть задачу 5"""
        window = WindowEventDemo()
        self.windows.append(window)
        window.show()
    
    def run(self):
        """Запуск приложения"""
        if PYQT_VERSION == 0:
            print("PyQt не установлен.")
            return
        
        # Главное окно
        main_window = QMainWindow()
        main_window.setWindowTitle("Практическое занятие 28: PyQt - сигналы и слоты")
        main_window.setGeometry(100, 100, 400, 350)
        
        layout = QVBoxLayout()
        
        title = QLabel("Выберите задачу:")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        title.setFont(font)
        layout.addWidget(title)
        
        for text, handler in self.tasks:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
        
        exit_btn = QPushButton("Выход")
        exit_btn.clicked.connect(main_window.close)
        layout.addWidget(exit_btn)
        
        layout.addStretch()
        
        central = QWidget()
        central.setLayout(layout)
        main_window.setCentralWidget(central)
        
        main_window.show()
        
        self.app.exec()


def main():
    """Точка входа"""
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()
