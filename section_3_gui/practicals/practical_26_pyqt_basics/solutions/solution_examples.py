# Решения для практического занятия 21: Создание GUI с помощью PyQt

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                            QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
                            QCheckBox, QRadioButton, QComboBox, QSpinBox, QSlider, 
                            QProgressBar, QTableWidgetItem, QListWidget, QTreeWidget,
                            QMessageBox, QTabWidget, QMenuBar, QStatusBar, QToolBar,
                            QTextEdit, QFrame, QSplitter, QGroupBox, QFileDialog, QColorDialog)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor
import json
import os
from typing import Dict, Any, List

# Решение задания 1: Основы PyQt
class BasicPyQtSolution(QMainWindow):
    """Решение для задания 1: Основы PyQt"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 1: Основы PyQt")
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

# Решение задания 2: Компоновка элементов
class LayoutSolution(QMainWindow):
    """Решение для задания 2: Компоновка элементов"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 2: Компоновка элементов")
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
        
        # Поля формы
        self.name_field = QLineEdit()
        self.email_field = QLineEdit()
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(0, 120)
        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.submit_form)
        
        layout.addRow("Имя:", self.name_field)
        layout.addRow("Email:", self.email_field)
        layout.addRow("Возраст:", self.age_spinbox)
        layout.addRow(self.submit_button)
        
        tab.setLayout(layout)
        return tab
    
    def show_layout_info(self, button_num, layout_type):
        """Показывает информацию о нажатии кнопки в макете"""
        QMessageBox.information(self, "Информация", 
                               f"Нажата кнопка {button_num} в {layout_type} макете")
    
    def submit_form(self):
        """Обработка отправки формы"""
        name = self.name_field.text()
        email = self.email_field.text()
        age = self.age_spinbox.value()
        
        info = f"Имя: {name}\nEmail: {email}\nВозраст: {age}"
        QMessageBox.information(self, "Данные формы", info)

# Решение задания 3: Виджеты PyQt
class WidgetsSolution(QMainWindow):
    """Решение для задания 3: Виджеты PyQt"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 3: Виджеты PyQt")
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

# Решение задания 4: Обработка событий
class EventHandlingSolution(QMainWindow):
    """Решение для задания 4: Обработка событий"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 4: Обработка событий")
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

