# Решения для практического задания 5: Работа с датой и временем в игровом контексте

# Ниже приведены полные реализации игровых систем с использованием модуля datetime согласно заданию


from datetime import datetime, timedelta, date
import pytz
from collections import deque, defaultdict
import random


# Задание 1.1: Создание системы отсчета игрового времени
class GameTimeTracker:
    """
    Класс для отслеживания игрового времени
    """
    def __init__(self):
        self.session_start = datetime.now()
        self.total_playtime = timedelta(0)
    
    def get_current_time(self):
        """
        Возвращает текущее время
        """
        return datetime.now()
    
    def get_session_duration(self):
        """
        Возвращает продолжительность текущей игровой сессии
        """
        return datetime.now() - self.session_start
    
    def format_duration(self, duration):
        """
        Форматирует продолжительность в удобочитаемый формат
        
        Args:
            duration (timedelta): Объект продолжительности
            
        Returns:
            str: Отформатированная строка продолжительности
        """
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Задание 1.2: Система регистрации игровых событий
class EventLogger:
    """
    Система регистрации игровых событий
    """
    def __init__(self, max_events=100):
        self.events = deque(maxlen=max_events)
    
    def log_event(self, event_type, player_name, details=""):
        """
        Регистрирует игровое событие
        
        Args:
            event_type (str): Тип события
            player_name (str): Имя игрока
            details (str): Дополнительные детали
        """
        event = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'player_name': player_name,
            'details': details
        }
        self.events.append(event)
    
    def get_events_by_type(self, event_type):
        """
        Возвращает все события заданного типа
        
        Args:
            event_type (str): Тип событий для поиска
            
        Returns:
            list: Список событий заданного типа
        """
        return [event for event in self.events if event['event_type'] == event_type]
    
    def get_events_by_timeframe(self, start_time, end_time):
        """
        Возвращает события в заданном временном промежутке
        
        Args:
            start_time (datetime): Начало промежутка
            end_time (datetime): Конец промежутка
            
        Returns:
            list: Список событий в промежутке
        """
        return [
            event for event in self.events 
            if start_time <= event['timestamp'] <= end_time
        ]


# Задание 2.1: Система кулдаунов для способностей
class CooldownManager:
    """
    Система управления кулдаунами способностей
    """
    def __init__(self):
        self.cooldowns = {}  # Словарь для хранения времени последнего использования способности
    
    def use_ability(self, player_id, ability_name, cooldown_seconds):
        """
        Попытка использования способности
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            cooldown_seconds (int): Время кулдауна в секундах
            
        Returns:
            tuple: (успешно ли использовано, время до готовности)
        """
        key = (player_id, ability_name)
        current_time = datetime.now()
        
        if key in self.cooldowns:
            last_used = self.cooldowns[key]
            time_passed = current_time - last_used
            cooldown_period = timedelta(seconds=cooldown_seconds)
            
            if time_passed < cooldown_period:
                remaining = cooldown_period - time_passed
                return False, remaining
            else:
                self.cooldowns[key] = current_time
                return True, timedelta(0)
        else:
            self.cooldowns[key] = current_time
            return True, timedelta(0)
    
    def get_remaining_cooldown(self, player_id, ability_name):
        """
        Возвращает оставшееся время до готовности способности
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            
        Returns:
            timedelta: Оставшееся время до готовности
        """
        key = (player_id, ability_name)
        if key not in self.cooldowns:
            return timedelta(0)
        
        last_used = self.cooldowns[key]
        cooldown_period = timedelta(seconds=30)  # Временно фиксированное значение
        time_passed = datetime.now() - last_used
        
        if time_passed < cooldown_period:
            return cooldown_period - time_passed
        else:
            return timedelta(0)
    
    def is_ready(self, player_id, ability_name):
        """
        Проверяет, готова ли способность к использованию
        
        Args:
            player_id (str): ID игрока
            ability_name (str): Название способности
            
        Returns:
            bool: Готова ли способность
        """
        remaining = self.get_remaining_cooldown(player_id, ability_name)
        return remaining == timedelta(0)


