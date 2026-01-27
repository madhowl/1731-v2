# delegation_example.py

class BattleLogger:
    """Компонент для ведения боевого лога"""
    def __init__(self):
        self.logs = []

    def log_combat_action(self, actor, action, target=None):
        log_entry = f"{actor.name} {action}"
        if target:
            log_entry += f" -> {target.name}"
        self.logs.append(log_entry)
        print(f"[БОЙ] {log_entry}")

    def log_special_ability(self, actor, ability_name, target=None):
        log_entry = f"{actor.name} использует способность '{ability_name}'"
        if target:
            log_entry += f" на {target.name}"
        self.logs.append(log_entry)
        print(f"[СПОСОБНОСТЬ] {log_entry}")

    def get_battle_report(self):
        return "\n".join(self.logs)


class EffectManager:
    """Компонент для управления эффектами"""
    def __init__(self):
        self.active_effects = {}

    def apply_effect(self, target, effect_name, duration, magnitude):
        if target not in self.active_effects:
            self.active_effects[target] = {}
        
        self.active_effects[target][effect_name] = {
            'duration': duration,
            'magnitude': magnitude,
            'remaining': duration
        }
        print(f"Эффект '{effect_name}' применен к {target.name} на {duration} ходов (сила: {magnitude})")

    def update_effects(self):
        """Обновить все активные эффекты"""
        targets_to_remove = []
        for target, effects in self.active_effects.items():
            effects_to_remove = []
            for effect_name, effect_data in effects.items():
                effect_data['remaining'] -= 1
                if effect_data['remaining'] <= 0:
                    effects_to_remove.append(effect_name)
                    print(f"Эффект '{effect_name}' закончился для {target.name}")
            
            for effect_name in effects_to_remove:
                del effects[effect_name]
            
            if not effects:
                targets_to_remove.append(target)
        
        for target in targets_to_remove:
            del self.active_effects[target]

    def get_effect_modifier(self, target, effect_type):
        """Получить модификатор от эффектов определенного типа"""
        modifier = 0
        if target in self.active_effects:
            for effect_name, effect_data in self.active_effects[target].items():
                if effect_type in effect_name.lower():
                    modifier += effect_data['magnitude']
        return modifier


class Character:
    """Базовый класс персонажа с делегированием"""
    def __init__(self, name, char_class="Воин"):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        
        # Компоненты, которым делегируется выполнение специфической логики
        self.logger = BattleLogger()
        self.effects = EffectManager()

    def delegate_log_combat_action(self, action, target=None):
        """Делегировать логирование боевого действия"""
        self.logger.log_combat_action(self, action, target)

    def delegate_log_special_ability(self, ability_name, target=None):
        """Делегировать логирование специальной способности"""
        self.logger.log_special_ability(self, ability_name, target)

    def delegate_apply_effect(self, target, effect_name, duration, magnitude):
        """Делегировать применение эффекта"""
        self.effects.apply_effect(target, effect_name, duration, magnitude)

    def delegate_update_effects(self):
        """Делегировать обновление эффектов"""
        self.effects.update_effects()

    def delegate_get_effect_modifier(self, effect_type):
        """Делегировать получение модификатора эффекта"""
        return self.effects.get_effect_modifier(self, effect_type)

    def attack(self, target):
        """Атака с делегированием логирования"""
        damage = 10 + self.delegate_get_effect_modifier("power")
        self.delegate_log_combat_action(f"атакует на {damage} урона", target)
        target.take_damage(damage)
        return damage

    def take_damage(self, damage):
        """Получение урона"""
        actual_damage = max(1, damage - self.delegate_get_effect_modifier("protection"))
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage

    def is_alive(self):
        """Проверка, жив ли персонаж"""
        return self.health > 0

    def __str__(self):
        return f"{self.name} ({self.char_class}): Здоровье {self.health}/{self.max_health}, Мана {self.mana}/{self.max_mana}"


