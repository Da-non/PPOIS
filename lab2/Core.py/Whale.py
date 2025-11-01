class Whale(MarineAnimal):
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Whale", age, weight, 90.0, 200)
        self.lung_capacity = weight * 0.5
        self.dive_depth_max = random.randint(500, 2000)
        self.song_frequency = random.uniform(10, 4000)
        self.blubber_thickness = random.uniform(10, 50)
        self.baleen_plates = random.randint(200, 400) if "Baleen" in name else 0

    def dive(self, target_depth: int) -> bool:
        if target_depth <= self.dive_depth_max:
            self.activity_level += 20
            return True
        return False

    def sing(self) -> str:
        song_duration = random.uniform(10, 60)
        self.stress_level = max(0, self.stress_level - 15)
        return f"Пение на частоте {self.song_frequency} Гц в течение {song_duration} минут"

    def filter_feed(self, plankton_density: float) -> float:
        if self.baleen_plates > 0:
            food_collected = plankton_density * self.baleen_plates * 0.01
            return food_collected
        return 0
