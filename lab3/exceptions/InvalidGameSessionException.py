class InvalidGameSessionException(GameDevelopmentBaseException):
    """Исключение при неверной игровой сессии."""
    def __init__(self, session_id):
        self.session_id = session_id
        super().__init__(f"Неверная игровая сессия {session_id}")
