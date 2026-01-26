# Лекция 17: PyQt - продвинутый уровень

## Продвинутые виджеты, MVC/MVP паттерны, многопоточность

### План лекции:
1. Продвинутые виджеты PyQt
2. Архитектурные паттерны в GUI-приложениях
3. Многопоточность в PyQt
4. Пользовательские виджеты
5. Работа с файловой системой
6. Практические примеры

---

## 1. Продвинутые виджеты PyQt

### QTableWidget и QTreeWidget

```python
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QTreeWidgetItem, 
                             QTabWidget, QPushButton, QLabel, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class AdvancedWidgetsDemo(QMainWindow):
    """
    Демонстрация продвинутых виджетов PyQt
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Продвинутые виджеты PyQt')
        self.setGeometry(100, 100, 900, 700)
        
        # Создание вкладок для разных виджетов
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
        # Вкладка таблицы
        tab_widget.addTab(self.create_table_tab(), "Таблица")
        
        # Вкладка дерева
        tab_widget.addTab(self.create_tree_tab(), "Дерево")
        
        # Вкладка списка
        tab_widget.addTab(self.create_list_tab(), "Список")
    
    def create_table_tab(self):
        """
        Создание вкладки с таблицей
        """
        table_widget = QWidget()
        layout = QVBoxLayout(table_widget)
        
        # Заголовок
        title = QLabel('Таблица (QTableWidget)')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Создание таблицы
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(['Имя', 'Возраст', 'Город', 'Профессия'])
        
        # Заполнение таблицы данными
        data = [
            ['Иван Иванов', '30', 'Москва', 'Программист'],
            ['Мария Петрова', '25', 'СПб', 'Дизайнер'],
            ['Алексей Сидоров', '35', 'Новосибирск', 'Аналитик'],
            ['Елена Козлова', '28', 'Екатеринбург', 'Менеджер'],
            ['Дмитрий Волков', '32', 'Казань', 'Тестировщик']
        ]
        
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                # Добавим немного стилизации
                if col == 1:  # Возраст
                    item.setBackground(QColor(240, 240, 255))
                elif col == 2:  # Город
                    item.setBackground(QColor(240, 255, 240))
                self.table.setItem(row, col, item)
        
        # Настройка таблицы
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSortingEnabled(True)
        
        # Добавление прокрутки и растягивания
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('Добавить строку')
        add_btn.clicked.connect(self.add_table_row)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton('Удалить строку')
        remove_btn.clicked.connect(self.remove_table_row)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        
        return table_widget
    
    def create_tree_tab(self):
        """
        Создание вкладки с деревом
        """
        tree_widget = QWidget()
        layout = QVBoxLayout(tree_widget)
        
        # Заголовок
        title = QLabel('Дерево (QTreeWidget)')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Создание дерева
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Название', 'Тип', 'Дата создания'])
        
        # Создание элементов дерева
        root_items = []
        for i in range(3):
            root_item = QTreeWidgetItem(self.tree, [f'Корень {i+1}', 'Папка', '2023-01-01'])
            root_items.append(root_item)
            
            for j in range(3):
                child_item = QTreeWidgetItem(root_item, [f'Дочерний {j+1}', 'Файл', f'2023-01-{10+j}'])
                
                for k in range(2):
                    grandchild_item = QTreeWidgetItem(child_item, [f'Внук {k+1}', 'Файл', f'2023-01-{20+k}'])
        
        # Настройка дерева
        self.tree.expandAll()
        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tree)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_branch_btn = QPushButton('Добавить ветвь')
        add_branch_btn.clicked.connect(self.add_tree_branch)
        button_layout.addWidget(add_branch_btn)
        
        collapse_btn = QPushButton('Свернуть все')
        collapse_btn.clicked.connect(self.tree.collapseAll)
        button_layout.addWidget(collapse_btn)
        
        expand_btn = QPushButton('Развернуть все')
        expand_btn.clicked.connect(self.tree.expandAll)
        button_layout.addWidget(expand_btn)
        
        layout.addLayout(button_layout)
        
        return tree_widget
    
    def create_list_tab(self):
        """
        Создание вкладки со списком
        """
        list_widget = QWidget()
        layout = QVBoxLayout(list_widget)
        
        # Заголовок
        title = QLabel('Список (QListWidget)')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Создание списка
        from PyQt5.QtWidgets import QListWidget
        self.list = QListWidget()
        
        items = ['Элемент 1', 'Элемент 2', 'Элемент 3', 'Элемент 4', 'Элемент 5']
        self.list.addItems(items)
        
        # Добавим пользовательские элементы
        for i in range(5, 8):
            item = QListWidgetItem(f'Пользовательский элемент {i}')
            item.setCheckState(Qt.Checked if i % 2 == 0 else Qt.Unchecked)
            self.list.addItem(item)
        
        layout.addWidget(self.list)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_item_btn = QPushButton('Добавить элемент')
        add_item_btn.clicked.connect(self.add_list_item)
        button_layout.addWidget(add_item_btn)
        
        remove_item_btn = QPushButton('Удалить элемент')
        remove_item_btn.clicked.connect(self.remove_list_item)
        button_layout.addWidget(remove_item_btn)
        
        layout.addLayout(button_layout)
        
        return list_widget
    
    def add_table_row(self):
        """Добавление строки в таблицу"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Добавляем пустые элементы
        for col in range(self.table.columnCount()):
            self.table.setItem(row_position, col, QTableWidgetItem(""))
    
    def remove_table_row(self):
        """Удаление выбранной строки из таблицы"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
    
    def add_tree_branch(self):
        """Добавление новой ветви в дерево"""
        selected_items = self.tree.selectedItems()
        if selected_items:
            parent = selected_items[0]
        else:
            parent = self.tree.invisibleRootItem()
        
        new_item = QTreeWidgetItem(parent, ['Новая ветвь', 'Папка', 'Только что'])
        parent.addChild(new_item)
    
    def add_list_item(self):
        """Добавление элемента в список"""
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 'Добавить элемент', 'Введите текст:')
        if ok and text:
            self.list.addItem(text)
    
    def remove_list_item(self):
        """Удаление выбранного элемента из списка"""
        current_row = self.list.currentRow()
        if current_row >= 0:
            self.list.takeItem(current_row)

def run_advanced_widgets_demo():
    app = QApplication(sys.argv)
    demo = AdvancedWidgetsDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации раскомментируйте следующую строку:
# run_advanced_widgets_demo()
```

