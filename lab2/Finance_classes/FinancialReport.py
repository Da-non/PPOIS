class FinancialReport:
"""
    Класс для генерации финансовых отчетов.
    
    Attributes:
        report_id (str): Уникальный идентификатор отчета
        period_start (datetime): Начало отчетного периода
        period_end (datetime): Конец отчетного периода
        report_type (str): Тип отчета (ежемесячный, квартальный, годовой)
    """
    
    def __init__(self, report_id: str, period_start: datetime, period_end: datetime, report_type: str):
        self.report_id = report_id
        self.period_start = period_start
        self.period_end = period_end
        self.report_type = report_type
        self.revenue_breakdown = {}
        self.expense_breakdown = {}
        self.profit_loss = 0.0
        self.visitor_statistics = {}
        self.animal_care_costs = 0.0
        self.staff_costs = 0.0
        self.maintenance_costs = 0.0
        self.generated_date = datetime.now()
        self.is_finalized = False
        
    def add_revenue_category(self, category: str, amount: float) -> None:
        """Добавляет категорию доходов."""
        self.revenue_breakdown[category] = amount
        
    def add_expense_category(self, category: str, amount: float) -> None:
        """Добавляет категорию расходов."""
        self.expense_breakdown[category] = amount
        
    def calculate_profit_loss(self) -> float:
        """Вычисляет прибыль/убыток."""
        total_revenue = sum(self.revenue_breakdown.values())
        total_expenses = sum(self.expense_breakdown.values())
        self.profit_loss = total_revenue - total_expenses
        return self.profit_loss
        
    def generate_summary(self) -> Dict[str, any]:
        """Генерирует сводку отчета."""
        return {
            "report_id": self.report_id,
            "period": f"{self.period_start.date()} - {self.period_end.date()}",
            "total_revenue": sum(self.revenue_breakdown.values()),
            "total_expenses": sum(self.expense_breakdown.values()),
            "net_profit": self.profit_loss,
            "visitor_count": self.visitor_statistics.get("total", 0),
            "generation_date": self.generated_date
        }
        
    def finalize_report(self) -> bool:
        """Финаализирует отчет."""
        self.calculate_profit_loss()
        self.is_finalized = True
        return True