# Решение задания 5: Комплексное приложение "Калькулятор"
class CalculatorSolution(QMainWindow):
    """Решение для задания 5: Комплексное приложение - калькулятор"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 5: Калькулятор на PyQt")
        self.setGeometry(100, 100, 400, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Дисплей калькулятора
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 16))
        self.display.setStyleSheet("padding: 10px; font-size: 18px; background-color: #f0f0f0;")
        layout.addWidget(self.display)
        
        # Кнопки калькулятора
        button_layout = QGridLayout()
        
        # Определяем кнопки
        buttons = [
            ("C", 0, 0), ("±", 0, 1), ("%", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("", 4, 2), ("=", 4, 3)
        ]
        
        self.buttons = {}
        for text, row, col in buttons:
            if text:
                button = QPushButton(text)
                button.setFont(QFont("Arial", 14))
                button.clicked.connect(lambda _, t=text: self.button_clicked(t))
                button_layout.addWidget(button, row, col)
                self.buttons[text] = button
        
        # Кнопка 0 занимает 2 колонки
        zero_button = self.buttons["0"]
        button_layout.addWidget(zero_button, 4, 0, 1, 2)  # rowspan=1, colspan=2
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        
        # Переменные состояния калькулятора
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_on_next_input = False
    
    def button_clicked(self, text):
        """Обработка нажатия кнопки калькулятора"""
        if text.isdigit() or text == ".":
            self.input_number(text)
        elif text in ["+", "-", "×", "÷"]:
            self.input_operator(text)
        elif text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_all()
        elif text == "±":
            self.change_sign()
        elif text == "%":
            self.percentage()
    
    def input_number(self, digit):
        """Ввод цифры"""
        if self.reset_on_next_input:
            self.current_input = "0"
            self.reset_on_next_input = False
        
        if digit == "." and "." in self.current_input:
            return  # Не допускаем двойную точку
        
        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.display.setText(self.current_input)
    
    def input_operator(self, op):
        """Ввод оператора"""
        if self.operator and not self.reset_on_next_input:
            self.calculate_result()
        
        self.previous_input = self.current_input
        self.operator = op
        self.reset_on_next_input = True
    
    def calculate_result(self):
        """Вычисление результата"""
        if self.operator and self.previous_input:
            try:
                prev_num = float(self.previous_input)
                curr_num = float(self.current_input)
                
                if self.operator == "+":
                    result = prev_num + curr_num
                elif self.operator == "-":
                    result = prev_num - curr_num
                elif self.operator == "×":
                    result = prev_num * curr_num
                elif self.operator == "÷":
                    if curr_num == 0:
                        QMessageBox.critical(self, "Ошибка", "Деление на ноль!")
                        return
                    result = prev_num / curr_num
                else:
                    return
                
                # Форматируем результат
                if result == int(result):
                    result = int(result)
                
                self.current_input = str(result)
                self.display.setText(self.current_input)
                self.operator = ""
                self.previous_input = ""
                self.reset_on_next_input = True
            except ValueError:
                QMessageBox.critical(self, "Ошибка", "Неверный ввод!")
    
    def clear_all(self):
        """Очистка всего"""
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.reset_on_next_input = False
        self.display.setText("0")
    
    def change_sign(self):
        """Изменение знака числа"""
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display.setText(self.current_input)
    
    def percentage(self):
        """Вычисление процента"""
        try:
            num = float(self.current_input) / 100
            self.current_input = str(num)
            self.display.setText(self.current_input)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Неверный ввод!")

# Дополнительные примеры использования виджетов PyQt
class AdvancedWidgetsExamples:
    """Дополнительные примеры продвинутого использования виджетов PyQt"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры виджетов PyQt")
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
        
        # Заполняем Treeview
        data = {
            "Пользователь": "Иванов Иван",
            "Email": "ivanov@example.com",
            "Телефон": "+7 (999) 123-45-67"
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
        
        # Запускаем анимацию в отдельном потоке, чтобы не блокировать интерфейс
        animation_thread = threading.Thread(target=animate)
        animation_thread.daemon = True
        animation_thread.start()
    
    def start_indeterminate(self):
        """Запускает неопределенный прогресс бар"""
        self.indeterminate_pb.start(10)  # Обновление каждые 10мс
    
    def stop_indeterminate(self):
        """Останавливает неопределенный прогресс бар"""
        self.indeterminate_pb.stop()
    
    def run(self):
        self.root.mainloop()

def demonstrate_pyqt_patterns():
    """Демонстрирует различные паттерны использования PyQt"""
    print("=== Демонстрация паттернов использования PyQt ===")
    
    print("\n1. Основы PyQt:")
    # basic_app = BasicPyQtSolution()
    # basic_app.show()
    
    print("\n2. Компоновка элементов:")
    # layout_app = LayoutSolution()
    # layout_app.show()
    
    print("\n3. Виджеты PyQt:")
    # widgets_app = WidgetsSolution()
    # widgets_app.show()
    
    print("\n4. Обработка событий:")
    # event_app = EventHandlingSolution()
    # event_app.show()
    
    print("\n5. Комплексное приложение (Калькулятор):")
    # calc_app = CalculatorSolution()
    # calc_app.show()
    
    print("\n6. Дополнительные примеры:")
    # advanced_app = AdvancedWidgetsExamples()
    # advanced_app.run()
    
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")

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
    print("=== Решения для практического занятия 21 ===")
    
    print("\n1. Решение задания 1: Основы PyQt")
    # app1 = QApplication(sys.argv)
    # basic_solution = BasicPyQtSolution()
    # basic_solution.show()
    # sys.exit(app1.exec_())  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Решение задания 2: Компоновка элементов")
    # app2 = QApplication(sys.argv)
    # layout_solution = LayoutSolution()
    # layout_solution.show()
    # sys.exit(app2.exec_())  # Закомментировано
    
    print("\n3. Решение задания 3: Виджеты PyQt")
    # app3 = QApplication(sys.argv)
    # widgets_solution = WidgetsSolution()
    # widgets_solution.show()
    # sys.exit(app3.exec_())  # Закомментировано
    
    print("\n4. Решение задания 4: Обработка событий")
    # app4 = QApplication(sys.argv)
    # event_solution = EventHandlingSolution()
    # event_solution.show()
    # sys.exit(app4.exec_())  # Закомментировано
    
    print("\n5. Решение задания 5: Комплексное приложение (Калькулятор)")
    # app5 = QApplication(sys.argv)
    # calc_solution = CalculatorSolution()
    # calc_solution.show()
    # sys.exit(app5.exec_())  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    demonstrate_pyqt_patterns()
    compare_pyqt_tkinter_implementations()
    
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")