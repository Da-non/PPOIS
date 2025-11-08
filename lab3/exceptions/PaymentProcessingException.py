class PaymentProcessingException(GameDevelopmentBaseException):
    """Исключение при ошибке обработки платежа в игре."""
    def __init__(self, transaction_id, error_message):
        self.transaction_id = transaction_id
        self.error_message = error_message
        super().__init__(f"Ошибка обработки платежа {transaction_id}: {error_message}")
