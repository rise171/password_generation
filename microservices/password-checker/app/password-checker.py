import re
from typing import Dict

class PasswordStrengthChecker:
    @staticmethod
    def check_strength(password: str) -> Dict:
        if not password:
            return {"strength": "Пустой", "score": 0}
        
        score = 0
        feedback = []
        
        # Проверка длины
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Пароль должен содержать минимум 8 символов")
        
        # Проверка на наличие цифр
        if re.search(r"\d", password):
            score += 1
        else:
            feedback.append("Добавьте цифры")
        
        # Проверка на наличие букв в нижнем регистре
        if re.search(r"[a-z]", password):
            score += 1
        else:
            feedback.append("Добавьте строчные буквы")
        
        # Проверка на наличие букв в верхнем регистре
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")
        
        # Проверка на наличие специальных символов
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")
        
        # Определение уровня сложности
        if score <= 2:
            strength = "Слабый"
        elif score <= 3:
            strength = "Средний"
        elif score <= 4:
            strength = "Хороший"
        else:
            strength = "Надёжный"
        
        return {
            "strength": strength,
            "score": score,
            "feedback": feedback,
            "length": len(password)
        }