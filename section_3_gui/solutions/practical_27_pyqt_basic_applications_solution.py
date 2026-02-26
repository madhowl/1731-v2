#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 27: PyQt6 - базовые приложения
Решение задач по основам создания приложений PyQt6

Автор: AI Assistant
"""

# Используем PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFormLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QComboBox, QMenuBar, QMenu, QToolBar,
    QStatusBar, QFileDialog, QColorDialog, QInputDialog,
    QMessageBox, QFontDialog, QDialogButtonBox, QGroupBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QCheckBox,
    QRadioButton, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem,
    QScrollArea, QSplitter, QFrame, QScrollBar
)
from PyQt6.QtCore import Qt, PYQT_VERSION
from PyQt6.QtGui import QAction, QFont, QIcon, QKeySequence


# ==============================================================================
# ЗАДАЧА 1: Базовое приложение
# ==============================================================================

class BasicAppDemo(QMainWindow):
    """Демонстрация базового приложения PyQt"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 1: Базовое приложение")
        self.setGeometry(100, 100, 400, 300)
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Макет
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Заголовок
        title = QLabel("Мое первое PyQt6 приложение!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Описание
        description = QLabel(
            "PyQt версия: 6\n"
            "Нажмите кнопку ниже"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        # Кнопка
        self.button = QPushButton("Нажми меня")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)
        
        # Статус бар
        self.statusBar().showMessage("Готов")
    
    def on_button_click(self):
        """Обработка нажатия кнопки"""
        self.statusBar().showMessage("Кнопка нажата!", 3000)
        QMessageBox.information(self, "Информация", "Кнопка была нажата!")


# ==============================================================================
# ЗАДАЧА 2: Основные виджеты
# ==============================================================================

class WidgetsDemo(QMainWindow):
    """Демонстрация основных виджетов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 2: Основные виджеты")
        self.setGeometry(100, 100, 500, 600)
        
        # Центральный виджет с вкладками
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        # Вкладка 1: Базовые виджеты
        tab1 = QWidget()
        tabs.addTab(tab1, "Базовые")
        self.create_basic_widgets_tab(tab1)
        
        # Вкладка 2: Ввод текста
        tab2 = QWidget()
        tabs.addTab(tab2, "Ввод текста")
        self.create_text_input_tab(tab2)
        
        # Вкладка 3: Выбор
        tab3 = QWidget()
        tabs.addTab(tab3, "Выбор")
        self.create_selection_tab(tab3)
    
    def create_basic_widgets_tab(self, parent):
        """Вкладка базовых виджетов"""
        layout = QVBoxLayout()
        
        # Кнопки
        layout.addWidget(QLabel("Кнопки:"))
        
        btn1 = QPushButton("Обычная кнопка")
        btn1.clicked.connect(lambda: self.show_message("Нажата обычная кнопка"))
        layout.addWidget(btn1)
        
        btn2 = QPushButton("Кнопка с иконкой")
        btn2.clicked.connect(lambda: self.show_message("Нажата кнопка с иконкой"))
        layout.addWidget(btn2)
        
        # Метки
        layout.addWidget(QLabel("\nМетки:"))
        
        label1 = QLabel("Обычная метка")
        layout.addWidget(label1)
        
        label2 = QLabel("Метка со ссылкой")
        label2.setOpenExternalLinks(True)
        layout.addWidget(label2)
        
        label3 = QLabel("Выровненная метка")
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label3.setStyleSheet("background-color: #e0e0e0; padding: 10px;")
        layout.addWidget(label3)
        
        # Прогресс бар
        layout.addWidget(QLabel("\nПрогресс:"))
        
        progress = QProgressBar()
        progress.setValue(75)
        layout.addWidget(progress)
        
        layout.addStretch()
        parent.setLayout(layout)
    
    def create_text_input_tab(self, parent):
        """Вкладка ввода текста"""
        layout = QFormLayout()
        
        # Однострочный ввод
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        layout.addRow("Имя:", self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@mail.ru")
        layout.addRow("Email:", self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        layout.addRow("Пароль:", self.password_input)
        
        # Многострочный ввод
        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Введите комментарий...")
        self.comment_input.setMaximumHeight(100)
        layout.addRow("Комментарий:", self.comment_input)
        
        # Выпадающий список
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Россия", "Украина", "Беларусь", "Казахстан", "Другое"])
        layout.addRow("Страна:", self.country_combo)
        
        # Кнопка отправки
        submit_btn = QPushButton("Отправить")
        submit_btn.clicked.connect(self.on_submit)
        layout.addRow("", submit_btn)
        
        parent.setLayout(layout)
    
    def create_selection_tab(self, parent):
        """Вкладка выбора"""
        layout = QVBoxLayout()
        
        # Чекбоксы
        layout.addWidget(QLabel("Чекбоксы:"))
        
        self.check1 = QCheckBox("Пункт 1")
        self.check2 = QCheckBox("Пункт 2")
        self.check3 = QCheckBox("Пункт 3")
        
        layout.addWidget(self.check1)
        layout.addWidget(self.check2)
        layout.addWidget(self.check3)
        
        # Радио кнопки
        layout.addWidget(QLabel("\nРадио кнопки:"))
        
        self.radio1 = QRadioButton("Вариант A")
        self.radio2 = QRadioButton("Вариант B")
        self.radio3 = QRadioButton("Вариант C")
        
        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)
        layout.addWidget(self.radio3)
        
        # Спинбокс
        layout.addWidget(QLabel("\nСпинбокс:"))
        
        spin_layout = QHBoxLayout()
        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(50)
        spin_layout.addWidget(spin)
        
        double_spin = QDoubleSpinBox()
        double_spin.setRange(0, 100)
        double_spin.setValue(3.14)
        double_spin.setDecimals(2)
        spin_layout.addWidget(double_spin)
        
        layout.addLayout(spin_layout)
        
        # Слайдер
        layout.addWidget(QLabel("\nСлайдер:"))
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        layout.addWidget(slider)
        
        layout.addStretch()
        parent.setLayout(layout)
    
    def on_submit(self):
        """Обработка отправки формы"""
        name = self.name_input.text()
        email = self.email_input.text()
        country = self.country_combo.currentText()
        
        message = f"Имя: {name}\nEmail: {email}\nСтрана: {country}"
        self.show_message(message)
    
    def show_message(self, text):
        """Показать сообщение"""
        QMessageBox.information(self, "Информация", text)


# ==============================================================================
# ЗАДАЧА 3: Компоновка
# ==============================================================================

class LayoutDemo(QMainWindow):
    """Демонстрация компоновки виджетов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 3: Компоновка")
        self.setGeometry(100, 100, 600, 500)
        
        # Центральный виджет с вкладками
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        
        # Вкладка 1: Вертикальная компоновка
        tab1 = QWidget()
        tabs.addTab(tab1, "Вертикальная")
        self.create_vbox_layout(tab1)
        
        # Вкладка 2: Горизонтальная компоновка
        tab2 = QWidget()
        tabs.addTab(tab2, "Горизонтальная")
        self.create_hbox_layout(tab2)
        
        # Вкладка 3: Сетка
        tab3 = QWidget()
        tabs.addTab(tab3, "Сетка")
        self.create_grid_layout(tab3)
        
        # Вкладка 4: Форма
        tab4 = QWidget()
        tabs.addTab(tab4, "Форма")
        self.create_form_layout(tab4)
        
        # Вкладка 5: Вложенные макеты
        tab5 = QWidget()
        tabs.addTab(tab5, "Вложенные")
        self.create_nested_layout(tab5)
    
    def create_vbox_layout(self, parent):
        """Вертикальная компоновка"""
        layout = QVBoxLayout()
        
        # Добавление виджетов
        for i in range(1, 6):
            btn = QPushButton(f"Кнопка {i}")
            layout.addWidget(btn)
        
        # Растяжка
        layout.addStretch()
        
        # Кнопки выравнивания
        align_frame = QFrame()
        align_frame.setFrameStyle(QFrame.Shape.Box)
        align_frame_layout = QVBoxLayout(align_frame)
        
        align_frame_layout.addWidget(QLabel("Выравнивание:"))
        
        align_top = QPushButton("AlignTop")
        align_top.setMaximumHeight(30)
        align_frame_layout.addWidget(align_top)
        
        align_center = QPushButton("AlignCenter")
        align_center.setMaximumHeight(30)
        align_frame_layout.addWidget(align_center)
        
        align_bottom = QPushButton("AlignBottom")
        align_bottom.setMaximumHeight(30)
        align_frame_layout.addWidget(align_bottom)
        
        layout.addWidget(align_frame)
        
        parent.setLayout(layout)
    
    def create_hbox_layout(self, parent):
        """Горизонтальная компоновка"""
        layout = QHBoxLayout()
        
        # Кнопки
        for i in range(1, 6):
            btn = QPushButton(f"{i}")
            layout.addWidget(btn)
        
        # Растяжка
        layout.addStretch()
        
        parent.setLayout(layout)
    
    def create_grid_layout(self, parent):
        """Сеточная компоновка"""
        layout = QGridLayout()
        
        # Заголовки
        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(QLabel("Пн"), 0, 1)
        layout.addWidget(QLabel("Вт"), 0, 2)
        layout.addWidget(QLabel("Ср"), 0, 3)
        layout.addWidget(QLabel("Чт"), 0, 4)
        layout.addWidget(QLabel("Пт"), 0, 5)
        
        # Дни недели
        days = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
        
        for row, time in enumerate(days, start=1):
            layout.addWidget(QLabel(time), row, 0)
            
            for col in range(1, 6):
                btn = QPushButton("-")
                btn.setMinimumHeight(40)
                layout.addWidget(btn, row, col)
        
        parent.setLayout(layout)
    
    def create_form_layout(self, parent):
        """Компоновка формы"""
        layout = QFormLayout()
        
        # Поля формы
        layout.addRow("Имя:", QLineEdit())
        layout.addRow("Фамилия:", QLineEdit())
        layout.addRow("Возраст:", QSpinBox())
        layout.addRow("Email:", QLineEdit())
        layout.addRow("Телефон:", QLineEdit())
        
        # Чекбокс
        layout.addRow("Согласен:", QCheckBox())
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addRow("", button_box)
        
        parent.setLayout(layout)
    
    def create_nested_layout(self, parent):
        """Вложенные макеты"""
        # Основной макет - вертикальный
        main_layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Вложенные макеты")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Средняя часть - сплиттер
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Левая панель
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("Левая панель"))
        for i in range(3):
            left_layout.addWidget(QPushButton(f"Кнопка {i+1}"))
        left_layout.addStretch()
        
        # Средняя панель
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.addWidget(QLabel("Центральная панель"))
        
        grid = QGridLayout()
        for i in range(3):
            for j in range(3):
                grid.addWidget(QPushButton(f"{i},{j}"), i, j)
        center_layout.addLayout(grid)
        
        # Правая панель
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("Правая панель"))
        
        form = QFormLayout()
        form.addRow("Поле 1:", QLineEdit())
        form.addRow("Поле 2:", QLineEdit())
        right_layout.addLayout(form)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(center_widget)
        splitter.addWidget(right_widget)
        
        main_layout.addWidget(splitter)
        
        # Нижняя панель - кнопки
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QPushButton("ОК"))
        bottom_layout.addStretch()
        bottom_layout.addWidget(QPushButton("Отмена"))
        
        main_layout.addLayout(bottom_layout)
        
        parent.setLayout(main_layout)


