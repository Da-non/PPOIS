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

## EQUIPMENT MODULE

Equipment 11 3 →
- Поля: equipment_id, name, manufacturer, installation_date, status, last_maintenance, maintenance_interval_days, power_consumption, warranty_expires, error_codes, operating_hours
- Методы: perform_maintenance, check_status, reset_error

WaterPump 4 3 → Equipment
- Поля: flow_rate, pressure, pump_type, impeller_speed
- Методы: perform_maintenance, adjust_flow_rate, check_cavitation

FilterSystem 5 4 → Equipment
- Поля: filter_capacity, filter_type, efficiency, filter_media_age, backwash_frequency
- Методы: perform_maintenance, backwash, replace_filter_media

TemperatureController 6 4 → Equipment
- Поля: target_temperature, current_temperature, heating_power, cooling_power, temperature_tolerance, sensor_accuracy
- Методы: perform_maintenance, set_temperature, regulate_temperature

Tank 11 7 → Animal, Equipment
- Поля: tank_id, capacity, current_volume, tank_type, animals, equipment, water_parameters, last_cleaned, viewing_windows, depth, surface_area
- Методы: add_animal, remove_animal, get_max_animals, check_animal_compatibility, add_equipment, check_water_quality, clean_tank

MonitoringSystem 8 6 →
- Поля: system_id, sensors, alerts, data_logs, monitoring_frequency, alert_thresholds, backup_systems, notification_emails
- Методы: add_sensor, read_sensor_data, check_alert_thresholds, create_alert, acknowledge_alert

SecuritySystem 8 5 →
- Поля: system_id, access_zones, key_cards, security_logs, emergency_mode, cameras, motion_sensors, alarm_status
- Методы: create_access_zone, issue_keycard, check_access, log_security_event, activate_emergency_mode

## FINANCE MODULE 

FinancialReport 13 5 →
- Поля: report_id, period_start, period_end, report_type, revenue_breakdown, expense_breakdown, profit_loss, visitor_statistics, animal_care_costs, staff_costs, maintenance_costs, generated_date, is_finalized
- Методы: add_revenue_category, add_expense_category, calculate_profit_loss, generate_summary, finalize_report

BankAccount 12 7 →
- Поля: account_number, holder_name, balance, currency, account_type, created_date, transactions, daily_limit, daily_spent, last_reset_date, is_frozen, overdraft_limit
- Методы: deposit, withdraw, transfer, add_transaction, get_balance, reset_daily_limit

CreditCard 12 4 →
- Поля: card_number, holder_name, expiry_date, cvv, credit_limit, current_balance, minimum_payment, interest_rate, is_active, is_blocked, transactions, payment_due_date
- Методы: charge, make_payment, block_card, unblock_card

PaymentProcessor 7 4 → CreditCard
- Поля: processor_id, supported_methods, transaction_fee, daily_limits, processed_transactions, failed_transactions, maintenance_mode
- Методы: process_payment, refund_payment, get_daily_volume

Ticket 11 3 →
- Поля: ticket_id, ticket_type, price, valid_from, valid_until, is_used, purchase_time, visitor_id, entry_time, exit_time, special_permissions
- Методы: validate, use_ticket, add_special_permission

Visitor 13 5 → Ticket, PaymentProcessor
- Поля: visitor_id, name, email, phone, age, registration_date, tickets, visit_history, preferences, membership_type, loyalty_points, emergency_contact, special_needs
- Методы: purchase_ticket, enter_oceanarium, exit_oceanarium, add_preference, upgrade_membership

TicketOffice 10 8 → Visitor, CreditCard, PaymentProcessor
- Поля: office_id, cashier_name, ticket_prices, daily_sales, cash_register, shift_start_time, shift_end_time, payment_processor, discount_codes, promotional_offers
- Методы: start_shift, sell_ticket, apply_discounts, end_shift, get_payment_method_breakdown, add_discount_code, add_promotional_offer

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

