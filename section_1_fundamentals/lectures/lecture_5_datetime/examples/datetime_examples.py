# Примеры работы с датой и временем в Python

"""
Этот файл содержит примеры использования модуля datetime и других инструментов 
для работы с датой и временем в Python.
"""

from datetime import datetime, date, time, timedelta, timezone
import time as time_module
import calendar
from typing import Union, List

# 1. Основы работы с datetime
def basic_datetime_examples():
    """
    Примеры базовой работы с датой и временем
    """
    print("=== Основы datetime ===")
    
    # Текущая дата и время
    now = datetime.now()
    print(f"Текущее время: {now}")
    
    # Текущая дата
    today = date.today()
    print(f"Текущая дата: {today}")
    
    # Текущее время
    current_time = time.now()
    print(f"Текущее время: {current_time}")
    
    # Создание конкретной даты
    specific_date = date(2023, 12, 25)
    print(f"Конкретная дата: {specific_date}")
    
    # Создание конкретного времени
    specific_time = time(14, 30, 45)
    print(f"Конкретное время: {specific_time}")
    
    # Создание datetime
    specific_datetime = datetime(2023, 12, 25, 14, 30, 45)
    print(f"Конкретная дата и время: {specific_datetime}")
    
    # Компоненты даты и времени
    print(f"Год: {now.year}, Месяц: {now.month}, День: {now.day}")
    print(f"Час: {now.hour}, Минута: {now.minute}, Секунда: {now.second}")
    
    # День недели
    print(f"День недели (0-6): {now.weekday()}")  # 0 - понедельник
    print(f"День недели (1-7): {now.isoweekday()}")  # 1 - понедельник
    print(f"Название дня недели: {now.strftime('%A')}")
    
    # Неделя года
    print(f"Неделя года: {now.isocalendar()[1]}")
    print()

basic_datetime_operations()

# 2. Работа с форматированием дат
def formatting_examples():
    """
    Примеры форматирования дат и времени
    """
    print("=== Форматирование дат ===")
    
    dt = datetime.now()
    
    # Форматирование с использованием strftime
    formats = {
        "Год-месяц-день": "%Y-%m-%d",
        "День.месяц.год": "%d.%m.%Y",
        "Месяц/день/год": "%m/%d/%Y",
        "Полная дата": "%A, %B %d, %Y",
        "Время 24-часовой формат": "%H:%M:%S",
        "Время 12-часовой формат": "%I:%M:%S %p",
        "Дата и время": "%Y-%m-%d %H:%M:%S",
        "ISO формат": "%Y-%m-%dT%H:%M:%S",
        "Человекочитаемый формат": "%B %d, %Y at %I:%M %p"
    }
    
    for description, fmt in formats.items():
        formatted = dt.strftime(fmt)
        print(f"{description}: {formatted}")
    
    # Парсинг строки в datetime
    date_string = "2023-12-25 14:30:45"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print(f"\nРазбор строки '{date_string}': {parsed_date}")
    
    # Примеры разных форматов для парсинга
    date_formats = [
        ("25/12/2023", "%d/%m/%Y"),
        ("December 25, 2023", "%B %d, %Y"),
        ("25-Dec-2023", "%d-%b-%Y"),
        ("2023-W51-1", "%Y-W%U-%w")  # ISO неделя (упрощенный пример)
    ]
    
    for date_str, fmt in date_formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            print(f"Разбор '{date_str}' с форматом '{fmt}': {parsed.date()}")
        except ValueError as e:
            print(f"Ошибка разбора '{date_str}' с форматом '{fmt}': {e}")
    
    print()

date_formatting_examples()

# 3. Работа с timedelta
def timedelta_examples():
    """
    Примеры работы с разницей во времени (timedelta)
    """
    print("=== Timedelta (разница во времени) ===")
    
    # Создание timedelta
    td1 = timedelta(days=7, hours=3, minutes=30, seconds=15)
    td2 = timedelta(weeks=2, days=1, hours=5)
    
    print(f"Timedelta 1: {td1}")
    print(f"Timedelta 2: {td2}")
    
    # Операции с timedelta
    now = datetime.now()
    future = now + td1
    past = now - td2
    
    print(f"Сейчас: {now}")
    print(f"Через td1: {future}")
    print(f"td2 назад: {past}")
    
    # Разница между двумя датами
    diff = future - past
    print(f"Разница между будущим и прошлым: {diff}")
    print(f"Разница в днях: {diff.days}")
    print(f"Разница в секундах: {diff.total_seconds()}")
    
    # Операции с timedelta
    doubled_td = td1 * 2
    halved_td = td2 / 2
    print(f"Удвоенный td1: {doubled_td}")
    print(f"Половина td2: {halved_td}")
    
    # Сравнение timedelta
    print(f"td1 > td2: {td1 > td2}")
    print(f"td1 == td2: {td1 == td2}")
    
    print()

