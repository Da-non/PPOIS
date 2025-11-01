class Oceanarium:
    """
    Главный класс океанариума.

    Attributes:
        name (str): Название океанариума
        location (str): Местоположение
        opening_hours (Dict): Часы работы
        capacity (int): Максимальная вместимость посетителей
    """

    def __init__(self, name: str, location: str, capacity: int):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.opening_hours = {
            "monday": {"open": "09:00", "close": "18:00"},
            "tuesday": {"open": "09:00", "close": "18:00"},
            "wednesday": {"open": "09:00", "close": "18:00"},
            "thursday": {"open": "09:00", "close": "18:00"},
            "friday": {"open": "09:00", "close": "20:00"},
            "saturday": {"open": "08:00", "close": "20:00"},
            "sunday": {"open": "08:00", "close": "19:00"}
        }

        # Основные компоненты
        self.animals = {}  # animal_id -> Animal
        self.tanks = {}    # tank_id -> Tank
        self.staff = {}    # staff_id -> Staff
        self.visitors = {} # visitor_id -> Visitor
        self.equipment = {} # equipment_id -> Equipment

        # Системы управления
        self.monitoring_system = MonitoringSystem("MAIN_MONITOR")
        self.security_system = SecuritySystem("MAIN_SECURITY")
        self.emergency_response = EmergencyResponse("MAIN_EMERGENCY")
        self.payment_processor = PaymentProcessor("MAIN_PAYMENT")

        # Финансы
        self.bank_account = BankAccount("OCN_MAIN_001", name, 1000000.0)
        self.ticket_offices = []

        # Поставщики и программы
        self.food_suppliers = {}
        self.educational_programs = {}

        # Статистика
        self.daily_visitors = 0
        self.monthly_revenue = 0.0
        self.operational_status = "open"
        self.last_inspection_date = datetime.now()

        # Инициализация базовых зон безопасности
        self._initialize_security_zones()
        self._initialize_emergency_plans()

    def _initialize_security_zones(self) -> None:
        """Инициализирует зоны безопасности."""
        zones = [
            ("PUBLIC_AREA", "Общественная зона", 1),
            ("STAFF_AREA", "Зона персонала", 2),
            ("ANIMAL_CARE", "Зона ухода за животными", 3),
            ("RESTRICTED", "Ограниченная зона", 4),
            ("ADMIN", "Административная зона", 5)
        ]

        for zone_id, zone_name, level in zones:
            self.security_system.create_access_zone(zone_id, zone_name, level)

    def _initialize_emergency_plans(self) -> None:
        """Инициализирует планы экстренного реагирования."""
        zones = [
            ("MAIN_HALL", 200, ["EXIT_1", "EXIT_2", "EXIT_3"]),
            ("DOLPHIN_SHOW", 150, ["EXIT_A", "EXIT_B"]),
            ("TOUCH_TANK", 50, ["EXIT_T1"]),
            ("STAFF_QUARTERS", 30, ["EXIT_S1", "EXIT_S2"])
        ]

        for zone_id, capacity, exits in zones:
            self.emergency_response.create_evacuation_plan(zone_id, capacity, exits)

    def add_animal(self, animal: Animal, tank_id: str) -> bool:
        """Добавляет животное в океанариум."""
        if tank_id not in self.tanks:
            raise ValueError(f"Резервуар {tank_id} не существует")

        tank = self.tanks[tank_id]
        if tank.add_animal(animal):
            self.animals[animal.animal_id] = animal
            return True
        return False

    def add_tank(self, tank: Tank) -> None:
        """Добавляет резервуар в океанариум."""
        self.tanks[tank.tank_id] = tank

        # Добавляем датчики мониторинга для нового резервуара
        sensor_types = ["temperature", "ph", "salinity", "ammonia"]
        for sensor_type in sensor_types:
            self.monitoring_system.add_sensor(sensor_type, f"Tank_{tank.tank_id}", tank.tank_id)

    def hire_staff(self, staff_member: Staff) -> None:
        """Нанимает сотрудника."""
        self.staff[staff_member.staff_id] = staff_member

        # Выдаём карту доступа
        self.security_system.issue_keycard(
            staff_member.staff_id,
            staff_member.name,
            staff_member.access_level
        )

    def add_visitor(self, visitor: Visitor) -> None:
        """Регистрирует посетителя."""
        self.visitors[visitor.visitor_id] = visitor
        self.daily_visitors += 1

    def create_ticket_office(self, office_id: str, cashier_name: str) -> TicketOffice:
        """Создаёт кассу."""
        office = TicketOffice(office_id, cashier_name)
        office.payment_processor = self.payment_processor
        self.ticket_offices.append(office)
        return office

    def add_food_supplier(self, supplier: FoodSupplier) -> None:
        """Добавляет поставщика корма."""
        self.food_suppliers[supplier.supplier_id] = supplier

    def create_educational_program(self, program_id: str, name: str,
                                 target_audience: str, duration: int) -> EducationalProgram:
        """Создаёт образовательную программу."""
        program = EducationalProgram(program_id, name, target_audience, duration)
        self.educational_programs[program_id] = program
        return program

    def feed_all_animals(self) -> Dict[str, bool]:
        """Кормит всех животных."""
        feeding_results = {}

        for animal_id, animal in self.animals.items():
            # Находим кормильца для этого животного
            feeder = self._find_available_feeder()
            if feeder:
                requirements = animal.get_feeding_requirements()
                fed = False

                for food_type, amount in requirements.items():
                    if feeder.feed_animal(animal, food_type, amount):
                        fed = True
                        break

                feeding_results[animal_id] = fed
            else:
                feeding_results[animal_id] = False

        return feeding_results

    def _find_available_feeder(self) -> Optional[Feeder]:
        """Находит доступного кормильца."""
        for staff_member in self.staff.values():
            if isinstance(staff_member, Feeder):
                return staff_member
        return None

    def conduct_health_checks(self) -> Dict[str, Dict]:
        """Проводит медицинские осмотры животных."""
        health_results = {}

        # Находим ветеринара
        veterinarian = self._find_veterinarian()
        if not veterinarian:
            raise AnimalHealthException("NO_VET", "Ветеринар не найден")

        for animal_id, animal in self.animals.items():
            examination = veterinarian.examine_animal(animal)
            health_results[animal_id] = examination

        return health_results

    def _find_veterinarian(self) -> Optional[Veterinarian]:
        """Находит ветеринара."""
        for staff_member in self.staff.values():
            if isinstance(staff_member, Veterinarian):
                return staff_member
        return None

    def monitor_water_quality(self) -> Dict[str, Dict]:
        """Мониторит качество воды во всех резервуарах."""
        quality_results = {}

        for tank_id, tank in self.tanks.items():
            quality_check = tank.check_water_quality()
            quality_results[tank_id] = quality_check

            # Если есть проблемы, создаём предупреждение
            for parameter, is_ok in quality_check.items():
                if not is_ok:
                    self.monitoring_system.create_alert(
                        tank_id, parameter, 0, "high"
                    )

        return quality_results

    def generate_daily_report(self) -> Dict[str, any]:
        """Генерирует ежедневный отчёт."""
        report = {
            "date": datetime.now().date(),
            "visitor_count": self.daily_visitors,
            "animal_count": len(self.animals),
            "staff_on_duty": len([s for s in self.staff.values() if hasattr(s, 'on_duty') and s.on_duty]),
            "tank_status": {},
            "revenue": 0.0,
            "incidents": len(self.emergency_response.incident_log),
            "alerts": len(self.monitoring_system.alerts)
        }

        # Статус резервуаров
        for tank_id, tank in self.tanks.items():
            report["tank_status"][tank_id] = {
                "animal_count": len(tank.animals),
                "water_quality": tank.check_water_quality(),
                "last_cleaned": tank.last_cleaned
            }

        # Подсчёт дневной выручки
        for office in self.ticket_offices:
            report["revenue"] += sum(sale["price"] for sale in office.daily_sales)

        return report

    def process_visitor_entry(self, visitor: Visitor, ticket_id: str) -> bool:
        """Обрабатывает вход посетителя."""
        # Находим билет
        ticket = None
        for visitor_ticket in visitor.tickets:
            if visitor_ticket.ticket_id == ticket_id:
                ticket = visitor_ticket
                break

        if not ticket:
            return False

        # Проверяем и используем билет
        if visitor.enter_oceanarium(ticket):
            self.add_visitor(visitor)
            return True

        return False

    def conduct_training_session(self, trainer_id: str, animal_id: str, skill: str) -> bool:
        """Проводит тренировочную сессию."""
        if trainer_id not in self.staff or animal_id not in self.animals:
            return False

        trainer = self.staff[trainer_id]
        animal = self.animals[animal_id]

        if isinstance(trainer, Trainer):
            return trainer.train_animal(animal, skill)

        return False

    def schedule_maintenance(self, equipment_id: str, maintenance_type: str) -> bool:
        """Планирует техническое обслуживание."""
        if equipment_id not in self.equipment:
            return False

        equipment = self.equipment[equipment_id]
        maintenance_worker = self._find_maintenance_worker(maintenance_type)

        if maintenance_worker:
            if maintenance_type == "repair":
                return maintenance_worker.repair_equipment(equipment, "general")
            else:
                return maintenance_worker.perform_preventive_maintenance(equipment)

        return False

    def _find_maintenance_worker(self, specialization: str = None) -> Optional[MaintenanceWorker]:
        """Находит работника технического обслуживания."""
        for staff_member in self.staff.values():
            if isinstance(staff_member, MaintenanceWorker):
                if not specialization or staff_member.specialization == specialization:
                    return staff_member
        return None

    def activate_emergency_protocol(self, emergency_type: str, location: str) -> str:
        """Активирует протокол чрезвычайной ситуации."""
        # Запускаем экстренное оповещение
        alert_id = self.emergency_response.trigger_emergency_alert(
            emergency_type, location, 8  # Высокая степень серьёзности
        )

        # Активируем режим ЧС в системе безопасности
        self.security_system.activate_emergency_mode()

        # Меняем операционный статус
        self.operational_status = "emergency"

        # Если требуется эвакуация
        if emergency_type in ["fire", "gas_leak", "structural_damage"]:
            self.emergency_response.initiate_evacuation(location)

        return alert_id

    def close_for_day(self) -> Dict[str, any]:
        """Закрывает океанариум на день."""
        closing_report = {
            "closing_time": datetime.now(),
            "daily_visitors": self.daily_visitors,
            "revenue": 0.0,
            "incidents": len(self.emergency_response.incident_log),
            "animals_fed": 0,
            "maintenance_completed": 0
        }

        # Подсчёт выручки
        total_revenue = 0.0
        for office in self.ticket_offices:
            office_report = office.end_shift()
            total_revenue += office_report["total_sales"]

        closing_report["revenue"] = total_revenue
        self.monthly_revenue += total_revenue

        # Вносим выручку на счёт
        self.bank_account.deposit(total_revenue, "Daily revenue")

        # Сброс дневных счётчиков
        self.daily_visitors = 0

        # Меняем статус
        self.operational_status = "closed"

        return closing_report

    def open_for_day(self, initial_cash_per_office: float = 5000.0) -> None:
        """Открывает океанариум на день."""
        self.operational_status = "open"

        # Запуск касс
        for office in self.ticket_offices:
            office.start_shift(initial_cash_per_office)

        # Сброс дневных логов
        self.emergency_response.incident_log.clear()
        for office in self.ticket_offices:
            office.daily_sales.clear()

    def get_occupancy_rate(self) -> float:
        """Возвращает текущую заполненность."""
        current_visitors = len([v for v in self.visitors.values()
                              if any(visit["exit_time"] is None for visit in v.visit_history)])
        return (current_visitors / self.capacity) * 100

    def transfer_animal(self, animal_id: str, from_tank_id: str, to_tank_id: str) -> bool:
        """Переводит животное из одного резервуара в другой."""
        if (animal_id not in self.animals or
            from_tank_id not in self.tanks or
            to_tank_id not in self.tanks):
            return False

        animal = self.animals[animal_id]
        from_tank = self.tanks[from_tank_id]
        to_tank = self.tanks[to_tank_id]

        # Удаляем из старого резервуара
        if from_tank.remove_animal(animal_id):
            # Добавляем в новый резервуар
            if to_tank.add_animal(animal):
                return True
            else:
                # Если не удалось добавить, возвращаем обратно
                from_tank.add_animal(animal)

        return False

    def calculate_monthly_expenses(self) -> Dict[str, float]:
        """Вычисляет месячные расходы."""
        expenses = {
            "staff_salaries": 0.0,
            "food_costs": 0.0,
            "utilities": 0.0,
            "maintenance": 0.0,
            "insurance": 0.0
        }

        # Зарплаты сотрудников
        for staff_member in self.staff.values():
            expenses["staff_salaries"] += staff_member.calculate_monthly_salary()

        # Примерные другие расходы
        expenses["food_costs"] = len(self.animals) * 5000  # 5000 руб/месяц на животное
        expenses["utilities"] = 150000  # Фиксированная сумма
        expenses["maintenance"] = len(self.equipment) * 2000  # 2000 руб/месяц на оборудование
        expenses["insurance"] = 75000  # Фиксированная сумма

        return expenses

    def get_animal_statistics(self) -> Dict[str, any]:
        """Возвращает статистику по животным."""
        stats = {
            "total_animals": len(self.animals),
            "species_count": {},
            "health_distribution": {"healthy": 0, "sick": 0, "stressed": 0},
            "feeding_status": {"recently_fed": 0, "needs_feeding": 0},
            "tank_distribution": {}
        }

        for animal in self.animals.values():
            # Подсчёт видов
            species = animal.species
            stats["species_count"][species] = stats["species_count"].get(species, 0) + 1

            # Распределение по здоровью
            health = animal.check_health()
            if health == "healthy":
                stats["health_distribution"]["healthy"] += 1
            elif health == "stressed":
                stats["health_distribution"]["stressed"] += 1
            else:
                stats["health_distribution"]["sick"] += 1

            # Статус кормления
            if animal.last_feeding and (datetime.now() - animal.last_feeding).total_seconds() < 6 * 3600:
                stats["feeding_status"]["recently_fed"] += 1
            else:
                stats["feeding_status"]["needs_feeding"] += 1

            # Распределение по резервуарам
            tank_id = animal.tank_id or "unassigned"
            stats["tank_distribution"][tank_id] = stats["tank_distribution"].get(tank_id, 0) + 1

        return stats
