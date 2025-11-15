class GameBalanceManager(GameEntity):
    """
    Класс менеджера баланса игры.
    
    Attributes:
        balance_manager_id (str): Уникальный идентификатор менеджера баланса
        monitored_metrics (Dict): Отслеживаемые метрики баланса
        balance_patches (List[Dict]): Выпущенные патчи баланса
    """

    def __init__(self, balance_manager_id: str):
        super().__init__(balance_manager_id, "GameBalanceManager")
        self.monitored_metrics = {
            "class_win_rates": {},
            "item_usage_stats": {},
            "skill_effectiveness": {},
            "economy_inflation": 0.0
        }
        self.balance_patches = []
        self.balance_thresholds = {
            "win_rate_deviation": 0.05,  # 5%
            "item_usage_min": 0.01,      # 1%
            "skill_usage_max": 0.3,      # 30%
            "inflation_max": 0.1         # 10%
        }

    def update(self, delta_time: float) -> None:
        """Обновляет состояние менеджера баланса."""
        # Периодическая проверка баланса
        if random.random() < 0.01:
            self._check_game_balance()

    def collect_balance_data(self, game_system: 'GameDevelopment') -> None:
        """Собирает данные для анализа баланса."""
        # Анализ классов
        for character in game_system.characters.values():
            class_name = character.character_class
            if class_name not in self.monitored_metrics["class_win_rates"]:
                self.monitored_metrics["class_win_rates"][class_name] = {
                    "wins": 0, "losses": 0, "total": 0
                }
        
        # Анализ предметов
        for player in game_system.players.values():
            for item in player.inventory:
                if item:
                    item_id = item.entity_id
                    if item_id not in self.monitored_metrics["item_usage_stats"]:
                        self.monitored_metrics["item_usage_stats"][item_id] = 0
                    self.monitored_metrics["item_usage_stats"][item_id] += 1

    def _check_game_balance(self) -> None:
        """Проверяет баланс игры и предлагает корректировки."""
        issues_found = []
        
        # Проверка баланса классов
        for class_name, stats in self.monitored_metrics["class_win_rates"].items():
            if stats["total"] > 0:
                win_rate = stats["wins"] / stats["total"]
                if abs(win_rate - 0.5) > self.balance_thresholds["win_rate_deviation"]:
                    issues_found.append({
                        "type": "class_imbalance",
                        "target": class_name,
                        "current_win_rate": win_rate,
                        "suggested_adjustment": "adjust_class_stats"
                    })
        
        # Проверка использования предметов
        total_items = sum(self.monitored_metrics["item_usage_stats"].values())
        for item_id, usage in self.monitored_metrics["item_usage_stats"].items():
            usage_rate = usage / total_items if total_items > 0 else 0
            if usage_rate < self.balance_thresholds["item_usage_min"]:
                issues_found.append({
                    "type": "underused_item",
                    "target": item_id,
                    "current_usage": usage_rate,
                    "suggested_adjustment": "buff_item_stats"
                })
        
        if issues_found:
            self._create_balance_patch(issues_found)

    def _create_balance_patch(self, issues: List[Dict]) -> str:
        """Создает патч баланса."""
        patch_id = f"balance_patch_{len(self.balance_patches) + 1:03d}"
        patch = {
            "patch_id": patch_id,
            "issues_resolved": issues,
            "created_at": datetime.now(),
            "status": "proposed",
            "changes": self._generate_balance_changes(issues)
        }
        
        self.balance_patches.append(patch)
        return patch_id

    def _generate_balance_changes(self, issues: List[Dict]) -> List[Dict]:
        """Генерирует изменения для балансировки."""
        changes = []
        for issue in issues:
            if issue["type"] == "class_imbalance":
                changes.append({
                    "target_type": "class",
                    "target_id": issue["target"],
                    "adjustment": random.uniform(-0.1, 0.1),
                    "stat_affected": random.choice(["strength", "agility", "intelligence"])
                })
            elif issue["type"] == "underused_item":
                changes.append({
                    "target_type": "item",
                    "target_id": issue["target"],
                    "adjustment": random.uniform(0.1, 0.3),
                    "stat_affected": "value"
                })
        
        return changes
