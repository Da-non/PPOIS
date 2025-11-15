class GameEvent(GameEntity):
    """
    Класс игрового события.

    Attributes:
        event_id (str): Уникальный идентификатор события
        name (str): Название события
        event_type (str): Тип события
        start_time (datetime): Время начала события
        end_time (datetime): Время окончания события
    """

    def __init__(self, event_id: str, name: str, event_type: str):
        super().__init__(event_id, name)
        self.event_type = event_type
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = 0
        self.participants = []
        self.rewards = {}
        self.requirements = {}
        self.status = "scheduled"  # scheduled, active, completed, cancelled
        self.description = ""
        self.location = ""
        self.max_participants = 100
        self.min_level = 1
        self.max_level = 100
        self.event_data = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние события."""
        if self.status == "active" and self.end_time:
            if datetime.now() >= self.end_time:
                self.status = "completed"
                self._distribute_rewards()

    def start_event(self) -> bool:
        """Запускает событие."""
        if self.status == "scheduled":
            self.status = "active"
            self.start_time = datetime.now()
            if self.duration > 0:
                self.end_time = self.start_time + timedelta(hours=self.duration)
            return True
        return False

    def end_event(self) -> bool:
        """Завершает событие."""
        if self.status == "active":
            self.status = "completed"
            self.end_time = datetime.now()
            self._distribute_rewards()
            return True
        return False

    def add_participant(self, player: Player) -> bool:
        """Добавляет участника события."""
        if (len(self.participants) < self.max_participants and
            self.min_level <= player.level <= self.max_level):
            self.participants.append(player)
            return True
        return False

    def remove_participant(self, player: Player) -> bool:
        """Удаляет участника события."""
        if player in self.participants:
            self.participants.remove(player)
            return True
        return False

    def _distribute_rewards(self) -> None:
        """Распределяет награды участникам."""
        for player in self.participants:
            for reward_type, amount in self.rewards.items():
                if reward_type == "experience":
                    player.gain_experience(amount)
                elif reward_type == "currency":
                    for currency_type, currency_amount in amount.items():
                        player.add_currency(currency_type, currency_amount)
                elif reward_type == "items":
                    for item_data in amount:
                        item = GameItem(
                            item_data["item_id"],
                            item_data["name"],
                            item_data["item_type"],
                            item_data.get("rarity", "common")
                        )
                        player.add_item(item)

