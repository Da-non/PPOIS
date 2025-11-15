class GameEconomy(GameEntity):
    """
    Класс игровой экономики.

    Attributes:
        economy_id (str): Уникальный идентификатор экономики
        currencies (Dict[str, GameCurrency]): Валюты экономики
        shops (Dict[str, GameShop]): Магазины экономики
        inflation_rate (float): Уровень инфляции
        gdp (float): ВВП экономики
    """

    def __init__(self, economy_id: str):
        super().__init__(economy_id, "GameEconomy")
        self.currencies = {}
        self.shops = {}
        self.subscriptions = {}
        self.payment_processors = {}
        self.inflation_rate = 0.02
        self.gdp = 0.0
        self.total_transactions = 0
        self.economic_indicators = {}
        self.market_trends = {}
        self.economic_events = []
        self.tax_rate = 0.1
        self.government_revenue = 0.0
        self.player_wealth_distribution = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние экономики."""
        # Обновляем все валюты
        for currency in self.currencies.values():
            currency.update(delta_time)
        
        # Обновляем все магазины
        for shop in self.shops.values():
            shop.update(delta_time)
        
        # Обновляем ВВП
        self._update_gdp()
        
        # Обновляем экономические индикаторы
        self._update_economic_indicators()

    def add_currency(self, currency: GameCurrency) -> None:
        """Добавляет валюту в экономику."""
        self.currencies[currency.entity_id] = currency

    def add_shop(self, shop: GameShop) -> None:
        """Добавляет магазин в экономику."""
        self.shops[shop.entity_id] = shop

    def add_subscription(self, subscription: Subscription) -> None:
        """Добавляет подписку в экономику."""
        self.subscriptions[subscription.entity_id] = subscription

    def add_payment_processor(self, processor: PaymentProcessor) -> None:
        """Добавляет процессор платежей в экономику."""
        self.payment_processors[processor.entity_id] = processor

    def _update_gdp(self) -> None:
        """Обновляет ВВП."""
        total_value = 0.0
        
        # Суммируем стоимость всех валют
        for currency in self.currencies.values():
            total_value += currency.market_cap
        
        # Добавляем доходы магазинов
        for shop in self.shops.values():
            total_value += shop.daily_revenue
        
        self.gdp = total_value

    def _update_economic_indicators(self) -> None:
        """Обновляет экономические индикаторы."""
        self.economic_indicators = {
            "gdp": self.gdp,
            "inflation_rate": self.inflation_rate,
            "unemployment_rate": random.uniform(0.05, 0.15),
            "interest_rate": random.uniform(0.01, 0.05),
            "consumer_confidence": random.uniform(0.6, 1.0),
            "market_volatility": random.uniform(0.1, 0.3)
        }

    def get_economic_health_score(self) -> float:
        """Возвращает балл здоровья экономики."""
        score = 100.0
        
        # Штрафы за негативные факторы
        if self.inflation_rate > 0.05:
            score -= (self.inflation_rate - 0.05) * 1000
        
        if self.economic_indicators.get("unemployment_rate", 0) > 0.1:
            score -= (self.economic_indicators["unemployment_rate"] - 0.1) * 500
        
        if self.economic_indicators.get("consumer_confidence", 1) < 0.7:
            score -= (0.7 - self.economic_indicators["consumer_confidence"]) * 200
        
        return max(0, min(100, score))

    def create_economic_event(self, event_type: str, description: str, 
                            impact: float, duration_hours: int) -> str:
        """Создает экономическое событие."""
        event_id = str(uuid.uuid4())
        event = {
            "event_id": event_id,
            "type": event_type,
            "description": description,
            "impact": impact,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=duration_hours),
            "is_active": True
        }
        self.economic_events.append(event)
        return event_id

    def get_market_analysis(self) -> Dict[str, Any]:
        """Возвращает анализ рынка."""
        return {
            "total_currencies": len(self.currencies),
            "total_shops": len(self.shops),
            "total_subscriptions": len(self.subscriptions),
            "gdp": self.gdp,
            "economic_health": self.get_economic_health_score(),
            "active_events": len([e for e in self.economic_events if e["is_active"]]),
            "market_trends": self.market_trends,
        }

