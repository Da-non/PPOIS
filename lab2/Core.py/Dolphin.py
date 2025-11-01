class Dolphin(MarineAnimal):
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Dolphin", age, weight, 95.0, 10)
        self.intelligence_level = random.randint(7, 10)
        self.echolocation_range = random.uniform(100, 200)
        self.social_group = []
        self.tricks_learned = []
        self.communication_frequency = random.uniform(20, 150)

    def perform_trick(self, trick_name: str) -> bool:
        if trick_name in self.tricks_learned:
            self.activity_level += 5
            return True
        return False

    def learn_trick(self, trick_name: str) -> bool:
        if len(self.tricks_learned) < self.intelligence_level:
            self.tricks_learned.append(trick_name)
            return True
        return False

    def echolocate(self, target_distance: float) -> bool:
        return target_distance <= self.echolocation_range

    def communicate(self, other_dolphin: 'Dolphin') -> bool:
        if other_dolphin.animal_id in self.social_group:
            self.stress_level = max(0, self.stress_level - 5)
            return True
        return False
