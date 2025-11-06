class WaterTreatmentSystem(Equipment):
    """Система обработки воды."""
    
    def __init__(self, system_id: str, capacity: float):
        super().__init__(system_id, f"WaterTreatment_{system_id}", "AquaSystems Inc.")
        self.system_id = system_id
        self.capacity = capacity
        self.filtration_level = 95.0
        self.chemical_balance = {
            "ph": 7.8,
            "chlorine": 0.0,
            "ammonia": 0.0,
            "nitrates": 5.0
        }
        self.maintenance_schedule = []
        self.water_quality_history = []
        self.filtration_media_age = 0  # дни
        self.max_media_age = 180  # дней

    def perform_maintenance(self) -> bool:
        """Выполняет техническое обслуживание системы."""
        self.last_maintenance = datetime.now()
        self.status = "operational"
        self.filtration_media_age = 0
        self.filtration_level = 95.0
        self.error_codes.clear()
        return True

    def treat_water(self, water_volume: float, source_quality: Dict[str, float]) -> Dict[str, float]:
        """Обрабатывает воду."""
        if water_volume > self.capacity:
            raise TankOverflowException(self.system_id, self.capacity, water_volume)

        # Симуляция обработки воды
        treated_water = {
            "ph": max(7.8, min(8.4, source_quality.get("ph", 7.0) + random.uniform(-0.1, 0.1))),
            "chlorine": 0.0,
            "ammonia": source_quality.get("ammonia", 0.0) * 0.1,  # Уменьшаем аммиак на 90%
            "nitrates": source_quality.get("nitrates", 10.0) * 0.3,  # Уменьшаем нитраты на 70%
            "turbidity": source_quality.get("turbidity", 10.0) * 0.05,  # Уменьшаем мутность на 95%
            "filtration_efficiency": self.filtration_level
        }

        # Увеличиваем возраст фильтрующего материала
        self.filtration_media_age += 1
        if self.filtration_media_age > self.max_media_age:
            self.filtration_level *= 0.99  # Постепенное ухудшение

        # Сохраняем историю качества воды
        self.water_quality_history.append({
            "timestamp": datetime.now(),
            "input_quality": source_quality,
            "output_quality": treated_water,
            "volume": water_volume
        })

        return treated_water

    def schedule_maintenance(self, maintenance_date: datetime, maintenance_type: str = "routine") -> bool:
        """Планирует техническое обслуживание."""
        maintenance = {
            "id": f"MAINT_{len(self.maintenance_schedule) + 1}",
            "date": maintenance_date,
            "type": maintenance_type,
            "scheduled_by": "System",
            "status": "scheduled"
        }
        self.maintenance_schedule.append(maintenance)
        return True

    def get_water_quality_report(self) -> Dict[str, Any]:
        """Возвращает отчёт о качестве воды."""
        recent_samples = self.water_quality_history[-10:] if self.water_quality_history else []
        
        return {
            "system_id": self.system_id,
            "filtration_level": self.filtration_level,
            "media_age_days": self.filtration_media_age,
            "chemical_balance": self.chemical_balance,
            "recent_samples": len(recent_samples),
            "maintenance_due": self.filtration_media_age > 150
        }

