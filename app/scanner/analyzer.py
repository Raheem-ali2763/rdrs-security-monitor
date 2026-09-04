from __future__ import annotations

import hashlib
import math
import mimetypes
from pathlib import Path


SAMPLE_SIZE = 64 * 1024


def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy for a byte sequence, 0.0 to 8.0."""
    if not data:
        return 0.0

    frequencies = [0] * 256

    for byte in data:
        frequencies[byte] += 1

    length = len(data)
    entropy = 0.0

    for frequency in frequencies:
        if frequency:
            probability = frequency / length
            entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def sha256_file(path: Path) -> str:
    """Calculate SHA-256 without loading the entire file into memory."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def analyze_file(path: str | Path) -> dict:
    """Collect static metadata and ransomware-oriented indicators."""
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    size = file_path.stat().st_size

    with file_path.open("rb") as file:
        sample = file.read(SAMPLE_SIZE)

    entropy = calculate_entropy(sample)
    sha256 = sha256_file(file_path)

    mime_type, _ = mimetypes.guess_type(file_path.name)

    indicators: list[str] = []
    score = 0

    if entropy >= 7.5:
        indicators.append("very_high_entropy")
        score += 25
    elif entropy >= 7.0:
        indicators.append("high_entropy")
        score += 15

    suspicious_extensions = {
        ".locked",
        ".encrypted",
        ".enc",
        ".crypt",
        ".crypto",
        ".ransom",
        ".wncry",
        ".lockbit",
    }

    if file_path.suffix.lower() in suspicious_extensions:
        indicators.append("suspicious_extension")
        score += 30

    ransomware_keywords = {
        "ransom",
        "decrypt",
        "encrypted",
        "bitcoin",
        "payment",
        "readme",
        "recover",
    }

    filename_lower = file_path.name.lower()

    matched_keywords = [
        keyword for keyword in ransomware_keywords
        if keyword in filename_lower
    ]

    if matched_keywords:
        indicators.append("ransomware_related_filename")
        score += 20

    if size > 0 and entropy >= 7.0 and file_path.suffix.lower() in suspicious_extensions:
        indicators.append("encrypted_file_pattern")
        score += 15

    score = min(score, 100)

    if score >= 70:
        verdict = "Malicious/Suspicious"
        severity = "Critical"
    elif score >= 40:
        verdict = "Suspicious"
        severity = "Warning"
    else:
        verdict = "No Strong Indicators"
        severity = "Normal"

    return {
        "filename": file_path.name,
        "path": str(file_path.resolve()),
        "size": size,
        "extension": file_path.suffix.lower(),
        "mime_type": mime_type or "application/octet-stream",
        "sha256": sha256,
        "entropy": entropy,
        "indicators": indicators,
        "score": score,
        "severity": severity,
        "verdict": verdict,
    }
