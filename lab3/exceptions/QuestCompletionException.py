class QuestCompletionException(GameDevelopmentBaseException):
    """Исключение при ошибке выполнения квеста."""
    def __init__(self, quest_id, error_reason):
        self.quest_id = quest_id
        self.error_reason = error_reason
        super().__init__(f"Ошибка выполнения квеста {quest_id}: {error_reason}")