# Задание 2.2: Игровой календарь с напоминаниями
class GameCalendar:
    """
    Игровой календарь с напоминаниями
    """
    def __init__(self):
        self.events = {}  # Словарь событий {id: event}
        self.reminders = defaultdict(list)  # Напоминания для событий
        self.next_id = 1
    
    def add_event(self, name, start_time, duration_minutes=60, description=""):
        """
        Добавляет событие в календарь
        
        Args:
            name (str): Название события
            start_time (datetime): Время начала события
            duration_minutes (int): Продолжительность события в минутах
            description (str): Описание события
            
        Returns:
            int: ID созданного события
        """
        event_id = self.next_id
        self.next_id += 1
        
        event = {
            'id': event_id,
            'name': name,
            'start_time': start_time,
            'end_time': start_time + timedelta(minutes=duration_minutes),
            'duration': duration_minutes,
            'description': description
        }
        
        self.events[event_id] = event
        return event_id
    
    def set_reminder(self, event_id, reminder_minutes_before):
        """
        Устанавливает напоминание для события
        
        Args:
            event_id (int): ID события
            reminder_minutes_before (int): За сколько минут до события
        """
        if event_id in self.events:
            reminder_time = self.events[event_id]['start_time'] - timedelta(minutes=reminder_minutes_before)
            self.reminders[event_id].append(reminder_time)
    
    def get_upcoming_events(self, timeframe_hours=24):
        """
        Возвращает предстоящие события в заданном временном промежутке
        
        Args:
            timeframe_hours (int): Временной промежуток в часах
            
        Returns:
            list: Список предстоящих событий
        """
        now = datetime.now()
        future_limit = now + timedelta(hours=timeframe_hours)
        
        upcoming = []
        for event in self.events.values():
            if now < event['start_time'] <= future_limit:
                upcoming.append(event)
        
        # Сортируем по времени начала
        upcoming.sort(key=lambda x: x['start_time'])
        return upcoming
    
    def check_reminders(self):
        """
        Проверяет, какие напоминания должны сработать
        
        Returns:
            list: Список событий, для которых сработали напоминания
        """
        now = datetime.now()
        triggered = []
        
        for event_id, reminder_times in self.reminders.items():
            event = self.events.get(event_id)
            if event:
                for reminder_time in reminder_times:
                    # Проверяем, сработало ли напоминание (в течение последней минуты)
                    if now >= reminder_time and (now - timedelta(minutes=1)) < reminder_time:
                        triggered.append(event)
                        break
        
        return triggered


# Задание 3.1: Система ежедневных заданий
class DailyQuestSystem:
    """
    Система ежедневных заданий
    """
    def __init__(self):
        self.daily_quests = {}
        self.player_progress = {}
        self.last_refresh_date = date.today()
        # Возможные задания
        self.quest_templates = [
            {"id": "kill_5_monsters", "name": "Победить 5 монстров", "target": 5, "reward": 100},
            {"id": "collect_10_items", "name": "Собрать 10 предметов", "target": 10, "reward": 150},
            {"id": "visit_3_locations", "name": "Посетить 3 локации", "target": 3, "reward": 200},
            {"id": "complete_1_quest", "name": "Выполнить 1 задание", "target": 1, "reward": 50},
            {"id": "win_3_battles", "name": "Выиграть 3 битвы", "target": 3, "reward": 180}
        ]
    
    def refresh_daily_quests(self):
        """
        Обновляет список ежедневных заданий
        """
        current_date = date.today()
        if current_date > self.last_refresh_date:
            # Создаем новые задания на сегодня
            selected_quests = random.sample(self.quest_templates, min(3, len(self.quest_templates)))
            self.daily_quests = {quest['id']: quest for quest in selected_quests}
            self.last_refresh_date = current_date
            
            # Сбрасываем прогресс для всех игроков
            for player_id in self.player_progress:
                self.player_progress[player_id] = {
                    quest_id: {"completed": False, "progress": 0, "claimed": False} 
                    for quest_id in self.daily_quests
                }
    
    def assign_daily_quests(self, player_id):
        """
        Назначает ежедневные задания игроку
        
        Args:
            player_id (str): ID игрока
        """
        self.refresh_daily_quests()
        
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {}
        
        for quest_id in self.daily_quests:
            if quest_id not in self.player_progress[player_id]:
                self.player_progress[player_id][quest_id] = {
                    "completed": False, 
                    "progress": 0, 
                    "claimed": False
                }
    
    def complete_quest(self, player_id, quest_id):
        """
        Отмечает выполнение задания
        
        Args:
            player_id (str): ID игрока
            quest_id (str): ID задания
        """
        if player_id in self.player_progress and quest_id in self.player_progress[player_id]:
            quest_info = self.player_progress[player_id][quest_id]
            template = self.daily_quests[quest_id]
            
            quest_info["progress"] = template["target"]
            quest_info["completed"] = True
            
            return template["reward"]
        return 0
    
    def get_player_quests(self, player_id):
        """
        Возвращает список заданий игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            list: Список заданий игрока
        """
        self.refresh_daily_quests()
        
        if player_id not in self.player_progress:
            self.assign_daily_quests(player_id)
        
        quests_with_status = []
        for quest_id, progress in self.player_progress[player_id].items():
            if quest_id in self.daily_quests:
                quest_template = self.daily_quests[quest_id]
                quest_with_status = quest_template.copy()
                quest_with_status["progress"] = progress["progress"]
                quest_with_status["completed"] = progress["completed"]
                quest_with_status["claimed"] = progress["claimed"]
                quests_with_status.append(quest_with_status)
        
        return quests_with_status
    
    def time_until_reset(self):
        """
        Возвращает время до следующего сброса заданий
        
        Returns:
            timedelta: Время до сброса
        """
        tomorrow = date.today() + timedelta(days=1)
        reset_time = datetime.combine(tomorrow, datetime.min.time())
        return reset_time - datetime.now()


