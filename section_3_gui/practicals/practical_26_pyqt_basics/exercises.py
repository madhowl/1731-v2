# Упражнения для практического занятия 21: Создание GUI с помощью PyQt

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                            QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
                            QCheckBox, QRadioButton, QComboBox, QSpinBox, QSlider, 
                            QProgressBar, QTableWidgetItem, QListWidget,
                            QTreeWidgetItem, QTreeWidget, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import json
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
        
        # Устанавливаем макет
        central_widget.setLayout(layout)
    
    def button_clicked(self):
        """Обработчик нажатия кнопки"""
        self.label.setText("Кнопка была нажата!")
        self.label.setStyleSheet("color: blue;")
    
    def display_text(self):
        """Отображает введенный текст"""
        text = self.line_edit.text()
        if text:
            self.label.setText(f"Вы ввели: {text}")
            self.label.setStyleSheet("color: green;")
        else:
            self.label.setText("Текст не введен")
            self.label.setStyleSheet("color: red;")

# Задание 2: Компоновка элементов
class LayoutApp(QMainWindow):
    """Приложение с различными макетами"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 2: Компоновка элементов")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем вкладки для разных макетов
        from PyQt5.QtWidgets import QTabWidget
        tab_widget = QTabWidget()
        
        # Вкладка вертикального макета
        vertical_tab = QWidget()
        vertical_layout = QVBoxLayout()
        
        for i in range(5):
            btn = QPushButton(f"Кнопка {i+1} (вертикальный)")
            btn.clicked.connect(lambda _, x=i+1: self.layout_button_clicked(x, "вертикальный"))
            vertical_layout.addWidget(btn)
        
        vertical_tab.setLayout(vertical_layout)
        tab_widget.addTab(vertical_tab, "Вертикальный")
        
        # Вкладка горизонтального макета
        horizontal_tab = QWidget()
        horizontal_layout = QHBoxLayout()
        
        for i in range(5):
            btn = QPushButton(f"Кнопка {i+1} (горизонт.)")
            btn.clicked.connect(lambda _, x=i+1: self.layout_button_clicked(x, "горизонтальный"))
            horizontal_layout.addWidget(btn)
        
        horizontal_tab.setLayout(horizontal_layout)
        tab_widget.addTab(horizontal_tab, "Горизонтальный")
        
        # Вкладка сеточного макета
        grid_tab = QWidget()
        grid_layout = QGridLayout()
        
        positions = [(i, j) for i in range(3) for j in range(3)]
        for i, pos in enumerate(positions):
            btn = QPushButton(f"Кнопка {i+1} (сетка)")
            btn.clicked.connect(lambda _, x=i+1: self.layout_button_clicked(x, "сеточный"))
            grid_layout.addWidget(btn, pos[0], pos[1])
        
        grid_tab.setLayout(grid_layout)
        tab_widget.addTab(grid_tab, "Сеточный")
        
        # Вкладка формы
        form_tab = QWidget()
        form_layout = QFormLayout()
        
        form_layout.addRow("Имя:", QLineEdit())
        form_layout.addRow("Фамилия:", QLineEdit())
        form_layout.addRow("Email:", QLineEdit())
        form_layout.addRow("Телефон:", QLineEdit())
        
        submit_btn = QPushButton("Отправить")
        submit_btn.clicked.connect(lambda: self.form_submitted(form_layout))
        form_layout.addRow(submit_btn)
        
        form_tab.setLayout(form_layout)
        tab_widget.addTab(form_tab, "Форма")
        
        # Устанавливаем вкладки в центральный виджет
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        central_widget.setLayout(layout)
    
    def layout_button_clicked(self, button_num, layout_type):
        """Обработка нажатия кнопки в макете"""
        QMessageBox.information(self, "Информация", 
                               f"Нажата кнопка {button_num} в {layout_type} макете")
    
    def form_submitted(self, form_layout):
        """Обработка отправки формы"""
        QMessageBox.information(self, "Форма отправлена", 
                               "Данные формы были успешно отправлены")

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
        checkbox_group = QWidget()
        checkbox_layout = QHBoxLayout()
        self.checkboxes = []
        for i in range(5):
            cb = QCheckBox(f"Флажок {i+1}")
            cb.stateChanged.connect(lambda state, x=i+1: self.checkbox_changed(state, x))
            checkbox_layout.addWidget(cb)
            self.checkboxes.append(cb)
        checkbox_group.setLayout(checkbox_layout)
        layout.addWidget(QLabel("Чекбоксы:"))
        layout.addWidget(checkbox_group)
        
        # QRadioButton
        radio_group = QWidget()
        radio_layout = QHBoxLayout()
        self.radiobuttons = []
        for i in range(3):
            rb = QRadioButton(f"Переключатель {i+1}")
            rb.toggled.connect(lambda checked, x=i+1: self.radiobutton_toggled(checked, x))
            radio_layout.addWidget(rb)
            self.radiobuttons.append(rb)
        radio_group.setLayout(radio_layout)
        layout.addWidget(QLabel("Переключатели:"))
        layout.addWidget(radio_group)
        
        # QComboBox
        self.combobox = QComboBox()
        self.combobox.addItems(["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"])
        self.combobox.currentTextChanged.connect(self.combobox_changed)
        layout.addWidget(QLabel("Комбобокс:"))
        layout.addWidget(self.combobox)
        
        # QSpinBox и QSlider
        spin_slider_group = QWidget()
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
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(QLabel("Прогресс бар:"))
        layout.addWidget(self.progress_bar)
        
        # Кнопка для запуска анимации прогресса
        self.progress_button = QPushButton("Запустить прогресс")
        self.progress_button.clicked.connect(self.start_progress_animation)
        layout.addWidget(self.progress_button)
        
        # QTableWidget
        table_label = QLabel("Таблица:")
        layout.addWidget(table_label)
        
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
        layout.addWidget(self.table)
        
        # QListWidget
        list_label = QLabel("Список:")
        layout.addWidget(list_label)
        
        self.list_widget = QListWidget()
        items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]
        self.list_widget.addItems(items)
        self.list_widget.itemClicked.connect(self.list_item_clicked)
        layout.addWidget(self.list_widget)
        
        # QTreeWidget
        tree_label = QLabel("Дерево:")
        layout.addWidget(tree_label)
        
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
        layout.addWidget(self.tree_widget)
        
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
        # Обновляем прогресс бар
        self.progress_bar.setValue(value)
    
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
        
        timer = QTimer()
        timer.timeout.connect(update_progress)
        timer.start(200)  # Обновление каждые 200мс
        self.timer = timer
    
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
    """Приложение для обработки событий"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Обработка событий")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Поле для отображения событий
        self.event_display = QLabel("Здесь будут отображаться события")
        self.event_display.setWordWrap(True)
        self.event_display.setStyleSheet("border: 1px solid gray; padding: 10px; background-color: lightgray;")
        layout.addWidget(self.event_display)
        
        # Кнопки для разных событий
        button_layout = QHBoxLayout()
        
        self.click_button = QPushButton("Кнопка клика")
        self.click_button.clicked.connect(self.handle_click)
        button_layout.addWidget(self.click_button)
        
        self.hover_button = QPushButton("Кнопка наведения")
        self.hover_button.enterEvent = self.handle_hover_enter
        self.hover_button.leaveEvent = self.handle_hover_leave
        button_layout.addWidget(self.hover_button)
        
        self.focus_button = QPushButton("Кнопка фокуса")
        self.focus_button.setFocusPolicy(Qt.StrongFocus)
        self.focus_button.focusInEvent = self.handle_focus_in
        self.focus_button.focusOutEvent = self.handle_focus_out
        button_layout.addWidget(self.focus_button)
        
        layout.addLayout(button_layout)
        
        # Специальная кнопка для клавиатуры
        self.key_button = QPushButton("Кнопка клавиатуры (нажмите Enter)")
        self.key_button.setFocus()
        self.key_button.keyPressEvent = self.handle_key_press
        layout.addWidget(self.key_button)
        
        # Кнопка для вызова контекстного меню
        self.context_button = QPushButton("Кнопка контекстного меню (правый клик)")
        self.context_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.context_button.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.context_button)
        
        central_widget.setLayout(layout)
    
    def handle_click(self):
        """Обработка клика"""
        self.event_display.setText("Событие: Клик по кнопке")
    
    def handle_hover_enter(self, event):
        """Обработка наведения мыши"""
        self.event_display.setText("Событие: Мыши наведена на кнопку")
        super().enterEvent(event)
    
    def handle_hover_leave(self, event):
        """Обработка ухода мыши"""
        self.event_display.setText("Событие: Мыши убрана с кнопки")
        super().leaveEvent(event)
    
    def handle_focus_in(self, event):
        """Обработка получения фокуса"""
        self.event_display.setText("Событие: Кнопка получила фокус")
        super().focusInEvent(event)
    
    def handle_focus_out(self, event):
        """Обработка потери фокуса"""
        self.event_display.setText("Событие: Кнопка потеряла фокус")
        super().focusOutEvent(event)
    
    def handle_key_press(self, event):
        """Обработка нажатия клавиши"""
        key_text = f"Событие: Нажата клавиша {event.text()}"
        self.event_display.setText(key_text)
        super().keyPressEvent(event)
    
    def show_context_menu(self, position):
        """Показывает контекстное меню"""
        menu = self.context_button.createStandardContextMenu()
        menu.addAction("Дополнительное действие", lambda: self.event_display.setText("Событие: Выбрано дополнительное действие"))
        menu.exec_(self.context_button.mapToGlobal(position))

# Задание 5: Комплексное приложение "Калькулятор"
class CalculatorApp(QMainWindow):
    """Калькулятор на PyQt"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Калькулятор на PyQt")
        self.setGeometry(100, 100, 400, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Дисплей калькулятора
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 16))
        self.display.setStyleSheet("padding: 10px; font-size: 18px;")
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

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 21 ===")
    
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
    
    print("\n5. Задание 5: Комплексное приложение (Калькулятор)")
    # app5 = QApplication(sys.argv)
    # calc_app = CalculatorApp()
    # calc_app.show()
    # sys.exit(app5.exec_())  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")