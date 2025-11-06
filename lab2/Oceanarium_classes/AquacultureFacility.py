class AquacultureFacility:
    """Аквакультурное предприятие."""
    
    def __init__(self, facility_id: str, production_type: str):
        self.facility_id = facility_id
        self.production_type = production_type
        self.production_capacity = 0.0
        self.species_cultured = []
        self.harvest_schedule = []
        self.water_quality_params = {}
        self.feed_inventory = {}
        self.growth_data = {}

    def add_species(self, species: str, initial_stock: int, growth_rate: float) -> bool:
        """Добавляет вид для культивирования."""
        species_data = {
            "species": species,
            "current_stock": initial_stock,
            "initial_stock": initial_stock,
            "growth_rate": growth_rate,
            "health_status": "healthy",
            "added_date": datetime.now()
        }
        self.species_cultured.append(species_data)
        self.production_capacity += initial_stock * 0.1  # Условная ёмкость
        return True

    def schedule_harvest(self, species: str, harvest_date: datetime, 
                        estimated_yield: float) -> str:
        """Планирует сбор урожая."""
        harvest_id = f"HARVEST_{len(self.harvest_schedule) + 1}"
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

    def monitor_growth(self, species: str) -> Dict[str, Any]:
        """Мониторит рост вида."""
        species_data = next((s for s in self.species_cultured if s["species"] == species), None)
        if not species_data:
            return {"error": "Вид не найден"}

        # Симуляция роста
        growth_factor = species_data["growth_rate"] * random.uniform(0.8, 1.2)
        weight_gain = species_data["current_stock"] * growth_factor * 0.01
        
        # Обновляем данные роста
        if species not in self.growth_data:
            self.growth_data[species] = []
        
        growth_record = {
            "date": datetime.now(),
            "stock_count": species_data["current_stock"],
            "average_weight": growth_factor,
            "health_index": random.uniform(85, 98)
        }
        self.growth_data[species].append(growth_record)

        return growth_record

    def perform_harvest(self, harvest_id: str) -> Dict[str, Any]:
        """Выполняет сбор урожая."""
        harvest = next((h for h in self.harvest_schedule if h["harvest_id"] == harvest_id), None)
        if not harvest or harvest["status"] != "scheduled":
            return {"success": False, "error": "Уборка не запланирована"}

        species_data = next((s for s in self.species_cultured if s["species"] == harvest["species"]), None)
        if not species_data:
            return {"success": False, "error": "Вид не найден"}

        # Симуляция уборки
        harvest_success = random.random() < 0.85  # 85% успеха
        if harvest_success:
            actual_yield = harvest["estimated_yield"] * random.uniform(0.9, 1.1)
            harvest["actual_yield"] = actual_yield
            harvest["status"] = "completed"
            harvest["quality_rating"] = random.uniform(80, 98)
            harvest["completion_date"] = datetime.now()

            # Уменьшаем запас
            species_data["current_stock"] = max(0, species_data["current_stock"] - int(actual_yield))

        return {
            "success": harvest_success,
            "harvest_id": harvest_id,
            "actual_yield": harvest["actual_yield"] if harvest_success else 0,
            "quality_rating": harvest["quality_rating"] if harvest_success else 0,
            "remaining_stock": species_data["current_stock"]
        }

    def get_facility_report(self) -> Dict[str, Any]:
        """Возвращает отчёт предприятия."""
        total_stock = sum(species["current_stock"] for species in self.species_cultured)
        scheduled_harvests = len([h for h in self.harvest_schedule if h["status"] == "scheduled"])
        completed_harvests = len([h for h in self.harvest_schedule if h["status"] == "completed"])
        
        return {
            "facility_id": self.facility_id,
            "production_type": self.production_type,
            "species_count": len(self.species_cultured),
            "total_stock": total_stock,
            "production_capacity": self.production_capacity,
            "scheduled_harvests": scheduled_harvests,
            "completed_harvests": completed_harvests,
            "utilization_rate": (total_stock / self.production_capacity * 100) if self.production_capacity > 0 else 0
        }