# Задание 3.2: Система мероприятий с часовыми поясами
class MultiTimeZoneEventManager:
    """
    Система управления мероприятиями в разных часовых поясах
    """
    def __init__(self):
        self.events = {}
        self.next_event_id = 1
    
    def create_event(self, name, start_time_utc, duration_hours, timezone_str, description=""):
        """
        Создает мероприятие в определенном часовом поясе
        
        Args:
            name (str): Название мероприятия
            start_time_utc (datetime): Время начала в UTC
            duration_hours (int): Продолжительность в часах
            timezone_str (str): Строковое обозначение часового пояса (например, 'Europe/Moscow')
            description (str): Описание мероприятия
        """
        event_id = self.next_event_id
        self.next_event_id += 1
        
        # Создаем timezone-aware объекты
        utc = pytz.UTC
        tz = pytz.timezone(timezone_str)
        
        # Преобразуем время начала в указанный часовой пояс
        start_time_localized = utc.localize(start_time_utc)
        start_time_in_tz = start_time_localized.astimezone(tz)
        
        event = {
            'id': event_id,
            'name': name,
            'start_time_utc': start_time_localized,
            'start_time_local': start_time_in_tz,
            'end_time_local': start_time_in_tz + timedelta(hours=duration_hours),
            'timezone': tz,
            'description': description,
            'duration': duration_hours
        }
        
        self.events[event_id] = event
        return event_id
    
    def get_event_time_in_timezone(self, event_id, timezone_str):
        """
        Возвращает время мероприятия в заданном часовом поясе
        
        Args:
            event_id (int): ID мероприятия
            timezone_str (str): Часовой пояс
            
        Returns:
            datetime: Время мероприятия в заданном часовом поясе
        """
        if event_id not in self.events:
            return None
        
        event = self.events[event_id]
        target_tz = pytz.timezone(timezone_str)
        
        # Конвертируем время начала из UTC в целевой часовой пояс
        return event['start_time_utc'].astimezone(target_tz)
    
    def get_events_for_user(self, user_timezone_str):
        """
        Возвращает мероприятия, актуальные для пользователя в его часовом поясе
        
        Args:
            user_timezone_str (str): Часовой пояс пользователя
            
        Returns:
            list: Список мероприятий
        """
        user_tz = pytz.timezone(user_timezone_str)
        user_now = datetime.now(user_tz)
        
        relevant_events = []
        for event in self.events.values():
            # Конвертируем время начала события в часовой пояс пользователя
            event_time_in_user_tz = event['start_time_utc'].astimezone(user_tz)
            
            # Проверяем, что событие еще не прошло (или начинается в ближайшие 24 часа)
            if event_time_in_user_tz >= user_now - timedelta(hours=24):
                event_copy = event.copy()
                event_copy['start_time_user_tz'] = event_time_in_user_tz
                relevant_events.append(event_copy)
        
        # Сортируем по времени начала в часовом поясе пользователя
        relevant_events.sort(key=lambda x: x['start_time_user_tz'])
        return relevant_events


