# Лекция 16: PyQt - основы

## Установка, базовые виджеты, сигналы и слоты

### План лекции:
1. Введение в PyQt
2. Установка PyQt
3. Основы архитектуры PyQt
4. Базовые виджеты PyQt
5. Сигналы и слоты
6. Система компоновки
7. Практические примеры

---

## 1. Введение в PyQt

### Что такое PyQt?

PyQt - это набор Python-привязок для набора библиотек Qt, которые являются кроссплатформенным приложением для разработки GUI. PyQt разработан компанией Riverbank Computing и предоставляет Python-интерфейс к фреймворку Qt.

### Основные особенности PyQt:
- Кроссплатформенность (Windows, macOS, Linux)
- Богатый набор виджетов
- Мощная система сигналов и слотов
- Поддержка стилей и тем
- Возможности для создания сложных интерфейсов
- Интеграция с Qt Designer для визуального проектирования

```python
# Установка PyQt
# pip install PyQt5  # Для PyQt5
# pip install PyQt6  # Для PyQt6 (новая версия)

# Основной импорт
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import sys

class BasicPyQtApp(QWidget):
    """
    Простое PyQt-приложение для демонстрации основ
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Настройка окна
        self.setWindowTitle('Базовое PyQt Приложение')
        self.setGeometry(100, 100, 400, 300)
        
        # Создание основных элементов интерфейса
        self.create_widgets()
        
        # Настройка компоновки
        self.setup_layout()
        
        # Подключение сигналов и слотов
        self.connect_signals()
    
    def create_widgets(self):
        # Создание виджетов
        self.title_label = QLabel('Добро пожаловать в PyQt!', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.text_label = QLabel('Это пример базового приложения', self)
        self.text_label.setAlignment(Qt.AlignCenter)
        
        self.click_button = QPushButton('Нажми меня!', self)
        self.status_label = QLabel('Статус: Готов', self)
        self.status_label.setAlignment(Qt.AlignCenter)
    
    def setup_layout(self):
        # Создание вертикальной компоновки
        layout = QVBoxLayout()
        
        # Добавление виджетов в компоновку
        layout.addWidget(self.title_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.click_button)
        layout.addWidget(self.status_label)
        
        # Установка компоновки для виджета
        self.setLayout(layout)
    
    def connect_signals(self):
        # Подключение сигнала кнопки к слоту
        self.click_button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        # Обработчик нажатия кнопки
        self.status_label.setText('Статус: Кнопка нажата!')

def main():
    # Создание экземпляра QApplication
    app = QApplication(sys.argv)
    
    # Создание и отображение главного окна
    window = BasicPyQtApp()
    window.show()
    
    # Запуск цикла событий
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

---

## 2. Установка PyQt

### Установка PyQt5 или PyQt6

PyQt5 и PyQt6 - это две основные версии библиотеки. PyQt5 основан на Qt 5, а PyQt6 - на Qt 6. PyQt6 является более новой версией, но PyQt5 до сих пор широко используется.

```bash
# Установка PyQt5
pip install PyQt5

# Установка PyQt6
pip install PyQt6

# Установка дополнительных компонентов PyQt5
pip install PyQt5-tools  # Инструменты разработки, включая Qt Designer

# Установка дополнительных компонентов PyQt6
pip install PyQt6-tools  # Инструменты разработки для PyQt6
```

### Проверка установки

```python
def check_pyqt_installation():
    """
    Проверка установки PyQt
    """
    try:
        from PyQt5.QtWidgets import QApplication
        print("PyQt5 установлен")
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication
            print("PyQt6 установлен")
        except ImportError:
            print("PyQt не установлен")
            return False
    
    return True

# Пример использования
if check_pyqt_installation():
    print("Можно использовать PyQt для создания GUI")
else:
    print("Установите PyQt: pip install PyQt5 или pip install PyQt6")
