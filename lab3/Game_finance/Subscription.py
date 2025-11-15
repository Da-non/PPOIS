class Subscription(GameEntity):
    """
    Класс подписки.

    Attributes:
        subscription_id (str): Уникальный идентификатор подписки
        name (str): Название подписки
        subscription_type (str): Тип подписки
        price (float): Цена подписки
        duration_days (int): Продолжительность в днях
        benefits (List[str]): Преимущества подписки
    """

    def __init__(self, subscription_id: str, name: str, subscription_type: str, price: float, duration_days: int):
        super().__init__(subscription_id, name)
        self.subscription_type = subscription_type
        self.price = price
        self.duration_days = duration_days
        self.benefits = []
        self.is_active = True
        self.auto_renewal = True
        self.trial_period_days = 0
        self.max_subscribers = 10000
        self.current_subscribers = 0
        self.subscription_history = []
        self.cancellation_rate = 0.0
        self.renewal_rate = 0.0

    def update(self, delta_time: float) -> None:
        """Обновляет состояние подписки."""
        # Подписки обычно не требуют обновления
        pass

    def add_benefit(self, benefit: str) -> None:
        """Добавляет преимущество подписки."""
        if benefit not in self.benefits:
            self.benefits.append(benefit)

    def remove_benefit(self, benefit: str) -> bool:
        """Удаляет преимущество подписки."""
        if benefit in self.benefits:
            self.benefits.remove(benefit)
            return True
        return False

    def subscribe_player(self, player: Player, payment_method: str) -> bool:
        """Подписывает игрока."""
        if self.current_subscribers >= self.max_subscribers:
            return False
        
        # Проверяем платеж
        if not self._process_payment(player, payment_method):
            return False
        
        # Создаем подписку игрока
        player_subscription = {
            "subscription_id": self.entity_id,
            "player_id": player.entity_id,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=self.duration_days),
            "is_active": True,
            "auto_renewal": self.auto_renewal,
            "payment_method": payment_method
        }
        
        self.subscription_history.append(player_subscription)
        self.current_subscribers += 1
        
        # Применяем преимущества
        self._apply_benefits(player)
        
        return True

    def unsubscribe_player(self, player: Player) -> bool:
        """Отписывает игрока."""
        for subscription in self.subscription_history:
            if (subscription["player_id"] == player.player_id and 
                subscription["is_active"]):
                subscription["is_active"] = False
                subscription["end_date"] = datetime.now()
                self.current_subscribers -= 1
                
                # Убираем преимущества
                self._remove_benefits(player)
                
                return True
        return False

    def _process_payment(self, player: Player, payment_method: str) -> bool:
        """Обрабатывает платеж."""
        # Упрощенная реализация
        if payment_method == "credit_card":
            return random.random() > 0.05  # 95% успеха
        elif payment_method == "paypal":
            return random.random() > 0.03  # 97% успеха
        else:
            return random.random() > 0.1  # 90% успеха

    def _apply_benefits(self, player: Player) -> None:
        """Применяет преимущества подписки."""
        for benefit in self.benefits:
            if benefit == "double_experience":
                player.experience *= 2
            elif benefit == "exclusive_items":
                # Даем эксклюзивный предмет
                exclusive_item = GameItem(
                    f"exclusive_{self.subscription_id}",
                    f"Exclusive {self.name} Item",
                    "special",
                    "legendary"
                )
                player.add_item(exclusive_item)
            elif benefit == "no_ads":
                # Убираем рекламу (упрощенно)
                player.metadata["no_ads"] = True

    def _remove_benefits(self, player: Player) -> None:
        """Убирает преимущеcтва подписки."""
        if "no_ads" in player.metadata:
            del player.metadata["no_ads"]
