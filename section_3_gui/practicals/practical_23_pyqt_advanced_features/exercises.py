# Упражнения для практического занятия 23: PyQt - продвинутые возможности

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                            QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
                            QCheckBox, QRadioButton, QComboBox, QSpinBox, QSlider, 
                            QProgressBar, QTableWidgetItem, QListWidget, QTreeWidget,
                            QTreeWidgetItem, QMessageBox, QTabWidget, QSplitter,
                            QStackedWidget, QGroupBox, QFrame, QScrollArea, QTextEdit,
                            QMenuBar, QStatusBar, QToolBar, QAction, QFileDialog,
                            QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem,
                            QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsTextItem,
                            QOpenGLWidget, QColorDialog, QFontDialog, QSystemTrayIcon,
                            QMenu, QDesktopWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QRectF, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPixmap, QIcon, QBrush, QPen, QLinearGradient, QPolygonF, QCursor
import json
import os
from typing import Dict, Any, List
import threading
import time
import random
from enum import Enum

# Задание 1: Пользовательские виджеты
class CustomWidgetExercise(QWidget):
    """Упражнение для создания пользовательского виджета"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 100)
        self.color = QColor(76, 175, 80)  # Green
        self.text = "Пользовательский виджет"
        self.border_width = 2
        self.counter = 0
        self.radius = 10
    
    def paintEvent(self, event):
        """Событие отрисовки виджета"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Рисуем фон с закругленными углами
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(QColor(0, 0, 0), self.border_width))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), self.radius, self.radius)
        
        # Рисуем текст
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.text}\nКликов: {self.counter}")
    
    def mousePressEvent(self, event):
        """Обработка нажатия мыши"""
        # Меняем цвет при клике
        colors = [QColor(76, 175, 80), QColor(244, 67, 54), QColor(33, 150, 243), 
                 QColor(255, 152, 0), QColor(156, 39, 176)]
        self.color = random.choice(colors)
        self.counter += 1
        self.update()  # Перерисовываем виджет

class CustomProgressWidgetExercise(QWidget):
    """Упражнение для создания анимированного прогресс бара"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 30)
        self.value = 0
        self.animation_step = 0
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)  # Обновление каждые 50мс
        self.bar_height = 20
    
    def paintEvent(self, event):
        """Отрисовка анимированного прогресс бара"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Рисуем фон
        painter.setBrush(QBrush(QColor(240, 240, 240)))
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 5, 5)
        
        # Рисуем прогресс
        progress_width = int(self.width() * self.value / 100)
        progress_rect = QRectF(2, 2, progress_width-4, self.height()-4)
        
        # Создаем градиент для прогресса
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0.0, QColor(76, 175, 80))
        gradient.setColorAt(1.0, QColor(46, 125, 50))
        
        painter.fillRect(progress_rect, QBrush(gradient))
        painter.setPen(QColor(76, 175, 80))
        painter.drawRoundedRect(progress_rect, 5, 5)
        
        # Рисуем анимированный индикатор
        animated_x = (self.animation_step * 20) % self.width()
        animated_rect = QRectF(animated_x, 0, 20, self.height())
        painter.fillRect(animated_rect, QColor(255, 255, 255, 100))
    
    def animate(self):
        """Анимация прогресса"""
        self.animation_step += 1
        self.update()
    
    def set_value(self, value):
        """Установка значения прогресса"""
        self.value = max(0, min(100, value))
        self.update()

class CustomWidgetExerciseApp(QMainWindow):
    """Приложение с пользовательскими виджетами (упражнение)"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 1: Пользовательские виджеты")
        self.setGeometry(100, 100, 700, 500)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        layout = QVBoxLayout()
        
        # Добавляем пользовательский виджет
        self.custom_widget = CustomWidgetExercise()
        layout.addWidget(QLabel("Пользовательский виджет (кликните для изменения цвета и счетчика):"))
        layout.addWidget(self.custom_widget)
        
        # Добавляем анимированный прогресс бар
        self.custom_progress = CustomProgressWidgetExercise()
        layout.addWidget(QLabel("Анимированный пользовательский прогресс бар:"))
        layout.addWidget(self.custom_progress)
        
        # Кнопки управления
        controls_layout = QHBoxLayout()
        
        self.inc_progress_btn = QPushButton("Увеличить прогресс")
        self.inc_progress_btn.clicked.connect(self.increment_progress)
        controls_layout.addWidget(self.inc_progress_btn)
        
        self.dec_progress_btn = QPushButton("Уменьшить прогресс")
        self.dec_progress_btn.clicked.connect(self.decrement_progress)
        controls_layout.addWidget(self.dec_progress_btn)
        
        self.reset_progress_btn = QPushButton("Сбросить прогресс")
        self.reset_progress_btn.clicked.connect(self.reset_progress)
        controls_layout.addWidget(self.reset_progress_btn)
        
        layout.addLayout(controls_layout)
        
        # Кнопка для изменения цвета виджета
        self.change_color_btn = QPushButton("Изменить цвет виджета")
        self.change_color_btn.clicked.connect(self.change_widget_color)
        layout.addWidget(self.change_color_btn)
        
        central_widget.setLayout(layout)
    
    def increment_progress(self):
        """Увеличивает прогресс"""
        current_value = self.custom_progress.value
        self.custom_progress.set_value(current_value + 10)
    
    def decrement_progress(self):
        """Уменьшает прогресс"""
        current_value = self.custom_progress.value
        self.custom_progress.set_value(current_value - 10)
    
    def reset_progress(self):
        """Сбрасывает прогресс"""
        self.custom_progress.set_value(0)
    
    def change_widget_color(self):
        """Изменяет цвет пользовательского виджета"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_widget.color = color
            self.custom_widget.update()

