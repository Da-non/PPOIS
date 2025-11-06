class Visitor:
    """
    Класс посетителя океанариума.

    Attributes:
        visitor_id (str): Уникальный идентификатор посетителя
        name (str): Имя посетителя
        email (str): Email адрес
        phone (str): Номер телефона
        age (int): Возраст
    """

    def __init__(self, name: str, email: str, phone: str, age: int):
        self.visitor_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.age = age
        self.registration_date = datetime.now()
        self.tickets = []
        self.visit_history = []
        self.preferences = []
        self.membership_type = "regular"
        self.loyalty_points = 0
        self.emergency_contact = None
        self.special_needs = []

    def purchase_ticket(self, ticket_type: str, price: float, payment_processor: PaymentProcessor,
                       payment_method: str, card: Optional[CreditCard] = None) -> Ticket:
        """Покупает билет."""
        # Обрабатываем платёж
        transaction = payment_processor.process_payment(payment_method, price, card)

        # Создаём билет
        ticket = Ticket(ticket_type, price)
        ticket.visitor_id = self.visitor_id
        self.tickets.append(ticket)

        # Начисляем бонусные баллы
        self.loyalty_points += int(price * 0.01)  # 1% от суммы

        return ticket

    def enter_oceanarium(self, ticket: Ticket) -> bool:
        """Входит в океанариум по билету."""
        if ticket in self.tickets and ticket.use_ticket():
            visit = {
                "visit_id": str(uuid.uuid4()),
                "entry_time": datetime.now(),
                "ticket_id": ticket.ticket_id,
                "exit_time": None
            }
            self.visit_history.append(visit)
            return True
        return False

    def exit_oceanarium(self) -> bool:
        """Выходит из океанариума."""
        # Находим последний незавершённый визит
        for visit in reversed(self.visit_history):
            if visit["exit_time"] is None:
                visit["exit_time"] = datetime.now()
                return True
        return False

    def add_preference(self, preference: str) -> None:
        """Добавляет предпочтение посетителя."""
        if preference not in self.preferences:
            self.preferences.append(preference)

    def upgrade_membership(self, new_type: str) -> bool:
        """Повышает уровень членства."""
        membership_levels = ["regular", "silver", "gold", "platinum"]
        current_index = membership_levels.index(self.membership_type)
        new_index = membership_levels.index(new_type)

        if new_index > current_index:
            self.membership_type = new_type
            return True
        return False
