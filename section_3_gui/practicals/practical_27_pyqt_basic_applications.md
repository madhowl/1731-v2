# Практическое занятие 27: PyQt6 - базовые приложения

## Цель занятия
Изучить основы создания графических приложений с использованием библиотеки PyQt6, освоить основные виджеты и принципы построения приложений.

## Задачи
1. Освоить создание приложения PyQt6
2. Изучить основные виджеты (QPushButton, QLabel, QLineEdit и др.)
3. Научиться использовать системы компоновки
4. Создать меню и тулбары

## Ход работы

### 1. Основы PyQt6

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

def create_basic_app():
    """
    Создает базовое приложение
    
    Returns:
        QMainWindow: Главное окно
    """
    # ВАШ КОД ЗДЕСЬ - создайте приложение
    pass
```

---

## 1. Теоретическая часть: Основы PyQt6

### Уровень 1 - Начальный

#### Задание 1.1: Базовое приложение

Создайте первое приложение:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - создайте окно
        # setWindowTitle - заголовок
        # setGeometry - размеры и положение
        pass
        
    def on_click(self):
        # ВАШ КОД ЗДЕСЬ - обработчик нажатия
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Первое приложение")
        self.setGeometry(100, 100, 400, 300)
        
        self.label = QLabel("Нажмите кнопку", self)
        self.label.setGeometry(50, 50, 200, 30)
        
        self.button = QPushButton("Нажми меня", self)
        self.button.setGeometry(50, 100, 150, 40)
        self.button.clicked.connect(self.on_click)
    
    def on_click(self):
        self.label.setText("Кнопка нажата!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Компоновка виджетов

Изучите системы компоновки:

```python
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout

class LayoutDemo(QMainWindow):
    """
    Демонстрация компоновки
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - создайте:
        # QVBoxLayout - вертикальная
        # QHBoxLayout - горизонтальная
        # QGridLayout - табличная
        # QFormLayout - форма
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Компоновка")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(QLineEdit())
        
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(QLineEdit())
        
        layout.addWidget(QPushButton("Отправить"))

app = QApplication(sys.argv)
window = LayoutDemo()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Меню и тулбары

Создайте интерфейс с навигацией:

```python
from PyQt6.QtGui import QAction

class MenuApp(QMainWindow):
    """
    Приложение с меню
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - создайте:
        # QMenuBar - строка меню
        # QToolBar - панель инструментов
        # QStatusBar - строка статуса
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QAction

class MenuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню и тулбар")
        self.setGeometry(100, 100, 600, 400)
        
        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        
        new_action = QAction("Новый", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Тулбар
        toolbar = self.addToolBar("Инструменты")
        toolbar.addAction(new_action)
        
        # Центральный виджет
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        
        # Статус бар
        self.statusBar().showMessage("Готов")
    
    def new_file(self):
        self.text_edit.clear()
        self.statusBar().showMessage("Новый файл")

app = QApplication(sys.argv)
window = MenuApp()
window.show()
sys.exit(app.exec())
```

</details>

---

## Требования к отчету
- Исходный код всех приложений
- Скриншоты интерфейсов
- Описание виджетов

## Критерии оценки
- Функциональность: 40%
- Качество интерфейса: 25%
- Качество кода: 20%
- Документация: 15%