# Задание 2: Работа с графикой
class GraphicsViewExercise(QMainWindow):
    """Упражнение для работы с графикой"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 2: Работа с графикой")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Создаем QGraphicsView
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)
        self.graphics_view.setScene(self.scene)
        
        # Добавляем элементы на сцену
        self.add_graphic_elements()
        
        layout.addWidget(self.graphics_view)
        
        # Кнопки управления
        controls_layout = QHBoxLayout()
        
        self.add_rect_btn = QPushButton("Добавить прямоугольник")
        self.add_rect_btn.clicked.connect(self.add_rectangle)
        controls_layout.addWidget(self.add_rect_btn)
        
        self.add_ellipse_btn = QPushButton("Добавить эллипс")
        self.add_ellipse_btn.clicked.connect(self.add_ellipse)
        controls_layout.addWidget(self.add_ellipse_btn)
        
        self.add_text_btn = QPushButton("Добавить текст")
        self.add_text_btn.clicked.connect(self.add_text_element)
        controls_layout.addWidget(self.add_text_btn)
        
        self.zoom_in_btn = QPushButton("Увеличить")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        controls_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("Уменьшить")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        controls_layout.addWidget(self.zoom_out_btn)
        
        self.clear_scene_btn = QPushButton("Очистить сцену")
        self.clear_scene_btn.clicked.connect(self.clear_scene)
        controls_layout.addWidget(self.clear_scene_btn)
        
        layout.addLayout(controls_layout)
        
        central_widget.setLayout(layout)
    
    def add_graphic_elements(self):
        """Добавляет элементы на сцену"""
        # Добавляем прямоугольники
        for i in range(3):
            rect_item = QGraphicsRectItem(50 + i*100, 50, 80, 60)
            rect_item.setBrush(QBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            rect_item.setFlag(QGraphicsItem.ItemIsMovable)
            rect_item.setFlag(QGraphicsItem.ItemIsSelectable)
            rect_item.setToolTip(f"Прямоугольник {i+1}")
            self.scene.addItem(rect_item)
        
        # Добавляем эллипсы
        for i in range(3):
            ellipse_item = QGraphicsEllipseItem(50, 150 + i*80, 60, 40)
            ellipse_item.setBrush(QBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            ellipse_item.setFlag(QGraphicsItem.ItemIsMovable)
            ellipse_item.setFlag(QGraphicsItem.ItemIsSelectable)
            ellipse_item.setToolTip(f"Эллипс {i+1}")
            self.scene.addItem(ellipse_item)
        
        # Добавляем текстовые элементы
        texts = ["Текст 1", "Текст 2", "Текст 3"]
        for i, text in enumerate(texts):
            text_item = QGraphicsTextItem(text)
            text_item.setPos(300, 50 + i*50)
            text_item.setDefaultTextColor(QColor(255, 0, 0))
            text_item.setTextInteractionFlags(Qt.TextEditable)
            text_item.setToolTip(f"Редактируемый текст {i+1}")
            self.scene.addItem(text_item)
    
    def add_rectangle(self):
        """Добавляет прямоугольник на сцену"""
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        width = random.randint(40, 80)
        height = random.randint(30, 60)
        
        rect_item = QGraphicsRectItem(x, y, width, height)
        rect_item.setBrush(QBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        rect_item.setFlag(QGraphicsItem.ItemIsMovable)
        rect_item.setFlag(QGraphicsItem.ItemIsSelectable)
        rect_item.setToolTip(f"Случайный прямоугольник")
        self.scene.addItem(rect_item)
    
    def add_ellipse(self):
        """Добавляет эллипс на сцену"""
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        width = random.randint(40, 80)
        height = random.randint(30, 60)
        
        ellipse_item = QGraphicsEllipseItem(x, y, width, height)
        ellipse_item.setBrush(QBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        ellipse_item.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse_item.setFlag(QGraphicsItem.ItemIsSelectable)
        ellipse_item.setToolTip(f"Случайный эллипс")
        self.scene.addItem(ellipse_item)
    
    def add_text_element(self):
        """Добавляет текстовый элемент на сцену"""
        x = random.randint(0, 700)
        y = random.randint(0, 500)
        
        text_item = QGraphicsTextItem(f"Текст {len(self.scene.items())}")
        text_item.setPos(x, y)
        text_item.setDefaultTextColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        text_item.setTextInteractionFlags(Qt.TextEditable)
        text_item.setToolTip(f"Редактируемый текст")
        self.scene.addItem(text_item)
    
    def zoom_in(self):
        """Увеличивает масштаб"""
        self.graphics_view.scale(1.2, 1.2)
    
    def zoom_out(self):
        """Уменьшает масштаб"""
        self.graphics_view.scale(0.8, 0.8)
    
    def clear_scene(self):
        """Очищает сцену"""
        self.scene.clear()
        self.add_graphic_elements()

# Задание 3: Многопоточность в GUI
class WorkerThreadExercise(QThread):
    """Рабочий поток для выполнения длительных операций (упражнение)"""
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    result_signal = pyqtSignal(object)
    
    def __init__(self, operation_name, duration, operation_func=None):
        super().__init__()
        self.operation_name = operation_name
        self.duration = duration
        self.operation_func = operation_func or self.default_operation
        self._stop_flag = False
    
    def default_operation(self):
        """Дефолтная длительная операция"""
        result = []
        for i in range(101):
            if self._stop_flag:
                break
            time.sleep(self.duration / 100)  # Имитация работы
            self.progress_signal.emit(i)
            # Добавляем немного данных для демонстрации
            if i % 10 == 0:
                result.append(f"Шаг {i}")
        return result
    
    def stop(self):
        """Останавливает выполнение потока"""
        self._stop_flag = True
    
    def run(self):
        """Выполнение длительной операции в потоке"""
        try:
            result = self.operation_func()
            self.result_signal.emit(result)
            if not self._stop_flag:
                self.finished_signal.emit(f"Операция '{self.operation_name}' завершена")
            else:
                self.finished_signal.emit(f"Операция '{self.operation_name}' была остановлена")
        except Exception as e:
            self.finished_signal.emit(f"Ошибка в потоке: {str(e)}")

class ThreadingExercise(QMainWindow):
    """Упражнение для многопоточности в GUI"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 3: Многопоточность в GUI")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Прогресс бар для отображения прогресса
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(QLabel("Прогресс выполнения:"))
        layout.addWidget(self.progress_bar)
        
        # Текстовое поле для лога
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(QLabel("Лог выполнения:"))
        layout.addWidget(self.log_text)
        
        # Кнопки управления
        controls_layout = QHBoxLayout()
        
        self.start_thread_btn = QPushButton("Запустить операцию в потоке")
        self.start_thread_btn.clicked.connect(self.start_thread_operation)
        controls_layout.addWidget(self.start_thread_btn)
        
        self.stop_thread_btn = QPushButton("Остановить поток")
        self.stop_thread_btn.clicked.connect(self.stop_thread_operation)
        self.stop_thread_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_thread_btn)
        
        self.simulate_long_task_btn = QPushButton("Симуляция длительной задачи")
        self.simulate_long_task_btn.clicked.connect(self.simulate_long_task)
        controls_layout.addWidget(self.simulate_long_task_btn)
        
        layout.addLayout(controls_layout)
        
        central_widget.setLayout(layout)
        
        # Переменные для управления потоком
        self.worker_thread = None
    
    def start_thread_operation(self):
        """Запускает операцию в потоке"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.log_text.append("Поток уже запущен!")
            return
        
        self.log_text.append("Запуск операции в отдельном потоке...")
        
        self.worker_thread = WorkerThreadExercise("Обработка данных", 2.0)  # 2 секунды
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.finished_signal.connect(self.thread_finished)
        self.worker_thread.result_signal.connect(self.thread_result)
        
        self.progress_bar.setValue(0)
        self.start_thread_btn.setEnabled(False)
        self.stop_thread_btn.setEnabled(True)
        self.worker_thread.start()
    
    def update_progress(self, value):
        """Обновляет прогресс бар"""
        self.progress_bar.setValue(value)
    
    def thread_finished(self, message):
        """Обработка завершения потока"""
        self.log_text.append(message)
        self.start_thread_btn.setEnabled(True)
        self.stop_thread_btn.setEnabled(False)
    
    def thread_result(self, result):
        """Обработка результата выполнения потока"""
        self.log_text.append(f"Результат операции: {result}")
    
    def stop_thread_operation(self):
        """Останавливает поток (если возможно)"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.log_text.append("Поток был остановлен")
            self.start_thread_btn.setEnabled(True)
            self.stop_thread_btn.setEnabled(False)
    
    def simulate_long_task(self):
        """Симулирует длительную задачу в отдельном потоке"""
        def long_task():
            for i in range(101):
                time.sleep(0.05)  # Имитация работы
                # Обновляем интерфейс в основном потоке
                self.progress_bar.setValue(i)
                QApplication.processEvents()  # Обрабатываем события интерфейса
            self.log_text.append("Длительная задача завершена")
        
        # Запускаем задачу в отдельном потоке
        task_thread = threading.Thread(target=long_task)
        task_thread.daemon = True
        task_thread.start()

