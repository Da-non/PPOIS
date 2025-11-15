class ServerCluster(GameEntity):
    """
    Класс кластера серверов для управления группой серверов.

    Attributes:
        cluster_id (str): Уникальный идентификатор кластера
        name (str): Название кластера
        region (str): Регион кластера
        servers (List[GameServer]): Серверы в кластере
        load_balancer (LoadBalancer): Балансировщик нагрузки
    """

    def __init__(self, cluster_id: str, name: str, region: str):
        super().__init__(cluster_id, name)
        self.region = region
        self.servers = []
        self.load_balancer = LoadBalancer(f"LB_{cluster_id}")
        self.max_servers = 10
        self.auto_scaling_enabled = True
        self.scaling_threshold = 80.0  # Процент загрузки для масштабирования
        self.maintenance_mode = False
        self.performance_metrics = {
            "total_players": 0,
            "average_load": 0.0,
            "health_status": "healthy"
        }
        self.backup_servers = []
        self.failover_enabled = True

    def update(self, delta_time: float) -> None:
        """Обновляет состояние кластера."""
        self._update_performance_metrics()
        self._check_auto_scaling()
        self._monitor_servers_health()

    def add_server(self, server: GameServer) -> bool:
        """Добавляет сервер в кластер."""
        if len(self.servers) < self.max_servers and server.region == self.region:
            self.servers.append(server)
            self.load_balancer.add_server(server)
            return True
        return False

    def remove_server(self, server_id: str) -> bool:
        """Удаляет сервер из кластера."""
        for server in self.servers:
            if server.server_id == server_id:
                self.servers.remove(server)
                self.load_balancer.remove_server(server_id)
                return True
        return False

    def distribute_player(self, player: Player) -> Optional[GameServer]:
        """Распределяет игрока на сервер с наименьшей нагрузкой."""
        if self.maintenance_mode:
            return None
        
        return self.load_balancer.get_best_server(player)

    def start_maintenance(self, duration_hours: int = 2) -> bool:
        """Начинает техническое обслуживание кластера."""
        if not self.maintenance_mode:
            self.maintenance_mode = True
            for server in self.servers:
                server.enter_maintenance_mode(duration_hours)
            return True
        return False

    def end_maintenance(self) -> bool:
        """Завершает техническое обслуживание кластера."""
        if self.maintenance_mode:
            self.maintenance_mode = False
            for server in self.servers:
                server.exit_maintenance_mode()
            return True
        return False

    def _update_performance_metrics(self) -> None:
        """Обновляет метрики производительности кластера."""
        total_players = sum(server.current_players for server in self.servers)
        average_load = sum(server.get_server_load() for server in self.servers) / max(1, len(self.servers))
        
        self.performance_metrics["total_players"] = total_players
        self.performance_metrics["average_load"] = average_load

    def _check_auto_scaling(self) -> None:
        """Проверяет необходимость автоматического масштабирования."""
        if not self.auto_scaling_enabled:
            return
        
        avg_load = self.performance_metrics["average_load"]
        if avg_load > self.scaling_threshold and len(self.servers) < self.max_servers:
            self._scale_up()
        elif avg_load < 30.0 and len(self.servers) > 1:
            self._scale_down()

    def _scale_up(self) -> None:
        """Добавляет сервер в кластер."""
        if len(self.servers) >= self.max_servers:
            return
        
        new_server = GameServer(f"server_{len(self.servers) + 1}", f"Auto-Scaled Server {len(self.servers) + 1}")
        new_server.region = self.region
        new_server.start_server()
        self.add_server(new_server)

    def _scale_down(self) -> None:
        """Удаляет сервер из кластера."""
        if len(self.servers) <= 1:
            return
        
        # Находим сервер с наименьшей нагрузкой
        least_loaded_server = min(self.servers, key=lambda s: s.current_players)
        if least_loaded_server.current_players == 0:
            self.remove_server(least_loaded_server.server_id)
            least_loaded_server.stop_server()

    def _monitor_servers_health(self) -> None:
        """Мониторит здоровье серверов."""
        unhealthy_servers = [s for s in self.servers if s.status in ["overloaded", "maintenance"]]
        
        if len(unhealthy_servers) > len(self.servers) * 0.5:  # Более 50% серверов проблемные
            self.performance_metrics["health_status"] = "degraded"
        elif unhealthy_servers:
            self.performance_metrics["health_status"] = "warning"
        else:
            self.performance_metrics["health_status"] = "healthy"

    def get_cluster_status(self) -> Dict[str, Any]:
        """Возвращает статус кластера."""
        return {
            "cluster_id": self.entity_id,
            "name": self.name,
            "region": self.region,
            "total_servers": len(self.servers),
            "total_players": self.performance_metrics["total_players"],
            "average_load": self.performance_metrics["average_load"],
            "health_status": self.performance_metrics["health_status"],
            "maintenance_mode": self.maintenance_mode,
            "auto_scaling": self.auto_scaling_enabled
        }

