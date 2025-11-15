class PvPSystem:
    """
    Система PvP (игрок против игрока).
    
    Attributes:
        pvp_id (str): Уникальный идентификатор PvP системы
        arenas (Dict[str, Arena]): Арены для PvP
        battlegrounds (Dict[str, Battleground]): Поля боя
        duels (Dict[str, Duel]): Дуэли
        honor_system (HonorSystem): Система чести
    """

    def __init__(self, pvp_id: str):
        self.pvp_id = pvp_id
        self.arenas = {}
        self.battlegrounds = {}
        self.duels = {}
        self.honor_system = HonorSystem()
        self.pvp_seasons = {}
        self.leaderboards = {}
        self.pvp_rewards = {}

    def start_duel(self, challenger: Player, target: Player) -> Optional[str]:
        """Начинает дуэль между игроками."""
        if challenger.entity_id == target.entity_id:
            return None
        
        if not self._can_duel(challenger, target):
            return None
        
        duel = Duel(challenger, target)
        self.duels[duel.duel_id] = duel
        
        # Отправляем запрос на дуэль
        target.notify({
            "type": "duel_request",
            "from": challenger.name,
            "duel_id": duel.duel_id,
            "expires": datetime.now() + timedelta(seconds=30)
        })
        
        return duel.duel_id

    def accept_duel(self, player: Player, duel_id: str) -> bool:
        """Принимает дуэль."""
        if duel_id not in self.duels:
            return False
        
        duel = self.duels[duel_id]
        if duel.target.entity_id != player.entity_id:
            return False
        
        if duel.status != "pending":
            return False
        
        return duel.start()

    def start_arena_match(self, team1: List[Player], team2: List[Player], arena_type: str = "2v2") -> Optional[str]:
        """Начинает матч на арене."""
        if len(team1) != len(team2):
            return None
        
        arena = Arena(team1, team2, arena_type)
        self.arenas[arena.arena_id] = arena
        
        # Уведомляем игроков
        for player in team1 + team2:
            player.notify({
                "type": "arena_match_start",
                "arena_id": arena.arena_id,
                "enemy_team": [p.name for p in (team2 if player in team1 else team1)],
                "arena_type": arena_type
            })
        
        return arena.arena_id

    def join_battleground(self, player: Player, battleground_id: str) -> bool:
        """Присоединяет игрока к полю боя."""
        if battleground_id not in self.battlegrounds:
            return False
        
        battleground = self.battlegrounds[battleground_id]
        return battleground.add_player(player)

    def calculate_honor(self, winner: Player, loser: Player, match_type: str) -> int:
        """Вычисляет количество чести за победу."""
        base_honor = {
            "duel": 10,
            "arena_2v2": 25,
            "arena_3v3": 35,
            "arena_5v5": 50,
            "battleground": 15
        }.get(match_type, 10)
        
        # Модификатор на основе разницы в рейтинге
        rating_diff = self.honor_system.get_rating(winner.entity_id) - self.honor_system.get_rating(loser.entity_id)
        rating_modifier = max(0.5, 1.0 - (rating_diff * 0.01))
        
        final_honor = int(base_honor * rating_modifier)
        self.honor_system.add_honor(winner.entity_id, final_honor)
        
        return final_honor

    def _can_duel(self, player1: Player, player2: Player) -> bool:
        """Проверяет, могут ли игроки драться на дуэли."""
        # Проверяем уровень
        if abs(player1.level - player2.level) > 10:
            return False
        
        # Проверяем зону (не все зоны разрешают PvP)
        if not player1.location.allow_pvp or not player2.location.allow_pvp:
            return False
        
        # Проверяем, не находятся ли игроки уже в бою
        if player1.in_combat or player2.in_combat:
            return False
        
        return True

    def get_pvp_stats(self, player: Player) -> Dict[str, Any]:
        """Возвращает PvP статистику игрока."""
        return {
            "honor": self.honor_system.get_honor(player.entity_id),
            "rating": self.honor_system.get_rating(player.entity_id),
            "duels_won": self.honor_system.get_duels_won(player.entity_id),
            "arena_wins": self.honor_system.get_arena_wins(player.entity_id),
            "battleground_wins": self.honor_system.get_battleground_wins(player.entity_id)
        }