class Warrior(Character):
    """Класс воина с делегированием специфичной логики"""
    def __init__(self, name):
        super().__init__(name, "Воин")
        self.rage = 0
        self.max_rage = 100

    def special_attack(self, target):
        """Специальная атака с делегированием"""
        if self.rage >= 30:
            self.rage -= 30
            bonus_damage = 15 + self.delegate_get_effect_modifier("rage")
            damage = 20 + bonus_damage
            self.delegate_log_special_ability("Яростная атака", target)
            self.delegate_log_combat_action(f"наносит {damage} урона", target)
            target.take_damage(damage)
            return damage
        else:
            print(f"{self.name} недостаточно ярости для специальной атаки")
            return 0

    def battle_cry(self, allies):
        """Боевой клич, усиливающий союзников"""
        self.delegate_log_special_ability("Боевой клич")
        for ally in allies:
            self.delegate_apply_effect(ally, "боевой дух", 3, 5)
            print(f"{ally.name} воодушевлен боевым кличем!")

    def take_damage(self, damage):
        """Переопределение получения урона с делегированием"""
        # Воин может использовать ярость для снижения урона
        rage_protection = min(self.rage, damage // 2)
        self.rage -= rage_protection
        damage -= rage_protection
        
        actual_damage = max(1, damage - self.delegate_get_effect_modifier("protection"))
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
            
        # Получение ярости при получении урона
        self.rage = min(self.max_rage, self.rage + actual_damage)
        
        return actual_damage


class Mage(Character):
    """Класс мага с делегированием специфичной логики"""
    def __init__(self, name):
        super().__init__(name, "Маг")
        self.mana_cost_multiplier = 1.0

    def cast_spell(self, spell_name, target=None):
        """Произнесение заклинания с делегированием"""
        base_mana_cost = 10
        mana_cost = int(base_mana_cost * self.mana_cost_multiplier)
        
        if self.mana >= mana_cost:
            self.mana -= mana_cost
            self.delegate_log_special_ability(f"произносит '{spell_name}'", target)
            
            if spell_name.lower() == "огненный шар":
                damage = 25 + self.delegate_get_effect_modifier("fire")
                if target:
                    target.take_damage(damage)
                    print(f"{target.name} получает {damage} огненного урона")
                return damage
            elif spell_name.lower() == "лечение":
                heal_amount = 30 + self.delegate_get_effect_modifier("heal")
                if target:
                    target.health = min(target.max_health, target.health + heal_amount)
                    print(f"{target.name} восстанавливает {heal_amount} здоровья")
                return heal_amount
            else:
                print(f"Неизвестное заклинание: {spell_name}")
                return 0
        else:
            print(f"{self.name} недостаточно маны для заклинания")
            return 0

    def take_damage(self, damage):
        """Переопределение получения урона с делегированием"""
        actual_damage = max(1, damage - self.delegate_get_effect_modifier("magic_resist"))
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage


# Пример использования делегирования
print("=== Демонстрация делегирования в игровом программировании ===")

warrior = Warrior("Конан")
mage = Mage("Мерлин")
enemy = Character("Гоблин")

print(f"Состояние персонажей:")
print(warrior)
print(mage)
print(enemy)

print(f"\n--- Боевая сцена ---")

# Атака с делегированием логирования
warrior.attack(enemy)

# Применение эффекта с делегированием
warrior.delegate_apply_effect(mage, "огненная мощь", 3, 10)

# Специальная атака воина
warrior.rage = 50  # Искусственно увеличиваем ярость
warrior.special_attack(enemy)

# Заклинание мага
mage.cast_spell("огненный шар", enemy)

# Боевой клич воина
warrior.battle_cry([mage])

# Обновление эффектов с делегированием
warrior.delegate_update_effects()

print(f"\nСостояние после боя:")
print(warrior)
print(mage)
print(enemy)

print(f"\n--- Боевой отчет ---")
print(warrior.logger.get_battle_report())


# Дополнительный пример с использованием __getattr__ для делегирования
class InventoryManager:
    """Класс управления инвентарем"""
    def __init__(self):
        self.items = []
        self.capacity = 10
        self.logger = BattleLogger()

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            self.logger.log_combat_action(f"добавил предмет '{item.name}' в инвентарь")
            return True
        else:
            print("Инвентарь полон!")
            return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.logger.log_combat_action(f"удалил предмет '{item.name}' из инвентаря")
            return True
        return False

    def get_item_count(self):
        return len(self.items)

    def get_total_weight(self):
        return sum(getattr(item, 'weight', 0) for item in self.items)

    def use_item(self, item_name, target):
        for item in self.items:
            if item.name == item_name:
                if hasattr(item, 'use'):
                    return item.use(target)
                else:
                    print(f"Предмет '{item_name}' нельзя использовать")
                    return False
        print(f"Предмет '{item_name}' не найден")
        return False


class Item:
    """Класс предмета"""
    def __init__(self, name, item_type="обычный", weight=1.0):
        self.name = name
        self.item_type = item_type
        self.weight = weight

    def __str__(self):
        return f"{self.name} ({self.item_type}), вес: {self.weight}"


class Consumable(Item):
    """Класс расходуемого предмета"""
    def __init__(self, name, effect_type, effect_value, weight=0.5):
        super().__init__(name, "расходуемый", weight)
        self.effect_type = effect_type
        self.effect_value = effect_value

    def use(self, target):
        if self.effect_type == "heal":
            target.health = min(target.max_health, target.health + self.effect_value)
            print(f"{target.name} восстановил {self.effect_value} здоровья")
        elif self.effect_type == "mana":
            target.mana = min(target.max_mana, target.mana + self.effect_value)
            print(f"{target.name} восстановил {self.effect_value} маны")
        return True


class Equipable(Item):
    """Класс экипируемого предмета"""
    def __init__(self, name, stat_bonus_type, stat_bonus_value, weight=2.0):
        super().__init__(name, "экипировка", weight)
        self.stat_bonus_type = stat_bonus_type
        self.stat_bonus_value = stat_bonus_value

    def equip(self, character):
        print(f"{character.name} экипировал {self.name}, получив +{self.stat_bonus_value} к {self.stat_bonus_type}")


class SmartCharacter:
    """Класс персонажа с делегированием через __getattr__"""
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        
        # Компонент инвентаря, которому будут делегированы некоторые методы
        self.inventory_manager = InventoryManager()

    def __getattr__(self, name):
        """
        Автоматически делегировать неопределенные атрибуты/методы 
        компоненту управления инвентарем
        """
        if hasattr(self.inventory_manager, name):
            attr = getattr(self.inventory_manager, name)
            if callable(attr):
                # Если это метод, вызвать его
                return attr
            else:
                # Если это атрибут, вернуть его значение
                return attr
        else:
            # Если атрибут не найден ни у персонажа, ни у компонента
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __str__(self):
        return f"{self.name}: Здоровье {self.health}/{self.max_health}, Мана {self.mana}/{self.max_mana}, Инвентарь: {self.get_item_count()}/{self.capacity}"


# Пример использования делегирования через __getattr__
print("\n=== Демонстрация делегирования через __getattr__ ===")

player = SmartCharacter("Артур")
print(player)

# Создание предметов
health_potion = Consumable("Зелье здоровья", "heal", 30)
mana_potion = Consumable("Зелье маны", "mana", 25)
strength_gloves = Equipable("Перчатки силы", "сила", 5)

# Добавление предметов в инвентарь (метод делегируется из inventory_manager)
player.add_item(health_potion)
player.add_item(mana_potion)
player.add_item(strength_gloves)

print(f"\nПосле добавления предметов: {player}")
print(f"Общий вес инвентаря: {player.get_total_weight()}")

# Использование предмета (метод делегируется из inventory_manager)
print(f"\nИспользование зелья здоровья:")
player.use_item("Зелье здоровья", player)
print(f"Состояние после использования: {player}")

# Получение количества предметов (метод делегируется из inventory_manager)
print(f"\nКоличество предметов в инвентаре: {player.get_item_count()}")