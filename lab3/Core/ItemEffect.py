class ItemEffect(GameEntity):
    """
    Класс эффекта предмета.

    Attributes:
        effect_id (str): Уникальный идентификатор эффекта
        name (str): Название эффекта
        effect_type (str): Тип эффекта
        value (float): Значение эффекта
        duration (float): Продолжительность эффекта
    """

    def __init__(self, effect_id: str, name: str, effect_type: str, value: float, duration: float = 0.0):
        super().__init__(effect_id, name)
        self.effect_type = effect_type
        self.value = value
        self.duration = duration
        self.remaining_time = duration
        self.is_permanent = duration <= 0
        self.stacks = 1
        self.max_stacks = 1

    def update(self, delta_time: float) -> None:
        """Обновляет состояние эффекта."""
        if not self.is_permanent:
            self.remaining_time = max(0, self.remaining_time - delta_time)

    def apply(self, target: GameEntity) -> None:
        """Применяет эффект к цели."""
        if self.effect_type == "damage":
            if hasattr(target, 'take_damage'):
                target.take_damage(self.value)
        elif self.effect_type == "healing":
            if hasattr(target, 'heal'):
                target.heal(self.value)
        elif self.effect_type == "stat_boost":
            if hasattr(target, 'stats'):
                stat_name = self.name.lower().replace(" ", "_")
                if stat_name in target.stats:
                    target.stats[stat_name] += self.value

    def is_expired(self) -> bool:
        """Проверяет, истек ли эффект."""
        return not self.is_permanent and self.remaining_time <= 0
