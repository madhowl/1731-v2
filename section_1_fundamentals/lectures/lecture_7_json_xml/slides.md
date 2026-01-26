# Лекция 7: Работа с JSON и XML

## Парсинг и создание JSON и XML документов, библиотеки xml.etree.ElementTree, lxml

### План лекции:
1. Введение в JSON и XML
2. Работа с JSON в Python
3. Работа с XML в Python
4. Библиотека xml.etree.ElementTree
5. Библиотека lxml (внешняя)
6. Практические примеры

---

## 1. Введение в JSON и XML

### Что такое JSON?

JSON (JavaScript Object Notation) - это легковесный формат обмена данными. Он легко читается и записывается людьми, а также легко парсится и генерируется машинами.

```json
{
  "name": "Иван Иванов",
  "age": 30,
  "email": "ivan@example.com",
  "address": {
    "street": "Ленина 10",
    "city": "Москва",
    "zipcode": "123456"
  },
  "phones": [
    {"type": "mobile", "number": "+7-123-456-78-90"},
    {"type": "home", "number": "+7-123-456-78-91"}
  ]
}
```

### Что такое XML?

XML (eXtensible Markup Language) - это расширяемый язык разметки, который определяет правила кодирования документов в формате, который является и человечески читаемым, и машиночитаемым.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<person>
  <name>Иван Иванов</name>
  <age>30</age>
  <email>ivan@example.com</email>
  <address>
    <street>Ленина 10</street>
    <city>Москва</city>
    <zipcode>123456</zipcode>
  </address>
  <phones>
    <phone type="mobile">+7-123-456-78-90</phone>
    <phone type="home">+7-123-456-78-91</phone>
  </phones>
</person>
```

### Сравнение JSON и XML:

| Особенность | JSON | XML |
|-------------|------|-----|
| Читаемость | Простой синтаксис | Более сложный синтаксис |
| Размер | Меньше | Больше из-за тегов |
| Типизация | Поддержка типов данных | Только строки |
| Парсинг | Простой | Требует больше кода |
| Поддержка | Широкая | Универсальная |

---

## 2. Работа с JSON в Python

В Python есть встроенный модуль `json` для работы с JSON-данными.

```python
import json

# Пример Python-объекта
data = {
    "name": "Иван Иванов",
    "age": 30,
    "email": "ivan@example.com",
    "hobbies": ["чтение", "плавание", "программирование"]
}

# Преобразование Python-объекта в JSON-строку (сериализация)
json_string = json.dumps(data, ensure_ascii=False, indent=2)
print(json_string)
```

### Основные методы модуля json:

```python
import json

# dumps() - преобразует Python-объект в JSON-строку
data = {"name": "Иван", "age": 30}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "Иван", "age": 30}

# loads() - преобразует JSON-строку в Python-объект
loaded_data = json.loads(json_str)
print(loaded_data)  # {'name': 'Иван', 'age': 30}

# dump() - записывает Python-объект в файл в формате JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# load() - читает JSON-данные из файла
with open('data.json', 'r', encoding='utf-8') as f:
    loaded_from_file = json.load(f)
    print(loaded_from_file)
```

### Параметры функций json:

```python
import json

data = {"name": "Иван", "age": 30, "active": True}

# ensure_ascii=False - позволяет использовать не-ASCII символы
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "Иван", "age": 30, "active": true}

# indent - форматирует вывод с отступами
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
# {
#   "name": "Иван",
#   "age": 30,
#   "active": true
# }

# separators - позволяет настроить разделители
json_str = json.dumps(data, separators=(',', ':'))
print(json_str)  # {"name":"Иван","age":30,"active":true}

# sort_keys - сортирует ключи
data_with_keys = {"z": 1, "a": 2, "m": 3}
json_str = json.dumps(data_with_keys, sort_keys=True, indent=2)
print(json_str)
# {
#   "a": 2,
#   "m": 3,
#   "z": 1
# }
```

---

## 3. Работа с XML в Python

Python предоставляет несколько способов работы с XML:
- `xml.etree.ElementTree` - встроенная библиотека
- `lxml` - внешняя библиотека (требует установки)
- `xml.dom.minidom` - древовидный интерфейс
- `xml.sax` - событийный интерфейс

### Создание XML с помощью ElementTree:

```python
import xml.etree.ElementTree as ET

# Создание корневого элемента
root = ET.Element("catalog")

# Добавление дочерних элементов
book1 = ET.SubElement(root, "book", id="1")
title1 = ET.SubElement(book1, "title")
title1.text = "Python Programming"
author1 = ET.SubElement(book1, "author")
author1.text = "John Doe"

book2 = ET.SubElement(root, "book", id="2")
title2 = ET.SubElement(book2, "title")
title2.text = "Web Development"
author2 = ET.SubElement(book2, "author")
author2.text = "Jane Smith"

