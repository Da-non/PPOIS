class UnderwaterTunnel:
    """Подводный туннель для посетителей."""
    
    def __init__(self, tunnel_id: str, length: float):
        self.tunnel_id = tunnel_id
        self.length = length
        self.viewing_windows = []
        self.cleaning_schedule = []
        self.visitor_capacity = 50
        self.current_visitors = []
        self.water_visibility = random.uniform(80, 100)
        self.lighting_intensity = random.uniform(70, 100)
        self.maintenance_status = "operational"

    def add_viewing_window(self, window_id: str, size: str, location: float) -> bool:
        """Добавляет смотровое окно."""
        window = {
            "window_id": window_id,
            "size": size,
            "location": location,  # положение вдоль туннеля
            "cleanliness": 100.0,
            "last_cleaned": datetime.now()
        }
        self.viewing_windows.append(window)
        return True

    def enter_tunnel(self, visitor: Visitor) -> bool:
        """Посетитель входит в туннель."""
        if len(self.current_visitors) < self.visitor_capacity:
            self.current_visitors.append(visitor)
            # Небольшое снижение видимости из-за посетителей
            self.water_visibility = max(60, self.water_visibility - 0.1)
            return True
        return False

    def exit_tunnel(self, visitor: Visitor) -> bool:
        """Посетитель выходит из туннеля."""
        if visitor in self.current_visitors:
            self.current_visitors.remove(visitor)
            return True
        return False

    def schedule_cleaning(self, cleaning_date: datetime, cleaning_crew: List[str]) -> str:
        """Планирует очистку туннеля."""
        cleaning_id = f"CLEAN_{len(self.cleaning_schedule) + 1}"
        cleaning = {
            "cleaning_id": cleaning_id,
            "date": cleaning_date,
            "crew": cleaning_crew,
            "status": "scheduled",
            "duration_hours": random.randint(2, 6)
        }
        self.cleaning_schedule.append(cleaning)
        return cleaning_id

    def perform_cleaning(self) -> bool:
        """Выполняет очистку туннеля."""
        self.water_visibility = 100.0
        for window in self.viewing_windows:
            window["cleanliness"] = 100.0
            window["last_cleaned"] = datetime.now()
        return True

    def get_tunnel_status(self) -> Dict[str, Any]:
        """Возвращает статус туннеля."""
        occupancy = (len(self.current_visitors) / self.visitor_capacity) * 100
        
        return {
            "tunnel_id": self.tunnel_id,
            "length": self.length,
            "current_visitors": len(self.current_visitors),
            "occupancy_rate": occupancy,
            "water_visibility": self.water_visibility,
            "viewing_windows": len(self.viewing_windows),
            "maintenance_status": self.maintenance_status,
            "next_cleaning": self.cleaning_schedule[0]["date"] if self.cleaning_schedule else None
        }


class MarineEcosystem:
    """Модель морской экосистемы."""
    
    def __init__(self, ecosystem_id: str, biome_type: str):
        self.ecosystem_id = ecosystem_id
        self.biome_type = biome_type
        self.species_diversity = []
        self.environmental_params = {
            "temperature": random.uniform(15, 28),
            "salinity": random.uniform(30, 40),
            "ph": random.uniform(7.8, 8.4),
            "oxygen_level": random.uniform(85, 100),
            "nutrient_level": random.uniform(60, 90)
        }
        self.conservation_status = "stable"
        self.food_web = {}
        self.biodiversity_index = random.uniform(70, 95)
        self.threat_level = random.randint(1, 5)

    def add_species(self, species: str, population: int, role: str) -> bool:
        """Добавляет вид в экосистему."""
        species_data = {
            "species": species,
            "population": population,
            "role": role,  # producer, consumer, decomposer
            "status": "stable",
            "last_assessment": datetime.now()
        }
        self.species_diversity.append(species_data)
        self.calculate_biodiversity_index()
        return True

    def update_environmental_param(self, param: str, value: float) -> bool:
        """Обновляет параметр окружающей среды."""
        if param in self.environmental_params:
            self.environmental_params[param] = value
            self.assess_ecosystem_health()
            return True
        return False

    def assess_ecosystem_health(self) -> str:
        """Оценивает здоровье экосистемы."""
        temp = self.environmental_params["temperature"]
        salinity = self.environmental_params["salinity"]
        ph = self.environmental_params["ph"]
        oxygen = self.environmental_params["oxygen_level"]

        health_score = 0
        
        # Оценка температуры
        if 20 <= temp <= 26:
            health_score += 25
        elif 18 <= temp <= 28:
            health_score += 20
        else:
            health_score += 10

        # Оценка солёности
        if 33 <= salinity <= 37:
            health_score += 25
        else:
            health_score += 15

        # Оценка pH
        if 7.8 <= ph <= 8.4:
            health_score += 25
        else:
            health_score += 15

        # Оценка кислорода
        if oxygen >= 90:
            health_score += 25
        elif oxygen >= 80:
            health_score += 20
        else:
            health_score += 10

        # Определение статуса сохранения
        if health_score >= 90:
            self.conservation_status = "excellent"
        elif health_score >= 75:
            self.conservation_status = "good"
        elif health_score >= 60:
            self.conservation_status = "stable"
        elif health_score >= 40:
            self.conservation_status = "vulnerable"
        else:
            self.conservation_status = "endangered"

        return self.conservation_status

    def calculate_biodiversity_index(self) -> float:
        """Вычисляет индекс биоразнообразия."""
        total_species = len(self.species_diversity)
        if total_species == 0:
            self.biodiversity_index = 0
            return 0

        # Простой расчет индекса разнообразия
        base_index = min(100, total_species * 5)
        population_health = sum(1 for s in self.species_diversity if s["status"] == "stable") / total_species * 100
        
        self.biodiversity_index = (base_index + population_health) / 2
        return self.biodiversity_index

    def get_ecosystem_report(self) -> Dict[str, Any]:
        """Возвращает отчёт экосистемы."""
        return {
            "ecosystem_id": self.ecosystem_id,
            "biome_type": self.biome_type,
            "species_count": len(self.species_diversity),
            "biodiversity_index": self.biodiversity_index,
            "conservation_status": self.conservation_status,
            "environmental_params": self.environmental_params,
            "threat_level": self.threat_level,
            "health_assessment": self.assess_ecosystem_health()
        }

