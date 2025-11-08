class PlayerNotFoundException(GameDevelopmentBaseException):
    """Исключение при попытке найти несуществующего игрока."""
    def __init__(self, player_id):
        self.player_id = player_id
        super().__init__(f"Игрок с ID {player_id} не найден")