# Задание 4: Анимация и эффекты
class AnimationExercise(QMainWindow):
    """Упражнение для анимации и эффектов"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Анимация и эффекты")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Canvas для анимации
        self.animation_canvas = QLabel()
        self.animation_canvas.setFixedSize(780, 400)
        self.animation_canvas.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.animation_canvas.setAlignment(Qt.AlignCenter)
        self.animation_canvas.setText("Здесь будут анимации")
        layout.addWidget(self.animation_canvas)
        
        # Кнопки управления анимацией
        controls_layout = QHBoxLayout()
        
        self.move_animation_btn = QPushButton("Анимация перемещения")
        self.move_animation_btn.clicked.connect(self.start_move_animation)
        controls_layout.addWidget(self.move_animation_btn)
        
        self.color_animation_btn = QPushButton("Анимация цвета")
        self.color_animation_btn.clicked.connect(self.start_color_animation)
        controls_layout.addWidget(self.color_animation_btn)
        
        self.scale_animation_btn = QPushButton("Анимация масштаба")
        self.scale_animation_btn.clicked.connect(self.start_scale_animation)
        controls_layout.addWidget(self.scale_animation_btn)
        
        self.complex_animation_btn = QPushButton("Комплексная анимация")
        self.complex_animation_btn.clicked.connect(self.start_complex_animation)
        controls_layout.addWidget(self.complex_animation_btn)
        
        layout.addLayout(controls_layout)
        
        # Дополнительные элементы для демонстрации анимации
        self.animated_widget = QLabel("Анимируемый элемент", self.animation_canvas)
        self.animated_widget.setGeometry(100, 100, 150, 50)
        self.animated_widget.setStyleSheet("background-color: blue; color: white; padding: 10px;")
        self.animated_widget.setAlignment(Qt.AlignCenter)
        
        # Используем QTimer для анимации
        self.animation_timer = None
        self.move_direction = 1
        self.color_step = 0
        self.scale_step = 0
        self.initial_size = self.animated_widget.size()
        
        central_widget.setLayout(layout)
    
    def start_move_animation(self):
        """Запускает анимацию перемещения"""
        self.move_step = 0
        self.move_direction = 1
        
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_step_animation)
        self.move_timer.start(20)  # Обновление каждые 20мс
    
    def move_step_animation(self):
        """Шаг анимации перемещения"""
        current_x = self.animated_widget.x()
        current_y = self.animated_widget.y()
        new_x = current_x + 5 * self.move_direction
        
        # Проверяем границы
        if new_x > 600 or new_x < 0:
            self.move_direction *= -1
            new_x = current_x + 5 * self.move_direction
        
        self.animated_widget.move(new_x, current_y)
        self.move_step += 1
        
        if self.move_step > 100:  # Останавливаем через 100 шагов
            self.move_timer.stop()
    
    def start_color_animation(self):
        """Запускает анимацию изменения цвета"""
        self.color_step = 0
        self.colors = [
            QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255),
            QColor(255, 255, 0), QColor(255, 0, 255), QColor(0, 255, 255)
        ]
        
        self.color_timer = QTimer()
        self.color_timer.timeout.connect(self.color_step_animation)
        self.color_timer.start(200)  # Обновление каждые 200мс
    
    def color_step_animation(self):
        """Шаг анимации изменения цвета"""
        color = self.colors[self.color_step % len(self.colors)]
        self.animated_widget.setStyleSheet(f"background-color: {color.name()}; color: white; padding: 10px;")
        self.color_step += 1
        
        if self.color_step > 30:  # Останавливаем через 30 шагов
            self.color_timer.stop()
    
    def start_scale_animation(self):
        """Запускает анимацию масштаба"""
        self.scale_step = 0
        
        self.scale_timer = QTimer()
        self.scale_timer.timeout.connect(self.scale_step_animation)
        self.scale_timer.start(50)  # Обновление каждые 50мс
    
    def scale_step_animation(self):
        """Шаг анимации масштаба"""
        import math
        scale_factor = 0.5 + 0.5 * abs(math.sin(self.scale_step * 0.1))  # Плавное изменение
        new_width = int(self.initial_size.width() * scale_factor)
        new_height = int(self.initial_size.height() * scale_factor)
        
        self.animated_widget.resize(new_width, new_height)
        self.scale_step += 1
        
        if self.scale_step > 100:  # Останавливаем через 100 шагов
            self.scale_timer.stop()
            # Возвращаем исходный размер
            self.animated_widget.resize(self.initial_size.width(), self.initial_size.height())
    
    def start_complex_animation(self):
        """Запускает комплексную анимацию"""
        # Запускаем все анимации одновременно
        self.start_move_animation()
        self.start_color_animation()
        self.start_scale_animation()

# Задание 5: Комплексное приложение "Графический редактор"
class DrawingTool(Enum):
    """Инструменты рисования"""
    PEN = "pen"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ERASER = "eraser"
    LINE = "line"

class GraphicsEditorExercise(QMainWindow):
    """Упражнение для комплексного приложения - графический редактор"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Графический редактор")
        self.setGeometry(100, 100, 1000, 800)
        
        # Переменные состояния
        self.current_tool = DrawingTool.PEN
        self.drawing = False
        self.start_point = None
        self.current_shape = None
        self.shapes = []  # Список всех нарисованных фигур
        self.layers = {"Layer 1": []}  # Словарь слоев
        self.current_layer = "Layer 1"
        
        # Создаем меню
        self.create_menu()
        
        # Создаем тулбар
        self.create_toolbar()
        
        # Создаем центральный виджет с QGraphicsView
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 900, 700)
        self.scene.setBackgroundBrush(QBrush(QColor(255, 255, 255)))
        self.graphics_view.setScene(self.scene)
        
        # Устанавливаем центральный виджет
        self.setCentralWidget(self.graphics_view)
        
        # Привязываем события мыши к сцене
        self.scene.mousePressEvent = self.scene_mouse_press
        self.scene.mouseMoveEvent = self.scene_mouse_move
        self.scene.mouseReleaseEvent = self.scene_mouse_release
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = self.menuBar()
        
        # Меню File
        file_menu = menubar.addMenu("Файл")
        
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)
        
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)
        
        export_action = QAction("Экспортировать", self)
        export_action.triggered.connect(self.export_image)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        clear_action = QAction("Очистить", self)
        clear_action.triggered.connect(self.clear_canvas)
        file_menu.addAction(clear_action)
    
    def create_toolbar(self):
        """Создает тулбар с инструментами"""
        toolbar = self.addToolBar("Инструменты")
        
        # Кнопки инструментов
        pen_action = QAction("Ручка", self)
        pen_action.setCheckable(True)
        pen_action.setChecked(True)
        pen_action.triggered.connect(lambda: self.set_tool(DrawingTool.PEN))
        toolbar.addAction(pen_action)
        
        line_action = QAction("Линия", self)
        line_action.setCheckable(True)
        line_action.triggered.connect(lambda: self.set_tool(DrawingTool.LINE))
        toolbar.addAction(line_action)
        
        rect_action = QAction("Прямоугольник", self)
        rect_action.setCheckable(True)
        rect_action.triggered.connect(lambda: self.set_tool(DrawingTool.RECTANGLE))
        toolbar.addAction(rect_action)
        
        circle_action = QAction("Круг", self)
        circle_action.setCheckable(True)
        circle_action.triggered.connect(lambda: self.set_tool(DrawingTool.CIRCLE))
        toolbar.addAction(circle_action)
        
        eraser_action = QAction("Ластик", self)
        eraser_action.setCheckable(True)
        eraser_action.triggered.connect(lambda: self.set_tool(DrawingTool.ERASER))
        toolbar.addAction(eraser_action)
        
        # Цвет
        toolbar.addSeparator()
        color_label = QLabel("Цвет:")
        toolbar.addWidget(color_label)
        
        self.color_button = QPushButton()
        self.color_button.setFixedSize(30, 30)
        self.color_button.setStyleSheet("background-color: black;")
        self.color_button.clicked.connect(self.choose_color)
        self.current_color = QColor(0, 0, 0)  # Черный по умолчанию
        toolbar.addWidget(self.color_button)
        
        # Размер кисти
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Размер:"))
        
        self.brush_size_spinbox = QSpinBox()
        self.brush_size_spinbox.setRange(1, 50)
        self.brush_size_spinbox.setValue(5)
        self.brush_size_spinbox.valueChanged.connect(self.brush_size_changed)
        self.current_brush_size = 5
        toolbar.addWidget(self.brush_size_spinbox)
    
    def set_tool(self, tool):
        """Устанавливает текущий инструмент"""
        self.current_tool = tool
    
    def choose_color(self):
        """Выбирает цвет для рисования"""
        color = QColorDialog.getColor(self.current_color, self, "Выберите цвет")
        if color.isValid():
            self.current_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
    
    def brush_size_changed(self, value):
        """Обработка изменения размера кисти"""
        self.current_brush_size = value
    
    def scene_mouse_press(self, event):
        """Обработка нажатия мыши на сцене"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = event.scenePos()
            
            if self.current_tool == DrawingTool.PEN:
                # Создаем кисть
                pen = QPen(self.current_color, self.current_brush_size, Qt.SolidLine)
                self.current_shape = self.scene.addLine(
                    self.start_point.x(), self.start_point.y(),
                    self.start_point.x(), self.start_point.y(),
                    pen
                )
            elif self.current_tool == DrawingTool.LINE:
                # Создаем линию
                pen = QPen(self.current_color, self.current_brush_size, Qt.SolidLine)
                self.current_shape = self.scene.addLine(
                    self.start_point.x(), self.start_point.y(),
                    self.start_point.x(), self.start_point.y(),
                    pen
                )
            elif self.current_tool == DrawingTool.RECTANGLE:
                # Создаем прямоугольник
                pen = QPen(self.current_color, self.current_brush_size, Qt.SolidLine)
                brush = QBrush(self.current_color if self.current_tool != DrawingTool.ERASER else QColor(255, 255, 255))
                self.current_shape = self.scene.addRect(
                    QRectF(self.start_point.x(), self.start_point.y(), 0, 0),
                    pen, brush
                )
            elif self.current_tool == DrawingTool.CIRCLE:
                # Создаем эллипс
                pen = QPen(self.current_color, self.current_brush_size, Qt.SolidLine)
                brush = QBrush(self.current_color if self.current_tool != DrawingTool.ERASER else QColor(255, 255, 255))
                self.current_shape = self.scene.addEllipse(
                    QRectF(self.start_point.x(), self.start_point.y(), 0, 0),
                    pen, brush
                )
    
    def scene_mouse_move(self, event):
        """Обработка движения мыши на сцене"""
        if self.drawing and self.current_shape:
            end_point = event.scenePos()
            
            if self.current_tool == DrawingTool.PEN:
                # Продолжаем рисовать линию
                # В реальном приложении мы бы добавляли точки к пути
                pass
            elif self.current_tool in [DrawingTool.LINE, DrawingTool.RECTANGLE, DrawingTool.CIRCLE]:
                # Обновляем размеры фигуры
                rect = QRectF(
                    min(self.start_point.x(), end_point.x()),
                    min(self.start_point.y(), end_point.y()),
                    abs(end_point.x() - self.start_point.x()),
                    abs(end_point.y() - self.start_point.y())
                )
                
                if self.current_tool == DrawingTool.LINE:
                    self.current_shape.setLine(
                        self.start_point.x(), self.start_point.y(),
                        end_point.x(), end_point.y()
                    )
                elif self.current_tool == DrawingTool.RECTANGLE:
                    self.current_shape.setRect(rect)
                elif self.current_tool == DrawingTool.CIRCLE:
                    self.current_shape.setRect(rect)
    
    def scene_mouse_release(self, event):
        """Обработка отпускания мыши на сцене"""
        self.drawing = False
        if self.current_shape:
            # Сохраняем фигуру в список
            self.shapes.append(self.current_shape)
            self.current_shape = None
    
    def save_image(self):
        """Сохраняет изображение"""
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", 
                                                 "Images (*.png *.jpg *.bmp)")
        if filename:
            # В реальном приложении мы бы сохраняли содержимое сцены как изображение
            pixmap = QPixmap(self.scene.sceneRect().size().toSize())
            painter = QPainter(pixmap)
            self.scene.render(painter)
            painter.end()
            pixmap.save(filename)
    
    def load_image(self):
        """Загружает изображение"""
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить изображение", "", 
                                                 "Images (*.png *.jpg *.bmp *.svg)")
        if filename:
            # В реальном приложении мы бы загружали изображение на сцену
            pass
    
    def export_image(self):
        """Экспортирует изображение"""
        self.save_image()
    
    def clear_canvas(self):
        """Очищает холст"""
        self.scene.clear()
        self.shapes = []

# Дополнительные примеры использования продвинутых возможностей PyQt
class AdvancedFeaturesExamples:
    """Дополнительные примеры продвинутых возможностей PyQt"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры продвинутых возможностей Tkinter")
        self.root.geometry("900x800")
        
        # Создаем ноутбук для различных примеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для продвинутых Entry
        self.entry_examples_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entry_examples_frame, text="Продвинутые Entry")
        self.create_advanced_entry_examples()
        
        # Вкладка для Treeview
        self.treeview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.treeview_frame, text="Treeview")
        self.create_treeview_example()
        
        # Вкладка для Progressbar
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="Прогресс бары")
        self.create_progress_examples()
        
        # Вкладка для Canvas
        self.canvas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.canvas_frame, text="Canvas")
        self.create_canvas_example()
    
    def create_advanced_entry_examples(self):
        """Создает примеры продвинутого использования Entry"""
        frame = ttk.LabelFrame(self.entry_examples_frame, text="Продвинутые возможности Entry")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Entry с плейсхолдером
        placeholder_frame = ttk.Frame(frame)
        placeholder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(placeholder_frame, text="Entry с плейсхолдером:").pack(anchor=tk.W)
        self.placeholder_entry = PlaceholderEntry(placeholder_frame, placeholder="Введите текст здесь...")
        self.placeholder_entry.pack(fill=tk.X, pady=5)
        
        # Entry с валидацией
        validation_frame = ttk.Frame(frame)
        validation_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(validation_frame, text="Entry с валидацией (только цифры):").pack(anchor=tk.W)
        vcmd = (self.root.register(self.validate_numeric), '%P')
        self.numeric_entry = ttk.Entry(validation_frame, validate='key', validatecommand=vcmd)
        self.numeric_entry.pack(fill=tk.X, pady=5)
        
        # Entry с маской (например, для телефона)
        mask_frame = ttk.Frame(frame)
        mask_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(mask_frame, text="Entry с маской (телефон):").pack(anchor=tk.W)
        self.phone_entry = MaskedEntry(mask_frame, mask='+7 (XXX) XXX-XX-XX')
        self.phone_entry.pack(fill=tk.X, pady=5)
        
        # Кнопка для демонстрации получения значений
        ttk.Button(frame, text="Получить значения", command=self.get_advanced_values).pack(pady=10)
        
        self.advanced_values_label = ttk.Label(frame, text="Значения будут здесь", foreground="blue")
        self.advanced_values_label.pack(pady=5)
    
    def validate_numeric(self, value):
        """Валидация ввода - только цифры"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def get_advanced_values(self):
        """Получение значений из продвинутых Entry"""
        placeholder_value = self.placeholder_entry.get()
        numeric_value = self.numeric_entry.get()
        phone_value = self.phone_entry.get()
        
        values_text = f"Placeholder: '{placeholder_value}'\nNumeric: '{numeric_value}'\nPhone: '{phone_value}'"
        self.advanced_values_label.config(text=values_text)
    
    def create_treeview_example(self):
        """Создает пример использования Treeview"""
        frame = ttk.LabelFrame(self.treeview_frame, text="Пример Treeview (таблица/дерево)")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Treeview с прокруткой
        tree_scrollbar = ttk.Scrollbar(frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.treeview = ttk.Treeview(frame, columns=("Value",), show="tree headings", 
                                    yscrollcommand=tree_scrollbar.set)
        self.treeview.heading("#0", text="Ключ")
        self.treeview.heading("Value", text="Значение")
        self.treeview.column("#0", width=150)
        self.treeview.column("Value", width=200)
        
        self.treeview.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.treeview.yview)
        
        # Добавляем данные в Treeview
        data = {
            "Пользователь": "Иванов Иван",
            "Email": "ivanov@example.com",
            "Телефон": "+7 (999) 123-45-67",
            "Должность": "Разработчик",
            "Отдел": "IT"
        }
        for key, value in data.items():
            self.treeview.insert("", tk.END, text=key, values=(value,))
        
        # Добавляем кнопки управления
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_tree_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.remove_tree_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
    
    def add_tree_item(self):
        """Добавляет элемент в Treeview"""
        key = f"Новый элемент {len(self.treeview.get_children())+1}"
        value = "Значение"
        self.treeview.insert("", tk.END, text=key, values=(value,))
    
    def remove_tree_item(self):
        """Удаляет выбранный элемент из Treeview"""
        selected = self.treeview.selection()
        if selected:
            self.treeview.delete(selected)
    
    def clear_tree(self):
        """Очищает Treeview"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def create_progress_examples(self):
        """Создает примеры использования Progressbar"""
        frame = ttk.LabelFrame(self.progress_frame, text="Примеры Progressbar")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Determinate progress bar
        det_frame = ttk.Frame(frame)
        det_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(det_frame, text="Определенный прогресс бар:").pack(anchor=tk.W)
        self.determinate_pb = ttk.Progressbar(det_frame, mode='determinate', maximum=100)
        self.determinate_pb.pack(fill=tk.X, pady=5)
        
        # Кнопка для запуска анимации
        ttk.Button(det_frame, text="Запустить анимацию", command=self.animate_progress).pack(pady=5)
        
        # Indeterminate progress bar
        indet_frame = ttk.Frame(frame)
        indet_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(indet_frame, text="Неопределенный прогресс бар:").pack(anchor=tk.W)
        self.indeterminate_pb = ttk.Progressbar(indet_frame, mode='indeterminate')
        self.indeterminate_pb.pack(fill=tk.X, pady=5)
        
        # Кнопки управления
        control_frame = ttk.Frame(indet_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Старт", command=self.start_indeterminate).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Стоп", command=self.stop_indeterminate).pack(side=tk.LEFT, padx=5)
    
    def animate_progress(self):
        """Анимирует определенный прогресс бар"""
        def animate():
            for i in range(101):
                self.determinate_pb['value'] = i
                self.root.update()
                time.sleep(0.02)
            self.determinate_pb['value'] = 0  # Сброс после анимации
        
        # Запускаем анимацию в отдельном потоке
        animation_thread = threading.Thread(target=animate)
        animation_thread.daemon = True
        animation_thread.start()
    
    def start_indeterminate(self):
        """Запускает неопределенный прогресс бар"""
        self.indeterminate_pb.start(10)  # Обновление каждые 10мс
    
    def stop_indeterminate(self):
        """Останавливает неопределенный прогресс бар"""
        self.indeterminate_pb.stop()
    
    def create_canvas_example(self):
        """Создает пример использования Canvas"""
        frame = ttk.LabelFrame(self.canvas_frame, text="Пример Canvas")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для рисования
        self.canvas = tk.Canvas(frame, bg="white", width=750, height=500)
        self.canvas.pack(pady=10)
        
        # Кнопки для рисования
        draw_frame = ttk.Frame(frame)
        draw_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(draw_frame, text="Нарисовать круг", command=self.draw_circle).pack(side=tk.LEFT, padx=5)
        ttk.Button(draw_frame, text="Нарисовать прямоугольник", command=self.draw_rectangle).pack(side=tk.LEFT, padx=5)
        ttk.Button(draw_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        
        # Привязываем события мыши к Canvas для рисования
        self.canvas.bind("<Button-1>", self.canvas_click)
    
    def draw_circle(self):
        """Рисует круг на Canvas"""
        import random
        x = random.randint(50, 700)
        y = random.randint(50, 450)
        radius = random.randint(20, 50)
        color = random.choice(["red", "green", "blue", "yellow", "purple", "orange"])
        
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                               fill=color, outline="black", width=2)
    
    def draw_rectangle(self):
        """Рисует прямоугольник на Canvas"""
        import random
        x1 = random.randint(50, 650)
        y1 = random.randint(50, 400)
        x2 = x1 + random.randint(30, 100)
        y2 = y1 + random.randint(30, 100)
        color = random.choice(["cyan", "magenta", "brown", "pink", "gray", "lightgreen"])
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
    
    def clear_canvas(self):
        """Очищает Canvas"""
        self.canvas.delete("all")
    
    def canvas_click(self, event):
        """Обработка клика на Canvas"""
        # Рисуем точку по клику
        x, y = event.x, event.y
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
    
    def run(self):
        self.root.mainloop()

