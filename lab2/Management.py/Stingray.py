class Stingray(MarineAnimal):
    """
    Класс ската.
    """
    
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Stingray", age, weight, 92.0, 100)
        self.wingspan = random.uniform(0.5, 3.0)
        self.sting_barb_count = random.randint(1, 3)
        self.electrical_output = random.uniform(0, 220)
        self.burial_depth = random.uniform(5, 30)
        self.sand_preference = random.choice(["fine", "coarse", "mixed"])

    def get_feeding_requirements(self) -> Dict[str, float]:
        base_food = self.weight * 0.06
        return {
            "mollusks": base_food * 0.4,
            "worms": base_food * 0.3,
            "small_fish": base_food * 0.3
        }

    def get_habitat_requirements(self) -> Dict[str, any]:
        return {
            "water_type": "saltwater",
            "temperature_range": (20, 28),
            "substrate": "sandy",
            "depth_minimum": 2,
            "sand_type": self.sand_preference
        }

    def bury_in_sand(self) -> bool:
        """Зарывается в песок."""
        self.stress_level = max(0, self.stress_level - 15)
        self.activity_level = max(0, self.activity_level - 5)
        return True

    def electric_shock(self, voltage: float) -> bool:
        """Производит электрический разряд."""
        if self.electrical_output > 0:
            can_shock = voltage <= self.electrical_output
            if can_shock:
                self.energy_level = max(0, self.energy_level - 10)
            return can_shock
        return False

    def glide(self, distance: float) -> float:
        """Плавает парящим движением."""
        energy_cost = distance * 0.1
        if self.energy_level >= energy_cost:
            self.energy_level -= energy_cost
            self.activity_level = min(100, self.activity_level + 8)
            return distance
        return 0
