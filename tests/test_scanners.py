import os
import sys
import unittest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_manager import DatabaseManager
from core.url_analyzer import URLAnalyzer
from core.phishing_detector import PhishingDetector
from core.password_analyzer import PasswordAnalyzer
from core.file_integrity import FileIntegrityAnalyzer

class TestCyberGuardModules(unittest.TestCase):
    def setUp(self):
        self.db_name = f"test_cyberguard_{self._testMethodName}.db"
        if os.path.exists(self.db_name):
            try: os.remove(self.db_name)
            except Exception: pass

        self.db = DatabaseManager(self.db_name)
        self.url_analyzer = URLAnalyzer(timeout=2)
        self.phishing_detector = PhishingDetector()
        self.password_analyzer = PasswordAnalyzer()
        self.file_analyzer = FileIntegrityAnalyzer()

    def tearDown(self):
        if hasattr(self, 'db_name') and os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except Exception:
                pass

    def test_database_init_and_logging(self):
        last_id = self.db.save_scan_log("https://test.com", "URL Security", 85, "Low Risk", {"test": True})
        self.assertGreater(last_id, 0)
        history = self.db.get_scan_history(limit=10)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["target"], "https://test.com")

    def test_url_analyzer(self):
        res = self.url_analyzer.analyze("http://192.168.1.1/login-banking-update-long-url-path-test-verify-credentials")
        self.assertEqual(res["risk_level"], "High Risk")
        self.assertLessEqual(res["risk_score"], 40)
        self.assertIn("issues", res)

    def test_phishing_detector(self):
        text = "URGENT ACTION REQUIRED! Your account will be suspended within 24 hours unless you click log in now and verify your password."
        res = self.phishing_detector.analyze(text)
        self.assertEqual(res["risk_level"], "High Risk")
        self.assertGreaterEqual(res["phishing_risk_score"], 60)

    def test_password_analyzer(self):
        res = self.password_analyzer.analyze("password123")
        self.assertEqual(res["risk_level"], "High Risk")
        self.assertTrue(res["is_common"])

        res_strong = self.password_analyzer.analyze("Tr0u84d0ur&CyberGuard#2026!")
        self.assertEqual(res_strong["status"], "Very Strong")
        self.assertGreaterEqual(res_strong["entropy_bits"], 80)

    def test_file_integrity(self):
        test_file = "test_invoice.pdf.exe"
        with open(test_file, "wb") as f:
            f.write(b"MZ\x90\x00\x03\x00\x00\x00")
        
        try:
            res = self.file_analyzer.analyze(test_file)
            self.assertTrue(res["is_double_ext"])
            self.assertEqual(res["risk_level"], "High Risk")
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