# Задание 1.3: Система ачивок с привязкой ко времени
class TimedAchievementSystem:
    """
    Система достижений с привязкой ко времени
    """
    def __init__(self):
        self.achievements = {}
        self.player_achievements = {}
        self.player_stats = {}
        self.next_achievement_id = 1
    
    def add_timed_achievement(self, name, description, time_requirement, requirement_type="playtime"):
        """
        Добавляет достижение, связанное со временем
        
        Args:
            name (str): Название достижения
            description (str): Описание достижения
            time_requirement (timedelta): Требуемое время
            requirement_type (str): Тип требования ("playtime", "online", "idle", etc.)
        """
        achievement_id = self.next_achievement_id
        self.next_achievement_id += 1
        
        achievement = {
            'id': achievement_id,
            'name': name,
            'description': description,
            'time_requirement': time_requirement,
            'requirement_type': requirement_type,
            'achieved_by': set()  # Игроки, получившие достижение
        }
        
        self.achievements[achievement_id] = achievement
    
    def track_player_activity(self, player_id, activity_time):
        """
        Отслеживает активность игрока
        
        Args:
            player_id (str): ID игрока
            activity_time (timedelta): Время активности
        """
        if player_id not in self.player_stats:
            self.player_stats[player_id] = {
                'playtime': timedelta(0),
                'last_activity': datetime.now()
            }
        
        self.player_stats[player_id]['playtime'] += activity_time
        self.player_stats[player_id]['last_activity'] = datetime.now()
    
    def check_achievements(self, player_id):
        """
        Проверяет, какие достижения были получены игроком
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            list: Список полученных достижений
        """
        if player_id not in self.player_stats:
            return []
        
        achieved = []
        player_stats = self.player_stats[player_id]
        
        for ach_id, achievement in self.achievements.items():
            if ach_id in [a['id'] for a in achieved]:  # Уже получено
                continue
                
            if achievement['requirement_type'] == 'playtime':
                if player_stats['playtime'] >= achievement['time_requirement']:
                    if player_id not in achievement['achieved_by']:
                        achievement['achieved_by'].add(player_id)
                        achieved.append(achievement)
        
        return achieved


# Задание 1.4: Система логирования с временным фильтром
class TimeFilteredLogger:
    """
    Система логирования с фильтрацией по времени
    """
    def __init__(self, max_logs=1000):
        self.logs = deque(maxlen=max_logs)
    
    def log(self, level, message, player_id=None):
        """
        Записывает сообщение в лог
        
        Args:
            level (str): Уровень сообщения (INFO, WARNING, ERROR)
            message (str): Текст сообщения
            player_id (str): ID игрока (опционально)
        """
        log_entry = {
            'timestamp': datetime.now(),
            'level': level.upper(),
            'message': message,
            'player_id': player_id
        }
        self.logs.append(log_entry)
    
    def get_logs_by_timeframe(self, start_time, end_time):
        """
        Возвращает логи в заданном временном промежутке
        
        Args:
            start_time (datetime): Начало промежутка
            end_time (datetime): Конец промежутка
            
        Returns:
            list: Список логов в промежутке
        """
        return [
            log for log in self.logs 
            if start_time <= log['timestamp'] <= end_time
        ]
    
    def get_logs_by_level(self, level, hours_back=24):
        """
        Возвращает логи заданного уровня за последнее время
        
        Args:
            level (str): Уровень логов
            hours_back (int): Количество часов назад
            
        Returns:
            list: Список логов
        """
        timeframe_start = datetime.now() - timedelta(hours=hours_back)
        level_upper = level.upper()
        
        return [
            log for log in self.logs 
            if log['level'] == level_upper and log['timestamp'] >= timeframe_start
        ]