# Преобразование в строку
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)  # Форматирование (Python 3.9+)
tree.write("catalog.xml", encoding="unicode", xml_declaration=True)

# Вывод строки
print(ET.tostring(root, encoding="unicode"))
```

---

## 4. Библиотека xml.etree.ElementTree

ElementTree предоставляет легковесный и эффективный API для парсинга и создания XML-данных.

### Парсинг XML:

```python
import xml.etree.ElementTree as ET

# XML-строка
xml_string = '''
<library>
    <book id="1">
        <title>Python Programming</title>
        <author>John Doe</author>
        <year>2022</year>
    </book>
    <book id="2">
        <title>Web Development</title>
        <author>Jane Smith</author>
        <year>2023</year>
    </book>
</library>
'''

# Парсинг строки
root = ET.fromstring(xml_string)

# Или парсинг из файла
# tree = ET.parse('library.xml')
# root = tree.getroot()

print(f"Корневой элемент: {root.tag}")

# Поиск элементов
for book in root.findall('book'):
    book_id = book.get('id')
    title = book.find('title').text
    author = book.find('author').text
    year = book.find('year').text
    
    print(f"Книга {book_id}: {title} ({author}), {year}")
```

### Манипуляции с XML:

```python
import xml.etree.ElementTree as ET

xml_string = '''
<library>
    <book id="1">
        <title>Python Programming</title>
        <author>John Doe</author>
    </book>
</library>
'''

root = ET.fromstring(xml_string)

# Добавление нового элемента
new_book = ET.SubElement(root, 'book', id='3')
new_title = ET.SubElement(new_book, 'title')
new_title.text = 'Advanced Python'
new_author = ET.SubElement(new_book, 'author')
new_author.text = 'Alice Johnson'

# Изменение существующего элемента
first_book = root.find('book')
first_book.set('category', 'beginner')

# Удаление элемента
# root.remove(some_element)

# Поиск элементов по условию
python_books = root.findall(".//title[.='Python Programming']")
for title in python_books:
    print(f"Найдена книга: {title.text}")

# Вывод результата
ET.indent(root, space="  ", level=0)
print(ET.tostring(root, encoding="unicode"))
```

### XPath-подобные выражения:

```python
import xml.etree.ElementTree as ET

xml_string = '''
<library>
    <book id="1" category="programming">
        <title>Python Programming</title>
        <author>John Doe</author>
        <price currency="USD">29.99</price>
    </book>
    <book id="2" category="web">
        <title>Web Development</title>
        <author>Jane Smith</author>
        <price currency="USD">34.99</price>
    </book>
    <book id="3" category="programming">
        <title>Advanced Python</title>
        <author>Alice Johnson</author>
        <price currency="USD">39.99</price>
    </book>
</library>
'''

root = ET.fromstring(xml_string)

# Найти все книги
all_books = root.findall('.//book')
print(f"Всего книг: {len(all_books)}")

# Найти книги по категории
programming_books = root.findall(".//book[@category='programming']")
print(f"Книг по программированию: {len(programming_books)}")

# Найти все названия книг
titles = root.findall('.//title')
for title in titles:
    print(f"Название: {title.text}")

# Найти книги с ценой выше 30
expensive_books = root.findall(".//book[price/text() > '30']")
# Примечание: для числовых сравнений нужно использовать Python код
for book in root.findall('.//book'):
    price = float(book.find('price').text)
    if price > 30:
        print(f"Дорогая книга: {book.find('title').text}, ${price}")
```

---

## 5. Библиотека lxml (внешняя)

lxml - мощная библиотека для работы с XML и HTML. Требует установки: `pip install lxml`

```python
# from lxml import etree, html

# Пример работы с lxml (требует установки)
try:
    from lxml import etree
    
    # Создание XML
    root = etree.Element("root")
    child = etree.SubElement(root, "child")
    child.text = "Пример текста"
    
    # Преобразование в строку с pretty printing
    print(etree.tostring(root, pretty_print=True, encoding='unicode'))
    
    # XPath запросы (одна из сильных сторон lxml)
    # result = root.xpath('//child/text()')
    # print(result)
except ImportError:
    print("lxml не установлен. Установите с помощью: pip install lxml")
