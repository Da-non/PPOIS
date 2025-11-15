class GameStatistics(GameEntity):
    """
    Класс игровой статистики.

    Attributes:
        stats_id (str): Уникальный идентификатор статистики
        player (Player): Игрок статистики
        total_playtime (float): Общее время игры
        level_reached (int): Достигнутый уровень
        quests_completed (int): Завершенные квесты
        monsters_killed (int): Убитые монстры
    """

    def __init__(self, stats_id: str, player: Player):
        super().__init__(stats_id, f"Stats_{player.name}")
        self.player = player
        self.total_playtime = 0.0
        self.level_reached = 1
        self.quests_completed = 0
        self.monsters_killed = 0
        self.players_killed = 0
        self.deaths = 0
        self.damage_dealt = 0.0
        self.damage_taken = 0.0
        self.healing_done = 0.0
        self.currency_earned = {}
        self.items_obtained = 0
        self.items_sold = 0
        self.trades_completed = 0
        self.guild_activities = 0
        self.pvp_matches = 0
        self.pvp_wins = 0
        self.pve_encounters = 0
        self.pve_victories = 0
        self.achievements_unlocked = 0
        self.skills_learned = 0
        self.crafting_attempts = 0
        self.crafting_successes = 0
        self.exploration_areas = 0
        self.secrets_found = 0
        self.friends_made = 0
        self.guilds_joined = 0
        self.events_participated = 0
        self.rankings = {}
        self.records = {}
        self.milestones = []

    def update(self, delta_time: float) -> None:
        """Обновляет статистику."""
        self.total_playtime += delta_time
        self.level_reached = max(self.level_reached, self.player.level)

    def add_quest_completion(self, quest_name: str) -> None:
        """Добавляет завершение квеста."""
        self.quests_completed += 1
        self.milestones.append({
            "type": "quest_completed",
            "name": quest_name,
            "timestamp": datetime.now()
        })

    def add_monster_kill(self, monster_name: str, experience: int) -> None:
        """Добавляет убийство монстра."""
        self.monsters_killed += 1
        self.damage_dealt += random.uniform(50, 200)

    def add_player_kill(self, player_name: str) -> None:
        """Добавляет убийство игрока."""
        self.players_killed += 1
        self.pvp_matches += 1

    def add_death(self, cause: str) -> None:
        """Добавляет смерть."""
        self.deaths += 1
        self.milestones.append({
            "type": "death",
            "cause": cause,
            "timestamp": datetime.now()
        })

    def add_damage_taken(self, amount: float) -> None:
        """Добавляет полученный урон."""
        self.damage_taken += amount

    def add_healing_done(self, amount: float) -> None:
        """Добавляет исцеление."""
        self.healing_done += amount

    def add_currency_earned(self, currency_type: str, amount: int) -> None:
        """Добавляет заработанную валюту."""
        if currency_type not in self.currency_earned:
            self.currency_earned[currency_type] = 0
        self.currency_earned[currency_type] += amount

    def add_item_obtained(self, item_name: str) -> None:
        """Добавляет полученный предмет."""
        self.items_obtained += 1

    def add_achievement(self, achievement_name: str) -> None:
        """Добавляет достижение."""
        self.achievements_unlocked += 1
        self.milestones.append({
            "type": "achievement",
            "name": achievement_name,
            "timestamp": datetime.now()
        })

    def add_skill_learned(self, skill_name: str) -> None:
        """Добавляет изученный навык."""
        self.skills_learned += 1

    def add_crafting_attempt(self, success: bool) -> None:
        """Добавляет попытку крафта."""
        self.crafting_attempts += 1
        if success:
            self.crafting_successes += 1

    def add_experience(self, amount: int) -> None:
        """Фиксирует полученный опыт в статистике."""
        self.records["experience_gained"] = self.records.get("experience_gained", 0) + int(amount)

    def get_win_rate(self) -> float:
        """Возвращает процент побед в PvP."""
        if self.pvp_matches == 0:
            return 0.0
        return (self.pvp_wins / self.pvp_matches) * 100

    def get_crafting_success_rate(self) -> float:
        """Возвращает процент успешного крафта."""
        if self.crafting_attempts == 0:
            return 0.0
        return (self.crafting_successes / self.crafting_attempts) * 100

    def get_kill_death_ratio(self) -> float:
        """Возвращает соотношение убийств к смертям."""
        if self.deaths == 0:
            return float(self.players_killed + self.monsters_killed)
        return (self.players_killed + self.monsters_killed) / self.deaths

    def get_efficiency_score(self) -> float:
        """Возвращает общий балл эффективности."""
        score = 0.0
        
        # Базовые показатели
        score += self.level_reached * 10
        score += self.quests_completed * 5
        score += self.achievements_unlocked * 15
        
        # Боевые показатели
        score += self.monsters_killed * 0.1
        score += self.players_killed * 2
        score -= self.deaths * 5
        
        # Экономические показатели
        total_currency = sum(self.currency_earned.values())
        score += total_currency * 0.001
        
        # Крафт
        score += self.crafting_successes * 0.5
        
        return max(0, score)
