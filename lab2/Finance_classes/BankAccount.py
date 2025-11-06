class BankAccount:
    """
    Класс банковского счёта.

    Attributes:
        account_number (str): Номер счёта
        holder_name (str): Имя владельца
        balance (float): Баланс счёта
        currency (str): Валюта
        account_type (str): Тип счёта
    """

    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = initial_balance
        self.currency = "RUB"
        self.account_type = "checking"
        self.created_date = datetime.now()
        self.transactions = []
        self.daily_limit = 100000.0
        self.daily_spent = 0.0
        self.last_reset_date = datetime.now().date()
        self.is_frozen = False
        self.overdraft_limit = 0.0

    def deposit(self, amount: float, description: str = "") -> bool:
        """Пополняет счёт."""
        if amount <= 0:
            return False

        self.balance += amount
        self.add_transaction("deposit", amount, description)
        return True

    def withdraw(self, amount: float, description: str = "") -> bool:
        """Снимает деньги со счёта."""
        if amount <= 0 or self.is_frozen:
            return False

        # Проверяем дневной лимит
        if self.daily_spent + amount > self.daily_limit:
            raise InsufficientFundsException(amount, self.daily_limit - self.daily_spent)

        # Проверяем баланс с учётом овердрафта
        available_amount = self.balance + self.overdraft_limit
        if amount > available_amount:
            raise InsufficientFundsException(amount, available_amount)

        self.balance -= amount
        self.daily_spent += amount
        self.add_transaction("withdrawal", -amount, description)
        return True

    def transfer(self, target_account: 'BankAccount', amount: float, description: str = "") -> bool:
        """Переводит деньги на другой счёт."""
        if self.withdraw(amount, f"Transfer to {target_account.account_number}: {description}"):
            target_account.deposit(amount, f"Transfer from {self.account_number}: {description}")
            return True
        return False

    def add_transaction(self, transaction_type: str, amount: float, description: str) -> None:
        """Добавляет транзакцию в историю."""
        transaction = {
            "id": str(uuid.uuid4()),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now(),
            "balance_after": self.balance
        }
        self.transactions.append(transaction)

    def get_balance(self) -> float:
        """Возвращает текущий баланс."""
        return self.balance

    def reset_daily_limit(self) -> None:
        """Сбрасывает дневной лимит."""
        current_date = datetime.now().date()
        if current_date > self.last_reset_date:
            self.daily_spent = 0.0
            self.last_reset_date = current_date