# Вспомогательные классы для продвинутых виджетов
class PlaceholderEntry(tk.Entry):
    """Entry с плейсхолдером"""
    def __init__(self, master, placeholder="", color='grey'):
        super().__init__(master)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
        
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
    
    def focus_in(self, *args):
        if self.get() == self.placeholder and self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self.config(fg=self.default_fg_color)
    
    def focus_out(self, *args):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get(self):
        content = super().get()
        if content == self.placeholder and self['fg'] == self.placeholder_color:
            return ''
        return content

class MaskedEntry(tk.Entry):
    """Entry с маской ввода"""
    def __init__(self, master, mask=""):
        super().__init__(master)
        self.mask = mask
        self.mask_char = 'X'
        
        self.bind('<KeyRelease>', self.on_key_release)
    
    def on_key_release(self, event):
        if event.keysym not in ['BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab']:
            current_text = self.get()
            masked_text = self.apply_mask(current_text)
            cursor_pos = self.index(tk.INSERT)
            
            self.delete(0, tk.END)
            self.insert(0, masked_text)
            self.icursor(cursor_pos)
    
    def apply_mask(self, text):
        result = ""
        text_index = 0
        
        for mask_char in self.mask:
            if mask_char == self.mask_char and text_index < len(text):
                result += text[text_index]
                text_index += 1
            else:
                result += mask_char
        
        return result