```

---

## 3. Основы архитектуры PyQt

### Иерархия классов

В PyQt все виджеты происходят от базового класса QObject. Основные классы:

- `QObject` - базовый класс для всех объектов Qt
- `QWidget` - базовый класс для всех виджетов
- `QMainWindow` - класс для главного окна приложения
- `QDialog` - класс для диалоговых окон
- `QApplication` - класс для управления приложением

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class CustomWidget(QWidget):
    """
    Пример пользовательского виджета
    """
    # Определение пользовательского сигнала
    value_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.init_ui()
    
    def init_ui(self):
        self.button = QPushButton(f'Значение: {self.value}', self)
        self.button.clicked.connect(self.increment_value)
    
    def increment_value(self):
        self.value += 1
        self.button.setText(f'Значение: {self.value}')
        # Вызов пользовательского сигнала
        self.value_changed.emit(self.value)

class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.create_central_widget()
    
    def init_ui(self):
        self.setWindowTitle('Архитектура PyQt')
        self.setGeometry(100, 100, 600, 400)
        
        # Создание меню
        self.create_menu()
        
        # Создание панели инструментов
        self.create_toolbar()
        
        # Создание строки состояния
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Готов')
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu('Файл')
        
        exit_action = file_menu.addAction('Выход')
        exit_action.triggered.connect(self.close)
    
    def create_toolbar(self):
        toolbar = self.addToolBar('Основная')
        
        action = toolbar.addAction('Выход')
        action.triggered.connect(self.close)
    
    def create_central_widget(self):
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Добавление пользовательского виджета
        self.custom_widget = CustomWidget()
        self.custom_widget.value_changed.connect(self.on_value_changed)
        
        # Создание макета для центрального виджета
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.custom_widget)
    
    def on_value_changed(self, value):
        self.status_bar.showMessage(f'Значение изменено на: {value}')

def run_main_window_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# Для запуска приложения раскомментируйте следующую строку:
# run_main_window_app()
```

---

## 4. Базовые виджеты PyQt

### Основные виджеты

PyQt предоставляет богатый набор виджетов для создания интерфейса:

```python
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTextEdit, QCheckBox, 
                             QRadioButton, QComboBox, QSpinBox, QSlider, QProgressBar,
                             QGroupBox, QTabWidget, QFrame, QScrollArea)

class BasicWidgetsDemo(QMainWindow):
    """
    Демонстрация базовых виджетов PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Базовые виджеты PyQt')
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout(central_widget)
        
        # Создание вкладок для разных виджетов
        self.create_input_widgets_tab(main_layout)
        self.create_display_widgets_tab(main_layout)
        self.create_selection_widgets_tab(main_layout)
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Демонстрация базовых виджетов PyQt')
    
    def create_input_widgets_tab(self, parent_layout):
        """
        Создание вкладки с входными виджетами
        """
        # Группировка виджетов
        input_group = QGroupBox('Входные виджеты')
        parent_layout.addWidget(input_group)
        
        layout = QVBoxLayout(input_group)
        
        # QLineEdit (поле ввода текста)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText('Введите текст здесь...')
        self.line_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(QLabel('Поле ввода (QLineEdit):'))
        layout.addWidget(self.line_edit)
        
        # QSpinBox (числовое поле)
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        self.spin_box.valueChanged.connect(self.on_spinbox_changed)
        layout.addWidget(QLabel('Числовое поле (QSpinBox):'))
        layout.addWidget(self.spin_box)
        
        # QSlider (ползунок)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(QLabel('Ползунок (QSlider):'))
        layout.addWidget(self.slider)
        
        # QTextEdit (многострочное поле ввода)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Введите многострочный текст...')
        layout.addWidget(QLabel('Многострочное поле ввода (QTextEdit):'))
        layout.addWidget(self.text_edit)
    
    def create_display_widgets_tab(self, parent_layout):
        """
        Создание вкладки с отображающими виджетами
        """
        display_group = QGroupBox('Отображающие виджеты')
        parent_layout.addWidget(display_group)
        
        layout = QVBoxLayout(display_group)
        
        # QLabel (метка)
        self.label = QLabel('Это метка (QLabel)')
        self.label.setStyleSheet("background-color: lightblue; padding: 10px;")
        layout.addWidget(QLabel('Метка (QLabel):'))
        layout.addWidget(self.label)
        
        # QProgressBar (индикатор прогресса)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(30)
        layout.addWidget(QLabel('Индикатор прогресса (QProgressBar):'))
        layout.addWidget(self.progress_bar)
        
        # Кнопка для запуска анимации прогресса
        progress_btn = QPushButton('Запустить анимацию прогресса')
        progress_btn.clicked.connect(self.animate_progress)
        layout.addWidget(progress_btn)
    
    def create_selection_widgets_tab(self, parent_layout):
        """
        Создание вкладки с виджетами выбора
        """
        selection_group = QGroupBox('Виджеты выбора')
        parent_layout.addWidget(selection_group)
        
        layout = QVBoxLayout(selection_group)
        
        # QCheckBox (флажок)
        self.check_box1 = QCheckBox('Опция 1')
        self.check_box2 = QCheckBox('Опция 2')
        self.check_box3 = QCheckBox('Опция 3')
        
        self.check_box1.stateChanged.connect(self.on_checkbox_changed)
        self.check_box2.stateChanged.connect(self.on_checkbox_changed)
        self.check_box3.stateChanged.connect(self.on_checkbox_changed)
        
        layout.addWidget(QLabel('Флажки (QCheckBox):'))
        layout.addWidget(self.check_box1)
        layout.addWidget(self.check_box2)
        layout.addWidget(self.check_box3)
        
        # QRadioButton (переключатель)
        radio_group = QGroupBox('Переключатели (QRadioButton):')
        radio_layout = QVBoxLayout(radio_group)
        
        self.radio_button1 = QRadioButton('Выбор 1')
        self.radio_button2 = QRadioButton('Выбор 2')
        self.radio_button3 = QRadioButton('Выбор 3')
        self.radio_button1.setChecked(True)
        
        self.radio_button1.toggled.connect(self.on_radio_button_toggled)
        
        radio_layout.addWidget(self.radio_button1)
        radio_layout.addWidget(self.radio_button2)
        radio_layout.addWidget(self.radio_button3)
        
        layout.addWidget(radio_group)
        
        # QComboBox (выпадающий список)
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Вариант 1', 'Вариант 2', 'Вариант 3', 'Длинный вариант с названием', 'Еще один вариант'])
        self.combo_box.currentIndexChanged.connect(self.on_combo_changed)
        layout.addWidget(QLabel('Выпадающий список (QComboBox):'))
        layout.addWidget(self.combo_box)
    
    def on_text_changed(self, text):
        self.status_bar.showMessage(f'Текст изменен: {text[:20]}...' if len(text) > 20 else f'Текст изменен: {text}')
    
    def on_spinbox_changed(self, value):
        self.status_bar.showMessage(f'Значение spinbox изменено: {value}')
    
    def on_slider_changed(self, value):
        self.status_bar.showMessage(f'Значение слайдера изменено: {value}')
    
    def on_checkbox_changed(self, state):
        sender = self.sender()  # Получаем виджет, который вызвал сигнал
        self.status_bar.showMessage(f'Флажок "{sender.text()}" изменен: {state}')
    
    def on_radio_button_toggled(self, checked):
        if checked:
            sender = self.sender()
            self.status_bar.showMessage(f'Переключатель "{sender.text()}" выбран')
    
    def on_combo_changed(self, index):
        text = self.combo_box.itemText(index)
        self.status_bar.showMessage(f'Выбран элемент: {text}')
    
    def animate_progress(self):
        """
        Анимация индикатора прогресса
        """
        from PyQt5.QtCore import QTimer
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Обновление каждые 100 мс
    
    def update_progress(self):
        self.progress_value += 5
        if self.progress_value > 100:
            self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)
        
        if self.progress_value == 0:  # Если вернулись к 0, останавливаем таймер
            self.timer.stop()

def run_widgets_demo():
    app = QApplication(sys.argv)
    demo = BasicWidgetsDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации базовых виджетов раскомментируйте следующую строку:
# run_widgets_demo()
```

---

## 5. Сигналы и слоты

### Основы системы сигналов и слотов

Сигналы и слоты - это механизм для связи между объектами в PyQt. Когда происходит событие, излучается сигнал, который может быть подключен к одному или нескольким слотам (функциям-обработчикам).