timedelta_operations()

# 4. Работа с часовыми поясами
def timezone_examples():
    """
    Примеры работы с часовыми поясами
    """
    print("=== Часовые пояса ===")
    
    # Создание даты с временной зоной
    utc_now = datetime.now(timezone.utc)
    print(f"Время в UTC: {utc_now}")
    
    # Создание конкретной временной зоны
    eastern = timezone(timedelta(hours=-5), name="EST")
    pacific = timezone(timedelta(hours=-8), name="PST")
    
    # Создание datetime с временной зоной
    est_time = datetime.now(eastern)
    pst_time = datetime.now(pacific)
    
    print(f"Время в EST: {est_time}")
    print(f"Время в PST: {pst_time}")
    
    # Преобразование между часовыми поясами
    utc_time = datetime.now(timezone.utc)
    
    # Создание временной зоны с помощью pytz (требует установки: pip install pytz)
    try:
        import pytz
        
        # Создание временных зон
        moscow_tz = pytz.timezone('Europe/Moscow')
        london_tz = pytz.timezone('Europe/London')
        
        # Локализация времени
        naive_dt = datetime(2023, 12, 25, 15, 30, 0)
        localized_dt = moscow_tz.localize(naive_dt)
        print(f"Локализованное время в Москве: {localized_dt}")
        
        # Преобразование в другую временную зону
        london_time = localized_dt.astimezone(london_tz)
        print(f"Время в Лондоне: {london_time}")
        
        # Список всех временных зон
        print(f"Пример временных зон: {len(pytz.all_timezones)} всего, первые 10: {pytz.all_timezones[:10]}")
        
    except ImportError:
        print("pytz не установлен. Установите с помощью: pip install pytz")
        print("Для полноценной работы с часовыми поясами рекомендуется использовать pytz или zoneinfo (Python 3.9+)")
    
    # Использование zoneinfo (доступно с Python 3.9+)
    try:
        from zoneinfo import ZoneInfo
        
        # Создание datetime с временной зоной
        tokyo_time = datetime.now(ZoneInfo("Asia/Tokyo"))
        print(f"Время в Токио: {tokyo_time}")
        
        # Преобразование временных зон
        tokyo_dt = datetime(2023, 12, 25, 15, 30, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
        moscow_dt = tokyo_dt.astimezone(ZoneInfo("Europe/Moscow"))
        print(f"Время в Токио: {tokyo_dt}")
        print(f"То же время в Москве: {moscow_dt}")
        
    except ImportError:
        print("zoneinfo не доступен (Python < 3.9), используйте pytz для работы с часовыми поясами")
    
    print()

timezone_examples()

# 5. Работа с модулем time
def time_module_examples():
    """
    Примеры работы с модулем time
    """
    print("=== Модуль time ===")
    
    # Текущее время в секундах с эпохи Unix (1 января 1970)
    timestamp = time_module.time()
    print(f"Текущий timestamp: {timestamp}")
    
    # Преобразование timestamp в локальное время
    local_time = time_module.localtime(timestamp)
    print(f"Локальное время: {local_time}")
    
    # Преобразование timestamp в UTC
    utc_time = time_module.gmtime(timestamp)
    print(f"Время в UTC: {utc_time}")
    
    # Форматирование времени с помощью time.strftime
    formatted_time = time_module.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print(f"Форматированное время: {formatted_time}")
    
    # Парсинг строки в struct_time
    parsed_time = time_module.strptime("2023-12-25 15:30:00", "%Y-%m-%d %H:%M:%S")
    print(f"Разобранное время: {parsed_time}")
    
    # Измерение времени выполнения
    start_time = time_module.perf_counter()
    # Симуляция работы
    time_module.sleep(0.1)
    end_time = time_module.perf_counter()
    print(f"Время выполнения: {end_time - start_time:.4f} секунд")
    
    # Измерение CPU времени
    cpu_start = time_module.process_time()
    # Симуляция вычислений
    sum(range(100000))
    cpu_end = time_module.process_time()
    print(f"CPU время: {cpu_end - cpu_start:.4f} секунд")
    
    print()

time_module_operations()

# 6. Календарь
def calendar_examples():
    """
    Примеры работы с календарем
    """
    print("=== Модуль calendar ===")
    
    # Печать календаря на месяц
    cal_month = calendar.month(2023, 12)
    print("Календарь декабря 2023:")
    print(cal_month)
    
    # Печать календаря на год
    print("\nКалендарь на 2023 год (первые 2 месяца):")
    print(calendar.month(2023, 1))
    print(calendar.month(2023, 2))
    
    # Определение високосного года
    print(f"2023 - високосный год: {calendar.isleap(2023)}")
    print(f"2024 - високосный год: {calendar.isleap(2024)}")
    
    # Количество дней в месяце
    print(f"Дней в феврале 2023: {calendar.monthrange(2023, 2)[1]}")
    print(f"Дней в феврале 2024: {calendar.monthrange(2024, 2)[1]}")
    
    # День недели для конкретной даты (0-6, понедельник-воскресенье)
    weekday = calendar.weekday(2023, 12, 25)
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    print(f"25 декабря 2023 - {weekdays[weekday]}")
    
    # Месяц как матрица (недели по 7 дней)
    month_matrix = calendar.monthcalendar(2023, 12)
    print(f"\nДекабрь 2023 как матрица:")
    for week in month_matrix:
        print(week)
    
    print()

calendar_operations()

# 7. Практические примеры использования
def practical_datetime_examples():
    """
    Практические примеры использования даты и времени
    """
    print("=== Практические примеры ===")
    
    # Пример 1: Календарь событий
    def create_event_calendar(events):
        """
        Создание календаря событий
        """
        calendar_dict = {}
        for event in events:
            event_date = event["date"].date()  # Преобразуем datetime в date
            if event_date not in calendar_dict:
                calendar_dict[event_date] = []
            calendar_dict[event_date].append(event["name"])
        return calendar_dict
    
    events = [
        {"name": "Встреча с командой", "date": datetime(2023, 12, 20, 10, 0)},
        {"name": "Дедлайн проекта", "date": datetime(2023, 12, 22, 17, 0)},
        {"name": "День рождения", "date": datetime(2023, 12, 25, 12, 0)},
        {"name": "Отпуск", "date": datetime(2024, 1, 1, 0, 0)}
    ]
    
    event_calendar = create_event_calendar(events)
    print("Календарь событий:")
    for date, event_list in sorted(event_calendar.items()):
        print(f"  {date}: {', '.join(event_list)}")
    
    # Пример 2: Вычисление возраста
    def calculate_age(birth_date):
        """
        Вычисление возраста по дате рождения
        """
        today = date.today()
        age = today.year - birth_date.year
        
        # Проверяем, был ли уже день рождения в этом году
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        return age
    
    birth_date = date(1990, 5, 15)
    age = calculate_age(birth_date)
    print(f"\nВозраст для даты рождения {birth_date}: {age} лет")
    
    # Пример 3: Работа с интервалами
    def generate_date_range(start_date, end_date, interval_days=1):
        """
        Генерация диапазона дат
        """
        current_date = start_date
        dates = []
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=interval_days)
        return dates
    
    start = date(2023, 12, 20)
    end = date(2023, 12, 30)
    date_range = generate_date_range(start, end, 2)
    print(f"\nДиапазон дат с интервалом 2 дня: {date_range}")
    
    # Пример 4: Сравнение дат
    def is_date_in_range(check_date, start_date, end_date):
        """
        Проверка, находится ли дата в диапазоне
        """
        return start_date <= check_date <= end_date
    
    check_date = date(2023, 12, 25)
    in_range = is_date_in_range(check_date, start, end)
    print(f"\nДата {check_date} в диапазоне {start}-{end}: {in_range}")
    
    # Пример 5: Форматирование дат для пользователей
    def format_date_for_user(dt, locale="ru"):
        """
        Форматирование даты для пользователя в зависимости от локали
        """
        if locale == "ru":
            return dt.strftime("%d.%m.%Y в %H:%M")
        elif locale == "en":
            return dt.strftime("%B %d, %Y at %I:%M %p")
        elif locale == "iso":
            return dt.isoformat()
        else:
            return str(dt)
    
    sample_dt = datetime(2023, 12, 25, 15, 30, 45)
    print(f"\nФорматирование даты {sample_dt} для разных локалей:")
    print(f"  Русский: {format_date_for_user(sample_dt, 'ru')}")
    print(f"  Английский: {format_date_for_user(sample_dt, 'en')}")
    print(f"  ISO: {format_date_for_user(sample_dt, 'iso')}")
    
    print()

