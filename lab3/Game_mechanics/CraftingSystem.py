class CraftingSystem:
    """
    Система крафта.

    Attributes:
        crafting_system_id (str): Уникальный идентификатор системы крафта
        recipes (Dict[str, Dict]): Рецепты крафта
        crafting_stations (List[str]): Станции крафта
    """

    def __init__(self, crafting_system_id: str):
        self.crafting_system_id = crafting_system_id
        self.recipes = {}
        self.crafting_stations = []
        self.crafting_categories = {}
        self.skill_requirements = {}

    def add_recipe(self, recipe_id: str, recipe: Dict[str, Any]) -> None:
        """Добавляет рецепт крафта."""
        self.recipes[recipe_id] = recipe

    def can_craft(self, player: Player, recipe_id: str) -> bool:
        """Проверяет, может ли игрок скрафтить предмет."""
        if recipe_id not in self.recipes:
            return False
        
        recipe = self.recipes[recipe_id]
        
        # Проверяем уровень
        if player.level < recipe.get("required_level", 1):
            return False
        
        # Проверяем навыки
        for skill_id, required_level in recipe.get("required_skills", {}).items():
            if skill_id not in player.skills or player.skills[skill_id].level < required_level:
                return False
        
        # Проверяем материалы
        for material_id, amount in recipe.get("materials", {}).items():
            if not self._has_material(player, material_id, amount):
                return False
        
        return True

    def craft_item(self, player: Player, recipe_id: str) -> Optional[GameItem]:
        """Крафтит предмет."""
        if not self.can_craft(player, recipe_id):
            return None
        
        recipe = self.recipes[recipe_id]
        
        # Тратим материалы
        for material_id, amount in recipe.get("materials", {}).items():
            self._consume_material(player, material_id, amount)
        
        # Создаем предмет
        item = GameItem(
            recipe["result"]["item_id"],
            recipe["result"]["name"],
            recipe["result"]["item_type"],
            recipe["result"].get("rarity", "common")
        )
        
        # Добавляем в инвентарь
        if player.add_item(item):
            return item
        
        return None

    def _has_material(self, player: Player, material_id: str, amount: int) -> bool:
        """Проверяет, есть ли у игрока материал."""
        count = 0
        for item in player.inventory:
            if item and item.entity_id == material_id:
                count += item.current_stack
        return count >= amount

    def _consume_material(self, player: Player, material_id: str, amount: int) -> None:
        """Тратит материал."""
        remaining = amount
        for item in list(player.inventory):
            if item and item.entity_id == material_id and remaining > 0:
                if item.current_stack >= remaining:
                    item.current_stack -= remaining
                    remaining = 0
                else:
                    remaining -= item.current_stack
                    item.current_stack = 0
                if item.current_stack <= 0:
                    player.remove_item(item.entity_id)
