from __future__ import annotations

from typing import Any, Dict

AUTHORIZED_COMMANDS = {
    "TAKEOFF",
    "LAND",
    "HOVER",
    "MOVE",
    "ROTATE",
    "RETURN_HOME",
}

SEVERITY_ORDER = {
    "None": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

def detect(
    current_packet: Dict[str, Any]
) -> Dict[str, Any]:

    command = str(
        current_packet.get("Command", "")
    ).strip().upper()

    source = str(
        current_packet.get("Command_Source", "")
    ).strip().upper()

    authorized = str(
        current_packet.get("Command_Authorized", "")
    ).strip().lower()

    if not command or command in {"NONE", "NORMAL"}:

        return {
            "detected": False,
            "threat": "Unauthorized Command",
            "severity": "None",
            "reason": "No command requiring authorization was received",
        }

    if command not in AUTHORIZED_COMMANDS:

        return {
            "detected": True,
            "threat": "Unauthorized Command",
            "severity": "High",
            "reason": (
                f"Unknown command '{command}' "
                f"was received from source '{source or 'UNKNOWN'}'"
            ),
        }

    if authorized not in {
        "true",
        "1",
        "yes"
    }:

        return {
            "detected": True,
            "threat": "Unauthorized Command",
            "severity": "High",
            "reason": (
                f"Valid command '{command}' was received "
                f"without legitimate authorization "
                f"(source: {source or 'UNKNOWN'})"
            ),
        }

    return {
        "detected": False,
        "threat": "Unauthorized Command",
        "severity": "None",
        "reason": (
            f"Command '{command}' was legitimately authorized "
            f"by source '{source or 'UNKNOWN'}'"
        ),
    }

__all__ = [
    "detect",
    "AUTHORIZED_COMMANDS",
]