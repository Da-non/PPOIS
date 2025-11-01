Oceanarium Domain Model
=====================

Основные классы (49):
Animal 13 4 → MarineAnimal, Tank, Veterinarian, Feeder
BankAccount 12 6 → PaymentProcessor, Oceanarium
CreditCard 10 5 → PaymentProcessor
Dolphin 8 4 → MarineAnimal, Trainer
EducationalProgram 8 5 → Staff, Visitor
EmergencyResponse 8 5 → SecuritySystem, Oceanarium
Equipment 10 4 → MaintenanceWorker, Tank
Feeder 8 4 → Animal, Staff, FoodSupplier
FilterSystem 8 4 → Equipment, Tank
FoodSupplier 8 4 → Animal, Feeder
Jellyfish 8 4 → MarineAnimal
Manager 8 4 → Staff
MaintenanceWorker 8 4 → Equipment, Staff
MarineAnimal 8 4 → Animal, Tank
MonitoringSystem 10 5 → Equipment, Tank, Oceanarium
Octopus 8 4 → MarineAnimal
Oceanarium 32 17 → Animal, BankAccount, Equipment, Staff, Tank, Visitor, MonitoringSystem, SecuritySystem, EmergencyResponse, PaymentProcessor
PaymentProcessor 10 5 → BankAccount, CreditCard, Ticket, TicketOffice
ResearchScientist 8 4 → Animal, Staff
SeaHorse 9 4 → MarineAnimal
SecurityGuard 8 4 → Staff, SecuritySystem
SecuritySystem 10 5 → Staff, Oceanarium, EmergencyResponse
Shark 8 4 → MarineAnimal
Staff 12 4 → Oceanarium, SecuritySystem, Animal
Stingray 8 4 → MarineAnimal
TemperatureController 8 4 → Equipment, Tank
Ticket 10 4 → PaymentProcessor, Visitor, Oceanarium
TicketOffice 12 6 → PaymentProcessor, Ticket, Visitor, Oceanarium
TourGuide 8 4 → Staff, Visitor
Trainer 8 4 → Animal, Staff
Turtle 8 4 → MarineAnimal
Veterinarian 9 4 → Animal, Staff
Visitor 12 6 → Ticket, EducationalProgram, Oceanarium
WaterPump 8 4 → Equipment, Tank

Исключения (13):
AnimalHealthException 2 1 → Animal, Veterinarian
AnimalNotFoundException 1 1 → Animal, Tank
EquipmentMalfunctionException 2 1 → Equipment, MaintenanceWorker
FeedingScheduleConflictException 2 1 → Animal, Feeder
InsufficientFundsException 2 1 → BankAccount, PaymentProcessor
InvalidPasswordException 1 1 → Staff, SecuritySystem
InvalidTemperatureException 3 1 → TemperatureController, Tank
MaintenanceModeException 2 1 → Equipment, Oceanarium
OceanariumBaseException 0 1 →
PaymentProcessingException 2 1 → PaymentProcessor, TicketOffice
TankOverflowException 3 1 → Tank, Animal
TicketExpiredException 2 1 → Ticket, Visitor
UnauthorizedAccessException 2 1 → SecuritySystem, Staff

Итоги
Поля: 287
Поведения: 201
Ассоциации: 67
Исключения: 13
