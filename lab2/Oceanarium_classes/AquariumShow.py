class AquariumShow:
    """Класс для управления шоу в океанариуме."""
    
    def __init__(self, show_id: str, name: str, duration: int):
        self.show_id = show_id
        self.name = name
        self.duration = duration
        self.schedule = []
        self.animals_involved = []
        self.trainers_required = []
        self.equipment_needed = []
        self.max_audience = random.randint(100, 500)
        self.show_type = ""
        self.difficulty_level = random.randint(1, 5)
        self.success_rate = random.uniform(75, 95)
        self.rehearsals_completed = 0

    def add_animal(self, animal: Animal, role: str) -> bool:
        """Добавляет животное в шоу."""
        if animal.animal_id not in [a.animal_id for a in self.animals_involved]:
            show_animal = {
                "animal": animal,
                "role": role,
                "performance_rating": random.uniform(60, 95),
                "rehearsals_attended": 0
            }
            self.animals_involved.append(show_animal)
            return True
        return False

    def schedule_show(self, date_time: datetime, location: str) -> str:
        """Планирует показ шоу."""
        schedule_id = f"SHOW_{len(self.schedule):04d}"
        show_schedule = {
            "schedule_id": schedule_id,
            "date_time": date_time,
            "location": location,
            "status": "scheduled",
            "audience_count": 0,
            "duration": self.duration,
            "trainers_assigned": []
        }
        self.schedule.append(show_schedule)
        return schedule_id

    def conduct_rehearsal(self) -> Dict[str, any]:
        """Проводит репетицию шоу."""
        rehearsal_result = {
            "show_id": self.show_id,
            "rehearsal_date": datetime.now(),
            "animals_participated": len(self.animals_involved),
            "success_rate": self.success_rate,
            "issues_found": random.randint(0, 3),
            "duration": self.duration * 0.8
        }

        for animal_data in self.animals_involved:
            animal_data["rehearsals_attended"] += 1
            animal_data["performance_rating"] = min(100, 
                animal_data["performance_rating"] + random.uniform(0.5, 2))

        self.rehearsals_completed += 1
        self.success_rate = min(98, self.success_rate + 0.5)
        
        return rehearsal_result

    def assign_trainer(self, trainer: Trainer) -> bool:
        """Назначает тренера на шоу."""
        if isinstance(trainer, Trainer) and trainer not in self.trainers_required:
            self.trainers_required.append(trainer)
            return True
        return False

    def calculate_show_readiness(self) -> float:
        """Рассчитывает готовность шоу."""
        base_readiness = self.success_rate
        rehearsal_bonus = min(20, self.rehearsals_completed * 2)
        animal_experience = sum(
            animal_data["performance_rating"] 
            for animal_data in self.animals_involved
        ) / max(1, len(self.animals_involved))
        
        readiness = (base_readiness + rehearsal_bonus + animal_experience) / 3
        return min(100, readiness)
