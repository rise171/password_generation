import json
import datetime
from typing import Dict, List
import os

class ActivityLogger:
    def __init__(self, log_file: str = "activity_logs.json"):
        self.log_file = log_file
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Создает файл логов если он не существует"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_activity(self, user_id: int, action: str, service_name: str = None, details: Dict = None) -> Dict:
        """Логирует действие пользователя"""
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "service_name": service_name,
            "details": details or {}
        }
        
        try:
            # Читаем существующие логи
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            # Добавляем новую запись
            logs.append(log_entry)
            
            # Сохраняем обратно (ограничиваем количество записей для демо)
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            return {"status": "success", "message": "Activity logged successfully"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to log activity: {str(e)}"}
    
    def get_user_activities(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Получает действия конкретного пользователя"""
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            user_logs = [log for log in logs if log.get('user_id') == user_id]
            return user_logs[-limit:]
            
        except Exception as e:
            return []
    
    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Получает последние действия всех пользователей"""
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            return logs[-limit:]
            
        except Exception as e:
            return []