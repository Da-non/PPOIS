class FilterSystem(Equipment):
    """
    Класс системы фильтрации.

    Attributes:
        filter_capacity (float): Производительность фильтра в л/ч
        filter_type (str): Тип фильтра
        efficiency (float): Эффективность очистки (%)
    """

    def __init__(self, equipment_id: str, name: str, manufacturer: str, filter_capacity: float):
        super().__init__(equipment_id, name, manufacturer)
        self.filter_capacity = filter_capacity
        self.filter_type = random.choice(["mechanical", "biological", "chemical", "UV"])
        self.efficiency = random.uniform(85, 99)
        self.filter_media_age = 0  # дни
        self.backwash_frequency = 7  # дней
        self.maintenance_interval_days = 14

    def perform_maintenance(self) -> bool:
        """Выполняет техническое обслуживание фильтра."""
        self.last_maintenance = datetime.now()
        self.status = "operational"
        self.filter_media_age = 0
        self.efficiency = random.uniform(85, 99)
        self.error_codes.clear()
        return True

    def backwash(self) -> bool:
        """Выполняет обратную промывку фильтра."""
        if self.filter_type in ["mechanical", "biological"]:
            self.efficiency = min(99, self.efficiency + 5)
            return True
        return False

    def replace_filter_media(self) -> bool:
        """Заменяет фильтрующий материал."""
        self.filter_media_age = 0
        self.efficiency = random.uniform(90, 99)
        return True
