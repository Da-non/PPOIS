class ResearchLaboratory:
    """Научно-исследовательская лаборатория."""
    
    def __init__(self, lab_id: str, specialization: str):
        self.lab_id = lab_id
        self.specialization = specialization
        self.equipment = []
        self.research_projects = []
        self.publications = []
        self.safety_level = 2
        self.researcher_capacity = 10
        self.current_researchers = []
        self.specimen_collection = []

    def add_equipment(self, equipment_name: str, purpose: str) -> None:
        """Добавляет оборудование в лабораторию."""
        equipment_item = {
            "name": equipment_name,
            "purpose": purpose,
            "status": "operational",
            "last_calibration": datetime.now(),
            "usage_hours": 0
        }
        self.equipment.append(equipment_item)

    def start_research_project(self, project_name: str, lead_researcher: ResearchScientist,
                             duration_days: int, budget: float) -> str:
        """Начинает исследовательский проект."""
        project_id = f"PROJ_{len(self.research_projects):04d}"
        project = {
            "project_id": project_id,
            "name": project_name,
            "lead_researcher": lead_researcher,
            "team": [],
            "start_date": datetime.now(),
            "duration": duration_days,
            "budget": budget,
            "status": "active",
            "progress": 0.0
        }
        self.research_projects.append(project)
        return project_id

    def publish_research(self, title: str, authors: List[str], 
                        journal: str, impact_factor: float) -> str:
        """Публикует исследовательскую работу."""
        publication_id = f"PUB_{len(self.publications):04d}"
        publication = {
            "publication_id": publication_id,
            "title": title,
            "authors": authors,
            "journal": journal,
            "publication_date": datetime.now(),
            "impact_factor": impact_factor,
            "citations": 0
        }
        self.publications.append(publication)
        return publication_id

    def add_researcher(self, researcher: ResearchScientist) -> bool:
        """Добавляет исследователя в лабораторию."""
        if len(self.current_researchers) < self.researcher_capacity:
            self.current_researchers.append(researcher)
            return True
        return False