```python
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit

class SignalEmitter(QObject):
    """
    Объект, излучающий сигналы
    """
    # Определение пользовательских сигналов
    number_changed = pyqtSignal(int)
    text_changed = pyqtSignal(str)
    status_changed = pyqtSignal(str, int)  # Сигнал с несколькими параметрами
    
    def __init__(self):
        super().__init__()
        self.number = 0
        self.text = ""
    
    def change_number(self, value):
        self.number = value
        # Излучение сигнала
        self.number_changed.emit(value)
    
    def change_text(self, value):
        self.text = value
        # Излучение сигнала
        self.text_changed.emit(value)
    
    def update_status(self, message, code):
        # Излучение сигнала с несколькими параметрами
        self.status_changed.emit(message, code)

class SignalReceiver:
    """
    Объект, принимающий сигналы
    """
    def __init__(self, display_widget):
        self.display_widget = display_widget
    
    def on_number_changed(self, value):
        self.display_widget.append(f"Число изменено на: {value}")
    
    def on_text_changed(self, value):
        self.display_widget.append(f"Текст изменен на: {value}")
    
    def on_status_changed(self, message, code):
        self.display_widget.append(f"Статус: {message} (код: {code})")

class SignalsSlotsDemo(QWidget):
    """
    Демонстрация сигналов и слотов
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        self.setWindowTitle('Сигналы и слоты в PyQt')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Кнопки для излучения сигналов
        self.btn_increment = QPushButton('Увеличить число', self)
        self.btn_change_text = QPushButton('Изменить текст', self)
        self.btn_update_status = QPushButton('Обновить статус', self)
        
        # Текстовое поле для отображения событий
        self.event_log = QTextEdit()
        self.event_log.setMaximumHeight(200)
        
        # Метка для отображения текущего значения
        self.value_label = QLabel('Значение: 0', self)
        
        # Добавление виджетов в макет
        layout.addWidget(self.value_label)
        layout.addWidget(self.btn_increment)
        layout.addWidget(self.btn_change_text)
        layout.addWidget(self.btn_update_status)
        layout.addWidget(QLabel('Лог событий:'))
        layout.addWidget(self.event_log)
        
        self.setLayout(layout)
    
    def setup_connections(self):
        # Создание объектов
        self.emitter = SignalEmitter()
        self.receiver = SignalReceiver(self.event_log)
        
        # Подключение сигналов к слотам
        self.emitter.number_changed.connect(self.receiver.on_number_changed)
        self.emitter.number_changed.connect(self.update_value_label)
        self.emitter.text_changed.connect(self.receiver.on_text_changed)
        self.emitter.status_changed.connect(self.receiver.on_status_changed)
        
        # Подключение сигналов кнопок
        self.btn_increment.clicked.connect(self.on_increment_clicked)
        self.btn_change_text.clicked.connect(self.on_text_change_clicked)
        self.btn_update_status.clicked.connect(self.on_status_update_clicked)
    
    def on_increment_clicked(self):
        # Изменение значения и излучение сигнала
        current_number = self.emitter.number
        self.emitter.change_number(current_number + 1)
    
    def on_text_change_clicked(self):
        # Изменение текста и излучение сигнала
        import random
        texts = ['Привет', 'Мир', 'PyQt', 'Сигналы', 'Слоты']
        random_text = random.choice(texts)
        self.emitter.change_text(random_text)
    
    def on_status_update_clicked(self):
        # Обновление статуса и излучение сигнала
        import random
        messages = ['Готов', 'Обработка', 'Ошибка', 'Выполнено']
        random_message = random.choice(messages)
        random_code = random.randint(100, 999)
        self.emitter.update_status(random_message, random_code)
    
    def update_value_label(self, value):
        # Обновление метки с текущим значением
        self.value_label.setText(f'Значение: {value}')

def run_signals_slots_demo():
    app = QApplication(sys.argv)
    demo = SignalsSlotsDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации сигналов и слотов раскомментируйте следующую строку:
# run_signals_slots_demo()
```

---

## 6. Система компоновки

### Менеджеры компоновки в PyQt

PyQt предоставляет несколько менеджеров компоновки для автоматического размещения виджетов:

1. `QVBoxLayout` - вертикальное расположение
2. `QHBoxLayout` - горизонтальное расположение
3. `QGridLayout` - сеточное расположение
4. `QFormLayout` - форматированное расположение (для форм)
5. `QStackedLayout` - стековое расположение

```python
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QFormLayout, QStackedLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QGroupBox)

class LayoutDemo(QWidget):
    """
    Демонстрация систем компоновки PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Системы компоновки PyQt')
        self.setGeometry(100, 100, 900, 700)
        
        # Создание вкладок для разных систем компоновки
        main_layout = QVBoxLayout()
        
        # 1. QVBoxLayout (вертикальная компоновка)
        vertical_group = QGroupBox('Вертикальная компоновка (QVBoxLayout)')
        vertical_layout = QVBoxLayout(vertical_group)
        
        for i in range(3):
            btn = QPushButton(f'Кнопка {i+1} (верт.)')
            vertical_layout.addWidget(btn)
        
        main_layout.addWidget(vertical_group)
        
        # 2. QHBoxLayout (горизонтальная компоновка)
        horizontal_group = QGroupBox('Горизонтальная компоновка (QHBoxLayout)')
        horizontal_layout = QHBoxLayout(horizontal_group)
        
        for i in range(3):
            btn = QPushButton(f'Кнопка {i+1} (гор.)')
            horizontal_layout.addWidget(btn)
        
        main_layout.addWidget(horizontal_group)
        
        # 3. QGridLayout (сеточная компоновка)
        grid_group = QGroupBox('Сеточная компоновка (QGridLayout)')
        grid_layout = QGridLayout(grid_group)
        
        positions = [(i, j) for i in range(3) for j in range(3)]
        
        for i, (row, col) in enumerate(positions):
            btn = QPushButton(f'{row},{col}')
            grid_layout.addWidget(btn, row, col)
        
        main_layout.addWidget(grid_group)
        
        # 4. QFormLayout (компоновка формы)
        form_group = QGroupBox('Форматированная компоновка (QFormLayout)')
        form_layout = QFormLayout(form_group)
        
        form_layout.addRow('Имя:', QLineEdit())
        form_layout.addRow('Фамилия:', QLineEdit())
        form_layout.addRow('Email:', QLineEdit())
        form_layout.addRow('Телефон:', QLineEdit())
        
        main_layout.addWidget(form_group)
        
        # 5. Комбинированная компоновка
        combined_group = QGroupBox('Комбинированная компоновка')
        combined_layout = QVBoxLayout(combined_group)
        
        # Горизонтальная компоновка внутри вертикальной
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel('Поле 1:'))
        top_row.addWidget(QLineEdit())
        top_row.addWidget(QLabel('Поле 2:'))
        top_row.addWidget(QLineEdit())
        
        # Сеточная компоновка внутри вертикальной
        grid_inner = QGridLayout()
        for i in range(2):
            for j in range(2):
                btn = QPushButton(f'Внутр. {i},{j}')
                grid_inner.addWidget(btn, i, j)
        
        # Добавление в основную компоновку
        combined_layout.addLayout(top_row)
        combined_layout.addLayout(grid_inner)
        
        main_layout.addWidget(combined_group)
        
        self.setLayout(main_layout)

def run_layout_demo():
    app = QApplication(sys.argv)
    demo = LayoutDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации компоновки раскомментируйте следующую строку:
# run_layout_demo()
```

---

## 7. Практические примеры

### Пример 1: Калькулятор на PyQt

