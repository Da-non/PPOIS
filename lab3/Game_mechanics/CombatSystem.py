class CombatSystem:
    """
    Система боя.

    Attributes:
        combat_id (str): Уникальный идентификатор боя
        participants (List[Character]): Участники боя
        turn_order (List[Character]): Порядок ходов
        current_turn (int): Текущий ход
        combat_state (str): Состояние боя
    """

    def __init__(self, combat_id: str):
        self.combat_id = combat_id
        self.participants = []
        self.turn_order = []
        self.current_turn = 0
        self.combat_state = "waiting"  # waiting, active, finished
        self.round_number = 1
        self.combat_log = []
        self.conditions = {}  # Статусные эффекты
        self.terrain_effects = []
        self.weather_effects = []

    def add_participant(self, character: Character) -> bool:
        """Добавляет участника боя."""
        if character not in self.participants:
            self.participants.append(character)
            return True
        return False

    def remove_participant(self, character: Character) -> bool:
        """Удаляет участника боя."""
        if character in self.participants:
            self.participants.remove(character)
            if character in self.turn_order:
                self.turn_order.remove(character)
            return True
        return False

    def start_combat(self) -> None:
        """Начинает бой."""
        if len(self.participants) < 2:
            raise InvalidGameStateException("start_combat", "Недостаточно участников")
        
        self.combat_state = "active"
        self.turn_order = sorted(self.participants, key=lambda x: x.stats.get("agility", 10), reverse=True)
        self.current_turn = 0
        self.round_number = 1
        self.combat_log.append(f"Бой начался! Участники: {[p.name for p in self.participants]}")

    def end_combat(self) -> None:
        """Завершает бой."""
        self.combat_state = "finished"
        self.combat_log.append("Бой завершен!")

    def get_current_character(self) -> Optional[Character]:
        """Возвращает текущего персонажа."""
        if self.combat_state == "active" and self.turn_order:
            return self.turn_order[self.current_turn % len(self.turn_order)]
        return None

    def next_turn(self) -> None:
        """Переходит к следующему ходу."""
        if self.combat_state != "active":
            return
        
        self.current_turn += 1
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.round_number += 1

    def attack(self, attacker: Character, target: Character, attack_type: str = "basic") -> Dict[str, Any]:
        """Выполняет атаку."""
        if self.combat_state != "active":
            raise InvalidGameStateException("attack", "Бой не активен")
        
        if attacker not in self.participants or target not in self.participants:
            raise ValueError("Участник не в бою")
        
        if attacker.health <= 0 or target.health <= 0:
            raise ValueError("Мертвый персонаж не может атаковать")
        
        # Вычисляем урон
        base_damage = attacker.calculate_damage(10)
        damage_modifier = self._calculate_damage_modifier(attacker, target, attack_type)
        final_damage = base_damage * damage_modifier
        
        # Применяем урон
        target.take_damage(final_damage)
        
        # Логируем атаку
        attack_log = {
            "attacker": attacker.name,
            "target": target.name,
            "attack_type": attack_type,
            "damage": final_damage,
            "target_health_after": target.health,
            "timestamp": datetime.now()
        }
        self.combat_log.append(attack_log)
        
        # Проверяем, не убит ли цель
        if target.health <= 0:
            self.combat_log.append(f"{target.name} убит!")
            self._check_combat_end()
        
        return attack_log

    def use_skill(self, caster: Character, target: Optional[Character], skill_id: str) -> Dict[str, Any]:
        """Использует навык в бою."""
        if self.combat_state != "active":
            raise InvalidGameStateException("use_skill", "Бой не активен")
        
        if skill_id not in caster.skills:
            raise ValueError("Навык не изучен")
        
        skill = caster.skills[skill_id]
        if not caster.use_mana(skill.mana_cost):
            raise ValueError("Недостаточно маны")
        
        # Активируем навык
        success = skill.activate(caster, target)
        
        skill_log = {
            "caster": caster.name,
            "target": target.name if target else None,
            "skill": skill.name,
            "success": success,
            "timestamp": datetime.now()
        }
        self.combat_log.append(skill_log)
        
        return skill_log

    def _calculate_damage_modifier(self, attacker: Character, target: Character, attack_type: str) -> float:
        """Вычисляет модификатор урона."""
        modifier = 1.0
        
        # Модификатор по типу атаки
        if attack_type == "critical":
            modifier *= 2.0
        elif attack_type == "weak":
            modifier *= 0.5
        
        # Модификатор по характеристикам
        attacker_strength = attacker.stats.get("strength", 10)
        target_constitution = target.stats.get("constitution", 10)
        stat_modifier = (attacker_strength - target_constitution) * 0.1
        modifier += stat_modifier
        
        # Случайный модификатор
        modifier *= random.uniform(0.8, 1.2)
        
        return max(0.1, modifier)  # Минимум 10% урона

    def _check_combat_end(self) -> None:
        """Проверяет, не закончился ли бой."""
        alive_participants = [p for p in self.participants if p.health > 0]
        if len(alive_participants) <= 1:
            self.end_combat()
