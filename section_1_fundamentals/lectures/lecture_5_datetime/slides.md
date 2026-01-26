# Лекция 5: Работа с датой и временем

## Модуль datetime, форматирование, временные зоны, модуль time

### План лекции:
1. Введение в работу с датой и временем
2. Модуль datetime
3. Классы datetime, date, time, timedelta
4. Форматирование даты и времени
5. Работа с часовыми поясами
6. Модуль time
7. Практические примеры

---

## 1. Введение в работу с датой и временем

В Python есть несколько модулей для работы с датой и временем:
- `datetime` - основной модуль для работы с датами и временем
- `time` - низкоуровневый модуль для работы с метками времени Unix
- `calendar` - для работы с календарями

---

## 2. Модуль datetime

Модуль `datetime` предоставляет классы для работы с датой и временем. Основные классы:

```python
from datetime import datetime, date, time, timedelta
import datetime as dt  # Также можно импортировать весь модуль
```

### Основные классы:
- `date` - для работы только с датами (год, месяц, день)
- `time` - для работы только со временем (часы, минуты, секунды, микросекунды)
- `datetime` - для работы с датой и временем
- `timedelta` - для работы с интервалами времени
- `tzinfo` - для работы с часовыми поясами
- `timezone` - подкласс tzinfo для работы с часовыми поясами

---

## 3. Классы datetime, date, time, timedelta

### Класс date

```python
from datetime import date

# Создание объекта date
today = date.today()
print(today)  # 2023-10-15 (текущая дата)

specific_date = date(2023, 10, 15)
print(specific_date)  # 2023-10-15

# Создание даты из порядкового номера дня
ordinal_date = date.fromordinal(738808)  # 738808-й день от 1 января 1 года
print(ordinal_date)  # 2023-10-15

# Создание даты из ISO формата
iso_date = date.fromisoformat('2023-10-15')
print(iso_date) # 2023-10-15

# Атрибуты даты
print(today.year)    # год
print(today.month)   # месяц
print(today.day)     # день
```

### Класс time

```python
from datetime import time

# Создание объекта time
current_time = time(14, 30, 45, 123456)
print(current_time)  # 14:30:45.123456

# Пустое время (00:00:00)
empty_time = time()
print(empty_time)  # 00:00:00

# Атрибуты времени
print(current_time.hour)         # часы
print(current_time.minute)       # минуты
print(current_time.second)       # секунды
print(current_time.microsecond)  # микросекунды
```

### Класс datetime

```python
from datetime import datetime

# Создание объекта datetime
now = datetime.now()
print(now)  # 2023-10-15 14:30:45.123456

# Создание конкретной даты и времени
specific_datetime = datetime(2023, 10, 15, 14, 30, 45)
print(specific_datetime)  # 2023-10-15 14:30:45

# Создание datetime из строки
dt_from_string = datetime.strptime('2023-10-15 14:30:45', '%Y-%m-%d %H:%M:%S')
print(dt_from_string)  # 2023-10-15 14:30:45

# Атрибуты datetime
print(now.year)        # год
print(now.month)       # месяц
print(now.day)         # день
print(now.hour)        # час
print(now.minute)      # минута
print(now.second)      # секунда
print(now.microsecond) # микросекунда
```

### Класс timedelta

```python
from datetime import datetime, timedelta

# Создание timedelta
one_day = timedelta(days=1)
one_hour = timedelta(hours=1)
one_week = timedelta(weeks=1)

# Арифметика с датами
today = datetime.now()
tomorrow = today + one_day
yesterday = today - one_day

print(f"Сегодня: {today}")
print(f"Завтра: {tomorrow}")
print(f"Вчера: {yesterday}")

# Разница между двумя датами
future_date = datetime(2024, 1, 1)
difference = future_date - today
print(f"Дней до Нового года: {difference.days}")

# Работа с timedelta
week_later = today + timedelta(weeks=1, days=2, hours=3)
print(f"Через неделю и 2 дня: {week_later}")
```

---

## 4. Форматирование даты и времени

### Метод strftime()

```python
from datetime import datetime

now = datetime.now()

# Форматирование даты и времени
formatted = now.strftime('%Y-%m-%d %H:%M:%S')
print(formatted)  # 2023-10-15 14:30:45

# Различные форматы
print(now.strftime('%A, %B %d, %Y'))  # Воскресенье, Октябрь 15, 2023
print(now.strftime('%d/%m/%Y'))       # 15/10/2023
print(now.strftime('%H:%M:%S'))       # 14:30:45
print(now.strftime('%c'))             # Воскресенье 15 октября 2023 г., 14:30:45
print(now.strftime('%x'))             # 15.10.2023
print(now.strftime('%X'))             # 14:30:45
```

### Метод strptime()

```python
from datetime import datetime

# Парсинг строки в datetime
date_string = "2023-10-15 14:30:45"
parsed_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
print(parsed_date)  # 2023-10-15 14:30:45

# Различные форматы для парсинга
date_str1 = "15/10/2023"
parsed1 = datetime.strptime(date_str1, '%d/%m/%Y')

date_str2 = "October 15, 2023"
parsed2 = datetime.strptime(date_str2, '%B %d, %Y')

time_str = "2:30:45 PM"
parsed_time = datetime.strptime(time_str, '%I:%M:%S %p')
```

### Спецификаторы формата

