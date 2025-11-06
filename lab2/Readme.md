Oceanarium Domain Model
=====================
## CORE MODULE

Animal 14 5 →
- Поля: animal_id, name, species, age, weight, health_status, last_feeding, tank_id, birth_date, medical_records, feeding_schedule, activity_level, stress_level, breeding_status
- Методы: get_feeding_requirements, get_habitat_requirements, feed, check_health, move_to_tank

MarineAnimal 5 3 → Animal
- Поля: salt_tolerance, depth_preference, swimming_speed, oxygen_consumption, territorial_radius
- Методы: get_feeding_requirements, get_habitat_requirements, swim

Dolphin 5 4 → MarineAnimal
- Поля: intelligence_level, echolocation_range, social_group, tricks_learned, communication_frequency
- Методы: perform_trick, learn_trick, echolocate, communicate

Shark 6 3 → MarineAnimal
- Поля: aggression_level, hunting_success_rate, teeth_count, electrical_sense_range, bite_force
- Методы: hunt, detect_electrical_field, shed_teeth

Whale 6 3 → MarineAnimal
- Поля: lung_capacity, dive_depth_max, song_frequency, blubber_thickness, baleen_plates
- Методы: dive, sing, filter_feed

Turtle 6 3 → MarineAnimal
- Поля: shell_hardness, navigation_accuracy, nesting_sites, magnetic_sensitivity, flipper_strength
- Методы: navigate, lay_eggs, retract_into_shell

Jellyfish 6 2 → MarineAnimal
- Поля: tentacle_length, toxicity_level, pulsation_rate, bioluminescence, regeneration_ability
- Методы: pulsate, sting

Octopus 6 3 → MarineAnimal
- Поля: arm_count, intelligence_level, camouflage_ability, ink_capacity, sucker_strength
- Методы: camouflage, release_ink, solve_puzzle

Stingray 5 2 → MarineAnimal
- Поля: wingspan, sting_barb_count, electrical_output, burial_depth
- Методы: bury_in_sand, electric_shock

SeaHorse 6 3 → MarineAnimal
- Поля: tail_length, color_change_ability, gender, pouch_capacity, grip_strength
- Методы: grip_with_tail, change_color, carry_eggs

Staff 11 3 →
- Поля: staff_id, name, position, salary, experience_years, hire_date, certifications, performance_rating, working_hours_per_week, department, access_level
- Методы: perform_daily_tasks, receive_certification, calculate_monthly_salary

Trainer 6 2 → Staff
- Поля: specialization, training_sessions_count, animals_trained, training_techniques, safety_incidents
- Методы: train_animal, assess_animal_behavior

Veterinarian 6 2 → Staff
- Поля: medical_license, surgeries_performed, specializations, patients_treated, emergency_calls
- Методы: examine_animal, prescribe_treatment

Feeder 6 3 → Staff
- Поля: feeding_schedule, food_inventory, animals_assigned, feeding_logs, nutrition_knowledge
- Методы: feed_animal, check_food_quality, restock_food
  
**Исключения**:

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

**Итоги**:
Классы: 63
Поля: 294
Поведения: 113
Ассоциации: 52
Исключения: 13

