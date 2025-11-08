class Player(GameEntity):
    """
    Класс игрока.

    Attributes:
        player_id (str): Уникальный идентификатор игрока
        username (str): Имя пользователя
        email (str): Email адрес
        level (int): Уровень игрока
        experience (int): Опыт игрока
        health (float): Здоровье
        mana (float): Мана
        stamina (float): Выносливость
    """

    def __init__(self, player_id: str, username: str, email: str):
        super().__init__(player_id, username)
        self.player_id = player_id  # алиас для entity_id
        self.username = username
        self.email = email
        self.level = 1
        self.experience = 0
        self.health = 100.0
        self.max_health = 100.0
        self.mana = 50.0
        self.max_mana = 50.0
        self.stamina = 100.0
        self.max_stamina = 100.0
        self.currency = {"gold": 0, "gems": 0, "tokens": 0}
        self.inventory = []
        self.equipped_items = {}
        self.skills = {}
        self.achievements = []
        self.friends = []
        self.guild_id = None
        self.last_login = datetime.now()
        self.total_playtime = 0.0
        self.character_class = "warrior"
        self.character_race = "human"
        self.reputation = {}
        self.pvp_rating = 1000
        self.pve_rating = 1000

    def update(self, delta_time: float) -> None:
        """Обновляет состояние игрока."""
        # Восстановление ресурсов
        self.health = min(self.max_health, self.health + delta_time * 2)
        self.mana = min(self.max_mana, self.mana + delta_time * 1.5)
        self.stamina = min(self.max_stamina, self.stamina + delta_time * 3)
        
        self.last_modified = datetime.now()

    def gain_experience(self, amount: int) -> bool:
        """Получает опыт и проверяет повышение уровня."""
        self.experience += amount
        old_level = self.level
        
        # Проверяем повышение уровня
        required_exp = self.level * 1000
        while self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            required_exp = self.level * 1000
            
            # Увеличиваем характеристики при повышении уровня
            self.max_health += 20
            self.max_mana += 10
            self.max_stamina += 15
            self.health = self.max_health
            self.mana = self.max_mana
            self.stamina = self.max_stamina
        
        return self.level > old_level

    def take_damage(self, damage: float) -> bool:
        """Получает урон."""
        self.health = max(0, self.health - damage)
        return self.health <= 0

    def heal(self, amount: float) -> None:
        """Восстанавливает здоровье."""
        self.health = min(self.max_health, self.health + amount)

    def use_mana(self, amount: float) -> bool:
        """Использует ману."""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def use_stamina(self, amount: float) -> bool:
        """Использует выносливость."""
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False

    def add_currency(self, currency_type: str, amount: int) -> None:
        """Добавляет валюту."""
        if currency_type in self.currency:
            self.currency[currency_type] += amount

    def spend_currency(self, currency_type: str, amount: int) -> bool:
        """Тратит валюту."""
        if currency_type in self.currency and self.currency[currency_type] >= amount:
            self.currency[currency_type] -= amount
            return True
        raise InsufficientGameCurrencyException(amount, self.currency.get(currency_type, 0), currency_type)

    def add_item(self, item: 'GameItem') -> bool:
        """Добавляет предмет в инвентарь."""
        if len(self.inventory) < 50:  # Максимум 50 предметов
            self.inventory.append(item)
            return True
        return False

    def remove_item(self, item_id: str) -> Optional['GameItem']:
        """Удаляет предмет из инвентаря."""
        for item in self.inventory:
            if item.entity_id == item_id:
                self.inventory.remove(item)
                return item
        return None

    def equip_item(self, item: 'GameItem', slot: str) -> bool:
        """Экипирует предмет."""
        if item.required_class and item.required_class != self.character_class:
            raise EquipmentMismatchException(item.name, item.required_class, self.character_class)
        
        if item.required_level > self.level:
            raise UnauthorizedGameActionException("equip_item", item.required_level, self.level)
        
        self.equipped_items[slot] = item
        return True

    def unequip_item(self, slot: str) -> Optional['GameItem']:
        """Снимает предмет."""
        return self.equipped_items.pop(slot, None)

    def learn_skill(self, skill: 'Skill') -> bool:
        """Изучает навык."""
        if skill.required_level <= self.level:
            self.skills[skill.skill_id] = skill
            return True
        return False

    def use_skill(self, skill_id: str, target: Optional['GameEntity'] = None) -> bool:
        """Использует навык."""
        if skill_id not in self.skills:
            return False
        
        skill = self.skills[skill_id]
        if not self.use_mana(skill.mana_cost):
            return False
        
        return skill.activate(self, target)

    def add_friend(self, friend_id: str) -> None:
        """Добавляет друга."""
        if friend_id not in self.friends:
            self.friends.append(friend_id)

    def remove_friend(self, friend_id: str) -> bool:
        """Удаляет друга."""
        if friend_id in self.friends:
            self.friends.remove(friend_id)
            return True
        return False

    def join_guild(self, guild_id: str) -> bool:
        """Вступает в гильдию."""
        if not self.guild_id:
            self.guild_id = guild_id
            return True
        return False

    def leave_guild(self) -> bool:
        """Покидает гильдию."""
        if self.guild_id:
            self.guild_id = None
            return True
        return False
