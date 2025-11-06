class MonitoringSystem:
    """
    Система мониторинга океанариума.

    Attributes:
        system_id (str): Идентификатор системы
        sensors (List[Dict]): Список датчиков
        alerts (List[Dict]): Список предупреждений
        data_logs (List[Dict]): Журнал данных
    """

    def __init__(self, system_id: str):
        self.system_id = system_id
        self.sensors = []
        self.alerts = []
        self.data_logs = []
        self.monitoring_frequency = 60  # секунды
        self.alert_thresholds = {
            "temperature": {"min": 20, "max": 28},
            "ph": {"min": 7.8, "max": 8.4},
            "ammonia": {"max": 0.25}
        }
        self.backup_systems = []
        self.notification_emails = []

    def add_sensor(self, sensor_type: str, location: str, tank_id: str) -> str:
        """Добавляет новый датчик."""
        sensor_id = f"SENS_{len(self.sensors):04d}"
        sensor = {
            "sensor_id": sensor_id,
            "type": sensor_type,
            "location": location,
            "tank_id": tank_id,
            "status": "active",
            "last_reading": None,
            "calibration_date": datetime.now()
        }
        self.sensors.append(sensor)
        return sensor_id

    def read_sensor_data(self, sensor_id: str) -> Optional[float]:
        """Считывает данные с датчика."""
        for sensor in self.sensors:
            if sensor["sensor_id"] == sensor_id:
                # Симуляция чтения данных
                if sensor["type"] == "temperature":
                    value = random.uniform(22, 26)
                elif sensor["type"] == "ph":
                    value = random.uniform(7.9, 8.3)
                elif sensor["type"] == "salinity":
                    value = random.uniform(33, 37)
                else:
                    value = random.uniform(0, 10)

                sensor["last_reading"] = {
                    "value": value,
                    "timestamp": datetime.now()
                }

                self.data_logs.append({
                    "sensor_id": sensor_id,
                    "value": value,
                    "timestamp": datetime.now()
                })

                # Проверяем пороги для предупреждений
                self.check_alert_thresholds(sensor, value)

                return value
        return None

    def check_alert_thresholds(self, sensor: Dict, value: float) -> None:
        """Проверяет пороги для предупреждений."""
        sensor_type = sensor["type"]
        if sensor_type in self.alert_thresholds:
            thresholds = self.alert_thresholds[sensor_type]

            alert_triggered = False
            if "min" in thresholds and value < thresholds["min"]:
                alert_triggered = True
                severity = "high"
            elif "max" in thresholds and value > thresholds["max"]:
                alert_triggered = True
                severity = "high"

            if alert_triggered:
                self.create_alert(sensor["sensor_id"], sensor_type, value, severity)

    def create_alert(self, sensor_id: str, parameter: str, value: float, severity: str) -> None:
        """Создаёт предупреждение."""
        alert = {
            "alert_id": f"ALERT_{len(self.alerts):04d}",
            "sensor_id": sensor_id,
            "parameter": parameter,
            "value": value,
            "severity": severity,
            "timestamp": datetime.now(),
            "acknowledged": False,
            "resolved": False
        }
        self.alerts.append(alert)

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Подтверждает получение предупреждения."""
        for alert in self.alerts:
            if alert["alert_id"] == alert_id:
                alert["acknowledged"] = True
                return True
        return False

