class PaymentProcessor:
    """
    Система обработки платежей.

    Attributes:
        processor_id (str): Идентификатор процессора
        supported_methods (List[str]): Поддерживаемые методы оплаты
        transaction_fee (float): Комиссия за транзакцию
        daily_limits (Dict): Дневные лимиты
    """

    def __init__(self, processor_id: str):
        self.processor_id = processor_id
        self.supported_methods = ["credit_card", "debit_card", "cash", "bank_transfer"]
        self.transaction_fee = 0.025  # 2.5%
        self.daily_limits = {
            "credit_card": 100000,
            "debit_card": 50000,
            "cash": 10000
        }
        self.processed_transactions = []
        self.failed_transactions = []
        self.maintenance_mode = False

    def process_payment(self, payment_method: str, amount: float, card: Optional[CreditCard] = None) -> Dict:
        """Обрабатывает платёж."""
        if self.maintenance_mode:
            raise MaintenanceModeException("Payment System", datetime.now() + timedelta(hours=2))

        transaction_id = str(uuid.uuid4())

        try:
            if payment_method == "credit_card" and card:
                success = card.charge(amount, "Oceanarium")
            elif payment_method == "cash":
                success = amount <= self.daily_limits["cash"]
            else:
                success = random.random() > 0.05  # 95% успеха для других методов

            if success:
                fee = amount * self.transaction_fee
                net_amount = amount - fee

                transaction = {
                    "transaction_id": transaction_id,
                    "amount": amount,
                    "fee": fee,
                    "net_amount": net_amount,
                    "method": payment_method,
                    "timestamp": datetime.now(),
                    "status": "completed"
                }
                self.processed_transactions.append(transaction)
                return transaction
            else:
                raise PaymentProcessingException(transaction_id, "Insufficient funds or card declined")

        except Exception as e:
            failed_transaction = {
                "transaction_id": transaction_id,
                "amount": amount,
                "method": payment_method,
                "timestamp": datetime.now(),
                "status": "failed",
                "error": str(e)
            }
            self.failed_transactions.append(failed_transaction)
            raise e

    def refund_payment(self, transaction_id: str) -> bool:
        """Возвращает платёж."""
        for transaction in self.processed_transactions:
            if transaction["transaction_id"] == transaction_id:
                transaction["status"] = "refunded"
                return True
        return False

    def get_daily_volume(self) -> float:
        """Возвращает дневной объём транзакций."""
        today = datetime.now().date()
        daily_total = 0.0

        for transaction in self.processed_transactions:
            if transaction["timestamp"].date() == today:
                daily_total += transaction["amount"]

        return daily_total

