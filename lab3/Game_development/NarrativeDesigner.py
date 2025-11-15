class NarrativeDesigner(GameEntity):
    """
    Класс нарративного дизайнера.
    
    Attributes:
        narrative_designer_id (str): Уникальный идентификатор дизайнера
        written_quests (List[str]): Написанные квесты
        character_backstories (Dict): Предыстории персонажей
        world_lore (Dict): Лор игрового мира
    """

    def __init__(self, narrative_designer_id: str, name: str):
        super().__init__(narrative_designer_id, name)
        self.written_quests = []
        self.character_backstories = {}
        self.world_lore = {}
        self.dialogue_trees = {}
        self.writing_style = "fantasy"  # fantasy, sci-fi, realistic, etc.
        self.story_arcs = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние нарративного дизайнера."""
        pass

    def create_character_backstory(self, character_id: str, backstory: str,
                                 personality_traits: List[str], motivations: List[str]) -> Dict[str, Any]:
        """Создает предысторию персонажа."""
        backstory_data = {
            "character_id": character_id,
            "backstory": backstory,
            "personality_traits": personality_traits,
            "motivations": motivations,
            "created_at": datetime.now(),
            "writer": self.entity_id
        }
        
        self.character_backstories[character_id] = backstory_data
        return backstory_data

    def write_quest_narrative(self, quest_id: str, introduction: str, conclusion: str,
                             npc_dialogues: Dict[str, str]) -> Dict[str, Any]:
        """Пишет нарратив для квеста."""
        narrative = {
            "quest_id": quest_id,
            "introduction": introduction,
            "conclusion": conclusion,
            "npc_dialogues": npc_dialogues,
            "written_at": datetime.now(),
            "writer": self.entity_id
        }
        
        self.written_quests.append(quest_id)
        return narrative

    def add_world_lore(self, lore_id: str, title: str, content: str, category: str) -> Dict[str, Any]:
        """Добавляет лор игрового мира."""
        lore_entry = {
            "lore_id": lore_id,
            "title": title,
            "content": content,
            "category": category,
            "added_at": datetime.now(),
            "writer": self.entity_id
        }
        
        self.world_lore[lore_id] = lore_entry
        return lore_entry

    def create_dialogue_tree(self, npc_id: str, dialogues: List[Dict]) -> Dict[str, Any]:
        """Создает дерево диалогов для NPC."""
        dialogue_tree = {
            "npc_id": npc_id,
            "dialogues": dialogues,
            "created_at": datetime.now(),
            "writer": self.entity_id
        }
        
        self.dialogue_trees[npc_id] = dialogue_tree
        return dialogue_tree

    def create_story_arc(self, arc_id: str, title: str, chapters: List[Dict]) -> Dict[str, Any]:
        """Создает сюжетную арку."""
        story_arc = {
            "arc_id": arc_id,
            "title": title,
            "chapters": chapters,
            "created_at": datetime.now(),
            "writer": self.entity_id,
            "estimated_playtime_hours": sum(chapter.get("duration_hours", 1) for chapter in chapters)
        }
        
        self.story_arcs[arc_id] = story_arc
        return story_arc

