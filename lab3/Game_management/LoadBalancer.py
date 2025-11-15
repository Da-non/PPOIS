class LoadBalancer(GameEntity):
    """
    Класс балансировщика нагрузки для распределения игроков по серверам.

    Attributes:
        balancer_id (str): Уникальный идентификатор балансировщика
        strategy (str): Стратегия балансировки
        servers (Dict[str, GameServer]): Серверы под управлением
    """

    def __init__(self, balancer_id: str, strategy: str = "least_connections"):
        super().__init__(balancer_id, "LoadBalancer")
        self.strategy = strategy  # least_connections, round_robin, weighted, geographic
        self.servers = {}  # server_id -> GameServer
        self.server_weights = {}
        self.current_index = 0  # Для round_robin
        self.health_checks_enabled = True
        self.health_check_interval = 30.0  # секунды
        self.last_health_check = datetime.now()

    def update(self, delta_time: float) -> None:
        """Обновляет состояние балансировщика."""
        current_time = datetime.now()
        if (current_time - self.last_health_check).total_seconds() >= self.health_check_interval:
            self._perform_health_checks()
            self.last_health_check = current_time

    def add_server(self, server: GameServer, weight: int = 1) -> None:
        """Добавляет сервер в балансировщик."""
        self.servers[server.server_id] = server
        self.server_weights[server.server_id] = weight

    def remove_server(self, server_id: str) -> bool:
        """Удаляет сервер из балансировщика."""
        if server_id in self.servers:
            del self.servers[server_id]
            if server_id in self.server_weights:
                del self.server_weights[server_id]
            return True
        return False

    def get_best_server(self, player: Player) -> Optional[GameServer]:
        """Возвращает лучший сервер для игрока по выбранной стратегии."""
        available_servers = self._get_available_servers()
        if not available_servers:
            return None

        if self.strategy == "least_connections":
            return min(available_servers, key=lambda s: s.current_players)
        elif self.strategy == "round_robin":
            return self._get_round_robin_server(available_servers)
        elif self.strategy == "weighted":
            return self._get_weighted_server(available_servers)
        elif self.strategy == "geographic":
            return self._get_geographic_server(available_servers, player)
        else:
            return available_servers[0]  # По умолчанию первый доступный

    def _get_available_servers(self) -> List[GameServer]:
        """Возвращает список доступных серверов."""
        return [server for server in self.servers.values() 
                if server.status == "online" and server.current_players < server.max_players]

    def _get_round_robin_server(self, servers: List[GameServer]) -> GameServer:
        """Возвращает сервер по стратегии round-robin."""
        if not servers:
            return None
        
        server = servers[self.current_index % len(servers)]
        self.current_index = (self.current_index + 1) % len(servers)
        return server

    def _get_weighted_server(self, servers: List[GameServer]) -> Optional[GameServer]:
        """Возвращает сервер по взвешенной стратегии."""
        if not servers:
            return None
        
        total_weight = sum(self.server_weights.get(s.server_id, 1) for s in servers)
        random_value = random.uniform(0, total_weight)
        
        current_weight = 0
        for server in servers:
            weight = self.server_weights.get(server.server_id, 1)
            current_weight += weight
            if random_value <= current_weight:
                return server
        
        return servers[0]

    def _get_geographic_server(self, servers: List[GameServer], player: Player) -> Optional[GameServer]:
        """Возвращает сервер по географической близости."""
        # Упрощенная реализация - выбираем сервер в том же регионе, что и игрок
        player_region = getattr(player, 'region', 'unknown')
        regional_servers = [s for s in servers if s.region == player_region]
        
        if regional_servers:
            return min(regional_servers, key=lambda s: s.current_players)
        else:
            return min(servers, key=lambda s: s.current_players)

    def _perform_health_checks(self) -> None:
        """Выполняет проверки здоровья серверов."""
        for server in self.servers.values():
            if server.status == "online":
                # Проверяем производительность
                if (server.performance_metrics["cpu_usage"] > 90 or 
                    server.performance_metrics["memory_usage"] > 95):
                    server.status = "overloaded"

    def update_server_weight(self, server_id: str, new_weight: int) -> bool:
        """Обновляет вес сервера."""
        if server_id in self.server_weights:
            self.server_weights[server_id] = new_weight
            return True
        return False

    def get_balancer_stats(self) -> Dict[str, Any]:
        """Возвращает статистику балансировщика."""
        available_servers = self._get_available_servers()
        total_capacity = sum(s.max_players for s in self.servers.values())
        used_capacity = sum(s.current_players for s in self.servers.values())
        
        return {
            "total_servers": len(self.servers),
            "available_servers": len(available_servers),
            "total_capacity": total_capacity,
            "used_capacity": used_capacity,
            "utilization_rate": (used_capacity / total_capacity * 100) if total_capacity > 0 else 0,
            "strategy": self.strategy,
            "health_checks_enabled": self.health_checks_enabled
        }
