from __future__ import annotations

from typing import Any, Dict
import math

CHANGE_LIMITS = {
    "Height": 2.0,     
    "Speed": 2.5,      
    "Pitch": 10.0,      
    "Roll": 10.0,       
    "Yaw": 45.0,       
    "Battery": 1.0,     
}

VALID_RANGES = {
    "Battery": (0.0, 100.0),
    "Height": (0.0, 30.0),
    "Speed": (0.0, 12.0),
    "Pitch": (-90.0, 90.0),
    "Roll": (-90.0, 90.0),
    "Yaw": (0.0, 360.0),
}

SEVERITY_ORDER = {
    "None": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

def _number(value: Any) -> float | None:

    try:

        number = float(value)

        if math.isfinite(number):
            return number

        return None

    except (TypeError, ValueError):

        return None

def _yaw_difference(
    current: float,
    previous: float
) -> float:

    difference = abs(current - previous)

    return min(
        difference,
        360.0 - difference
    )

def detect(
    current_packet: Dict[str, Any],
    previous_packet: Dict[str, Any] | None
) -> Dict[str, Any]:

    if previous_packet is None:

        return {
            "detected": False,
            "threat": "Noise / Sensor Anomaly",
            "severity": "None",
            "reason": "No previous packet available for comparison",
        }

    issues = []
    severity = "None"

    for field, limit in CHANGE_LIMITS.items():

        current = _number(
            current_packet.get(field)
        )

        previous = _number(
            previous_packet.get(field)
        )

        if current is None or previous is None:
            continue

        minimum, maximum = VALID_RANGES[field]

        if not (
            minimum <= current <= maximum
        ):
            continue

        if field == "Yaw":

            change = _yaw_difference(
                current,
                previous
            )

        else:

            change = abs(
                current - previous
            )

        if change > limit:

            if change > limit * 2:

                level = "High"

            else:

                level = "Medium"


            issues.append(
                f"Sudden {field} change: "
                f"{change:.2f} "
                f"(limit {limit:.2f})"
            )


            if (
                SEVERITY_ORDER[level]
                > SEVERITY_ORDER[severity]
            ):

                severity = level

    return {

        "detected": bool(issues),

        "threat": "Noise / Sensor Anomaly",

        "severity": severity,

        "reason": (
            "; ".join(issues)
            if issues
            else "No sensor anomaly detected"
        ),
    }

__all__ = [
    "detect",
    "CHANGE_LIMITS",
]