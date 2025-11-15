class Tooltip(GameEntity):
    """Подсказка для элементов интерфейса."""

    def __init__(self, tooltip_id: str, text: str):
        super().__init__(tooltip_id, "Tooltip")
        self.text = text
        self.visible = False
        self.anchor: Optional[str] = None

    

    def show(self, anchor_id: str) -> None:
        """Показывает подсказку, привязанную к конкретному элементу UI"""
        self.anchor = anchor_id
        self.visible = True

    def hide(self) -> None:
        """Полностью скрывает и сбрасывает подсказку"""
        self.visible = False
        self.anchor = None
