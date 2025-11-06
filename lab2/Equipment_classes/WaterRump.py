class WaterPump(Equipment):
    """
    Класс водяного насоса.

    Attributes:
        flow_rate (float): Скорость потока в л/мин
        pressure (float): Давление в барах
        pump_type (str): Тип насоса
    """

    def __init__(self, equipment_id: str, name: str, manufacturer: str, flow_rate: float):
        super().__init__(equipment_id, name, manufacturer)
        self.flow_rate = flow_rate
        self.pressure = random.uniform(1.0, 5.0)
        self.pump_type = random.choice(["centrifugal", "submersible", "magnetic_drive"])
        self.impeller_speed = random.uniform(1000, 3000)  # об/мин
        self.maintenance_interval_days = 60

    def perform_maintenance(self) -> bool:
        """Выполняет техническое обслуживание насоса."""
        self.last_maintenance = datetime.now()
        self.status = "operational"
        self.error_codes.clear()
        # Очистка импеллера, замена уплотнений
        self.impeller_speed = random.uniform(1000, 3000)
        return True

    def adjust_flow_rate(self, new_rate: float) -> bool:
        """Регулирует скорость потока."""
        if 0 <= new_rate <= self.flow_rate * 1.2:
            self.flow_rate = new_rate
            return True
        return False

    def check_cavitation(self) -> bool:
        """Проверяет наличие кавитации."""
        return self.pressure < 0.5 or self.impeller_speed > 2800
