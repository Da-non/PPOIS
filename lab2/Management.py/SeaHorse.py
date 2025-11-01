class SeaHorse(MarineAnimal):
    """
    Класс морского конька.
    """
    
    def __init__(self, animal_id: str, name: str, age: int, weight: float, gender: str):
        super().__init__(animal_id, name, "Sea Horse", age, weight, 88.0, 15)
        self.tail_length = random.uniform(5, 15)
        self.color_change_ability = random.choice([True, False])
        self.gender = gender
        self.pouch_capacity = random.randint(100, 2000) if gender == "male" else 0
        self.grip_strength = random.uniform(10, 50)
        self.current_color = "brown"

    def get_feeding_requirements(self) -> Dict[str, float]:
        base_food = self.weight * 0.15
        return {
            "brine_shrimp": base_food * 0.6,
            "copepods": base_food * 0.4
        }

    def get_habitat_requirements(self) -> Dict[str, any]:
        return {
            "water_type": "saltwater",
            "temperature_range": (22, 26),
            "vegetation": "sea_grass",
            "current_strength": "gentle",
            "anchoring_points": True
        }

    def grip_with_tail(self, object_strength: float) -> bool:
        """Хватается хвостом за объект."""
        success = self.grip_strength >= object_strength
        if success:
            self.stress_level = max(0, self.stress_level - 5)
        return success

    def change_color(self, target_color: str) -> bool:
        """Меняет цвет."""
        if self.color_change_ability:
            self.current_color = target_color
            self.stress_level = max(0, self.stress_level - 5)
            return True
        return False

    def carry_eggs(self, egg_count: int) -> bool:
        """Вынашивает икру (только самцы)."""
        if self.gender == "male" and egg_count <= self.pouch_capacity:
            self.health = min(100, self.health - 5)  # Небольшой стресс
            return True
        return False

    def vertical_swim(self, height: float) -> float:
        """Плавает вертикально."""
        energy_cost = height * 0.2
        if self.energy_level >= energy_cost:
            self.energy_level -= energy_cost
            return height
        return 0
