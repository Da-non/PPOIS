class NotificationSystem(GameEntity):
    """Система всплывающих уведомлений."""

    def __init__(self, notif_id: str):
        super().__init__(notif_id, "Notifications")
        self.queue: List[Dict[str, Any]] = []
        self.history: List[Dict[str, Any]] = []
        self.max_history: int = 100

    def push(self, message: str, level: str = "info") -> None:
        """Добавляет новое уведомление в очередь"""
        note = {"message": message, "level": level, "time": datetime.now()}
        self.queue.append(note)

    def flush(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Извлекает уведомления из очереди для отображения"""
        out = self.queue[:limit]
        self.queue = self.queue[limit:]
        self.history.extend(out)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]
        return out
