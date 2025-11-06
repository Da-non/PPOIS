class TemperatureController(Equipment):
    """
    Класс контроллера температуры.

    Attributes:
        target_temperature (float): Целевая температура в °C
        current_temperature (float): Текущая температура в °C
        heating_power (float): Мощность нагрева в Вт
    """

    def __init__(self, equipment_id: str, name: str, manufacturer: str, heating_power: float):
        super().__init__(equipment_id, name, manufacturer)
        self.target_temperature = 24.0
        self.current_temperature = random.uniform(22, 26)
        self.heating_power = heating_power
        self.cooling_power = heating_power * 0.8
        self.temperature_tolerance = 0.5
        self.sensor_accuracy = 0.1
        self.maintenance_interval_days = 90

    def perform_maintenance(self) -> bool:
        """Выполняет техническое обслуживание контроллера."""
        self.last_maintenance = datetime.now()
        self.status = "operational"
        self.sensor_accuracy = 0.1
        self.error_codes.clear()
        return True

    def set_temperature(self, temperature: float) -> bool:
        """Устанавливает целевую температуру."""
        if 15 <= temperature <= 30:
            self.target_temperature = temperature
            return True
        raise InvalidTemperatureException(temperature, 15, 30)

    def regulate_temperature(self) -> float:
        """Регулирует температуру."""
        temp_diff = self.target_temperature - self.current_temperature

        if abs(temp_diff) > self.temperature_tolerance:
            if temp_diff > 0:  # Нужно нагреть
                self.current_temperature += min(temp_diff, 0.5)
            else:  # Нужно охладить
                self.current_temperature += max(temp_diff, -0.3)

        return self.current_temperature