---

## 2. Архитектурные паттерны в GUI-приложениях

### MVC (Model-View-Controller)

```python
from PyQt5.QtCore import QObject, pyqtSignal

class UserModel(QObject):
    """
    Модель данных пользователя
    """
    data_changed = pyqtSignal()  # Сигнал для уведомления об изменениях
    
    def __init__(self):
        super().__init__()
        self._users = [
            {'id': 1, 'name': 'Иван Иванов', 'email': 'ivan@example.com', 'role': 'Администратор'},
            {'id': 2, 'name': 'Мария Петрова', 'email': 'maria@example.com', 'role': 'Пользователь'},
            {'id': 3, 'name': 'Алексей Сидоров', 'email': 'alex@example.com', 'role': 'Модератор'}
        ]
    
    def get_users(self):
        """Получение списка пользователей"""
        return self._users.copy()
    
    def add_user(self, name, email, role):
        """Добавление нового пользователя"""
        new_id = max([user['id'] for user in self._users]) + 1 if self._users else 1
        new_user = {'id': new_id, 'name': name, 'email': email, 'role': role}
        self._users.append(new_user)
        self.data_changed.emit()  # Уведомляем об изменении данных
    
    def remove_user(self, user_id):
        """Удаление пользователя по ID"""
        self._users = [user for user in self._users if user['id'] != user_id]
        self.data_changed.emit()
    
    def update_user(self, user_id, name, email, role):
        """Обновление пользователя"""
        for user in self._users:
            if user['id'] == user_id:
                user['name'] = name
                user['email'] = email
                user['role'] = role
                self.data_changed.emit()
                break

class UserView(QWidget):
    """
    Представление пользовательского интерфейса
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Управление пользователями (MVC)')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Таблица пользователей
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Email', 'Роль'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Обработка событий таблицы
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.table)
        
        # Форма для редактирования
        form_layout = QHBoxLayout()
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('ID')
        self.id_input.setEnabled(False)
        form_layout.addWidget(self.id_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Имя')
        form_layout.addWidget(self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        form_layout.addWidget(self.email_input)
        
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText('Роль')
        form_layout.addWidget(self.role_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('Добавить')
        add_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_btn)
        
        update_btn = QPushButton('Обновить')
        update_btn.clicked.connect(self.update_user)
        button_layout.addWidget(update_btn)
        
        delete_btn = QPushButton('Удалить')
        delete_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
    
    def update_table(self, users):
        """Обновление таблицы с пользователями"""
        self.table.setRowCount(0)
        
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(user['name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(user['email']))
            self.table.setItem(row_position, 3, QTableWidgetItem(user['role']))
    
    def get_selected_user_id(self):
        """Получение ID выбранного пользователя"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            item = self.table.item(row, 0)  # ID в первом столбце
            if item:
                return int(item.text())
        return None
    
    def on_selection_changed(self):
        """Обработка изменения выбора в таблице"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            
            # Заполняем поля ввода данными выбранного пользователя
            self.id_input.setText(self.table.item(row, 0).text())
            self.name_input.setText(self.table.item(row, 1).text())
            self.email_input.setText(self.table.item(row, 2).text())
            self.role_input.setText(self.table.item(row, 3).text())
    
    def add_user(self):
        """Добавление нового пользователя"""
        name = self.name_input.text()
        email = self.email_input.text()
        role = self.role_input.text()
        
        if name and email and role:
            self.controller.add_user(name, email, role)
            self.clear_inputs()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Предупреждение', 'Все поля должны быть заполнены!')
    
    def update_user(self):
        """Обновление выбранного пользователя"""
        user_id = self.get_selected_user_id()
        name = self.name_input.text()
        email = self.email_input.text()
        role = self.role_input.text()
        
        if user_id and name and email and role:
            self.controller.update_user(user_id, name, email, role)
            self.clear_inputs()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Предупреждение', 'Выберите пользователя и заполните все поля!')
    
    def delete_user(self):
        """Удаление выбранного пользователя"""
        user_id = self.get_selected_user_id()
        if user_id:
            self.controller.remove_user(user_id)
            self.clear_inputs()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Предупреждение', 'Выберите пользователя для удаления!')
    
    def clear_inputs(self):
        """Очистка полей ввода"""
        self.id_input.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.role_input.clear()

class UserController:
    """
    Контроллер для управления пользователями
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Подключаем сигнал изменения данных к обновлению представления
        self.model.data_changed.connect(self.update_view)
        
        # Инициализируем представление
        self.update_view()
    
    def add_user(self, name, email, role):
        """Добавление пользователя"""
        self.model.add_user(name, email, role)
    
    def remove_user(self, user_id):
        """Удаление пользователя"""
        self.model.remove_user(user_id)
    
    def update_user(self, user_id, name, email, role):
        """Обновление пользователя"""
        self.model.update_user(user_id, name, email, role)
    
    def update_view(self):
        """Обновление представления"""
        users = self.model.get_users()
        self.view.update_table(users)

class MVCExampleApp(QMainWindow):
    """
    Пример приложения с паттерном MVC
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Создаем компоненты MVC
        self.model = UserModel()
        self.view = UserView(None)  # Временно None, контроллер создадим позже
        self.controller = UserController(self.model, self.view)
        
        # Назначаем контроллер в представление
        self.view.controller = self.controller
        
        # Устанавливаем представление как центральный виджет
        self.setCentralWidget(self.view)
    
    def init_ui(self):
        self.setWindowTitle('Пример MVC в PyQt')
        self.setGeometry(100, 100, 800, 600)

def run_mvc_example():
    app = QApplication(sys.argv)
    mvc_app = MVCExampleApp()
    mvc_app.show()
    sys.exit(app.exec_())

# Для запуска примера MVC раскомментируйте следующую строку:
# run_mvc_example()
```

