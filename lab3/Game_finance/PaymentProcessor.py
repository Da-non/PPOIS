class PaymentProcessor(GameEntity):
    """
    Класс обработчика платежей.

    Attributes:
        processor_id (str): Уникальный идентификатор процессора
        name (str): Название процессора
        supported_methods (List[str]): Поддерживаемые методы оплаты
        transaction_fee (float): Комиссия за транзакцию
    """

    def __init__(self, processor_id: str, name: str):
        super().__init__(processor_id, name)
        self.supported_methods = ["credit_card", "paypal", "apple_pay", "google_pay", "crypto"]
        self.transaction_fee = 0.029  # 2.9%
        self.processing_time = 1.0  # секунды
        self.success_rate = 0.95
        self.daily_limit = 1000000.0
        self.daily_processed = 0.0
        self.transactions = []
        self.failed_transactions = []
        self.refunds = []
        self.chargebacks = []
        self.is_active = True
        self.maintenance_mode = False

    def update(self, delta_time: float) -> None:
        """Обновляет состояние процессора."""
        # Сбрасываем дневной лимит
        if datetime.now().hour == 0:
            self.daily_processed = 0.0

    def process_payment(self, amount: float, payment_method: str, player: Player, 
                       description: str = "") -> Dict[str, Any]:
        """Обрабатывает платеж."""
        if self.maintenance_mode:
            raise GameServerMaintenanceException("PaymentProcessor", datetime.now() + timedelta(hours=1))
        
        if not self.is_active:
            raise PaymentProcessingException("", "Процессор неактивен")
        
        if payment_method not in self.supported_methods:
            raise PaymentProcessingException("", f"Неподдерживаемый метод оплаты: {payment_method}")
        
        if self.daily_processed + amount > self.daily_limit:
            raise PaymentProcessingException("", "Превышен дневной лимит")
        
        transaction_id = str(uuid.uuid4())
        fee = amount * self.transaction_fee
        net_amount = amount - fee
        
        # Симуляция обработки платежа
        success = random.random() < self.success_rate
        
        transaction = {
            "transaction_id": transaction_id,
            "player_id": player.entity_id,
            "amount": amount,
            "fee": fee,
            "net_amount": net_amount,
            "payment_method": payment_method,
            "description": description,
            "timestamp": datetime.now(),
            "status": "completed" if success else "failed",
            "processing_time": self.processing_time
        }
        
        if success:
            self.transactions.append(transaction)
            self.daily_processed += amount
        else:
            self.failed_transactions.append(transaction)
            raise PaymentProcessingException(transaction_id, "Платеж отклонен")
        
        return transaction

    def refund_payment(self, transaction_id: str, amount: float = None) -> bool:
        """Возвращает платеж."""
        for transaction in self.transactions:
            if transaction["transaction_id"] == transaction_id:
                refund_amount = amount or transaction["net_amount"]
                
                refund = {
                    "refund_id": str(uuid.uuid4()),
                    "original_transaction_id": transaction_id,
                    "amount": refund_amount,
                    "timestamp": datetime.now(),
                    "status": "completed"
                }
                self.refunds.append(refund)
                
                transaction["status"] = "refunded"
                return True
        return False

    def process_chargeback(self, transaction_id: str, reason: str) -> bool:
        """Обрабатывает чарджбек."""
        for transaction in self.transactions:
            if transaction["transaction_id"] == transaction_id:
                chargeback = {
                    "chargeback_id": str(uuid.uuid4()),
                    "original_transaction_id": transaction_id,
                    "reason": reason,
                    "timestamp": datetime.now(),
                    "status": "pending"
                }
                self.chargebacks.append(chargeback)
                
                transaction["status"] = "chargeback"
                return True
        return False

    def get_daily_stats(self) -> Dict[str, Any]:
        """Возвращает дневную статистику."""
        today = datetime.now().date()
        today_transactions = [t for t in self.transactions if t["timestamp"].date() == today]
        
        return {
            "date": today,
            "transactions_count": len(today_transactions),
            "total_amount": sum(t["amount"] for t in today_transactions),
            "total_fees": sum(t["fee"] for t in today_transactions),
            "success_rate": len(today_transactions) / max(1, len(today_transactions) + len(self.failed_transactions)),
            "average_transaction": sum(t["amount"] for t in today_transactions) / max(1, len(today_transactions))
        }


