class MarineConservation:
    """Отдел морской консервации."""
    
    def __init__(self, department_id: str, focus_areas: List[str]):
        self.department_id = department_id
        self.focus_areas = focus_areas
        self.conservation_projects = []
        self.research_grants = []
        self.community_outreach = []
        self.success_stories = []
        self.partnerships = []

    def create_conservation_project(self, project_name: str, target_species: str,
                                  duration_months: int, budget: float) -> str:
        """Создаёт проект по сохранению."""
        project_id = f"CONS_{len(self.conservation_projects) + 1}"
        project = {
            "project_id": project_id,
            "name": project_name,
            "target_species": target_species,
            "duration_months": duration_months,
            "budget": budget,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=duration_months * 30),
            "status": "active",
            "progress": 0.0,
            "team_members": [],
            "milestones": []
        }
        self.conservation_projects.append(project)
        return project_id

    def apply_for_grant(self, grant_name: str, amount: float, 
                       purpose: str) -> Dict[str, Any]:
        """Подаёт заявку на грант."""
        grant_id = f"GRANT_{len(self.research_grants) + 1}"
        
        # Симуляция успеха заявки
        success_chance = random.uniform(30, 70)
        approved = random.random() < (success_chance / 100)

        grant = {
            "grant_id": grant_id,
            "name": grant_name,
            "requested_amount": amount,
            "approved_amount": amount * random.uniform(0.7, 1.0) if approved else 0,
            "purpose": purpose,
            "application_date": datetime.now(),
            "status": "approved" if approved else "rejected",
            "decision_date": datetime.now()
        }
        self.research_grants.append(grant)

        return {
            "grant_id": grant_id,
            "approved": approved,
            "amount_approved": grant["approved_amount"],
            "success_chance": success_chance
        }

    def organize_community_event(self, event_name: str, event_type: str,
                               target_audience: str, expected_attendance: int) -> str:
        """Организует мероприятие для сообщества."""
        event_id = f"EVENT_{len(self.community_outreach) + 1}"
        event = {
            "event_id": event_id,
            "name": event_name,
            "type": event_type,  # workshop, seminar, cleanup, etc.
            "target_audience": target_audience,
            "expected_attendance": expected_attendance,
            "actual_attendance": 0,
            "date": datetime.now() + timedelta(days=random.randint(7, 30)),
            "status": "planned",
            "impact_score": 0
        }
        self.community_outreach.append(event)
        return event_id

    def record_success_story(self, title: str, description: str, 
                           species_impacted: str, evidence: str) -> str:
        """Записывает историю успеха."""
        story_id = f"STORY_{len(self.success_stories) + 1}"
        story = {
            "story_id": story_id,
            "title": title,
            "description": description,
            "species_impacted": species_impacted,
            "evidence": evidence,
            "date_recorded": datetime.now(),
            "verification_status": "verified",
            "impact_level": random.choice(["local", "regional", "national"])
        }
        self.success_stories.append(story)
        return story_id

    def get_conservation_report(self) -> Dict[str, Any]:
        """Возвращает отчёт по консервации."""
        active_projects = len([p for p in self.conservation_projects if p["status"] == "active"])
        total_grant_money = sum(g["approved_amount"] for g in self.research_grants if g["status"] == "approved")
        upcoming_events = len([e for e in self.community_outreach if e["status"] == "planned"])
        
        return {
            "department_id": self.department_id,
            "focus_areas": self.focus_areas,
            "active_projects": active_projects,
            "total_grants": len(self.research_grants),
            "grant_money": total_grant_money,
            "community_events": len(self.community_outreach),
            "upcoming_events": upcoming_events,
            "success_stories": len(self.success_stories),
            "partnerships": len(self.partnerships)
        }