practical_datetime_operations()

# 8. Примеры для работы с файлами и датами
def file_datetime_examples():
    """
    Примеры использования дат для работы с файлами
    """
    print("=== Даты и работа с файлами ===")
    
    import os
    from datetime import datetime
    
    # Создание временного файла для демонстрации
    temp_filename = "temp_datetime_demo.txt"
    with open(temp_filename, "w") as f:
        f.write("Файл для демонстрации работы с датами")
    
    # Получение даты создания/изменения файла
    file_stats = os.stat(temp_filename)
    created = datetime.fromtimestamp(file_stats.st_ctime)
    modified = datetime.fromtimestamp(file_stats.st_mtime)
    
    print(f"Файл: {temp_filename}")
    print(f"Дата создания: {created}")
    print(f"Дата модификации: {modified}")
    
    # Создание имени файла с временной меткой
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"backup_{timestamp}.txt"
    print(f"Имя файла с временной меткой: {filename_with_timestamp}")
    
    # Функция для очистки старых файлов
    def cleanup_old_files(directory, days_old=7):
        """
        Удаление файлов старше указанного количества дней
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        old_files = []
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_modified < cutoff_date:
                    old_files.append(filename)
        
        return old_files
    
    # Пример использования (без реального удаления файлов)
    print(f"Файлы старше 7 дней в текущей директории: {cleanup_old_files('.', 7)}")
    
    # Удаление временного файла
    os.remove(temp_filename)
    print()

file_datetime_examples()

# 9. Примеры планировщика задач
def scheduler_examples():
    """
    Примеры планировщика задач с использованием дат и времени
    """
    print("=== Планировщик задач ===")
    
    class TaskScheduler:
        def __init__(self):
            self.tasks = []
        
        def add_task(self, name, execution_time, recurring=False, interval=None):
            """
            Добавление задачи в планировщик
            """
            task = {
                "name": name,
                "execution_time": execution_time,
                "recurring": recurring,
                "interval": interval,
                "last_run": None
            }
            self.tasks.append(task)
            print(f"Добавлена задача: {name}")
        
        def get_due_tasks(self):
            """
            Получение задач, которые должны быть выполнены сейчас
            """
            now = datetime.now()
            due_tasks = []
            
            for task in self.tasks:
                if task["last_run"] is None and task["execution_time"] <= now:
                    due_tasks.append(task)
                elif task["recurring"] and task["interval"]:
                    if task["last_run"] is None:
                        if task["execution_time"] <= now:
                            due_tasks.append(task)
                    else:
                        next_run = task["last_run"] + task["interval"]
                        if next_run <= now:
                            due_tasks.append(task)
            
            return due_tasks
        
        def run_due_tasks(self):
            """
            Выполнение задач, которые должны быть выполнены
            """
            due_tasks = self.get_due_tasks()
            for task in due_tasks:
                print(f"Выполняется задача: {task['name']}")
                # Здесь обычно происходит выполнение задачи
                task["last_run"] = datetime.now()
    
    # Демонстрация планировщика
    scheduler = TaskScheduler()
    
    # Добавление задач
    scheduler.add_task("Отправить отчет", datetime.now() + timedelta(seconds=5))
    scheduler.add_task("Резервное копирование", datetime.now() + timedelta(seconds=10), 
                      recurring=True, interval=timedelta(minutes=1))
    
    print(f"Всего задач: {len(scheduler.tasks)}")
    print("Задачи:")
    for task in scheduler.tasks:
        print(f"  - {task['name']}: {task['execution_time']}, повторяющаяся: {task['recurring']}")
    
    print()

scheduler_examples()

# 10. Заключение: советы по работе с датой и временем
def datetime_best_practices():
    """
    Рекомендации по работе с датой и временем
    """
    print("=== Рекомендации по работе с датой и временем ===")
    
    recommendations = [
        "1. Используйте datetime.now(timezone.utc) для получения текущего времени в UTC",
        "2. При работе с временнýми зонами используйте pytz или zoneinfo",
        "3. Для хранения времени в базах данных используйте UTC",
        "4. Используйте timedelta для операций с интервалами времени",
        "5. Для парсинга строк используйте datetime.strptime с явным форматом",
        "6. При форматировании для пользователей учитывайте локаль",
        "7. Для измерения производительности используйте time.perf_counter()",
        "8. Для измерения CPU времени используйте time.process_time()"
    ]
    
    for rec in recommendations:
        print(rec)
    
    print()

datetime_best_practices()
