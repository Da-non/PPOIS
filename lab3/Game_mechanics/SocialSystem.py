class SocialSystem:
    """
    Система социальных взаимодействий между игроками.
    
    Attributes:
        social_id (str): Уникальный идентификатор социальной системы
        friendships (Dict[str, List[Friendship]]): Дружеские отношения
        parties (Dict[str, Party]): Группы игроков
        guilds (Dict[str, Guild]): Гильдии
        ignore_lists (Dict[str, List[str]]): Списки игнорирования
    """

    def __init__(self, social_id: str):
        self.social_id = social_id
        self.friendships = {}
        self.parties = {}
        self.guilds = {}
        self.ignore_lists = {}
        self.chat_channels = {}
        self.reputation_system = {}
        self.social_events = []

    def send_friend_request(self, sender: Player, receiver: Player, message: str = "") -> bool:
        """Отправляет запрос на дружбу."""
        if sender.entity_id == receiver.entity_id:
            return False
        
        if self.are_friends(sender, receiver):
            return False
        
        if receiver.entity_id in self.ignore_lists.get(sender.entity_id, []):
            return False
        
        # Создаем запрос на дружбу
        friendship = Friendship(sender.entity_id, receiver.entity_id, "pending", message)
        
        if sender.entity_id not in self.friendships:
            self.friendships[sender.entity_id] = []
        self.friendships[sender.entity_id].append(friendship)
        
        # Уведомляем получателя
        receiver.notify({
            "type": "friend_request",
            "from": sender.name,
            "message": message,
            "timestamp": datetime.now()
        })
        
        return True

    def accept_friend_request(self, player: Player, friend_id: str) -> bool:
        """Принимает запрос на дружбу."""
        for friendship in self.friendships.get(friend_id, []):
            if friendship.player2_id == player.entity_id and friendship.status == "pending":
                friendship.status = "accepted"
                friendship.accepted_date = datetime.now()
                
                # Добавляем взаимную дружбу
                mutual_friendship = Friendship(player.entity_id, friend_id, "accepted")
                if player.entity_id not in self.friendships:
                    self.friendships[player.entity_id] = []
                self.friendships[player.entity_id].append(mutual_friendship)
                
                player.notify({
                    "type": "friend_added",
                    "friend_name": friendship.get_friend_name(player),
                    "timestamp": datetime.now()
                })
                
                return True
        return False

    def remove_friend(self, player: Player, friend_id: str) -> bool:
        """Удаляет друга."""
        if player.entity_id in self.friendships:
            for friendship in self.friendships[player.entity_id][:]:
                if friendship.get_other_player(player.entity_id) == friend_id:
                    self.friendships[player.entity_id].remove(friendship)
                    
                    # Удаляем взаимную дружбу
                    if friend_id in self.friendships:
                        for mutual_friendship in self.friendships[friend_id][:]:
                            if mutual_friendship.get_other_player(friend_id) == player.entity_id:
                                self.friendships[friend_id].remove(mutual_friendship)
                    
                    return True
        return False

    def are_friends(self, player1: Player, player2: Player) -> bool:
        """Проверяет, являются ли игроки друзьями."""
        for friendship in self.friendships.get(player1.entity_id, []):
            if friendship.get_other_player(player1.entity_id) == player2.entity_id and friendship.status == "accepted":
                return True
        return False

    def create_party(self, leader: Player, party_name: str) -> str:
        """Создает группу."""
        party = Party(party_name, leader)
        self.parties[party.party_id] = party
        
        leader.notify({
            "type": "party_created",
            "party_name": party_name,
            "party_id": party.party_id
        })
        
        return party.party_id

    def invite_to_party(self, inviter: Player, target: Player, party_id: str) -> bool:
        """Приглашает игрока в группу."""
        if party_id not in self.parties:
            return False
        
        party = self.parties[party_id]
        if party.leader.entity_id != inviter.entity_id and not party.is_officer(inviter):
            return False
        
        if target.entity_id in party.members:
            return False
        
        # Отправляем приглашение
        party.invitations[target.entity_id] = datetime.now()
        
        target.notify({
            "type": "party_invite",
            "from": inviter.name,
            "party_name": party.name,
            "party_id": party_id,
            "expires": datetime.now() + timedelta(minutes=5)
        })
        
        return True

    def send_private_message(self, sender: Player, receiver: Player, message: str) -> bool:
        """Отправляет личное сообщение."""
        if receiver.entity_id in self.ignore_lists.get(sender.entity_id, []):
            return False
        
        if not self.are_friends(sender, receiver) and receiver.privacy_settings.get("messages_from_non_friends", False):
            return False
        
        receiver.notify({
            "type": "private_message",
            "from": sender.name,
            "message": message,
            "timestamp": datetime.now()
        })
        
        return True

    def add_to_ignore_list(self, player: Player, target_id: str) -> bool:
        """Добавляет игрока в список игнорирования."""
        if player.entity_id not in self.ignore_lists:
            self.ignore_lists[player.entity_id] = []
        
        if target_id not in self.ignore_lists[player.entity_id]:
            self.ignore_lists[player.entity_id].append(target_id)
            return True
        return False

    def get_friend_list(self, player: Player) -> List[Dict[str, Any]]:
        """Возвращает список друзей."""
        friends = []
        for friendship in self.friendships.get(player.entity_id, []):
            if friendship.status == "accepted":
                friend_data = {
                    "player_id": friendship.get_other_player(player.entity_id),
                    "status": friendship.get_friend_status(),
                    "last_online": friendship.last_interaction,
                    "note": friendship.note
                }
                friends.append(friend_data)
        return friends

