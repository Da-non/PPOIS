class Shark(MarineAnimal):
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Shark", age, weight, 98.0, 50)
        self.aggression_level = random.randint(5, 10)
        self.hunting_success_rate = random.uniform(60, 90)
        self.teeth_count = random.randint(200, 300)
        self.electrical_sense_range = random.uniform(1, 5)
        self.bite_force = weight * 10

    def hunt(self, prey_type: str) -> bool:
        success = random.random() < (self.hunting_success_rate / 100)
        if success:
            self.activity_level += 15
            self.stress_level = max(0, self.stress_level - 10)
        return success

    def detect_electrical_field(self, distance: float) -> bool:
        return distance <= self.electrical_sense_range

    def shed_teeth(self) -> int:
        shed_count = random.randint(1, 10)
        return shed_count
