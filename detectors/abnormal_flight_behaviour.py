from __future__ import annotations

from typing import Any, Dict
import math

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

def detect(
    current_packet: Dict[str, Any],
    previous_packet: Dict[str, Any] | None = None
) -> Dict[str, Any]:

    issues = []
    severity = "None"

    def add_issue(reason: str, level: str):

        nonlocal severity

        issues.append(reason)

        if (
            SEVERITY_ORDER[level]
            > SEVERITY_ORDER[severity]
        ):

            severity = level

    speed = _number(
        current_packet.get("Speed")
    )

    height = _number(
        current_packet.get("Height")
    )

    pitch = _number(
        current_packet.get("Pitch")
    )

    roll = _number(
        current_packet.get("Roll")
    )

    if (
        speed is not None
        and pitch is not None
        and speed > 8
        and abs(pitch) > 35
    ):

        add_issue(
            f"High-speed flight with extreme pitch "
            f"(speed={speed:.2f} m/s, "
            f"pitch={pitch:.2f}°)",
            "High"
        )

    if (
        speed is not None
        and roll is not None
        and speed > 8
        and abs(roll) > 35
    ):

        add_issue(
            f"High-speed flight with extreme roll "
            f"(speed={speed:.2f} m/s, "
            f"roll={roll:.2f}°)",
            "High"
        )

    if (
        speed is not None
        and height is not None
        and speed > 8
        and height > 20
    ):

        add_issue(
            f"High-speed flight at high altitude "
            f"(speed={speed:.2f} m/s, "
            f"height={height:.2f} m)",
            "Medium"
        )

    if (
        pitch is not None
        and roll is not None
        and abs(pitch) > 35
        and abs(roll) > 35
    ):

        add_issue(
            f"Aggressive flight attitude "
            f"(pitch={pitch:.2f}°, "
            f"roll={roll:.2f}°)",
            "High"
        )

    if (
        speed is not None
        and pitch is not None
        and roll is not None
        and speed > 6
        and (
            abs(pitch) > 30
            or abs(roll) > 30
        )
    ):

        add_issue(
            f"Aggressive high-speed manoeuvre "
            f"(speed={speed:.2f} m/s)",
            "Medium"
        )

    return {

        "detected": bool(issues),

        "threat": "Abnormal Flight Behaviour",

        "severity": severity,

        "reason": (
            "; ".join(issues)
            if issues
            else "Normal flight behaviour"
        )
    }

__all__ = ["detect"]