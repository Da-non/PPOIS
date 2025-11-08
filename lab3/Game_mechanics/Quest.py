class Quest(GameEntity):
    """
    Класс квеста.

    Attributes:
        quest_id (str): Уникальный идентификатор квеста
        name (str): Название квеста
        description (str): Описание квеста
        quest_type (str): Тип квеста
        objectives (List[Dict]): Цели квеста
        rewards (Dict): Награды за квест
        requirements (Dict): Требования к квесту
    """

    def __init__(self, quest_id: str, name: str, description: str, quest_type: str = "main"):
        super().__init__(quest_id, name)
        self.description = description
        self.quest_type = quest_type
        self.objectives = []
        self.rewards = {"experience": 0, "currency": {}, "items": []}
        self.requirements = {"level": 1, "class": None, "completed_quests": []}
        self.status = "available"  # available, active, completed, failed
        self.start_date = None
        self.completion_date = None
        self.time_limit = None
        self.difficulty = "normal"
        self.quest_giver = None
        self.location = None
        self.prerequisites = []
        self.follow_up_quests = []

    def update(self, delta_time: float) -> None:
        """Обновляет состояние квеста."""
        if self.status == "active" and self.time_limit:
            if datetime.now() > self.time_limit:
                self.status = "failed"
                self.completion_date = datetime.now()

    def start_quest(self, player: Player) -> bool:
        """Начинает квест."""
        if self.status != "available":
            return False
        
        if not self._check_requirements(player):
            return False
        
        self.status = "active"
        self.start_date = datetime.now()
        if self.time_limit:
            self.time_limit = datetime.now() + timedelta(hours=self.time_limit)
        
        return True

    def complete_quest(self, player: Player) -> bool:
        """Завершает квест."""
        if self.status != "active":
            return False
        
        if not self._check_objectives_completed(player):
            return False
        
        self.status = "completed"
        self.completion_date = datetime.now()
        self._give_rewards(player)
        
        return True

    def fail_quest(self, player: Player) -> None:
        """Проваливает квест."""
        self.status = "failed"
        self.completion_date = datetime.now()

    def add_objective(self, objective_type: str, description: str, target: str, amount: int = 1) -> None:
        """Добавляет цель квеста."""
        objective = {
            "type": objective_type,
            "description": description,
            "target": target,
            "amount": amount,
            "completed": 0,
            "completed_at": None
        }
        self.objectives.append(objective)

    def update_objective(self, objective_type: str, target: str, amount: int = 1) -> bool:
        """Обновляет прогресс цели квеста."""
        for objective in self.objectives:
            if objective["type"] == objective_type and objective["target"] == target:
                objective["completed"] = min(objective["amount"], objective["completed"] + amount)
                if objective["completed"] >= objective["amount"]:
                    objective["completed_at"] = datetime.now()
                return True
        return False

    def _check_requirements(self, player: Player) -> bool:
        """Проверяет требования к квесту."""
        if player.level < self.requirements["level"]:
            return False
        
        if self.requirements["class"] and player.character_class != self.requirements["class"]:
            return False
        
        for quest_id in self.requirements["completed_quests"]:
            if quest_id not in [q.quest_id for q in player.achievements if hasattr(q, 'quest_id')]:
                return False
        
        return True

    def _check_objectives_completed(self, player: Player) -> bool:
        """Проверяет, выполнены ли все цели квеста."""
        for objective in self.objectives:
            if objective["completed"] < objective["amount"]:
                return False
        return True

    def _give_rewards(self, player: Player) -> None:
        """Выдает награды за квест."""
        if self.rewards["experience"] > 0:
            player.gain_experience(self.rewards["experience"])
        
        for currency_type, amount in self.rewards["currency"].items():
            player.add_currency(currency_type, amount)
        
        for item_data in self.rewards["items"]:
            item = GameItem(
                item_data["item_id"],
                item_data["name"],
                item_data["item_type"],
                item_data.get("rarity", "common")
            )
            player.add_item(item)