### MVP (Model-View-Presenter) паттерн

```python
from abc import ABC, abstractmethod

class IUserView(ABC):
    """
    Абстрактный интерфейс представления
    """
    @abstractmethod
    def display_users(self, users):
        pass
    
    @abstractmethod
    def get_user_data(self):
        pass
    
    @abstractmethod
    def show_message(self, message):
        pass

class UserPresenter:
    """
    Презентер для MVP паттерна
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def load_users(self):
        """Загрузка пользователей"""
        users = self.model.get_users()
        self.view.display_users(users)
    
    def add_user(self):
        """Добавление пользователя"""
        user_data = self.view.get_user_data()
        try:
            self.model.add_user(user_data['name'], user_data['email'], user_data['role'])
            self.load_users()
            self.view.show_message('Пользователь успешно добавлен')
        except ValueError as e:
            self.view.show_message(f'Ошибка: {str(e)}')
    
    def update_user(self):
        """Обновление пользователя"""
        user_data = self.view.get_user_data()
        try:
            self.model.update_user(user_data['id'], user_data['name'], user_data['email'], user_data['role'])
            self.load_users()
            self.view.show_message('Пользователь успешно обновлен')
        except ValueError as e:
            self.view.show_message(f'Ошибка: {str(e)}')
    
    def remove_user(self, user_id):
        """Удаление пользователя"""
        try:
            self.model.remove_user(user_id)
            self.load_users()
            self.view.show_message('Пользователь успешно удален')
        except ValueError as e:
            self.view.show_message(f'Ошибка: {str(e)}')

class MVPUserView(QWidget, IUserView):
    """
    Представление для MVP паттерна
    """
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Управление пользователями (MVP)')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Таблица пользователей
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Email', 'Роль'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Обработка событий таблицы
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.table)
        
        # Форма для редактирования
        form_layout = QHBoxLayout()
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('ID')
        self.id_input.setEnabled(False)
        form_layout.addWidget(self.id_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Имя')
        form_layout.addWidget(self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        form_layout.addWidget(self.email_input)
        
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText('Роль')
        form_layout.addWidget(self.role_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('Добавить')
        add_btn.clicked.connect(self.presenter.add_user)
        button_layout.addWidget(add_btn)
        
        update_btn = QPushButton('Обновить')
        update_btn.clicked.connect(self.presenter.update_user)
        button_layout.addWidget(update_btn)
        
        delete_btn = QPushButton('Удалить')
        delete_btn.clicked.connect(self.on_delete_click)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
    
    def display_users(self, users):
        """Отображение пользователей"""
        self.table.setRowCount(0)
        
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(user['name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(user['email']))
            self.table.setItem(row_position, 3, QTableWidgetItem(user['role']))
    
    def get_user_data(self):
        """Получение данных пользователя из формы"""
        return {
            'id': int(self.id_input.text()) if self.id_input.text().isdigit() else 0,
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'role': self.role_input.text()
        }
    
    def show_message(self, message):
        """Показ сообщения пользователю"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, 'Информация', message)
    
    def on_selection_changed(self):
        """Обработка изменения выбора в таблице"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            
            # Заполняем поля ввода данными выбранного пользователя
            self.id_input.setText(self.table.item(row, 0).text())
            self.name_input.setText(self.table.item(row, 1).text())
            self.email_input.setText(self.table.item(row, 2).text())
            self.role_input.setText(self.table.item(row, 3).text())
    
    def on_delete_click(self):
        """Обработка нажатия кнопки удаления"""
        user_id = self.get_selected_user_id()
        if user_id:
            self.presenter.remove_user(user_id)
        else:
            self.show_message('Выберите пользователя для удаления!')
    
    def get_selected_user_id(self):
        """Получение ID выбранного пользователя"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            item = self.table.item(row, 0)
            if item:
                return int(item.text())
        return None

class MVPExampleApp(QMainWindow):
    """
    Пример приложения с паттерном MVP
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Создаем компоненты MVP
        self.model = UserModel()
        self.view = MVPUserView(None)  # Временно None
        self.presenter = UserPresenter(self.model, self.view)
        
        # Назначаем презентер в представление
        self.view.presenter = self.presenter
        
        # Инициализируем отображение
        self.presenter.load_users()
        
        # Устанавливаем представление как центральный виджет
        self.setCentralWidget(self.view)
    
    def init_ui(self):
        self.setWindowTitle('Пример MVP в PyQt')
        self.setGeometry(100, 100, 800, 600)

def run_mvp_example():
    app = QApplication(sys.argv)
    mvp_app = MVPExampleApp()
    mvp_app.show()
    sys.exit(app.exec_())

# Для запуска примера MVP раскомментируйте следующую строку:
# run_mvp_example()
```

