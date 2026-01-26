# Упражнения для практического занятия 22: PyQt - проектирование UI

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                            QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
                            QCheckBox, QRadioButton, QComboBox, QSpinBox, QSlider, 
                            QProgressBar, QTableWidgetItem, QListWidget, QTreeWidget,
                            QTreeWidgetItem, QMessageBox, QTabWidget, QSplitter,
                            QStackedWidget, QGroupBox, QFrame, QScrollArea, QTextEdit,
                            QMenuBar, QStatusBar, QToolBar, QAction, QFileDialog,
                            QStyleFactory, QDesktopWidget, QInputDialog, QColorDialog,
                            QFontDialog, QProgressDialog)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPixmap, QIcon
import json
import os
from typing import Dict, Any, List

# Задание 1: Основы PyQt
class BasicPyQtApp(QMainWindow):
    """Приложение с основами PyQt"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 1: Основы PyQt")
        self.setGeometry(100, 100, 600, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        layout = QVBoxLayout()
        
        # QLabel
        self.label = QLabel("Это пример QLabel")
        self.label.setFont(QFont("Arial", 14))
        layout.addWidget(self.label)
        
        # QLineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Введите текст здесь...")
        layout.addWidget(self.line_edit)
        
        # QPushButton
        self.button = QPushButton("Нажми меня!")
        self.button.clicked.connect(self.button_clicked)
        layout.addWidget(self.button)
        
        # Кнопка для отображения введенного текста
        self.display_button = QPushButton("Показать введенный текст")
        self.display_button.clicked.connect(self.display_text)
        layout.addWidget(self.display_button)
        
        # Кнопка для очистки
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_fields)
        layout.addWidget(self.clear_button)
        
        # Устанавливаем макет
        central_widget.setLayout(layout)
    
    def button_clicked(self):
        """Обработчик нажатия кнопки"""
        self.label.setText("Кнопка была нажата!")
        self.label.setStyleSheet("color: blue; font-weight: bold;")
    
    def display_text(self):
        """Отображает введенный текст"""
        text = self.line_edit.text()
        if text:
            self.label.setText(f"Вы ввели: {text}")
            self.label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.label.setText("Текст не введен")
            self.label.setStyleSheet("color: red; font-weight: bold;")
    
    def clear_fields(self):
        """Очищает поля ввода"""
        self.line_edit.clear()
        self.label.setText("Поля очищены")
        self.label.setStyleSheet("color: black; font-weight: normal;")

# Задание 2: Компоновка элементов
class LayoutApp(QMainWindow):
    """Приложение для демонстрации компоновки"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 2: Компоновка элементов")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем вкладки для разных макетов
        tab_widget = QTabWidget()
        
        # Вкладка вертикального макета
        vertical_tab = self.create_vertical_layout_tab()
        tab_widget.addTab(vertical_tab, "Вертикальный")
        
        # Вкладка горизонтального макета
        horizontal_tab = self.create_horizontal_layout_tab()
        tab_widget.addTab(horizontal_tab, "Горизонтальный")
        
        # Вкладка сеточного макета
        grid_tab = self.create_grid_layout_tab()
        tab_widget.addTab(grid_tab, "Сеточный")
        
        # Вкладка формы
        form_tab = self.create_form_layout_tab()
        tab_widget.addTab(form_tab, "Форма")
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        central_widget.setLayout(layout)
    
    def create_vertical_layout_tab(self):
        """Создает вкладку с вертикальным макетом"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        for i in range(5):
            btn = QPushButton(f"Кнопка {i+1} (вертикальный)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "вертикальный"))
            layout.addWidget(btn)
        
        # Добавляем текстовое поле в конец
        text_field = QLineEdit("Текстовое поле в вертикальном макете")
        layout.addWidget(text_field)
        
        tab.setLayout(layout)
        return tab
    
    def create_horizontal_layout_tab(self):
        """Создает вкладку с горизонтальным макетом"""
        tab = QWidget()
        layout = QHBoxLayout()
        
        for i in range(5):
            btn = QPushButton(f"Кнопка {i+1} (горизонт.)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "горизонтальный"))
            layout.addWidget(btn)
        
        # Добавляем метку в конец
        label = QLabel("Метка в горизонтальном макете")
        layout.addWidget(label)
        
        tab.setLayout(layout)
        return tab
    
    def create_grid_layout_tab(self):
        """Создает вкладку с сеточным макетом"""
        tab = QWidget()
        layout = QGridLayout()
        
        # Добавляем элементы в сетку
        positions = [(i, j) for i in range(3) for j in range(3)]
        for i, (row, col) in enumerate(positions):
            btn = QPushButton(f"Кнопка {i+1}")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "сеточный"))
            layout.addWidget(btn, row, col)
        
        # Добавляем элемент, занимающий несколько ячеек
        multi_cell_btn = QPushButton("Многоячеечная кнопка")
        multi_cell_btn.clicked.connect(lambda: self.show_layout_info(0, "многоячеечный"))
        layout.addWidget(multi_cell_btn, 3, 0, 1, 3)  # Занимает всю нижнюю строку
        
        tab.setLayout(layout)
        return tab
    
    def create_form_layout_tab(self):
        """Создает вкладку с формой"""
        tab = QWidget()
        layout = QFormLayout()
        
        layout.addRow("Имя:", QLineEdit())
        layout.addRow("Email:", QLineEdit())
        layout.addRow("Телефон:", QLineEdit())
        
        submit_btn = QPushButton("Отправить")
        submit_btn.clicked.connect(lambda: self.show_layout_info(0, "форма"))
        layout.addRow(submit_btn)
        
        tab.setLayout(layout)
        return tab
    
    def show_layout_info(self, button_num, layout_type):
        """Показывает информацию о нажатом элементе"""
        QMessageBox.information(self, "Информация", 
                               f"Нажата кнопка {button_num} в {layout_type} макете")

# Задание 3: Виджеты PyQt
class WidgetsApp(QMainWindow):
    """Приложение с различными виджетами PyQt"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 3: Виджеты PyQt")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # QCheckBox
        checkbox_group = QGroupBox("Чекбоксы")
        checkbox_layout = QHBoxLayout()
        self.checkboxes = []
        for i in range(5):
            cb = QCheckBox(f"Флажок {i+1}")
            cb.stateChanged.connect(lambda state, x=i+1: self.checkbox_changed(state, x))
            checkbox_layout.addWidget(cb)
            self.checkboxes.append(cb)
        checkbox_group.setLayout(checkbox_layout)
        layout.addWidget(checkbox_group)
        
        # QRadioButton
        radio_group = QGroupBox("Переключатели")
        radio_layout = QHBoxLayout()
        self.radiobuttons = []
        for i in range(3):
            rb = QRadioButton(f"Переключатель {i+1}")
            rb.toggled.connect(lambda checked, x=i+1: self.radiobutton_toggled(checked, x))
            radio_layout.addWidget(rb)
            self.radiobuttons.append(rb)
        radio_group.setLayout(radio_layout)
        layout.addWidget(radio_group)
        
        # QComboBox
        combo_group = QGroupBox("Комбобокс")
        combo_layout = QHBoxLayout()
        self.combobox = QComboBox()
        self.combobox.addItems(["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"])
        self.combobox.currentTextChanged.connect(self.combobox_changed)
        combo_layout.addWidget(QLabel("Выберите элемент:"))
        combo_layout.addWidget(self.combobox)
        combo_group.setLayout(combo_layout)
        layout.addWidget(combo_group)
        
        # QSpinBox и QSlider
        spin_slider_group = QGroupBox("Спинбокс и слайдер")
        spin_slider_layout = QHBoxLayout()
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        self.spin_box.valueChanged.connect(self.spinbox_changed)
        spin_slider_layout.addWidget(QLabel("Спинбокс:"))
        spin_slider_layout.addWidget(self.spin_box)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slider_changed)
        spin_slider_layout.addWidget(QLabel("Слайдер:"))
        spin_slider_layout.addWidget(self.slider)
        
        spin_slider_group.setLayout(spin_slider_layout)
        layout.addWidget(spin_slider_group)
        
        # QProgressBar
        progress_group = QGroupBox("Прогресс бар")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_button = QPushButton("Запустить анимацию")
        self.progress_button.clicked.connect(self.start_progress_animation)
        progress_layout.addWidget(self.progress_button)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # QTableWidget
        table_group = QGroupBox("Таблица")
        table_layout = QVBoxLayout()
        
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Должность"])
        
        # Заполняем таблицу
        data = [
            ["Иванов Иван", "30", "Разработчик"],
            ["Петрова Мария", "25", "Дизайнер"],
            ["Сидоров Алексей", "35", "Менеджер"],
            ["Козлова Елена", "28", "Тестировщик"],
            ["Морозов Дмитрий", "32", "Архитектор"]
        ]
        
        for i, row_data in enumerate(data):
            for j, cell_data in enumerate(row_data):
                self.table.setItem(i, j, QTableWidgetItem(cell_data))
        
        self.table.cellClicked.connect(self.table_cell_clicked)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # QListWidget
        list_group = QGroupBox("Список")
        list_layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]
        self.list_widget.addItems(items)
        self.list_widget.itemClicked.connect(self.list_item_clicked)
        list_layout.addWidget(self.list_widget)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # QTreeWidget
        tree_group = QGroupBox("Дерево")
        tree_layout = QVBoxLayout()
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Имя", "Значение"])
        
        # Добавляем элементы в дерево
        root_items = ["Отдел 1", "Отдел 2", "Отдел 3"]
        for root_item_text in root_items:
            root_item = QTreeWidgetItem(self.tree_widget)
            root_item.setText(0, root_item_text)
            root_item.setText(1, "Корневой элемент")
            
            # Добавляем дочерние элементы
            for i in range(3):
                child_item = QTreeWidgetItem(root_item)
                child_item.setText(0, f"Сотрудник {i+1}")
                child_item.setText(1, f"Должность {i+1}")
        
        self.tree_widget.itemClicked.connect(self.tree_item_clicked)
        tree_layout.addWidget(self.tree_widget)
        tree_group.setLayout(tree_layout)
        layout.addWidget(tree_group)
        
        central_widget.setLayout(layout)
    
    def checkbox_changed(self, state, checkbox_num):
        """Обработка изменения флажка"""
        if state == Qt.Checked:
            print(f"Флажок {checkbox_num} отмечен")
        else:
            print(f"Флажок {checkbox_num} снят")
    
    def radiobutton_toggled(self, checked, radio_num):
        """Обработка изменения переключателя"""
        if checked:
            print(f"Переключатель {radio_num} выбран")
    
    def combobox_changed(self, text):
        """Обработка изменения комбобокса"""
        print(f"Выбран элемент: {text}")
    
    def spinbox_changed(self, value):
        """Обработка изменения спинбокса"""
        print(f"Значение спинбокса: {value}")
        # Синхронизируем со слайдером
        self.slider.setValue(value)
    
    def slider_changed(self, value):
        """Обработка изменения слайдера"""
        print(f"Значение слайдера: {value}")
        # Синхронизируем со спинбоксом
        self.spin_box.setValue(value)
        # Обновляем прогресс бар
        self.progress_bar.setValue(value)
    
    def start_progress_animation(self):
        """Запускает анимацию прогресса"""
        def update_progress():
            current_value = self.progress_bar.value()
            if current_value < 100:
                self.progress_bar.setValue(current_value + 10)
            else:
                self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(update_progress)
        self.timer.start(200)  # Обновление каждые 200мс
    
    def table_cell_clicked(self, row, column):
        """Обработка клика по ячейке таблицы"""
        item = self.table.item(row, column)
        if item:
            print(f"Клик по ячейке ({row}, {column}): {item.text()}")
    
    def list_item_clicked(self, item):
        """Обработка клика по элементу списка"""
        print(f"Клик по элементу списка: {item.text()}")
    
    def tree_item_clicked(self, item, column):
        """Обработка клика по элементу дерева"""
        print(f"Клик по элементу дерева: {item.text(0)}, колонка: {column}")