def demonstrate_advanced_pyqt_patterns():
    """Демонстрирует различные паттерны использования продвинутых возможностей PyQt"""
    print("=== Демонстрация паттернов продвинутого использования PyQt ===")
    
    # Пользовательские виджеты
    print("\n1. Пользовательские виджеты:")
    custom_widget = CustomWidgetSolution()
    print(f"Размер виджета: {custom_widget.minimumSize()}")
    
    # Работа с графикой
    print("\n2. Работа с графикой:")
    scene = QGraphicsScene()
    print(f"Размер сцены по умолчанию: {scene.sceneRect()}")
    
    # Многопоточность
    print("\n3. Многопоточность:")
    worker = WorkerThreadSolution("Тест", 0.1)
    print(f"Название операции: {worker.operation_name}")
    
    # Анимация
    print("\n4. Анимация:")
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    animation = QPropertyAnimation()
    print(f"Состояние анимации: {animation.state()}")
    
    # Системная информация
    print("\n5. Системная информация:")
    print(f"Версия Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"Платформа: {sys.platform}")
    print(f"Кодировка файловой системы: {sys.getfilesystemencoding()}")

def compare_pyqt_tkinter_implementations():
    """Сравнение реализаций PyQt и Tkinter"""
    print("\n=== Сравнение реализаций PyQt и Tkinter ===")
    print("""
    1. PyQt:
       + Более современный и профессиональный внешний вид
       + Богатая коллекция виджетов
       + Отличная документация и сообщество
       + Мощные возможности для создания сложных интерфейсов
       - Требует установки дополнительного пакета (PyQt5/PyQt6)
       - Более сложная лицензия (GPL/Commercial)
       - Кривая обучения немного выше
    
    2. Tkinter:
       + Встроен в Python
       + Простая установка и использование
       + Легкая кривая обучения
       + Подходит для прототипирования
       - Более ограниченный набор виджетов
       - Менее современный внешний вид
       - Меньше возможностей для сложных интерфейсов
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 23 ===")
    
    print("\n1. Задание 1: Пользовательские виджеты")
    # app1 = QApplication(sys.argv)
    # basic_exercise = BasicPyQtExercise()
    # basic_exercise.show()
    # sys.exit(app1.exec_())  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Задание 2: Работа с графикой")
    # app2 = QApplication(sys.argv)
    # graphics_exercise = GraphicsViewExercise()
    # graphics_exercise.show()
    # sys.exit(app2.exec_())  # Закомментировано
    
    print("\n3. Задание 3: Многопоточность в GUI")
    # app3 = QApplication(sys.argv)
    # threading_exercise = ThreadingExercise()
    # threading_exercise.show()
    # sys.exit(app3.exec_())  # Закомментировано
    
    print("\n4. Задание 4: Анимация и эффекты")
    # app4 = QApplication(sys.argv)
    # animation_exercise = AnimationExercise()
    # animation_exercise.show()
    # sys.exit(app4.exec_())  # Закомментировано
    
    print("\n5. Задание 5: Комплексное приложение (Графический редактор)")
    # app5 = QApplication(sys.argv)
    # editor_exercise = GraphicsEditorExercise()
    # editor_exercise.show()
    # sys.exit(app5.exec_())  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # advanced_app = AdvancedFeaturesExamples()
    # advanced_app.run()  # Закомментировано
    
    demonstrate_advanced_pyqt_patterns()
    compare_pyqt_tkinter_implementations()
    
    print("\nДля запуска приложений раскомментируйте соответствующие строки в коде")