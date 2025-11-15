class CommunityManager(GameEntity):
    """
    Класс менеджера сообщества.
    
    Attributes:
        community_manager_id (str): Уникальный идентификатор менеджера
        managed_platforms (List): Управляемые платформы
        community_events (List): Мероприятия сообщества
        feedback_reports (Dict): Отчеты по обратной связи
    """

    def __init__(self, community_manager_id: str, name: str):
        super().__init__(community_manager_id, name)
        self.managed_platforms = ["discord", "forum", "social_media"]
        self.community_events = []
        self.feedback_reports = {}
        self.player_sentiment = {}
        self.community_guidelines = {}
        self.communication_channels = {}

    def update(self, delta_time: float) -> None:
        """Обновляет состояние менеджера сообщества."""
        # Мониторинг настроения сообщества
        if random.random() < 0.005:
            self._update_player_sentiment()

    def organize_community_event(self, event_id: str, title: str, event_type: str,
                               start_time: datetime, duration_hours: int) -> Dict[str, Any]:
        """Организует мероприятие для сообщества."""
        community_event = {
            "event_id": event_id,
            "title": title,
            "type": event_type,  # contest, tournament, qna, etc.
            "start_time": start_time,
            "duration_hours": duration_hours,
            "organized_by": self.entity_id,
            "status": "scheduled",
            "participants": [],
            "prizes": []
        }
        
        self.community_events.append(community_event)
        return community_event

    def collect_player_feedback(self, feedback_id: str, player_id: str,
                              category: str, content: str, rating: int) -> Dict[str, Any]:
        """Собирает обратную связь от игроков."""
        feedback = {
            "feedback_id": feedback_id,
            "player_id": player_id,
            "category": category,  # gameplay, balance, bugs, suggestions
            "content": content,
            "rating": rating,  # 1-5 stars
            "received_at": datetime.now(),
            "status": "new",
            "priority": self._calculate_feedback_priority(category, rating)
        }
        
        self.feedback_reports[feedback_id] = feedback
        return feedback

    def create_community_report(self, report_id: str, period: str) -> Dict[str, Any]:
        """Создает отчет по сообществу."""
        report = {
            "report_id": report_id,
            "period": period,  # daily, weekly, monthly
            "generated_at": datetime.now(),
            "total_feedback": len(self.feedback_reports),
            "average_sentiment": self._calculate_average_sentiment(),
            "active_community_members": random.randint(100, 10000),
            "top_issues": self._get_top_issues(),
            "event_participation": len([e for e in self.community_events if e["status"] == "completed"]),
            "recommendations": self._generate_recommendations()
        }
        
        return report

    def _update_player_sentiment(self) -> None:
        """Обновляет данные о настроении игроков."""
        sentiment_categories = ["gameplay", "balance", "content", "performance", "support"]
        for category in sentiment_categories:
            self.player_sentiment[category] = random.uniform(0.3, 0.9)

    def _calculate_feedback_priority(self, category: str, rating: int) -> str:
        """Вычисляет приоритет обратной связи."""
        if rating <= 2:
            return "high"
        elif category in ["bugs", "performance"]:
            return "medium"
        else:
            return "low"

    def _calculate_average_sentiment(self) -> float:
        """Вычисляет среднее настроение сообщества."""
        if not self.player_sentiment:
            return 0.7
        return sum(self.player_sentiment.values()) / len(self.player_sentiment)

    def _get_top_issues(self) -> List[Dict]:
        """Возвращает топ проблем от сообщества."""
        issues = []
        categories = ["balance", "bugs", "performance", "content", "ui"]
        for category in categories:
            issues.append({
                "category": category,
                "count": random.randint(5, 50),
                "sentiment": random.uniform(0.3, 0.8)
            })
        return sorted(issues, key=lambda x: x["count"], reverse=True)[:3]

    def _generate_recommendations(self) -> List[str]:
        """Генерирует рекомендации на основе обратной связи."""
        recommendations = []
        
        if self.player_sentiment.get("balance", 0.7) < 0.6:
            recommendations.append("Рассмотреть баланс классов и предметов")
        
        if self.player_sentiment.get("content", 0.7) < 0.6:
            recommendations.append("Добавить новый контент и активность")
        
        if len(self.feedback_reports) > 50:
            recommendations.append("Увеличить скорость обработки обратной связи")
        
        return recommendations