# Задание 2.3: Система турниров с расписанием
class TournamentScheduler:
    """
    Система расписания турниров
    """
    def __init__(self):
        self.tournaments = {}
        self.next_tournament_id = 1
    
    def schedule_tournament(self, name, start_time, duration_minutes, registration_end_delta=None):
        """
        Планирует турнир
        
        Args:
            name (str): Название турнира
            start_time (datetime): Время начала
            duration_minutes (int): Продолжительность в минутах
            registration_end_delta (timedelta): За сколько времени до начала закрывается регистрация
        """
        tournament_id = self.next_tournament_id
        self.next_tournament_id += 1
        
        if registration_end_delta is None:
            registration_end_delta = timedelta(hours=1)  # По умолчанию регистрация закрывается за 1 час
        
        registration_end = start_time - registration_end_delta
        
        tournament = {
            'id': tournament_id,
            'name': name,
            'start_time': start_time,
            'end_time': start_time + timedelta(minutes=duration_minutes),
            'registration_end': registration_end,
            'duration': duration_minutes,
            'registered_players': [],
            'status': 'scheduled'  # scheduled, ongoing, finished
        }
        
        self.tournaments[tournament_id] = tournament
        return tournament_id
    
    def register_player(self, tournament_id, player_id):
        """
        Регистрирует игрока на турнир
        
        Args:
            tournament_id (int): ID турнира
            player_id (str): ID игрока
        """
        if tournament_id not in self.tournaments:
            return False, "Турнир не найден"
        
        tournament = self.tournaments[tournament_id]
        
        if not self.is_registration_open(tournament_id):
            return False, "Регистрация закрыта"
        
        if player_id in tournament['registered_players']:
            return False, "Игрок уже зарегистрирован"
        
        # Ограничение на количество участников (например, 16)
        if len(tournament['registered_players']) >= 16:
            return False, "Турнир уже набран"
        
        tournament['registered_players'].append(player_id)
        return True, "Успешно зарегистрирован"
    
    def get_upcoming_tournaments(self, hours_ahead=24):
        """
        Возвращает предстоящие турниры
        
        Args:
            hours_ahead (int): На сколько часов вперед
            
        Returns:
            list: Список предстоящих турниров
        """
        now = datetime.now()
        future_limit = now + timedelta(hours=hours_ahead)
        
        upcoming = []
        for tournament in self.tournaments.values():
            if now < tournament['start_time'] <= future_limit:
                tournament_copy = tournament.copy()
                tournament_copy['spots_left'] = 16 - len(tournament['registered_players'])
                upcoming.append(tournament_copy)
        
        # Сортируем по времени начала
        upcoming.sort(key=lambda x: x['start_time'])
        return upcoming
    
    def is_registration_open(self, tournament_id):
        """
        Проверяет, открыта ли регистрация на турнир
        
        Args:
            tournament_id (int): ID турнира
            
        Returns:
            bool: Открыта ли регистрация
        """
        if tournament_id not in self.tournaments:
            return False
        
        tournament = self.tournaments[tournament_id]
        now = datetime.now()
        
        return now <= tournament['registration_end'] and len(tournament['registered_players']) < 16


# Задание 2.4: Система ежедневных наград
class DailyRewardSystem:
    """
    Система ежедневных наград
    """
    def __init__(self):
        self.player_streaks = {}  # Серии получения наград
        self.rewards_calendar = {}  # Календарь наград
        self.reward_schedule = [
            {"day": 1, "reward": "100 монет"},
            {"day": 2, "reward": "200 монет"},
            {"day": 3, "reward": "300 монет"},
            {"day": 4, "reward": "Зелье лечения x5"},
            {"day": 5, "reward": "500 монет"},
            {"day": 6, "reward": "Магический свиток"},
            {"day": 7, "reward": "Эпическое оружие"}
        ]
    
    def claim_daily_reward(self, player_id):
        """
        Получение ежедневной награды
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            tuple: (успешно ли, награда, серия)
        """
        today = date.today()
        
        if player_id not in self.player_streaks:
            self.player_streaks[player_id] = {
                'current_streak': 0,
                'last_claimed': None,
                'total_claims': 0
            }
        
        player_data = self.player_streaks[player_id]
        
        # Проверяем, не получал ли игрок награду сегодня
        if player_data['last_claimed'] == today:
            return False, "Награда уже получена сегодня", player_data['current_streak']
        
        # Проверяем, был ли пропуск дня
        if player_data['last_claimed'] is not None:
            days_since_last = (today - player_data['last_claimed']).days
            if days_since_last > 1:
                # Серия прервана
                player_data['current_streak'] = 0
        
        # Увеличиваем серию
        player_data['current_streak'] += 1
        player_data['last_claimed'] = today
        player_data['total_claims'] += 1
        
        # Определяем награду
        day_index = min(player_data['current_streak'], 7) - 1  # Ограничиваем до 7 дней
        reward = self.reward_schedule[day_index]['reward']
        
        return True, reward, player_data['current_streak']
    
    def get_current_streak(self, player_id):
        """
        Возвращает текущую серию игрока
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            int: Количество дней подряд
        """
        if player_id not in self.player_streaks:
            return 0
        return self.player_streaks[player_id]['current_streak']
    
    def get_next_reward_info(self, player_id):
        """
        Возвращает информацию о следующей награде
        
        Args:
            player_id (str): ID игрока
            
        Returns:
            dict: Информация о следующей награде
        """
        current_streak = self.get_current_streak(player_id)
        next_day = current_streak + 1
        
        # Определяем следующую награду
        day_index = min(next_day, 7) - 1
        next_reward = self.reward_schedule[day_index]['reward']
        
        # Проверяем, когда игрок сможет получить награду
        if player_id in self.player_streaks and self.player_streaks[player_id]['last_claimed'] == date.today():
            # Награда доступна завтра
            next_claim_date = date.today() + timedelta(days=1)
        else:
            # Награда доступна сегодня
            next_claim_date = date.today()
        
        return {
            'day': next_day,
            'reward': next_reward,
            'available_date': next_claim_date,
            'current_streak': current_streak
        }


