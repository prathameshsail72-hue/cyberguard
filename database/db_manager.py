import sqlite3
import json
import os
import tempfile
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=None):
        requested_path = str(db_path or os.environ.get("CYBERGUARD_DB_PATH") or DB_PATH)
        self.db_path = requested_path
        
        # Test write access to requested DB path
        try:
            self.init_db()
        except Exception:
            # Fallback to temp directory if primary path is read-only or fails
            temp_db = os.path.join(tempfile.gettempdir(), "cyberguard_fallback.db")
            self.db_path = temp_db
            try:
                self.init_db()
            except Exception:
                # Ultimate fallback to in-memory database
                self.db_path = ":memory:"
                self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

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
                CREATE TABLE IF NOT EXISTS survey_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age_group TEXT NOT NULL,
                    role TEXT NOT NULL,
                    awareness_rating INTEGER NOT NULL,
                    two_factor_auth TEXT NOT NULL,
                    password_reuse TEXT NOT NULL,
                    training_interest TEXT NOT NULL,
                    comments TEXT,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    badge_earned TEXT NOT NULL,
                    percentage INTEGER NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Seed default scan logs if empty
            cursor.execute("SELECT COUNT(*) FROM scan_history")
            if cursor.fetchone()[0] == 0:
                seed_scans = [
                    ("https://github.com", "URL Audit", 95, "Low Risk", json.dumps({"status": "Secure", "https": True})),
                    ("http://192.168.1.1/login-bank", "URL Audit", 20, "High Risk", json.dumps({"status": "Insecure IP", "https": False})),
                    ("[Email: Account Suspended Notice]", "Phishing Scan", 35, "High Risk", json.dumps({"triggers": ["urgent", "account suspended"]})),
                    ("[Password: Tr0ub4dor&3]", "Password Entropy", 88, "Low Risk", json.dumps({"entropy": 68.2, "status": "Strong"})),
                    ("security_audit_report.pdf", "File Integrity", 95, "Low Risk", json.dumps({"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}))
                ]
                cursor.executemany(
                    "INSERT INTO scan_history (target, scan_type, risk_score, risk_level, details_json) VALUES (?, ?, ?, ?, ?)",
                    seed_scans
                )
            
            # Seed default survey analytics if empty for demonstration visuals
            cursor.execute("SELECT COUNT(*) FROM survey_responses")
            if cursor.fetchone()[0] == 0:
                seed_surveys = [
                    ("Alex R.", "18-24", "Student / Educator", 4, "Always on all accounts", "Unique passphrase per account", "Yes, strongly interested", "Great awareness project!"),
                    ("Priya K.", "25-34", "IT / Security Professional", 5, "Always on all accounts", "Unique passphrase per account", "Yes, strongly interested", "Crucial initiative for digital safety."),
                    ("John D.", "35-50", "Corporate Employee", 3, "Only on banking/work", "A few variations reused", "Yes, strongly interested", "Need more workshops at work."),
                    ("Maria S.", "50+", "General Public", 2, "Rarely", "Same password everywhere", "Yes, strongly interested", "Very helpful explanations."),
                    ("David L.", "18-24", "Student / Educator", 4, "Always on all accounts", "A few variations reused", "Maybe in future", "Loved the interactive quiz!")
                ]
                cursor.executemany(
                    "INSERT INTO survey_responses (name, age_group, role, awareness_rating, two_factor_auth, password_reuse, training_interest, comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    seed_surveys
                )

            # Seed default quiz leaderboard entries if empty
            cursor.execute("SELECT COUNT(*) FROM quiz_scores")
            if cursor.fetchone()[0] == 0:
                seed_quizzes = [
                    ("Prathamesh S.", 8, 8, "🛡️ Cyber Guardian Gold", 100),
                    ("Sarah Connor", 8, 8, "🛡️ Cyber Guardian Gold", 100),
                    ("Elliot Alderson", 7, 8, "🥈 Security Apprentice Silver", 88),
                    ("Ada Lovelace", 7, 8, "🥈 Security Apprentice Silver", 88),
                    ("Linus Torvalds", 6, 8, "🥈 Security Apprentice Silver", 75),
                    ("Neo", 5, 8, "🥉 Cyber Defender Bronze", 63)
                ]
                cursor.executemany(
                    "INSERT INTO quiz_scores (player_name, score, total_questions, badge_earned, percentage) VALUES (?, ?, ?, ?, ?)",
                    seed_quizzes
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

            cursor.execute("SELECT * FROM scan_history ORDER BY scanned_at DESC LIMIT 10")
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

    def save_survey_response(
        self,
        role: str = "General Consumer",
        q1: str = "N/A",
        q2: str = "N/A",
        q3: str = "N/A",
        score: int = 0,
        risk_level: str = "Unknown",
        comments: str = "None",
        name: str = "Anonymous",
        age_group: str = "Not Specified",
        training_interest: str = "Not Specified"
    ) -> int:
        """Saves survey responses into the survey_responses table."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO survey_responses (
                    name, age_group, role, awareness_rating, 
                    two_factor_auth, password_reuse, training_interest, comments
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    name,
                    age_group,
                    role,
                    score,
                    q2,
                    q1,
                    training_interest,
                    comments
                )
            )
            conn.commit()
            return cursor.lastrowid

    def get_survey_analytics(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # By Role
            cursor.execute(
                '''
                SELECT role, 
                       ROUND(AVG(awareness_rating), 2) as avg_rating,
                       COUNT(*) as response_count
                FROM survey_responses
                GROUP BY role
                '''
            )
            by_role = [dict(r) for r in cursor.fetchall()]

            # By 2FA
            cursor.execute(
                '''
                SELECT two_factor_auth, COUNT(*) as count
                FROM survey_responses
                GROUP BY two_factor_auth
                '''
            )
            by_2fa = [dict(r) for r in cursor.fetchall()]

            # By Password Reuse
            cursor.execute(
                '''
                SELECT password_reuse, COUNT(*) as count
                FROM survey_responses
                GROUP BY password_reuse
                '''
            )
            by_reuse = [dict(r) for r in cursor.fetchall()]

            # All responses for table view
            cursor.execute("SELECT id, name, age_group, role, awareness_rating, two_factor_auth, password_reuse, training_interest, submitted_at FROM survey_responses ORDER BY submitted_at DESC LIMIT 20")
            recent_responses = [dict(r) for r in cursor.fetchall()]

            return {
                "by_role": by_role,
                "by_2fa": by_2fa,
                "by_reuse": by_reuse,
                "recent_responses": recent_responses
            }

    def save_quiz_score(self, score: int, total_questions: int, badge_earned: str, player_name: str = "Cyber Explorer") -> int:
        percentage = int((score / max(1, total_questions)) * 100)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO quiz_scores (player_name, score, total_questions, badge_earned, percentage)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (player_name or "Cyber Explorer", score, total_questions, badge_earned, percentage)
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

            cursor.execute("SELECT player_name, score, total_questions, percentage, badge_earned, completed_at FROM quiz_scores ORDER BY score DESC, percentage DESC, completed_at ASC LIMIT 10")
            leaderboard = [dict(r) for r in cursor.fetchall()]

            return {
                "total_attempts": total_attempts,
                "avg_percentage": avg_pct,
                "high_score": high_score,
                "leaderboard": leaderboard
            }
