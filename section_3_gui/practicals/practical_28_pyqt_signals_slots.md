# Практическое занятие 28: PyQt6 - сигналы и слоты

## Цель занятия
Изучить механизм сигналов и слотов в PyQt6, научиться создавать собственные сигналы, обрабатывать события и строить приложения на основе событийной модели.

## Задачи
1. Освоить базовый механизм сигналов и слотов
2. Научиться создавать собственные сигналы
3. Обрабатывать события мыши и клавиатуры
4. Управлять жизненным циклом окна

## Ход работы

### 1. Основы сигналов и слотов

```python
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class MyWidget:
    """
    Виджет с собственными сигналами
    """
    # Объявление сигнала
    my_signal = pyqtSignal(str)
    
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ
        pass
```

---

## 1. Теоретическая часть: Сигналы и слоты в PyQt6

### Уровень 1 - Начальный

#### Задание 1.1: Основы сигналов и слотов

Освойте базовый механизм:

```python
class SignalDemo(QMainWindow):
    """
    Демонстрация сигналов и слотов
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # Подключение сигналов к слотам
        # Встроенные сигналы виджетов
        # Лямбда-функции как слоты
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class SignalDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сигналы и слоты")
        self.setGeometry(100, 100, 300, 200)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.label = QLabel("Нажмите кнопку")
        layout.addWidget(self.label)
        
        button = QPushButton("Нажми меня")
        layout.addWidget(button)
        
        # Простое соединение
        button.clicked.connect(self.on_click)
        
        # Лямбда с аргументом
        button.clicked.connect(lambda checked, x=10: self.process(x))
        
    def on_click(self):
        self.label.setText("Нажато!")
        
    def process(self, value):
        print(f"Обработано: {value}")

app = QApplication(sys.argv)
window = SignalDemo()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Собственные сигналы

Создайте пользовательские сигналы:

```python
from PyQt6.QtCore import pyqtSignal, QObject

class DataProcessor(QObject):
    """
    Обработчик данных с сигналами
    """
    started = pyqtSignal()
    progress = pyqtSignal(int)  # сигнал с int параметром
    finished = pyqtSignal(str)  # сигнал с str параметром
    
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import pyqtSignal, QObject

class DataProcessor(QObject):
    started = pyqtSignal()
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def process(self):
        self.started.emit()
        for i in range(100):
            self.progress.emit(i + 1)
        self.finished.emit("Готово!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Собственные сигналы")
        self.setGeometry(100, 100, 300, 200)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.label = QLabel("Нажмите кнопку")
        layout.addWidget(self.label)
        
        self.button = QPushButton("Запустить")
        layout.addWidget(self.button)
        
        self.processor = DataProcessor()
        self.button.clicked.connect(self.start_process)
        
        self.processor.started.connect(self.on_started)
        self.processor.progress.connect(self.on_progress)
        self.processor.finished.connect(self.on_finished)
        
    def start_process(self):
        self.processor.process()
        
    def on_started(self):
        self.label.setText("Начато...")
        
    def on_progress(self, value):
        self.label.setText(f"Прогресс: {value}%")
        
    def on_finished(self, result):
        self.label.setText(result)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: События окна

Управляйте жизненным циклом:

```python
class EventWindow(QMainWindow):
    """
    Обработка событий окна
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # showEvent, closeEvent
        # resizeEvent, moveEvent
        # focusInEvent, focusOutEvent
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout

class EventWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("События окна")
        self.setGeometry(100, 100, 400, 300)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        self.status_label = QLabel("Ожидание...")
        layout.addWidget(self.status_label)
        
    def showEvent(self, event):
        self.status_label.setText("Окно показано")
        super().showEvent(event)
        
    def closeEvent(self, event):
        self.status_label.setText("Окно закрывается")
        super().closeEvent(event)
        
    def resizeEvent(self, event):
        self.status_label.setText(f"Размер: {event.size().width()}x{event.size().height()}")
        super().resizeEvent(event)

app = QApplication(sys.argv)
window = EventWindow()
window.show()
sys.exit(app.exec())
```

</details>

---

## Требования к отчету
- Исходный код всех примеров
- Описание сигналов и слотов
- Примеры собственных сигналов

## Критерии оценки
- Понимание механизма: 35%
- Создание сигналов: 25%
- Обработка событий: 25%
- Документация: 15%