# Задание 3.3: Система игрового времени с ускорением
class GameTimeSystem:
    """
    Система игрового времени с возможностью ускорения
    """
    def __init__(self, real_time_multiplier=1.0):
        self.real_time_multiplier = real_time_multiplier
        self.game_epoch = datetime.now()  # Начало игровой эпохи
        self.reference_real_time = datetime.now()
        self.paused = False
        self.pause_time = None
        self.adjusted_time_offset = timedelta(0)
    
    def get_game_time(self):
        """
        Возвращает текущее игровое время
        
        Returns:
            datetime: Текущее игровое время
        """
        if self.paused:
            # Возвращаем время на момент паузы
            return self.game_epoch + self.adjusted_time_offset
        
        # Вычисляем прошедшее игровое время с учетом ускорения
        real_time_passed = datetime.now() - self.reference_real_time
        game_time_passed = real_time_passed * self.real_time_multiplier
        
        return self.game_epoch + self.adjusted_time_offset + game_time_passed
    
    def accelerate_time(self, multiplier):
        """
        Устанавливает множитель скорости времени
        
        Args:
            multiplier (float): Множитель (например, 2.0 для 2x скорости)
        """
        # Обновляем смещение, чтобы избежать скачков во времени
        current_game_time = self.get_game_time()
        self.game_epoch = current_game_time
        self.reference_real_time = datetime.now()
        self.real_time_multiplier = multiplier
    
    def pause_resume(self):
        """
        Пауза/возобновление игрового времени
        """
        if self.paused:
            # Возобновляем
            self.reference_real_time = datetime.now()
            self.paused = False
        else:
            # Приостанавливаем
            self.adjusted_time_offset += (datetime.now() - self.reference_real_time) * self.real_time_multiplier
            self.pause_time = datetime.now()
            self.paused = True
    
    def advance_time(self, time_delta):
        """
        Принудительно продвигает игровое время вперед
        
        Args:
            time_delta (timedelta): Время, на которое нужно продвинуть
        """
        self.adjusted_time_offset += time_delta
        # Обновляем эпоху, чтобы избежать смещения при изменении множителя
        self.game_epoch = self.get_game_time() - self.adjusted_time_offset
        self.reference_real_time = datetime.now()


