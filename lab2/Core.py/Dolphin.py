class Dolphin(MarineAnimal):
    """
    Класс дельфина.

    Attributes:
        intelligence_level (int): Уровень интеллекта (1-10)
        echolocation_range (float): Дальность эхолокации в метрах
        social_group (List[str]): Список ID других дельфинов в группе
    """

    def __init__(self, animal_id: str, name: str, age: int, weight: float):
        super().__init__(animal_id, name, "Dolphin", age, weight, 95.0, 10)
        self.intelligence_level = random.randint(7, 10)
        self.echolocation_range = random.uniform(100, 200)
        self.social_group = []
        self.tricks_learned = []
        self.communication_frequency = random.uniform(20, 150)  # кГц

    def perform_trick(self, trick_name: str) -> bool:
        """Выполняет трюк."""
        if trick_name in self.tricks_learned:
            self.activity_level += 5
            return True
        return False

    def learn_trick(self, trick_name: str) -> bool:
        """Изучает новый трюк."""
        if len(self.tricks_learned) < self.intelligence_level:
            self.tricks_learned.append(trick_name)
            return True
        return False

    def echolocate(self, target_distance: float) -> bool:
        """Использует эхолокацию."""
        return target_distance <= self.echolocation_range

    def communicate(self, other_dolphin: 'Dolphin') -> bool:
        """Общается с другим дельфином."""
        if other_dolphin.animal_id in self.social_group:
            self.stress_level = max(0, self.stress_level - 5)
            return True
        return False
