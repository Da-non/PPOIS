class Whale(MarineAnimal):
    """
    Класс кита.

    Attributes:
        lung_capacity (float): Объём лёгких в литрах
        dive_depth_max (int): Максимальная глубина погружения
        song_frequency (float): Частота пения в Гц
    """

    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Whale", age, weight, 90.0, 200)
        self.lung_capacity = weight * 0.5
        self.dive_depth_max = random.randint(500, 2000)
        self.song_frequency = random.uniform(10, 4000)
        self.blubber_thickness = random.uniform(10, 50)  # см
        self.baleen_plates = random.randint(200, 400) if "Baleen" in name else 0

    def dive(self, target_depth: int) -> bool:
        """Погружается на заданную глубину."""
        if target_depth <= self.dive_depth_max:
            self.activity_level += 20
            return True
        return False

    def sing(self) -> str:
        """Поёт песню."""
        song_duration = random.uniform(10, 60)  # минуты
        self.stress_level = max(0, self.stress_level - 15)
        return f"Пение на частоте {self.song_frequency} Гц в течение {song_duration} минут"

    def filter_feed(self, plankton_density: float) -> float:
        """Фильтрует планктон."""
        if self.baleen_plates > 0:
            food_collected = plankton_density * self.baleen_plates * 0.01
            return food_collected
        return 0
