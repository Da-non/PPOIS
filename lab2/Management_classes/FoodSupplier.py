class FoodSupplier:
    """
    Класс поставщика корма.
    """
    
    def __init__(self, supplier_id: str, company_name: str):
        self.supplier_id = supplier_id
        self.company_name = company_name
        self.food_types = []
        self.delivery_schedule = {}
        self.quality_rating = random.uniform(80, 98)
        self.price_per_kg = {}
        self.reliability_score = random.uniform(85, 99)
        self.contact_info = {}
        self.payment_terms = random.randint(15, 60)
        self.delivery_vehicles = []
        self.certifications = []

    def add_food_type(self, food_type: str, price_per_kg: float) -> None:
        """Добавляет тип корма."""
        if food_type not in self.food_types:
            self.food_types.append(food_type)
            self.price_per_kg[food_type] = price_per_kg

    def schedule_delivery(self, food_type: str, quantity_kg: float, delivery_date: datetime) -> Dict[str, any]:
        """Планирует поставку корма."""
        if food_type not in self.food_types:
            raise ValueError(f"Поставщик не предоставляет {food_type}")

        delivery_id = f"DEL_{len(self.delivery_schedule):04d}"
        total_cost = quantity_kg * self.price_per_kg[food_type]
        
        delivery = {
            "delivery_id": delivery_id,
            "food_type": food_type,
            "quantity": quantity_kg,
            "price_per_kg": self.price_per_kg[food_type],
            "total_cost": total_cost,
            "delivery_date": delivery_date,
            "status": "scheduled",
            "supplier": self.company_name
        }

        self.delivery_schedule[delivery_id] = delivery
        return delivery

    def deliver_food(self, delivery_id: str) -> bool:
        """Выполняет поставку корма."""
        if delivery_id in self.delivery_schedule:
            delivery = self.delivery_schedule[delivery_id]

            # Симуляция успешности поставки с учетом надежности
            delivery_success = random.random() < (self.reliability_score / 100)
            
            if delivery_success:
                delivery["status"] = "delivered"
                delivery["actual_delivery_date"] = datetime.now()
                delivery["quality_check"] = self.quality_rating + random.uniform(-5, 5)
                return True
            else:
                delivery["status"] = "delayed"
                delivery["new_delivery_date"] = delivery["delivery_date"] + timedelta(days=1)
                return False
        return False

    def check_quality(self, delivery_id: str) -> float:
        """Проверяет качество поставленного корма."""
        if delivery_id in self.delivery_schedule:
            quality_score = self.quality_rating + random.uniform(-5, 5)
            return max(0, min(100, quality_score))
        return 0.0

    def add_delivery_vehicle(self, vehicle_type: str, capacity_kg: float) -> None:
        """Добавляет транспортное средство."""
        vehicle = {
            "type": vehicle_type,
            "capacity": capacity_kg,
            "status": "available"
        }
        self.delivery_vehicles.append(vehicle)

    def update_reliability(self, successful_deliveries: int, total_deliveries: int) -> None:
        """Обновляет показатель надежности."""
        if total_deliveries > 0:
            self.reliability_score = (successful_deliveries / total_deliveries) * 100