---

## 3. Многопоточность в PyQt

### QThread и сигналы/слоты

```python
from PyQt5.QtCore import QThread, pyqtSignal
import time
import random

class WorkerThread(QThread):
    """
    Рабочий поток для выполнения задач в фоне
    """
    # Определение сигналов
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, task_name, task_duration=100):
        super().__init__()
        self.task_name = task_name
        self.task_duration = task_duration
        self._is_running = True
    
    def run(self):
        """
        Метод, который выполняется в потоке
        """
        try:
            for i in range(self.task_duration):
                if not self._is_running:
                    break
                
                # Симуляция работы
                time.sleep(0.05)
                
                # Отправка прогресса
                self.progress_signal.emit(int((i+1)/self.task_duration * 100))
            
            if self._is_running:
                self.result_signal.emit(f"Задача '{self.task_name}' завершена")
            else:
                self.result_signal.emit(f"Задача '{self.task_name}' отменена")
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def stop(self):
        """
        Остановка потока
        """
        self._is_running = False

class ThreadingDemo(QWidget):
    """
    Демонстрация многопоточности в PyQt
    """
    def __init__(self):
        super().__init__()
        self.threads = []  # Список активных потоков
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Многопоточность в PyQt')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Текстовая область для вывода
        self.output_area = QTextEdit()
        self.output_area.setMaximumHeight(200)
        layout.addWidget(QLabel('Вывод:'))
        layout.addWidget(self.output_area)
        
        # Прогресс бары
        self.progress_bars = []
        for i in range(3):
            progress_layout = QHBoxLayout()
            progress_label = QLabel(f'Задача {i+1}:')
            progress_bar = QProgressBar()
            progress_bar.setValue(0)
            
            progress_layout.addWidget(progress_label)
            progress_layout.addWidget(progress_bar)
            
            layout.addLayout(progress_layout)
            self.progress_bars.append(progress_bar)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        start_all_btn = QPushButton('Запустить все задачи')
        start_all_btn.clicked.connect(self.start_all_tasks)
        button_layout.addWidget(start_all_btn)
        
        stop_all_btn = QPushButton('Остановить все задачи')
        stop_all_btn.clicked.connect(self.stop_all_tasks)
        button_layout.addWidget(stop_all_btn)
        
        clear_btn = QPushButton('Очистить вывод')
        clear_btn.clicked.connect(self.clear_output)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
    
    def start_all_tasks(self):
        """
        Запуск всех задач в отдельных потоках
        """
        self.clear_output()
        
        for i in range(3):
            task_name = f"Задача {i+1}"
            task_duration = random.randint(50, 150)  # Случайная продолжительность
            
            thread = WorkerThread(task_name, task_duration)
            thread.progress_signal.connect(lambda value, idx=i: self.update_progress(value, idx))
            thread.result_signal.connect(self.show_result)
            thread.error_signal.connect(self.show_error)
            
            self.threads.append(thread)
            thread.start()
    
    def update_progress(self, value, index):
        """
        Обновление прогресса для конкретной задачи
        """
        if 0 <= index < len(self.progress_bars):
            self.progress_bars[index].setValue(value)
    
    def show_result(self, message):
        """
        Отображение результата
        """
        self.output_area.append(f"Результат: {message}")
    
    def show_error(self, message):
        """
        Отображение ошибки
        """
        self.output_area.append(f"Ошибка: {message}")
    
    def stop_all_tasks(self):
        """
        Остановка всех активных задач
        """
        for thread in self.threads:
            if thread.isRunning():
                thread.stop()
        
        # Ожидание завершения всех потоков
        for thread in self.threads:
            if thread.isRunning():
                thread.wait(1000)  # Ждать до 1 секунды
        
        self.threads.clear()
        self.output_area.append("Все задачи остановлены")
    
    def clear_output(self):
        """
        Очистка текстовой области
        """
        self.output_area.clear()
        
        # Сброс всех прогресс баров
        for bar in self.progress_bars:
            bar.setValue(0)

class NetworkWorker(QThread):
    """
    Поток для имитации сетевых операций
    """
    data_received_signal = pyqtSignal(dict)
    status_signal = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self._is_running = True
    
    def run(self):
        """
        Имитация сетевого запроса
        """
        self.status_signal.emit(f"Начинается запрос к {self.url}")
        
        # Имитация сетевой задержки
        for i in range(10):
            if not self._is_running:
                return
            time.sleep(0.2)
            self.status_signal.emit(f"Загрузка... {i*10}%")
        
        if self._is_running:
            # Имитация полученных данных
            data = {
                'url': self.url,
                'status': 'success',
                'data': f'Данные с {self.url}',
                'timestamp': time.time()
            }
            self.data_received_signal.emit(data)
    
    def stop_request(self):
        """
        Остановка запроса
        """
        self._is_running = False

class NetworkRequestDemo(QWidget):
    """
    Демонстрация сетевых запросов в потоке
    """
    def __init__(self):
        super().__init__()
        self.network_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Сетевые запросы в потоке')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Поле ввода URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel('URL:'))
        self.url_input = QLineEdit('http://example.com/api/data')
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.request_btn = QPushButton('Выполнить запрос')
        self.request_btn.clicked.connect(self.make_request)
        button_layout.addWidget(self.request_btn)
        
        self.cancel_btn = QPushButton('Отменить запрос')
        self.cancel_btn.clicked.connect(self.cancel_request)
        self.cancel_btn.setEnabled(False)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel('Готов')
        layout.addWidget(self.status_label)
        
        # Результат
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(QLabel('Результат:'))
        layout.addWidget(self.result_area)
    
    def make_request(self):
        """
        Выполнение сетевого запроса
        """
        if self.network_thread and self.network_thread.isRunning():
            self.status_label.setText('Запрос уже выполняется')
            return
        
        url = self.url_input.text()
        if not url:
            self.status_label.setText('Введите URL')
            return
        
        self.request_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.network_thread = NetworkWorker(url)
        self.network_thread.data_received_signal.connect(self.on_data_received)
        self.network_thread.status_signal.connect(self.on_status_update)
        
        self.network_thread.start()
    
    def on_data_received(self, data):
        """
        Обработка полученных данных
        """
        self.result_area.setPlainText(str(data))
        self.status_label.setText('Запрос завершен успешно')
        self.request_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def on_status_update(self, status):
        """
        Обновление статуса
        """
        self.status_label.setText(status)
        if 'Загрузка' in status and '%' in status:
            try:
                percent = int(status.split()[-1].rstrip('%'))
                self.progress_bar.setValue(percent)
            except:
                pass
    
    def cancel_request(self):
        """
        Отмена сетевого запроса
        """
        if self.network_thread and self.network_thread.isRunning():
            self.network_thread.stop_request()
            self.status_label.setText('Запрос отменен')
            self.request_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            self.progress_bar.setVisible(False)

def run_threading_demo():
    app = QApplication(sys.argv)
    demo = ThreadingDemo()
    demo.show()
    sys.exit(app.exec_())

def run_network_demo():
    app = QApplication(sys.argv)
    demo = NetworkRequestDemo()
    demo.show()
    sys.exit(app.exec_())

# Для запуска демонстрации многопоточности раскомментируйте следующую строку:
# run_threading_demo()
```

