#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 29: PyQt6 - пользовательские диалоги
Решение задач по созданию диалоговых окон

Автор: AI Assistant
"""

# Используем PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFormLayout, QLabel, QPushButton, QLineEdit,
    QTextEdit, QDialog, QDialogButtonBox, QCheckBox, QRadioButton,
    QComboBox, QSpinBox, QGroupBox, QTabWidget, QStackedWidget,
    QWizard, QWizardPage, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, PYQT_VERSION
from PyQt6.QtGui import QFont


# ==============================================================================
# ЗАДАЧА 1: Базовые диалоги
# ==============================================================================

class SimpleDialog(QDialog):
    """Простой диалог"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Простой диалог")
        self.setModal(True)
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        
        # Сообщение
        label = QLabel("Это простой модальный диалог.\nНажмите ОК для закрытия.")
        layout.addWidget(label)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)


class ReturnValueDialog(QDialog):
    """Диалог с возвращаемым значением"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Диалог с возвращаемым значением")
        self.setModal(True)
        self.resize(350, 200)
        
        layout = QFormLayout()
        
        # Поля ввода
        self.name_edit = QLineEdit()
        layout.addRow("Имя:", self.name_edit)
        
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 150)
        self.age_spin.setValue(25)
        layout.addRow("Возраст:", self.age_spin)
        
        self.city_combo = QComboBox()
        self.city_combo.addItems(["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"])
        layout.addRow("Город:", self.city_combo)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow("", button_box)
        
        self.setLayout(layout)
    
    def get_data(self):
        """Получить данные"""
        return {
            "name": self.name_edit.text(),
            "age": self.age_spin.value(),
            "city": self.city_combo.currentText()
        }


class BasicDialogsDemo(QMainWindow):
    """Демонстрация базовых диалогов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 1: Базовые диалоги")
        self.setGeometry(100, 100, 400, 300)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Базовые диалоги")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Кнопки
        layout.addWidget(QLabel("1. Простой модальный диалог:"))
        
        simple_btn = QPushButton("Открыть простой диалог")
        simple_btn.clicked.connect(self.show_simple_dialog)
        layout.addWidget(simple_btn)
        
        layout.addWidget(QLabel("\n2. Диалог с возвращаемыми значениями:"))
        
        return_btn = QPushButton("Открыть диалог с данными")
        return_btn.clicked.connect(self.show_return_dialog)
        layout.addWidget(return_btn)
        
        # Результат
        layout.addWidget(QLabel("\nРезультат:"))
        
        self.result_label = QLabel("-")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def show_simple_dialog(self):
        """Показать простой диалог"""
        dialog = SimpleDialog(self)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self.result_label.setText("Диалог принят (ОК)")
        else:
            self.result_label.setText("Диалог отклонен (Отмена)")
    
    def show_return_dialog(self):
        """Показать диалог с возвращаемым значением"""
        dialog = ReturnValueDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.result_label.setText(
                f"Имя: {data['name']}, Возраст: {data['age']}, Город: {data['city']}"
            )
        else:
            self.result_label.setText("Отменено пользователем")


# ==============================================================================
# ЗАДАЧА 2: Формы ввода
# ==============================================================================

