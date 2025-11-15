class GameDesigner(GameEntity):
    """
    Класс игрового дизайнера.
    
    Attributes:
        designer_id (str): Уникальный идентификатор дизайнера
        specialization (str): Специализация (геймдизайн, баланс, нарратив)
        designed_quests (List[str]): Список созданных квестов
        designed_items (List[str]): Список созданных предметов
    """

    def __init__(self, designer_id: str, name: str, specialization: str):
        super().__init__(designer_id, name)
        self.specialization = specialization
        self.designed_quests = []
        self.designed_items = []
        self.balance_proposals = []
        self.design_documents = {}
        self.experience_level = 1
        self.creativity_score = random.randint(70, 100)
        self.analytical_skills = random.randint(60, 95)

    def update(self, delta_time: float) -> None:
        """Обновляет состояние дизайнера."""
        # Дизайнеры улучшают навыки со временем
        if random.random() < 0.001:
            self.creativity_score = min(100, self.creativity_score + 1)
            self.analytical_skills = min(100, self.analytical_skills + 1)

    def create_quest_design(self, quest_id: str, title: str, description: str, 
                          objectives: List[Dict], rewards: Dict) -> Dict[str, Any]:
        """Создает дизайн квеста."""
        quest_design = {
            "quest_id": quest_id,
            "title": title,
            "description": description,
            "objectives": objectives,
            "rewards": rewards,
            "designer": self.entity_id,
            "created_at": datetime.now(),
            "balance_score": self._calculate_balance_score(rewards, objectives)
        }
        
        self.designed_quests.append(quest_id)
        self.design_documents[f"quest_{quest_id}"] = quest_design
        return quest_design

    def create_item_design(self, item_id: str, name: str, item_type: str, 
                          stats: Dict, rarity: str) -> Dict[str, Any]:
        """Создает дизайн предмета."""
        item_design = {
            "item_id": item_id,
            "name": name,
            "type": item_type,
            "stats": stats,
            "rarity": rarity,
            "designer": self.entity_id,
            "created_at": datetime.now(),
            "power_level": self._calculate_power_level(stats, rarity)
        }
        
        self.designed_items.append(item_id)
        self.design_documents[f"item_{item_id}"] = item_design
        return item_design

    def propose_balance_change(self, target_type: str, target_id: str, 
                             changes: Dict, reason: str) -> str:
        """Предлагает изменение баланса."""
        proposal_id = f"balance_{len(self.balance_proposals):04d}"
        proposal = {
            "proposal_id": proposal_id,
            "target_type": target_type,
            "target_id": target_id,
            "changes": changes,
            "reason": reason,
            "designer": self.entity_id,
            "created_at": datetime.now(),
            "status": "pending"
        }
        
        self.balance_proposals.append(proposal)
        return proposal_id

    def _calculate_balance_score(self, rewards: Dict, objectives: List[Dict]) -> float:
        """Вычисляет балл баланса для квеста."""
        exp_reward = rewards.get("experience", 0)
        currency_reward = sum(rewards.get("currency", {}).values())
        objective_difficulty = sum(obj.get("difficulty", 1) for obj in objectives)
        
        balance_score = (exp_reward + currency_reward) / max(1, objective_difficulty)
        return min(10.0, balance_score / 100)

    def _calculate_power_level(self, stats: Dict, rarity: str) -> float:
        """Вычисляет уровень силы предмета."""
        rarity_multiplier = {
            "common": 1.0, "uncommon": 1.5, "rare": 2.0, 
            "epic": 3.0, "legendary": 5.0
        }
        
        total_stats = sum(stats.values())
        return total_stats * rarity_multiplier.get(rarity, 1.0)


class LevelDesigner(GameEntity):
    """
    Класс дизайнера уровней.
    
    Attributes:
        level_designer_id (str): Уникальный идентификатор дизайнера уровней
        designed_levels (List[str]): Список созданных уровней
        environment_assets (List[str]): Используемые ассеты окружения
    """

    def __init__(self, level_designer_id: str, name: str):
        super().__init__(level_designer_id, name)
        self.designed_levels = []
        self.environment_assets = []
        self.level_templates = {}
        self.navigation_meshes = {}
        self.lighting_setups = {}
        self.specialization = "general"  # indoor, outdoor, dungeon, city

    def update(self, delta_time: float) -> None:
        """Обновляет состояние дизайнера уровней."""
        pass

    def create_level(self, level_id: str, level_name: str, level_type: str,
                    size: Tuple[int, int], terrain: Dict) -> Dict[str, Any]:
        """Создает новый уровень."""
        level_design = {
            "level_id": level_id,
            "name": level_name,
            "type": level_type,
            "size": size,
            "terrain": terrain,
            "spawn_points": [],
            "objectives_locations": [],
            "lighting_setup": "default",
            "created_at": datetime.now(),
            "designer": self.entity_id
        }
        
        self.designed_levels.append(level_id)
        self.level_templates[level_id] = level_design
        return level_design

    def add_spawn_point(self, level_id: str, point_type: str, position: Tuple[float, float, float],
                       rotation: Tuple[float, float, float]) -> bool:
        """Добавляет точку спавна на уровень."""
        if level_id not in self.level_templates:
            return False
        
        spawn_point = {
            "type": point_type,  # player, enemy, item
            "position": position,
            "rotation": rotation,
            "id": f"spawn_{len(self.level_templates[level_id]['spawn_points']):03d}"
        }
        
        self.level_templates[level_id]["spawn_points"].append(spawn_point)
        return True

    def generate_navigation_mesh(self, level_id: str, resolution: float = 1.0) -> Dict[str, Any]:
        """Генерирует навигационную сетку для уровня."""
        if level_id not in self.level_templates:
            return {}
        
        # Упрощенная генерация навмеша
        level_size = self.level_templates[level_id]["size"]
        nav_mesh = {
            "level_id": level_id,
            "resolution": resolution,
            "walkable_areas": [],
            "obstacles": [],
            "generated_at": datetime.now()
        }
        
        self.navigation_meshes[level_id] = nav_mesh
        return nav_mesh

    def optimize_level_performance(self, level_id: str) -> Dict[str, Any]:
        """Оптимизирует уровень для производительности."""
        if level_id not in self.level_templates:
            return {}
        
        optimization_report = {
            "level_id": level_id,
            "original_polycount": random.randint(10000, 50000),
            "optimized_polycount": random.randint(5000, 15000),
            "lights_optimized": random.randint(5, 20),
            "colliders_optimized": random.randint(10, 30),
            "performance_gain": random.uniform(15, 40)
        }
        
        return optimization_report
