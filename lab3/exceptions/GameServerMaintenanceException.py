class GameServerMaintenanceException(GameDevelopmentBaseException):
    """Исключение при попытке доступа во время технического обслуживания сервера."""
    def __init__(self, server_id, maintenance_end_time):
        self.server_id = server_id
        self.maintenance_end_time = maintenance_end_time
        super().__init__(f"Сервер {server_id} на техническом обслуживании до {maintenance_end_time}")
