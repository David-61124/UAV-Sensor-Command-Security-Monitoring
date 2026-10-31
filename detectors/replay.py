def detect_replay(current_packet, previous_packet):

    if previous_packet is None:

        return {
            "detected": False,
            "threat": "None",
            "reason": "No previous packet available",
            "severity": "None"
        }

    fields_to_compare = [
        "Battery",
        "Height",
        "Speed",
        "Pitch",
        "Roll",
        "Yaw",
        "Flight_Time"
    ]

    identical = True

    for field in fields_to_compare:

        if current_packet.get(field) != previous_packet.get(field):

            identical = False
            break

    if identical:

        return {
            "detected": True,
            "threat": "Replay Attack",
            "reason": "Current packet contains identical telemetry to the previous packet",
            "severity": "High"
        }

    return {
        "detected": False,
        "threat": "None",
        "reason": "No replay detected",
        "severity": "None"
    }
