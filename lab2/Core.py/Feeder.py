class Feeder(Staff):
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int):
        super().__init__(staff_id, name, "Feeder", salary, experience_years)
        self.feeding_schedule = {}
        self.food_inventory = {}
        self.animals_assigned = []
        self.feeding_logs = []
        self.nutrition_knowledge = random.uniform(60, 95)
        self.access_level = 2

    def perform_daily_tasks(self) -> List[str]:
        return [
            "Кормление назначенных животных",
            "Проверка качества корма",
            "Обновление инвентаря корма",
            "Ведение журнала кормления"
        ]

    def feed_animal(self, animal: Animal, food_type: str, amount: float) -> bool:
        if food_type in self.food_inventory and self.food_inventory[food_type] >= amount:
            success = animal.feed(food_type, amount)
            if success:
                self.food_inventory[food_type] -= amount
                self.feeding_logs.append({
                    "animal_id": animal.animal_id,
                    "food_type": food_type,
                    "amount": amount,
                    "timestamp": datetime.now()
                })
            return success
        return False

    def check_food_quality(self, food_type: str) -> bool:
        freshness = random.uniform(0, 100)
        return freshness > 70

    def restock_food(self, food_type: str, amount: float) -> None:
        if food_type in self.food_inventory:
            self.food_inventory[food_type] += amount
        else:
            self.food_inventory[food_type] = amount
