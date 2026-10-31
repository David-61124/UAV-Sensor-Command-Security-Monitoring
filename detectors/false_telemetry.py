from __future__ import annotations

from typing import Any, Dict, List
import math

LIMITS = {
    "Battery": (0.0, 100.0),
    "Height": (0.0, 30.0),
    "Speed": (0.0, 12.0),
    "Pitch": (-90.0, 90.0),
    "Roll": (-90.0, 90.0),
    "Yaw": (0.0, 360.0),
}
SEVERITY_ORDER = {"None": 0, "Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def _number(value: Any) -> float | None:
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def detect(row: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    severity = "None"

    def add(reason: str, level: str) -> None:
        nonlocal severity
        issues.append(reason)
        if SEVERITY_ORDER[level] > SEVERITY_ORDER[severity]:
            severity = level

    numeric: Dict[str, float | None] = {}
    for field in LIMITS:
        if field not in row:
            add(f"Missing telemetry field: {field}", "Critical")
            numeric[field] = None
            continue
        value = _number(row[field])
        numeric[field] = value
        if value is None:
            add(f"Invalid non-numeric value for {field}: {row[field]}", "High")

    for field, (minimum, maximum) in LIMITS.items():
        value = numeric[field]
        if value is not None and (value < minimum or value > maximum):
            level = "Critical" if field in {"Height", "Speed"} else "High"
            add(f"Impossible {field}: {value:g} (allowed {minimum:g} to {maximum:g})", level)

    height, speed = numeric["Height"], numeric["Speed"]
    pitch, roll = numeric["Pitch"], numeric["Roll"]
    if height is not None and speed is not None and height == 0 and speed > 10:
        add("Height is 0 m while speed is above 10 m/s", "High")
    if pitch is not None and roll is not None and abs(pitch) > 80 and abs(roll) > 80:
        add("Pitch and roll are simultaneously near their physical limits", "High")

    return {
        "detected": bool(issues),
        "threat": "False Telemetry",
        "severity": severity,
        "reason": "; ".join(issues)
        if issues
        else "No false telemetry detected",
    }

__all__ = ["detect", "LIMITS"]
