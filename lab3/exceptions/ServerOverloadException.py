class ServerOverloadException(GameDevelopmentBaseException):
    """Исключение при перегрузке игрового сервера."""
    def __init__(self, server_id, current_load, max_capacity):
        self.server_id = server_id
        self.current_load = current_load
        self.max_capacity = max_capacity
        super().__init__(f"Сервер {server_id} перегружен: нагрузка {current_load}%, максимум {max_capacity}%")
