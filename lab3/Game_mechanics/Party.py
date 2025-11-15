class Party:
    """
    Класс группы игроков.
    
    Attributes:
        party_id (str): Уникальный идентификатор группы
        name (str): Название группы
        leader (Player): Лидер группы
        members (Dict[str, Player]): Участники группы
        invitations (Dict[str, datetime]): Приглашения
        settings (Dict): Настройки группы
    """

    def __init__(self, name: str, leader: Player):
        self.party_id = f"party_{random.randint(1000, 9999)}"
        self.name = name
        self.leader = leader
        self.members = {leader.entity_id: leader}
        self.invitations = {}
        self.settings = {
            "loot_method": "round_robin",  # round_robin, need_before_greed, master_loot
            "level_range": 10,
            "auto_accept_invites": False
        }
        self.officers = []
        self.party_chat = []
        self.created_date = datetime.now()
        self.party_buffs = []

    def add_member(self, player: Player) -> bool:
        """Добавляет участника в группу."""
        if len(self.members) >= 6:  # Максимум 6 человек в группе
            return False
        
        if player.entity_id in self.members:
            return False
        
        self.members[player.entity_id] = player
        player.party_id = self.party_id
        
        # Применяем групповые баффы
        self._apply_party_buffs(player)
        
        # Уведомляем группу
        self.broadcast_message(f"{player.name} присоединился к группе")
        
        return True

    def remove_member(self, player: Player) -> bool:
        """Удаляет участника из группы."""
        if player.entity_id in self.members:
            del self.members[player.entity_id]
            player.party_id = None
            
            # Снимаем групповые баффы
            self._remove_party_buffs(player)
            
            # Уведомляем группу
            self.broadcast_message(f"{player.name} покинул группу")
            
            # Если лидер ушел, выбираем нового
            if player.entity_id == self.leader.entity_id and self.members:
                self.leader = next(iter(self.members.values()))
                self.broadcast_message(f"{self.leader.name} теперь лидер группы")
            
            return True
        return False

    def broadcast_message(self, message: str, sender: Optional[Player] = None) -> None:
        """Отправляет сообщение всем участникам группы."""
        chat_message = {
            "sender": sender.name if sender else "Система",
            "message": message,
            "timestamp": datetime.now(),
            "type": "party"
        }
        
        self.party_chat.append(chat_message)
        
        for member in self.members.values():
            member.notify({
                "type": "party_message",
                "message": chat_message
            })

    def is_officer(self, player: Player) -> bool:
        """Проверяет, является ли игрок офицером."""
        return player.entity_id in self.officers

    def distribute_loot(self, item: GameItem, method: str = None) -> Player:
        """Распределяет добычу согласно выбранному методу."""
        loot_method = method or self.settings["loot_method"]
        
        if loot_method == "round_robin":
            return self._round_robin_loot(item)
        elif loot_method == "need_before_greed":
            return self._need_before_greed_loot(item)
        elif loot_method == "master_loot":
            return self.leader  # Лидер решает
        
        return None

    def _round_robin_loot(self, item: GameItem) -> Player:
        """Распределяет добычу по круговой системе."""
        eligible_players = [p for p in self.members.values() if p.can_use_item(item)]
        return random.choice(eligible_players) if eligible_players else None

    def _need_before_greed(self, item: GameItem) -> Player:
        """Распределяет добычу по системе 'нужда перед жадностью'."""
        need_players = [p for p in self.members.values() if self._item_is_needed(p, item)]
        if need_players:
            return random.choice(need_players)
        
        # Если никто не нуждается, случайный игрок из желающих
        greed_players = [p for p in self.members.values() if p.wants_item(item)]
        return random.choice(greed_players) if greed_players else None

    def _item_is_needed(self, player: Player, item: GameItem) -> bool:
        """Проверяет, нужен ли предмет игроку для основного снаряжения."""
        # В реальной реализации здесь была бы проверка класса, специализации и текущего снаряжения
        return True

    def _apply_party_buffs(self, player: Player) -> None:
        """Применяет групповые баффы к новому участнику."""
        for buff in self.party_buffs:
            player.apply_buff(buff)

    def _remove_party_buffs(self, player: Player) -> None:
        """Снимает групповые баффы с покидающего участника."""
        for buff in self.party_buffs:
            player.remove_buff(buff)


