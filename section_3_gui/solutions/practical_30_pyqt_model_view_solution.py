#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 30: PyQt6 - Model-View
Решение задач по архитектуре Model-View в PyQt6

Автор: AI Assistant
"""

# Используем PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFormLayout, QLabel, QPushButton, QTableView,
    QListView, QTreeView, QAbstractItemView, QHeaderView,
    QItemDelegate, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QAbstractListModel, QModelIndex, PYQT_VERSION, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QColor, QFont, QIcon


# ==============================================================================
# ЗАДАЧА 1: Основы Model-View
# ==============================================================================

class TableModelDemo(QStandardItemModel):
    """Демонстрация табличной модели"""
    
    def __init__(self, rows=5, columns=3):
        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])
        
        # Заполнение данными
        data = [
            ["Алексей", "30", "Москва"],
            ["Мария", "25", "Санкт-Петербург"],
            ["Иван", "35", "Новосибирск"],
            ["Елена", "28", "Екатеринбург"],
            ["Дмитрий", "32", "Казань"],
        ]
        
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QStandardItem(value)
                self.setItem(row, col, item)


class BasicModelViewDemo(QMainWindow):
    """Демонстрация основ Model-View"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 1: Основы Model-View")
        self.setGeometry(100, 100, 600, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Основы Model-View")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Таблица
        layout.addWidget(QLabel("QTableView:"))
        
        self.table_view = QTableView()
        self.table_model = TableModelDemo()
        self.table_view.setModel(self.table_model)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_view)
        
        # Список
        layout.addWidget(QLabel("\nQListView:"))
        
        self.list_view = QListView()
        self.list_model = QStandardItemModel()
        
        items = ["Первый", "Второй", "Третий", "Четвертый", "Пятый"]
        for item_text in items:
            item = QStandardItem(item_text)
            self.list_model.appendRow(item)
        
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)
        
        central.setLayout(layout)


# ==============================================================================
# ЗАДАЧА 2: Таблицы
# ==============================================================================

class ContactsTableModel(QAbstractTableModel):
    """Модель контактов для таблицы"""
    
    def __init__(self, data=None):
        super().__init__()
        self._data = data or [
            ["Алексей", "+7 999 123-45-67", "alexey@mail.ru"],
            ["Мария", "+7 999 234-56-78", "maria@mail.ru"],
            ["Иван", "+7 999 345-67-89", "ivan@mail.ru"],
            ["Елена", "+7 999 456-78-90", "elena@mail.ru"],
            ["Дмитрий", "+7 999 567-89-01", "dmitry@mail.ru"],
        ]
        self.headers = ["Имя", "Телефон", "Email"]
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[row][col]
        
        if role == Qt.ItemDataRole.EditRole:
            return self._data[row][col]
        
        if role == Qt.ItemDataRole.BackgroundRole:
            # Чередование цветов
            if row % 2 == 0:
                return QColor(240, 240, 240)
        
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None
    
    def add_row(self, row_data):
        """Добавить строку"""
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(row_data)
        self.endInsertRows()
    
    def remove_row(self, row):
        """Удалить строку"""
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.pop(row)
        self.endRemoveRows()


