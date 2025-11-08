class Menu(GameEntity):
    """Простое меню с пунктами и обработчиками."""

    def __init__(self, menu_id: str, name: str):
        super().__init__(menu_id, name)
        self.items: Dict[str, Any] = {}
        self.visible: bool = False

    def update(self, delta_time: float) -> None:
        # Меню не требует обновлений по времени
        pass

    def add_item(self, key: str, callback: Any) -> None:
        self.items[key] = callback

    def remove_item(self, key: str) -> bool:
        return self.items.pop(key, None) is not None

    def trigger(self, key: str) -> bool:
        cb = self.items.get(key)
        if cb:
            cb()
            return True
        return False
