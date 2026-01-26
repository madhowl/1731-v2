# Примеры продвинутых паттернов PyQt

"""
Этот файл содержит примеры использования продвинутых паттернов и возможностей PyQt
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QTextEdit, QTabWidget, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
                             QFileSystemModel, QTreeView, QListView, QAbstractItemView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem

class MVCExampleModel:
    """
    Модель для примера MVC в PyQt
    """
    def __init__(self):
        self._data = [
            {"name": "Иван Иванов", "age": 30, "position": "Разработчик"},
            {"name": "Мария Петрова", "age": 25, "position": "Дизайнер"},
            {"name": "Алексей Сидоров", "age": 35, "position": "Менеджер"}
        ]
    
    def get_data(self):
        """Получение данных"""
        return self._data.copy()
    
    def add_employee(self, name, age, position):
        """Добавление сотрудника"""
        employee = {"name": name, "age": int(age), "position": position}
        self._data.append(employee)
    
    def remove_employee(self, index):
        """Удаление сотрудника"""
        if 0 <= index < len(self._data):
            del self._data[index]
    
    def update_employee(self, index, name, age, position):
        """Обновление данных сотрудника"""
        if 0 <= index < len(self._data):
            self._data[index] = {"name": name, "age": int(age), "position": position}

class MVCExampleView(QWidget):
    """
    Представление для примера MVC в PyQt
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Таблица для отображения данных
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Имя", "Возраст", "Должность"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Обработка событий таблицы
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)
        
        # Форма для ввода данных
        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        form_layout.addWidget(self.name_input)
        
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")
        form_layout.addWidget(self.age_input)
        
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Должность")
        form_layout.addWidget(self.position_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add_click)
        button_layout.addWidget(add_btn)
        
        update_btn = QPushButton("Обновить")
        update_btn.clicked.connect(self.on_update_click)
        button_layout.addWidget(update_btn)
        
        remove_btn = QPushButton("Удалить")
        remove_btn.clicked.connect(self.on_remove_click)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
    
    def update_table(self, data):
        """Обновление таблицы с данными"""
        self.table.setRowCount(0)  # Очистка таблицы
        
        for row, employee in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(employee["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(employee["age"])))
            self.table.setItem(row, 2, QTableWidgetItem(employee["position"]))
    
    def get_selected_index(self):
        """Получение индекса выбранной строки"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            return selected_rows[0].row()
        return -1
    
    def get_inputs(self):
        """Получение значений из полей ввода"""
        return {
            "name": self.name_input.text().strip(),
            "age": self.age_input.text().strip(),
            "position": self.position_input.text().strip()
        }
    
    def clear_inputs(self):
        """Очистка полей ввода"""
        self.name_input.clear()
        self.age_input.clear()
        self.position_input.clear()
    
    def on_selection_changed(self):
        """Обработка изменения выделения в таблице"""
        index = self.get_selected_index()
        if index != -1:
            data = self.controller.model.get_data()
            if index < len(data):
                employee = data[index]
                self.name_input.setText(employee["name"])
                self.age_input.setText(str(employee["age"]))
                self.position_input.setText(employee["position"])
    
    def on_add_click(self):
        """Обработка нажатия кнопки добавления"""
        inputs = self.get_inputs()
        if all(inputs.values()):
            self.controller.add_employee(inputs["name"], inputs["age"], inputs["position"])
            self.clear_inputs()
    
    def on_update_click(self):
        """Обработка нажатия кнопки обновления"""
        index = self.get_selected_index()
        if index != -1:
            inputs = self.get_inputs()
            if all(inputs.values()):
                self.controller.update_employee(index, inputs["name"], inputs["age"], inputs["position"])
                self.clear_inputs()
    
    def on_remove_click(self):
        """Обработка нажатия кнопки удаления"""
        index = self.get_selected_index()
        if index != -1:
            self.controller.remove_employee(index)

class MVCExampleController:
    """
    Контроллер для примера MVC в PyQt
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_view()
    
    def update_view(self):
        """Обновление представления"""
        data = self.model.get_data()
        self.view.update_table(data)
    
    def add_employee(self, name, age, position):
        """Добавление сотрудника"""
        self.model.add_employee(name, age, position)
        self.update_view()
    
    def remove_employee(self, index):
        """Удаление сотрудника"""
        self.model.remove_employee(index)
        self.update_view()
    
    def update_employee(self, index, name, age, position):
        """Обновление сотрудника"""
        self.model.update_employee(index, name, age, position)
        self.update_view()

class WorkerThread(QThread):
    """
    Рабочий поток для выполнения задач в фоне
    """
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    
    def __init__(self, task_duration=100):
        super().__init__()
        self.task_duration = task_duration
    
    def run(self):
        """Выполнение задачи в потоке"""
        for i in range(self.task_duration):
            # Симуляция работы
            import time
            time.sleep(0.01)
            # Отправка прогресса
            self.progress_signal.emit(int((i+1)/self.task_duration * 100))
        
        # Отправка результата
        self.result_signal.emit(f"Задача завершена за {self.task_duration} итераций")

class ThreadingExample(QMainWindow):
    """
    Пример использования потоков в PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = None
    
    def init_ui(self):
        self.setWindowTitle('Пример многопоточности в PyQt')
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title = QLabel('Многопоточность в PyQt')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Текстовая область для вывода
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Здесь будут отображаться результаты...")
        layout.addWidget(self.text_area)
        
        # Индикатор прогресса
        from PyQt5.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        start_btn = QPushButton('Запустить задачу')
        start_btn.clicked.connect(self.start_task)
        button_layout.addWidget(start_btn)
        
        cancel_btn = QPushButton('Отменить задачу')
        cancel_btn.clicked.connect(self.cancel_task)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def start_task(self):
        """Запуск задачи в фоновом потоке"""
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.text_area.append("Задача уже выполняется!")
            return
        
        self.worker_thread = WorkerThread(task_duration=200)
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.result_signal.connect(self.task_completed)
        
        self.text_area.append("Запуск фоновой задачи...")
        self.worker_thread.start()
    
    def update_progress(self, value):
        """Обновление индикатора прогресса"""
        self.progress_bar.setValue(value)
    
    def task_completed(self, result):
        """Обработка завершения задачи"""
        self.text_area.append(f"Результат: {result}")
        self.progress_bar.setValue(0)
    
    def cancel_task(self):
        """Отмена задачи"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.text_area.append("Задача отменена")
            self.progress_bar.setValue(0)

class CustomWidgetExample(QWidget):
    """
    Пример создания пользовательского виджета
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Пользовательский виджет')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Создание пользовательского элемента
        self.custom_input = self.create_custom_input()
        layout.addWidget(self.custom_input)
        
        # Кнопка для получения значения
        get_value_btn = QPushButton('Получить значение')
        get_value_btn.clicked.connect(self.get_custom_value)
        layout.addWidget(get_value_btn)
    
    def create_custom_input(self):
        """Создание пользовательского элемента ввода"""
        # Это комбинация из нескольких стандартных виджетов
        container = QWidget()
        container_layout = QHBoxLayout(container)
        
        label = QLabel('Значение:')
        self.custom_line_edit = QLineEdit()
        self.custom_line_edit.setPlaceholderText('Введите значение...')
        
        clear_btn = QPushButton('Очистить')
        clear_btn.clicked.connect(self.custom_line_edit.clear)
        
        container_layout.addWidget(label)
        container_layout.addWidget(self.custom_line_edit)
        container_layout.addWidget(clear_btn)
        
        return container
    
    def get_custom_value(self):
        """Получение значения из пользовательского виджета"""
        value = self.custom_line_edit.text()
        if value:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, 'Значение', f'Вы ввели: {value}')
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Поле ввода пустое!')

class FileBrowserExample(QMainWindow):
    """
    Пример файлового браузера с использованием PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Файловый браузер PyQt')
        self.setGeometry(100, 100, 800, 600)
        
        # Создание центрального виджета с разделителем
        splitter = QSplitter(Qt.Horizontal)
        
        # Модель файловой системы
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')
        
        # Дерево файлов
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(''))
        self.tree_view.setHeaderHidden(False)
        
        # Список файлов
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        
        # Установка текущего каталога
        self.tree_view.setRootIndex(self.file_model.index(''))
        
        # Подключение событий
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        
        # Добавление виджетов к разделителю
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.list_view)
        splitter.setSizes([400, 400])
        
        self.setCentralWidget(splitter)
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Готов')
    
    def on_tree_view_clicked(self, index):
        """Обработка клика по дереву файлов"""
        path = self.file_model.filePath(index)
        self.list_view.setRootIndex(index)
        self.status_bar.showMessage(f'Выбран путь: {path}')

