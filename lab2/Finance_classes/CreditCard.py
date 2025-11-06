class CreditCard:
    """
    Класс кредитной карты.

    Attributes:
        card_number (str): Номер карты
        holder_name (str): Имя держателя
        expiry_date (datetime): Дата истечения
        cvv (str): CVV код
        credit_limit (float): Кредитный лимит
    """

    def __init__(self, card_number: str, holder_name: str, expiry_date: datetime, cvv: str):
        self.card_number = card_number
        self.holder_name = holder_name
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.credit_limit = random.uniform(50000, 500000)
        self.current_balance = 0.0
        self.minimum_payment = 0.0
        self.interest_rate = random.uniform(12, 24)  # годовая ставка
        self.is_active = True
        self.is_blocked = False
        self.transactions = []
        self.payment_due_date = datetime.now() + timedelta(days=30)

    def charge(self, amount: float, merchant: str) -> bool:
        """Списывает деньги с карты."""
        if not self.is_active or self.is_blocked:
            return False

        if datetime.now() > self.expiry_date:
            raise TicketExpiredException(self.card_number, self.expiry_date)

        available_credit = self.credit_limit - self.current_balance
        if amount > available_credit:
            raise InsufficientFundsException(amount, available_credit)

        self.current_balance += amount
        self.minimum_payment += amount * 0.05  # 5% минимальный платёж

        transaction = {
            "id": str(uuid.uuid4()),
            "amount": amount,
            "merchant": merchant,
            "timestamp": datetime.now(),
            "type": "purchase"
        }
        self.transactions.append(transaction)
        return True

    def make_payment(self, amount: float) -> bool:
        """Погашает задолженность по карте."""
        if amount <= 0:
            return False

        payment_amount = min(amount, self.current_balance)
        self.current_balance -= payment_amount
        self.minimum_payment = max(0, self.minimum_payment - payment_amount)

        transaction = {
            "id": str(uuid.uuid4()),
            "amount": -payment_amount,
            "merchant": "Payment",
            "timestamp": datetime.now(),
            "type": "payment"
        }
        self.transactions.append(transaction)
        return True

    def block_card(self) -> None:
        """Блокирует карту."""
        self.is_blocked = True

    def unblock_card(self) -> None:
        """Разблокирует карту."""
        self.is_blocked = False

