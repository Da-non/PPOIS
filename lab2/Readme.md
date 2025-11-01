Oceanarium Domain Model
=====================
Animal 15 4 → Tank, MedicalRecord, FeedingSchedule
MarineAnimal 5 2 → Animal
Dolphin 5 4 → MarineAnimal
Shark 5 4 → MarineAnimal
Whale 5 3 → MarineAnimal
Turtle 5 3 → MarineAnimal
Staff 10 3 → Department, Certification
Trainer 6 3 → Staff, Animal
Veterinarian 6 3 → Staff, Animal
Feeder 6 3 → Staff, Animal

Jellyfish 6 3 → MarineAnimal
Octopus 6 4 → MarineAnimal
Stingray 6 3 → MarineAnimal
SeaHorse 6 3 → MarineAnimal
Manager 6 3 → Staff
SecurityGuard 6 3 → Staff
MaintenanceWorker 6 3 → Staff, Equipment
TourGuide 6 3 → Staff, Visitor
ResearchScientist 6 3 → Staff, Animal
FoodSupplier 7 3 → FoodType, Delivery
EducationalProgram 7 3 → Visitor, Staff
EmergencyResponse 7 3 → EvacuationPlan, Equipment

Equipment 10 3 → Maintenance
WaterPump 4 3 → Equipment
FilterSystem 5 3 → Equipment
TemperatureController 6 3 → Equipment
Tank 10 6 → Animal, Equipment, WaterParameters
MonitoringSystem 8 4 → Sensor, Alert
SecuritySystem 7 4 → AccessZone, KeyCard

FinancialReport 10 3 → Revenue, Expense
BankAccount 10 5 → Transaction
CreditCard 8 3 → Transaction
PaymentProcessor 8 4 → Transaction
Ticket 8 3 → Visitor
Visitor 10 5 → Ticket, VisitHistory
TicketOffice 8 5 → Ticket, Visitor

AquariumShow 5 0 →
ConservationProgram 5 0 →
WaterTreatmentSystem 5 0 →
BreedingProgram 5 0 →
VisitorCenter 5 0 →
ResearchLaboratory 5 0 →
AnimalHospital 5 0 →
UnderwaterTunnel 5 0 →
MarineEcosystem 5 0 →
EducationalCenter 5 0 →
AquacultureFacility 5 0 →
MarineConservation 5 0 →
OceanographicResearch 5 0 →
Oceanarium 15 13 → Animal, Tank, Staff, Visitor, Equipment, MonitoringSystem, SecuritySystem, BankAccount, TicketOffice, FoodSupplier, EducationalProgram, EmergencyResponse

Исключения:

OceanariumBaseException 0 0 →
AnimalNotFoundException 1 0 →
InsufficientFundsException 2 0 →
InvalidPasswordException 1 0 →
TankOverflowException 3 0 →
EquipmentMalfunctionException 2 0 →
UnauthorizedAccessException 2 0 →
FeedingScheduleConflictException 2 0 →
InvalidTemperatureException 3 0 →
TicketExpiredException 2 0 →
MaintenanceModeException 2 0 →
AnimalHealthException 2 0 →
PaymentProcessingException 2 0 →

Итоги:
Классы: 63
Поля: 294
Поведения: 113
Ассоциации: 52
Исключения: 13

