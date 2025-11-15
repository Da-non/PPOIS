class AdminSystem(GameEntity):
    """
    Система административного управления игрой.

    Attributes:
        admin_system_id (str): Уникальный идентификатор системы
        admins (Dict[str, Admin]): Администраторы системы
        permissions (Dict): Разрешения системы
        audit_log (List[Dict]): Лог аудита
    """

    def __init__(self, admin_system_id: str):
        super().__init__(admin_system_id, "AdminSystem")
        self.admins = {}
        self.permissions = {
            "player_management": ["view", "modify", "ban"],
            "server_management": ["restart", "maintenance", "monitor"],
            "economy_management": ["adjust_currency", "view_transactions"],
            "content_management": ["create", "modify", "delete"],
            "system_management": ["shutdown", "backup", "update"]
        }
        self.audit_log = []
        self.backup_schedule = "daily"
        self.system_alerts = []
        self.maintenance_windows = []
        self.security_level = "high"

    def update(self, delta_time: float) -> None:
        """Обновляет состояние административной системы."""
        self._check_system_alerts()
        self._process_scheduled_tasks()

    def add_admin(self, admin_id: str, username: str, permission_level: int) -> 'Admin':
        """Добавляет администратора."""
        admin = Admin(admin_id, username, permission_level)
        self.admins[admin_id] = admin
        return admin

    def remove_admin(self, admin_id: str) -> bool:
        """Удаляет администратора."""
        if admin_id in self.admins:
            del self.admins[admin_id]
            self._log_audit("admin_removed", f"Admin {admin_id} removed from system")
            return True
        return False

    def execute_admin_command(self, admin_id: str, command: str, target: str, 
                            parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Выполняет административную команду."""
        if admin_id not in self.admins:
            raise UnauthorizedGameActionException("execute_admin_command", 1, 0)
        
        admin = self.admins[admin_id]
        if not admin.has_permission(command):
            raise UnauthorizedGameActionException(command, admin.permission_level, admin.permission_level - 1)
        
        result = admin.execute_command(command, target, parameters or {})
        
        # Логируем действие
        self._log_audit(
            "admin_command",
            f"Admin {admin_id} executed {command} on {target}",
            {
                "admin_id": admin_id,
                "command": command,
                "target": target,
                "parameters": parameters,
                "result": result,
                "timestamp": datetime.now()
            }
        )
        
        return result

    def create_maintenance_window(self, start_time: datetime, end_time: datetime, 
                                description: str, affected_servers: List[str]) -> str:
        """Создает окно технического обслуживания."""
        window_id = f"maintenance_{len(self.maintenance_windows) + 1:04d}"
        maintenance_window = {
            "window_id": window_id,
            "start_time": start_time,
            "end_time": end_time,
            "description": description,
            "affected_servers": affected_servers,
            "status": "scheduled",
            "created_at": datetime.now()
        }
        
        self.maintenance_windows.append(maintenance_window)
        self._log_audit("maintenance_scheduled", f"Maintenance window {window_id} scheduled")
        
        return window_id

    def _check_system_alerts(self) -> None:
        """Проверяет системные алерты."""
        current_time = datetime.now()
        
        # Проверяем предстоящие окна обслуживания
        for window in self.maintenance_windows:
            if (window["status"] == "scheduled" and 
                window["start_time"] <= current_time <= window["end_time"]):
                window["status"] = "active"
                self._create_alert("maintenance_started", f"Maintenance started: {window['description']}")

    def _process_scheduled_tasks(self) -> None:
        """Обрабатывает запланированные задачи."""
        current_time = datetime.now()
        
        # Автоматическое резервное копирование
        if self.backup_schedule == "daily" and current_time.hour == 2 and current_time.minute == 0:
            self._perform_system_backup()

    def _perform_system_backup(self) -> None:
        """Выполняет системное резервное копирование."""
        backup_data = {
            "timestamp": datetime.now(),
            "total_players": len(self.admins),  # В реальной системе здесь была бы настоящая статистика
            "system_status": "online",
            "backup_type": "scheduled"
        }
        
        self._log_audit("system_backup", "Scheduled system backup performed", backup_data)

    def _create_alert(self, alert_type: str, message: str, severity: str = "medium") -> None:
        """Создает системный алерт."""
        alert = {
            "alert_id": f"alert_{len(self.system_alerts) + 1:04d}",
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now(),
            "acknowledged": False
        }
        
        self.system_alerts.append(alert)

    def _log_audit(self, action_type: str, description: str, details: Dict[str, Any] = None) -> None:
        """Логирует аудиторское событие."""
        audit_entry = {
            "log_id": f"audit_{len(self.audit_log) + 1:06d}",
            "action_type": action_type,
            "description": description,
            "details": details or {},
            "timestamp": datetime.now()
        }
        
        self.audit_log.append(audit_entry)

    def get_system_report(self) -> Dict[str, Any]:
        """Возвращает системный отчет."""
        return {
            "total_admins": len(self.admins),
            "active_maintenance_windows": len([w for w in self.maintenance_windows if w["status"] == "active"]),
            "pending_alerts": len([a for a in self.system_alerts if not a["acknowledged"]]),
            "audit_log_entries": len(self.audit_log),
            "security_level": self.security_level,
            "backup_schedule": self.backup_schedule
        }

