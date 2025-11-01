class TicketOffice:
    """
    Касса океанариума.

    Attributes:
        office_id (str): Идентификатор кассы
        cashier_name (str): Имя кассира
        ticket_prices (Dict): Цены на билеты
        daily_sales (List): Продажи за день
    """

    def __init__(self, office_id: str, cashier_name: str):
        self.office_id = office_id
        self.cashier_name = cashier_name
        self.ticket_prices = {
            "adult": 1500.0,
            "child": 800.0,
            "student": 1200.0,
            "senior": 1000.0,
            "family": 4000.0,
            "vip": 3000.0
        }
        self.daily_sales = []
        self.cash_register = 0.0
        self.shift_start_time = None
        self.shift_end_time = None
        self.payment_processor = PaymentProcessor(f"POS_{office_id}")
        self.discount_codes = {}
        self.promotional_offers = []

    def start_shift(self, initial_cash: float) -> None:
        """Начинает рабочую смену."""
        self.shift_start_time = datetime.now()
        self.cash_register = initial_cash
        self.daily_sales.clear()

    def sell_ticket(self, visitor: Visitor, ticket_type: str, payment_method: str,
                   card: Optional[CreditCard] = None, discount_code: str = None) -> Ticket:
        """Продаёт билет посетителю."""
        if ticket_type not in self.ticket_prices:
            raise ValueError(f"Неизвестный тип билета: {ticket_type}")

        base_price = self.ticket_prices[ticket_type]
        final_price = self.apply_discounts(base_price, visitor, discount_code)

        # Продаём билет через посетителя
        ticket = visitor.purchase_ticket(ticket_type, final_price, self.payment_processor,
                                       payment_method, card)

        # Записываем продажу
        sale = {
            "sale_id": str(uuid.uuid4()),
            "ticket_id": ticket.ticket_id,
            "visitor_id": visitor.visitor_id,
            "ticket_type": ticket_type,
            "price": final_price,
            "payment_method": payment_method,
            "cashier": self.cashier_name,
            "timestamp": datetime.now()
        }
        self.daily_sales.append(sale)

        if payment_method == "cash":
            self.cash_register += final_price

        return ticket

    def apply_discounts(self, base_price: float, visitor: Visitor, discount_code: str = None) -> float:
        """Применяет скидки к цене билета."""
        final_price = base_price

        # Скидка по возрасту
        if visitor.age >= 65:
            final_price *= 0.9  # 10% скидка для пенсионеров
        elif visitor.age <= 12:
            final_price *= 0.5  # 50% скидка для детей

        # Скидка по членству
        membership_discounts = {
            "silver": 0.05,
            "gold": 0.10,
            "platinum": 0.15
        }
        if visitor.membership_type in membership_discounts:
            final_price *= (1 - membership_discounts[visitor.membership_type])

        # Промокод
        if discount_code and discount_code in self.discount_codes:
            discount = self.discount_codes[discount_code]
            final_price *= (1 - discount)

        return final_price

    def end_shift(self) -> Dict:
        """Завершает рабочую смену."""
        self.shift_end_time = datetime.now()

        total_sales = sum(sale["price"] for sale in self.daily_sales)
        tickets_sold = len(self.daily_sales)

        shift_report = {
            "cashier": self.cashier_name,
            "shift_start": self.shift_start_time,
            "shift_end": self.shift_end_time,
            "total_sales": total_sales,
            "tickets_sold": tickets_sold,
            "cash_in_register": self.cash_register,
            "payment_methods": self.get_payment_method_breakdown()
        }

        return shift_report

    def get_payment_method_breakdown(self) -> Dict[str, int]:
        """Возвращает разбивку по методам оплаты."""
        breakdown = {}
        for sale in self.daily_sales:
            method = sale["payment_method"]
            breakdown[method] = breakdown.get(method, 0) + 1
        return breakdown

    def add_discount_code(self, code: str, discount_percent: float) -> None:
        """Добавляет промокод."""
        self.discount_codes[code] = discount_percent / 100

    def add_promotional_offer(self, offer_name: str, description: str,
                            discount_percent: float, valid_until: datetime) -> None:
        """Добавляет рекламное предложение."""
        offer = {
            "offer_id": str(uuid.uuid4()),
            "name": offer_name,
            "description": description,
            "discount": discount_percent / 100,
            "valid_until": valid_until,
            "active": True
        }
        self.promotional_offers.append(offer)
