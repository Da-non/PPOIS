class OceanographicResearch:
    """Океанографические исследования."""
    
    def __init__(self, research_id: str, ocean_region: str):
        self.research_id = research_id
        self.ocean_region = ocean_region
        self.research_vessels = []
        self.data_collection = []
        self.scientific_discoveries = []
        self.research_expeditions = []
        self.collaborating_institutions = []
        self.funding_sources = []
        self.publication_records = []

    def add_research_vessel(self, vessel_name: str, capacity: int, 
                          equipment: List[str]) -> None:
        """Добавляет исследовательское судно."""
        vessel = {
            "name": vessel_name,
            "capacity": capacity,
            "equipment": equipment,
            "current_location": "port",
            "operational_status": "ready",
            "mission_history": []
        }
        self.research_vessels.append(vessel)

    def plan_expedition(self, expedition_name: str, objectives: List[str],
                       duration_days: int, team_size: int) -> str:
        """Планирует исследовательскую экспедицию."""
        expedition_id = f"EXPED_{len(self.research_expeditions):04d}"
        expedition = {
            "expedition_id": expedition_id,
            "name": expedition_name,
            "objectives": objectives,
            "start_date": datetime.now(),
            "duration": duration_days,
            "team_size": team_size,
            "status": "planned",
            "vessel_assigned": None,
            "data_collected": []
        }
        self.research_expeditions.append(expedition)
        return expedition_id

    def collect_oceanographic_data(self, parameter: str, location: str,
                                 value: float, depth: float) -> str:
        """Собирает океанографические данные."""
        data_id = f"DATA_{len(self.data_collection):04d}"
        data_point = {
            "data_id": data_id,
            "parameter": parameter,
            "location": location,
            "value": value,
            "depth": depth,
            "timestamp": datetime.now(),
            "quality_rating": random.uniform(85, 99)
        }
        self.data_collection.append(data_point)
        return data_id

    def record_discovery(self, discovery_type: str, description: str,
                        significance: int, location: str) -> str:
        """Регистрирует научное открытие."""
        discovery_id = f"DISC_{len(self.scientific_discoveries):04d}"
        discovery = {
            "discovery_id": discovery_id,
            "type": discovery_type,
            "description": description,
            "significance": significance,  # 1-10
            "location": location,
            "discovery_date": datetime.now(),
            "verified": False
        }
        self.scientific_discoveries.append(discovery)
        return discovery_id
