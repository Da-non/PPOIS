class GameMaster(GameEntity):
    """
    Класс гейммастера (GM) для помощи игрокам и управления игровым миром.

    Attributes:
        gm_id (str): Уникальный идентификатор гейммастера
        name (str): Имя гейммастера
        rank (str): Ранг гейммастера
        available (bool): Доступен ли для помощи
    """

    def __init__(self, gm_id: str, name: str, rank: str = "junior"):
        super().__init__(gm_id, name)
        self.rank = rank  # junior, senior, lead
        self.available = True
        self.current_tickets = []
        self.resolved_tickets = []
        self.specializations = ["general_support", "bug_reports", "player_disputes"]
        self.working_hours = {"start": 9, "end": 21}
        self.response_time_target = 300.0  # 5 минут в секундах
        self.gm_tools = []
        self.teleport_locations = {}
        self.moderator_powers = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние гейммастера."""
        self._check_working_hours()
        self._update_ticket_priorities()

    def accept_ticket(self, ticket: 'SupportTicket') -> bool:
        """Принимает тикет в работу."""
        if self.available and ticket.status == "open":
            ticket.assign_to(self.entity_id)
            self.current_tickets.append(ticket)
            return True
        return False

    def resolve_ticket(self, ticket_id: str, solution: str) -> bool:
        """Решает тикет."""
        for ticket in self.current_tickets:
            if ticket.ticket_id == ticket_id:
                ticket.resolve(solution)
                self.current_tickets.remove(ticket)
                self.resolved_tickets.append(ticket)
                return True
        return False

    def escalate_ticket(self, ticket_id: str, reason: str) -> bool:
        """Эскалирует тикет старшему GM."""
        for ticket in self.current_tickets:
            if ticket.ticket_id == ticket_id:
                ticket.escalate(reason)
                self.current_tickets.remove(ticket)
                return True
        return False

    def teleport_player(self, player: Player, location: str) -> bool:
        """Телепортирует игрока в указанную локацию."""
        if location in self.teleport_locations:
            teleport_log = {
                "gm_id": self.entity_id,
                "player_id": player.player_id,
                "location": location,
                "timestamp": datetime.now()
            }
            return True
        return False

    def spawn_item(self, player: Player, item_template: str, quantity: int = 1) -> bool:
        """Создает предмет для игрока."""
        spawn_log = {
            "gm_id": self.entity_id,
            "player_id": player.player_id,
            "item": item_template,
            "quantity": quantity,
            "timestamp": datetime.now()
        }
        return True

    def restore_character(self, player: Player, backup_data: Dict[str, Any]) -> bool:
        """Восстанавливает персонажа из бэкапа."""
        restore_log = {
            "gm_id": self.entity_id,
            "player_id": player.player_id,
            "restore_time": datetime.now(),
            "backup_date": backup_data.get("backup_date")
        }
        return True

    def _check_working_hours(self) -> None:
        """Проверяет рабочие часы GM."""
        current_hour = datetime.now().hour
        self.available = (self.working_hours["start"] <= current_hour < self.working_hours["end"])

    def _update_ticket_priorities(self) -> None:
        """Обновляет приоритеты тикетов на основе времени ожидания."""
        for ticket in self.current_tickets:
            wait_time = (datetime.now() - ticket.created_time).total_seconds()
            if wait_time > 600:  # 10 минут
                ticket.priority = "high"
            elif wait_time > 300:  # 5 минут
                ticket.priority = "medium"

    def get_gm_performance(self) -> Dict[str, Any]:
        """Возвращает показатели эффективности GM."""
        total_resolved = len(self.resolved_tickets)
        avg_resolution_time = 0.0
        
        if total_resolved > 0:
            total_time = sum((t.resolved_time - t.created_time).total_seconds() 
                           for t in self.resolved_tickets if t.resolved_time)
            avg_resolution_time = total_time / total_resolved
        
        return {
            "gm_id": self.entity_id,
            "name": self.name,
            "rank": self.rank,
            "available": self.available,
            "current_tickets": len(self.current_tickets),
            "resolved_tickets": total_resolved,
            "average_resolution_time": avg_resolution_time,
            "escalated_tickets": len([t for t in self.resolved_tickets if t.escalated]),
            "specializations": self.specializations
        }
