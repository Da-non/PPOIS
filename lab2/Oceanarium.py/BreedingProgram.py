class BreedingProgram:
    """Программа разведения животных."""
    
    def __init__(self, program_id: str, target_species: str):
        self.program_id = program_id
        self.target_species = target_species
        self.breeding_pairs = []
        self.successful_births = 0
        self.genetic_diversity = 85.0
        self.facilities = []
        self.breeding_season = "year_round"
        self.offspring_records = []
        self.research_data = []

    def add_breeding_pair(self, male: Animal, female: Animal) -> bool:
        """Добавляет пару для разведения."""
        if (male.species == self.target_species and 
            female.species == self.target_species and
            male.gender == "male" and 
            female.gender == "female"):
            
            pair = {
                "male": male,
                "female": female,
                "pairing_date": datetime.now(),
                "successful_breedings": 0,
                "compatibility_score": random.uniform(60, 95)
            }
            self.breeding_pairs.append(pair)
            return True
        return False

    def record_birth(self, mother: Animal, offspring_count: int, date: datetime) -> str:
        """Регистрирует рождение потомства."""
        birth_id = f"BIRTH_{len(self.offspring_records):04d}"
        birth_record = {
            "birth_id": birth_id,
            "mother": mother.animal_id,
            "offspring_count": offspring_count,
            "birth_date": date,
            "survival_rate": random.uniform(80, 98),
            "health_status": "good"
        }
        
        self.offspring_records.append(birth_record)
        self.successful_births += offspring_count
        
        # Обновление генетического разнообразия
        self.genetic_diversity = min(95, self.genetic_diversity + 0.5)
        
        return birth_id

    def calculate_success_rate(self) -> float:
        """Рассчитывает успешность программы разведения."""
        if not self.breeding_pairs:
            return 0.0
            
        total_pairs = len(self.breeding_pairs)
        successful_pairs = sum(1 for pair in self.breeding_pairs 
                             if pair["successful_breedings"] > 0)
        
        pair_success = (successful_pairs / total_pairs) * 100
        genetic_score = self.genetic_diversity
        birth_success = min(100, (self.successful_births / max(1, total_pairs)) * 10)
        
        return (pair_success + genetic_score + birth_success) / 3
