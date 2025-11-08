class Character(Player):
    """
    Класс игрового персонажа.

    Attributes:
        character_id (str): Уникальный идентификатор персонажа
        character_class (str): Класс персонажа
        character_race (str): Раса персонажа
        stats (Dict): Характеристики персонажа
        abilities (List): Способности персонажа
    """

    def __init__(self, character_id: str, name: str, character_class: str, character_race: str):
        super().__init__(character_id, name, "")
        self.character_class = character_class
        self.character_race = character_race
        self.stats = {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "constitution": 10,
            "charisma": 10,
            "wisdom": 10
        }
        self.abilities = []
        self.specializations = []
        self.talents = []
        self.mounts = []
        self.pets = []
        self.title = ""
        self.gender = "unknown"
        self.age = 0
        self.birth_place = ""
        self.alignment = "neutral"

    def update(self, delta_time: float) -> None:
        """Обновляет состояние персонажа."""
        super().update(delta_time)
        
        # Восстановление способностей
        for ability in self.abilities:
            if hasattr(ability, 'cooldown_remaining'):
                ability.cooldown_remaining = max(0, ability.cooldown_remaining - delta_time)

    def level_up_stats(self) -> None:
        """Увеличивает характеристики при повышении уровня."""
        stat_points = 5  # Очки характеристик за уровень
        
        # Распределяем очки случайно
        for _ in range(stat_points):
            stat = random.choice(list(self.stats.keys()))
            self.stats[stat] += 1

    def add_ability(self, ability: 'Ability') -> bool:
        """Добавляет способность."""
        if ability not in self.abilities:
            self.abilities.append(ability)
            return True
        return False

    def use_ability(self, ability_name: str, target: Optional['GameEntity'] = None) -> bool:
        """Использует способность."""
        for ability in self.abilities:
            if ability.name == ability_name:
                if hasattr(ability, 'cooldown_remaining') and ability.cooldown_remaining > 0:
                    return False
                
                if ability.activate(self, target):
                    if hasattr(ability, 'cooldown'):
                        ability.cooldown_remaining = ability.cooldown
                    return True
        return False

    def calculate_damage(self, base_damage: float) -> float:
        """Вычисляет урон на основе характеристик."""
        strength_bonus = self.stats["strength"] * 0.1
        return base_damage + strength_bonus

    def calculate_armor(self) -> float:
        """Вычисляет защиту на основе характеристик."""
        constitution_bonus = self.stats["constitution"] * 0.2
        return constitution_bonus

