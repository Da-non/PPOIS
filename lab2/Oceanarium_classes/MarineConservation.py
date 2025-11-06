class MarineConservation:
    """Отдел морской консервации."""
    
    def __init__(self, department_id: str, focus_areas: List[str]):
        self.department_id = department_id
        self.focus_areas = focus_areas
        self.conservation_projects = []
        self.research_grants = []
        self.community_outreach = []
        self.partnerships = []
        self.volunteer_program = None
        self.education_initiatives = []

    def create_conservation_project(self, project_name: str, target_species: str,
                                 duration_months: int, budget: float) -> str:
        """Создает проект по консервации."""
        project_id = f"CONS_{len(self.conservation_projects):04d}"
        project = {
            "project_id": project_id,
            "name": project_name,
            "target_species": target_species,
            "start_date": datetime.now(),
            "duration": duration_months,
            "budget": budget,
            "status": "active",
            "progress": 0.0,
            "team_members": []
        }
        self.conservation_projects.append(project)
        return project_id

    def apply_for_grant(self, grant_name: str, amount: float, 
                       purpose: str) -> Dict[str, any]:
        """Подает заявку на грант."""
        grant_application = {
            "grant_name": grant_name,
            "amount": amount,
            "purpose": purpose,
            "application_date": datetime.now(),
            "status": "submitted",
            "success_probability": random.uniform(30, 70)
        }
        
        # Симуляция результата заявки
        if random.random() < (grant_application["success_probability"] / 100):
            grant_application["status"] = "approved"
            self.research_grants.append(grant_application)
        else:
            grant_application["status"] = "rejected"
            
        return grant_application

    def organize_community_event(self, event_name: str, event_type: str,
                               expected_attendance: int, date: datetime) -> str:
        """Организует мероприятие для сообщества."""
        event_id = f"EVENT_{len(self.community_outreach):04d}"
        event = {
            "event_id": event_id,
            "name": event_name,
            "type": event_type,
            "date": date,
            "expected_attendance": expected_attendance,
            "actual_attendance": 0,
            "budget": 0.0,
            "volunteers_needed": 0
        }
        self.community_outreach.append(event)
        return event_id
