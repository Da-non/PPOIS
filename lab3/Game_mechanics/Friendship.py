class Friendship:
    """Класс дружеских отношений."""
    
    def __init__(self, player1_id: str, player2_id: str, status: str = "pending", note: str = ""):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.status = status  # pending, accepted, blocked
        self.created_date = datetime.now()
        self.accepted_date = None
        self.last_interaction = datetime.now()
        self.note = note
        self.shared_achievements = []
    
    def get_other_player(self, player_id: str) -> str:
        """Возвращает ID другого игрока."""
        return self.player2_id if self.player1_id == player_id else self.player1_id
    
    def get_friend_name(self, player: Player) -> str:
        """Возвращает имя друга."""
        # В реальной реализации здесь был бы поиск по ID игрока
        return "Friend"
    
    def get_friend_status(self) -> str:
        """Возвращает статус друга."""
        return "online"  # В реальной реализации проверялся бы статус онлайн
