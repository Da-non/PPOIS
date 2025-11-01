class Tank:
    """
    Класс резервуара для животных.

    Attributes:
        tank_id (str): Уникальный идентификатор резервуара
        capacity (float): Объём в литрах
        current_volume (float): Текущий объём воды
        animals (List[Animal]): Список животных в резервуаре
        equipment (List[Equipment]): Список оборудования
    """

    def __init__(self, tank_id: str, capacity: float, tank_type: str):
        self.tank_id = tank_id
        self.capacity = capacity
        self.current_volume = capacity * 0.9  # 90% заполнения
        self.tank_type = tank_type  # "display", "quarantine", "breeding"
        self.animals = []
        self.equipment = []
        self.water_parameters = {
            "temperature": 24.0,
            "salinity": 35.0,
            "ph": 8.1,
            "ammonia": 0.0,
            "nitrite": 0.0,
            "nitrate": 5.0
        }
        self.last_cleaned = datetime.now()
        self.viewing_windows = random.randint(1, 4)
        self.depth = random.uniform(3, 15)  # метры
        self.surface_area = capacity / (self.depth * 1000)  # м²

    def add_animal(self, animal: Animal) -> bool:
        """Добавляет животное в резервуар."""
        if len(self.animals) >= self.get_max_animals():
            return False

        # Проверяем совместимость
        if self.check_animal_compatibility(animal):
            self.animals.append(animal)
            animal.move_to_tank(self.tank_id)
            return True
        return False

    def remove_animal(self, animal_id: str) -> bool:
        """Удаляет животное из резервуара."""
        for animal in self.animals:
            if animal.animal_id == animal_id:
                self.animals.remove(animal)
                animal.tank_id = None
                return True
        raise AnimalNotFoundException(animal_id)

    def get_max_animals(self) -> int:
        """Возвращает максимальное количество животных."""
        base_capacity = int(self.capacity / 10000)  # 1 животное на 10000л
        return max(1, base_capacity)

    def check_animal_compatibility(self, new_animal: Animal) -> bool:
        """Проверяет совместимость с существующими животными."""
        from .core import Shark  # Локальный импорт для избежания циклических зависимостей
        for existing_animal in self.animals:
            # Хищники и добыча несовместимы
            if (isinstance(existing_animal, Shark) and not isinstance(new_animal, Shark)) or \
               (isinstance(new_animal, Shark) and not isinstance(existing_animal, Shark)):
                return False
        return True

    def add_equipment(self, equipment: Equipment) -> bool:
        """Добавляет оборудование к резервуару."""
        self.equipment.append(equipment)
        return True

    def check_water_quality(self) -> Dict[str, bool]:
        """Проверяет качество воды."""
        quality_check = {}

        # Проверяем каждый параметр
        quality_check["temperature"] = 20 <= self.water_parameters["temperature"] <= 28
        quality_check["salinity"] = 30 <= self.water_parameters["salinity"] <= 40
        quality_check["ph"] = 7.8 <= self.water_parameters["ph"] <= 8.4
        quality_check["ammonia"] = self.water_parameters["ammonia"] < 0.25
        quality_check["nitrite"] = self.water_parameters["nitrite"] < 0.5
        quality_check["nitrate"] = self.water_parameters["nitrate"] < 20

        return quality_check

    def clean_tank(self) -> bool:
        """Очищает резервуар."""
        self.last_cleaned = datetime.now()
        # Улучшаем качество воды после очистки
        self.water_parameters["ammonia"] *= 0.5
        self.water_parameters["nitrite"] *= 0.5
        self.water_parameters["nitrate"] *= 0.7
        return True
