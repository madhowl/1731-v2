# Решения для практического задания 2: Создание декораторов в игровом контексте

# Ниже приведены полные реализации игровых декораторов согласно заданию


def log_game_action(func):
    """
    Декоратор, который логирует вызовы игровых действий
    """
    def wrapper(*args, **kwargs):
        print(f"Выполняется действие: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Действие {func.__name__} завершено")
        return result
    return wrapper


def timing_game_action(func):
    """
    Декоратор, который измеряет время выполнения игрового действия
    """
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения {func.__name__}: {execution_time:.4f} секунд")
        return result
    return wrapper


def check_alive(func):
    """
    Декоратор, который проверяет, жив ли персонаж перед выполнением действия
    """
    def wrapper(character, *args, **kwargs):
        if hasattr(character, 'health') and character.health > 0:
            return func(character, *args, **kwargs)
        else:
            print(f"{character.name} мертв и не может выполнить действие")
            return None
    return wrapper


def log_action(action_type):
    """
    Декоратор, который логирует игровое действие
    
    Args:
        action_type (str): Тип действия для логирования
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[ЛОГ] Начало {action_type}: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[ЛОГ] Завершено {action_type}: {result}")
            return result
        return wrapper
    return decorator


def requires_mana(mana_cost):
    """
    Декоратор, который проверяет наличие маны перед использованием заклинания
    
    Args:
        mana_cost (int): Количество требуемой маны
    """
    def decorator(func):
        def wrapper(caster, *args, **kwargs):
            if caster.mana >= mana_cost:
                caster.mana -= mana_cost
                print(f"{caster.name} тратит {mana_cost} маны")
                return func(caster, *args, **kwargs)
            else:
                print(f"{caster.name} не хватает {mana_cost - caster.mana} маны для заклинания")
                return None
        return wrapper
    return decorator


def conditional_effect(effect_condition):
    """
    Декоратор, который проверяет наличие состояния перед выполнением действия
    
    Args:
        effect_condition (str): Условие, которое блокирует выполнение действия
    """
    def decorator(func):
        def wrapper(character, *args, **kwargs):
            if effect_condition in character.effects:
                print(f"{character.name} не может выполнить действие из-за состояния '{effect_condition}'")
                return None
            else:
                return func(character, *args, **kwargs)
        return wrapper
    return decorator


def cached_property(func):
    """
    Декоратор, который кэширует результаты вычисления свойств персонажа
    """
    attr_name = '_' + func.__name__
    
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper


def requires_conditions(**conditions):
    """
    Декоратор, который проверяет несколько условий перед выполнением действия
    
    Args:
        **conditions: Условия в формате имя_атрибута=значение
    """
    def decorator(func):
        def wrapper(obj, *args, **kwargs):
            for attr, required_value in conditions.items():
                if not hasattr(obj, attr):
                    print(f"Объект не имеет атрибута '{attr}'")
                    return None
                
                actual_value = getattr(obj, attr)
                
                if isinstance(required_value, tuple) and len(required_value) == 2:
                    # Проверка диапазона (min, max)
                    min_val, max_val = required_value
                    if not (min_val <= actual_value <= max_val):
                        print(f"Недостаточно значения '{attr}': требуется между {min_val}-{max_val}, имеется {actual_value}")
                        return None
                elif actual_value < required_value:
                    print(f"Недостаточно значения '{attr}': требуется {required_value}, имеется {actual_value}")
                    return None
            
            return func(obj, *args, **kwargs)
        return wrapper
    return decorator


def game_message(prefix="[ИГРА]", suffix="[КОНЕЦ]"):
    """
    Декоратор, который оборачивает результат функции в игровое сообщение
    
    Args:
        prefix (str): Префикс сообщения
        suffix (str): Суффикс сообщения
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{prefix} {result} {suffix}"
        return wrapper
    return decorator


