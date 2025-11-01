class Manager(Staff):
    """
    Класс менеджера океанариума.
    """
    
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int, department: str):
        super().__init__(staff_id, name, "Manager", salary, experience_years)
        self.department = department
        self.team_size = random.randint(5, 20)
        self.decision_authority = random.randint(6, 10)
        self.meetings_per_week = random.randint(3, 8)
        self.budget_responsibility = random.uniform(100000, 1000000)
        self.access_level = 5
        self.managed_projects = []
        self.performance_metrics = {}

    def perform_daily_tasks(self) -> List[str]:
        tasks = [
            "Планирование работы отдела",
            "Проведение совещаний",
            "Контроль выполнения задач",
            "Подготовка отчётов",
            "Принятие управленческих решений",
            "Координация с другими отделами"
        ]
        self.workload = min(100, self.workload + 20)
        return tasks

    def make_decision(self, decision_complexity: int) -> bool:
        """Принимает управленческое решение."""
        success_chance = (self.decision_authority / 10) * (self.experience_years / 20)
        success = random.random() < success_chance
        if success:
            self.performance_metrics["decisions_made"] = self.performance_metrics.get("decisions_made", 0) + 1
        return success

    def conduct_meeting(self, attendees: int, duration_hours: float) -> Dict[str, any]:
        """Проводит совещание."""
        effectiveness = min(100, self.experience_years * 5 + random.uniform(-10, 10))
        
        meeting_result = {
            "attendees": attendees,
            "duration": duration_hours,
            "decisions_made": random.randint(1, 5),
            "action_items": random.randint(2, 10),
            "effectiveness": effectiveness,
            "participant_engagement": random.uniform(60, 95)
        }
        
        self.workload = min(100, self.workload + duration_hours * 10)
        return meeting_result

    def approve_budget(self, amount: float) -> bool:
        """Утверждает бюджет."""
        can_approve = amount <= self.budget_responsibility
        if can_approve:
            self.performance_metrics["budget_approved"] = self.performance_metrics.get("budget_approved", 0) + amount
        return can_approve

    def add_project(self, project_name: str, budget: float) -> None:
        """Добавляет проект под управление."""
        project = {
            "name": project_name,
            "budget": budget,
            "start_date": datetime.now(),
            "status": "active"
        }
        self.managed_projects.append(project)
