class ResearchScientist(Staff):
    """
    Класс учёного-исследователя.
    """
    
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int, research_field: str):
        super().__init__(staff_id, name, "Research Scientist", salary, experience_years)
        self.research_field = research_field
        self.publications = []
        self.current_projects = []
        self.research_grants = []
        self.laboratory_access = True
        self.access_level = 6
        self.research_focus = []
        self.collaborators = []

    def perform_daily_tasks(self) -> List[str]:
        tasks = [
            "Проведение исследований",
            "Сбор и анализ данных",
            "Написание научных статей",
            "Наблюдение за животными",
            "Участие в конференциях",
            "Руководство исследовательской группой"
        ]
        self.workload = min(100, self.workload + 35)
        return tasks

    def conduct_study(self, animal: Animal, study_type: str, duration_days: int) -> Dict[str, any]:
        """Проводит исследование животного."""
        study_id = f"STUDY_{len(self.current_projects):04d}"
        
        # Влияние на животное
        animal_stress_increase = random.uniform(1, 5)
        animal.stress_level = min(100, animal.stress_level + animal_stress_increase)

        study_result = {
            "study_id": study_id,
            "animal_id": animal.animal_id,
            "animal_species": animal.species,
            "study_type": study_type,
            "duration": duration_days,
            "data_points": random.randint(50, 500),
            "findings": f"Исследование {study_type} для {animal.species}",
            "start_date": datetime.now(),
            "researcher": self.name,
            "animal_stress_impact": animal_stress_increase,
            "success_rate": random.uniform(75, 95)
        }

        self.current_projects.append({
            "id": study_id,
            "type": study_type,
            "animal": animal.animal_id,
            "status": "active"
        })
        
        self.workload = min(100, self.workload + duration_days * 2)
        return study_result

    def publish_research(self, title: str, journal: str) -> str:
        """Публикует исследование."""
        publication_id = f"PUB_{len(self.publications):04d}"
        impact_factor = random.uniform(1.0, 10.0)
        
        publication = {
            "publication_id": publication_id,
            "title": title,
            "journal": journal,
            "author": self.name,
            "publication_date": datetime.now(),
            "field": self.research_field,
            "impact_factor": impact_factor,
            "citations": 0
        }
        
        self.publications.append(publication)
        self.workload = min(100, self.workload + 20)
        return publication_id

    def apply_for_grant(self, grant_amount: float, project_description: str) -> bool:
        """Подаёт заявку на грант."""
        base_success_rate = 0.3
        publications_bonus = len(self.publications) * 0.05
        experience_bonus = self.experience_years * 0.02
        
        success_rate = base_success_rate + publications_bonus + experience_bonus
        success_rate = min(0.8, success_rate)

        if random.random() < success_rate:
            grant = {
                "amount": grant_amount,
                "description": project_description,
                "approval_date": datetime.now(),
                "duration_months": random.randint(12, 36),
                "id": f"GRANT_{len(self.research_grants):04d}"
            }
            self.research_grants.append(grant)
            return True
        return False

    def add_research_focus(self, focus_area: str) -> None:
        """Добавляет область исследований."""
        if focus_area not in self.research_focus:
            self.research_focus.append(focus_area)
