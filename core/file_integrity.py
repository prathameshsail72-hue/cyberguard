import os
import hashlib
import mimetypes
from typing import Dict, Any, List

# Known Magic Byte signatures for major file formats
MAGIC_SIGNATURES = {
    "exe": [b'MZ'],
    "dll": [b'MZ'],
    "pdf": [b'%PDF'],
    "png": [b'\x89PNG\r\n\x1a\n'],
    "jpg": [b'\xff\xd8\xff'],
    "jpeg": [b'\xff\xd8\xff'],
    "gif": [b'GIF87a', b'GIF89a'],
    "zip": [b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'],
    "docx": [b'PK\x03\x04'],
    "xlsx": [b'PK\x03\x04'],
    "pptx": [b'PK\x03\x04'],
    "elf": [b'\x7fELF'],
    "rar": [b'Rar!\x1a\x07\x00', b'Rar!\x1a\x07\x01\x00'],
    "7z": [b'7z\xbc\xaf\x27\x1c']
}

DANGEROUS_EXTENSIONS = {
    'exe', 'bat', 'cmd', 'vbs', 'vbe', 'js', 'jse', 'wsf', 'wsh', 'ps1',
    'scr', 'pif', 'com', 'dll', 'sys', 'drv', 'cpl', 'hta', 'jar'
}

class FileIntegrityAnalyzer:
    def analyze(self, file_path: str) -> Dict[str, Any]:
        if not file_path or not os.path.exists(file_path):
            return {"error": f"File path does not exist: {file_path}"}

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        score = 100
        anomalies = []
        recommendations = []

        # 1. Double Extension Masking Detection
        name_parts = file_name.split('.')
        is_double_ext = False
        true_ext = name_parts[-1].lower() if len(name_parts) > 1 else ""
        masked_ext = name_parts[-2].lower() if len(name_parts) > 2 else ""

        if len(name_parts) > 2:
            if true_ext in DANGEROUS_EXTENSIONS and masked_ext in ['pdf', 'doc', 'docx', 'jpg', 'png', 'txt']:
                is_double_ext = True
                score -= 70
                anomalies.append(f"CRITICAL: Double extension deception detected! File poses as '.{masked_ext}' but is an executable '.{true_ext}'.")
                recommendations.append("Do NOT execute or open this file. It is using extension spoofing to bypass user caution.")

        # 2. Executable Extension Check
        if true_ext in DANGEROUS_EXTENSIONS and not is_double_ext:
            score -= 20
            anomalies.append(f"Executable script/program format (.{true_ext}).")
            recommendations.append("Verify the file source before running executable files.")

        # 3. Magic Bytes / Header Validation
        header_bytes = b""
        try:
            with open(file_path, 'rb') as f:
                header_bytes = f.read(16)
                f.seek(0)
                sha256_hash = hashlib.sha256(f.read()).hexdigest()
                f.seek(0)
                md5_hash = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}

        magic_match = False
        expected_magics = MAGIC_SIGNATURES.get(true_ext, [])
        if expected_magics:
            for magic in expected_magics:
                if header_bytes.startswith(magic):
                    magic_match = True
                    break
            if not magic_match:
                score -= 35
                anomalies.append(f"MIME / Magic header mismatch! File extension '.{true_ext}' does not match file header bytes ({header_bytes[:8].hex()}).")
                recommendations.append("File headers indicate content tampering or disguised file format.")
        else:
            magic_match = True  # Unknown signature format

        # Detected MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        score = max(0, min(100, score))
        if score >= 76:
            risk_level = "Low Risk"
        elif score >= 41:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return {
            "file_name": file_name,
            "file_path": file_path,
            "file_size_bytes": file_size,
            "file_size_formatted": self.format_size(file_size),
            "extension": true_ext,
            "mime_type": mime_type,
            "sha256": sha256_hash,
            "md5": md5_hash,
            "header_hex": header_bytes[:8].hex(' '),
            "is_double_ext": is_double_ext,
            "magic_matched": magic_match,
            "risk_score": score,
            "risk_level": risk_level,
            "anomalies": anomalies,
            "recommendations": recommendations
        }

    @staticmethod
    def format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
