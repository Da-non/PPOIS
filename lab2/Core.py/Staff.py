class Staff(ABC):
    def __init__(self, staff_id: str, name: str, position: str, salary: float, experience_years: int):
        self.staff_id = staff_id
        self.name = name
        self.position = position
        self.salary = salary
        self.experience_years = experience_years
        self.hire_date = datetime.now() - timedelta(days=experience_years*365)
        self.certifications = []
        self.performance_rating = random.uniform(3.0, 5.0)
        self.working_hours_per_week = 40
        self.department = None
        self.access_level = 1

    @abstractmethod
    def perform_daily_tasks(self) -> List[str]:
        pass

    def receive_certification(self, cert_name: str) -> None:
        if cert_name not in self.certifications:
            self.certifications.append(cert_name)

    def calculate_monthly_salary(self) -> float:
        base_monthly = self.salary / 12
        experience_bonus = base_monthly * (self.experience_years * 0.02)
        performance_bonus = base_monthly * (self.performance_rating - 3.0) * 0.1
        return base_monthly + experience_bonus + performance_bonus