---

## 4. Пользовательские виджеты

### Создание пользовательского виджета

```python
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import QRect, QPoint

class CustomButton(QPushButton):
    """
    Пользовательская кнопка с дополнительными возможностями
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        # Добавим анимацию при наведении
        self.animation_active = False
    
    def enterEvent(self, event):
        """Событие при наведении курсора"""
        self.animation_active = True
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Событие при уходе курсора"""
        self.animation_active = False
        super().leaveEvent(event)

class StatusIndicator(QWidget):
    """
    Пользовательский виджет индикатора статуса
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = "neutral"  # neutral, success, warning, error
        self.size = 20
        self.setFixedSize(self.size, self.size)
    
    def set_status(self, status):
        """
        Установка статуса индикатора
        """
        self.status = status
        self.update()  # Перерисовка виджета
    
    def paintEvent(self, event):
        """
        Перерисовка виджета
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Определение цвета в зависимости от статуса
        colors = {
            "neutral": QColor(128, 128, 128),   # Серый
            "success": QColor(0, 255, 0),      # Зеленый
            "warning": QColor(255, 255, 0),    # Желтый
            "error": QColor(255, 0, 0)         # Красный
        }
        
        color = colors.get(self.status, colors["neutral"])
        
        # Рисование круга
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color, 2))
        painter.drawEllipse(2, 2, self.size-4, self.size-4)

class CustomInputWidget(QWidget):
    """
    Пользовательский виджет ввода с индикатором валидности
    """
    def __init__(self, label_text="Поле ввода:", parent=None):
        super().__init__(parent)
        self.init_ui(label_text)
    
    def init_ui(self, label_text):
        layout = QHBoxLayout(self)
        
        # Метка
        self.label = QLabel(label_text)
        layout.addWidget(self.label)
        
        # Поле ввода
        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.validate_input)
        layout.addWidget(self.line_edit)
        
        # Индикатор валидности
        self.status_indicator = StatusIndicator()
        layout.addWidget(self.status_indicator)
        
        # Кнопка очистки
        self.clear_button = QPushButton("×")
        self.clear_button.setFixedSize(25, 25)
        self.clear_button.clicked.connect(self.clear_input)
        layout.addWidget(self.clear_button)
    
    def validate_input(self, text):
        """
        Валидация ввода и обновление индикатора
        """
        if len(text) == 0:
            self.status_indicator.set_status("neutral")
        elif len(text) < 3:
            self.status_indicator.set_status("warning")
        else:
            self.status_indicator.set_status("success")
    
    def clear_input(self):
        """
        Очистка поля ввода
        """
        self.line_edit.clear()
    
    def get_text(self):
        """
        Получение текста из поля ввода
        """
        return self.line_edit.text()
    
    def set_text(self, text):
        """
        Установка текста в поле ввода
        """
        self.line_edit.setText(text)

class DashboardWidget(QWidget):
    """
    Сложный пользовательский виджет - дашборд
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metrics = {
            'users': 0,
            'orders': 0,
            'revenue': 0.0
        }
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Дашборд')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Создание метрик
        metrics_layout = QHBoxLayout()
        
        self.create_metric_card(metrics_layout, 'Пользователи', 'users')
        self.create_metric_card(metrics_layout, 'Заказы', 'orders')
        self.create_metric_card(metrics_layout, 'Доход', 'revenue')
        
        layout.addLayout(metrics_layout)
        
        # Кнопки обновления
        button_layout = QHBoxLayout()
        
        update_btn = QPushButton('Обновить метрики')
        update_btn.clicked.connect(self.update_metrics)
        button_layout.addWidget(update_btn)
        
        reset_btn = QPushButton('Сбросить метрики')
        reset_btn.clicked.connect(self.reset_metrics)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
    
    def create_metric_card(self, parent_layout, title, metric_key):
        """
        Создание карточки метрики
        """
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(str(self.metrics[metric_key]))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 24px; color: #333;")
        card_layout.addWidget(value_label)
        
        # Сохраняем ссылку на метку значения
        setattr(self, f"{metric_key}_label", value_label)
        
        parent_layout.addWidget(card)
    
    def update_metrics(self):
        """
        Обновление метрик с имитацией получения данных
        """
        import random
        
        self.metrics['users'] = random.randint(100, 1000)
        self.metrics['orders'] = random.randint(50, 500)
        self.metrics['revenue'] = round(random.uniform(1000, 10000), 2)
        
        # Обновление отображения
        self.users_label.setText(str(self.metrics['users']))
        self.orders_label.setText(str(self.metrics['orders']))
        self.revenue_label.setText(f"${self.metrics['revenue']:,.2f}")
    
    def reset_metrics(self):
        """
        Сброс метрик
        """
        self.metrics = {'users': 0, 'orders': 0, 'revenue': 0.0}
        
        self.users_label.setText(str(self.metrics['users']))
        self.orders_label.setText(str(self.metrics['orders']))
        self.revenue_label.setText(f"${self.metrics['revenue']:,.2f}")

def run_custom_widgets_demo():
    """
    Запуск демонстрации пользовательских виджетов
    """
    app = QApplication(sys.argv)
    
    # Создание главного окна
    main_window = QMainWindow()
    main_window.setWindowTitle('Пользовательские виджеты PyQt')
    main_window.setGeometry(100, 100, 800, 600)
    
    # Центральный виджет
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    
    # Пример пользовательской кнопки
    custom_btn = CustomButton("Нажми меня!")
    layout.addWidget(custom_btn)
    
    # Пример пользовательского виджета ввода
    input_widget = CustomInputWidget("Введите имя:")
    layout.addWidget(input_widget)
    
    # Пример дашборда
    dashboard = DashboardWidget()
    layout.addWidget(dashboard)
    
    main_window.show()
    sys.exit(app.exec_())

# Для запуска демонстрации пользовательских виджетов раскомментируйте следующую строку:
# run_custom_widgets_demo()
```

