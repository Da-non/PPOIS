class HUD(GameEntity):
    """HUD, показывающий параметры игрока."""

    def __init__(self, hud_id: str, player: Player):
        super().__init__(hud_id, "HUD")
        self.player = player
        self.last_snapshot: Dict[str, Any] = {}
        self.visible: bool = True

    def update(self, delta_time: float) -> None:
        if not self.visible:
            return
        self.last_snapshot = {
            "health": self.player.health,
            "mana": self.player.mana,
            "stamina": self.player.stamina,
            "level": self.player.level,
        }

    def toggle(self) -> None:
        self.visible = not self.visible
