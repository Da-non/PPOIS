class Animal(ABC):
    """
    Абстрактный базовый класс для всех животных океанариума.

    Attributes:
        animal_id (str): Уникальный идентификатор животного
        name (str): Имя животного
        species (str): Вид животного
        age (int): Возраст в годах
        weight (float): Вес в килограммах
        health_status (str): Состояние здоровья
        last_feeding (datetime): Время последнего кормления
        tank_id (str): Идентификатор резервуара
    """

    def __init__(self, animal_id: str, name: str, species: str, age: int, weight: float):
        self.animal_id = animal_id
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.health_status = "healthy"
        self.last_feeding = None
        self.tank_id = None
        self.birth_date = datetime.now() - timedelta(days=age*365)
        self.medical_records = []
        self.feeding_schedule = {}
        self.activity_level = 100
        self.stress_level = 0
        self.breeding_status = "not_breeding"

    @abstractmethod
    def get_feeding_requirements(self) -> Dict[str, float]:
        """Возвращает требования к кормлению."""
        pass

    @abstractmethod
    def get_habitat_requirements(self) -> Dict[str, any]:
        """Возвращает требования к среде обитания."""
        pass

    def feed(self, food_type: str, amount: float) -> bool:
        """Кормит животное."""
        if self.last_feeding and (datetime.now() - self.last_feeding).total_seconds() < 3 * 3600:
            return False
        self.last_feeding = datetime.now()
        self.activity_level = min(100, self.activity_level + 10)
        return True

    def check_health(self) -> str:
        """Проверяет состояние здоровья."""
        if self.stress_level > 80:
            self.health_status = "stressed"
        elif self.activity_level < 30:
            self.health_status = "lethargic"
        else:
            self.health_status = "healthy"
        return self.health_status

    def move_to_tank(self, tank_id: str) -> None:
        """Перемещает животное в другой резервуар."""
        self.tank_id = tank_id
        self.stress_level += 5  # Стресс от перемещения
