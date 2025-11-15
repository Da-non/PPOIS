class GameShop(GameEntity):
    """
    Класс игрового магазина.

    Attributes:
        shop_id (str): Уникальный идентификатор магазина
        name (str): Название магазина
        shop_type (str): Тип магазина
        items (Dict[str, Dict]): Товары магазина
        currency_accepted (List[str]): Принимаемые валюты
    """

    def __init__(self, shop_id: str, name: str, shop_type: str = "general"):
        super().__init__(shop_id, name)
        self.shop_type = shop_type
        self.items = {}
        self.currency_accepted = ["gold", "gems", "tokens"]
        self.discounts = {}
        self.sales = []
        self.shop_owner = None
        self.location = ""
        self.opening_hours = {"start": 0, "end": 24}
        self.is_open = True
        self.reputation = 100
        self.sales_history = []
        self.daily_revenue = 0.0
        self.inventory = {}
        self.restock_schedule = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние магазина."""
        # Проверяем время работы
        current_hour = datetime.now().hour
        self.is_open = self.opening_hours["start"] <= current_hour < self.opening_hours["end"]
        
        # Обновляем репутацию
        if random.random() < 0.001:  # 0.1% шанс изменения репутации
            self.reputation += random.uniform(-1, 1)
            self.reputation = max(0, min(100, self.reputation))

    def add_item(self, item: GameItem, price: int, currency_type: str, stock: int = -1) -> bool:
        """Добавляет товар в магазин."""
        if currency_type not in self.currency_accepted:
            return False
        
        item_key = f"{item.entity_id}_{currency_type}"
        self.items[item_key] = {
            "item": item,
            "price": price,
            "currency_type": currency_type,
            "stock": stock,
            "original_price": price,
            "discount": 0.0
        }
        
        if stock > 0:
            self.inventory[item.entity_id] = stock
        
        return True

    def remove_item(self, item_id: str, currency_type: str) -> bool:
        """Удаляет товар из магазина."""
        item_key = f"{item_id}_{currency_type}"
        if item_key in self.items:
            del self.items[item_key]
            if item_id in self.inventory:
                del self.inventory[item_id]
            return True
        return False

    def buy_item(self, player: Player, item_id: str, currency_type: str, quantity: int = 1) -> bool:
        """Покупает товар."""
        if not self.is_open:
            return False
        item_key = f"{item_id}_{currency_type}"
        if item_key not in self.items:
            return False
        item_data = self.items[item_key]
        if item_data["stock"] != -1 and item_data["stock"] < quantity:
            return False
        total_price = item_data["price"] * quantity
        if item_data["discount"] > 0:
            total_price *= (1 - item_data["discount"])
        if not player.spend_currency(currency_type, int(total_price)):
            return False
        base_item: GameItem = item_data["item"]
        for _ in range(quantity):
            item_copy = GameItem(
                f"{base_item.entity_id}_copy_{uuid.uuid4().hex[:8]}",
                base_item.name,
                base_item.item_type,
                base_item.rarity,
            )
            item_copy.value = base_item.value
            item_copy.required_level = base_item.required_level
            if not player.add_item(item_copy):
                player.add_currency(currency_type, int(total_price))
                return False
        if item_data["stock"] != -1:
            item_data["stock"] -= quantity
        sale = {
            "sale_id": str(uuid.uuid4()),
            "player_id": player.entity_id,
            "item_id": item_id,
            "quantity": quantity,
            "price": total_price,
            "currency_type": currency_type,
            "timestamp": datetime.now(),
        }
        self.sales_history.append(sale)
        self.daily_revenue += total_price
        return True

    def sell_item(self, player: Player, item: GameItem, currency_type: str) -> bool:
        """Продает предмет игрока."""
        if currency_type not in self.currency_accepted:
            return False
        sell_price = int(item.value * 0.5)
        if not player.remove_item(item.entity_id):
            return False
        player.add_currency(currency_type, sell_price)
        purchase = {
            "purchase_id": str(uuid.uuid4()),
            "player_id": player.entity_id,
            "item_id": item.entity_id,
            "price": sell_price,
            "currency_type": currency_type,
            "timestamp": datetime.now(),
        }
        self.sales_history.append(purchase)
        return True

    def set_discount(self, item_id: str, currency_type: str, discount_percent: float) -> bool:
        """Устанавливает скидку на товар."""
        item_key = f"{item_id}_{currency_type}"
        if item_key in self.items:
            self.items[item_key]["discount"] = min(1.0, max(0.0, discount_percent / 100))
            return True
        return False

    def start_sale(self, sale_name: str, discount_percent: float, duration_hours: int) -> str:
        """Начинает распродажу."""
        sale_id = str(uuid.uuid4())
        sale = {
            "sale_id": sale_id,
            "name": sale_name,
            "discount_percent": discount_percent,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=duration_hours),
            "is_active": True
        }
        self.sales.append(sale)
        return sale_id

    def end_sale(self, sale_id: str) -> bool:
        """Завершает распродажу."""
        for sale in self.sales:
            if sale["sale_id"] == sale_id and sale["is_active"]:
                sale["is_active"] = False
                sale["end_time"] = datetime.now()
                return True
        return False