```python
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QPushButton, QLineEdit, QLabel)
from PyQt5.QtCore import Qt

class Calculator(QMainWindow):
    """
    Простой калькулятор на PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_calculator_logic()
    
    def init_ui(self):
        self.setWindowTitle('PyQt Калькулятор')
        self.setGeometry(100, 100, 300, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Макет для калькулятора
        layout = QGridLayout(central_widget)
        
        # Дисплей
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 18px; padding: 10px;")
        layout.addWidget(self.display, 0, 0, 1, 4)
        
        # Кнопки калькулятора
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for (text, row, col) in buttons:
            if text == '0':
                # Кнопка 0 занимает 2 колонки
                button = QPushButton(text)
                button.clicked.connect(lambda _, t=text: self.button_click(t))
                layout.addWidget(button, 5, 0, 1, 2)  # rowspan=1, colspan=2
            elif text == '.':
                # Кнопка точки
                button = QPushButton(text)
                button.clicked.connect(lambda _, t=text: self.button_click(t))
                layout.addWidget(button, 5, 2)
            else:
                button = QPushButton(text)
                button.clicked.connect(lambda _, t=text: self.button_click(t))
                layout.addWidget(button, row, col)
        
        # Установка размеров колонок
        for col in range(4):
            layout.setColumnStretch(col, 1)
    
    def setup_calculator_logic(self):
        self.current_input = '0'
        self.operator = ''
        self.previous_input = ''
        self.reset_next_input = False
    
    def button_click(self, text):
        """
        Обработка нажатия кнопки
        """
        if text.isdigit() or text == '.':
            self.input_number(text)
        elif text in ['+', '-', '×', '÷']:
            self.input_operator(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '±':
            self.change_sign()
        elif text == '%':
            self.percentage()
    
    def input_number(self, number):
        """
        Ввод числа
        """
        if self.reset_next_input:
            self.current_input = '0'
            self.reset_next_input = False
        
        if number == '.' and '.' in self.current_input:
            return  # Избегаем нескольких точек
        
        if self.current_input == '0' and number != '.':
            self.current_input = number
        else:
            self.current_input += number
        
        self.display.setText(self.current_input)
    
    def input_operator(self, op):
        """
        Ввод оператора
        """
        if self.operator and not self.reset_next_input:
            self.calculate()
        
        self.previous_input = self.current_input
        self.operator = op
        self.reset_next_input = True
    
    def calculate(self):
        """
        Выполнение вычисления
        """
        if not self.operator or not self.previous_input:
            return
        
        try:
            prev_num = float(self.previous_input)
            curr_num = float(self.current_input)
            
            if self.operator == '+':
                result = prev_num + curr_num
            elif self.operator == '-':
                result = prev_num - curr_num
            elif self.operator == '×':
                result = prev_num * curr_num
            elif self.operator == '÷':
                if curr_num == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = prev_num / curr_num
            
            # Форматирование результата
            if result.is_integer():
                result = int(result)
            
            self.current_input = str(result)
            self.display.setText(self.current_input)
            self.operator = ''
            self.previous_input = ''
            self.reset_next_input = True
        except ZeroDivisionError:
            self.display.setText("Ошибка: деление на ноль")
            self.clear()
        except Exception as e:
            self.display.setText(f"Ошибка: {str(e)}")
            self.clear()
    
    def clear(self):
        """
        Очистка калькулятора
        """
        self.current_input = '0'
        self.operator = ''
        self.previous_input = ''
        self.reset_next_input = False
        self.display.setText(self.current_input)
    
    def change_sign(self):
        """
        Изменение знака числа
        """
        if self.current_input != '0':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display.setText(self.current_input)
    
    def percentage(self):
        """
        Вычисление процента
        """
        try:
            value = float(self.current_input) / 100
            if value.is_integer():
                value = int(value)
            self.current_input = str(value)
            self.display.setText(self.current_input)
        except:
            pass

def run_calculator():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

# Для запуска калькулятора раскомментируйте следующую строку:
# run_calculator()
```

### Пример 2: Форма регистрации