# ==============================================================================
# ЗАДАЧА 4: Меню и тулбары
# ==============================================================================

class MenuToolbarDemo(QMainWindow):
    """Демонстрация меню и тулбаров"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 4: Меню и тулбары")
        self.setGeometry(100, 100, 700, 500)
        
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_central_widget()
    
    def create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        # Файл меню
        file_menu = menubar.addMenu("&Файл")
        
        new_action = QAction("&Новый", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.statusBar().showMessage("Новый файл"))
        file_menu.addAction(new_action)
        
        open_action = QAction("&Открыть", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("В&ыход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Правка меню
        edit_menu = menubar.addMenu("&Правка")
        
        edit_menu.addAction("&Копировать").triggered.connect(
            lambda: self.statusBar().showMessage("Копировать")
        )
        edit_menu.addAction("&Вставить").triggered.connect(
            lambda: self.statusBar().showMessage("Вставить")
        )
        edit_menu.addAction("&Вырезать").triggered.connect(
            lambda: self.statusBar().showMessage("Вырезать")
        )
        
        # Вид меню
        view_menu = menubar.addMenu("&Вид")
        
        view_menu.addAction("Панель &инструментов").setCheckable(True)
        view_menu.addAction("Панель &статуса").setCheckable(True)
        
        # Справка меню
        help_menu = menubar.addMenu("&Справка")
        
        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Основная панель")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Действия
        new_action = QAction("Новый", self)
        new_action.triggered.connect(lambda: self.statusBar().showMessage("Новый"))
        toolbar.addAction(new_action)
        
        open_action = QAction("Открыть", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Выпадающий список
        combo = QComboBox()
        combo.addItems(["Стиль 1", "Стиль 2", "Стиль 3"])
        toolbar.addWidget(combo)
        
        toolbar.addSeparator()
        
        # Поиск
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск...")
        search_input.setMaximumWidth(200)
        toolbar.addWidget(search_input)
    
    def create_statusbar(self):
        """Создание строки статуса"""
        status = self.statusBar()
        status.showMessage("Готов")
        
        # Дополнительные элементы
        status.addPermanentWidget(QLabel("|"))
        
        label = QLabel("PyQt Меню и тулбары")
        status.addPermanentWidget(label)
        
        status.addPermanentWidget(QLabel("|"))
        
        time_label = QLabel("12:00")
        status.addPermanentWidget(time_label)
    
    def create_central_widget(self):
        """Создание центрального виджета"""
        central = QWidget()
        layout = QVBoxLayout(central)
        
        layout.addWidget(QLabel("Текстовый редактор"))
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        
        self.setCentralWidget(central)
    
    def open_file(self):
        """Открыть файл"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
                self.statusBar().showMessage(f"Открыт: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def save_file(self):
        """Сохранить файл"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.statusBar().showMessage(f"Сохранено: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
    
    def show_about(self):
        """Показать о программе"""
        QMessageBox.about(
            self,
            "О программе",
            "Демонстрация меню и тулбаров PyQt\n\n"
            "Создано в учебных целях"
        )


# ==============================================================================
# ЗАДАЧА 5: Диалоговые окна
# ==============================================================================

class DialogsDemo(QMainWindow):
    """Демонстрация диалоговых окон"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 5: Диалоговые окна")
        self.setGeometry(100, 100, 500, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Стандартные диалоговые окна")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        title.setFont(font)
        layout.addWidget(title)
        
        # Кнопки диалогов
        dialogs = [
            ("QFileDialog - Открыть файл", self.show_file_dialog),
            ("QFileDialog - Сохранить файл", self.show_save_dialog),
            ("QColorDialog - Выбор цвета", self.show_color_dialog),
            ("QFontDialog - Выбор шрифта", self.show_font_dialog),
            ("QInputDialog - Ввод текста", self.show_input_dialog),
            ("QInputDialog - Выбор числа", self.show_number_dialog),
            ("QInputDialog - Выбор из списка", self.show_item_dialog),
            ("QMessageBox - Информация", self.show_info),
            ("QMessageBox - Вопрос", self.show_question),
            ("QMessageBox - Предупреждение", self.show_warning),
            ("QMessageBox - Критическая ошибка", self.show_critical),
        ]
        
        for text, handler in dialogs:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
        
        # Результат
        layout.addWidget(QLabel("\nРезультат:"))
        
        self.result_label = QLabel("-")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
    
    def show_file_dialog(self):
        """Диалог открытия файла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть файл",
            "",
            "Text Files (*.txt);;Python Files (*.py);;All Files (*)"
        )
        if file_name:
            self.result_label.setText(f"Выбран файл: {file_name}")
    
    def show_save_dialog(self):
        """Диалог сохранения файла"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            self.result_label.setText(f"Сохранение в: {file_name}")
    
    def show_color_dialog(self):
        """Диалог выбора цвета"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.result_label.setText(f"Выбран цвет: {color.name()}")
            self.result_label.setStyleSheet(f"color: {color.name()}")
    
    def show_font_dialog(self):
        """Диалог выбора шрифта"""
        font, ok = QFontDialog.getFont()
        if ok:
            self.result_label.setText(f"Выбран шрифт: {font.family()} {font.pointSize()}")
            self.result_label.setFont(font)
    
    def show_input_dialog(self):
        """Диалог ввода текста"""
        text, ok = QInputDialog.getText(
            self,
            "Ввод текста",
            "Введите ваше имя:"
        )
        if ok:
            self.result_label.setText(f"Введено: {text}")
    
    def show_number_dialog(self):
        """Диалог ввода числа"""
        number, ok = QInputDialog.getInt(
            self,
            "Ввод числа",
            "Введите возраст:",
            value=25,
            min=0,
            max=150
        )
        if ok:
            self.result_label.setText(f"Введено число: {number}")
    
    def show_item_dialog(self):
        """Диалог выбора из списка"""
        items = ["Пункт 1", "Пункт 2", "Пункт 3", "Пункт 4"]
        item, ok = QInputDialog.getItem(
            self,
            "Выбор элемента",
            "Выберите пункт:",
            items,
            0,
            False
        )
        if ok:
            self.result_label.setText(f"Выбрано: {item}")
    
    def show_info(self):
        """Информационное сообщение"""
        QMessageBox.information(
            self,
            "Информация",
            "Это информационное сообщение.\n\n"
            "PyQt - мощная библиотека для создания GUI."
        )
    
    def show_question(self):
        """Вопрос"""
        reply = QMessageBox.question(
            self,
            "Вопрос",
            "Хотите сохранить изменения?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )
        
        if reply == QMessageBox.StandardButton.Save:
            self.result_label.setText("Сохранено")
        elif reply == QMessageBox.StandardButton.Discard:
            self.result_label.setText("Изменения отклонены")
        else:
            self.result_label.setText("Отмена")
    
    def show_warning(self):
        """Предупреждение"""
        QMessageBox.warning(
            self,
            "Предупреждение",
            "Внимание! Произошла неожиданная ситуация."
        )
    
    def show_critical(self):
        """Критическая ошибка"""
        QMessageBox.critical(
            self,
            "Критическая ошибка",
            "Произошла критическая ошибка!\n\n"
            "Приложение будет закрыто."
        )


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self):
        if PYQT_VERSION > 0:
            self.app = QApplication([])
        
        # Список для хранения ссылок на открытые окна
        # (чтобы они не были удалены сборщиком мусора)
        self.windows = []
        
        self.tasks = [
            ("Задача 1: Базовое приложение", self.open_task1),
            ("Задача 2: Основные виджеты", self.open_task2),
            ("Задача 3: Компоновка", self.open_task3),
            ("Задача 4: Меню и тулбары", self.open_task4),
            ("Задача 5: Диалоговые окна", self.open_task5),
        ]
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = BasicAppDemo()
        self.windows.append(window)  # Сохраняем ссылку
        window.show()
    
    def open_task2(self):
        """Открыть задачу 2"""
        window = WidgetsDemo()
        self.windows.append(window)  # Сохраняем ссылку
        window.show()
    
    def open_task3(self):
        """Открыть задачу 3"""
        window = LayoutDemo()
        self.windows.append(window)  # Сохраняем ссылку
        window.show()
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = MenuToolbarDemo()
        self.windows.append(window)  # Сохраняем ссылку
        window.show()
    
    def open_task5(self):
        """Открыть задачу 5"""
        window = DialogsDemo()
        self.windows.append(window)  # Сохраняем ссылку
        window.show()
    
    def run(self):
        """Запуск приложения"""
        if PYQT_VERSION == 0:
            print("PyQt не установлен. Установите PyQt5 или PyQt6.")
            print("pip install PyQt5")
            return
        
        # Главное окно выбора задач
        main_window = QMainWindow()
        main_window.setWindowTitle("Практическое занятие 27: PyQt - базовые приложения")
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
