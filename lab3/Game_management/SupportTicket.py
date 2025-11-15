class SupportTicket(GameEntity):
    """
    Класс тикета поддержки.

    Attributes:
        ticket_id (str): Уникальный идентификатор тикета
        player (Player): Игрок создавший тикет
        category (str): Категория тикета
        description (str): Описание проблемы
    """

    def __init__(self, ticket_id: str, player: Player, category: str, description: str):
        super().__init__(ticket_id, f"Ticket_{player.name}")
        self.player = player
        self.category = category
        self.description = description
        self.status = "open"  # open, assigned, in_progress, resolved, escalated
        self.priority = "normal"  # low, normal, high, critical
        self.created_time = datetime.now()
        self.assigned_gm = None
        self.assigned_time = None
        self.resolved_time = None
        self.solution = ""
        self.escalated = False
        self.escalation_reason = ""
        self.attachments = []
        self.chat_history = []

    def update(self, delta_time: float) -> None:
        """Обновляет состояние тикета."""
        # Автоматическое повышение приоритета при долгом ожидании
        if self.status == "open":
            wait_time = (datetime.now() - self.created_time).total_seconds()
            if wait_time > 900:  # 15 минут
                self.priority = "high"
            elif wait_time > 300:  # 5 минут
                self.priority = "medium"

    def assign_to(self, gm_id: str) -> None:
        """Назначает тикет гейммастеру."""
        self.assigned_gm = gm_id
        self.assigned_time = datetime.now()
        self.status = "assigned"

    def resolve(self, solution: str) -> None:
        """Решает тикет."""
        self.solution = solution
        self.resolved_time = datetime.now()
        self.status = "resolved"

    def escalate(self, reason: str) -> None:
        """Эскалирует тикет."""
        self.escalated = True
        self.escalation_reason = reason
        self.status = "escalated"

    def add_message(self, sender: str, message: str, is_gm: bool = False) -> None:
        """Добавляет сообщение в историю чата тикета."""
        chat_message = {
            "sender": sender,
            "message": message,
            "is_gm": is_gm,
            "timestamp": datetime.now()
        }
        self.chat_history.append(chat_message)

    def add_attachment(self, file_name: str, file_type: str, file_size: int) -> None:
        """Добавляет вложение к тикету."""
        attachment = {
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size,
            "uploaded_at": datetime.now()
        }
        self.attachments.append(attachment)

    def get_ticket_info(self) -> Dict[str, Any]:
        """Возвращает информацию о тикете."""
        return {
            "ticket_id": self.entity_id,
            "player_id": self.player.player_id,
            "player_name": self.player.name,
            "category": self.category,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_time": self.created_time,
            "assigned_gm": self.assigned_gm,
            "waiting_time": (datetime.now() - self.created_time).total_seconds() if self.status != "resolved" else 0,
            "has_attachments": len(self.attachments) > 0,
            "chat_messages": len(self.chat_history)
        }
