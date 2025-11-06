class AnimalHospital:
    """Ветеринарная больница для животных."""
    
    def __init__(self, hospital_id: str, capacity: int):
        self.hospital_id = hospital_id
        self.capacity = capacity
        self.quarantine_units = []
        self.surgical_rooms = []
        self.patients = []
        self.medical_equipment = []
        self.veterinarians = []
        self.recovery_rate = 85.0
        self.emergency_capacity = 5

    def admit_patient(self, animal: Animal, condition: str, severity: int) -> str:
        """Принимает животное на лечение."""
        if len(self.patients) < self.capacity:
            patient_id = f"PATIENT_{len(self.patients):04d}"
            patient = {
                "patient_id": patient_id,
                "animal": animal,
                "admission_date": datetime.now(),
                "condition": condition,
                "severity": severity,
                "treatment_plan": [],
                "status": "under_observation",
                "assigned_vet": None
            }
            self.patients.append(patient)
            return patient_id
        return ""

    def assign_veterinarian(self, patient_id: str, vet: Veterinarian) -> bool:
        """Назначает ветеринара пациенту."""
        for patient in self.patients:
            if patient["patient_id"] == patient_id:
                patient["assigned_vet"] = vet
                return True
        return False

    def perform_surgery(self, patient_id: str, surgery_type: str, 
                       duration_hours: float) -> Dict[str, any]:
        """Выполняет операцию."""
        surgery_result = {
            "patient_id": patient_id,
            "surgery_type": surgery_type,
            "duration": duration_hours,
            "success": random.random() > 0.1,  # 90% успеха
            "complications": random.randint(0, 2),
            "timestamp": datetime.now()
        }
        
        if surgery_result["success"]:
            self.recovery_rate = min(95, self.recovery_rate + 1)
        
        return surgery_result

    def add_quarantine_unit(self, unit_id: str, capacity: int) -> None:
        """Добавляет карантинный блок."""
        unit = {
            "unit_id": unit_id,
            "capacity": capacity,
            "current_occupants": 0,
            "isolation_level": "high",
            "cleaning_status": "clean"
        }
        self.quarantine_units.append(unit)
