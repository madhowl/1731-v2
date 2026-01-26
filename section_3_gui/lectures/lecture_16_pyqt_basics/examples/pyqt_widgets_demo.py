# Примеры виджетов PyQt

"""
Этот файл содержит примеры использования различных виджетов PyQt
"""

import sys
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                 QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QCheckBox, 
                                 QRadioButton, QListWidget, QTableWidget, QTableWidgetItem, 
                                 QProgressBar, QSlider, QSpinBox, QMenuBar, QMenu, QAction, 
                                 QStatusBar, QFileDialog, QMessageBox, QDialog, QFormLayout)
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont, QPixmap
    
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("PyQt5 не установлен. Установите с помощью: pip install PyQt5")

if PYQT_AVAILABLE:
    class PyQtWidgetsDemo(QMainWindow):
        """
        Демонстрация различных виджетов PyQt
        """
        def __init__(self):
            super().__init__()
            self.init_ui()
        
        def init_ui(self):
            self.setWindowTitle('PyQt Виджеты Демо')
            self.setGeometry(100, 100, 900, 700)
            
            # Центральный виджет
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Основной макет
            main_layout = QVBoxLayout(central_widget)
            
            # Заголовок
            title_label = QLabel('Демонстрация PyQt Виджетов')
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFont(QFont("Arial", 16, QFont.Bold))
            main_layout.addWidget(title_label)
            
            # Создание вкладок для разных виджетов
            self.create_input_widgets_tab(main_layout)
            self.create_display_widgets_tab(main_layout)
            self.create_selection_widgets_tab(main_layout)
            
            # Статус бар
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            self.status_bar.showMessage('Готов')
        
        def create_input_widgets_tab(self, parent_layout):
            """
            Создание вкладки с входными виджетами
            """
            input_group = QWidget()
            parent_layout.addWidget(input_group)
            
            layout = QVBoxLayout(input_group)
            
            # Заголовок
            input_title = QLabel('Входные виджеты')
            input_title.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(input_title)
            
            # QLineEdit
            self.line_edit = QLineEdit()
            self.line_edit.setPlaceholderText('Введите текст здесь...')
            layout.addWidget(QLabel('Поле ввода (QLineEdit):'))
            layout.addWidget(self.line_edit)
            
            # QSpinBox
            self.spin_box = QSpinBox()
            self.spin_box.setRange(0, 100)
            self.spin_box.setValue(50)
            layout.addWidget(QLabel('Числовое поле (QSpinBox):'))
            layout.addWidget(self.spin_box)
            
            # QSlider
            self.slider = QSlider(Qt.Horizontal)
            self.slider.setRange(0, 100)
            self.slider.setValue(50)
            self.slider.valueChanged.connect(self.on_slider_change)
            layout.addWidget(QLabel('Ползунок (QSlider):'))
            layout.addWidget(self.slider)
            
            # Кнопка для демонстрации
            button = QPushButton('Показать значения')
            button.clicked.connect(self.show_values)
            layout.addWidget(button)
        
        def create_display_widgets_tab(self, parent_layout):
            """
            Создание вкладки с отображающими виджетами
            """
            display_group = QWidget()
            parent_layout.addWidget(display_group)
            
            layout = QVBoxLayout(display_group)
            
            # Заголовок
            display_title = QLabel('Отображающие виджеты')
            display_title.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(display_title)
            
            # QTextEdit
            self.text_edit = QTextEdit()
            self.text_edit.setPlainText('Это многострочное текстовое поле')
            layout.addWidget(QLabel('Текстовое поле (QTextEdit):'))
            layout.addWidget(self.text_edit)
            
            # QProgressBar
            self.progress_bar = QProgressBar()
            self.progress_bar.setValue(30)
            layout.addWidget(QLabel('Индикатор прогресса (QProgressBar):'))
            layout.addWidget(self.progress_bar)
            
            # Кнопка для анимации прогресса
            progress_btn = QPushButton('Анимировать прогресс')
            progress_btn.clicked.connect(self.animate_progress)
            layout.addWidget(progress_btn)
        
        def create_selection_widgets_tab(self, parent_layout):
            """
            Создание вкладки с виджетами выбора
            """
            selection_group = QWidget()
            parent_layout.addWidget(selection_group)
            
            layout = QVBoxLayout(selection_group)
            
            # Заголовок
            selection_title = QLabel('Виджеты выбора')
            selection_title.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(selection_title)
            
            # QComboBox
            self.combo_box = QComboBox()
            self.combo_box.addItems(['Вариант 1', 'Вариант 2', 'Вариант 3', 'Длинный вариант с названием', 'Еще один вариант'])
            layout.addWidget(QLabel('Выпадающий список (QComboBox):'))
            layout.addWidget(self.combo_box)
            
            # QCheckBox
            self.check_box1 = QCheckBox('Опция 1')
            self.check_box2 = QCheckBox('Опция 2')
            self.check_box3 = QCheckBox('Опция 3')
            layout.addWidget(QLabel('Флажки (QCheckBox):'))
            layout.addWidget(self.check_box1)
            layout.addWidget(self.check_box2)
            layout.addWidget(self.check_box3)
            
            # QRadioButton
            radio_layout = QHBoxLayout()
            self.radio_button1 = QRadioButton('Выбор 1')
            self.radio_button2 = QRadioButton('Выбор 2')
            self.radio_button3 = QRadioButton('Выбор 3')
            self.radio_button1.setChecked(True)
            
            radio_layout.addWidget(self.radio_button1)
            radio_layout.addWidget(self.radio_button2)
            radio_layout.addWidget(self.radio_button3)
            
            layout.addWidget(QLabel('Переключатели (QRadioButton):'))
            layout.addLayout(radio_layout)
        
        def on_slider_change(self, value):
            """
            Обработка изменения значения ползунка
            """
            self.status_bar.showMessage(f'Значение ползунка: {value}')
        
        def show_values(self):
            """
            Показ значений виджетов
            """
            line_text = self.line_edit.text()
            spin_value = self.spin_box.value()
            slider_value = self.slider.value()
            combo_text = self.combo_box.currentText()
            
            checked_boxes = []
            if self.check_box1.isChecked():
                checked_boxes.append(self.check_box1.text())
            if self.check_box2.isChecked():
                checked_boxes.append(self.check_box2.text())
            if self.check_box3.isChecked():
                checked_boxes.append(self.check_box3.text())
            
            selected_radio = None
            if self.radio_button1.isChecked():
                selected_radio = self.radio_button1.text()
            elif self.radio_button2.isChecked():
                selected_radio = self.radio_button2.text()
            elif self.radio_button3.isChecked():
                selected_radio = self.radio_button3.text()
            
            message = f"""
            Значения виджетов:
            Текст: {line_text}
            Число: {spin_value}
            Ползунок: {slider_value}
            Комбо: {combo_text}
            Флажки: {', '.join(checked_boxes) if checked_boxes else 'Нет выбранных'}
            Переключатель: {selected_radio}
            """
            
            QMessageBox.information(self, 'Значения', message.strip())
        
        def animate_progress(self):
            """
            Анимация индикатора прогресса
            """
            self.progress_timer = QTimer()
            self.progress_value = 0
            self.progress_timer.timeout.connect(self.update_progress)
            self.progress_timer.start(100)  # Обновление каждые 100 мс
        
        def update_progress(self):
            """
            Обновление значения прогресса
            """
            self.progress_value += 5
            if self.progress_value > 100:
                self.progress_value = 0
            
            self.progress_bar.setValue(self.progress_value)
            
            if self.progress_value == 0:  # Если достигли 0, останавливаем таймер
                self.progress_timer.stop()

    class PyQtAdvancedWidgets(QMainWindow):
        """
        Демонстрация продвинутых виджетов PyQt
        """
        def __init__(self):
            super().__init__()
            self.init_ui()
        
        def init_ui(self):
            self.setWindowTitle('PyQt Продвинутые Виджеты')
            self.setGeometry(100, 100, 900, 700)
            
            # Центральный виджет
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Основной макет
            main_layout = QVBoxLayout(central_widget)
            
            # Заголовок
            title_label = QLabel('Демонстрация Продвинутых PyQt Виджетов')
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFont(QFont("Arial", 16, QFont.Bold))
            main_layout.addWidget(title_label)
            
            # QTableWidget
            self.table_widget = QTableWidget(5, 3)
            self.table_widget.setHorizontalHeaderLabels(['Имя', 'Возраст', 'Город'])
            
            # Заполнение таблицы
            data = [
                ['Иван Иванов', '30', 'Москва'],
                ['Мария Петрова', '25', 'СПб'],
                ['Алексей Сидоров', '35', 'Новосибирск'],
                ['Елена Козлова', '28', 'Екатеринбург'],
                ['Дмитрий Волков', '32', 'Казань']
            ]
            
            for row, row_data in enumerate(data):
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.table_widget.setItem(row, col, item)
            
            main_layout.addWidget(QLabel('Таблица (QTableWidget):'))
            main_layout.addWidget(self.table_widget)
            
            # QListWidget
            self.list_widget = QListWidget()
            items = ['Элемент 1', 'Элемент 2', 'Элемент 3', 'Элемент 4', 'Элемент 5']
            self.list_widget.addItems(items)
            
            main_layout.addWidget(QLabel('Список (QListWidget):'))
            main_layout.addWidget(self.list_widget)
            
            # Кнопки управления
            button_layout = QHBoxLayout()
            
            add_btn = QPushButton('Добавить в список')
            add_btn.clicked.connect(self.add_to_list)
            button_layout.addWidget(add_btn)
            
            remove_btn = QPushButton('Удалить из списка')
            remove_btn.clicked.connect(self.remove_from_list)
            button_layout.addWidget(remove_btn)
            
            main_layout.addLayout(button_layout)
            
            # Статус бар
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            self.status_bar.showMessage('Готов')
        
        def add_to_list(self):
            """
            Добавление элемента в список
            """
            text, ok = QInputDialog.getText(self, 'Добавить элемент', 'Введите текст:')
            if ok and text:
                self.list_widget.addItem(text)
        
        def remove_from_list(self):
            """
            Удаление выбранного элемента из списка
            """
            current_item = self.list_widget.currentItem()
            if current_item:
                self.list_widget.takeItem(self.list_widget.row(current_item))

    # Запуск приложения
    def main():
        app = QApplication(sys.argv)
        
        # Выбор демонстрации
        print("Выберите пример:")
        print("1 - Базовые виджеты")
        print("2 - Продвинутые виджеты")
        
        choice = input("Введите номер (1 или 2): ").strip()
        
        if choice == "1":
            demo = PyQtWidgetsDemo()
            demo.show()
        elif choice == "2":
            demo = PyQtAdvancedWidgets()
            demo.show()
        else:
            print("Неверный выбор")
            return
        
        sys.exit(app.exec_())
    
    if __name__ == "__main__":
        main()
else:
    print("Для запуска этого примера установите PyQt5: pip install PyQt5")
