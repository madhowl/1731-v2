# Практическое занятие 30: PyQt6 - Model-View

## Цель занятия
Изучить архитектуру Model-View в PyQt6, освоить QAbstractItemModel, QTableView, QTreeView, QListView и научиться создавать приложения с табличными и древовидными данными.

## Задачи
1. Освоить архитектуру Model-View
2. Изучить QAbstractItemModel
3. Научиться использовать QTableView, QTreeView, QListView
4. Создать приложение с табличными и древовидными данными

## Ход работы

### 1. Основы Model-View

```python
from PyQt6.QtWidgets import QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

def create_table_view(parent):
    """
    Создает табличное представление
    
    Args:
        parent: Родительский виджет
    """
    # ВАШ КОД ЗДЕСЬ - создайте модель и представление
    pass
```

---

## 1. Теоретическая часть: Model-View в PyQt6

### Уровень 1 - Начальный

#### Задание 1.1: Основы Model-View

Изучите архитектуру:

```python
from PyQt6.QtWidgets import QTableView, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TableViewDemo(QMainWindow):
    """
    Демонстрация табличного представления
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # QAbstractItemModel
        # QStandardItemModel
        # QTableView - табличное представление
        # QListView - список
        # Связь модели и представления
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TableViewDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Табличное представление")
        self.setGeometry(100, 100, 600, 400)
        
        # Создаем модель
        self.model = QStandardItemModel(3, 3)
        self.model.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])
        
        # Заполняем данными
        for row in range(3):
            for col in range(3):
                item = QStandardItem(f"Данные {row},{col}")
                self.model.setItem(row, col, item)
        
        # Создаем представление
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        
        # Устанавливаем представление как центральный виджет
        self.setCentralWidget(self.table_view)

app = QApplication(sys.argv)
window = TableViewDemo()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Таблицы

Создайте табличное приложение:

```python
class TableApp(QMainWindow):
    """
    Приложение с таблицей
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # Заполнение данными
        # Редактирование ячеек
        # Сортировка
        # Фильтрация
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица")
        self.setGeometry(100, 100, 700, 500)
        
        # Модель
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])
        
        # Представление
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        
        # Кнопки управления
        add_btn = QPushButton("Добавить строку")
        add_btn.clicked.connect(self.add_row)
        
        delete_btn = QPushButton("Удалить строку")
        delete_btn.clicked.connect(self.delete_row)
        
        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Заполняем начальными данными
        self.populate_initial_data()
    
    def populate_initial_data(self):
        data = [
            ["Анна", "25", "Москва"],
            ["Иван", "30", "Санкт-Петербург"],
            ["Мария", "28", "Новосибирск"]
        ]
        
        for row_data in data:
            items = [QStandardItem(field) for field in row_data]
            self.model.appendRow(items)
    
    def add_row(self):
        items = [QStandardItem(""), QStandardItem(""), QStandardItem("")]
        self.model.appendRow(items)
    
    def delete_row(self):
        selected = self.table_view.selectedIndexes()
        if selected:
            row = selected[0].row()
            self.model.removeRow(row)

app = QApplication(sys.argv)
window = TableApp()
window.show()
sys.exit(app.exec())
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Древовидные структуры

Освойте дерево:

```python
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItem

class TreeViewDemo(QMainWindow):
    """
    Демонстрация древовидного представления
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ:
        # QTreeView
        # Иерархические данные
        # Развернуть/свернуть узлы
        # Узлы с данными и без
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class TreeViewDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Дерево")
        self.setGeometry(100, 100, 500, 400)
        
        # Модель
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Название", "Тип"])
        
        # Создаем дерево
        root = self.model.invisibleRootItem()
        
        # Родительский элемент
        folder1 = QStandardItem("Папка 1")
        folder1.appendRow([QStandardItem("Файл 1.txt"), QStandardItem("Файл")])
        folder1.appendRow([QStandardItem("Файл 2.txt"), QStandardItem("Файл")])
        
        folder2 = QStandardItem("Папка 2")
        folder2.appendRow([QStandardItem("Файл 3.txt"), QStandardItem("Файл")])
        
        root.appendRow([folder1, QStandardItem("Папка")])
        root.appendRow([folder2, QStandardItem("Папка")])
        
        # Представление
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()
        
        # Кнопки управления
        expand_btn = QPushButton("Развернуть все")
        expand_btn.clicked.connect(self.tree_view.expandAll)
        
        collapse_btn = QPushButton("Свернуть все")
        collapse_btn.clicked.connect(self.tree_view.collapseAll)
        
        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(expand_btn)
        btn_layout.addWidget(collapse_btn)
        layout.addLayout(btn_layout)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = TreeViewDemo()
window.show()
sys.exit(app.exec())
```

</details>

---

## Требования к отчету
- Исходный код всех примеров
- Описание архитектуры MVC/MVVM
- Диаграмма Model-View

## Критерии оценки
- Понимание архитектуры: 35%
- Функциональность: 30%
- Качество реализации: 20%
- Документация: 15%