```python
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFormLayout, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QCheckBox, QComboBox, QDateEdit, QLabel, QFrame)
from PyQt5.QtCore import QDate

class RegistrationForm(QMainWindow):
    """
    Форма регистрации пользователя
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Форма регистрации')
        self.setGeometry(100, 100, 500, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title_label = QLabel('Регистрация нового пользователя')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: gray;")
        main_layout.addWidget(separator)
        
        # Макет формы
        form_layout = QFormLayout()
        
        # Поля формы
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        # Комбинированный список для выбора страны
        self.country_combo = QComboBox()
        self.country_combo.addItems(['Россия', 'США', 'Канада', 'Германия', 'Франция', 'Япония'])
        
        # Дата рождения
        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate.currentDate().addYears(-20))  # По умолчанию - 20 лет назад
        self.birth_date.setDisplayFormat("dd.MM.yyyy")
        self.birth_date.setCalendarPopup(True)
        
        # Пол
        gender_layout = QHBoxLayout()
        self.male_radio = QRadioButton('Мужской')
        self.female_radio = QRadioButton('Женский')
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        
        # Флажки для соглашений
        self.agreement_check = QCheckBox('Я согласен с условиями использования')
        self.newsletter_check = QCheckBox('Подписаться на рассылку')
        
        # Добавление полей в форму
        form_layout.addRow('Имя:', self.first_name_edit)
        form_layout.addRow('Фамилия:', self.last_name_edit)
        form_layout.addRow('Email:', self.email_edit)
        form_layout.addRow('Пароль:', self.password_edit)
        form_layout.addRow('Страна:', self.country_combo)
        form_layout.addRow('Дата рождения:', self.birth_date)
        form_layout.addRow('Пол:', gender_layout)
        form_layout.addRow('', self.agreement_check)
        form_layout.addRow('', self.newsletter_check)
        
        main_layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        submit_btn = QPushButton('Зарегистрироваться')
        submit_btn.clicked.connect(self.submit_form)
        
        clear_btn = QPushButton('Очистить')
        clear_btn.clicked.connect(self.clear_form)
        
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(clear_btn)
        
        main_layout.addLayout(button_layout)
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Готов к регистрации')
    
    def submit_form(self):
        """
        Обработка отправки формы
        """
        # Сбор данных из формы
        data = {
            'first_name': self.first_name_edit.text(),
            'last_name': self.last_name_edit.text(),
            'email': self.email_edit.text(),
            'password': self.password_edit.text(),
            'country': self.country_combo.currentText(),
            'birth_date': self.birth_date.date().toString("dd.MM.yyyy"),
            'gender': 'Мужской' if self.male_radio.isChecked() else 'Женский' if self.female_radio.isChecked() else 'Не указан',
            'agreement': self.agreement_check.isChecked(),
            'newsletter': self.newsletter_check.isChecked()
        }
        
        # Валидация данных
        errors = []
        if not data['first_name'].strip():
            errors.append('Имя обязательно')
        if not data['last_name'].strip():
            errors.append('Фамилия обязательна')
        if '@' not in data['email']:
            errors.append('Некорректный email')
        if len(data['password']) < 6:
            errors.append('Пароль должен быть не менее 6 символов')
        if not data['agreement']:
            errors.append('Необходимо согласие с условиями использования')
        
        if errors:
            error_message = 'Обнаружены ошибки:\n' + '\n'.join(errors)
            self.status_bar.showMessage(error_message)
            QMessageBox.warning(self, 'Ошибка валидации', error_message)
        else:
            # В реальном приложении здесь была бы отправка данных на сервер
            success_message = f"Пользователь {data['first_name']} {data['last_name']} успешно зарегистрирован!"
            self.status_bar.showMessage('Регистрация успешна')
            QMessageBox.information(self, 'Успех', success_message)
    
    def clear_form(self):
        """
        Очистка формы
        """
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.email_edit.clear()
        self.password_edit.clear()
        self.country_combo.setCurrentIndex(0)
        self.birth_date.setDate(QDate.currentDate().addYears(-20))
        self.male_radio.setChecked(False)
        self.female_radio.setChecked(False)
        self.agreement_check.setChecked(False)
        self.newsletter_check.setChecked(False)
        self.status_bar.showMessage('Форма очищена')

def run_registration_form():
    app = QApplication(sys.argv)
    form = RegistrationForm()
    form.show()
    sys.exit(app.exec_())

# Для запуска формы регистрации раскомментируйте следующую строку:
# run_registration_form()
```

---

## Заключение

PyQt предоставляет мощный и гибкий инструментарий для создания графических интерфейсов в Python. Система сигналов и слотов, богатый набор виджетов и продвинутые возможности компоновки делают его отличным выбором для создания сложных настольных приложений.

## Контрольные вопросы:
1. В чем отличие PyQt от Tkinter?
2. Какие основные компоненты входят в архитектуру PyQt?
3. Как работает система сигналов и слотов?
4. Какие менеджеры компоновки доступны в PyQt?
5. Как создать пользовательский сигнал?
