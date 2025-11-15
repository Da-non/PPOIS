class EmergencyResponse:
    """
    Система экстренного реагирования.

    Attributes:
        response_id (str): Идентификатор системы
        emergency_contacts (Dict): Контакты экстренных служб
        evacuation_plans (Dict): Планы эвакуации
        emergency_equipment (List): Аварийное оборудование
    """

    def __init__(self, response_id: str):
        self.response_id = response_id
        self.emergency_contacts = {
            "fire_department": "101",
            "police": "102",
            "ambulance": "103",
            "gas_service": "104"
        }
        self.evacuation_plans = {}
        self.emergency_equipment = []
        self.incident_log = []
        self.alert_system = None
        self.response_time_target = 180  # секунды

    def create_evacuation_plan(self, zone_id: str, capacity: int, exit_routes: List[str]) -> None:
        """Создаёт план эвакуации для зоны."""
        self.evacuation_plans[zone_id] = {
            "capacity": capacity,
            "exit_routes": exit_routes,
            "assembly_points": [f"Point_{i+1}" for i in range(len(exit_routes))],
            "evacuation_time_estimate": capacity * 0.5  # секунды
        }

    def trigger_emergency_alert(self, emergency_type: str, location: str, severity: int) -> str:
        """Запускает экстренное оповещение."""
        alert_id = f"ALERT_EM_{len(self.incident_log):04d}"

        alert = {
            "alert_id": alert_id,
            "emergency_type": emergency_type,
            "location": location,
            "severity": severity,
            "timestamp": datetime.now(),
            "response_actions": [],
            "status": "active"
        }

        # Определяем необходимые действия
        if emergency_type == "fire":
            alert["response_actions"] = ["activate_sprinklers", "call_fire_department", "evacuate_zone"]
        elif emergency_type == "medical":
            alert["response_actions"] = ["call_ambulance", "provide_first_aid", "clear_area"]
        elif emergency_type == "security":
            alert["response_actions"] = ["lock_down_facility", "call_police", "secure_animals"]

        self.incident_log.append(alert)
        return alert_id

    def initiate_evacuation(self, zone_id: str) -> Dict[str, any]:
        """Инициирует эвакуацию зоны."""
        if zone_id not in self.evacuation_plans:
            return {"error": f"План эвакуации для зоны {zone_id} не найден"}

        plan = self.evacuation_plans[zone_id]
        evacuation_result = {
            "zone_id": zone_id,
            "estimated_time": plan["evacuation_time_estimate"],
            "exit_routes": plan["exit_routes"],
            "assembly_points": plan["assembly_points"],
            "initiation_time": datetime.now()
        }

        return evacuation_result

    def add_emergency_equipment(self, equipment_type: str, location: str, quantity: int) -> None:
        """Добавляет аварийное оборудование."""
        equipment = {
            "type": equipment_type,
            "location": location,
            "quantity": quantity,
            "last_inspection": datetime.now(),
            "status": "operational"
        }
        self.emergency_equipment.append(equipment)

    def test_emergency_systems(self) -> Dict[str, bool]:
        """Тестирует системы экстренного реагирования."""
        test_results = {}

        # Тест оборудования
        for equipment in self.emergency_equipment:
            test_results[f"{equipment['type']}_{equipment['location']}"] = random.random() > 0.05

        # Тест планов эвакуации
        for zone_id in self.evacuation_plans:
            test_results[f"evacuation_plan_{zone_id}"] = random.random() > 0.02

        return test_results
