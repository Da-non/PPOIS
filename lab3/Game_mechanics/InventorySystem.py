class InventorySystem:
    """
    Система инвентаря.

    Attributes:
        inventory_id (str): Уникальный идентификатор инвентаря
        owner (Player): Владелец инвентаря
        items (List[GameItem]): Предметы в инвентаре
        max_slots (int): Максимальное количество слотов
        weight_limit (float): Лимит веса
    """

    def __init__(self, inventory_id: str, owner: Player, max_slots: int = 50, weight_limit: float = 1000.0):
        self.inventory_id = inventory_id
        self.owner = owner
        self.items = []
        self.max_slots = max_slots
        self.weight_limit = weight_limit
        self.current_weight = 0.0
        self.special_slots = {}  # Специальные слоты (оружие, броня и т.д.)

    def add_item(self, item: GameItem, slot: Optional[int] = None) -> bool:
        """Добавляет предмет в инвентарь."""
        if len(self.items) >= self.max_slots:
            return False
        
        if self.current_weight + item.weight > self.weight_limit:
            return False
        
        if slot is not None and 0 <= slot < self.max_slots:
            if slot < len(self.items) and self.items[slot] is None:
                self.items[slot] = item
            else:
                return False
        else:
            self.items.append(item)
        
        self.current_weight += item.weight
        return True

    def remove_item(self, item: GameItem) -> bool:
        """Удаляет предмет из инвентаря."""
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.weight
            return True
        return False

    def get_item_by_id(self, item_id: str) -> Optional[GameItem]:
        """Возвращает предмет по ID."""
        for item in self.items:
            if item and item.entity_id == item_id:
                return item
        return None

    def get_items_by_type(self, item_type: str) -> List[GameItem]:
        """Возвращает предметы по типу."""
        return [item for item in self.items if item and item.item_type == item_type]

    def sort_inventory(self, sort_by: str = "name") -> None:
        """Сортирует инвентарь."""
        if sort_by == "name":
            self.items.sort(key=lambda x: x.name if x else "")
        elif sort_by == "type":
            self.items.sort(key=lambda x: x.item_type if x else "")
        elif sort_by == "value":
            self.items.sort(key=lambda x: x.value if x else 0, reverse=True)

    def get_inventory_weight(self) -> float:
        """Возвращает текущий вес инвентаря."""
        return sum(item.weight for item in self.items if item)

    def can_fit_item(self, item: GameItem) -> bool:
        """Проверяет, поместится ли предмет в инвентарь."""
        return (len(self.items) < self.max_slots and 
                self.current_weight + item.weight <= self.weight_limit)

