# Решения для практического занятия 5: Работа с датой и временем

from datetime import datetime, date, time, timedelta
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # для более старых версий
import calendar
import pytz  # если установлен

# Решение задания 1: Основы работы с датами
def get_current_datetime_info():
    """Получает текущую дату и время, выводит информацию о них"""
    now = datetime.now()
    
    print(f"Текущая дата и время: {now}")
    print(f"Только дата: {now.date()}")
    print(f"Только время: {now.time()}")
    print(f"Год: {now.year}")
    print(f"Месяц: {now.month}")
    print(f"День: {now.day}")
    print(f"Час: {now.hour}")
    print(f"Минута: {now.minute}")
    print(f"Секунда: {now.second}")
    
    return now

def calculate_date_difference(date1, date2):
    """Вычисляет разницу между двумя датами"""
    difference = abs(date2 - date1)
    return difference.days

# Решение задания 2: Форматирование дат
def string_to_datetime(date_string, format_string="%Y-%m-%d %H:%M:%S"):
    """Преобразует строку в объект datetime"""
    try:
        return datetime.strptime(date_string, format_string)
    except ValueError as e:
        print(f"Ошибка при преобразовании строки в datetime: {e}")
        return None

def datetime_to_string(dt_obj, format_string="%Y-%m-%d %H:%M:%S"):
    """Преобразует объект datetime в строку"""
    return dt_obj.strftime(format_string)

def format_various_ways(dt_obj):
    """Преобразует datetime в различные форматы"""
    formats = {
        "ISO": dt_obj.isoformat(),
        "DD/MM/YYYY": dt_obj.strftime("%d/%m/%Y"),
        "MM-DD-YYYY HH:MM": dt_obj.strftime("%m-%d-%Y %H:%M"),
        "Full weekday name": dt_obj.strftime("%A, %B %d, %Y"),
        "Short format": dt_obj.strftime("%d.%m.%y %H:%M")
    }
    return formats

# Решение задания 3: Работа с часовыми поясами
def convert_timezone(dt_naive, from_tz_str, to_tz_str):
    """Преобразует время из одного часового пояса в другой"""
    # Делаем наивную дату осознанной (aware)
    from_tz = ZoneInfo(from_tz_str)
    to_tz = ZoneInfo(to_tz_str)
    
    dt_aware = dt_naive.replace(tzinfo=from_tz)
    dt_converted = dt_aware.astimezone(to_tz)
    
    return dt_converted

def get_time_in_different_zones(base_dt):
    """Возвращает время в нескольких часовых поясах"""
    zones = ["Europe/Moscow", "America/New_York", "Asia/Tokyo", "UTC"]
    times_in_zones = {}
    
    for zone in zones:
        tz = ZoneInfo(zone)
        aware_dt = base_dt.replace(tzinfo=ZoneInfo("UTC")) if base_dt.tzinfo is None else base_dt
        times_in_zones[zone] = aware_dt.astimezone(tz)
    
    return times_in_zones

# Решение задания 4: Календарные вычисления
def add_days(dt, days):
    """Добавляет дни к дате"""
    return dt + timedelta(days=days)

def add_weeks(dt, weeks):
    """Добавляет недели к дате"""
    return dt + timedelta(weeks=weeks)

def add_months(dt, months):
    """Добавляет месяцы к дате (с учетом разного количества дней в месяцах)"""
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

def day_of_week(dt):
    """Определяет день недели для заданной даты"""
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[dt.weekday()]

def find_next_occurrence_of_weekday(dt, target_weekday):
    """Находит следующий день недели (0-6, где 0 - понедельник)"""
    days_ahead = target_weekday - dt.weekday()
    if days_ahead <= 0:  # Целевой день уже прошел на этой неделе
        days_ahead += 7
    return dt + timedelta(days_ahead)

def is_leap_year(year):
    """Проверяет, является ли год високосным"""
    return calendar.isleap(year)

def get_business_days(start_date, end_date):
    """Возвращает количество рабочих дней между двумя датами (без праздников)"""
    business_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Пн-Пт (0-4)
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days

# Решение задания 5: Календарь встреч
class MeetingScheduler:
    """Класс для планирования встреч"""
    def __init__(self):
        self.meetings = []
    
    def add_meeting(self, title, start_time, end_time):
        """Добавляет встречу, проверяя пересечения"""
        new_meeting = {
            'title': title,
            'start': start_time,
            'end': end_time
        }
        
        # Проверяем пересечения
        for meeting in self.meetings:
            if self._check_overlap(new_meeting, meeting):
                print(f"Внимание: Новая встреча '{title}' пересекается с '{meeting['title']}'")
                return False
        
        self.meetings.append(new_meeting)
        print(f"Встреча '{title}' успешно добавлена")
        return True
    
    def _check_overlap(self, meeting1, meeting2):
        """Проверяет пересечение двух встреч"""
        return meeting1['start'] < meeting2['end'] and meeting2['start'] < meeting1['end']
    
    def remove_meeting(self, title):
        """Удаляет встречу по названию"""
        for i, meeting in enumerate(self.meetings):
            if meeting['title'] == title:
                del self.meetings[i]
                print(f"Встреча '{title}' удалена")
                return True
        print(f"Встреча '{title}' не найдена")
        return False
    
    def get_upcoming_meetings(self, from_time, hours_ahead=24):
        """Возвращает предстоящие встречи в течение заданного периода"""
        end_time = from_time + timedelta(hours=hours_ahead)
        upcoming = []
        
        for meeting in self.meetings:
            if from_time < meeting['start'] < end_time:
                upcoming.append(meeting)
        
        return sorted(upcoming, key=lambda m: m['start'])
    
    def get_meetings_for_day(self, target_date):
        """Возвращает встречи для конкретного дня"""
        day_start = datetime.combine(target_date, time.min)
        day_end = datetime.combine(target_date, time.max)
        
        daily_meetings = []
        for meeting in self.meetings:
            if day_start <= meeting['start'] <= day_end or day_start <= meeting['end'] <= day_end:
                daily_meetings.append(meeting)
        
        return sorted(daily_meetings, key=lambda m: m['start'])

