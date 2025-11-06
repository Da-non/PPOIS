class EducationalProgram:
    """
    Класс образовательной программы.
    """
    
    def __init__(self, program_id: str, name: str, target_audience: str, duration_minutes: int):
        self.program_id = program_id
        self.name = name
        self.target_audience = target_audience
        self.duration_minutes = duration_minutes
        self.learning_objectives = []
        self.required_animals = []
        self.materials_needed = []
        self.instructor = None
        self.participant_limit = random.randint(10, 30)
        self.effectiveness_rating = random.uniform(75, 95)
        self.sessions_conducted = 0
        self.feedback_scores = []

    def add_learning_objective(self, objective: str) -> None:
        """Добавляет учебную цель."""
        if objective not in self.learning_objectives:
            self.learning_objectives.append(objective)
            self.effectiveness_rating = min(100, self.effectiveness_rating + 1)

    def assign_instructor(self, instructor: Staff) -> bool:
        """Назначает инструктора программы."""
        if isinstance(instructor, (TourGuide, ResearchScientist)):
            self.instructor = instructor
            # Повышение эффективности при назначении опытного инструктора
            if hasattr(instructor, 'experience_years'):
                experience_bonus = min(10, instructor.experience_years)
                self.effectiveness_rating = min(100, self.effectiveness_rating + experience_bonus)
            return True
        return False

    def conduct_session(self, participants: List[Visitor]) -> Dict[str, any]:
        """Проводит образовательную сессию."""
        if len(participants) > self.participant_limit:
            return {"error": "Превышен лимит участников"}

        if not self.instructor:
            return {"error": "Не назначен инструктор"}

        if not participants:
            return {"error": "Нет участников"}

        # Расчет успешности сессии
        base_effectiveness = self.effectiveness_rating
        participant_ratio = len(participants) / self.participant_limit
        ratio_bonus = participant_ratio * 10
        
        session_effectiveness = base_effectiveness + ratio_bonus
        session_effectiveness = max(50, min(100, session_effectiveness))

        session_result = {
            "program_id": self.program_id,
            "program_name": self.name,
            "participant_count": len(participants),
            "duration": self.duration_minutes,
            "effectiveness": session_effectiveness,
            "objectives_covered": len(self.learning_objectives),
            "instructor": self.instructor.name,
            "timestamp": datetime.now(),
            "target_audience": self.target_audience
        }

        self.sessions_conducted += 1
        return session_result

    def evaluate_effectiveness(self, feedback_scores: List[float]) -> float:
        """Оценивает эффективность программы."""
        if feedback_scores:
            self.feedback_scores.extend(feedback_scores)
            average_score = sum(self.feedback_scores) / len(self.feedback_scores)
            # Взвешенное среднее с предыдущим рейтингом
            self.effectiveness_rating = (self.effectiveness_rating + average_score * 2) / 3
            return self.effectiveness_rating
        return self.effectiveness_rating

    def add_required_animal(self, animal_species: str) -> None:
        """Добавляет требуемое животное для программы."""
        if animal_species not in self.required_animals:
            self.required_animals.append(animal_species)

    def add_material(self, material: str) -> None:
        """Добавляет необходимый материал."""
        if material not in self.materials_needed:
            self.materials_needed.append(material)
