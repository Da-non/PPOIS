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
        self.max_spectators = random.randint(50, 300)
        self.show_type = random.choice(["dolphin", "seal", "diving", "feeding"])
        self.difficulty_level = random.randint(1, 5)
        self.success_rate = random.uniform(80, 98)

    def schedule_show(self, show_date: datetime, location: str, trainer_ids: List[str]) -> bool:
        """Планирует показ шоу."""
        show_slot = {
            "show_id": self.show_id,
            "date": show_date,
            "location": location,
            "trainers": trainer_ids,
            "status": "scheduled",
            "spectators_count": 0
        }
        self.schedule.append(show_slot)
        return True

    def add_animal(self, animal: Animal) -> bool:
        """Добавляет животное в шоу."""
        if animal.animal_id not in [a.animal_id for a in self.animals_involved]:
            self.animals_involved.append(animal)
            animal.activity_level += 5  # Животные возбуждаются перед шоу
            return True
        return False

    def add_trainer(self, trainer: Trainer) -> bool:
        """Добавляет тренера в шоу."""
        if trainer.staff_id not in [t.staff_id for t in self.trainers_required]:
            self.trainers_required.append(trainer)
            return True
        return False

    def conduct_show(self) -> Dict[str, Any]:
        """Проводит шоу."""
        if len(self.animals_involved) == 0:
            raise ValueError("Нет животных для шоу")
        
        if len(self.trainers_required) == 0:
            raise ValueError("Нет тренеров для шоу")

        # Симуляция успешности шоу
        show_success = random.random() < (self.success_rate / 100)
        spectator_satisfaction = random.uniform(70, 99)
        
        # Влияние на животных
        for animal in self.animals_involved:
            animal.activity_level += random.randint(10, 20)
            animal.stress_level += random.randint(5, 15)

        result = {
            "show_id": self.show_id,
            "name": self.name,
            "duration": self.duration,
            "animals_count": len(self.animals_involved),
            "trainers_count": len(self.trainers_required),
            "success": show_success,
            "spectator_satisfaction": spectator_satisfaction,
            "timestamp": datetime.now()
        }

        return result

    def get_show_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику шоу."""
        return {
            "total_scheduled": len(self.schedule),
            "animals_involved": len(self.animals_involved),
            "trainers_required": len(self.trainers_required),
            "success_rate": self.success_rate,
            "max_spectators": self.max_spectators
        }

