class Ticket:
    """
    Класс билета.

    Attributes:
        ticket_id (str): Уникальный идентификатор билета
        ticket_type (str): Тип билета
        price (float): Цена билета
        valid_from (datetime): Действителен с
        valid_until (datetime): Действителен до
    """

    def __init__(self, ticket_type: str, price: float, validity_hours: int = 24):
        self.ticket_id = str(uuid.uuid4())
        self.ticket_type = ticket_type
        self.price = price
        self.valid_from = datetime.now()
        self.valid_until = datetime.now() + timedelta(hours=validity_hours)
        self.is_used = False
        self.purchase_time = datetime.now()
        self.visitor_id = None
        self.entry_time = None
        self.exit_time = None
        self.special_permissions = []

    def validate(self) -> bool:
        """Проверяет действительность билета."""
        current_time = datetime.now()
        if current_time < self.valid_from or current_time > self.valid_until:
            raise TicketExpiredException(self.ticket_id, self.valid_until)
        return not self.is_used

    def use_ticket(self) -> bool:
        """Использует билет для входа."""
        if self.validate():
            self.is_used = True
            self.entry_time = datetime.now()
            return True
        return False

    def add_special_permission(self, permission: str) -> None:
        """Добавляет специальное разрешение к билету."""
        if permission not in self.special_permissions:
            self.special_permissions.append(permission)
