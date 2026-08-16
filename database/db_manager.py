import sqlite3
import json
from typing import List, Dict, Any, Optional
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = str(db_path or DB_PATH)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT NOT NULL,
                    scan_type TEXT NOT NULL,
                    risk_score INTEGER NOT NULL,
                    risk_level TEXT NOT NULL,
                    details_json TEXT,
                    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS survey_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_category TEXT NOT NULL,
                    phishing_awareness_score INTEGER NOT NULL,
                    password_habit_score INTEGER NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    badge_earned TEXT NOT NULL,
                    percentage INTEGER NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Seed default survey analytics if empty for demonstration visuals
            cursor.execute("SELECT COUNT(*) FROM survey_analytics")
            if cursor.fetchone()[0] == 0:
                seed_data = [
                    ("Student / Educator", 85, 70),
                    ("IT Professional", 95, 90),
                    ("General Public", 60, 50),
                    ("Corporate Employee", 75, 80),
                    ("Senior Citizen", 55, 45)
                ]
                cursor.executemany(
                    "INSERT INTO survey_analytics (user_category, phishing_awareness_score, password_habit_score) VALUES (?, ?, ?)",
                    seed_data
                )
            
            conn.commit()

    def save_scan_log(self, target: str, scan_type: str, risk_score: int, risk_level: str, details: Optional[Dict[str, Any]] = None) -> int:
        details_str = json.dumps(details) if details else "{}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO scan_history (target, scan_type, risk_score, risk_level, details_json)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (target, scan_type, risk_score, risk_level, details_str)
            )
            conn.commit()
            return cursor.lastrowid

    def get_scan_history(self, limit: int = 50, scan_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if scan_type:
                cursor.execute(
                    "SELECT * FROM scan_history WHERE scan_type = ? ORDER BY scanned_at DESC LIMIT ?",
                    (scan_type, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM scan_history ORDER BY scanned_at DESC LIMIT ?",
                    (limit,)
                )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("details_json"):
                    try:
                        item["details"] = json.loads(item["details_json"])
                    except Exception:
                        item["details"] = {}
                else:
                    item["details"] = {}
                results.append(item)
            return results

    def get_dashboard_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(risk_score) FROM scan_history")
            total_row = cursor.fetchone()
            total_scans = total_row[0] or 0
            avg_score = round(total_row[1] or 0, 1)

            cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'High Risk'")
            high_risk_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'Medium Risk'")
            medium_risk_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'Low Risk'")
            low_risk_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT scan_type, COUNT(*) FROM scan_history GROUP BY scan_type")
            by_type = dict(cursor.fetchall())

            cursor.execute("SELECT * FROM scan_history ORDER BY scanned_at DESC LIMIT 5")
            recent_scans = [dict(r) for r in cursor.fetchall()]

            return {
                "total_scans": total_scans,
                "avg_score": avg_score,
                "high_risk_count": high_risk_count,
                "medium_risk_count": medium_risk_count,
                "low_risk_count": low_risk_count,
                "by_type": by_type,
                "recent_scans": recent_scans
            }

    def save_survey_response(self, user_category: str, phishing_score: int, password_score: int) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO survey_analytics (user_category, phishing_awareness_score, password_habit_score)
                VALUES (?, ?, ?)
                ''',
                (user_category, phishing_score, password_score)
            )
            conn.commit()
            return cursor.lastrowid

    def get_survey_analytics(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT user_category, 
                       ROUND(AVG(phishing_awareness_score), 1) as avg_phishing,
                       ROUND(AVG(password_habit_score), 1) as avg_password,
                       COUNT(*) as response_count
                FROM survey_analytics
                GROUP BY user_category
                '''
            )
            return [dict(r) for r in cursor.fetchall()]

    def save_quiz_score(self, score: int, total_questions: int, badge_earned: str) -> int:
        percentage = int((score / max(1, total_questions)) * 100)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO quiz_scores (score, total_questions, badge_earned, percentage)
                VALUES (?, ?, ?, ?)
                ''',
                (score, total_questions, badge_earned, percentage)
            )
            conn.commit()
            return cursor.lastrowid

    def get_quiz_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(percentage), MAX(score) FROM quiz_scores")
            row = cursor.fetchone()
            total_attempts = row[0] or 0
            avg_pct = round(row[1] or 0, 1)
            high_score = row[2] or 0

            cursor.execute("SELECT * FROM quiz_scores ORDER BY completed_at DESC LIMIT 5")
            recent_attempts = [dict(r) for r in cursor.fetchall()]

            return {
                "total_attempts": total_attempts,
                "avg_percentage": avg_pct,
                "high_score": high_score,
                "recent_attempts": recent_attempts
            }