class PyQtAdvancedPatternsDemo(QMainWindow):
    """
    Демонстрация продвинутых паттернов PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Продвинутые паттерны PyQt')
        self.setGeometry(100, 100, 1000, 700)
        
        # Создание вкладок для разных примеров
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
        # Добавление примеров как вкладок
        mvc_model = MVCExampleModel()
        mvc_view = MVCExampleView(None)  # Контроллер будет назначен позже
        mvc_controller = MVCExampleController(mvc_model, mvc_view)
        mvc_view.controller = mvc_controller  # Устанавливаем контроллер после создания
        
        tab_widget.addTab(mvc_view, "MVC Паттерн")
        tab_widget.addTab(ThreadingExample(), "Многопоточность")
        tab_widget.addTab(CustomWidgetExample(), "Пользовательский виджет")
        tab_widget.addTab(FileBrowserExample(), "Файловый браузер")

def run_advanced_patterns_demo():
    """
    Запуск демонстрации продвинутых паттернов
    """
    app = QApplication(sys.argv)
    demo = PyQtAdvancedPatternsDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации раскомментируйте следующую строку:
# run_advanced_patterns_demo()

if __name__ == "__main__":
    print("Примеры продвинутых паттернов PyQt")
    print("1. MVC (Model-View-Controller) паттерн")
    print("2. Многопоточность")
    print("3. Пользовательские виджеты")
    print("4. Файловый браузер")
    
    choice = input("\nВыберите пример для запуска (1-4) или 0 для всех: ").strip()
    
    if choice == "1":
        app = QApplication(sys.argv)
        model = MVCExampleModel()
        view = MVCExampleView(None)
        controller = MVCExampleController(model, view)
        view.controller = controller
        view.show()
        sys.exit(app.exec_())
    elif choice == "2":
        app = QApplication(sys.argv)
        threading_example = ThreadingExample()
        threading_example.show()
        sys.exit(app.exec_())
    elif choice == "3":
        app = QApplication(sys.argv)
        custom_widget_example = CustomWidgetExample()
        custom_widget_example.show()
        sys.exit(app.exec_())
    elif choice == "4":
        app = QApplication(sys.argv)
        file_browser_example = FileBrowserExample()
        file_browser_example.show()
        sys.exit(app.exec_())
    elif choice == "0":
        app = QApplication(sys.argv)
        demo = PyQtAdvancedPatternsDemo()
        demo.show()
        sys.exit(app.exec_())
    else:
        print("Неверный выбор")
