class Ability(GameEntity):
    """
    Класс способности.

    Attributes:
        ability_id (str): Уникальный идентификатор способности
        name (str): Название способности
        ability_type (str): Тип способности
        cooldown (float): Время перезарядки
        mana_cost (float): Стоимость маны
    """

    def __init__(self, ability_id: str, name: str, ability_type: str):
        super().__init__(ability_id, name)
        self.ability_id = ability_id  # алиас для entity_id
        self.ability_type = ability_type
        self.cooldown = 0.0
        self.cooldown_remaining = 0.0
        self.mana_cost = 0.0
        self.range = 0.0
        self.damage = 0.0
        self.healing = 0.0
        self.duration = 0.0
        self.description = ""
        self.effects = []
        self.requirements = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние способности."""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0, self.cooldown_remaining - delta_time)

    def activate(self, caster: Player, target: Optional[GameEntity] = None) -> bool:
        """Активирует способность."""
        if self.cooldown_remaining > 0:
            return False
        
        if not caster.use_mana(self.mana_cost):
            return False
        
        # Применяем эффекты способности
        for effect in self.effects:
            effect.apply(caster, target)
        
        self.cooldown_remaining = self.cooldown
        return True

    def add_effect(self, effect: 'AbilityEffect') -> None:
        """Добавляет эффект к способности."""
        self.effects.append(effect)
