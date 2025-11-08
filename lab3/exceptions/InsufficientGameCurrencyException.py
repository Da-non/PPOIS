class InsufficientGameCurrencyException(GameDevelopmentBaseException):
    """Исключение при недостатке игровой валюты."""
    def __init__(self, required_amount, available_amount, currency_type):
        self.required_amount = required_amount
        self.available_amount = available_amount
        self.currency_type = currency_type
        super().__init__(f"Недостаточно {currency_type}: требуется {required_amount}, доступно {available_amount}")
