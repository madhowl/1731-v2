"""
Упражнения к практической работе 30: Model-View в PyQt6

Выполните следующие упражнения для закрепления навыков
работы с паттерном Model-View в PyQt6.
"""

# ЗАДАНИЕ 1: QListView с кастомной моделью
def exercise_list_view():
    """
    ЗАДАНИЕ 1.1: Создайте приложение с QListView и кастомной моделью.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QListView, QPushButton, QLabel
    # QStandardItemModel, QStandardItem из PyQt6.QtGui
    # Qt из PyQt6.QtCore
    
    # TODO: Создайте приложение QApplication
    app = None
    
    # ЗАДАНИЕ 1.2: Создайте главное окно
    # TODO: Создайте виджет QWidget
    window = None
    
    # TODO: Установите заголовок и размеры окна
    
    # ЗАДАНИЕ 1.3: Создайте вертикальный макет
    # TODO: Создайте QVBoxLayout
    layout = None
    
    # ЗАДАНИЕ 1.4: Создайте метку для отображения выбранного элемента
    # TODO: Создайте QLabel с текстом "Выберите элемент:"
    label = None
    
    # TODO: Добавьте метку в макет
    
    # ЗАДАНИЕ 1.5: Создайте QListView и модель
    # TODO: Создайте QListView
    list_view = None
    
    # TODO: Создайте QStandardItemModel
    model = None
    
    # ЗАДАНИЕ 1.6: Добавьте элементы в модель
    # TODO: Добавьте элементы ["Python", "JavaScript", "C++", "Java", "Go", "Rust"] в модель
    
    # ЗАДАНИЕ 1.7: Установите модель для представления
    # TODO: Установите модель для list_view
    
    # TODO: Добавьте list_view в макет
    
    # ЗАДАНИЕ 1.8: Создайте обработчик клика по элементу
    # TODO: Реализуйте функцию on_clicked, которая будет обновлять текст метки
    
    # ЗАДАНИЕ 1.9: Привяжите обработчик к сигналу клика
    # TODO: Привяжите функцию on_clicked к сигналу clicked у list_view
    
    # ЗАДАНИЕ 1.10: Установите макет для окна и отобразите его
    # TODO: Установите макет для окна и покажите его
    
    # ЗАДАНИЕ 1.11: Запустите цикл обработки событий
    # TODO: Запустите главный цикл приложения
    pass


# ЗАДАНИЕ 2: QTableView с моделью
def exercise_table_view():
    """
    ЗАДАНИЕ 2.1: Создайте приложение с QTableView и табличной моделью.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QTableView, QPushButton
    # QStandardItemModel из PyQt6.QtGui
    
    # TODO: Создайте приложение
    app = None
    
    # TODO: Создайте главное окно
    window = None
    
    # TODO: Установите заголовок и геометрию окна
    
    # TODO: Создайте вертикальный макет
    layout = None
    
    # TODO: Создайте QTableView
    table_view = None
    
    # TODO: Создайте QStandardItemModel с 5 строками и 3 колонками
    model = None
    
    # ЗАДАНИЕ 2.2: Установите заголовки колонок
    # TODO: Установите заголовки колонок: ["Имя", "Возраст", "Город"]
    
    # ЗАДАНИЕ 2.3: Добавьте данные в таблицу
    data = [
        ["Анна", "25", "Москва"],
        ["Борис", "30", "Санкт-Петербург"],
        ["Виктор", "35", "Новосибирск"],
        ["Галина", "28", "Екатеринбург"],
        ["Дмитрий", "32", "Казань"],
    ]
    # TODO: Добавьте данные в модель
    
    # ЗАДАНИЕ 2.4: Установите модель для представления
    # TODO: Установите модель для table_view
    
    # TODO: Автоматически подгоните размеры колонок под содержимое
    
    # TODO: Добавьте table_view в макет
    
    # TODO: Установите макет для окна
    
    # TODO: Покажите окно
    
    # TODO: Запустите цикл обработки событий приложения
    pass


