# Решения для практического занятия 22: PyQt - проектирование UI

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
import threading
import time

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
        
        # Вкладка с вложенными макетами
        nested_tab = self.create_nested_layout_tab()
        tab_widget.addTab(nested_tab, "Вложенные")
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        central_widget.setLayout(layout)
    
    def create_vertical_layout_tab(self):
        """Создает вкладку с вертикальным макетом"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Группировка элементов
        group1 = QGroupBox("Группа 1")
        group1_layout = QVBoxLayout()
        for i in range(3):
            btn = QPushButton(f"Кнопка {i+1} (группа 1)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "вертикальный (группа 1)"))
            group1_layout.addWidget(btn)
        group1.setLayout(group1_layout)
        layout.addWidget(group1)
        
        group2 = QGroupBox("Группа 2")
        group2_layout = QVBoxLayout()
        for i in range(2):
            btn = QPushButton(f"Кнопка {i+1} (группа 2)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "вертикальный (группа 2)"))
            group2_layout.addWidget(btn)
        group2.setLayout(group2_layout)
        layout.addWidget(group2)
        
        # Добавляем текстовое поле в конец
        text_field = QLineEdit("Текстовое поле в вертикальном макете")
        layout.addWidget(text_field)
        
        tab.setLayout(layout)
        return tab
    
    def create_horizontal_layout_tab(self):
        """Создает вкладку с горизонтальным макетом"""
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Группировка элементов
        group1 = QGroupBox("Группа 1")
        group1_layout = QHBoxLayout()
        for i in range(3):
            btn = QPushButton(f"Кнопка {i+1} (гориз.)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "горизонтальный (группа 1)"))
            group1_layout.addWidget(btn)
        group1.setLayout(group1_layout)
        layout.addWidget(group1)
        
        group2 = QGroupBox("Группа 2")
        group2_layout = QHBoxLayout()
        for i in range(2):
            btn = QPushButton(f"Кнопка {i+1} (гориз.)")
            btn.clicked.connect(lambda _, x=i+1: self.show_layout_info(x, "горизонтальный (группа 2)"))
            group2_layout.addWidget(btn)
        group2.setLayout(group2_layout)
        layout.addWidget(group2)
        
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
        self.age_field = QSpinBox()
        self.age_field.setRange(0, 120)
        self.age_field.setValue(25)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Мужской", "Женский", "Другой"])
        
        layout.addRow("Имя:", self.name_field)
        layout.addRow("Email:", self.email_field)
        layout.addRow("Возраст:", self.age_field)
        layout.addRow("Пол:", self.gender_combo)
        
        submit_btn = QPushButton("Отправить")
        submit_btn.clicked.connect(self.submit_form)
        layout.addRow(submit_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_nested_layout_tab(self):
        """Создает вкладку с вложенными макетами"""
        tab = QWidget()
        main_layout = QVBoxLayout()
        
        # Верхняя часть - горизонтальный макет
        top_section = QFrame()
        top_section.setFrameStyle(QFrame.StyledPanel)
        top_layout = QHBoxLayout()
        
        top_layout.addWidget(QLabel("Элемент 1"))
        top_layout.addWidget(QPushButton("Кнопка 1"))
        top_layout.addWidget(QLineEdit())
        
        top_section.setLayout(top_layout)
        main_layout.addWidget(top_section)
        
        # Средняя часть - сеточный макет
        middle_section = QFrame()
        middle_section.setFrameStyle(QFrame.StyledPanel)
        middle_layout = QGridLayout()
        
        labels = ["Метка 1", "Метка 2", "Метка 3", "Метка 4"]
        for i, text in enumerate(labels):
            row = i // 2
            col = i % 2
            middle_layout.addWidget(QLabel(text), row, col)
        
        middle_section.setLayout(middle_layout)
        main_layout.addWidget(middle_section)
        
        # Нижняя часть - вертикальный макет
        bottom_section = QFrame()
        bottom_section.setFrameStyle(QFrame.StyledPanel)
        bottom_layout = QVBoxLayout()
        
        for i in range(3):
            bottom_layout.addWidget(QPushButton(f"Кнопка {i+1} (нижняя)"))
        
        bottom_section.setLayout(bottom_layout)
        main_layout.addWidget(bottom_section)
        
        tab.setLayout(main_layout)
        return tab
    
    def show_layout_info(self, button_num, layout_type):
        """Показывает информацию о нажатом элементе"""
        QMessageBox.information(self, "Информация", 
                               f"Нажата кнопка {button_num} в {layout_type} макете")
    
    def submit_form(self):
        """Обработка отправки формы"""
        name = self.name_field.text()
        email = self.email_field.text()
        age = self.age_field.value()
        gender = self.gender_combo.currentText()
        
        info = f"Имя: {name}\nEmail: {email}\nВозраст: {age}\nПол: {gender}"
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
        
        # Создаем вкладки для разных виджетов
        tab_widget = QTabWidget()
        
        # Вкладка чекбоксов
        checkbox_tab = self.create_checkbox_tab()
        tab_widget.addTab(checkbox_tab, "Чекбоксы")
        
        # Вкладка радиокнопок
        radio_tab = self.create_radio_tab()
        tab_widget.addTab(radio_tab, "Радиокнопки")
        
        # Вкладка комбобоксов
        combo_tab = self.create_combo_tab()
        tab_widget.addTab(combo_tab, "Комбобоксы")
        
        # Вкладка спинбоксов и слайдеров
        spin_slider_tab = self.create_spin_slider_tab()
        tab_widget.addTab(spin_slider_tab, "Спинбоксы и слайдеры")
        
        # Вкладка прогресс баров
        progress_tab = self.create_progress_tab()
        tab_widget.addTab(progress_tab, "Прогресс бары")
        
        # Вкладка таблиц
        table_tab = self.create_table_tab()
        tab_widget.addTab(table_tab, "Таблицы")
        
        # Вкладка списков
        list_tab = self.create_list_tab()
        tab_widget.addTab(list_tab, "Списки")
        
        # Вкладка деревьев
        tree_tab = self.create_tree_tab()
        tab_widget.addTab(tree_tab, "Деревья")
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        central_widget.setLayout(layout)
    
    def create_checkbox_tab(self):
        """Создает вкладку с чекбоксами"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Группа чекбоксов
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
        
        # Кнопка для получения состояния чекбоксов
        get_state_btn = QPushButton("Получить состояние чекбоксов")
        get_state_btn.clicked.connect(self.get_checkbox_states)
        layout.addWidget(get_state_btn)
        
        self.checkbox_state_label = QLabel("Состояния чекбоксов будут здесь")
        layout.addWidget(self.checkbox_state_label)
        
        tab.setLayout(layout)
        return tab
    
    def create_radio_tab(self):
        """Создает вкладку с радиокнопками"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Группа радиокнопок
        radio_group = QGroupBox("Радиокнопки")
        radio_layout = QVBoxLayout()
        
        self.radiobuttons = []
        options = ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"]
        for i, option in enumerate(options):
            rb = QRadioButton(option)
            rb.toggled.connect(lambda checked, x=i+1: self.radiobutton_toggled(checked, x))
            radio_layout.addWidget(rb)
            self.radiobuttons.append(rb)
        
        radio_group.setLayout(radio_layout)
        layout.addWidget(radio_group)
        
        # Кнопка для получения выбранного варианта
        get_selected_btn = QPushButton("Получить выбранный вариант")
        get_selected_btn.clicked.connect(self.get_selected_radio)
        layout.addWidget(get_selected_btn)
        
        self.radio_selection_label = QLabel("Выбранный вариант будет здесь")
        layout.addWidget(self.radio_selection_label)
        
        tab.setLayout(layout)
        return tab
    
    def create_combo_tab(self):
        """Создает вкладку с комбобоксами"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Комбобокс с элементами
        self.combobox = QComboBox()
        self.combobox.addItems(["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"])
        self.combobox.setEditable(True)
        self.combobox.currentTextChanged.connect(self.combobox_changed)
        layout.addWidget(QLabel("Комбобокс:"))
        layout.addWidget(self.combobox)
        
        # Кнопка для добавления элемента
        add_item_btn = QPushButton("Добавить элемент")
        add_item_btn.clicked.connect(self.add_combo_item)
        layout.addWidget(add_item_btn)
        
        # Кнопка для получения текущего элемента
        get_current_btn = QPushButton("Получить текущий элемент")
        get_current_btn.clicked.connect(self.get_current_combo_item)
        layout.addWidget(get_current_btn)
        
        self.combo_selection_label = QLabel("Выбранный элемент будет здесь")
        layout.addWidget(self.combo_selection_label)
        
        tab.setLayout(layout)
        return tab
    
    def create_spin_slider_tab(self):
        """Создает вкладку со спинбоксами и слайдерами"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Спинбокс
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("Спинбокс:"))
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        self.spin_box.valueChanged.connect(self.spinbox_changed)
        spin_layout.addWidget(self.spin_box)
        layout.addLayout(spin_layout)
        
        # Слайдер
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Слайдер:"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slider_changed)
        slider_layout.addWidget(self.slider)
        layout.addLayout(slider_layout)
        
        # Синхронизация
        sync_frame = QFrame()
        sync_frame.setFrameStyle(QFrame.StyledPanel)
        sync_layout = QVBoxLayout()
        
        sync_label = QLabel("Значения будут синхронизированы")
        sync_layout.addWidget(sync_label)
        
        # Кнопки для синхронизации
        sync_btns_layout = QHBoxLayout()
        sync_to_slider_btn = QPushButton("Спинбокс -> Слайдер")
        sync_to_slider_btn.clicked.connect(lambda: self.slider.setValue(self.spin_box.value()))
        sync_to_spin_btn = QPushButton("Слайдер -> Спинбокс")
        sync_to_spin_btn.clicked.connect(lambda: self.spin_box.setValue(self.slider.value()))
        sync_btns_layout.addWidget(sync_to_slider_btn)
        sync_btns_layout.addWidget(sync_to_spin_btn)
        sync_layout.addLayout(sync_btns_layout)
        
        sync_frame.setLayout(sync_layout)
        layout.addWidget(sync_frame)
        
        tab.setLayout(layout)
        return tab
    
    def create_progress_tab(self):
        """Создает вкладку с прогресс барами"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Определенный прогресс бар
        det_progress_frame = QGroupBox("Определенный прогресс бар")
        det_progress_layout = QVBoxLayout()
        
        self.determinate_pb = QProgressBar()
        self.determinate_pb.setValue(30)
        det_progress_layout.addWidget(self.determinate_pb)
        
        det_control_layout = QHBoxLayout()
        inc_btn = QPushButton("Увеличить")
        inc_btn.clicked.connect(lambda: self.determinate_pb.setValue(min(100, self.determinate_pb.value() + 10)))
        dec_btn = QPushButton("Уменьшить")
        dec_btn.clicked.connect(lambda: self.determinate_pb.setValue(max(0, self.determinate_pb.value() - 10)))
        reset_btn = QPushButton("Сброс")
        reset_btn.clicked.connect(lambda: self.determinate_pb.setValue(0))
        det_control_layout.addWidget(inc_btn)
        det_control_layout.addWidget(dec_btn)
        det_control_layout.addWidget(reset_btn)
        det_progress_layout.addLayout(det_control_layout)
        
        det_progress_frame.setLayout(det_progress_layout)
        layout.addWidget(det_progress_frame)
        
        # Неопределенный прогресс бар
        indet_progress_frame = QGroupBox("Неопределенный прогресс бар")
        indet_progress_layout = QVBoxLayout()
        
        self.indeterminate_pb = QProgressBar()
        self.indeterminate_pb.setRange(0, 0)  # Неопределенный режим
        indet_progress_layout.addWidget(self.indeterminate_pb)
        
        indet_control_layout = QHBoxLayout()
        start_btn = QPushButton("Старт")
        start_btn.clicked.connect(lambda: self.indeterminate_pb.setRange(0, 0))
        stop_btn = QPushButton("Стоп")
        stop_btn.clicked.connect(lambda: self.indeterminate_pb.setRange(0, 100))
        indet_control_layout.addWidget(start_btn)
        indet_control_layout.addWidget(stop_btn)
        indet_progress_layout.addLayout(indet_control_layout)
        
        indet_progress_frame.setLayout(indet_progress_layout)
        layout.addWidget(indet_progress_frame)
        
        tab.setLayout(layout)
        return tab
    
    def create_table_tab(self):
        """Создает вкладку с таблицами"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Таблица
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Должность", "Зарплата"])
        
        # Заполняем таблицу
        data = [
            ["Иванов Иван", "30", "Разработчик", "120000"],
            ["Петрова Мария", "25", "Дизайнер", "90000"],
            ["Сидоров Алексей", "35", "Менеджер", "150000"],
            ["Козлова Елена", "28", "Тестировщик", "85000"],
            ["Морозов Дмитрий", "32", "Архитектор", "180000"]
        ]
        
        for i, row_data in enumerate(data):
            for j, cell_data in enumerate(row_data):
                self.table.setItem(i, j, QTableWidgetItem(cell_data))
        
        self.table.cellClicked.connect(self.table_cell_clicked)
        layout.addWidget(QLabel("Таблица сотрудников:"))
        layout.addWidget(self.table)
        
        # Кнопка для добавления строки
        add_row_btn = QPushButton("Добавить строку")
        add_row_btn.clicked.connect(self.add_table_row)
        layout.addWidget(add_row_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_list_tab(self):
        """Создает вкладку со списками"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Список
        self.list_widget = QListWidget()
        items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]
        self.list_widget.addItems(items)
        self.list_widget.itemClicked.connect(self.list_item_clicked)
        layout.addWidget(QLabel("Список элементов:"))
        layout.addWidget(self.list_widget)
        
        # Кнопки управления
        list_control_layout = QHBoxLayout()
        add_item_btn = QPushButton("Добавить элемент")
        add_item_btn.clicked.connect(self.add_list_item)
        remove_item_btn = QPushButton("Удалить элемент")
        remove_item_btn.clicked.connect(self.remove_list_item)
        list_control_layout.addWidget(add_item_btn)
        list_control_layout.addWidget(remove_item_btn)
        layout.addLayout(list_control_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_tree_tab(self):
        """Создает вкладку с деревьями"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Дерево
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Имя", "Должность", "Зарплата"])
        
        # Добавляем элементы в дерево
        departments = ["Отдел разработки", "Отдел дизайна", "Отдел управления"]
        employees = {
            "Отдел разработки": [
                ("Иванов Иван", "Старший разработчик", "150000"),
                ("Петров Петр", "Младший разработчик", "90000")
            ],
            "Отдел дизайна": [
                ("Сидорова Мария", "Главный дизайнер", "120000"),
                ("Козлова Анна", "Дизайнер", "80000")
            ],
            "Отдел управления": [
                ("Морозов Алексей", "Руководитель", "200000"),
                ("Волкова Елена", "Менеджер", "100000")
            ]
        }
        
        for dept_name in departments:
            dept_item = QTreeWidgetItem(self.tree_widget)
            dept_item.setText(0, dept_name)
            dept_item.setText(1, "Отдел")
            dept_item.setText(2, "")
            
            for emp_name, emp_pos, emp_salary in employees[dept_name]:
                emp_item = QTreeWidgetItem(dept_item)
                emp_item.setText(0, emp_name)
                emp_item.setText(1, emp_pos)
                emp_item.setText(2, emp_salary)
        
        self.tree_widget.itemClicked.connect(self.tree_item_clicked)
        layout.addWidget(QLabel("Дерево сотрудников по отделам:"))
        layout.addWidget(self.tree_widget)
        
        tab.setLayout(layout)
        return tab
    
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
    
    def get_checkbox_states(self):
        """Получает состояние всех чекбоксов"""
        states = []
        for i, cb in enumerate(self.checkboxes):
            state = "отмечен" if cb.isChecked() else "не отмечен"
            states.append(f"Флажок {i+1}: {state}")
        self.checkbox_state_label.setText("; ".join(states))
    
    def get_selected_radio(self):
        """Получает выбранный вариант радиокнопки"""
        for i, rb in enumerate(self.radiobuttons):
            if rb.isChecked():
                self.radio_selection_label.setText(f"Выбран вариант: {i+1}")
                return
        self.radio_selection_label.setText("Ничего не выбрано")
    
    def add_combo_item(self):
        """Добавляет элемент в комбобокс"""
        text, ok = QInputDialog.getText(self, "Добавить элемент", "Введите текст элемента:")
        if ok and text:
            self.combobox.addItem(text)
    
    def get_current_combo_item(self):
        """Получает текущий элемент комбобокса"""
        current_text = self.combobox.currentText()
        self.combo_selection_label.setText(f"Текущий элемент: {current_text}")
    
    def table_cell_clicked(self, row, column):
        """Обработка клика по ячейке таблицы"""
        item = self.table.item(row, column)
        if item:
            print(f"Клик по ячейке ({row}, {column}): {item.text()}")
    
    def add_table_row(self):
        """Добавляет строку в таблицу"""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem(f"Новый сотрудник {row_count+1}"))
        self.table.setItem(row_count, 1, QTableWidgetItem("25"))
        self.table.setItem(row_count, 2, QTableWidgetItem("Стажер"))
        self.table.setItem(row_count, 3, QTableWidgetItem("50000"))
    
    def list_item_clicked(self, item):
        """Обработка клика по элементу списка"""
        print(f"Клик по элементу списка: {item.text()}")
    
    def add_list_item(self):
        """Добавляет элемент в список"""
        text, ok = QInputDialog.getText(self, "Добавить элемент", "Введите текст элемента:")
        if ok and text:
            self.list_widget.addItem(text)
    
    def remove_list_item(self):
        """Удаляет выбранный элемент из списка"""
        selected = self.list_widget.currentItem()
        if selected:
            self.list_widget.takeItem(self.list_widget.row(selected))
    
    def tree_item_clicked(self, item, column):
        """Обработка клика по элементу дерева"""
        print(f"Клик по элементу дерева: {item.text(0)}, колонка: {column}")

# Решение задания 4: Обработка событий
class EventHandlingSolution(QMainWindow):
    """Решение для задания 4: Обработка событий"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение задания 4: Обработка событий")
        self.setGeometry(100, 100, 700, 600)
        
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
        
        # Дополнительные примеры обработки событий
        events_group = QGroupBox("Примеры обработки событий")
        events_layout = QVBoxLayout()
        
        # Кнопка с несколькими обработчиками
        multi_event_btn = QPushButton("Кнопка с несколькими событиями")
        multi_event_btn.clicked.connect(lambda: self.event_label.setText("Клик по кнопке"))
        multi_event_btn.mousePressEvent = lambda event: self.event_label.setText("Нажата кнопка мыши на кнопке")
        multi_event_btn.enterEvent = lambda event: self.event_label.setText("Курсор над кнопкой")
        multi_event_btn.leaveEvent = lambda event: self.event_label.setText("Курсор покинул кнопку")
        events_layout.addWidget(multi_event_btn)
        
        # Поле ввода с обработкой событий
        input_field = QLineEdit()
        input_field.setPlaceholderText("Поле ввода с событиями")
        input_field.textChanged.connect(lambda text: self.event_label.setText(f"Текст изменен: {text[:20]}..."))
        input_field.returnPressed.connect(lambda: self.event_label.setText("Нажата клавиша Enter"))
        events_layout.addWidget(input_field)
        
        events_group.setLayout(events_layout)
        layout.addWidget(events_group)
        
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
class AdvancedFeaturesExamples:
    """Дополнительные примеры продвинутых возможностей PyQt"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры продвинутых возможностей PyQt")
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
    
    def focus_in(self, event):
        if self.get() == self.placeholder and self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self.config(fg=self.default_fg_color)
    
    def focus_out(self, event):
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

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 22 ===")
    
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
    # advanced_solution = AdvancedFeaturesExamples()
    # advanced_solution.run()  # Закомментировано
    
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")