# Дополнительные примеры использования модуля datetime
def demonstrate_timedelta_operations():
    """Демонстрирует различные операции с timedelta"""
    today = datetime.today()
    print(f"Сегодня: {today}")
    
    # Операции с timedelta
    yesterday = today - timedelta(days=1)
    next_week = today + timedelta(weeks=1)
    hour_ago = today - timedelta(hours=1)
    next_month = add_months(today, 1)
    
    print(f"Вчера: {yesterday}")
    print(f"Следующая неделя: {next_week}")
    print(f"Час назад: {hour_ago}")
    print(f"Через месяц: {next_month}")

def demonstrate_date_range():
    """Демонстрирует создание диапазона дат"""
    start_date = date(2023, 1, 1)
    end_date = date(2023, 1, 10)
    
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    print(f"Диапазон дат с {start_date} по {end_date}: {date_range}")
    return date_range

def parse_iso_format(iso_string):
    """Разбирает ISO формат даты"""
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 5 ===")
    
    print("\n1. Решение задания 1: Основы работы с датами")
    current_dt = get_current_datetime_info()
    
    date1 = datetime(2023, 5, 15)
    date2 = datetime(2023, 6, 20)
    diff = calculate_date_difference(date1, date2)
    print(f"Разница между {date1.date()} и {date2.date()}: {diff} дней")
    
    print("\n2. Решение задания 2: Форматирование дат")
    date_str = "2023-10-15 14:30:00"
    dt_from_str = string_to_datetime(date_str)
    print(f"Дата из строки: {dt_from_str}")
    
    str_from_dt = datetime_to_string(current_dt)
    print(f"Строка из даты: {str_from_dt}")
    
    various_formats = format_various_ways(current_dt)
    print("Различные форматы:")
    for fmt_name, fmt_value in various_formats.items():
        print(f"  {fmt_name}: {fmt_value}")
    
    print("\n3. Решение задания 3: Работа с часовыми поясами")
    naive_dt = datetime(2023, 6, 15, 12, 0, 0)
    converted_dt = convert_timezone(naive_dt, "UTC", "Europe/Moscow")
    print(f"Время в Москве: {converted_dt}")
    
    times_in_zones = get_time_in_different_zones(current_dt)
    print("Время в разных часовых поясах:")
    for zone, time_in_zone in times_in_zones.items():
        print(f"  {zone}: {time_in_zone}")
    
    print("\n4. Решение задания 4: Календарные вычисления")
    future_date = add_days(current_dt, 30)
    print(f"Дата через 30 дней: {future_date.date()}")
    
    future_week = add_weeks(current_dt, 2)
    print(f"Дата через 2 недели: {future_week.date()}")
    
    future_month = add_months(current_dt, 3)
    print(f"Дата через 3 месяца: {future_month.date()}")
    
    weekday = day_of_week(current_dt)
    print(f"День недели для {current_dt.date()}: {weekday}")
    
    next_friday = find_next_occurrence_of_weekday(current_dt, 4)  # 4 - пятница
    print(f"Следующая пятница: {next_friday.date()}")
    
    year = 2024
    leap = is_leap_year(year)
    print(f"Год {year} {'високосный' if leap else 'не високосный'}")
    
    business_days = get_business_days(date1.date(), date2.date())
    print(f"Рабочих дней между {date1.date()} и {date2.date()}: {business_days}")
    
    print("\n5. Решение задания 5: Календарь встреч")
    scheduler = MeetingScheduler()
    
    # Добавляем встречи
    meeting1_start = current_dt + timedelta(hours=2)
    meeting1_end = meeting1_start + timedelta(hours=1)
    scheduler.add_meeting("Встреча с командой", meeting1_start, meeting1_end)
    
    meeting2_start = current_dt + timedelta(hours=3)
    meeting2_end = meeting2_start + timedelta(hours=1)
    scheduler.add_meeting("Встреча с клиентом", meeting2_start, meeting2_end)  # Это вызовет конфликт
    
    meeting3_start = current_dt + timedelta(hours=4)
    meeting3_end = meeting3_start + timedelta(hours=1)
    scheduler.add_meeting("Обсуждение проекта", meeting3_start, meeting3_end)
    
    # Показываем предстоящие встречи
    upcoming = scheduler.get_upcoming_meetings(current_dt, 6)
    print(f"Предстоящие встречи в ближайшие 6 часов:")
    for meeting in upcoming:
        print(f"  {meeting['title']}: {meeting['start'].strftime('%H:%M')} - {meeting['end'].strftime('%H:%M')}")
    
    print("\n6. Дополнительные примеры")
    demonstrate_timedelta_operations()
    
    print("\n7. Диапазон дат")
    demonstrate_date_range()
    
    iso_date = "2023-06-15T10:30:00"
    parsed_iso = parse_iso_format(iso_date)
    print(f"Разобранный ISO формат: {parsed_iso}")