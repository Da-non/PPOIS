class MarineAnimal(Animal):
    def __init__(self, animal_id: str, name: str, species: str, age: int, weight: float,
                 salt_tolerance: float, depth_preference: int):
        super().__init__(animal_id, name, species, age, weight)
        self.salt_tolerance = salt_tolerance
        self.depth_preference = depth_preference
        self.swimming_speed = random.uniform(1.0, 15.0)
        self.oxygen_consumption = weight * 0.1
        self.territorial_radius = random.uniform(5, 50)

    def get_feeding_requirements(self) -> Dict[str, float]:
        base_food = self.weight * 0.05
        return {
            "fish": base_food * 0.6,
            "krill": base_food * 0.3,
            "seaweed": base_food * 0.1
        }

    def get_habitat_requirements(self) -> Dict[str, any]:
        return {
            "water_type": "saltwater",
            "temperature_range": (15, 25),
            "salinity": 35,
            "depth": self.depth_preference,
            "current_strength": "moderate"
        }

    def swim(self, distance: float) -> float:
        time_taken = distance / self.swimming_speed
        self.activity_level = max(0, self.activity_level - distance * 0.1)
        return time_taken
