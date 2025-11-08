class AbilityEffect(GameEntity):
    """
    Класс эффекта способности.

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

    def update(self, delta_time: float) -> None:
        """Обновляет состояние эффекта."""
        if not self.is_permanent:
            self.remaining_time = max(0, self.remaining_time - delta_time)

    def apply(self, caster: Player, target: Optional[GameEntity] = None) -> None:
        """Применяет эффект к цели."""
        if self.effect_type == "damage":
            if target and hasattr(target, 'take_damage'):
                damage = self.value + caster.calculate_damage(0)
                target.take_damage(damage)
        elif self.effect_type == "healing":
            if target and hasattr(target, 'heal'):
                healing = self.value + caster.calculate_damage(0) * 0.5
                target.heal(healing)
        elif self.effect_type == "teleport":
            if target and hasattr(target, 'position'):
                # Телепортация (упрощенная)
                target.position = (0, 0, 0)  # Новая позиция

    def is_expired(self) -> bool:
        """Проверяет, истек ли эффект."""
        return not self.is_permanent and self.remaining_time <= 0
