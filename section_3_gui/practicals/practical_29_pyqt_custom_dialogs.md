# Практическое занятие 29: PyQt6 - пользовательские диалоги

## Цель занятия
Изучить создание пользовательских диалоговых окон в PyQt6, освоить модальные и немодальные окна, научиться передавать данные между диалогом и основным приложением.

## Задачи
1. Освоить стандартные диалоги
2. Научиться создавать формы ввода
3. Создать кастомные диалоги
4. Изучить модальные и немодальные режимы

## Ход работы

### 1. Основы диалогов

```python
from PyQt6.QtWidgets import QDialog

class MyDialog(QDialog):
    """
    Базовый диалог
    """
    def __init__(self, parent=None):
        # ВАШ КОД ЗДЕСЬ
        pass
```

---

## 1. Теоретическая часть: Пользовательские диалоги

### Уровень 1 - Начальный

#### Задание 1.1: Базовые диалоги

Освойте стандартные диалоги:

```python
class DialogDemo(QMainWindow):
    """
    Демонстрация диалогов
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # QDialog - базовый класс
        # Модальные диалоги
        # Возвращаемые значения
        # Принятие/отклонение
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QDialogButtonBox

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Мой диалог")
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите данные:"))
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

class DialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Диалоги")
        self.setGeometry(100, 100, 300, 200)
        
        button = QPushButton("Открыть диалог")
        button.clicked.connect(self.open_dialog)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(button)
        widget.setLayout(layout)
        
    def open_dialog(self):
        dialog = MyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print("Диалог принят")
        else:
            print("Диалог отклонен")

app = QApplication(sys.argv)
window = DialogDemo()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Формы ввода

Создайте диалоги ввода:

```python
from PyQt6.QtWidgets import QFormLayout, QLineEdit, QSpinBox

class InputDialog(QDialog):
    """
    Диалог ввода данных
    """
    def __init__(self, parent=None):
        # ВАШ КОД ЗДЕСЬ:
        # QLineEdit - поле ввода
        # QSpinBox - числовое поле
        # QFormLayout - форма
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод данных")
        self.resize(300, 150)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        layout.addRow("Имя:", self.name_edit)
        
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 150)
        layout.addRow("Возраст:", self.age_spin)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "age": self.age_spin.value()
        }

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Формы ввода")
        self.setGeometry(100, 100, 300, 200)
        
        button = QPushButton("Открыть форму")
        button.clicked.connect(self.open_form)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(button)
        widget.setLayout(layout)
        
    def open_form(self):
        dialog = InputDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            print(f"Имя: {data['name']}, Возраст: {data['age']}")

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Модальные vs Немодальные

Изучите режимы отображения:

```python
class ModalVsNonModal(QMainWindow):
    """
    Сравнение модальных и немодальных окон
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # exec() - модальное окно
        # show() - немодальное окно
        # Взаимодействие между окнами
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QTextEdit

class PreviewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предпросмотр")
        self.resize(300, 200)
        self.setModal(False)  # Немодальный
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Предварительный просмотр"))
        self.content = QTextEdit()
        layout.addWidget(self.content)
        self.setLayout(layout)
    
    def update_content(self, text):
        self.content.setPlainText(text)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Модальные vs Немодальные")
        self.setGeometry(100, 100, 400, 300)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        
        self.modal_btn = QPushButton("Модальный диалог")
        self.modal_btn.clicked.connect(self.open_modal)
        
        self.non_modal_btn = QPushButton("Немодальный диалог")
        self.non_modal_btn.clicked.connect(self.open_non_modal)
        
        self.text_edit = QTextEdit()
        
        layout.addWidget(self.modal_btn)
        layout.addWidget(self.non_modal_btn)
        layout.addWidget(self.text_edit)
        
        widget.setLayout(layout)
        
        self.preview_dialog = None
    
    def open_modal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Модальный")
        dialog.resize(200, 100)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это модальное окно"))
        dialog.setLayout(layout)
        dialog.exec()  # Блокирует родительское окно
    
    def open_non_modal(self):
        if not self.preview_dialog:
            self.preview_dialog = PreviewDialog(self)
        self.preview_dialog.update_content(self.text_edit.toPlainText())
        self.preview_dialog.show()

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())
```

</details>

---

## Требования к отчету
- Исходный код всех диалогов
- Схемы взаимодействия
- Описание модальности
- Примеры передачи данных

## Критерии оценки
- Функциональность: 30%
- Гибкость: 25%
- Качество кода: 25%
- Документация: 20%