class TableDemo(QMainWindow):
    """Демонстрация таблиц"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 2: Таблицы")
        self.setGeometry(100, 100, 600, 450)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Работа с таблицами")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Таблица
        self.table_view = QTableView()
        self.model = ContactsTableModel()
        self.table_view.setModel(self.model)
        
        # Настройка таблицы
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table_view)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_row)
        btn_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Удалить")
        remove_btn.clicked.connect(self.remove_row)
        btn_layout.addWidget(remove_btn)
        
        sort_btn = QPushButton("Сортировать")
        sort_btn.clicked.connect(self.sort_table)
        btn_layout.addWidget(sort_btn)
        
        layout.addLayout(btn_layout)
        
        # Поиск/фильтр
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Фильтр:"))
        
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Введите имя для фильтрации...")
        self.filter_edit.textChanged.connect(self.filter_data)
        filter_layout.addWidget(self.filter_edit)
        
        layout.addLayout(filter_layout)
        
        central.setLayout(layout)
    
    def add_row(self):
        """Добавить строку"""
        new_row = ["Новый", "+7 000 000-00-00", "new@mail.ru"]
        self.model.add_row(new_row)
    
    def remove_row(self):
        """Удалить строку"""
        current_row = self.table_view.currentIndex().row()
        if current_row >= 0:
            self.model.remove_row(current_row)
    
    def sort_table(self):
        """Сортировка"""
        self.table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
    
    def filter_data(self, text):
        """Фильтрация данных"""
        # Простая фильтрация - скрываем не matching строки
        for row in range(self.model.rowCount()):
            match = False
            for col in range(self.model.columnCount()):
                index = self.model.index(row, col)
                data = self.model.data(index)
                if text.lower() in data.lower():
                    match = True
                    break
            
            if text and not match:
                self.table_view.setRowHidden(row, True)
            else:
                self.table_view.setRowHidden(row, False)


# ==============================================================================
# ЗАДАЧА 3: Древовидные структуры
# ==============================================================================

class TreeDemo(QMainWindow):
    """Демонстрация дерева"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 3: Древовидные структуры")
        self.setGeometry(100, 100, 500, 450)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Древовидные структуры")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Дерево
        self.tree_view = QTreeView()
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Название", "Тип", "Размер"])
        
        # Создание иерархической структуры
        # Корень - файловая система
        root = QStandardItem("Мой компьютер")
        self.tree_model.appendRow(root)
        
        # Диски
        disks = ["Диск C:", "Диск D:"]
        for disk_name in disks:
            disk = QStandardItem(disk_name)
            disk.setIcon(QIcon.fromTheme("drive-harddisk"))
            root.appendRow(disk)
            
            # Папки
            folders = ["Документы", "Загрузки", "Изображения"]
            for folder in folders:
                folder_item = QStandardItem(folder)
                folder_item.setIcon(QIcon.fromTheme("folder"))
                disk.appendRow(folder_item)
                
                # Файлы
                files = ["Файл 1.txt", "Файл 2.doc", "Файл 3.pdf"]
                for file in files:
                    file_item = QStandardItem(file)
                    file_item.setIcon(QIcon.fromTheme("text-x-generic"))
                    folder_item.appendRow(file_item)
        
        # Добавить еще одну ветку
        projects = QStandardItem("Проекты")
        projects.setIcon(QIcon.fromTheme("folder"))
        root.appendRow(projects)
        
        project1 = QStandardItem("Проект 1")
        project1.setIcon(QIcon.fromTheme("folder"))
        projects.appendRow(project1)
        
        src = QStandardItem("src")
        src.setIcon(QIcon.fromTheme("folder"))
        project1.appendRow(src)
        
        src.appendRow(QStandardItem("main.py"))
        src.appendRow(QStandardItem("utils.py"))
        
        project1.appendRow(QStandardItem("README.md"))
        
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        
        layout.addWidget(self.tree_view)
        
        # Информация о выбранном
        self.info_label = QLabel("Выберите элемент")
        layout.addWidget(self.info_label)
        
        # Связь с выбором
        self.tree_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        central.setLayout(layout)
    
    def on_selection_changed(self, selected, deselected):
        """Обработка изменения выбора"""
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            item = self.tree_model.itemFromIndex(index)
            self.info_label.setText(f"Выбрано: {item.text()}")


# ==============================================================================
# ЗАДАЧА 4: Списки
# ==============================================================================