# Задание 3.4: Комплексная система событий
class ComprehensiveEventManager:
    """
    Комплексная система управления игровыми событиями
    """
    def __init__(self):
        self.events = {}
        self.event_participants = defaultdict(set)
        self.player_timezones = {}  # Часовые пояса игроков
        self.notifications = {}  # Система уведомлений
        self.next_event_id = 1
    
    def create_recurring_event(self, name, start_time, duration_minutes, recurrence_pattern, timezone_str, description=""):
        """
        Создает повторяющееся событие
        
        Args:
            name (str): Название события
            start_time (datetime): Время начала
            duration_minutes (int): Продолжительность
            recurrence_pattern (str): Паттерн повторения ('daily', 'weekly', 'monthly')
            timezone_str (str): Часовой пояс
            description (str): Описание
        """
        event_id = self.next_event_id
        self.next_event_id += 1
        
        # Создаем timezone-aware объекты
        tz = pytz.timezone(timezone_str)
        start_time_localized = tz.localize(start_time)
        
        event = {
            'id': event_id,
            'name': name,
            'start_time': start_time_localized,  # Время в заданном часовом поясе
            'end_time': start_time_localized + timedelta(minutes=duration_minutes),
            'duration': duration_minutes,
            'recurrence': recurrence_pattern,
            'timezone': tz,
            'description': description,
            'created_at': datetime.now()
        }
        
        self.events[event_id] = event
        return event_id
    
    def register_for_event(self, event_id, player_id, preferred_timezone=None):
        """
        Регистрирует игрока на событие
        
        Args:
            event_id (int): ID события
            player_id (str): ID игрока
            preferred_timezone (str): Предпочтительный часовой пояс игрока
        """
        if event_id not in self.events:
            return False, "Событие не найдено"
        
        self.event_participants[event_id].add(player_id)
        
        if preferred_timezone:
            self.player_timezones[player_id] = pytz.timezone(preferred_timezone)
        
        return True, "Успешно зарегистрирован"
    
    def get_player_events(self, player_id, timeframe_days=7):
        """
        Возвращает события для конкретного игрока
        
        Args:
            player_id (str): ID игрока
            timeframe_days (int): На сколько дней вперед
            
        Returns:
            list: Список событий игрока
        """
        player_tz = self.player_timezones.get(player_id, pytz.UTC)
        now = datetime.now(player_tz)
        future_limit = now + timedelta(days=timeframe_days)
        
        player_events = []
        for event_id, participants in self.event_participants.items():
            if player_id in participants and event_id in self.events:
                event = self.events[event_id]
                
                # Преобразуем время события в часовой пояс игрока
                event_time_in_player_tz = event['start_time'].astimezone(player_tz)
                
                # Проверяем, что событие в пределах заданного времени
                if now <= event_time_in_player_tz <= future_limit:
                    event_copy = event.copy()
                    event_copy['start_time_player_tz'] = event_time_in_player_tz
                    event_copy['participant_count'] = len(participants)
                    player_events.append(event_copy)
        
        # Сортируем по времени начала в часовом поясе игрока
        player_events.sort(key=lambda x: x['start_time_player_tz'])
        return player_events
    
    def send_reminders(self):
        """
        Отправляет уведомления участникам событий
        """
        now = datetime.now(pytz.UTC)
        notification_window = timedelta(minutes=15)  # Напоминать за 15 минут
        
        notifications_sent = []
        for event_id, event in self.events.items():
            # Проверяем, приближается ли время события
            time_to_start = event['start_time'].astimezone(pytz.UTC) - now
            
            if timedelta(0) <= time_to_start <= notification_window:
                # Отправляем напоминание всем участникам
                for participant in self.event_participants[event_id]:
                    participant_tz = self.player_timezones.get(participant, pytz.UTC)
                    event_time_in_participant_tz = event['start_time'].astimezone(participant_tz)
                    
                    notification = {
                        'player_id': participant,
                        'event_id': event_id,
                        'event_name': event['name'],
                        'event_time': event_time_in_participant_tz.strftime('%Y-%m-%d %H:%M %Z'),
                        'sent_at': now
                    }
                    
                    notifications_sent.append(notification)
        
        return notifications_sent


