"""
Пример: Полиморфизм в игровых персонажах
"""

class Character:
    """Базовый класс персонажа"""
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.max_health = health

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def special_ability(self):
        """Абстрактный метод специальной способности"""
        raise NotImplementedError("Каждый персонаж должен реализовать свою специальную способность")


class Warrior(Character):
    """Класс воина"""
    def __init__(self, name, weapon="Меч"):
        super().__init__(name, health=150)
        self.weapon = weapon

    def special_ability(self):
        """Специальная способность воина - яростная атака"""
        return f"{self.name} использует яростную атаку с {self.weapon}!"


class Mage(Character):
    """Класс мага"""
    def __init__(self, name, spell="Огненный шар"):
        super().__init__(name, health=80)
        self.spell = spell
        self.mana = 100
        self.max_mana = 100

    def special_ability(self):
        """Специальная способность мага - заклинание"""
        if self.mana >= 20:
            self.mana -= 20
            return f"{self.name} произносит заклинание '{self.spell}'! Осталось маны: {self.mana}"
        else:
            return f"{self.name} не хватает маны для заклинания"


class Archer(Character):
    """Класс лучника"""
    def __init__(self, name, bow="Длинный лук"):
        super().__init__(name, health=100)
        self.bow = bow
        self.arrows = 20

    def special_ability(self):
        """Специальная способность лучника - меткий выстрел"""
        if self.arrows > 0:
            self.arrows -= 1
            return f"{self.name} делает меткий выстрел из {self.bow}! Осталось стрел: {self.arrows}"
        else:
            return f"{self.name} закончились стрелы!"


class Healer(Character):
    """Класс целителя"""
    def __init__(self, name, healing_spell="Лечение"):
        super().__init__(name, health=90)
        self.healing_spell = healing_spell
        self.mana = 120
        self.max_mana = 120

    def special_ability(self):
        """Специальная способность целителя - лечение"""
        if self.mana >= 15:
            self.mana -= 15
            return f"{self.name} применяет '{self.healing_spell}'! Осталось маны: {self.mana}"
        else:
            return f"{self.name} не хватает маны для лечения"


class BattleSystem:
    """Система боя, использующая полиморфизм"""
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        """Добавить персонажа в бой"""
        self.characters.append(character)

    def battle_round(self):
        """Выполнить раунд боя"""
        print("=== Раунд боя начат ===")
        for character in self.characters:
            if character.is_alive():
                # Каждый персонаж использует свою специальную способность
                # благодаря полиморфизму - вызываем одинаковый метод, получаем разные результаты
                ability_result = character.special_ability()
                print(ability_result)
            else:
                print(f"{character.name} мертв и пропускает ход")
        print("=== Раунд боя завершен ===\n")


def demonstrate_polymorphism():
    """Демонстрация полиморфизма"""
    print("=== Демонстрация полиморфизма ===")
    
    # Полиморфное использование - все персонажи вызывают один и тот же метод, но по-разному
    characters = [
        Warrior("Артур"),
        Mage("Мерлин"),
        Archer("Робин"),
        Healer("Эльза")
    ]

    print("Демонстрация полиморфизма:")
    for char in characters:
        print(char.special_ability())
        print(f"Здоровье {char.name}: {char.health}/{char.max_health}")
        print("-" * 40)


def demonstrate_battle_system():
    """Демонстрация боевой системы с использованием полиморфизма"""
    print("\n=== Демонстрация боевой системы ===")
    
    # Создаем боевую систему и добавляем персонажей
    battle = BattleSystem()

    warrior = Warrior("Конан")
    mage = Mage("Гэндальф")
    archer = Archer("Леголас")
    healer = Healer("Ариэль")

    battle.add_character(warrior)
    battle.add_character(mage)
    battle.add_character(archer)
    battle.add_character(healer)

    # Выполняем несколько раундов боя
    for round_num in range(3):
        print(f"РАУНД {round_num + 1}")
        battle.battle_round()


if __name__ == "__main__":
    demonstrate_polymorphism()
    demonstrate_battle_system()