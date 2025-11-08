class UnauthorizedGameActionException(GameDevelopmentBaseException):
    """Исключение при попытке неавторизованного игрового действия."""
    def __init__(self, action_name, required_level, player_level):
        self.action_name = action_name
        self.required_level = required_level
        self.player_level = player_level
        super().__init__(f"Недостаточный уровень для действия {action_name}: требуется {required_level}, у игрока {player_level}")