# Задание 4: Обработка событий
class EventHandlingApp(QMainWindow):
    """Приложение для демонстрации обработки событий"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Обработка событий")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Canvas для рисования и обработки событий
        self.canvas = QLabel()
        self.canvas.setFixedSize(680, 300)
        self.canvas.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.canvas.setText("Нажмите мышью или клавишей для демонстрации событий")
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setFont(QFont("Arial", 12))
        
        # Включаем возможность получения фокуса и обработки клавиш
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.mousePressEvent = self.canvas_mouse_press
        self.canvas.keyPressEvent = self.canvas_key_press
        
        layout.addWidget(self.canvas)
        
        # Метка для отображения событий
        self.event_label = QLabel("Последнее событие будет отображаться здесь")
        self.event_label.setStyleSheet("border: 1px solid gray; padding: 10px; background-color: lightgray;")
        layout.addWidget(self.event_label)
        
        # Кнопка для сброса событий
        reset_button = QPushButton("Сбросить события")
        reset_button.clicked.connect(self.reset_events)
        layout.addWidget(reset_button)
        
        central_widget.setLayout(layout)
    
    def canvas_mouse_press(self, event):
        """Обработка нажатия мыши на холсте"""
        x, y = event.x(), event.y()
        event_type = ""
        if event.button() == Qt.LeftButton:
            event_type = "Левая кнопка"
        elif event.button() == Qt.RightButton:
            event_type = "Правая кнопка"
        elif event.button() == Qt.MiddleButton:
            event_type = "Средняя кнопка"
        
        event_info = f"Мышь: {event_type} ({x}, {y})"
        self.event_label.setText(event_info)
        self.canvas.setText(f"Нажата {event_type} в ({x}, {y})")
    
    def canvas_key_press(self, event):
        """Обработка нажатия клавиши на холсте"""
        key_info = f"Клавиша: {event.text()} (код: {event.key()})"
        self.event_label.setText(key_info)
        self.canvas.setText(f"Нажата клавиша: {event.text()}")
    
    def reset_events(self):
        """Сброс информации о событиях"""
        self.event_label.setText("Последнее событие будет отображаться здесь")
        self.canvas.setText("Нажмите мышью или клавишей для демонстрации событий")

# Задание 5: Комплексное приложение "Заметки"
class NotesModel:
    """Модель данных для заметок"""
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = []
        self.next_id = 1
        self.load_notes()
    
    def add_note(self, title: str, content: str, category: str = "Общее"):
        """Добавляет заметку"""
        note = {
            'id': self.next_id,
            'title': title,
            'content': content,
            'category': category,
            'created_at': __import__('datetime').datetime.now().isoformat(),
            'updated_at': __import__('datetime').datetime.now().isoformat()
        }
        self.notes.append(note)
        self.next_id += 1
        self.save_notes()
        return note['id']
    
    def update_note(self, note_id: int, title: str = None, content: str = None, category: str = None):
        """Обновляет заметку"""
        for note in self.notes:
            if note['id'] == note_id:
                if title is not None:
                    note['title'] = title
                    note['updated_at'] = __import__('datetime').datetime.now().isoformat()
                if content is not None:
                    note['content'] = content
                    note['updated_at'] = __import__('datetime').datetime.now().isoformat()
                if category is not None:
                    note['category'] = category
                    note['updated_at'] = __import__('datetime').datetime.now().isoformat()
                self.save_notes()
                return True
        return False
    
    def delete_note(self, note_id: int):
        """Удаляет заметку"""
        self.notes = [note for note in self.notes if note['id'] != note_id]
        self.save_notes()
    
    def get_notes(self, category: str = None, search_term: str = None) -> List[Dict[str, Any]]:
        """Получает заметки с фильтрацией"""
        notes = self.notes.copy()
        
        if category:
            notes = [note for note in notes if note['category'] == category]
        
        if search_term:
            search_term = search_term.lower()
            notes = [note for note in notes 
                    if search_term in note['title'].lower() or search_term in note['content'].lower()]
        
        return notes
    
    def get_categories(self) -> List[str]:
        """Получает список всех категорий"""
        categories = set(note['category'] for note in self.notes)
        return sorted(list(categories))
    
    def save_notes(self):
        """Сохраняет заметки в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")
    
    def load_notes(self):
        """Загружает заметки из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
                    if self.notes:
                        self.next_id = max(note['id'] for note in self.notes) + 1
            except Exception as e:
                print(f"Ошибка загрузки заметок: {e}")
                self.notes = []

class NotesView(QWidget):
    """Представление для заметок"""
    note_selected = pyqtSignal(int)
    note_deleted = pyqtSignal(int)
    filter_changed = pyqtSignal(str, str)  # category, search_term
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Панель фильтров
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.StyledPanel)
        filter_layout = QHBoxLayout()
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        self.category_combo.currentTextChanged.connect(self.on_filter_changed)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(self.on_search_changed)
        
        filter_layout.addWidget(QLabel("Категория:"))
        filter_layout.addWidget(self.category_combo)
        filter_layout.addWidget(QLabel("Поиск:"))
        filter_layout.addWidget(self.search_input)
        
        filter_frame.setLayout(filter_layout)
        layout.addWidget(filter_frame)
        
        # Список заметок
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.on_note_selected)
        layout.addWidget(self.notes_list)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def update_notes_list(self, notes: List[Dict[str, Any]], categories: List[str]):
        """Обновляет список заметок"""
        self.notes_list.clear()
        
        # Обновляем категории
        self.category_combo.clear()
        self.category_combo.addItems(["Все категории"] + categories)
        
        # Добавляем заметки
        for note in notes:
            item_text = f"{note['title']} [{note['category']}]"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, note['id'])
            self.notes_list.addItem(item)
    
    def get_selected_note_id(self) -> int:
        """Получает ID выбранной заметки"""
        item = self.notes_list.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None
    
    def on_note_selected(self, item):
        """Обработка выбора заметки"""
        note_id = item.data(Qt.UserRole)
        self.note_selected.emit(note_id)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def on_filter_changed(self):
        """Обработка изменения фильтра категории"""
        category = self.category_combo.currentText()
        if category == "Все категории":
            category = None
        search_term = self.search_input.text()
        self.filter_changed.emit(category, search_term)
    
    def on_search_changed(self):
        """Обработка изменения поискового запроса"""
        category = self.category_combo.currentText()
        if category == "Все категории":
            category = None
        search_term = self.search_input.text()
        self.filter_changed.emit(category, search_term)

class NoteEditor(QWidget):
    """Редактор заметок"""
    note_saved = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.note_id = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Заголовок заметки")
        layout.addWidget(QLabel("Заголовок:"))
        layout.addWidget(self.title_input)
        
        # Категория
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Категория:"))
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        category_layout.addWidget(self.category_input)
        layout.addLayout(category_layout)
        
        # Содержимое
        layout.addWidget(QLabel("Содержимое:"))
        self.content_input = QTextEdit()
        layout.addWidget(self.content_input)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_note)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.cancel_edit)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_note(self, note_id: int, notes: List[Dict[str, Any]]):
        """Загружает заметку для редактирования"""
        self.note_id = note_id
        for note in notes:
            if note['id'] == note_id:
                self.title_input.setText(note['title'])
                self.content_input.setPlainText(note['content'])
                self.category_input.setCurrentText(note['category'])
                break
    
    def save_note(self):
        """Сохраняет заметку"""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        category = self.category_input.currentText().strip()
        
        if not title:
            QMessageBox.warning(self, "Ошибка", "Заголовок не может быть пустым")
            return
        
        if not category:
            category = "Общее"
        
        # Добавим категорию в список возможных категорий
        if category not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
            self.category_input.addItem(category)
        
        self.note_saved.emit()
    
    def cancel_edit(self):
        """Отменяет редактирование"""
        self.title_input.clear()
        self.content_input.clear()
        self.category_input.setCurrentText("")
        self.note_id = None
    
    def get_note_data(self) -> Dict[str, str]:
        """Получает данные текущей заметки"""
        return {
            'title': self.title_input.text().strip(),
            'content': self.content_input.toPlainText().strip(),
            'category': self.category_input.currentText().strip() or "Общее"
        }

class NotesApp(QMainWindow):
    """Комплексное приложение - заметки"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Комплексное приложение (Заметки)")
        self.setGeometry(100, 100, 1000, 700)
        
        # Создаем модель и представления
        self.model = NotesModel()
        self.list_view = NotesView()
        self.editor_view = NoteEditor()
        
        # Создаем меню
        self.create_menu()
        
        # Основной макет
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель - список заметок
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.list_view)
        left_panel.setLayout(left_layout)
        main_splitter.addWidget(left_panel)
        
        # Правая панель - редактор
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.editor_view)
        right_panel.setLayout(right_layout)
        main_splitter.addWidget(right_panel)
        
        main_splitter.setSizes([300, 700])
        
        self.setCentralWidget(main_splitter)
        
        # Подключаем сигналы
        self.list_view.note_selected.connect(self.load_selected_note)
        self.list_view.note_deleted.connect(self.delete_note)
        self.list_view.filter_changed.connect(self.apply_filters)
        self.editor_view.note_saved.connect(self.save_current_note)
        
        # Подключаем кнопки
        self.list_view.add_button.clicked.connect(self.add_new_note)
        self.list_view.edit_button.clicked.connect(self.edit_current_note)
        self.list_view.delete_button.clicked.connect(self.confirm_delete_note)
        
        # Инициализируем список
        self.refresh_notes_list()
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = self.menuBar()
        
        # Меню File
        file_menu = menubar.addMenu("Файл")
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_notes)
        file_menu.addAction(save_action)
        
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_notes)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def refresh_notes_list(self):
        """Обновляет список заметок"""
        notes = self.model.get_notes()
        categories = self.model.get_categories()
        self.list_view.update_notes_list(notes, categories)
    
    def apply_filters(self, category: str, search_term: str):
        """Применяет фильтры к списку заметок"""
        notes = self.model.get_notes(category=category, search_term=search_term)
        categories = self.model.get_categories()
        self.list_view.update_notes_list(notes, categories)
    
    def load_selected_note(self, note_id: int):
        """Загружает выбранную заметку в редактор"""
        all_notes = self.model.get_notes()
        for note in all_notes:
            if note['id'] == note_id:
                self.editor_view.load_note(note_id, all_notes)
                break
    
    def add_new_note(self):
        """Добавляет новую заметку"""
        note_id = self.model.add_note("Новая заметка", "Содержимое новой заметки", "Общее")
        self.refresh_notes_list()
        
        # Выбираем новую заметку в списке
        for i in range(self.list_view.notes_list.count()):
            item = self.list_view.notes_list.item(i)
            if item.data(Qt.UserRole) == note_id:
                self.list_view.notes_list.setCurrentItem(item)
                break
    
    def edit_current_note(self):
        """Редактирует текущую заметку"""
        note_id = self.list_view.get_selected_note_id()
        if note_id:
            self.load_selected_note(note_id)
    
    def save_current_note(self):
        """Сохраняет текущую заметку"""
        note_data = self.editor_view.get_note_data()
        note_id = self.list_view.get_selected_note_id()
        
        if note_id:
            # Обновляем существующую заметку
            self.model.update_note(note_id, 
                                 title=note_data['title'],
                                 content=note_data['content'],
                                 category=note_data['category'])
        else:
            # Создаем новую заметку
            self.model.add_note(note_data['title'], note_data['content'], note_data['category'])
        
        self.refresh_notes_list()
        self.editor_view.cancel_edit()
        QMessageBox.information(self, "Сохранено", "Заметка успешно сохранена!")
    
    def confirm_delete_note(self):
        """Подтверждает удаление заметки"""
        note_id = self.list_view.get_selected_note_id()
        if note_id:
            reply = QMessageBox.question(self, "Подтверждение", 
                                       "Удалить выбранную заметку?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_note(note_id)
    
    def delete_note(self, note_id: int):
        """Удаляет заметку"""
        self.model.delete_note(note_id)
        self.refresh_notes_list()
        self.editor_view.cancel_edit()
        QMessageBox.information(self, "Удалено", "Заметка успешно удалена!")
    
    def save_notes(self):
        """Сохраняет все заметки"""
        self.model.save_notes()
        QMessageBox.information(self, "Сохранено", "Все заметки сохранены!")
    
    def load_notes(self):
        """Загружает все заметки"""
        self.model.load_notes()
        self.refresh_notes_list()
        QMessageBox.information(self, "Загружено", "Заметки успешно загружены!")

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 22 ===")
    
    print("\n1. Задание 1: Основы PyQt")
    # app1 = QApplication(sys.argv)
    # basic_app = BasicPyQtApp()
    # basic_app.show()
    # sys.exit(app1.exec_())  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Задание 2: Компоновка элементов")
    # app2 = QApplication(sys.argv)
    # layout_app = LayoutApp()
    # layout_app.show()
    # sys.exit(app2.exec_())  # Закомментировано
    
    print("\n3. Задание 3: Виджеты PyQt")
    # app3 = QApplication(sys.argv)
    # widgets_app = WidgetsApp()
    # widgets_app.show()
    # sys.exit(app3.exec_())  # Закомментировано
    
    print("\n4. Задание 4: Обработка событий")
    # app4 = QApplication(sys.argv)
    # event_app = EventHandlingApp()
    # event_app.show()
    # sys.exit(app4.exec_())  # Закомментировано
    
    print("\n5. Задание 5: Комплексное приложение (Заметки)")
    # app5 = QApplication(sys.argv)
    # notes_app = NotesApp()
    # notes_app.show()
    # sys.exit(app5.exec_())  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")