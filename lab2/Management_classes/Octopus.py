class Octopus(MarineAnimal):
    """
    Класс осьминога.
    """
    
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Octopus", age, weight, 95.0, 30)
        self.arm_count = 8
        self.intelligence_level = random.randint(7, 10)
        self.camouflage_ability = random.uniform(80, 95)
        self.ink_capacity = random.uniform(10, 50)
        self.sucker_strength = random.uniform(100, 500)
        self.problem_solving_skills = random.uniform(60, 95)

    def get_feeding_requirements(self) -> Dict[str, float]:
        base_food = self.weight * 0.08
        return {
            "crabs": base_food * 0.5,
            "fish": base_food * 0.3,
            "shrimp": base_food * 0.2
        }

    def get_habitat_requirements(self) -> Dict[str, any]:
        return {
            "water_type": "saltwater",
            "temperature_range": (15, 25),
            "hiding_places": True,
            "substrate": "rocky",
            "enrichment_toys": True
        }

    def camouflage(self) -> bool:
        """Маскируется под окружение."""
        success = random.random() < (self.camouflage_ability / 100)
        if success:
            self.stress_level = max(0, self.stress_level - 10)
        return success

    def release_ink(self) -> float:
        """Выпускает чернила."""
        if self.ink_capacity > 5:
            released = min(self.ink_capacity, 10)
            self.ink_capacity -= released
            self.stress_level = min(100, self.stress_level + 5)
            return released
        return 0

    def solve_puzzle(self, difficulty: int) -> bool:
        """Решает головоломку."""
        success_chance = (self.intelligence_level / 10) * (self.problem_solving_skills / 100)
        success = random.random() < success_chance
        if success:
            self.activity_level = min(100, self.activity_level + 15)
        return success

    def use_tool(self, tool_complexity: int) -> bool:
        """Использует инструмент."""
        return self.intelligence_level >= tool_complexity
