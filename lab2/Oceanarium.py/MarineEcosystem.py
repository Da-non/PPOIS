class MarineEcosystem:
    """Модель морской экосистемы."""
    
    def __init__(self, ecosystem_id: str, biome_type: str):
        self.ecosystem_id = ecosystem_id
        self.biome_type = biome_type
        self.species_diversity = []
        self.environmental_params = {
            "temperature": random.uniform(15, 28),
            "salinity": random.uniform(30, 38),
            "ph": random.uniform(7.5, 8.4),
            "oxygen_level": random.uniform(85, 100)
        }
        self.conservation_status = "stable"
        self.food_web = {}
        self.biodiversity_index = 0.0
        self.threats = []

    def add_species(self, species_name: str, population: int, role: str) -> None:
        """Добавляет вид в экосистему."""
        species = {
            "name": species_name,
            "population": population,
            "role": role,  # producer, consumer, decomposer
            "status": "stable",
            "reproduction_rate": random.uniform(1.0, 3.0)
        }
        self.species_diversity.append(species)
        self._update_biodiversity_index()

    def _update_biodiversity_index(self) -> None:
        """Обновляет индекс биоразнообразия."""
        species_count = len(self.species_diversity)
        population_diversity = sum(
            sp["population"] for sp in self.species_diversity
        ) / max(1, species_count)
        
        self.biodiversity_index = (species_count * population_diversity) / 100

    def simulate_ecosystem_changes(self, time_period: str) -> Dict[str, any]:
        """Симулирует изменения в экосистеме."""
        changes = {
            "period": time_period,
            "timestamp": datetime.now(),
            "population_changes": {},
            "environmental_changes": {},
            "new_interactions": []
        }

        # Симуляция изменений популяции
        for species in self.species_diversity:
            change_factor = random.uniform(0.9, 1.1)
            new_population = int(species["population"] * change_factor)
            changes["population_changes"][species["name"]] = {
                "old": species["population"],
                "new": new_population
            }
            species["population"] = new_population

        # Симуляция изменений окружающей среды
        for param in self.environmental_params:
            change = random.uniform(-0.5, 0.5)
            self.environmental_params[param] += change

        self._update_biodiversity_index()
        return changes
