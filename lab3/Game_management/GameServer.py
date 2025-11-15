class GameServer(GameEntity):
    """
    Класс игрового сервера.

    Attributes:
        server_id (str): Уникальный идентификатор сервера
        name (str): Название сервера
        server_type (str): Тип сервера
        max_players (int): Максимальное количество игроков
        current_players (int): Текущее количество игроков
        status (str): Статус сервера
    """

    def __init__(self, server_id: str, name: str, server_type: str = "game"):
        super().__init__(server_id, name)
        self.server_id = server_id  # алиас для entity_id
        self.server_type = server_type
        self.max_players = 1000
        self.current_players = 0
        self.status = "offline"  # offline, online, maintenance, full
        self.region = "unknown"
        self.ip_address = ""
        self.port = 0
        self.version = "1.0.0"
        self.uptime = 0.0
        self.last_restart = datetime.now()
        self.performance_metrics = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "network_latency": 0.0,
            "tick_rate": 60.0
        }
        self.connected_players = []
        self.active_sessions = []
        self.server_rules = {}
        self.maintenance_schedule = []
        self.backup_schedule = []

    def update(self, delta_time: float) -> None:
        """Обновляет состояние сервера."""
        if self.status == "online":
            self.uptime += delta_time
            self._update_performance_metrics()
            self._check_server_health()

    def start_server(self) -> bool:
        """Запускает сервер."""
        if self.status == "offline":
            self.status = "online"
            self.last_restart = datetime.now()
            self.uptime = 0.0
            return True
        return False

    def stop_server(self) -> bool:
        """Останавливает сервер."""
        if self.status == "online":
            self.status = "offline"
            self.connected_players.clear()
            self.active_sessions.clear()
            return True
        return False

    def restart_server(self) -> bool:
        """Перезапускает сервер."""
        if self.stop_server():
            return self.start_server()
        return False

    def enter_maintenance_mode(self, duration_hours: int = 2) -> bool:
        """Включает режим технического обслуживания."""
        if self.status == "online":
            self.status = "maintenance"
            self.maintenance_schedule.append({
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(hours=duration_hours),
                "reason": "scheduled_maintenance"
            })
            return True
        return False

    def exit_maintenance_mode(self) -> bool:
        """Выключает режим технического обслуживания."""
        if self.status == "maintenance":
            self.status = "online"
            return True
        return False

    def add_player(self, player: Player) -> bool:
        """Добавляет игрока на сервер."""
        if self.status != "online":
            raise GameServerMaintenanceException(self.entity_id, datetime.now() + timedelta(hours=2))
        
        if self.current_players >= self.max_players:
            raise ServerOverloadException(self.entity_id, self.current_players, self.max_players)
        
        if player not in self.connected_players:
            self.connected_players.append(player)
            self.current_players = len(self.connected_players)
            return True
        return False

    def remove_player(self, player: Player) -> bool:
        """Удаляет игрока с сервера."""
        if player in self.connected_players:
            self.connected_players.remove(player)
            self.current_players = len(self.connected_players)
            return True
        return False

    def get_server_load(self) -> float:
        """Возвращает загрузку сервера."""
        return (self.current_players / self.max_players) * 100

    def _update_performance_metrics(self) -> None:
        """Обновляет метрики производительности."""
        self.performance_metrics["cpu_usage"] = random.uniform(10, 80)
        self.performance_metrics["memory_usage"] = random.uniform(20, 90)
        self.performance_metrics["network_latency"] = random.uniform(10, 100)
        self.performance_metrics["tick_rate"] = random.uniform(55, 65)

    def _check_server_health(self) -> None:
        """Проверяет здоровье сервера."""
        if self.performance_metrics["cpu_usage"] > 90:
            self.status = "overloaded"
        elif self.performance_metrics["memory_usage"] > 95:
            self.status = "overloaded"
        elif self.current_players >= self.max_players:
            self.status = "full"

