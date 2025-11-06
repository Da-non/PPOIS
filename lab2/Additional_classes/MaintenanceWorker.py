class MaintenanceWorker(Staff):
    """
    Класс работника технического обслуживания.
    """
    
    def __init__(self, staff_id: str, name: str, salary: float, experience_years: int, specialization: str):
        super().__init__(staff_id, name, "Maintenance Worker", salary, experience_years)
        self.specialization = specialization
        self.tools_inventory = []
        self.work_orders_completed = 0
        self.safety_incidents = 0
        self.efficiency_rating = random.uniform(70, 95)
        self.access_level = 3
        self.certifications = []
        self.active_work_orders = []

    def perform_daily_tasks(self) -> List[str]:
        tasks = [
            "Выполнение заявок на ремонт",
            "Профилактическое обслуживание оборудования",
            "Проверка систем безопасности",
            "Ведение журнала работ",
            "Заказ запчастей"
        ]
        self.workload = min(100, self.workload + 30)
        return tasks

    def repair_equipment(self, equipment: Equipment, issue_type: str) -> bool:
        """Ремонтирует оборудование."""
        success_rate = 0.8

        # Повышаем шансы при соответствии специализации
        specialization_bonus = 0
        if (self.specialization == "electrical" and "electric" in issue_type.lower()) or \
           (self.specialization == "plumbing" and "water" in issue_type.lower()) or \
           (self.specialization == "mechanical" and "mechanical" in issue_type.lower()):
            specialization_bonus = 0.15

        # Учитываем опыт и эффективность
        experience_bonus = self.experience_years * 0.01
        efficiency_bonus = (self.efficiency_rating - 70) / 100
        
        success_rate += specialization_bonus + experience_bonus + efficiency_bonus
        success_rate = min(0.95, success_rate)

        if random.random() < success_rate:
            equipment.status = "operational"
            if hasattr(equipment, 'error_codes'):
                equipment.error_codes.clear()
            self.work_orders_completed += 1
            self.workload = min(100, self.workload + 10)
            return True
        
        self.safety_incidents += 0.1  # Неудачная попытка
        return False

    def perform_preventive_maintenance(self, equipment: Equipment) -> bool:
        """Выполняет профилактическое обслуживание."""
        maintenance_success = random.random() < (self.efficiency_rating / 100)
        
        if maintenance_success and hasattr(equipment, 'perform_maintenance'):
            result = equipment.perform_maintenance()
            self.work_orders_completed += 1
            return result
        return False

    def add_tool(self, tool_name: str) -> None:
        """Добавляет инструмент в инвентарь."""
        if tool_name not in self.tools_inventory:
            self.tools_inventory.append(tool_name)

    def add_certification(self, certification: str) -> None:
        """Добавляет сертификацию."""
        if certification not in self.certifications:
            self.certifications.append(certification)
            self.efficiency_rating = min(95, self.efficiency_rating + 5)