def limited_uses(max_uses):
    """
    Декоратор, который ограничивает количество использований способности
    
    Args:
        max_uses (int): Максимальное количество использований
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not hasattr(wrapper, 'uses'):
                wrapper.uses = 0
            
            if wrapper.uses < max_uses:
                wrapper.uses += 1
                result = func(*args, **kwargs)
                print(f"Осталось использований: {max_uses - wrapper.uses}")
                return result
            else:
                print(f"Способность '{func.__name__}' больше не может быть использована")
                return None
        return wrapper
    return decorator


def requires_class(*allowed_classes):
    """
    Декоратор, который проверяет класс персонажа перед использованием способности
    
    Args:
        *allowed_classes: Допустимые классы персонажа
    """
    def decorator(func):
        def wrapper(character, *args, **kwargs):
            if not hasattr(character, 'char_class'):
                print(f"Персонаж {character.name} не имеет класса")
                return None
            
            if character.char_class in allowed_classes:
                return func(character, *args, **kwargs)
            else:
                print(f"{character.name} (класс: {character.char_class}) не может использовать эту способность")
                return None
        return wrapper
    return decorator


def add_effect_on_success(effect_name, duration=1):
    """
    Декоратор, который добавляет эффект при успешном выполнении действия
    
    Args:
        effect_name (str): Название эффекта
        duration (int): Длительность эффекта
    """
    def decorator(func):
        def wrapper(character, *args, **kwargs):
            result = func(character, *args, **kwargs)
            
            if result is not None:  # Проверяем, что функция выполнилась успешно
                character.add_effect(effect_name, duration)
            
            return result
        return wrapper
    return decorator


import random

def critical_hit(chance=0.1, multiplier=2.0, condition=None):
    """
    Декоратор, который реализует механику критических ударов
    
    Args:
        chance (float): Шанс критического удара (от 0 до 1)
        multiplier (float): Множитель урона при критическом ударе
        condition (callable): Функция-условие для возможности критического удара
    """
    def decorator(func):
        def wrapper(attacker, target, base_damage, *args, **kwargs):
            # Вызовите оригинальную функцию для получения базового урона
            damage = func(attacker, target, base_damage, *args, **kwargs)
            
            # Проверяем, применимо ли условие (если задано)
            if condition is None or condition(attacker, target):
                # Проверяем, случился ли критический удар
                if random.random() < chance:
                    critical_damage = damage * multiplier
                    print(f"КРИТИЧЕСКИЙ УДАР! {attacker.name} наносит {critical_damage:.1f} урона вместо {damage}!")
                    return critical_damage
            
            return damage
        return wrapper
    return decorator


def game_mechanic(**rules):
    """
    Универсальный декоратор для игровых механик
    
    Args:
        **rules: Правила в формате ключ=значение
        Возможные правила:
        - required_resources: требуемые ресурсы
        - cooldown: время перезарядки
        - chance: шанс успеха
        - effect_on_success: эффект при успехе
        - cost_on_use: расход ресурсов при использовании
    """
    def decorator(func):
        def wrapper(entity, *args, **kwargs):
            import time
            
            # Проверка времени перезарядки
            if 'cooldown' in rules:
                action_name = func.__name__
                current_time = time.time()
                
                if hasattr(entity, 'cooldowns') and action_name in entity.cooldowns:
                    last_used = entity.cooldowns[action_name]
                    if current_time - last_used < rules['cooldown']:
                        remaining = rules['cooldown'] - (current_time - last_used)
                        print(f"{entity.name}: Перезарядка, осталось {remaining:.1f} секунд")
                        return None
                
            # Проверка требуемых ресурсов
            if 'required_resources' in rules:
                for resource, required_amount in rules['required_resources'].items():
                    if not hasattr(entity, resource):
                        print(f"{entity.name}: Нет ресурса '{resource}'")
                        return None
                    
                    if getattr(entity, resource) < required_amount:
                        print(f"{entity.name}: Недостаточно {resource}, требуется {required_amount}, есть {getattr(entity, resource)}")
                        return None
            
            # Проверка шанса успеха
            if 'chance' in rules:
                if not isinstance(rules['chance'], (int, float)) or rules['chance'] < random.random():
                    print(f"{entity.name}: Действие '{func.__name__}' не удалось из-за шанса")
                    # Применяем расход даже при неудаче, если указан
                    if 'cost_on_use' in rules:
                        for resource, cost in rules['cost_on_use'].items():
                            if hasattr(entity, resource):
                                setattr(entity, resource, getattr(entity, resource) - cost)
                    return None
            
            # Выполнение действия
            result = func(entity, *args, **kwargs)
            
            # Применение расхода ресурсов
            if 'cost_on_use' in rules:
                for resource, cost in rules['cost_on_use'].items():
                    if hasattr(entity, resource):
                        setattr(entity, resource, getattr(entity, resource) - cost)
            
            # Применение эффекта при успехе
            if result is not None and 'effect_on_success' in rules:
                effect_name = rules['effect_on_success']
                if hasattr(entity, 'add_effect'):
                    duration = rules.get('effect_duration', 1)
                    entity.add_effect(effect_name, duration)
            
            # Установка времени перезарядки
            if 'cooldown' in rules:
                if not hasattr(entity, 'cooldowns'):
                    entity.cooldowns = {}
                entity.cooldowns[action_name] = time.time()
            
            return result
        return wrapper
    return decorator


# Примеры классов для тестирования декораторов

class Character:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
    
    @check_alive
    def attack(self, target, damage):
        """Атака цели"""
        print(f"{self.name} атакует {target.name} на {damage} урона")
        target.take_damage(damage)
        return f"{self.name} атаковал {target.name}"

    def take_damage(self, damage):
        """Получение урона"""
        self.health = max(0, self.health - damage)
        print(f"{self.name} получил {damage} урона. Осталось здоровья: {self.health}")

    def __str__(self):
        return f"Character(name='{self.name}', health={self.health})"


class Mage:
    def __init__(self, name, mana=100):
        self.name = name
        self.mana = mana

    @log_action("casting")
    def cast_fireball(self, target):
        """Произнесение заклинания огненного шара"""
        cost = 10
        if self.mana >= cost:
            self.mana -= cost
            return f"{self.name} произносит огненный шар в {target}"
        else:
            return f"{self.name} не хватает маны для заклинания"

    def __str__(self):
        return f"Mage(name='{self.name}', mana={self.mana})"


class Wizard:
    def __init__(self, name, mana=50):
        self.name = name
        self.mana = mana

    @requires_mana(15)
    def cast_lightning_bolt(self, target):
        """Произнесение заклинания молнии"""
        return f"{self.name} поражает {target} молнией!"

    @requires_mana(30)
    def cast_teleport(self):
        """Произнесение заклинания телепортации"""
        return f"{self.name} телепортируется!"

    def __str__(self):
        return f"Wizard(name='{self.name}', mana={self.mana})"


class EnhancedCharacter:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.effects = []  # Список активных состояний

    def add_effect(self, effect):
        """Добавить состояние к персонажу"""
        self.effects.append(effect)

    def remove_effect(self, effect):
        """Удалить состояние у персонажа"""
        if effect in self.effects:
            self.effects.remove(effect)

    @conditional_effect("stunned")
    def attack(self, target, damage):
        """Атака цели"""
        return f"{self.name} атакует {target.name} на {damage} урона"

    @conditional_effect("silenced")
    def cast_spell(self, spell_name):
        """Произнесение заклинания"""
        return f"{self.name} произносит заклинание {spell_name}"

    def __str__(self):
        return f"EnhancedCharacter(name='{self.name}', health={self.health}, effects={self.effects})"


class AdvancedCharacter:
    def __init__(self, name, base_strength=10, base_agility=10, base_intelligence=10):
        self.name = name
        self.base_strength = base_strength
        self.base_agility = base_agility
        self.base_intelligence = base_intelligence
        self.buffs = []  # Список баффов
        self.debuffs = [] # Список дебаффов

    def add_buff(self, stat, value):
        """Добавить бафф к характеристике"""
        self.buffs.append((stat, value))

    def add_debuff(self, stat, value):
        """Добавить дебафф к характеристике"""
        self.debuffs.append((stat, value))

    @cached_property
    def strength(self):
        """Вычисление общей силы с учетом баффов/дебаффов"""
        total = self.base_strength
        for stat, value in self.buffs:
            if stat == "strength":
                total += value
        for stat, value in self.debuffs:
            if stat == "strength":
                total -= value
        print(f"Вычисляется сила для {self.name}: {total}")
        return total

    @cached_property
    def agility(self):
        """Вычисление общей ловкости с учетом баффов/дебаффов"""
        total = self.base_agility
        for stat, value in self.buffs:
            if stat == "agility":
                total += value
        for stat, value in self.debuffs:
            if stat == "agility":
                total -= value
        print(f"Вычисляется ловкость для {self.name}: {total}")
        return total

    @cached_property
    def intelligence(self):
        """Вычисление общего интеллекта с учетом баффов/дебаффов"""
        total = self.base_intelligence
        for stat, value in self.buffs:
            if stat == "intelligence":
                total += value
        for stat, value in self.debuffs:
            if stat == "intelligence":
                total -= value
        print(f"Вычисляется интеллект для {self.name}: {total}")
        return total

    def __str__(self):
        return f"AdvancedCharacter(name='{self.name}', strength={self.strength}, agility={self.agility}, intelligence={self.intelligence})"


class Warrior:
    def __init__(self, name, level=1, rage=0):
        self.name = name
        self.level = level
        self.rage = rage

    @requires_conditions(level=5, rage=10)
    def use_berserk(self):
        """Использовать состояние берсерка"""
        self.rage -= 10
        return f"{self.name} входит в состояние берсерка!"

    @requires_conditions(level=10)
    def use_whirlwind(self, targets):
        """Использовать вращающийся удар по нескольким целям"""
        return f"{self.name} использует вращающийся удар по {len(targets)} целям!"

    def __str__(self):
        return f"Warrior(name='{self.name}', level={self.level}, rage={self.rage})"


class Paladin:
    def __init__(self, name):
        self.name = name

    @limited_uses(3)
    def cast_divine_shield(self):
        """Произнесение божественного щита"""
        return f"{self.name} использует божественный щит!"

    def __str__(self):
        return f"Paladin(name='{self.name}')"


class GameCharacter:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class

    @requires_class("mage", "archer")
    def use_ranged_ability(self, target):
        """Использовать дальнобойную способность"""
        return f"{self.name} использует дальнобойную способность против {target}"

    @requires_class("warrior", "paladin")
    def use_melee_ability(self, target):
        """Использовать ближнюю способность"""
        return f"{self.name} использует ближнюю способность против {target}"

    def __str__(self):
        return f"GameCharacter(name='{self.name}', class='{self.char_class}')"


class EffectCharacter:
    def __init__(self, name):
        self.name = name
        self.effects = {}

    def add_effect(self, effect_name, duration):
        """Добавить эффект к персонажу"""
        self.effects[effect_name] = duration
        print(f"{self.name} получил эффект '{effect_name}' на {duration} ходов")

    def remove_effect(self, effect_name):
        """Удалить эффект у персонажа"""
        if effect_name in self.effects:
            del self.effects[effect_name]
            print(f"Эффект '{effect_name}' у {self.name} истек")

    @add_effect_on_success("invincibility", 2)
    def use_ultimate(self):
        """Использовать ультимейт способность"""
        print(f"{self.name} использует ультимейт способность!")
        return "Ультимейт активирован"

    @add_effect_on_success("poison", 3)
    def use_poison_trap(self, target):
        """Использовать ядовитую ловушку"""
        print(f"{self.name} активирует ядовитую ловушку на {target.name}")
        return f"Ловушка активирована на {target.name}"

    def __str__(self):
        return f"EffectCharacter(name='{self.name}', effects={self.effects})"


class CombatCharacter:
    def __init__(self, name, crit_chance_bonus=0):
        self.name = name
        self.crit_chance_bonus = crit_chance_bonus

    @critical_hit(chance=0.15, multiplier=2.5)
    def basic_attack(self, target, base_damage):
        """Базовая атака"""
        print(f"{self.name} атакует {target.name}")
        return base_damage

    @critical_hit(
        chance=0.2, 
        multiplier=3.0, 
        condition=lambda attacker, target: attacker.crit_chance_bonus > 0
    )
    def special_attack(self, target, base_damage):
        """Специальная атака с условием"""
        print(f"{self.name} выполняет специальную атаку по {target.name}")
        return base_damage

    def __str__(self):
        return f"CombatCharacter(name='{self.name}', crit_bonus={self.crit_chance_bonus})"


class GameEntity:
    def __init__(self, name, health=100, mana=50, stamina=100):
        self.name = name
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.cooldowns = {}

    def add_effect(self, effect_name, duration):
        """Добавить эффект к сущности"""
        if not hasattr(self, 'effects'):
            self.effects = {}
        self.effects[effect_name] = duration

    @game_mechanic(
        required_resources={'mana': 20},
        cooldown=3,
        effect_on_success='invincible',
        cost_on_use={'mana': 20, 'stamina': 10}
    )
    def divine_protection(self):
        """Божественная защита"""
        return f"{self.name} использует божественную защиту!"

    @game_mechanic(
        required_resources={'stamina': 30},
        chance=0.7,
        effect_on_success='strong'
    )
    def power_strike(self, target):
        """Мощный удар"""
        return f"{self.name} наносит мощный удар по {target.name}!"

    def __str__(self):
        return f"GameEntity(name='{self.name}', health={self.health}, mana={self.mana}, stamina={self.stamina})"


# Примеры использования декораторов
if __name__ == "__main__":
    print("=== Примеры использования игровых декораторов ===\n")
    
    # Пример использования декоратора log_game_action
    print("--- Декоратор log_game_action ---")
    @log_game_action
    def cast_spell(character, spell_name, mana_cost):
        """Функция произнесения заклинания персонажем"""
        return f"{character} произносит заклинание {spell_name}"
    
    result = cast_spell("Герой", "Огненный шар", 20)
    print(f"Результат: {result}\n")
    
    # Пример использования декоратора timing_game_action
    print("--- Декоратор timing_game_action ---")
    @timing_game_action
    def cast_heavy_spell():
        """Функция, которая имитирует произнесение сложного заклинания"""
        import time
        time.sleep(0.5)
        return "Заклинание исцеления произнесено!"
    
    result = cast_heavy_spell()
    print(f"Результат: {result}\n")
    
    # Пример использования декоратора check_alive
    print("--- Декоратор check_alive ---")
    hero = Character("Герой", 50)
    enemy = Character("Враг", 30)
    
    print("Атака живого персонажа:")
    hero.attack(enemy, 10)
    print()
    
    print("Убиваем героя и пробуем снова атаковать:")
    hero.health = 0
    hero.attack(enemy, 10)
    print()
    
    # Пример использования декоратора log_action
    print("--- Декоратор log_action ---")
    mage = Mage("Маг", 30)
    result = mage.cast_fireball("Дракон")
    print(f"Результат: {result}\n")
    
    # Пример использования декоратора requires_mana
    print("--- Декоратор requires_mana ---")
    wizard = Wizard("Волшебник", 20)
    result = wizard.cast_lightning_bolt("Гоблин")
    print(f"Результат: {result}")
    
    result = wizard.cast_teleport()  # Не хватит маны
    print(f"Результат: {result}\n")
    
    # Пример использования декоратора conditional_effect
    print("--- Декоратор conditional_effect ---")
    enhanced_char = EnhancedCharacter("Эльф", 40)
    result = enhanced_char.attack(enemy, 15)
    print(f"Результат: {result}")
    
    enhanced_char.add_effect("stunned")
    result = enhanced_char.attack(enemy, 15)
    print(f"Результат: {result}\n")
    
    # Пример использования декоратора cached_property
    print("--- Декоратор cached_property ---")
    advanced_char = AdvancedCharacter("Рыцарь", 15, 12, 8)
    print(f"Сила: {advanced_char.strength}")
    print(f"Сила (второй вызов): {advanced_char.strength}")  # Не должно вычисляться снова
    
    advanced_char.add_buff("strength", 5)
    print(f"Сила после баффа: {advanced_char.strength}")  # Должно вычислиться снова
    print()
    
    # Пример использования декоратора limited_uses
    print("--- Декоратор limited_uses ---")
    paladin = Paladin("Святой")
    for i in range(4):
        result = paladin.cast_divine_shield()
        print(f"Попытка {i+1}: {result}")
    print()
    
    # Пример использования декоратора critical_hit
    print("--- Декоратор critical_hit ---")
    combat_char = CombatCharacter("Боец", 1)
    enemy2 = Character("Монстр", 100)
    
    for i in range(5):
        result = combat_char.special_attack(enemy2, 20)
        print(f"Атака {i+1}: {result}")
    print()
    
    # Пример использования декоратора game_mechanic
    print("--- Декоратор game_mechanic ---")
    entity = GameEntity("Тестовая сущность", 100, 50, 100)
    result = entity.divine_protection()
    print(f"Результат: {result}")
    print(f"Состояние сущности после использования: {entity}")
    print()
    
    print("Все игровые декораторы успешно реализованы и готовы к использованию!")