---

## 5. Работа с файловой системой

### QFileSystemModel и QTreeView

```python
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QListView, QSplitter
import os

class FileSystemBrowser(QMainWindow):
    """
    Файловый браузер с использованием QFileSystemModel
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Файловый браузер')
        self.setGeometry(100, 100, 1000, 700)
        
        # Создание центрального виджета с разделителем
        splitter = QSplitter(Qt.Horizontal)
        
        # Модель файловой системы
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        
        # Дерево файлов
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(''))
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        
        # Список файлов
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        
        # Подключение событий
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        self.list_view.clicked.connect(self.on_list_view_clicked)
        
        # Добавление виджетов к разделителю
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.list_view)
        splitter.setSizes([500, 500])
        
        self.setCentralWidget(splitter)
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Готов')
    
    def on_tree_view_clicked(self, index):
        """
        Обработка клика по дереву файлов
        """
        file_path = self.file_model.filePath(index)
        file_info = QFileInfo(file_path)
        
        if file_info.isDir():
            # Если кликнули на директорию, обновляем список
            self.list_view.setRootIndex(index)
            self.status_bar.showMessage(f'Директория: {file_path}')
        else:
            # Если кликнули на файл, показываем информацию
            size = file_info.size()
            modified = file_info.lastModified().toString()
            self.status_bar.showMessage(f'Файл: {file_path}, Размер: {size} байт, Изменен: {modified}')
    
    def on_list_view_clicked(self, index):
        """
        Обработка клика по списку файлов
        """
        file_path = self.file_model.filePath(index)
        file_info = QFileInfo(file_path)
        
        if file_info.isDir():
            # Если кликнули на директорию в списке, обновляем дерево
            self.tree_view.setRootIndex(index)
            self.status_bar.showMessage(f'Директория: {file_path}')
        else:
            # Если кликнули на файл, показываем информацию
            size = file_info.size()
            modified = file_info.lastModified().toString()
            self.status_bar.showMessage(f'Файл: {file_path}, Размер: {size} байт, Изменен: {modified}')

def run_file_system_browser():
    app = QApplication(sys.argv)
    browser = FileSystemBrowser()
    browser.show()
    sys.exit(app.exec_())

# Для запуска файлового браузера раскомментируйте следующую строку:
# run_file_system_browser()
```

---

## 6. Практические примеры

### Пример 1: Система управления задачами

