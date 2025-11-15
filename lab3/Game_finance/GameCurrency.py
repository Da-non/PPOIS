class GameCurrency(GameEntity):
    """
    Класс игровой валюты.

    Attributes:
        currency_id (str): Уникальный идентификатор валюты
        name (str): Название валюты
        symbol (str): Символ валюты
        exchange_rate (float): Курс обмена
        total_supply (int): Общее количество валюты
        circulating_supply (int): Количество в обращении
    """

    def __init__(self, currency_id: str, name: str, symbol: str):
        super().__init__(currency_id, name)
        self.symbol = symbol
        self.exchange_rate = 1.0
        self.total_supply = 1000000
        self.circulating_supply = 0
        self.currency_type = "virtual"  # virtual, real, hybrid
        self.decimals = 2
        self.inflation_rate = 0.02  # 2% в год
        self.deflation_rate = 0.01  # 1% в год
        self.transaction_fee = 0.001  # 0.1%
        self.min_transaction_amount = 0.01
        self.max_transaction_amount = 1000000
        self.holders = {}
        self.transaction_history = []
        self.market_cap = 0.0
        self.price_history = []

    def update(self, delta_time: float) -> None:
        """Обновляет состояние валюты."""
        # Обновляем рыночную капитализацию
        self.market_cap = self.circulating_supply * self.exchange_rate
        
        # Добавляем инфляцию/дефляцию
        if random.random() < 0.01:  # 1% шанс изменения курса
            change = random.uniform(-0.05, 0.05)
            self.exchange_rate *= (1 + change)
            self.exchange_rate = max(0.01, self.exchange_rate)  # Минимум 0.01

    def mint_currency(self, amount: int, to_player: Player) -> bool:
        """Создает новую валюту."""
        if self.circulating_supply + amount <= self.total_supply:
            self.circulating_supply += amount
            if to_player.player_id not in self.holders:
                self.holders[to_player.player_id] = 0
            self.holders[to_player.player_id] += amount
            return True
        return False

    def burn_currency(self, amount: int, from_player: Player) -> bool:
        """Уничтожает валюту."""
        pid = from_player.player_id
        if pid in self.holders and self.holders[pid] >= amount:
            self.holders[pid] -= amount
            self.circulating_supply -= amount
            return True
        return False

    def transfer_currency(self, from_player: Player, to_player: Player, amount: int) -> bool:
        """Переводит валюту между игроками."""
        from_pid = from_player.player_id
        to_pid = to_player.player_id
        if from_pid in self.holders and self.holders[from_pid] >= amount:
            fee = int(amount * self.transaction_fee)
            net_amount = amount - fee
            self.holders[from_pid] -= amount
            if to_pid not in self.holders:
                self.holders[to_pid] = 0
            self.holders[to_pid] += net_amount
            transaction = {
                "transaction_id": str(uuid.uuid4()),
                "from_player": from_pid,
                "to_player": to_pid,
                "amount": amount,
                "fee": fee,
                "net_amount": net_amount,
                "timestamp": datetime.now()
            }
            self.transaction_history.append(transaction)
            return True
        return False

    def get_balance(self, player: Player) -> int:
        """Возвращает баланс игрока."""
        return self.holders.get(player.player_id, 0)

    def get_exchange_rate(self, target_currency: 'GameCurrency') -> float:
        """Возвращает курс обмена с другой валютой."""
        return self.exchange_rate / target_currency.exchange_rate

