class SecurityGuard(Staff):
    """
    Класс охранника.
    """
    
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int):
        super().__init__(staff_id, name, "Security Guard", salary, experience_years)
        self.patrol_route = []
        self.security_clearance = random.randint(3, 7)
        self.emergency_response_time = random.uniform(2, 8)
        self.incident_reports = []
        self.radio_frequency = random.uniform(450, 470)
        self.access_level = 4
        self.shift_schedule = "day"  # day, night, swing
        self.equipment = ["radio", "flashlight", "first_aid_kit"]

    def perform_daily_tasks(self) -> List[str]:
        tasks = [
            "Патрулирование территории",
            "Мониторинг систем безопасности",
            "Проверка пропусков посетителей",
            "Составление отчётов о происшествиях",
            "Проверка камер наблюдения"
        ]
        self.workload = min(100, self.workload + 15)
        return tasks

    def patrol(self, zone: str) -> Dict[str, any]:
        """Патрулирует зону."""
        patrol_duration = random.uniform(15, 45)
        incidents_found = random.randint(0, 2)
        
        patrol_result = {
            "zone": zone,
            "duration": patrol_duration,
            "incidents_found": incidents_found,
            "timestamp": datetime.now(),
            "guard": self.name,
            "route_completed": True
        }
        
        self.workload = min(100, self.workload + patrol_duration / 2)
        return patrol_result

    def respond_to_emergency(self, emergency_type: str, location: str) -> float:
        """Реагирует на чрезвычайную ситуацию."""
        base_time = self.emergency_response_time
        
        # Модификаторы времени реагирования
        time_modifiers = {
            "fire": 0.8,
            "medical": 0.9,
            "security": 1.0,
            "animal_escape": 0.7
        }
        
        response_time = base_time * time_modifiers.get(emergency_type, 1.0)
        
        # Учет опыта
        response_time *= max(0.5, 1.0 - (self.experience_years * 0.05))
        
        self.workload = min(100, self.workload + 25)
        return response_time

    def file_incident_report(self, incident_type: str, description: str, severity: int) -> str:
        """Заполняет отчёт о происшествии."""
        report_id = f"INC_{len(self.incident_reports):04d}"
        report = {
            "report_id": report_id,
            "incident_type": incident_type,
            "description": description,
            "severity": severity,
            "timestamp": datetime.now(),
            "guard_id": self.staff_id,
            "status": "open",
            "resolution": ""
        }
        self.incident_reports.append(report)
        return report_id

    def add_patrol_route(self, route_name: str, checkpoints: List[str]) -> None:
        """Добавляет маршрут патрулирования."""
        route = {
            "name": route_name,
            "checkpoints": checkpoints,
            "estimated_duration": len(checkpoints) * 5  # минут на точку
        }
        self.patrol_route.append(route)
