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

## ADDITIONAL MODULE 

Jellyfish 6 4 → MarineAnimal
- Поля: tentacle_length, toxicity_level, pulsation_rate, bioluminescence, regeneration_ability
- Методы: get_feeding_requirements, get_habitat_requirements, pulsate, sting

Octopus 6 5 → MarineAnimal
- Поля: arm_count, intelligence_level, camouflage_ability, ink_capacity, sucker_strength
- Методы: get_feeding_requirements, get_habitat_requirements, camouflage, release_ink, solve_puzzle

Stingray 5 4 → MarineAnimal
- Поля: wingspan, sting_barb_count, electrical_output, burial_depth
- Методы: get_feeding_requirements, get_habitat_requirements, bury_in_sand, electric_shock

SeaHorse 6 5 → MarineAnimal
- Поля: tail_length, color_change_ability, gender, pouch_capacity, grip_strength
- Методы: get_feeding_requirements, get_habitat_requirements, grip_with_tail, change_color, carry_eggs

Manager 6 4 → Staff
- Поля: department, team_size, decision_authority, meetings_per_week, budget_responsibility
- Методы: perform_daily_tasks, make_decision, conduct_meeting, approve_budget

SecurityGuard 6 4 → Staff
- Поля: patrol_route, security_clearance, emergency_response_time, incident_reports, radio_frequency
- Методы: perform_daily_tasks, patrol, respond_to_emergency, file_incident_report

MaintenanceWorker 6 4 → Staff
- Поля: specialization, tools_inventory, work_orders_completed, safety_incidents, efficiency_rating
- Методы: perform_daily_tasks, repair_equipment, perform_preventive_maintenance, add_tool

TourGuide 6 4 → Staff
- Поля: languages, tour_routes, groups_per_day, visitor_satisfaction, knowledge_base
- Методы: perform_daily_tasks, conduct_tour, add_language, learn_animal_facts

ResearchScientist 6 4 → Staff
- Поля: research_field, publications, current_projects, research_grants, laboratory_access
- Методы: perform_daily_tasks, conduct_study, publish_research, apply_for_grant

FoodSupplier 9 4 →
- Поля: supplier_id, company_name, food_types, delivery_schedule, quality_rating, price_per_kg, reliability_score, contact_info, payment_terms
- Методы: add_food_type, schedule_delivery, deliver_food, check_quality

EducationalProgram 10 4 → Staff, Visitor
- Поля: program_id, name, target_audience, duration_minutes, learning_objectives, required_animals, materials_needed, instructor, participant_limit, effectiveness_rating
- Методы: add_learning_objective, assign_instructor, conduct_session, evaluate_effectiveness

EmergencyResponse 7 5 →
- Поля: response_id, emergency_contacts, evacuation_plans, emergency_equipment, incident_log, alert_system, response_time_target
- Методы: create_evacuation_plan, trigger_emergency_alert, initiate_evacuation, add_emergency_equipment, test_emergency_systems

## OCEANARIUM MAIN MODULE 

AquariumShow 11 5 → Animal, Trainer
- Поля: show_id, name, duration, schedule, animals_involved, trainers_required, equipment_needed, max_spectators, show_type, difficulty_level, success_rate
- Методы: schedule_show, add_animal, add_trainer, conduct_show, get_show_statistics

ConservationProgram 11 6 → ResearchScientist
- Поля: program_id, species, goal, budget, researchers, success_rate, start_date, end_date, milestones, funding_sources, published_research
- Методы: allocate_budget, add_researcher, add_milestone, complete_milestone, publish_research, get_program_progress

WaterTreatmentSystem 8 5 → Equipment
- Поля: system_id, capacity, filtration_level, chemical_balance, maintenance_schedule, water_quality_history, filtration_media_age, max_media_age
- Методы: perform_maintenance, treat_water, schedule_maintenance, get_water_quality_report

