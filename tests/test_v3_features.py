import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_manager import DatabaseManager

class TestCyberGuard3ProFeatures(unittest.TestCase):
    def setUp(self):
        self.db_name = f"test_cyberguard_{self._testMethodName}.db"
        if os.path.exists(self.db_name):
            try: os.remove(self.db_name)
            except Exception: pass
        self.db = DatabaseManager(self.db_name)

    def tearDown(self):
        if hasattr(self, 'db_name') and os.path.exists(self.db_name):
            try: os.remove(self.db_name)
            except Exception: pass

    def test_quiz_database_integration(self):
        last_id = self.db.save_quiz_score(score=5, total_questions=5, badge_earned="Cyber Master - Level 3")
        self.assertGreater(last_id, 0)

        stats = self.db.get_quiz_stats()
        self.assertGreaterEqual(stats["total_attempts"], 1)
        self.assertGreaterEqual(stats["high_score"], 5)
        self.assertGreater(stats["avg_percentage"], 0)

    def test_survey_analytics(self):
        self.db.save_survey_response(
            name="Alice", age_group="25-34", role="Corporate Employee", awareness_rating=8,
            two_factor_auth="Yes, on all accounts", password_reuse="Never", training_interest="Yes, interested", comments="Great tool!"
        )
        analytics = self.db.get_survey_analytics()
        self.assertTrue(any(item["role"] == "Corporate Employee" for item in analytics.get("by_role", [])))

if __name__ == "__main__":
    unittest.main()
