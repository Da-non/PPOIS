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

    def add_research_vessel(self, vessel_name: str, capacity: int, 
                          equipment: List[str]) -> str:
        """Добавляет исследовательское судно."""
        vessel_id = f"VESSEL_{len(self.research_vessels) + 1}"
        vessel = {
            "vessel_id": vessel_id,
            "name": vessel_name,
            "capacity": capacity,
            "equipment": equipment,
            "current_location": self.ocean_region,
            "status": "docked",
            "maintenance_schedule": []
        }
        self.research_vessels.append(vessel)
        return vessel_id

    def plan_expedition(self, expedition_name: str, objectives: List[str],
                       duration_days: int, vessel_id: str) -> str:
        """Планирует исследовательскую экспедицию."""
        expedition_id = f"EXPED_{len(self.research_expeditions) + 1}"
        expedition = {
            "expedition_id": expedition_id,
            "name": expedition_name,
            "objectives": objectives,
            "duration_days": duration_days,
            "vessel_id": vessel_id,
            "start_date": datetime.now() + timedelta(days=random.randint(14, 60)),
            "end_date": None,
            "status": "planned",
            "team": [],
            "budget": random.uniform(50000, 500000)
        }
        self.research_expeditions.append(expedition)
        return expedition_id

    def collect_ocean_data(self, data_type: str, location: str, 
                          depth: float, parameters: Dict[str, float]) -> str:
        """Собирает океанографические данные."""
        data_id = f"DATA_{len(self.data_collection) + 1}"
        data_record = {
            "data_id": data_id,
            "type": data_type,  # temperature, salinity, currents, etc.
            "location": location,
            "depth": depth,
            "parameters": parameters,
            "collection_date": datetime.now(),
            "quality_rating": random.uniform(85, 99),
            "research_value": random.uniform(70, 95)
        }
        self.data_collection.append(data_record)
        return data_id

    def record_discovery(self, discovery_title: str, description: str,
                       significance: int, evidence: List[str]) -> str:
        """Записывает научное открытие."""
        discovery_id = f"DISCOV_{len(self.scientific_discoveries) + 1}"
        discovery = {
            "discovery_id": discovery_id,
            "title": discovery_title,
            "description": description,
            "significance": significance,  # 1-10 scale
            "evidence": evidence,
            "discovery_date": datetime.now(),
            "verification_status": "pending",
            "potential_impact": random.choice(["low", "medium", "high", "breakthrough"])
        }
        self.scientific_discoveries.append(discovery)
        return discovery_id

    def get_research_summary(self) -> Dict[str, Any]:
        """Возвращает сводку исследований."""
        active_expeditions = len([e for e in self.research_expeditions if e["status"] == "active"])
        total_data_points = len(self.data_collection)
        verified_discoveries = len([d for d in self.scientific_discoveries if d["verification_status"] == "verified"])
        
        return {
            "research_id": self.research_id,
            "ocean_region": self.ocean_region,
            "research_vessels": len(self.research_vessels),
            "active_expeditions": active_expeditions,
            "data_collection_points": total_data_points,
            "scientific_discoveries": len(self.scientific_discoveries),
            "verified_discoveries": verified_discoveries,
            "collaborating_institutions": len(self.collaborating_institutions)
        }