# ЗАДАНИЕ 3: QTreeView с иерархической моделью
def exercise_tree_view():
    """
    ЗАДАНИЕ 3.1: Создайте приложение с QTreeView и иерархической моделью.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QTreeView, QPushButton
    # QStandardItemModel, QStandardItem из PyQt6.QtGui
    
    # TODO: Создайте приложение
    app = None
    
    # TODO: Создайте главное окно
    window = None
    
    # TODO: Установите заголовок и геометрию окна
    
    # TODO: Создайте вертикальный макет
    layout = None
    
    # TODO: Создайте QTreeView
    tree_view = None
    
    # TODO: Создайте QStandardItemModel
    model = None
    
    # ЗАДАНИЕ 3.2: Установите заголовок колонки
    # TODO: Установите заголовок колонки: ["Название"]
    
    # ЗАДАНИЕ 3.3: Создайте иерархию элементов
    # TODO: Создайте корневой элемент "Компьютер"
    root = None
    
    # TODO: Добавьте корневой элемент в модель
    
    # TODO: Создайте дочерние элементы "Программы" и "Документы"
    programs = None
    docs = None
    
    # TODO: Добавьте "Программы" и "Документы" как дочерние элементы корня
    
    # TODO: Добавьте элементы "Word", "Excel", "Chrome" в "Программы"
    
    # TODO: Добавьте элементы "Отчёт.docx", "Презентация.pptx" в "Документы"
    
    # TODO: Добавьте элементы "Музыка" и "Видео" как дочерние элементы корня
    
    # ЗАДАНИЕ 3.4: Установите модель для представления
    # TODO: Установите модель для tree_view
    
    # TODO: Разверните все узлы дерева
    
    # TODO: Добавьте tree_view в макет
    
    # TODO: Установите макет для окна
    
    # TODO: Покажите окно
    
    # TODO: Запустите цикл обработки событий приложения
    pass


# ЗАДАНИЕ 4: Редактируемая модель
def exercise_editable_model():
    """
    ЗАДАНИЕ 4.1: Создайте редактируемую табличную модель.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QTableView, QPushButton, QMessageBox
    # QStandardItemModel, QStandardItem из PyQt6.QtGui
    # Qt из PyQt6.QtCore
    
    class EditableTableModel:
        """
        ЗАДАНИЕ 4.2: Создайте редактируемую модель
        - Наследуйте QStandardItemModel
        - Переопределите метод flags для включения редактирования
        """
        # TODO: Наследуйте QStandardItemModel
        
        def __init__(self, rows, cols):
            """
            ЗАДАНИЕ 4.3: Инициализируйте модель
            - Вызовите родительский конструктор
            """
            # TODO: Вызовите родительский конструктор с параметрами rows и cols
            pass
        
        def flags(self, index):
            """
            ЗАДАНИЕ 4.4: Переопределите метод flags
            - Включите флаги ItemIsEnabled, ItemIsSelectable, ItemIsEditable
            """
            # TODO: Если индекс действителен, верните флаги: ItemIsEnabled | ItemIsSelectable | ItemIsEditable
            # TODO: Иначе верните родительскую реализацию
            pass
    
    # TODO: Создайте приложение
    app = None
    
    # TODO: Создайте главное окно
    window = None
    
    # TODO: Установите заголовок и геометрию окна
    
    # TODO: Создайте вертикальный макет
    layout = None
    
    # TODO: Создайте QTableView
    table_view = None
    
    # TODO: Создайте EditableTableModel с 3 строками и 2 колонками
    model = None
    
    # ЗАДАНИЕ 4.5: Установите заголовки колонок
    # TODO: Установите заголовки колонок: ["Товар", "Цена"]
    
    # ЗАДАНИЕ 4.6: Добавьте начальные данные
    data = [["Ноутбук", "50000"], ["Телефон", "30000"], ["Планшет", "25000"]]
    # TODO: Добавьте начальные данные в модель
    
    # ЗАДАНИЕ 4.7: Установите модель для представления
    # TODO: Установите модель для table_view
    
    # TODO: Добавьте table_view в макет
    
    def show_data():
        """
        ЗАДАНИЕ 4.8: Реализуйте функцию отображения данных
        - Пройдитесь по всем элементам модели
        - Выведите данные в консоль
        - Покажите сообщение в MessageBox
        """
        # TODO: Пройдитесь по всем строкам и колонкам модели
        # TODO: Выведите данные в консоль
        # TODO: Покажите QMessageBox с информацией
        pass
    
    # TODO: Создайте кнопку "Показать данные" с обработчиком show_data
    button = None
    
    # TODO: Подключите сигнал clicked кнопки к функции show_data
    
    # TODO: Добавьте кнопку в макет
    
    # TODO: Установите макет для окна
    
    # TODO: Покажите окно
    
    # TODO: Запустите цикл обработки событий приложения
    pass