class ListDemo(QMainWindow):
    """Демонстрация списков"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 4: Списки")
        self.setGeometry(100, 100, 450, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Работа со списками")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Список
        self.list_view = QListView()
        self.list_model = QStandardItemModel()
        
        # Элементы с иконками
        items_data = [
            ("Задача 1", False),
            ("Задача 2", True),
            ("Задача 3", False),
            ("Задача 4", True),
            ("Задача 5", False),
        ]
        
        for text, checked in items_data:
            item = QStandardItem(text)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
            
            # Цвет текста
            if checked:
                item.setForeground(QColor(100, 100, 100))
            
            self.list_model.appendRow(item)
        
        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        layout.addWidget(self.list_view)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_item)
        btn_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Удалить")
        remove_btn.clicked.connect(self.remove_item)
        btn_layout.addWidget(remove_btn)
        
        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.clear_list)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Выбранные элементы
        self.selection_label = QLabel("Выбрано: -")
        layout.addWidget(self.selection_label)
        
        # Связь с выбором
        self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
        central.setLayout(layout)
    
    def add_item(self):
        """Добавить элемент"""
        import random
        text = f"Элемент {random.randint(100, 999)}"
        item = QStandardItem(text)
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Unchecked)
        
        self.list_model.appendRow(item)
    
    def remove_item(self):
        """Удалить выбранные элементы"""
        selected_indexes = self.list_view.selectedIndexes()
        for index in reversed(selected_indexes):
            self.list_model.removeRow(index.row())
    
    def clear_list(self):
        """Очистить список"""
        self.list_model.clear()
    
    def on_selection_changed(self, selected, deselected):
        """Обработка изменения выбора"""
        selected_indexes = self.list_view.selectedIndexes()
        if selected_indexes:
            texts = [self.list_model.data(index) for index in selected_indexes]
            self.selection_label.setText(f"Выбрано: {', '.join(texts)}")
        else:
            self.selection_label.setText("Выбрано: -")


# ==============================================================================
# ЗАДАЧА 5: Продвинутые техники
# ==============================================================================

class AdvancedModelDemo(QMainWindow):
    """Демонстрация продвинутых техник Model-View"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 5: Продвинутые техники")
        self.setGeometry(100, 100, 600, 500)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Продвинутые техники Model-View")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Notebook для разных примеров
        from PyQt6.QtWidgets import QTabWidget
        
        tabs = QTabWidget()
        
        # Вкладка 1: Сортировка и фильтрация
        tab1 = QWidget()
        self.create_sort_filter_tab(tab1)
        tabs.addTab(tab1, "Сортировка и фильтр")
        
        # Вкладка 2: Большие наборы данных
        tab2 = QWidget()
        self.create_large_data_tab(tab2)
        tabs.addTab(tab2, "Большие данные")
        
        # Вкладка 3: Экспорт/импорт
        tab3 = QWidget()
        self.create_export_import_tab(tab3)
        tabs.addTab(tab3, "Экспорт/импорт")
        
        layout.addWidget(tabs)
        
        central.setLayout(layout)
    
    def create_sort_filter_tab(self, parent):
        """Вкладка сортировки и фильтрации"""
        layout = QVBoxLayout()
        
        # Модель с данными
        self.sort_filter_model = QStandardItemModel(10, 3)
        self.sort_filter_model.setHorizontalHeaderLabels(["Имя", "Возраст", "Город"])
        
        data = [
            ["Алексей", "30", "Москва"],
            ["Мария", "25", "Санкт-Петербург"],
            ["Иван", "35", "Новосибирск"],
            ["Елена", "28", "Екатеринбург"],
            ["Дмитрий", "32", "Казань"],
            ["Ольга", "27", "Москва"],
            ["Сергей", "40", "Санкт-Петербург"],
            ["Анна", "24", "Новосибирск"],
            ["Павел", "33", "Казань"],
            ["Татьяна", "29", "Екатеринбург"],
        ]
        
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.sort_filter_model.setItem(row, col, QStandardItem(value))
        
        # Прокси модель для сортировки/фильтрации
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.sort_filter_model)
        
        # Таблица
        table = QTableView()
        table.setModel(self.proxy_model)
        table.setSortingEnabled(True)
        layout.addWidget(table)
        
        # Фильтр
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Фильтр по городу:"))
        
        city_combo = QComboBox()
        city_combo.addItems(["Все", "Москва", "Санкт-Петербург", "Новосибирск", "Казань", "Екатеринбург"])
        city_combo.currentTextChanged.connect(lambda text: self.apply_filter(text, 2))
        filter_layout.addWidget(city_combo)
        
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        parent.setLayout(layout)
    
    def apply_filter(self, text, column):
        """Применить фильтр"""
        if text == "Все":
            self.proxy_model.setFilterRegExp("")
        else:
            self.proxy_model.setFilterRegExp(text)
            self.proxy_model.setFilterKeyColumn(column)
    
    def create_large_data_tab(self, parent):
        """Вкладка с большими данными"""
        layout = QVBoxLayout()
        
        # Модель для большого набора данных
        large_model = QStandardItemModel(1000, 5)
        large_model.setHorizontalHeaderLabels(["ID", "Название", "Статус", "Дата", "Значение"])
        
        import random
        statuses = ["Активный", "Ожидание", "Завершено", "Отменено"]
        
        for row in range(1000):
            for col in range(5):
                if col == 0:
                    value = str(row + 1)
                elif col == 1:
                    value = f"Элемент {row + 1}"
                elif col == 2:
                    value = random.choice(statuses)
                elif col == 3:
                    value = f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                else:
                    value = str(random.randint(0, 1000))
                
                large_model.setItem(row, col, QStandardItem(value))
        
        table = QTableView()
        table.setModel(large_model)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Оптимизация для больших данных (удалено в PyQt6)
        # table.setUniformRowHeights(True)
        
        layout.addWidget(QLabel(f"Таблица с {large_model.rowCount()} строками:"))
        layout.addWidget(table)
        
        parent.setLayout(layout)
    
    def create_export_import_tab(self, parent):
        """Вкладка экспорта/импорта"""
        layout = QVBoxLayout()
        
        # Демонстрационная таблица
        demo_model = QStandardItemModel(5, 3)
        demo_model.setHorizontalHeaderLabels(["Имя", "Телефон", "Email"])
        
        data = [
            ["Алексей", "+7 999 123-45-67", "alexey@mail.ru"],
            ["Мария", "+7 999 234-56-78", "maria@mail.ru"],
            ["Иван", "+7 999 345-67-89", "ivan@mail.ru"],
            ["Елена", "+7 999 456-78-90", "elena@mail.ru"],
            ["Дмитрий", "+7 999 567-89-01", "dmitry@mail.ru"],
        ]
        
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                demo_model.setItem(row, col, QStandardItem(value))
        
        table = QTableView()
        table.setModel(demo_model)
        layout.addWidget(table)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        export_btn = QPushButton("Экспорт в CSV")
        export_btn.clicked.connect(lambda: self.export_csv(demo_model))
        btn_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Импорт из CSV")
        import_btn.clicked.connect(lambda: self.import_csv(demo_model))
        btn_layout.addWidget(import_btn)
        
        layout.addLayout(btn_layout)
        
        parent.setLayout(layout)
    
    def export_csv(self, model):
        """Экспорт в CSV"""
        from PyQt6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Заголовки
                    headers = [model.headerData(i, Qt.Horizontal) for i in range(model.columnCount())]
                    f.write(",".join(headers) + "\n")
                    
                    # Данные
                    for row in range(model.rowCount()):
                        row_data = []
                        for col in range(model.columnCount()):
                            index = model.index(row, col)
                            row_data.append(model.data(index))
                        f.write(",".join(row_data) + "\n")
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Экспорт", f"Данные экспортированы в {filename}")
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def import_csv(self, model):
        """Импорт из CSV"""
        from PyQt6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getOpenFileName(
            self, "Импорт", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                model.clear()
                model.setHorizontalHeaderLabels(["Имя", "Телефон", "Email"])
                
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    for line in lines[1:]:  # Пропустить заголовок
                        parts = line.strip().split(",")
                        for col, value in enumerate(parts):
                            model.setItem(len(model), col, QStandardItem(value))
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Импорт", "Данные импортированы")
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Ошибка", str(e))


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
            ("Задача 1: Основы Model-View", self.open_task1),
            ("Задача 2: Таблицы", self.open_task2),
            ("Задача 3: Древовидные структуры", self.open_task3),
            ("Задача 4: Списки", self.open_task4),
            ("Задача 5: Продвинутые техники", self.open_task5),
        ]
    
    def open_task1(self):
        window = BasicModelViewDemo()
        self.windows.append(window)
        window.show()
    
    def open_task2(self):
        window = TableDemo()
        self.windows.append(window)
        window.show()
    
    def open_task3(self):
        window = TreeDemo()
        self.windows.append(window)
        window.show()
    
    def open_task4(self):
        window = ListDemo()
        self.windows.append(window)
        window.show()
    
    def open_task5(self):
        window = AdvancedModelDemo()
        self.windows.append(window)
        window.show()
    
    def run(self):
        if PYQT_VERSION == 0:
            print("PyQt не установлен.")
            return
        
        main_window = QMainWindow()
        main_window.setWindowTitle("Практическое занятие 30: PyQt - Model-View")
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
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()