| Спецификатор | Описание | Пример |
|--------------|----------|---------|
| `%Y` | Год с веком как десятичное число | 2023 |
| `%y` | Год без века как десятичное число [00,99] | 23 |
| `%m` | Месяц как десятичное число [01,12] | 10 |
| `%B` | Полное название месяца | October |
| `%b` | Сокращенное название месяца | Oct |
| `%d` | День месяца как десятичное число [01,31] | 15 |
| `%A` | Полное название дня недели | Sunday |
| `%a` | Сокращенное название дня недели | Sun |
| `%H` | Время в 24-часовом формате | 14 |
| `%I` | Время в 12-часовом формате | 02 |
| `%M` | Минуты как десятичное число [00,59] | 30 |
| `%S` | Секунды как десятичное число [00,61] | 45 |
| `%p` | AM или PM | PM |

---

## 5. Работа с часовыми поясами

### Класс timezone

```python
from datetime import datetime, timezone, timedelta

# UTC время
utc_now = datetime.now(timezone.utc)
print(utc_now)  # 2023-10-15 08:30:45.123456+00:00

# Создание часового пояса с UTC+3 (Москва)
moscow_tz = timezone(timedelta(hours=3))
moscow_time = datetime.now(moscow_tz)
print(moscow_time)  # 2023-10-15 11:30:45.123456+03:00

# Часовой пояс UTC
utc_tz = timezone.utc
print(utc_tz)  # UTC

# Преобразование между часовыми поясами
utc_time = datetime(2023, 10, 15, 8, 30, 45, tzinfo=timezone.utc)
moscow_time = utc_time.astimezone(moscow_tz)
print(f"UTC: {utc_time}")
print(f"Москва: {moscow_time}")
```

### Работа с pytz (внешняя библиотека)

```python
# pip install pytz
import pytz
from datetime import datetime

# Создание даты в определенном часовом поясе
eastern = pytz.timezone('US/Eastern')
utc = pytz.UTC

# Локализация даты в часовом поясе
local_dt = eastern.localize(datetime(2023, 10, 15, 12, 0, 0))
print(local_dt)  # 2023-10-15 12:00:00-04:00

# Преобразование в UTC
utc_dt = local_dt.astimezone(utc)
print(utc_dt)  # 2023-10-15 16:00:00+00:00

# Преобразование в другой часовой пояс
tokyo_tz = pytz.timezone('Asia/Tokyo')
tokyo_time = utc_dt.astimezone(tokyo_tz)
print(tokyo_time)  # 2023-10-16 01:00:00+09:00
```

---

## 6. Модуль time

Модуль `time` предоставляет функции для работы с метками времени Unix (секунды с 1 января 1970 года).

```python
import time

# Текущее время в секундах с начала эпохи
current_timestamp = time.time()
print(current_timestamp)  # 1702654245.123456

# Приостановка выполнения программы
print("Ожидание...")
time.sleep(2)  # Пауза на 2 секунды
print("Продолжение")

# Преобразование timestamp в struct_time
local_time = time.localtime(current_timestamp)
print(local_time)  # time.struct_time(tm_year=2023, tm_mon=10, ...)

# Преобразование timestamp в читаемую строку
readable_time = time.ctime(current_timestamp)
print(readable_time)  # Sun Oct 15 14:30:45 2023

# Форматирование времени
formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
print(formatted_time)  # 2023-10-15 14:30:45

# Парсинг строки во время
parsed_time = time.strptime('2023-10-15 14:30:45', '%Y-%m-%d %H:%M:%S')
print(parsed_time)  # time.struct_time(tm_year=2023, ...)
```

---

## 7. Практические примеры

### Пример 1: Калькулятор возраста

```python
from datetime import date

def calculate_age(birth_date):
    """Вычисляет возраст по дате рождения"""
    today = date.today()
    age = today.year - birth_date.year
    
    # Проверяем, был ли уже день рождения в этом году
    if today.month < birth_date.month or \
       (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age

birth = date(1990, 5, 15)
age = calculate_age(birth)
print(f"Возраст: {age} лет")
```

### Пример 2: Работа с расписанием

```python
from datetime import datetime, timedelta

def next_weekday(d, weekday):
    """Возвращает следующий указанный день недели"""
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Целевой день уже прошел в этой неделе
        days_ahead += 7
    return d + timedelta(days_ahead)

# Найти следующий понедельник
d = datetime.now()
next_monday = next_weekday(d, 0)  # 0 - понедельник
print(f"Следующий понедельник: {next_monday.strftime('%Y-%m-%d')}")

# Работа с интервалами
def work_schedule(start_date, end_date):
    """Генерирует рабочие дни в диапазоне дат"""
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Пн-Пт
            yield current
        current += timedelta(days=1)

start = datetime(2023, 10, 1)
end = datetime(2023, 10, 15)
work_days = list(work_schedule(start, end))
print(f"Рабочие дни: {len(work_days)}")
```

### Пример 3: Таймер выполнения

```python
import time
from datetime import datetime

def measure_execution_time(func):
    """Декоратор для измерения времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнена за {execution_time:.4f} секунд")
        return result
    return wrapper

@measure_execution_time
def slow_function():
    time.sleep(1)
    return "Готово!"

result = slow_function()
```

---

## Заключение

Работа с датой и временем в Python предоставляет мощные инструменты для управления временнýми данными. Модуль `datetime` особенно полезен для большинства задач, в то время как модуль `time` предоставляет низкоуровневый доступ к системному времени.

## Контрольные вопросы:
1. В чем разница между классами date, time и datetime?
2. Как создать объект timedelta и для чего он используется?
3. Какие методы форматирования даты и времени существуют?
4. Как работать с часовыми поясами?
5. В чем разница между time.time() и datetime.now()?