BreedingProgram 9 5 → Animal
- Поля: program_id, target_species, breeding_pairs, successful_births, genetic_diversity, breeding_season, gestation_period, offspring_survival_rate, research_data
- Методы: add_breeding_pair, attempt_breeding, introduce_new_genetics, get_program_statistics

VisitorCenter 9 6 → Visitor, TourGuide
- Поля: center_id, capacity, facilities, daily_visitors, guided_tours, current_visitors, opening_time, closing_time, facility_cleanliness
- Методы: add_facility, register_visitor, remove_visitor, schedule_guided_tour, clean_facilities, get_center_status

ResearchLaboratory 8 6 → Equipment, ResearchScientist
- Поля: lab_id, specialization, equipment, research_projects, publications, safety_level, certification_status, resource_utilization
- Методы: add_equipment, start_research_project, add_team_member, record_finding, publish_research, get_laboratory_report

AnimalHospital 8 7 → Animal, Veterinarian
- Поля: hospital_id, capacity, quarantine_units, surgical_rooms, patients, medical_staff, medical_equipment, success_rate
- Методы: add_quarantine_unit, add_surgical_room, admit_patient, assign_veterinarian, perform_surgery, discharge_patient, get_hospital_status

UnderwaterTunnel 9 6 → Visitor
- Поля: tunnel_id, length, viewing_windows, cleaning_schedule, visitor_capacity, current_visitors, water_visibility, lighting_intensity, maintenance_status
- Методы: add_viewing_window, enter_tunnel, exit_tunnel, schedule_cleaning, perform_cleaning, get_tunnel_status

MarineEcosystem 8 6 →
- Поля: ecosystem_id, biome_type, species_diversity, environmental_params, conservation_status, food_web, biodiversity_index, threat_level
- Методы: add_species, update_environmental_param, assess_ecosystem_health, calculate_biodiversity_index, get_ecosystem_report

EducationalCenter 7 7 → Staff
- Поля: center_id, classrooms, workshops, student_groups, educational_materials, available_classrooms, booking_schedule
- Методы: create_workshop, register_student_group, add_educational_material, book_classroom, conduct_workshop, get_center_statistics

AquacultureFacility 8 6 →
- Поля: facility_id, production_type, production_capacity, species_cultured, harvest_schedule, water_quality_params, feed_inventory, growth_data
- Методы: add_species, schedule_harvest, monitor_growth, perform_harvest, get_facility_report

MarineConservation 7 6 →
- Поля: department_id, focus_areas, conservation_projects, research_grants, community_outreach, success_stories, partnerships
- Методы: create_conservation_project, apply_for_grant, organize_community_event, record_success_story, get_conservation_report

OceanographicResearch 7 6 →
- Поля: research_id, ocean_region, research_vessels, data_collection, scientific_discoveries, research_expeditions, collaborating_institutions
- Методы: add_research_vessel, plan_expedition, collect_ocean_data, record_discovery, get_research_summary

Oceanarium 21 20 → Animal, Tank, Staff, Visitor, Equipment, MonitoringSystem, SecuritySystem, EmergencyResponse, PaymentProcessor, BankAccount, TicketOffice, FoodSupplier, EducationalProgram
- Поля: name, location, capacity, opening_hours, animals, tanks, staff, visitors, equipment, monitoring_system, security_system, emergency_response, payment_processor, bank_account, ticket_offices, food_suppliers, educational_programs, daily_visitors, monthly_revenue, operational_status, last_inspection_date
- Методы: add_animal, add_tank, hire_staff, add_visitor, create_ticket_office, add_food_supplier, create_educational_program, feed_all_animals, conduct_health_checks, monitor_water_quality, generate_daily_report, process_visitor_entry, conduct_training_session, schedule_maintenance, activate_emergency_protocol, close_for_day, open_for_day, get_occupancy_rate, transfer_animal, calculate_monthly_expenses, get_animal_statistics

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
Поля: 418
Поведения: 246
Ассоциации: 52
Исключения: 13

