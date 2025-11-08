class Skill(GameEntity):
    """
    Класс навыка.

    Attributes:
        skill_id (str): Уникальный идентификатор навыка
        name (str): Название навыка
        skill_type (str): Тип навыка
        level (int): Уровень навыка
        experience (int): Опыт навыка
        required_level (int): Требуемый уровень игрока
    """

    def __init__(self, skill_id: str, name: str, skill_type: str, required_level: int = 1):
        super().__init__(skill_id, name)
        self.skill_id = skill_id  # алиас для entity_id
        self.skill_type = skill_type
        self.level = 1
        self.experience = 0
        self.required_level = required_level
        self.max_level = 100
        self.mana_cost = 0
        self.cooldown = 0.0
        self.range = 0.0
        self.damage = 0.0
        self.healing = 0.0
        self.duration = 0.0
        self.description = ""
        self.effects = []
        self.requirements = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние навыка."""
        # Навыки обычно не требуют обновления
        pass

    def gain_experience(self, amount: int) -> bool:
        """Получает опыт навыка."""
        self.experience += amount
        old_level = self.level
        
        # Проверяем повышение уровня навыка
        required_exp = self.level * 100
        while self.experience >= required_exp and self.level < self.max_level:
            self.level += 1
            self.experience -= required_exp
            required_exp = self.level * 100
        
        return self.level > old_level

    def activate(self, caster: Player, target: Optional[GameEntity] = None) -> bool:
        """Активирует навык."""
        if not caster.use_mana(self.mana_cost):
            return False
        
        # Применяем эффекты навыка
        for effect in self.effects:
            effect.apply(caster, target)
        
        return True

    def add_effect(self, effect: 'SkillEffect') -> None:
        """Добавляет эффект к навыку."""
        self.effects.append(effect)
