class ConservationProgram:
    """Программа сохранения морских видов."""
    
    def __init__(self, program_id: str, species: str, goal: str):
        self.program_id = program_id
        self.species = species
        self.goal = goal
        self.budget = 0.0
        self.researchers = []
        self.success_rate = random.uniform(50, 90)
        self.start_date = datetime.now()
        self.end_date = datetime.now() + timedelta(days=365 * 3)  # 3 года
        self.milestones = []
        self.funding_sources = []
        self.published_research = []

    def allocate_budget(self, amount: float) -> bool:
        """Выделяет бюджет программе."""
        if amount > 0:
            self.budget += amount
            return True
        return False

    def add_researcher(self, researcher: ResearchScientist) -> bool:
        """Добавляет исследователя в программу."""
        if researcher.staff_id not in [r.staff_id for r in self.researchers]:
            self.researchers.append(researcher)
            return True
        return False

    def add_milestone(self, milestone: str, deadline: datetime) -> bool:
        """Добавляет веху в программу."""
        milestone_data = {
            "id": f"MILESTONE_{len(self.milestones) + 1}",
            "description": milestone,
            "deadline": deadline,
            "completed": False,
            "completion_date": None
        }
        self.milestones.append(milestone_data)
        return True

    def complete_milestone(self, milestone_id: str) -> bool:
        """Отмечает веху как выполненную."""
        for milestone in self.milestones:
            if milestone["id"] == milestone_id:
                milestone["completed"] = True
                milestone["completion_date"] = datetime.now()
                self.success_rate += 2.0  # Увеличиваем успешность
                return True
        return False

    def publish_research(self, title: str, findings: str) -> str:
        """Публикует исследование по программе."""
        publication_id = f"PUB_{len(self.published_research) + 1}"
        publication = {
            "id": publication_id,
            "title": title,
            "findings": findings,
            "publication_date": datetime.now(),
            "authors": [r.name for r in self.researchers]
        }
        self.published_research.append(publication)
        return publication_id

    def get_program_progress(self) -> Dict[str, Any]:
        """Возвращает прогресс программы."""
        completed_milestones = len([m for m in self.milestones if m["completed"]])
        total_milestones = len(self.milestones)
        
        return {
            "program_id": self.program_id,
            "species": self.species,
            "progress": (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0,
            "budget_utilized": self.budget,
            "researchers_count": len(self.researchers),
            "publications_count": len(self.published_research),
            "success_rate": self.success_rate
        }
