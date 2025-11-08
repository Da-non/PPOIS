class GameItem(GameEntity):
    """
    Класс игрового предмета.

    Attributes:
        item_id (str): Уникальный идентификатор предмета
        name (str): Название предмета
        item_type (str): Тип предмета
        rarity (str): Редкость предмета
        value (int): Стоимость предмета
        required_level (int): Требуемый уровень
        required_class (str): Требуемый класс
    """

    def __init__(self, item_id: str, name: str, item_type: str, rarity: str = "common"):
        super().__init__(item_id, name)
        self.item_type = item_type
        self.rarity = rarity
        self.value = random.randint(10, 1000)
        self.required_level = 1
        self.required_class = None
        self.weight = random.uniform(0.1, 10.0)
        self.stats = {}
        self.durability = 100.0
        self.max_durability = 100.0
        self.stack_size = 1
        self.current_stack = 1
        self.description = ""
        self.effects = []
        self.socket_count = 0
        self.sockets = []
        self.enchantments = []
        self.bound_to_player = None
        self.tradeable = True
        self.sellable = True

    def update(self, delta_time: float) -> None:
        """Обновляет состояние предмета."""
        # Предметы обычно не требуют обновления
        pass

    def add_stat(self, stat_name: str, value: float) -> None:
        """Добавляет характеристику к предмету."""
        self.stats[stat_name] = value

    def add_effect(self, effect: 'ItemEffect') -> None:
        """Добавляет эффект к предмету."""
        self.effects.append(effect)

    def add_enchantment(self, enchantment: 'Enchantment') -> None:
        """Добавляет зачарование к предмету."""
        if len(self.enchantments) < 3:  # Максимум 3 зачарования
            self.enchantments.append(enchantment)

    def repair(self, amount: float) -> None:
        """Ремонтирует предмет."""
        self.durability = min(self.max_durability, self.durability + amount)

    def damage(self, amount: float) -> None:
        """Повреждает предмет."""
        self.durability = max(0, self.durability - amount)

    def is_broken(self) -> bool:
        """Проверяет, сломан ли предмет."""
        return self.durability <= 0

    def bind_to_player(self, player_id: str) -> None:
        """Привязывает предмет к игроку."""
        self.bound_to_player = player_id
        self.tradeable = False

    def can_stack_with(self, other_item: 'GameItem') -> bool:
        """Проверяет, можно ли складывать предметы."""
        return (self.entity_id == other_item.entity_id and 
                self.current_stack < self.stack_size and
                other_item.current_stack < other_item.stack_size)

    def stack_with(self, other_item: 'GameItem') -> int:
        """Складывает предметы."""
        if not self.can_stack_with(other_item):
            return 0
        
        transfer_amount = min(other_item.current_stack, 
                            self.stack_size - self.current_stack)
        self.current_stack += transfer_amount
        other_item.current_stack -= transfer_amount
        return transfer_amount