```python
class Task:
    """
    Класс для представления задачи
    """
    def __init__(self, title, description="", priority="normal"):
        self.id = id(self)  # Простой ID для демонстрации
        self.title = title
        self.description = description
        self.priority = priority  # low, normal, high
        self.completed = False
        self.created_at = QDateTime.currentDateTime()

class TaskManagerModel(QObject):
    """
    Модель для управления задачами
    """
    tasks_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.tasks = []
    
    def add_task(self, title, description="", priority="normal"):
        """
        Добавление задачи
        """
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.tasks_changed.emit()
    
    def remove_task(self, task_id):
        """
        Удаление задачи по ID
        """
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.tasks_changed.emit()
    
    def complete_task(self, task_id):
        """
        Отметка задачи как выполненной
        """
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.tasks_changed.emit()
                break
    
    def get_tasks(self):
        """
        Получение всех задач
        """
        return self.tasks.copy()

class TaskManagerView(QWidget):
    """
    Представление для управления задачами
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Менеджер задач')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Форма добавления задачи
        form_layout = QHBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Название задачи')
        form_layout.addWidget(self.title_input)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText('Описание задачи')
        form_layout.addWidget(self.desc_input)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(['Низкий', 'Обычный', 'Высокий'])
        form_layout.addWidget(self.priority_combo)
        
        layout.addLayout(form_layout)
        
        # Кнопка добавления
        add_btn = QPushButton('Добавить задачу')
        add_btn.clicked.connect(self.add_task)
        layout.addWidget(add_btn)
        
        # Таблица задач
        self.task_table = QTableWidget(0, 4)
        self.task_table.setHorizontalHeaderLabels(['Название', 'Описание', 'Приоритет', 'Статус'])
        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.task_table)
        
        # Кнопки действий
        action_layout = QHBoxLayout()
        
        complete_btn = QPushButton('Выполнить задачу')
        complete_btn.clicked.connect(self.complete_task)
        action_layout.addWidget(complete_btn)
        
        delete_btn = QPushButton('Удалить задачу')
        delete_btn.clicked.connect(self.delete_task)
        action_layout.addWidget(delete_btn)
        
        layout.addLayout(action_layout)
    
    def update_task_table(self, tasks):
        """
        Обновление таблицы задач
        """
        self.task_table.setRowCount(0)
        
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            
            self.task_table.setItem(row_position, 0, QTableWidgetItem(task.title))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(task.description))
            
            priority_text = {"low": "Низкий", "normal": "Обычный", "high": "Высокий"}.get(task.priority, "Обычный")
            self.task_table.setItem(row_position, 2, QTableWidgetItem(priority_text))
            
            status_text = "Выполнена" if task.completed else "В процессе"
            status_item = QTableWidgetItem(status_text)
            
            # Изменение цвета в зависимости от статуса
            if task.completed:
                status_item.setBackground(QColor(144, 238, 144))  # Светло-зеленый
            else:
                status_item.setBackground(QColor(255, 182, 193))  # Светло-розовый
            
            self.task_table.setItem(row_position, 3, status_item)
    
    def add_task(self):
        """
        Добавление задачи
        """
        title = self.title_input.text().strip()
        description = self.desc_input.text().strip()
        priority_idx = self.priority_combo.currentIndex()
        priorities = ['low', 'normal', 'high']
        priority = priorities[priority_idx]
        
        if title:
            self.controller.add_task(title, description, priority)
            self.title_input.clear()
            self.desc_input.clear()
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Название задачи обязательно!')
    
    def complete_task(self):
        """
        Отметка задачи как выполненной
        """
        selected_rows = self.task_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            item = self.task_table.item(row, 0)  # Получаем ID из скрытой колонки
            if item:
                # В реальном приложении ID задачи хранился бы в скрытой колонке или в данных элемента
                # Для простоты примера будем использовать индекс в списке задач
                task_id = self.controller.get_task_id_by_index(row)
                self.controller.complete_task(task_id)
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите задачу для выполнения!')
    
    def delete_task(self):
        """
        Удаление задачи
        """
        selected_rows = self.task_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            task_id = self.controller.get_task_id_by_index(row)
            self.controller.remove_task(task_id)
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите задачу для удаления!')

class TaskManagerController:
    """
    Контроллер для управления задачами
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Подключение сигнала обновления
        self.model.tasks_changed.connect(self.update_view)
        
        # Инициализация представления
        self.update_view()
    
    def add_task(self, title, description, priority):
        """
        Добавление задачи
        """
        self.model.add_task(title, description, priority)
    
    def remove_task(self, task_id):
        """
        Удаление задачи
        """
        self.model.remove_task(task_id)
    
    def complete_task(self, task_id):
        """
        Отметка задачи как выполненной
        """
        self.model.complete_task(task_id)
    
    def update_view(self):
        """
        Обновление представления
        """
        tasks = self.model.get_tasks()
        self.view.update_task_table(tasks)
    
    def get_task_id_by_index(self, index):
        """
        Получение ID задачи по индексу (для демонстрации)
        """
        tasks = self.model.get_tasks()
        if 0 <= index < len(tasks):
            return tasks[index].id
        return None

class TaskManagerApp(QMainWindow):
    """
    Приложение менеджера задач
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Создание компонентов MVC
        self.model = TaskManagerModel()
        self.view = TaskManagerView(None)  # Временно None
        self.controller = TaskManagerController(self.model, self.view)
        
        # Назначение контроллера
        self.view.controller = self.controller
        
        self.setCentralWidget(self.view)
    
    def init_ui(self):
        self.setWindowTitle('Менеджер задач')
        self.setGeometry(100, 100, 900, 600)

def run_task_manager():
    app = QApplication(sys.argv)
    task_manager = TaskManagerApp()
    task_manager.show()
    sys.exit(app.exec_())

# Для запуска менеджера задач раскомментируйте следующую строку:
# run_task_manager()
```

### Пример 2: Калькулятор с историей

