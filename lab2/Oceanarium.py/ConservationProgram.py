class ConservationProgram:
    """Программа сохранения морских видов."""
    
    def __init__(self, program_id: str, species: str, goal: str):
        self.program_id = program_id
        self.species = species
        self.goal = goal
        self.budget = 0.0
        self.researchers = []
        self.success_rate = 0.0
        self.start_date = datetime.now()
        self.end_date = None
        self.milestones = []
        self.partners = []
        self.fieldwork_locations = []
        self.publications = []

    def allocate_budget(self, amount: float) -> bool:
        """Выделяет бюджет для программы."""
        if amount > 0:
            self.budget += amount
            return True
        return False

    def add_researcher(self, researcher: ResearchScientist) -> bool:
        """Добавляет исследователя в программу."""
        if isinstance(researcher, ResearchScientist):
            self.researchers.append(researcher)
            self.success_rate = min(100, self.success_rate + 5)
            return True
        return False

    def add_milestone(self, milestone: str, deadline: datetime) -> str:
        """Добавляет веху в программу."""
        milestone_id = f"MILESTONE_{len(self.milestones):04d}"
        self.milestones.append({
            "id": milestone_id,
            "description": milestone,
            "deadline": deadline,
            "completed": False,
            "completion_date": None
        })
        return milestone_id

    def complete_milestone(self, milestone_id: str) -> bool:
        """Отмечает веху как выполненную."""
        for milestone in self.milestones:
            if milestone["id"] == milestone_id:
                milestone["completed"] = True
                milestone["completion_date"] = datetime.now()
                self.success_rate = min(100, self.success_rate + 10)
                return True
        return False

    def publish_findings(self, title: str, journal: str) -> str:
        """Публикует результаты исследований."""
        publication_id = f"PUB_{len(self.publications):04d}"
        publication = {
            "id": publication_id,
            "title": title,
            "journal": journal,
            "date": datetime.now(),
            "program": self.program_id,
            "impact_factor": random.uniform(1.0, 8.0)
        }
        self.publications.append(publication)
        return publication_id
