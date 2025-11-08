class InvalidGameStateException(GameDevelopmentBaseException):
    """Исключение при недопустимом состоянии игры."""
    def __init__(self, current_state, required_state):
        self.current_state = current_state
        self.required_state = required_state
        super().__init__(f"Недопустимое состояние игры: текущее {current_state}, требуется {required_state}")