class SettingsDialog(QDialog):
    """Диалог настроек"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки приложения")
        self.setModal(True)
        self.resize(450, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        layout = QVBoxLayout()
        
        # Вкладки
        tabs = QTabWidget()
        
        # Общие настройки
        general_tab = QWidget()
        general_layout = QFormLayout()
        
        general_layout.addRow("Имя пользователя:", QLineEdit())
        general_layout.addRow("Email:", QLineEdit())
        
        self.notifications_check = QCheckBox("Включить уведомления")
        general_layout.addRow("", self.notifications_check)
        
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "Общие")
        
        # Внешний вид
        appearance_tab = QWidget()
        appearance_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая", "Темная", "Системная"])
        appearance_layout.addRow("Тема:", self.theme_combo)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "Courier New", "Verdana"])
        appearance_layout.addRow("Шрифт:", self.font_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        self.font_size_spin.setValue(12)
        appearance_layout.addRow("Размер шрифта:", self.font_size_spin)
        
        appearance_tab.setLayout(appearance_layout)
        tabs.addTab(appearance_tab, "Внешний вид")
        
        # Дополнительно
        advanced_tab = QWidget()
        advanced_layout = QFormLayout()
        
        self.auto_save_check = QCheckBox("Автосохранение")
        advanced_layout.addRow("", self.auto_save_check)
        
        self.backup_check = QCheckBox("Создавать резервные копии")
        advanced_layout.addRow("", self.backup_check)
        
        self.cache_spin = QSpinBox()
        self.cache_spin.setRange(50, 1000)
        self.cache_spin.setValue(200)
        self.cache_spin.setSuffix(" MB")
        advanced_layout.addRow("Размер кэша:", self.cache_spin)
        
        advanced_tab.setLayout(advanced_layout)
        tabs.addTab(advanced_tab, "Дополнительно")
        
        layout.addWidget(tabs)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def apply_settings(self):
        """Применение настроек"""
        QMessageBox.information(self, "Настройки", "Настройки применены!")


class InputFormDialog(QDialog):
    """Диалог ввода с валидацией"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Форма регистрации")
        self.setModal(True)
        self.resize(400, 350)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        layout = QFormLayout()
        
        # Поля с валидацией
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Придумайте логин")
        layout.addRow("Логин*:", self.username_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("example@mail.ru")
        layout.addRow("Email*:", self.email_edit)
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Минимум 8 символов")
        layout.addRow("Пароль*:", self.password_edit)
        
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Подтвердите пароль*:", self.confirm_edit)
        
        # Чекбокс условий
        self.terms_check = QCheckBox("Я принимаю условия использования")
        layout.addRow("", self.terms_check)
        
        # Сообщение об ошибке
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addRow("", self.error_label)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addRow("", button_box)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        """Валидация и принятие"""
        errors = []
        
        # Проверка логина
        username = self.username_edit.text()
        if len(username) < 3:
            errors.append("Логин должен содержать минимум 3 символа")
        
        # Проверка email
        email = self.email_edit.text()
        if "@" not in email or "." not in email:
            errors.append("Введите корректный email")
        
        # Проверка пароля
        password = self.password_edit.text()
        if len(password) < 8:
            errors.append("Пароль должен содержать минимум 8 символов")
        
        # Проверка совпадения паролей
        if password != self.confirm_edit.text():
            errors.append("Пароли не совпадают")
        
        # Проверка условий
        if not self.terms_check.isChecked():
            errors.append("Необходимо принять условия использования")
        
        if errors:
            self.error_label.setText("\n".join(errors))
        else:
            self.error_label.setText("")
            self.accept()
    
    def get_data(self):
        """Получить данные"""
        return {
            "username": self.username_edit.text(),
            "email": self.email_edit.text(),
            "password": self.password_edit.text()
        }


class InputFormsDemo(QMainWindow):
    """Демонстрация форм ввода"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 2: Формы ввода")
        self.setGeometry(100, 100, 450, 350)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Формы ввода")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Кнопки
        settings_btn = QPushButton("Диалог настроек")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)
        
        form_btn = QPushButton("Форма регистрации")
        form_btn.clicked.connect(self.show_registration)
        layout.addWidget(form_btn)
        
        # Результат
        layout.addWidget(QLabel("\nРезультат:"))
        
        self.result_label = QLabel("-")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def show_settings(self):
        """Показать диалог настроек"""
        dialog = SettingsDialog(self)
        dialog.exec()
        self.result_label.setText("Настройки сохранены")
    
    def show_registration(self):
        """Показать форму регистрации"""
        dialog = InputFormDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.result_label.setText(f"Регистрация: {data['username']} ({data['email']})")
        else:
            self.result_label.setText("Регистрация отменена")


# ==============================================================================
# ЗАДАЧА 3: Кастомные диалоги
# ==============================================================================

class CustomDialog(QDialog):
    """Кастомный диалог"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.result_data = None
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация UI"""
        layout = QVBoxLayout()
        
        # Заголовок
        self.title_label = QLabel(self.windowTitle())
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        
        # Контент (переопределить в подклассе)
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        
        # Кнопки
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def set_content_widget(self, widget):
        """Установить виджет контента"""
        self.content_layout.addWidget(widget)
    
    def get_result(self):
        """Получить результат"""
        return self.result_data


class ColorPickerDialog(CustomDialog):
    """Диалог выбора цвета"""
    
    def __init__(self, parent=None):
        super().__init__("Выбор цвета", parent)
        self.selected_color = "#000000"
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        # Превью цвета
        self.color_preview = QLabel()
        self.color_preview.setMinimumSize(200, 100)
        self.color_preview.setStyleSheet(f"background-color: {self.selected_color};")
        self.color_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_preview.setText(self.selected_color)
        self.set_content_widget(self.color_preview)
        
        # Ползунки RGB
        layout = QFormLayout()
        
        self.r_slider = QSpinBox()
        self.r_slider.setRange(0, 255)
        self.r_slider.setValue(0)
        self.r_slider.valueChanged.connect(self.update_color)
        layout.addRow("R:", self.r_slider)
        
        self.g_slider = QSpinBox()
        self.g_slider.setRange(0, 255)
        self.g_slider.setValue(0)
        self.g_slider.valueChanged.connect(self.update_color)
        layout.addRow("G:", self.g_slider)
        
        self.b_slider = QSpinBox()
        self.b_slider.setRange(0, 255)
        self.b_slider.setValue(0)
        self.b_slider.valueChanged.connect(self.update_color)
        layout.addRow("B:", self.b_slider)
        
        container = QWidget()
        container.setLayout(layout)
        self.content_layout.addWidget(container)
    
    def update_color(self):
        """Обновление цвета"""
        r = self.r_slider.value()
        g = self.g_slider.value()
        b = self.b_slider.value()
        
        self.selected_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.setStyleSheet(f"background-color: {self.selected_color};")
        self.color_preview.setText(self.selected_color)
    
    def get_color(self):
        """Получить выбранный цвет"""
        return self.selected_color


class CustomDialogsDemo(QMainWindow):
    """Демонстрация кастомных диалогов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 3: Кастомные диалоги")
        self.setGeometry(100, 100, 400, 300)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Кастомные диалоги")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Кнопки
        custom_btn = QPushButton("Кастомный диалог")
        custom_btn.clicked.connect(self.show_custom)
        layout.addWidget(custom_btn)
        
        color_btn = QPushButton("Выбор цвета")
        color_btn.clicked.connect(self.show_color_picker)
        layout.addWidget(color_btn)
        
        # Результат
        layout.addWidget(QLabel("\nРезультат:"))
        
        self.result_label = QLabel("-")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def show_custom(self):
        """Показать кастомный диалог"""
        dialog = CustomDialog("Мой диалог", self)
        
        # Добавление содержимого
        content = QLabel("Это кастомный диалог с добавленным содержимым!")
        dialog.set_content_widget(content)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.result_label.setText("Диалог принят")
        else:
            self.result_label.setText("Диалог отклонен")
    
    def show_color_picker(self):
        """Показать выбор цвета"""
        dialog = ColorPickerDialog(self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            color = dialog.get_color()
            self.result_label.setText(f"Выбран цвет: {color}")


# ==============================================================================
# ЗАДАЧА 4: Модальные vs Немодальные диалоги
# ==============================================================================

class NonModalDialog(QDialog):
    """Немодальный диалог"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Немодальный диалог")
        self.setModal(False)
        self.resize(300, 150)
        
        layout = QVBoxLayout()
        
        label = QLabel("Это немодальный диалог.\nВы можете работать с главным окном!")
        layout.addWidget(label)
        
        self.counter_label = QLabel("Счетчик: 0")
        layout.addWidget(self.counter_label)
        
        count_btn = QPushButton("Увеличить счетчик")
        count_btn.clicked.connect(self.increment)
        layout.addWidget(count_btn)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        self.counter = 0
    
    def increment(self):
        """Увеличить счетчик"""
        self.counter += 1
        self.counter_label.setText(f"Счетчик: {self.counter}")
    
    def update_content(self, data):
        """Обновить содержимое"""
        self.counter_label.setText(f"Получены данные: {data}")


class ModalDemo(QMainWindow):
    """Демонстрация модальных и немодальных диалогов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 4: Модальные vs Немодальные")
        self.setGeometry(100, 100, 450, 350)
        
        self.non_modal_dialog = None
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Модальные vs Немодальные диалоги")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Описание
        layout.addWidget(QLabel(
            "Модальный (exec()): блокирует родительское окно\n"
            "Немодальный (show()): не блокирует родительское окно"
        ))
        
        # Модальный диалог
        modal_btn = QPushButton("Модальный диалог (exec)")
        modal_btn.clicked.connect(self.show_modal)
        layout.addWidget(modal_btn)
        
        # Немодальный диалог
        nonmodal_btn = QPushButton("Немодальный диалог (show)")
        nonmodal_btn.clicked.connect(self.show_nonmodal)
        layout.addWidget(nonmodal_btn)
        
        # Отправить данные в немодальный
        send_btn = QPushButton("Отправить данные в немодальный")
        send_btn.clicked.connect(self.send_to_nonmodal)
        layout.addWidget(send_btn)
        
        # Счетчик главного окна
        self.main_counter = QLabel("Счетчик главного окна: 0")
        layout.addWidget(self.main_counter)
        
        counter_btn = QPushButton("Увеличить счетчик окна")
        counter_btn.clicked.connect(self.increment_main)
        layout.addWidget(counter_btn)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def show_modal(self):
        """Показать модальный диалог"""
        dialog = SimpleDialog(self)
        dialog.exec()
    
    def show_nonmodal(self):
        """Показать немодальный диалог"""
        if self.non_modal_dialog is None:
            self.non_modal_dialog = NonModalDialog(self)
            self.non_modal_dialog.destroyed.connect(self.on_nonmodal_destroyed)
        
        self.non_modal_dialog.show()
        self.non_modal_dialog.raise_()
        self.non_modal_dialog.activateWindow()
    
    def send_to_nonmodal(self):
        """Отправить данные в немодальный"""
        if self.non_modal_dialog is not None:
            import random
            data = random.randint(1, 100)
            self.non_modal_dialog.update_content(str(data))
        else:
            QMessageBox.warning(self, "Внимание", "Сначала откройте немодальный диалог")
    
    def on_nonmodal_destroyed(self):
        """Обработчик закрытия немодального диалога"""
        self.non_modal_dialog = None
    
    def increment_main(self):
        """Увеличить счетчик главного окна"""
        count = int(self.main_counter.text().split(": ")[1]) + 1
        self.main_counter.setText(f"Счетчик главного окна: {count}")


# ==============================================================================
# ЗАДАЧА 5: Продвинутые диалоги
# ==============================================================================

class MyWizard(QWizard):
    """Мастер создания"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Мастер настройки")
        
        # Добавить страницы
        self.addPage(self.create_intro_page())
        self.addPage(self.create_account_page())
        self.addPage(self.create_finish_page())
        
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
    
    def create_intro_page(self):
        """Страница введения"""
        page = QWizardPage()
        page.setTitle("Добро пожаловать")
        page.setSubTitle("Это мастер настройки приложения. Нажмите Далее для продолжения.")
        
        layout = QVBoxLayout()
        
        checkbox = QCheckBox("Я принимаю условия лицензии")
        checkbox.setChecked(False)
        layout.addWidget(checkbox)
        
        page.setLayout(layout)
        return page
    
    def create_account_page(self):
        """Страница аккаунта"""
        page = QWizardPage()
        page.setTitle("Настройка аккаунта")
        page.setSubTitle("Введите данные для создания аккаунта")
        
        layout = QFormLayout()
        
        layout.addRow("Имя пользователя:", QLineEdit())
        layout.addRow("Пароль:", QLineEdit())
        layout.addRow("Email:", QLineEdit())
        
        page.setLayout(layout)
        return page
    
    def create_finish_page(self):
        """Страница завершения"""
        page = QWizardPage()
        page.setTitle("Готово!")
        page.setSubTitle("Нажмите Готово для завершения настройки.")
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Настройка завершена успешно!"))
        
        page.setLayout(layout)
        return page


class PreviewDialog(QDialog):
    """Диалог с предпросмотром"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предпросмотр")
        self.setModal(False)
        self.resize(500, 400)
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        layout = QHBoxLayout()
        
        # Настройки
        settings = QWidget()
        settings_layout = QFormLayout()
        
        settings_layout.addRow("Заголовок:", QLineEdit("Заголовок"))
        settings_layout.addRow("Текст:", QTextEdit())
        
        settings.setLayout(settings_layout)
        layout.addWidget(settings)
        
        # Предпросмотр
        preview = QWidget()
        preview_layout = QVBoxLayout()
        
        preview_layout.addWidget(QLabel("Превью:"))
        
        self.preview_label = QLabel("Заголовок")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.preview_label.setFont(font)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.preview_label)
        
        self.preview_text = QLabel("Текст сообщения...")
        self.preview_text.setWordWrap(True)
        preview_layout.addWidget(self.preview_text)
        
        preview.setLayout(preview_layout)
        layout.addWidget(preview)
        
        self.setLayout(layout)
    
    def update_preview(self, data):
        """Обновить превью"""
        if "title" in data:
            self.preview_label.setText(data["title"])
        if "text" in data:
            self.preview_text.setText(data["text"])


