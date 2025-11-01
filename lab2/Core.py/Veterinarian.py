class Veterinarian(Staff):
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int, medical_license: str):
        super().__init__(staff_id, name, "Veterinarian", salary, experience_years)
        self.medical_license = medical_license
        self.surgeries_performed = 0
        self.specializations = []
        self.patients_treated = []
        self.emergency_calls = 0
        self.access_level = 4

    def perform_daily_tasks(self) -> List[str]:
        return [
            "Медицинский осмотр животных",
            "Анализ медицинских записей",
            "Подготовка лекарственных препаратов",
            "Консультации с тренерами"
        ]

    def examine_animal(self, animal: Animal) -> Dict[str, any]:
        examination_result = {
            "temperature": random.uniform(36, 39),
            "heart_rate": random.randint(60, 120),
            "respiratory_rate": random.randint(12, 30),
            "weight": animal.weight,
            "overall_health": animal.check_health(),
            "recommendations": []
        }

        if examination_result["temperature"] > 38.5:
            examination_result["recommendations"].append("Контроль температуры")

        self.patients_treated.append(animal.animal_id)
        return examination_result

    def prescribe_treatment(self, animal: Animal, condition: str) -> List[str]:
        treatments = {
            "infection": ["Антибиотики", "Покой", "Контроль температуры"],
            "injury": ["Обезболивающие", "Перевязка", "Ограничение движения"],
            "stress": ["Успокоительные", "Изменение среды", "Сокращение контактов"]
        }
        return treatments.get(condition, ["Общеукрепляющие препараты"])
