class Equipment(ABC):
    """
    Абстрактный базовый класс для оборудования.

    Attributes:
        equipment_id (str): Уникальный идентификатор оборудования
        name (str): Название оборудования
        manufacturer (str): Производитель
        installation_date (datetime): Дата установки
        status (str): Текущий статус
    """

    def __init__(self, equipment_id: str, name: str, manufacturer: str):
        self.equipment_id = equipment_id
        self.name = name
        self.manufacturer = manufacturer
        self.installation_date = datetime.now()
        self.status = "operational"
        self.last_maintenance = None
        self.maintenance_interval_days = 30
        self.power_consumption = random.uniform(100, 500)  # Вт
        self.warranty_expires = datetime.now() + timedelta(days=365)
        self.error_codes = []
        self.operating_hours = 0

    @abstractmethod
    def perform_maintenance(self) -> bool:
        """Выполняет техническое обслуживание."""
        pass

    def check_status(self) -> str:
        """Проверяет статус оборудования."""
        if self.last_maintenance:
            days_since_maintenance = (datetime.now() - self.last_maintenance).days
            if days_since_maintenance > self.maintenance_interval_days:
                self.status = "needs_maintenance"

        if random.random() < 0.01:  # 1% шанс поломки
            self.status = "malfunction"
            self.error_codes.append(f"ERR_{random.randint(1000, 9999)}")

        return self.status

    def reset_error(self, error_code: str) -> bool:
        """Сбрасывает код ошибки."""
        if error_code in self.error_codes:
            self.error_codes.remove(error_code)
            if not self.error_codes:
                self.status = "operational"
            return True
        return False