# Примеры использования всех классов
if __name__ == "__main__":
    print("=== Демонстрация игровых систем с использованием модуля datetime ===\n")
    
    # Пример использования GameTimeTracker
    print("--- Система отслеживания игрового времени ---")
    time_tracker = GameTimeTracker()
    print(f"Текущее время: {time_tracker.get_current_time()}")
    session_duration = time_tracker.get_session_duration()
    print(f"Длительность сессии: {time_tracker.format_duration(session_duration)}")
    print()
    
    # Пример использования EventLogger
    print("--- Система регистрации событий ---")
    event_logger = EventLogger(max_events=50)
    event_logger.log_event("battle_won", "Игрок1", "Победа над драконом")
    event_logger.log_event("item_found", "Игрок1", "Меч легенд")
    battle_events = event_logger.get_events_by_type("battle_won")
    print(f"Боевые события: {len(battle_events)}")
    print()
    
    # Пример использования CooldownManager
    print("--- Система кулдаунов ---")
    cooldown_mgr = CooldownManager()
    success, remaining = cooldown_mgr.use_ability("player1", "fireball", 30)
    print(f"Использование способности: {success}, осталось: {remaining}")
    ready = cooldown_mgr.is_ready("player1", "fireball")
    print(f"Способность готова: {ready}")
    print()
    
    # Пример использования GameCalendar
    print("--- Игровой календарь ---")
    calendar = GameCalendar()
    event_id = calendar.add_event("Турнир", datetime(2023, 10, 15, 18, 0), 120, "Еженедельный турнир")
    calendar.set_reminder(event_id, 30)  # Напомнить за 30 минут
    upcoming = calendar.get_upcoming_events(24)
    print(f"Предстоящие события: {len(upcoming)}")
    print()
    
    # Пример использования DailyQuestSystem
    print("--- Система ежедневных заданий ---")
    quest_system = DailyQuestSystem()
    quest_system.assign_daily_quests("player1")
    player_quests = quest_system.get_player_quests("player1")
    print(f"Задания игрока: {len(player_quests)}")
    reset_time = quest_system.time_until_reset()
    print(f"Время до сброса заданий: {reset_time}")
    print()
    
    # Пример использования MultiTimeZoneEventManager
    print("--- Система мероприятий с часовыми поясами ---")
    event_manager = MultiTimeZoneEventManager()
    event_id = event_manager.create_event(
        "Глобальный турнир", 
        datetime(2023, 10, 15, 15, 0),  # 15:00 UTC
        2, 
        "Europe/Moscow", 
        "Ежемесячный глобальный турнир"
    )
    moscow_time = event_manager.get_event_time_in_timezone(event_id, "Europe/Moscow")
    print(f"Время турнира в Москве: {moscow_time}")
    user_events = event_manager.get_events_for_user("Europe/Moscow")
    print(f"События для пользователя в часовом поясе Москвы: {len(user_events)}")
    print()
    
    # Пример использования TimedAchievementSystem
    print("--- Система достижений с привязкой ко времени ---")
    achievement_system = TimedAchievementSystem()
    achievement_system.add_timed_achievement("Марафонец", "Играть 10 часов подряд", timedelta(hours=10), "playtime")
    achievement_system.track_player_activity("player1", timedelta(hours=5))
    achieved = achievement_system.check_achievements("player1")
    print(f"Полученные достижения: {len(achieved)}")
    print()
    
    # Пример использования TimeFilteredLogger
    print("--- Система логирования с временным фильтром ---")
    time_logger = TimeFilteredLogger(max_logs=100)
    time_logger.log("INFO", "Игрок вошел в игру", "player1")
    time_logger.log("ERROR", "Ошибка подключения", "player2")
    recent_logs = time_logger.get_logs_by_level("ERROR", 1)
    print(f"Ошибки за последний час: {len(recent_logs)}")
    print()
    
    # Пример использования TournamentScheduler
    print("--- Система расписания турниров ---")
    tournament_scheduler = TournamentScheduler()
    tournament_id = tournament_scheduler.schedule_tournament("Еженедельный турнир", datetime(2023, 10, 20, 19, 0), 120)
    success, msg = tournament_scheduler.register_player(tournament_id, "player1")
    print(f"Регистрация: {success}, сообщение: {msg}")
    upcoming_tournaments = tournament_scheduler.get_upcoming_tournaments(24)
    print(f"Предстоящие турниры: {len(upcoming_tournaments)}")
    print()
    
    # Пример использования DailyRewardSystem
    print("--- Система ежедневных наград ---")
    daily_rewards = DailyRewardSystem()
    success, reward, streak = daily_rewards.claim_daily_reward("player1")
    print(f"Получение награды: {success}, награда: {reward}, серия: {streak}")
    next_reward_info = daily_rewards.get_next_reward_info("player1")
    print(f"Следующая награда: {next_reward_info}")
    print()
    
    # Пример использования GameTimeSystem
    print("--- Система игрового времени с ускорением ---")
    game_time_system = GameTimeSystem(real_time_multiplier=0.5)  # Игровое время идет в 2 раза медленнее
    current_game_time = game_time_system.get_game_time()
    print(f"Текущее игровое время: {current_game_time}")
    print()
    
    # Пример использования ComprehensiveEventManager
    print("--- Комплексная система событий ---")
    comp_event_manager = ComprehensiveEventManager()
    recurring_event_id = comp_event_manager.create_recurring_event(
        "Еженедельный турнир", 
        datetime(2023, 10, 15, 18, 0), 
        120, 
        "weekly", 
        "Europe/Moscow"
    )
    comp_event_manager.register_for_event(recurring_event_id, "player1", "Europe/Moscow")
    player_events = comp_event_manager.get_player_events("player1", 7)
    print(f"События игрока: {len(player_events)}")
    reminders = comp_event_manager.send_reminders()
    print(f"Отправлено напоминаний: {len(reminders)}")
    print()
    
    print("Все игровые системы с использованием модуля datetime успешно реализованы!")