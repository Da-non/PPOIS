class BreedingProgram:
    """Программа разведения животных."""
    
    def __init__(self, program_id: str, target_species: str):
        self.program_id = program_id
        self.target_species = target_species
        self.breeding_pairs = []
        self.successful_births = 0
        self.genetic_diversity = 85.0
        self.breeding_season = random.choice(["spring", "summer", "year_round"])
        self.gestation_period = random.randint(30, 365)  # дни
        self.offspring_survival_rate = random.uniform(60, 95)
        self.research_data = []

    def add_breeding_pair(self, animal1: Animal, animal2: Animal) -> bool:
        """Добавляет пару для разведения."""
        if (animal1.species == self.target_species and 
            animal2.species == self.target_species and
            animal1.animal_id != animal2.animal_id):
            
            pair = {
                "male": animal1 if random.random() > 0.5 else animal2,
                "female": animal2 if random.random() > 0.5 else animal1,
                "pairing_date": datetime.now(),
                "successful_breedings": 0,
                "last_breeding": None
            }
            self.breeding_pairs.append(pair)
            return True
        return False

    def attempt_breeding(self, pair_index: int) -> Dict[str, Any]:
        """Пытается провести размножение пары."""
        if pair_index >= len(self.breeding_pairs):
            raise ValueError("Неверный индекс пары")

        pair = self.breeding_pairs[pair_index]
        success_chance = random.uniform(40, 80)
        
        # Учитываем генетическое разнообразие
        success_chance *= (self.genetic_diversity / 100)
        
        success = random.random() < (success_chance / 100)

        if success:
            pair["successful_breedings"] += 1
            pair["last_breeding"] = datetime.now()
            self.successful_births += random.randint(1, 3)  # 1-3 детёныша
            self.genetic_diversity = max(70, self.genetic_diversity - 0.5)  # Небольшое снижение разнообразия

        result = {
            "success": success,
            "pair_index": pair_index,
            "breeding_date": datetime.now(),
            "genetic_diversity_impact": -0.5 if success else 0,
            "offspring_count": random.randint(1, 3) if success else 0
        }

        self.research_data.append(result)
        return result

    def introduce_new_genetics(self, new_animal: Animal) -> bool:
        """Вводит новую генетику в программу."""
        if new_animal.species == self.target_species:
            self.genetic_diversity = min(95.0, self.genetic_diversity + 5.0)
            return True
        return False

    def get_program_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику программы."""
        active_pairs = len([p for p in self.breeding_pairs if p["last_breeding"] is None or 
                          (datetime.now() - p["last_breeding"]).days > 30])
        
        return {
            "program_id": self.program_id,
            "target_species": self.target_species,
            "breeding_pairs": len(self.breeding_pairs),
            "active_pairs": active_pairs,
            "successful_births": self.successful_births,
            "genetic_diversity": self.genetic_diversity,
            "survival_rate": self.offspring_survival_rate,
            "research_data_points": len(self.research_data)
        }

