class Moderator(GameEntity):
    """
    Класс модератора.

    Attributes:
        moderator_id (str): Уникальный идентификатор модератора
        name (str): Имя модератора
        permission_level (int): Уровень разрешений
        moderation_tools (List[str]): Инструменты модерации
    """

    def __init__(self, moderator_id: str, name: str, permission_level: int = 1):
        super().__init__(moderator_id, name)
        self.permission_level = permission_level
        self.moderation_tools = []
        self.active_reports = []
        self.resolved_reports = []
        self.warnings_issued = 0
        self.bans_issued = 0
        self.mutes_issued = 0
        self.kicks_issued = 0
        self.moderation_log = []
        self.working_hours = {"start": 9, "end": 17}
        self.specializations = []
        self.languages = ["russian"]

    def update(self, delta_time: float) -> None:
        """Обновляет состояние модератора."""
        # Модераторы обычно не требуют обновления
        pass

    def issue_warning(self, player: Player, reason: str, severity: int = 1) -> str:
        """Выдает предупреждение игроку."""
        warning_id = f"WARN_{len(self.moderation_log):04d}"
        warning = {
            "type": "warning",
            "warning_id": warning_id,
            "player_id": player.entity_id,
            "player_name": player.name,
            "reason": reason,
            "severity": severity,
            "moderator_id": self.entity_id,
            "timestamp": datetime.now(),
            "status": "active",
        }
        self.moderation_log.append(warning)
        self.warnings_issued += 1
        if self._should_auto_ban(player):
            self.ban_player(player, "Автоматический бан за множественные нарушения", 7)
        return warning_id

    def mute_player(self, player: Player, duration_minutes: int, reason: str) -> str:
        """Заглушает игрока."""
        mute_id = f"MUTE_{len(self.moderation_log):04d}"
        mute = {
            "type": "mute",
            "mute_id": mute_id,
            "player_id": player.entity_id,
            "player_name": player.name,
            "duration_minutes": duration_minutes,
            "reason": reason,
            "moderator_id": self.entity_id,
            "timestamp": datetime.now(),
            "expires_at": datetime.now() + timedelta(minutes=duration_minutes),
            "status": "active",
        }
        self.moderation_log.append(mute)
        self.mutes_issued += 1
        return mute_id

    def kick_player(self, player: Player, reason: str) -> str:
        """Выгоняет игрока с сервера."""
        kick_id = f"KICK_{len(self.moderation_log):04d}"
        kick = {
            "type": "kick",
            "kick_id": kick_id,
            "player_id": player.entity_id,
            "player_name": player.name,
            "reason": reason,
            "moderator_id": self.entity_id,
            "timestamp": datetime.now(),
            "status": "executed",
        }
        self.moderation_log.append(kick)
        self.kicks_issued += 1
        return kick_id

    def ban_player(self, player: Player, reason: str, duration_days: int = 0) -> str:
        """Банит игрока."""
        ban_id = f"BAN_{len(self.moderation_log):04d}"
        ban = {
            "type": "ban",
            "ban_id": ban_id,
            "player_id": player.entity_id,
            "player_name": player.name,
            "reason": reason,
            "duration_days": duration_days,
            "moderator_id": self.entity_id,
            "timestamp": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=duration_days) if duration_days > 0 else None,
            "status": "active",
        }
        self.moderation_log.append(ban)
        self.bans_issued += 1
        return ban_id

    def unban_player(self, player: Player, reason: str) -> bool:
        """Разбанивает игрока."""
        for action in reversed(self.moderation_log):
            if (
                action.get("player_id") == player.player_id
                and action.get("type") == "ban"
                and action.get("status") == "active"
            ):
                action["status"] = "revoked"
                action["unban_reason"] = reason
                action["unban_timestamp"] = datetime.now()
                return True
        return False

    def _should_auto_ban(self, player: Player) -> bool:
        """Проверяет, нужно ли автоматически забанить игрока."""
        warning_count = 0
        for action in self.moderation_log:
            if (
                action.get("player_id") == player.player_id
                and action.get("type") == "warning"
                and action.get("status") == "active"
            ):
                warning_count += 1
        return warning_count >= 3  # 3 предупреждения = автобан


