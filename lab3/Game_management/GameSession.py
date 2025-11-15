class GameSession(GameEntity):
    """
    Класс игровой сессии.

    Attributes:
        session_id (str): Уникальный идентификатор сессии
        player (Player): Игрок сессии
        server (GameServer): Сервер сессии
        start_time (datetime): Время начала сессии
        end_time (datetime): Время окончания сессии
    """

    def __init__(self, session_id: str, player: Player, server: GameServer):
        super().__init__(session_id, f"Session_{player.name}")
        self.player = player
        self.server = server
        self.start_time = datetime.now()
        self.end_time = None
        self.session_duration = 0.0
        self.actions_performed = 0
        self.experience_gained = 0
        self.currency_earned = {}
        self.items_obtained = []
        self.quests_completed = []
        self.combat_encounters = 0
        self.deaths = 0
        self.session_data = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние сессии."""
        if self.end_time is None:
            self.session_duration += delta_time

    def end_session(self) -> None:
        """Завершает сессию."""
        self.end_time = datetime.now()
        self.session_duration = (self.end_time - self.start_time).total_seconds()

    def add_action(self, action_type: str, data: Dict[str, Any] = None) -> None:
        """Добавляет действие в сессию."""
        self.actions_performed += 1
        action = {
            "type": action_type,
            "timestamp": datetime.now(),
            "data": data or {}
        }
        self.session_data[f"action_{self.actions_performed}"] = action

    def add_experience(self, amount: int) -> None:
        """Добавляет опыт к сессии."""
        self.experience_gained += amount

    def add_currency(self, currency_type: str, amount: int) -> None:
        """Добавляет валюту к сессии."""
        if currency_type not in self.currency_earned:
            self.currency_earned[currency_type] = 0
        self.currency_earned[currency_type] += amount

    def add_item(self, item_name: str) -> None:
        """Добавляет предмет к сессии."""
        self.items_obtained.append({
            "name": item_name,
            "timestamp": datetime.now()
        })

    def complete_quest(self, quest_name: str) -> None:
        """Добавляет завершенный квест к сессии."""
        self.quests_completed.append({
            "name": quest_name,
            "timestamp": datetime.now()
        })

    def add_combat_encounter(self) -> None:
        """Добавляет боевую встречу к сессии."""
        self.combat_encounters += 1

    def add_death(self) -> None:
        """Добавляет смерть к сессии."""
        self.deaths += 1


