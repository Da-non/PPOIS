class ResearchLaboratory:
    """Научно-исследовательская лаборатория."""
    
    def __init__(self, lab_id: str, specialization: str):
        self.lab_id = lab_id
        self.specialization = specialization
        self.equipment = []
        self.research_projects = []
        self.publications = []
        self.safety_level = random.randint(1, 4)
        self.certification_status = "certified"
        self.resource_utilization = 0.0

    def add_equipment(self, equipment: Equipment) -> bool:
        """Добавляет оборудование в лабораторию."""
        if equipment not in self.equipment:
            self.equipment.append(equipment)
            return True
        return False

    def start_research_project(self, project_name: str, lead_scientist: ResearchScientist, 
                             duration_days: int, budget: float) -> str:
        """Начинает исследовательский проект."""
        project_id = f"PROJ_{len(self.research_projects) + 1}"
        project = {
            "project_id": project_id,
            "name": project_name,
            "lead_scientist": lead_scientist,
            "team": [],
            "duration_days": duration_days,
            "budget": budget,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=duration_days),
            "status": "active",
            "progress": 0.0,
            "findings": []
        }
        self.research_projects.append(project)
        return project_id

    def add_team_member(self, project_id: str, scientist: ResearchScientist) -> bool:
        """Добавляет члена команды в проект."""
        for project in self.research_projects:
            if project["project_id"] == project_id:
                if scientist not in project["team"]:
                    project["team"].append(scientist)
                    return True
        return False

    def record_finding(self, project_id: str, finding: str, significance: int) -> bool:
        """Записывает находку в проект."""
        for project in self.research_projects:
            if project["project_id"] == project_id:
                finding_data = {
                    "id": f"FINDING_{len(project['findings']) + 1}",
                    "description": finding,
                    "significance": significance,
                    "timestamp": datetime.now()
                }
                project["findings"].append(finding_data)
                project["progress"] = min(100.0, project["progress"] + (100 / project["duration_days"]))
                return True
        return False

    def publish_research(self, project_id: str, journal: str) -> str:
        """Публикует исследование."""
        for project in self.research_projects:
            if project["project_id"] == project_id and project["progress"] >= 100.0:
                publication_id = f"PUB_{len(self.publications) + 1}"
                publication = {
                    "publication_id": publication_id,
                    "project_id": project_id,
                    "project_name": project["name"],
                    "journal": journal,
                    "authors": [project["lead_scientist"].name] + [s.name for s in project["team"]],
                    "publication_date": datetime.now()
                }
                self.publications.append(publication)
                project["status"] = "completed"
                return publication_id
        return ""

    def get_laboratory_report(self) -> Dict[str, Any]:
        """Возвращает отчёт лаборатории."""
        active_projects = len([p for p in self.research_projects if p["status"] == "active"])
        completed_projects = len([p for p in self.research_projects if p["status"] == "completed"])
        
        return {
            "lab_id": self.lab_id,
            "specialization": self.specialization,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "publications": len(self.publications),
            "equipment_count": len(self.equipment),
            "safety_level": self.safety_level,
            "certification_status": self.certification_status
        }