# ЗАДАНИЕ 5: Фильтрация модели
def exercise_filter_model():
    """
    ЗАДАНИЕ 5.1: Создайте таблицу с возможностью фильтрации.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QTableView, QLineEdit
    # QStandardItemModel, QStandardItem, QSortFilterProxyModel из PyQt6.QtGui
    
    # TODO: Создайте приложение
    app = None
    
    # TODO: Создайте главное окно
    window = None
    
    # TODO: Установите заголовок и геометрию окна
    
    # TODO: Создайте вертикальный макет
    layout = None
    
    # TODO: Создайте QLineEdit для поиска
    search = None
    
    # TODO: Установите плейсхолдер "Поиск..."
    
    # TODO: Добавьте поле поиска в макет
    
    # TODO: Создайте QTableView
    table_view = None
    
    # ЗАДАНИЕ 5.2: Создайте исходную модель
    # TODO: Создайте QStandardItemModel с 5 строками и 2 колонками
    source_model = None
    
    # TODO: Установите заголовки колонок: ["Имя", "Город"]
    
    data = [
        ["Анна Москва", "Москва"],
        ["Борис Санкт", "Санкт-Петербург"],
        ["Виктор Новосиб", "Новосибирск"],
        ["Галина Екат", "Екатеринбург"],
        ["Дмитрий Казань", "Казань"],
    ]
    # TODO: Добавьте данные в исходную модель
    
    # ЗАДАНИЕ 5.3: Создайте прокси-модель для фильтрации
    # TODO: Создайте QSortFilterProxyModel
    proxy_model = None
    
    # TODO: Установите исходную модель для прокси-модели
    
    # TODO: Установите колонку для фильтрации (0 - первая колонка)
    
    # ЗАДАНИЕ 5.4: Установите модель для представления
    # TODO: Установите прокси-модель для table_view
    
    # TODO: Добавьте table_view в макет
    
    def on_search(text):
        """
        ЗАДАНИЕ 5.5: Реализуйте обработчик поиска
        - Установите регулярное выражение фильтрации
        """
        # TODO: Установите регулярное выражение фильтрации для прокси-модели
        pass
    
    # TODO: Подключите сигнал textChanged поля поиска к функции on_search
    
    # TODO: Установите макет для окна
    
    # TODO: Покажите окно
    
    # TODO: Запустите цикл обработки событий приложения
    pass


# ЗАДАНИЕ 6: Кастомная модель списка
class CustomListModel:
    """Кастомная модель для списка задач"""
    
    def __init__(self, items=None):
        """
        ЗАДАНИЕ 6.1: Инициализируйте кастомную модель
        - Сохраните список элементов
        """
        # TODO: Сохраните items или создайте пустой список
        self.items = []
    
    def rowCount(self, parent=None):
        """
        ЗАДАНИЕ 6.2: Реализуйте метод rowCount
        - Верните количество элементов
        """
        # TODO: Верните длину списка элементов
        pass
    
    def data(self, index, role):
        """
        ЗАДАНИЕ 6.3: Реализуйте метод data
        - Верните данные элемента по индексу
        """
        # TODO: Если роль DisplayRole (0) и индекс действителен, верните элемент
        # TODO: Иначе верните None
        pass
    
    def addItem(self, item):
        """
        ЗАДАНИЕ 6.4: Реализуйте метод addItem
        - Добавьте элемент в список
        """
        # TODO: Добавьте элемент в список
        pass
    
    def removeRow(self, row):
        """
        ЗАДАНИЕ 6.5: Реализуйте метод removeRow
        - Удалите элемент по индексу
        """
        # TODO: Если индекс в пределах допустимого диапазона, удалите элемент и верните True
        # TODO: Иначе верните False
        pass


def exercise_custom_model():
    """
    ЗАДАНИЕ 6.6: Создайте кастомную модель и представление.
    """
    # TODO: Импортируйте необходимые элементы:
    # QApplication, QWidget, QVBoxLayout, QListView, QPushButton, QLineEdit
    # QAbstractListModel из PyQt6.QtCore
    # Qt, QModelIndex из PyQt6.QtCore
    
    class StringListModel:
        """
        ЗАДАНИЕ 6.7: Создайте модель на основе QAbstractListModel
        - Реализуйте необходимые методы
        """
        # TODO: Наследуйте QAbstractListModel
        
        def __init__(self, data=None):
            """
            ЗАДАНИЕ 6.8: Инициализируйте модель
            - Вызовите родительский конструктор
            - Сохраните данные
            """
            # TODO: Вызовите родительский конструктор
            # TODO: Сохраните data или создайте пустой список
            self._data = []
        
        def rowCount(self, parent=None):
            """
            ЗАДАНИЕ 6.9: Реализуйте метод rowCount
            - Верните количество элементов
            """
            # TODO: Верните длину списка данных
            pass
        
        def data(self, index, role=None):
            """
            ЗАДАНИЕ 6.10: Реализуйте метод data
            - Верните данные элемента по индексу
            """
            # TODO: Если роль DisplayRole и индекс действителен, верните элемент
            # TODO: Иначе верните None
            pass
        
        def appendRow(self, text):
            """
            ЗАДАНИЕ 6.11: Реализуйте метод appendRow
            - Добавьте элемент в модель с правильными сигналами
            """
            # TODO: Вызовите beginInsertRows с правильными параметрами
            # TODO: Добавьте элемент в список данных
            # TODO: Вызовите endInsertRows
            pass
    
    # TODO: Создайте приложение
    app = None
    
    # TODO: Создайте главное окно
    window = None
    
    # TODO: Установите заголовок и геометрию окна
    
    # TODO: Создайте вертикальный макет
    layout = None
    
    # TODO: Создайте QListView
    list_view = None
    
    # TODO: Создайте StringListModel с начальными элементами ["Первый", "Второй", "Третий"]
    model = None
    
    # TODO: Установите модель для list_view
    
    # TODO: Добавьте list_view в макет
    
    # TODO: Создайте QLineEdit с плейсхолдером "Новый элемент"
    edit = None
    
    # TODO: Добавьте поле ввода в макет
    
    def add_item():
        """
        ЗАДАНИЕ 6.12: Реализуйте функцию добавления элемента
        - Получите текст из поля ввода
        - Добавьте элемент в модель
        - Очистите поле ввода
        """
        # TODO: Получите текст из поля ввода
        # TODO: Если текст не пустой, добавьте его в модель
        # TODO: Очистите поле ввода
        pass
    
    def remove_selected():
        """
        ЗАДАНИЕ 6.13: Реализуйте функцию удаления выбранного элемента
        - Получите текущий индекс
        - Удалите элемент из модели
        """
        # TODO: Получите текущий индекс из list_view
        # TODO: Если индекс действителен, удалите строку из модели
        pass
    
    # TODO: Создайте вертикальный макет для кнопок
    btn_layout = None
    
    # TODO: Создайте кнопки "Добавить" и "Удалить"
    add_btn = None
    remove_btn = None
    
    # TODO: Подключите сигналы кнопок к соответствующим функциям
    
    # TODO: Добавьте кнопки в макет кнопок
    
    # TODO: Добавьте макет кнопок в основной макет
    
    # TODO: Установите макет для окна
    
    # TODO: Покажите окно
    
    # TODO: Запустите цикл обработки событий приложения
    pass


if __name__ == "__main__":
    print("Доступные упражнения:")
    print("1. exercise_list_view() - QListView")
    print("2. exercise_table_view() - QTableView")
    print("3. exercise_tree_view() - QTreeView")
    print("4. exercise_editable_model() - Редактируемая модель")
    print("5. exercise_filter_model() - Фильтрация")
    print("6. exercise_custom_model() - Кастомная модель")
    print("\nДля запуска упражнения раскомментируйте нужную функцию:")
    # exercise_list_view()
    # exercise_table_view()
    # exercise_tree_view()
    # exercise_editable_model()
    # exercise_filter_model()
    # exercise_custom_model()
