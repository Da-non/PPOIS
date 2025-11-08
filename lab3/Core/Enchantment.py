class Enchantment(GameEntity):
    """
    Класс зачарования.

    Attributes:
        enchantment_id (str): Уникальный идентификатор зачарования
        name (str): Название зачарования
        enchantment_type (str): Тип зачарования
        level (int): Уровень зачарования
        effects (List): Эффекты зачарования
    """

    def __init__(self, enchantment_id: str, name: str, enchantment_type: str, level: int = 1):
        super().__init__(enchantment_id, name)
        self.enchantment_type = enchantment_type
        self.level = level
        self.effects = []
        self.durability = 100.0
        self.max_durability = 100.0
        self.description = ""
        self.requirements = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние зачарования."""
        # Зачарования обычно не требуют обновления
        pass

    def add_effect(self, effect: ItemEffect) -> None:
        """Добавляет эффект к зачарованию."""
        self.effects.append(effect)

    def apply_to_item(self, item: GameItem) -> bool:
        """Применяет зачарование к предмету."""
        if len(item.enchantments) < 3:  # Максимум 3 зачарования
            item.enchantments.append(self)
            return True
        return False
