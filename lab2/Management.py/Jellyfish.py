class Jellyfish(MarineAnimal):
    """
    Класс медузы.
    """
    
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Jellyfish", age, weight, 100.0, 5)
        self.tentacle_length = random.uniform(10, 100)
        self.toxicity_level = random.randint(1, 8)
        self.pulsation_rate = random.uniform(20, 80)
        self.bioluminescence = random.choice([True, False])
        self.regeneration_ability = random.uniform(50, 95)

    def get_feeding_requirements(self) -> Dict[str, float]:
        base_food = self.weight * 0.02
        return {
            "plankton": base_food * 0.8,
            "small_fish": base_food * 0.2
        }

    def get_habitat_requirements(self) -> Dict[str, any]:
        return {
            "water_type": "saltwater",
            "temperature_range": (18, 28),
            "current_strength": "gentle",
            "lighting": "dim" if self.bioluminescence else "moderate"
        }

    def pulsate(self) -> float:
        """Совершает пульсирующие движения."""
        self.activity_level = min(100, self.activity_level + 2)
        return self.pulsation_rate

    def sting(self, target_distance: float) -> bool:
        """Жалит цель щупальцами."""
        if target_distance <= self.tentacle_length / 100:
            return self.toxicity_level > 3
        return False

    def regenerate(self) -> float:
        """Регенерирует ткани."""
        regeneration_amount = random.uniform(1, 5)
        self.health = min(100, self.health + regeneration_amount)
        return regeneration_amount