```

### Преимущества lxml:

1. Поддержка XPath 1.0 и XSLT 1.0
2. Более быстрый парсинг
3. Поддержка валидации схем
4. Лучшая поддержка пространств имен
5. Возможность обработки больших XML-файлов

---

## 6. Практические примеры

### Пример 1: Чтение и запись JSON-конфигурации

```python
import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.default_config = {
            'host': 'localhost',
            'port': 8000,
            'debug': False,
            'database_url': 'sqlite:///app.db'
        }
    
    def load_config(self):
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Создаем файл с конфигурацией по умолчанию
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config):
        """Сохранение конфигурации в файл"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def update_config(self, key, value):
        """Обновление отдельного параметра конфигурации"""
        config = self.load_config()
        config[key] = value
        self.save_config(config)

# Использование
config_manager = ConfigManager()
config = config_manager.load_config()
print(f"Конфигурация: {config}")

config_manager.update_config('port', 9000)
updated_config = config_manager.load_config()
print(f"Обновленный порт: {updated_config['port']}")
```

### Пример 2: Обработка XML-файла с книгами

```python
import xml.etree.ElementTree as ET

def parse_library_xml(xml_content=None, xml_file=None):
    """Парсинг XML-файла библиотеки"""
    if xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    else:
        root = ET.fromstring(xml_content)
    
    books = []
    for book in root.findall('.//book'):
        book_data = {
            'id': book.get('id'),
            'title': book.find('title').text if book.find('title') is not None else '',
            'author': book.find('author').text if book.find('author') is not None else '',
            'year': int(book.find('year').text) if book.find('year') is not None else None,
            'price': float(book.find('price').text) if book.find('price') is not None else None,
            'category': book.get('category', 'unknown')
        }
        books.append(book_data)
    
    return books

def filter_books_by_category(books, category):
    """Фильтрация книг по категории"""
    return [book for book in books if book['category'] == category]

def find_books_by_author(books, author):
    """Поиск книг по автору"""
    return [book for book in books if author.lower() in book['author'].lower()]

# Пример использования
xml_data = '''
<library>
    <book id="1" category="programming">
        <title>Python Programming</title>
        <author>John Doe</author>
        <year>2022</year>
        <price>29.99</price>
    </book>
    <book id="2" category="web">
        <title>Web Development</title>
        <author>Jane Smith</author>
        <year>2023</year>
        <price>34.99</price>
    </book>
</library>
'''

books = parse_library_xml(xml_content=xml_data)
programming_books = filter_books_by_category(books, 'programming')
print(f"Книги по программированию: {len(programming_books)}")

john_books = find_books_by_author(books, 'John')
print(f"Книги John: {john_books}")
```

### Пример 3: Конвертация JSON в XML и обратно

```python
import json
import xml.etree.ElementTree as ET

def json_to_xml(json_obj, root_name='root'):
    """Конвертация JSON-объекта в XML"""
    def build_xml(element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                sub_element = ET.SubElement(element, key)
                build_xml(sub_element, value)
        elif isinstance(data, list):
            for item in data:
                sub_element = ET.SubElement(element, 'item')
                build_xml(sub_element, item)
        else:
            element.text = str(data)
    
    root = ET.Element(root_name)
    build_xml(root, json_obj)
    return root

def xml_to_json(element):
    """Конвертация XML в JSON"""
    def build_json(elem):
        # Проверяем, есть ли дочерние элементы
        children = list(elem)
        attributes = elem.attrib
        
        if not children and not attributes:
            # Это листовой элемент
            return elem.text
        
        result = {}
        
        # Добавляем атрибуты
        for attr_name, attr_value in attributes.items():
            result[f"@{attr_name}"] = attr_value
        
        # Обрабатываем дочерние элементы
        child_groups = {}
        for child in children:
            child_data = build_json(child)
            if child.tag in child_groups:
                if not isinstance(child_groups[child.tag], list):
                    child_groups[child.tag] = [child_groups[child.tag]]
                child_groups[child.tag].append(child_data)
            else:
                child_groups[child.tag] = child_data
        
        result.update(child_groups)
        
        # Если элемент не имеет текста и атрибутов, кроме дочерних элементов
        if elem.text and elem.text.strip():
            if result:
                result["#text"] = elem.text.strip()
            else:
                return elem.text.strip()
        
        return result
    
    return build_json(element)

# Пример использования
json_data = {
    "name": "Иван Иванов",
    "age": 30,
    "skills": ["Python", "JavaScript", "SQL"],
    "address": {
        "city": "Москва",
        "street": "Ленина 10"
    }
}

# Конвертация JSON в XML
xml_root = json_to_xml(json_data, 'person')
ET.indent(xml_root, space="  ", level=0)
xml_string = ET.tostring(xml_root, encoding="unicode")
print("JSON -> XML:")
print(xml_string)

# Конвертация XML обратно в JSON
xml_root = ET.fromstring(xml_string)
json_result = xml_to_json(xml_root)['person']
print("\nXML -> JSON:")
print(json.dumps(json_result, ensure_ascii=False, indent=2))
```

---

## Заключение

JSON и XML - два основных формата для обмена данными в приложениях. JSON проще в использовании и легче по весу, тогда как XML более гибкий и позволяет определять сложные структуры данных. В Python есть встроенные средства для работы с обоими форматами, а также мощные сторонние библиотеки для сложных случаев.

## Контрольные вопросы:
1. В чем разница между JSON и XML?
2. Какие методы предоставляет модуль json в Python?
3. Что такое ElementTree и для чего он используется?
4. Как парсить XML-документ с помощью ElementTree?
5. Какие преимущества имеет библиотека lxml над ElementTree?
