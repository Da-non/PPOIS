class AquacultureFacility:
    """Аквакультурное предприятие."""
    
    def __init__(self, facility_id: str, production_type: str):
        self.facility_id = facility_id
        self.production_type = production_type
        self.production_capacity = 0.0
        self.species_cultured = []
        self.harvest_schedule = []
        self.water_quality = {}
        self.feeding_regimen = {}
        self.growth_rates = {}
        self.operational_costs = 0.0

    def add_species(self, species: str, initial_stock: int, growth_rate: float) -> None:
        """Добавляет вид для культивирования."""
        cultured_species = {
            "species": species,
            "initial_stock": initial_stock,
            "current_stock": initial_stock,
            "growth_rate": growth_rate,
            "harvest_ready": False,
            "days_to_maturity": random.randint(90, 180)
        }
        self.species_cultured.append(cultured_species)

    def schedule_harvest(self, species: str, harvest_date: datetime, 
                        estimated_yield: float) -> str:
        """Планирует сбор урожая."""
        harvest_id = f"HARVEST_{len(self.harvest_schedule):04d}"
        harvest = {
            "harvest_id": harvest_id,
            "species": species,
            "scheduled_date": harvest_date,
            "estimated_yield": estimated_yield,
            "actual_yield": 0.0,
            "status": "scheduled",
            "quality_rating": 0.0
        }
        self.harvest_schedule.append(harvest)
        return harvest_id

    def monitor_growth(self) -> Dict[str, any]:
        """Мониторит рост культивируемых видов."""
        growth_report = {
            "facility_id": self.facility_id,
            "timestamp": datetime.now(),
            "species_growth": {},
            "water_parameters": self.water_quality,
            "health_status": "good"
        }

        for species_data in self.species_cultured:
            growth_rate = species_data["growth_rate"]
            current_stock = species_data["current_stock"]
            
            # Симуляция роста
            new_stock = current_stock * (1 + growth_rate / 100)
            species_data["current_stock"] = int(new_stock)
            
            growth_report["species_growth"][species_data["species"]] = {
                "growth_percentage": growth_rate,
                "current_biomass": new_stock
            }

        return growth_report

    def calculate_production_efficiency(self) -> float:
        """Рассчитывает эффективность производства."""
        if not self.species_cultured:
            return 0.0
            
        total_biomass = sum(sp["current_stock"] for sp in self.species_cultured)
        capacity_utilization = (total_biomass / self.production_capacity) * 100
        growth_efficiency = sum(sp["growth_rate"] for sp in self.species_cultured) / len(self.species_cultured)
        
        return (capacity_utilization + growth_efficiency) / 2