class AdvancedDialogsDemo(QMainWindow):
    """Демонстрация продвинутых диалогов"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача 5: Продвинутые диалоги")
        self.setGeometry(100, 100, 450, 350)
        
        self.preview_dialog = None
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        title = QLabel("Продвинутые диалоги")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Кнопки
        wizard_btn = QPushButton("Мастер (Wizard)")
        wizard_btn.clicked.connect(self.show_wizard)
        layout.addWidget(wizard_btn)
        
        preview_btn = QPushButton("Диалог с предпросмотром")
        preview_btn.clicked.connect(self.show_preview)
        layout.addWidget(preview_btn)
        
        # Результат
        layout.addWidget(QLabel("\nРезультат:"))
        
        self.result_label = QLabel("-")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        central.setLayout(layout)
    
    def show_wizard(self):
        """Показать мастер"""
        wizard = MyWizard(self)
        
        if wizard.exec() == QDialog.DialogCode.Accepted:
            self.result_label.setText("Мастер завершен успешно!")
        else:
            self.result_label.setText("Мастер отменен")
    
    def show_preview(self):
        """Показать диалог предпросмотра"""
        if self.preview_dialog is None:
            self.preview_dialog = PreviewDialog(self)
            self.preview_dialog.destroyed.connect(self.on_preview_closed)
        
        self.preview_dialog.show()
        self.preview_dialog.update_preview({
            "title": "Заголовок",
            "text": "Текст для предпросмотра"
        })
    
    def on_preview_closed(self):
        """Обработчик закрытия"""
        self.preview_dialog = None


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
            ("Задача 1: Базовые диалоги", self.open_task1),
            ("Задача 2: Формы ввода", self.open_task2),
            ("Задача 3: Кастомные диалоги", self.open_task3),
            ("Задача 4: Модальные vs Немодальные", self.open_task4),
            ("Задача 5: Продвинутые диалоги", self.open_task5),
        ]
    
    def open_task1(self):
        window = BasicDialogsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task2(self):
        window = InputFormsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task3(self):
        window = CustomDialogsDemo()
        self.windows.append(window)
        window.show()
    
    def open_task4(self):
        window = ModalDemo()
        self.windows.append(window)
        window.show()
    
    def open_task5(self):
        window = AdvancedDialogsDemo()
        self.windows.append(window)
        window.show()
    
    def run(self):
        if PYQT_VERSION == 0:
            print("PyQt не установлен.")
            return
        
        main_window = QMainWindow()
        main_window.setWindowTitle("Практическое занятие 29: PyQt - пользовательские диалоги")
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
