class GameModerationException(GameDevelopmentBaseException):
    """Исключение при нарушении правил игры."""
    def __init__(self, player_id, violation_type, severity):
        self.player_id = player_id
        self.violation_type = violation_type
        self.severity = severity
        super().__init__(f"Нарушение правил игроком {player_id}: {violation_type} (серьезность: {severity})")
