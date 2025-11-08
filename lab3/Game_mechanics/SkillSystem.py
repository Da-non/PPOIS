class SkillSystem:
    """
    Система навыков.

    Attributes:
        skill_system_id (str): Уникальный идентификатор системы навыков
        available_skills (Dict[str, Skill]): Доступные навыки
        skill_trees (Dict[str, List[str]]): Деревья навыков
    """

    def __init__(self, skill_system_id: str):
        self.skill_system_id = skill_system_id
        self.available_skills = {}
        self.skill_trees = {}
        self.skill_categories = {}
        self.skill_requirements = {}

    def add_skill(self, skill: Skill) -> None:
        """Добавляет навык в систему."""
        self.available_skills[skill.entity_id] = skill

    def add_skill_to_tree(self, tree_name: str, skill_id: str) -> None:
        """Добавляет навык в дерево навыков."""
        if tree_name not in self.skill_trees:
            self.skill_trees[tree_name] = []
        if skill_id not in self.skill_trees[tree_name]:
            self.skill_trees[tree_name].append(skill_id)

    def get_available_skills_for_player(self, player: Player) -> List[Skill]:
        """Возвращает доступные навыки для игрока."""
        available = []
        for skill in self.available_skills.values():
            if self._can_learn_skill(player, skill):
                available.append(skill)
        return available

    def learn_skill(self, player: Player, skill_id: str) -> bool:
        """Изучает навык."""
        if skill_id not in self.available_skills:
            return False
        
        skill = self.available_skills[skill_id]
        if not self._can_learn_skill(player, skill):
            return False
        
        return player.learn_skill(skill)

    def _can_learn_skill(self, player: Player, skill: Skill) -> bool:
        """Проверяет, может ли игрок изучить навык."""
        if player.level < skill.required_level:
            return False
        
        if skill.entity_id in player.skills:
            return False
        
        # Проверяем требования по дереву навыков
        for tree_name, skills in self.skill_trees.items():
            if skill.entity_id in skills:
                skill_index = skills.index(skill.entity_id)
                if skill_index > 0:
                    prev_skill_id = skills[skill_index - 1]
                    if prev_skill_id not in player.skills:
                        return False
        
        return True

    def get_skill_progression(self, player: Player, skill_id: str) -> Dict[str, Any]:
        """Возвращает прогресс изучения навыка."""
        if skill_id not in self.available_skills:
            return {}
        
        skill = self.available_skills[skill_id]
        if skill_id in player.skills:
            player_skill = player.skills[skill_id]
            return {
                "level": player_skill.level,
                "experience": player_skill.experience,
                "max_level": player_skill.max_level,
                "progress": player_skill.experience / (player_skill.level * 100)
            }
        else:
            return {
                "level": 0,
                "experience": 0,
                "max_level": skill.max_level,
                "progress": 0
            }
