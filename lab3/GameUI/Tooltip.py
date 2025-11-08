class Tooltip(GameEntity):
    """Подсказка для элементов интерфейса."""

    def __init__(self, tooltip_id: str, text: str):
        super().__init__(tooltip_id, "Tooltip")
        self.text = text
        self.visible = False
        self.anchor: Optional[str] = None

    def update(self, delta_time: float) -> None:
        # Нет динамики по умолчанию
        pass

    def show(self, anchor_id: str) -> None:
        self.anchor = anchor_id
        self.visible = True

    def hide(self) -> None:
        self.visible = False
        self.anchor = None
