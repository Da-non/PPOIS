class AnimalHospital:
    """Ветеринарная больница для животных."""
    
    def __init__(self, hospital_id: str, capacity: int):
        self.hospital_id = hospital_id
        self.capacity = capacity
        self.quarantine_units = []
        self.surgical_rooms = []
        self.patients = []
        self.medical_staff = []
        self.medical_equipment = []
        self.success_rate = random.uniform(85, 98)

    def add_quarantine_unit(self, unit_id: str, capacity: int) -> bool:
        """Добавляет карантинное отделение."""
        unit = {
            "unit_id": unit_id,
            "capacity": capacity,
            "current_patients": [],
            "isolation_level": random.randint(1, 3)
        }
        self.quarantine_units.append(unit)
        return True

    def add_surgical_room(self, room_id: str, equipment: List[str]) -> bool:
        """Добавляет операционную."""
        room = {
            "room_id": room_id,
            "equipment": equipment,
            "is_occupied": False,
            "last_sterilization": datetime.now()
        }
        self.surgical_rooms.append(room)
        return True

    def admit_patient(self, animal: Animal, condition: str, severity: int) -> str:
        """Принимает пациента в больницу."""
        if len(self.patients) >= self.capacity:
            raise Exception("Больница переполнена")

        case_id = f"CASE_{len(self.patients) + 1}"
        patient = {
            "case_id": case_id,
            "animal": animal,
            "condition": condition,
            "severity": severity,
            "admission_date": datetime.now(),
            "treatment_plan": [],
            "status": "under_observation",
            "assigned_vet": None
        }
        self.patients.append(patient)
        return case_id

    def assign_veterinarian(self, case_id: str, veterinarian: Veterinarian) -> bool:
        """Назначает ветеринара на случай."""
        for patient in self.patients:
            if patient["case_id"] == case_id:
                patient["assigned_vet"] = veterinarian
                return True
        return False

    def perform_surgery(self, case_id: str, surgery_type: str, room_id: str) -> Dict[str, Any]:
        """Выполняет операцию."""
        # Находим пациента и операционную
        patient = next((p for p in self.patients if p["case_id"] == case_id), None)
        room = next((r for r in self.surgical_rooms if r["room_id"] == room_id), None)
        
        if not patient or not room or room["is_occupied"]:
            return {"success": False, "error": "Недоступно"}

        room["is_occupied"] = True
        success = random.random() < (self.success_rate / 100)

        if success:
            patient["status"] = "recovering"
            patient["treatment_plan"].append({
                "type": "surgery",
                "surgery_type": surgery_type,
                "date": datetime.now(),
                "success": True
            })
        else:
            patient["status"] = "critical"

        room["is_occupied"] = False
        room["last_sterilization"] = datetime.now()

        return {
            "success": success,
            "case_id": case_id,
            "surgery_type": surgery_type,
            "patient_status": patient["status"]
        }

    def discharge_patient(self, case_id: str) -> bool:
        """Выписывает пациента."""
        for i, patient in enumerate(self.patients):
            if patient["case_id"] == case_id:
                discharged_patient = self.patients.pop(i)
                # Обновляем здоровье животного
                discharged_patient["animal"].health_status = "healthy"
                discharged_patient["animal"].stress_level = max(0, discharged_patient["animal"].stress_level - 20)
                return True
        return False

    def get_hospital_status(self) -> Dict[str, Any]:
        """Возвращает статус больницы."""
        current_patients = len(self.patients)
        available_rooms = len([r for r in self.surgical_rooms if not r["is_occupied"]])
        
        return {
            "hospital_id": self.hospital_id,
            "current_patients": current_patients,
            "capacity_utilization": (current_patients / self.capacity) * 100,
            "available_surgical_rooms": available_rooms,
            "quarantine_units": len(self.quarantine_units),
            "medical_staff": len(self.medical_staff),
            "success_rate": self.success_rate
        }
