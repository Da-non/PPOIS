class Turtle(MarineAnimal):
    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Sea Turtle", age, weight, 85.0, 20)
        self.shell_hardness = random.randint(7, 10)
        self.navigation_accuracy = random.uniform(85, 99)
        self.nesting_sites = []
        self.magnetic_sensitivity = random.uniform(0.1, 1.0)
        self.flipper_strength = random.uniform(50, 150)

    def navigate(self, destination: str) -> bool:
        success = random.random() < (self.navigation_accuracy / 100)
        if success:
            self.activity_level += 10
        return success

    def lay_eggs(self, nesting_site: str) -> int:
        if nesting_site in self.nesting_sites:
            egg_count = random.randint(50, 120)
            return egg_count
        return 0

    def retract_into_shell(self) -> bool:
        self.stress_level = max(0, self.stress_level - 20)
        return True
