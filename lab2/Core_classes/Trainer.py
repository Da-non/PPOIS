class Trainer(Staff):
    """
    Класс тренера животных.

    Attributes:
        specialization (str): Специализация тренера
        training_sessions_count (int): Количество проведённых тренировок
        animals_trained (List[str]): Список ID обученных животных
    """

    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int, specialization: str):
        super().__init__(staff_id, name, "Trainer", salary, experience_years)
        self.specialization = specialization
        self.training_sessions_count = 0
        self.animals_trained = []
        self.training_techniques = []
        self.safety_incidents = 0
        self.access_level = 3

    def perform_daily_tasks(self) -> List[str]:
        return [
            "Проведение тренировочной сессии",
            "Оценка поведения животных",
            "Подготовка корма для тренировок",
            "Обновление записей о тренировках"
        ]

    def train_animal(self, animal: Animal, skill: str) -> bool:
        """Тренирует животное."""
        if isinstance(animal, Dolphin) and self.specialization == "marine_mammals":
            success = animal.learn_trick(skill)
            if success:
                self.training_sessions_count += 1
                if animal.animal_id not in self.animals_trained:
                    self.animals_trained.append(animal.animal_id)
            return success
        return False

    def assess_animal_behavior(self, animal: Animal) -> Dict[str, any]:
        """Оценивает поведение животного."""
        assessment = {
            "activity_level": animal.activity_level,
            "stress_level": animal.stress_level,
            "health_status": animal.health_status,
            "trainability": random.uniform(1, 10),
            "aggression": random.uniform(1, 5)
        }
        return assessment
