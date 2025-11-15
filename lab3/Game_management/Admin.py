class Admin(GameEntity):
    """
    Класс администратора игры.

    Attributes:
        admin_id (str): Уникальный идентификатор администратора
        username (str): Имя администратора
        permission_level (int): Уровень разрешений
        last_login (datetime): Последний вход
    """

    def __init__(self, admin_id: str, username: str, permission_level: int):
        super().__init__(admin_id, username)
        self.admin_id = admin_id
        self.username = username
        self.permission_level = permission_level
        self.last_login = datetime.now()
        self.is_active = True
        self.assigned_servers = []
        self.specializations = []
        self.command_history = []
        self.login_history = []
        self.two_factor_enabled = False
        self.session_timeout = 3600  # 1 час в секундах
        self.email = f"{username}@gameadmin.com"
        self.phone_number = ""
        self.department = "operations"

    def update(self, delta_time: float) -> None:
        """Обновляет состояние администратора."""
        # Проверка таймаута сессии
        if (datetime.now() - self.last_login).total_seconds() > self.session_timeout:
            self.is_active = False

    def has_permission(self, permission: str) -> bool:
        """Проверяет наличие разрешения."""
        permission_levels = {
            "view_players": 1,
            "modify_players": 2,
            "ban_players": 3,
            "restart_servers": 2,
            "system_maintenance": 4,
            "economy_management": 3,
            "content_management": 3,
            "system_shutdown": 5,
            "view_logs": 1,
            "manage_admins": 5
        }
        
        required_level = permission_levels.get(permission, 999)
        return self.permission_level >= required_level

    def execute_command(self, command: str, target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Выполняет административную команду."""
        if not self.has_permission(command):
            raise UnauthorizedGameActionException(command, self.permission_level + 1, self.permission_level)
        
        # Симуляция выполнения команды
        command_result = {
            "command": command,
            "target": target,
            "parameters": parameters,
            "executed_by": self.entity_id,
            "timestamp": datetime.now(),
            "success": True,
            "message": f"Command {command} executed successfully on {target}",
            "execution_time": random.uniform(0.1, 2.0)
        }
        
        # Специфическая логика для разных команд
        if command == "restart_servers":
            command_result["affected_servers"] = parameters.get("servers", [])
            command_result["restart_time"] = datetime.now() + timedelta(minutes=5)
        elif command == "ban_players":
            command_result["banned_players"] = parameters.get("players", [])
            command_result["duration_days"] = parameters.get("duration", 7)
        
        # Записываем в историю команд
        self.command_history.append(command_result)
        
        return command_result

    def login(self, password_hash: str) -> bool:
        """Выполняет вход администратора."""
        # Упрощенная проверка аутентификации
        if self._authenticate(password_hash):
            self.last_login = datetime.now()
            self.is_active = True
            
            login_record = {
                "timestamp": self.last_login,
                "ip_address": "127.0.0.1",  # В реальной системе здесь был бы реальный IP
                "success": True
            }
            self.login_history.append(login_record)
            
            return True
        return False

    def logout(self) -> None:
        """Выполняет выход администратора."""
        self.is_active = False

    def add_specialization(self, specialization: str) -> None:
        """Добавляет специализацию администратора."""
        if specialization not in self.specializations:
            self.specializations.append(specialization)

    def assign_server(self, server_id: str) -> bool:
        """Назначает сервер под управление администратора."""
        if server_id not in self.assigned_servers:
            self.assigned_servers.append(server_id)
            return True
        return False

    def _authenticate(self, password_hash: str) -> bool:
        """Аутентифицирует администратора."""
        # Упрощенная реализация аутентификации
        expected_hash = hashlib.sha256(f"admin_{self.username}".encode()).hexdigest()
        return password_hash == expected_hash

    def get_admin_stats(self) -> Dict[str, Any]:
        """Возвращает статистику администратора."""
        return {
            "admin_id": self.entity_id,
            "username": self.username,
            "permission_level": self.permission_level,
            "is_active": self.is_active,
            "assigned_servers": len(self.assigned_servers),
            "specializations": self.specializations,
            "total_commands": len(self.command_history),
            "last_login": self.last_login,
            "session_active": self.is_active
        }