```python
class CalculatorHistoryModel(QObject):
    """
    Модель для хранения истории вычислений
    """
    history_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.history = []
    
    def add_calculation(self, expression, result):
        """
        Добавление вычисления в историю
        """
        calculation = {
            'expression': expression,
            'result': result,
            'timestamp': QDateTime.currentDateTime().toString("hh:mm:ss")
        }
        self.history.append(calculation)
        
        # Ограничиваем историю последними 50 записями
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        self.history_updated.emit()
    
    def get_history(self):
        """
        Получение истории вычислений
        """
        return self.history.copy()
    
    def clear_history(self):
        """
        Очистка истории
        """
        self.history.clear()
        self.history_updated.emit()

class CalculatorView(QWidget):
    """
    Представление калькулятора
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel('Калькулятор с историей')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Дисплей
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 18px; padding: 10px; background-color: #f0f0f0;")
        self.display.setFixedHeight(50)
        layout.addWidget(self.display)
        
        # Кнопки калькулятора
        buttons_layout = self.create_buttons_layout()
        layout.addLayout(buttons_layout)
        
        # История вычислений
        history_frame = QFrame()
        history_frame.setFrameShape(QFrame.StyledPanel)
        history_layout = QVBoxLayout(history_frame)
        
        history_title = QLabel('История вычислений')
        history_title.setStyleSheet("font-weight: bold;")
        history_layout.addWidget(history_title)
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        # Кнопка очистки истории
        clear_history_btn = QPushButton('Очистить историю')
        clear_history_btn.clicked.connect(self.controller.clear_history)
        history_layout.addWidget(clear_history_btn)
        
        layout.addWidget(history_frame)
        
        # Инициализация состояния
        self.current_input = '0'
        self.operator = None
        self.previous_input = None
        self.reset_on_next_input = False
    
    def create_buttons_layout(self):
        """
        Создание макета для кнопок калькулятора
        """
        grid_layout = QGridLayout()
        
        # Кнопки
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
                button.clicked.connect(lambda _, t=text: self.button_clicked(t))
                grid_layout.addWidget(button, row, col, 1, 2)
            else:
                button = QPushButton(text)
                button.clicked.connect(lambda _, t=text: self.button_clicked(t))
                grid_layout.addWidget(button, row, col)
        
        return grid_layout
    
    def button_clicked(self, text):
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
        if self.reset_on_next_input:
            self.current_input = '0'
            self.reset_on_next_input = False
        
        if self.current_input == '0' and number != '.':
            self.current_input = number
        elif number == '.' and '.' not in self.current_input:
            self.current_input += number
        elif number != '.':
            self.current_input += number
        
        self.display.setText(self.current_input)
    
    def input_operator(self, op):
        """
        Ввод оператора
        """
        if self.operator is not None and self.previous_input is not None and not self.reset_on_next_input:
            self.calculate()
        
        self.previous_input = self.current_input
        self.operator = op
        self.reset_on_next_input = True
    
    def calculate(self):
        """
        Выполнение вычисления
        """
        if self.operator is None or self.previous_input is None:
            return
        
        try:
            prev = float(self.previous_input)
            curr = float(self.current_input)
            
            if self.operator == '+':
                result = prev + curr
            elif self.operator == '-':
                result = prev - curr
            elif self.operator == '×':
                result = prev * curr
            elif self.operator == '÷':
                if curr == 0:
                    raise ZeroDivisionError("Деление на ноль")
                result = prev / curr
            
            # Добавление в историю
            expression = f"{self.previous_input} {self.operator} {self.current_input}"
            self.controller.add_to_history(expression, result)
            
            # Форматирование результата
            if result.is_integer():
                result = int(result)
            
            self.current_input = str(result)
            self.display.setText(self.current_input)
            
            self.operator = None
            self.previous_input = None
            self.reset_on_next_input = True
        except ZeroDivisionError:
            QMessageBox.error(self, "Ошибка", "Деление на ноль невозможно")
            self.clear()
        except Exception as e:
            QMessageBox.error(self, "Ошибка", f"Ошибка вычисления: {str(e)}")
            self.clear()
    
    def clear(self):
        """
        Очистка калькулятора
        """
        self.current_input = '0'
        self.operator = None
        self.previous_input = None
        self.reset_on_next_input = False
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

class CalculatorController:
    """
    Контроллер калькулятора
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Подключение сигнала обновления истории
        self.model.history_updated.connect(self.update_history_view)
    
    def add_to_history(self, expression, result):
        """
        Добавление вычисления в историю
        """
        self.model.add_calculation(expression, result)
    
    def clear_history(self):
        """
        Очистка истории
        """
        self.model.clear_history()
    
    def update_history_view(self):
        """
        Обновление представления истории
        """
        self.view.history_list.clear()
        history = self.model.get_history()
        
        for record in reversed(history):  # Отображаем в обратном порядке (новые сверху)
            item_text = f"{record['timestamp']}: {record['expression']} = {record['result']}"
            self.view.history_list.addItem(item_text)

class CalculatorApp(QMainWindow):
    """
    Приложение калькулятора
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Создание компонентов
        self.model = CalculatorHistoryModel()
        self.view = CalculatorView(None)  # Временно None
        self.controller = CalculatorController(self.model, self.view)
        
        # Назначение контроллера
        self.view.controller = self.controller
        
        self.setCentralWidget(self.view)
    
    def init_ui(self):
        self.setWindowTitle('Калькулятор с историей')
        self.setGeometry(100, 100, 400, 600)

def run_calculator_app():
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())

# Для запуска калькулятора раскомментируйте следующую строку:
# run_calculator_app()
```

---

## Заключение

Tkinter предоставляет мощный и гибкий инструментарий для создания графических интерфейсов в Python. Продвинутые виджеты, такие как QTableWidget, QTreeWidget и QListView, позволяют создавать сложные интерфейсы. Архитектурные паттерны MVC и MVP помогают организовать код приложения. Многопоточность позволяет выполнять длительные операции без блокировки интерфейса. Создание пользовательских виджетов расширяет возможности стандартных компонентов.

## Контрольные вопросы:
1. Какие продвинутые виджеты доступны в PyQt?
2. В чем отличие паттернов MVC и MVP?
3. Как реализовать многопоточность в PyQt?
4. Как создать пользовательский виджет?
5. Как работать с файловой системой в PyQt?
